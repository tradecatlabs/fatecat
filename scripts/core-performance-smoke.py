#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fate_core.capabilities import CapabilityExecutor, CapabilityInput

SAMPLE_PAYLOAD = {
    "birthDateTime": "1990-01-01 08:00:00",
    "gender": "male",
    "longitude": 116.4074,
    "latitude": 39.9042,
    "birthPlace": "北京市",
    "name": "性能样本",
    "useTrueSolarTime": True,
}


def percentile(values: list[float], ratio: float) -> float:
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, round((len(ordered) - 1) * ratio)))
    return ordered[index]


def benchmark(capability_id: str, *, samples: int, budget_ms: float) -> dict[str, Any]:
    executor = CapabilityExecutor()
    request = CapabilityInput(capability_id=capability_id, payload=dict(SAMPLE_PAYLOAD))
    executor.execute(request)
    durations: list[float] = []
    output_fields: list[str] = []
    for _ in range(samples):
        started = time.perf_counter()
        result = executor.execute(request)
        durations.append((time.perf_counter() - started) * 1000)
        output_fields = sorted(result.data)
    p95_ms = percentile(durations, 0.95)
    return {
        "capabilityId": capability_id,
        "samples": samples,
        "meanMs": round(statistics.fmean(durations), 3),
        "p95Ms": round(p95_ms, 3),
        "maxMs": round(max(durations), 3),
        "budgetMs": budget_ms,
        "status": "passed" if p95_ms <= budget_ms else "failed",
        "outputFieldCount": len(output_fields),
        "outputFields": output_fields,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="FateCat core warm-path performance smoke")
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--output-json", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.samples < 1 or args.samples > 20:
        raise SystemExit("--samples 必须在 1-20 之间")
    budgets = {
        "bazi": float(os.getenv("FATECAT_BAZI_WARM_P95_BUDGET_MS", "2000")),
        "ziwei": float(os.getenv("FATECAT_ZIWEI_WARM_P95_BUDGET_MS", "2000")),
    }
    results = [
        benchmark(capability_id, samples=args.samples, budget_ms=budget) for capability_id, budget in budgets.items()
    ]
    status = "passed" if all(item["status"] == "passed" for item in results) else "failed"
    payload = {
        "schemaVersion": 1,
        "kind": "fatecat.core_performance_smoke",
        "generatedAt": datetime.now(UTC).isoformat(),
        "status": status,
        "measurement": "single-process warm wall-clock; not production p95/p99 evidence",
        "results": results,
        "privacyBoundary": "Uses only the fixed Beijing performance fixture; no user input or report body is stored.",
    }
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output_json:
        output_path = Path(args.output_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
