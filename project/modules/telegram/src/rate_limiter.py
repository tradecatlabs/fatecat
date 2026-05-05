"""
请求限流与队列机制
- 全局并发限制
- 请求队列
"""

import asyncio
from functools import wraps

# ========== 配置 ==========
MAX_CONCURRENT = 1  # 最大同时计算数
QUEUE_MAX_SIZE = 9999  # 队列无限制

# ========== 状态 ==========
_semaphore = asyncio.Semaphore(MAX_CONCURRENT)
_queue_size = 0


def check_rate_limit(user_id: int) -> tuple[bool, str]:
    """
    检查用户是否可以发起请求
    返回: (是否允许, 拒绝原因)
    """
    global _queue_size

    # 检查队列
    if _queue_size >= QUEUE_MAX_SIZE:
        return False, "服务器繁忙，请稍后再试"

    return True, ""


def record_request(user_id: int):
    """兼容旧调用；当前不再做用户冷却/每日次数记录。"""
    return None


async def acquire_slot():
    """获取计算槽位"""
    global _queue_size
    _queue_size += 1
    await _semaphore.acquire()


def release_slot():
    """释放计算槽位"""
    global _queue_size
    _queue_size = max(0, _queue_size - 1)
    _semaphore.release()


def get_queue_status() -> dict:
    """获取队列状态"""
    return {
        "concurrent": MAX_CONCURRENT - _semaphore._value,
        "max_concurrent": MAX_CONCURRENT,
        "queue_size": _queue_size,
        "queue_max": QUEUE_MAX_SIZE,
    }


def rate_limit(func):
    """装饰器：自动限流"""

    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id

        allowed, reason = check_rate_limit(user_id)
        if not allowed:
            await update.message.reply_text(f"⏳ {reason}")
            return

        record_request(user_id)

        try:
            await acquire_slot()
            return await func(update, context, *args, **kwargs)
        finally:
            release_slot()

    return wrapper
