from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Event
from types import SimpleNamespace

from fate_core.adapters import ziwei_iztro


class _TimeAnchor:
    def __init__(self, birth_dt: datetime, *_args, **_kwargs) -> None:
        self.birth_dt = birth_dt
        self.calc_dt = birth_dt
        self.true_solar_time = birth_dt
        self.zi_time_analysis = {"timeZhi": "辰"}
        self.true_solar_detail = {"totalOffsetMinutes": 0}

    def _get_birth_info(self) -> dict[str, str]:
        return {"solar": self.birth_dt.strftime("%Y-%m-%d %H:%M:%S")}


def test_concurrent_ziwei_calculation_does_not_replace_process_stdout(monkeypatch) -> None:
    first_inside = Event()
    second_inside = Event()
    release_second = Event()

    class FakeFortelZiweiCalculator:
        def __init__(self, _birth_dt: datetime, _gender: str, longitude: float) -> None:
            self.longitude = longitude

        def calculate_professional_ziwei(self, *, as_of: datetime) -> dict:
            if self.longitude == 116.0:
                first_inside.set()
                assert second_inside.wait(timeout=2)
            else:
                second_inside.set()
                assert first_inside.wait(timeout=2)
                assert release_second.wait(timeout=2)
            chart = {"palaces": [], "fiveElementsClass": "木三局", "solarDate": "1990-01-01"}
            return {"professionalZiwei": chart, "horoscope": {"asOf": as_of.isoformat()}}

    monkeypatch.setattr(ziwei_iztro, "BaziCalculator", _TimeAnchor)
    monkeypatch.setattr(ziwei_iztro, "FortelZiweiCalculator", FakeFortelZiweiCalculator)
    monkeypatch.setattr(ziwei_iztro, "now_cn", lambda: datetime(2026, 7, 13, 12, 0, 0))

    initial_stdout = sys.stdout
    payload = SimpleNamespace(
        birth_dt=datetime(1990, 1, 1, 8, 0, 0),
        gender="male",
        latitude=39.9042,
        name="测试用户",
        birth_place="北京市",
        use_true_solar_time=True,
        as_of=datetime(2026, 7, 13, 12, 0, 0),
    )

    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(
            ziwei_iztro.calculate_ziwei_iztro,
            SimpleNamespace(**vars(payload), longitude=116.0),
        )
        second = executor.submit(
            ziwei_iztro.calculate_ziwei_iztro,
            SimpleNamespace(**vars(payload), longitude=117.0),
        )
        first_result = first.result(timeout=3)
        release_second.set()
        second_result = second.result(timeout=3)

    assert sys.stdout is initial_stdout
    assert first_result["ziweiChart"] == second_result["ziweiChart"]
    assert first_result["ziweiHoroscope"] == second_result["ziweiHoroscope"]
