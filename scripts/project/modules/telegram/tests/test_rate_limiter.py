#!/usr/bin/env python3
"""测试请求限流配置已移除用户冷却与每日上限。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import rate_limiter


def test_record_request_no_longer_blocks_follow_up_requests(monkeypatch):
    monkeypatch.setattr(rate_limiter, "_queue_size", 0)

    rate_limiter.record_request(12345)
    allowed, reason = rate_limiter.check_rate_limit(12345)

    assert allowed is True
    assert reason == ""


def test_queue_limit_still_blocks_when_queue_full(monkeypatch):
    monkeypatch.setattr(rate_limiter, "_queue_size", rate_limiter.QUEUE_MAX_SIZE)

    allowed, reason = rate_limiter.check_rate_limit(12345)

    assert allowed is False
    assert "服务器繁忙" in reason
