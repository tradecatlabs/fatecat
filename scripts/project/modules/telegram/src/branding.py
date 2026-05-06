from __future__ import annotations

import sys

from _paths import FATE_CORE_SRC_DIR

if str(FATE_CORE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC_DIR))

from fate_core.support.branding import (  # noqa: E402
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
    "get_branding_payload",
    "get_disclaimer_payload",
    "load_branding",
]
