from __future__ import annotations

import json
import os
import urllib.request


def call_almanac(base_url: str) -> dict:
    payload = {
        "dateRange": {"start": "2026-05-08", "end": "2026-05-08"},
        "eventType": "出行",
        "place": "北京",
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/capabilities/almanac/calculate",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    api_url = os.getenv("FATECAT_API_URL", "http://127.0.0.1:8001")
    print(json.dumps(call_almanac(api_url), ensure_ascii=False, indent=2))
