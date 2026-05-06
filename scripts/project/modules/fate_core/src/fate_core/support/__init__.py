"""支撑工具模块。"""

from .branding import (
    append_branding_markdown,
    append_branding_text,
    attach_branding,
    build_brand_footer_markdown,
    build_brand_footer_text,
    build_branding_markdown,
    build_branding_text,
    build_disclaimer_markdown,
    build_disclaimer_text,
    get_branding_payload,
    get_disclaimer_payload,
    load_branding,
)
from .paths import FATE_PROFILE_DIR, FATE_REPO_ROOT, TELEGRAM_SRC_DIR

__all__ = [
    "append_branding_markdown",
    "append_branding_text",
    "attach_branding",
    "build_brand_footer_markdown",
    "build_brand_footer_text",
    "build_branding_markdown",
    "build_branding_text",
    "build_disclaimer_markdown",
    "build_disclaimer_text",
    "FATE_PROFILE_DIR",
    "FATE_REPO_ROOT",
    "TELEGRAM_SRC_DIR",
    "get_branding_payload",
    "get_disclaimer_payload",
    "load_branding",
]
