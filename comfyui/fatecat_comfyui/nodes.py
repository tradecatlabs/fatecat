from __future__ import annotations

import asyncio
import threading
from typing import Any

from . import core

try:
    from comfy_api.latest import InputImpl

    _HAS_COMFY = True
except Exception:  # pragma: no cover - 非 ComfyUI 环境只加载核心逻辑
    InputImpl = None
    _HAS_COMFY = False


class _ComfyUIProgressReporter:
    def __init__(self, node_id: str | None = None) -> None:
        self._node_id = node_id
        self._api: Any = None
        if _HAS_COMFY:
            try:
                from comfy_api.latest import ComfyAPI

                self._api = ComfyAPI()
            except Exception:
                self._api = None

    def __call__(self, message: str, current: int, total: int) -> None:
        del message
        if self._api is None:
            return
        try:
            asyncio.run(
                self._api.execution.set_progress(
                    float(current),
                    float(total),
                    node_id=self._node_id,
                )
            )
        except Exception:
            return


def _current_comfy_node_id() -> str | None:
    if not _HAS_COMFY:
        return None
    try:
        from comfy_execution.utils import get_executing_context

        context = get_executing_context()
        return context.node_id if context is not None else None
    except Exception:
        return None


def _comfy_cancel_check() -> bool:
    if not _HAS_COMFY:
        return False
    try:
        from comfy.model_management import processing_interrupted

        return bool(processing_interrupted())
    except Exception:
        return False


def _report_widgets() -> dict[str, Any]:
    return {
        "birth_date": ("STRING", {"default": core.default_birth_date()}),
        "birth_time": ("STRING", {"default": core.default_birth_time()}),
        "birth_place": ("STRING", {"default": core.default_birth_place()}),
        "location_id": ("STRING", {"default": ""}),
        "gender": (["male", "female"], {"default": "male"}),
        "report_system": (core.report_system_options(), {"default": "bazi"}),
        "name": ("STRING", {"default": core.default_name()}),
        "time_basis": (core.time_basis_options(), {"default": "beijing_time"}),
        "fold_choice": (["", "earlier", "later"], {"default": ""}),
    }


class FateCatValidate:
    CATEGORY = "TradeCat/FateCat"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {"required": dict(_report_widgets())}

    RETURN_TYPES = ("STRING", "INT", "BOOLEAN", "STRING")
    RETURN_NAMES = ("title", "count", "valid", "message")
    FUNCTION = "validate"

    def validate(
        self,
        birth_date: str,
        birth_time: str,
        birth_place: str,
        location_id: str,
        gender: str,
        report_system: str,
        name: str,
        time_basis: str,
        fold_choice: str,
    ) -> tuple[str, int, bool, str]:
        result = core.validate_from_inputs(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=birth_place,
            location_id=location_id,
            gender=gender,
            report_system=report_system,
            name=name,
            time_basis=time_basis,
            fold_choice=fold_choice,
        )
        return (
            str(result["title"]),
            int(result["count"]),
            bool(result["valid"]),
            str(result["message"]),
        )


class FateCatProduce:
    CATEGORY = "TradeCat/FateCat"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {"required": dict(_report_widgets())}

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("run_id", "markdown_path", "manifest_path", "markdown")
    FUNCTION = "produce"

    def produce(
        self,
        birth_date: str,
        birth_time: str,
        birth_place: str,
        location_id: str,
        gender: str,
        report_system: str,
        name: str,
        time_basis: str,
        fold_choice: str,
    ) -> tuple[str, str, str, str]:
        node_id = _current_comfy_node_id()
        progress_reporter = _ComfyUIProgressReporter(node_id)
        result = _run_in_thread(
            core.produce_from_inputs,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=birth_place,
            location_id=location_id,
            gender=gender,
            report_system=report_system,
            name=name,
            time_basis=time_basis,
            fold_choice=fold_choice,
            progress_callback=progress_reporter,
            cancel_check=_comfy_cancel_check,
        )
        return (
            str(result["run_id"]),
            str(result["markdown_path"]),
            str(result["manifest_path"]),
            str(result["markdown"]),
        )


class FateCatPreview:
    CATEGORY = "TradeCat/FateCat"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {"required": dict(_report_widgets())}

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "preview_path")
    FUNCTION = "preview"

    def preview(
        self,
        birth_date: str,
        birth_time: str,
        birth_place: str,
        location_id: str,
        gender: str,
        report_system: str,
        name: str,
        time_basis: str,
        fold_choice: str,
    ) -> tuple[Any, str]:
        result = _run_in_thread(
            core.render_preview_image,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_place=birth_place,
            location_id=location_id,
            gender=gender,
            report_system=report_system,
            name=name,
            time_basis=time_basis,
            fold_choice=fold_choice,
        )
        image = _load_image_tensor(result["preview_path_wsl"])
        return image, str(result["preview_path"])


NODE_CLASS_MAPPINGS = {
    "FateCatValidate": FateCatValidate,
    "FateCatProduce": FateCatProduce,
    "FateCatPreview": FateCatPreview,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FateCatValidate": "FateCat Validate",
    "FateCatProduce": "FateCat Produce",
    "FateCatPreview": "FateCat Preview",
}


def _load_image_tensor(path: str) -> Any:
    import numpy as np
    import torch
    from PIL import Image

    with Image.open(path).convert("RGB") as image:
        array = np.asarray(image, dtype=np.float32) / 255.0
    return torch.from_numpy(array).unsqueeze(0)


def _run_in_thread(function: Any, *args: Any, **kwargs: Any) -> Any:
    outputs: list[Any] = []
    errors: list[BaseException] = []

    def worker() -> None:
        try:
            outputs.append(function(*args, **kwargs))
        except BaseException as exc:  # noqa: BLE001 - 需要原样抛回 ComfyUI
            if _HAS_COMFY and isinstance(exc, core.ProductionCancelled):
                try:
                    from comfy.model_management import InterruptProcessingException

                    errors.append(InterruptProcessingException(str(exc)))
                    return
                except Exception:
                    pass
            errors.append(exc)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    thread.join()
    if errors:
        raise errors[0]
    return outputs[0]
