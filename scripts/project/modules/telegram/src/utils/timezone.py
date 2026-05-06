from datetime import datetime
from zoneinfo import ZoneInfo

# 固定北京时间（UTC+8）作为全局唯一时区
CN_TZ = ZoneInfo("Asia/Shanghai")


def now_cn() -> datetime:
    """返回带时区的当前北京时间"""
    return datetime.now(CN_TZ)


def ensure_cn(dt: datetime) -> datetime:
    """将任意 datetime 规范为北京时间"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=CN_TZ)
    return dt.astimezone(CN_TZ)


def fmt_cn(dt: datetime, fmt: str = "%Y-%m-%d %H:%M") -> str:
    """格式化为北京时间字符串"""
    return ensure_cn(dt).strftime(fmt)
