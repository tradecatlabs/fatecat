from __future__ import annotations

import json
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


class FateCatClientError(RuntimeError):
    """FateCat 客户端基础异常。"""


class FateCatTransportError(FateCatClientError):
    """网络、协议或响应格式错误。"""


class FateCatAPIError(FateCatClientError):
    """服务端返回非成功 HTTP 状态。"""

    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(f"FateCat API request failed with HTTP {status_code}")


class FateCatClient:
    """无运行依赖的 FateCat 远程 HTTP API 客户端。"""

    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        timeout_seconds: float = 30.0,
        max_response_bytes: int = 10 * 1024 * 1024,
    ) -> None:
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.query or parsed.fragment:
            raise ValueError("base_url 必须是无 query/fragment 的 http(s) URL")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds 必须大于 0")
        if max_response_bytes <= 0:
            raise ValueError("max_response_bytes 必须大于 0")
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout_seconds = float(timeout_seconds)
        self.max_response_bytes = int(max_response_bytes)

    def health(self) -> dict[str, Any]:
        return self._request_json("GET", "/health")

    def capabilities(self) -> dict[str, Any]:
        return self._request_json("GET", "/capabilities")

    def calculate(self, capability_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        capability_id = _validate_identifier("capability_id", capability_id)
        return self._request_json("POST", f"/capabilities/{capability_id}/calculate", payload)

    def create_report_job(self, payload: dict[str, Any], *, web: bool = False) -> dict[str, Any]:
        path = "/api/v1/report/jobs/web" if web else "/api/v1/report/jobs"
        return self._request_json("POST", path, payload)

    def get_report_job(self, job_id: str) -> dict[str, Any]:
        job_id = _validate_identifier("job_id", job_id)
        return self._request_json("GET", f"/api/v1/report/jobs/{job_id}")

    def _request_json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("path 必须是站内绝对路径")
        headers = {
            "Accept": "application/json",
            "User-Agent": "fatecat-client/0.1.0",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        body = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        request = Request(f"{self.base_url}{path}", data=body, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310
                response_body = response.read(self.max_response_bytes + 1)
        except HTTPError as exc:
            error_body = exc.read(64 * 1024).decode("utf-8", errors="replace")
            raise FateCatAPIError(exc.code, error_body) from exc
        except (OSError, URLError) as exc:
            raise FateCatTransportError(str(exc)) from exc
        if len(response_body) > self.max_response_bytes:
            raise FateCatTransportError("响应超过 max_response_bytes")
        try:
            decoded = json.loads(response_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise FateCatTransportError("服务端响应不是有效 UTF-8 JSON") from exc
        if not isinstance(decoded, dict):
            raise FateCatTransportError("服务端 JSON 顶层必须是 object")
        return decoded


def _validate_identifier(name: str, value: str) -> str:
    if not _IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError(f"{name} 格式无效")
    return value
