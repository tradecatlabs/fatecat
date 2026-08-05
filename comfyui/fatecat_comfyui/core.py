"""FateCat ComfyUI 节点核心逻辑（薄胶水）。

复用 fatecat 现有业务入口：`web_report_service.build_web_report_result`
完成 校验 -> 排盘计算 -> Markdown 生成；本模块只做参数解析、调用、
产物落盘与进度/取消桥接，不重新实现任何命理算法。
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

FATECAT_REPO_ENV = "FATECAT_REPO"
_RUNTIME_SUBDIR = Path("infra") / "runtime" / "local-state" / "comfyui"


class ProductionCancelled(Exception):
    """业务侧取消异常，由节点层转换为 ComfyUI InterruptProcessingException。"""


def _is_fatecat_root(candidate: Path) -> bool:
    return (candidate / "pyproject.toml").exists() and (candidate / "domains").is_dir()


def find_project_root() -> Path:
    configured = os.environ.get(FATECAT_REPO_ENV)
    if configured:
        candidate = Path(configured).resolve()
        if candidate.is_dir():
            return candidate
    current = Path(__file__).resolve()
    for candidate in [current, *current.parents]:
        if _is_fatecat_root(candidate):
            return candidate
    try:
        import fate_core

        current = Path(fate_core.__file__).resolve()
        for candidate in [current, *current.parents]:
            if _is_fatecat_root(candidate):
                return candidate
    except Exception:
        pass
    raise RuntimeError(f"无法定位 FateCat 仓库根目录，请设置 {FATECAT_REPO_ENV}")


def _src_dirs(project_root: Path) -> list[Path]:
    return [
        project_root / "domains" / "fate-analysis" / "services" / "fate-core" / "src",
        project_root / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src",
    ]


def _ensure_src_paths() -> Path:
    project_root = find_project_root()
    for src_dir in _src_dirs(project_root):
        resolved = str(src_dir.resolve())
        if resolved not in sys.path:
            sys.path.insert(0, resolved)
    return project_root


def _business() -> Any:
    _ensure_src_paths()
    from web_report_service import build_web_report_result  # noqa: F401

    return build_web_report_result


def _runtime_root(project_root: Path) -> Path:
    return project_root / _RUNTIME_SUBDIR


def _runs_dir(project_root: Path) -> Path:
    path = _runtime_root(project_root) / "runs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _manifests_dir(project_root: Path) -> Path:
    path = _runtime_root(project_root) / "manifests"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _previews_dir(project_root: Path) -> Path:
    path = _runtime_root(project_root) / "previews"
    path.mkdir(parents=True, exist_ok=True)
    return path


def new_run_id() -> str:
    return f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"


def default_birth_date() -> str:
    return "1990-01-01"


def default_birth_time() -> str:
    return "08:00"


def default_birth_place() -> str:
    return "北京"


def default_name() -> str:
    return ""


def report_system_options() -> list[str]:
    return ["bazi", "ziwei"]


def time_basis_options() -> list[str]:
    return ["beijing_time", "local_civil", "utc"]


def _form_from_inputs(
    *,
    birth_date: str,
    birth_time: str,
    birth_place: str,
    location_id: str,
    gender: str,
    report_system: str,
    name: str,
    time_basis: str,
    fold_choice: str,
) -> Any:
    _ensure_src_paths()
    from web_forms import WebReportForm

    return WebReportForm(
        birth_date=str(birth_date or "").strip(),
        birth_time=str(birth_time or "").strip(),
        birth_place=str(birth_place or "").strip(),
        location_mode="domestic",
        location_id=str(location_id or "").strip(),
        time_basis=str(time_basis or "beijing_time").strip() or "beijing_time",
        fold_choice=str(fold_choice or "").strip(),
        gender=str(gender or "").strip(),
        name=str(name or "").strip(),
        report_system=str(report_system or "bazi").strip() or "bazi",
        submitted=True,
    )


def _cancel_check_proxy(cancel_check: Callable[[], bool] | None) -> None:
    if cancel_check is not None and cancel_check():
        raise ProductionCancelled("用户取消")


def validate_from_inputs(
    *,
    birth_date: str,
    birth_time: str,
    birth_place: str,
    location_id: str = "",
    gender: str,
    report_system: str = "bazi",
    name: str = "",
    time_basis: str = "beijing_time",
    fold_choice: str = "",
) -> dict[str, Any]:
    """轻量校验：字段完整性、地区可解析、时间口径归一化，不生成报告。"""
    _ensure_src_paths()
    from prediction_systems import enabled_report_system_ids
    from web_report_service import validate_web_report_form

    title = str(name or "").strip() or "未命名命主"
    count = len(enabled_report_system_ids())
    form = _form_from_inputs(
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
    try:
        validate_web_report_form(form)
    except ValueError as exc:
        return {"title": title, "count": count, "valid": False, "message": str(exc)}
    except Exception as exc:  # noqa: BLE001 - 校验失败必须转成可读消息
        return {"title": title, "count": count, "valid": False, "message": f"校验异常：{exc}"}
    return {"title": title, "count": count, "valid": True, "message": "参数校验通过，可生成报告。"}


def produce_from_inputs(
    *,
    birth_date: str,
    birth_time: str,
    birth_place: str,
    location_id: str = "",
    gender: str,
    report_system: str = "bazi",
    name: str = "",
    time_basis: str = "beijing_time",
    fold_choice: str = "",
    progress_callback: Callable[[str, int, int], None] | None = None,
    cancel_check: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """一键生产：校验 -> 排盘计算 -> Markdown -> 落盘 report.md 与 manifest.json。"""
    project_root = _ensure_src_paths()
    form = _form_from_inputs(
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

    def progress(current: int, total: int) -> None:
        if progress_callback is not None:
            progress_callback("", current, total)

    _cancel_check_proxy(cancel_check)
    build_web_report_result = _business()
    progress(1, 5)
    _cancel_check_proxy(cancel_check)
    result = build_web_report_result(form)
    progress(2, 5)
    _cancel_check_proxy(cancel_check)
    progress(3, 5)

    run_id = new_run_id()
    report_path = _runs_dir(project_root) / run_id / "report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(result.markdown, encoding="utf-8")
    manifest_path = _manifests_dir(project_root) / f"{run_id}.json"
    manifest = {
        "run_id": run_id,
        "report_system": result.report_system,
        "report_system_label": result.report_system_label,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "inputs": {
            "birthDate": form.birth_date,
            "birthTime": form.birth_time,
            "birthPlace": form.birth_place,
            "locationId": form.location_id or None,
            "gender": form.gender,
            "reportSystem": form.report_system,
            "name": form.name or None,
            "timeBasis": form.time_basis,
            "foldChoice": form.fold_choice or None,
        },
        "resolvedLocation": {
            "locationId": result.resolved_location_id,
            "name": result.resolved_location_name,
            "timezone": result.resolved_timezone,
            "longitude": result.resolved_longitude,
            "latitude": result.resolved_latitude,
        },
        "reportPath": str(report_path),
        "markdownChars": len(result.markdown),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    progress(4, 5)
    _cancel_check_proxy(cancel_check)
    progress(5, 5)
    return {
        "run_id": run_id,
        "markdown_path": str(report_path),
        "manifest_path": str(manifest_path),
        "markdown": result.markdown,
    }


def _zh_font(size: int) -> Any:
    from PIL import ImageFont

    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
    ]
    for path in candidates:
        if Path(path).is_file():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _preview_lines(workbench: dict[str, Any], report_system: str) -> list[tuple[str, str]]:
    if report_system == "ziwei":
        lines: list[tuple[str, str]] = []
        for palace in workbench.get("palaces", []) if isinstance(workbench.get("palaces"), list) else []:
            if not isinstance(palace, dict):
                continue
            name = str(palace.get("name", ""))
            branch = str(palace.get("earthlyBranch", ""))
            stars = "、".join(
                str(star.get("name", "")) for star in palace.get("majorStars", []) if isinstance(star, dict)
            )
            marks = "命" if palace.get("isOriginalPalace") else ""
            marks += "身" if palace.get("isBodyPalace") else ""
            lines.append((f"{name} {branch} {marks}".strip(), stars))
        return lines

    pillars = workbench.get("fourPillars", {}) if isinstance(workbench.get("fourPillars"), dict) else {}
    lines = []
    for key, label in [("year", "年柱"), ("month", "月柱"), ("day", "日柱"), ("hour", "时柱")]:
        item = pillars.get(key, {}) if isinstance(pillars.get(key), dict) else {}
        lines.append((label, str(item.get("fullName", ""))))
    benchmark = workbench.get("baziBenchmark", {}) if isinstance(workbench.get("baziBenchmark"), dict) else {}
    strength = benchmark.get("strengthScore", {}) if isinstance(benchmark.get("strengthScore"), dict) else {}
    lines.append(("五行强弱", str(strength.get("summary", ""))))
    yongshen = workbench.get("yongShen", {}) if isinstance(workbench.get("yongShen"), dict) else {}
    yong = yongshen.get("yongShenName") or yongshen.get("name") or yongshen.get("yongShen", "")
    lines.append(("用神策略", str(yong or "-")))
    return lines


def render_preview_image(
    *,
    birth_date: str,
    birth_time: str,
    birth_place: str,
    location_id: str = "",
    gender: str,
    report_system: str = "bazi",
    name: str = "",
    time_basis: str = "beijing_time",
    fold_choice: str = "",
) -> dict[str, str]:
    """生产前静态预览：生成一张命盘简表 PNG，不写入正式 runs 目录。"""
    from PIL import Image, ImageDraw

    project_root = _ensure_src_paths()
    form = _form_from_inputs(
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
    build_web_report_result = _business()
    result = build_web_report_result(form)
    workbench = result.workbench if isinstance(result.workbench, dict) else {}

    title = str(name or "").strip() or "未命名命主"
    lines = _preview_lines(workbench, result.report_system)
    title_font = _zh_font(44)
    header_font = _zh_font(30)
    body_font = _zh_font(26)

    width = 1200
    line_height = 52
    header_height = 120
    height = header_height + len(lines) * line_height + 40
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((60, 40), f"{title}｜FateCat 命盘预览｜{result.report_system_label}", font=title_font, fill="black")
    draw.text(
        (60, 110),
        f"{form.birth_date} {form.birth_time}｜{form.birth_place}｜{form.gender}",
        font=header_font,
        fill="black",
    )
    for index, (key, value) in enumerate(lines):
        y = header_height + index * line_height
        draw.text((60, y), key, font=body_font, fill="black")
        draw.text((300, y), value, font=body_font, fill="black")

    preview_path = _previews_dir(project_root) / f"fatecat-preview-{new_run_id()}.png"
    image.save(preview_path)
    return {"preview_path": str(preview_path), "preview_path_wsl": str(preview_path)}
