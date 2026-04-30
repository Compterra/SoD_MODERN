#!/usr/bin/env python3
"""printc.py - tiny colored echo utility for the modular build chain.

Why this exists:
- Windows cmd has historically been inconsistent with ANSI colors.
- colorama makes colored output reliable.

Respects:
- NO_COLOR=1 environment variable to disable color.

Examples:
  python build/tools/printc.py title "Modular Overhaul"
  python build/tools/printc.py step  "Building fragments -> compile/"
"""

from __future__ import annotations

import argparse
import os
import sys

# Vendor colorama so contributors don't need pip.
_VENDOR_ROOT = os.path.join(os.path.dirname(__file__), "_vendor")
if _VENDOR_ROOT not in sys.path:
    sys.path.insert(0, _VENDOR_ROOT)

try:
    from colorama import init as _c_init
    from colorama import Fore as _F
    from colorama import Style as _S
except Exception:
    _c_init = None
    _F = _S = None


def _colors_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    # If colorama import failed, fall back to plain.
    return _c_init is not None


def _style_map():
    # Keep styles conservative/readable.
    if not _colors_enabled():
        return {}
    return {
        "title": _F.CYAN + _S.BRIGHT,
        "version": _F.CYAN,
        "step": _F.MAGENTA + _S.BRIGHT,
        "substep": _F.MAGENTA,
        "info": _F.WHITE + _S.BRIGHT,
        "ok": _F.GREEN + _S.BRIGHT,
        "warn": _F.YELLOW + _S.BRIGHT,
        "error": _F.RED + _S.BRIGHT,
        "doctor": _F.CYAN,
        "tag": _F.BLUE + _S.BRIGHT,
        "dim": _S.DIM,
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("style")
    ap.add_argument("message", nargs=argparse.REMAINDER)
    ns = ap.parse_args(argv)

    msg = " ".join(ns.message).strip()
    style = (ns.style or "info").lower()

    if _colors_enabled():
        _c_init()  # safe to call multiple times
        sm = _style_map()
        prefix = sm.get(style, "")
        reset = _S.RESET_ALL if prefix else ""
        sys.stdout.write(f"{prefix}{msg}{reset}\n")
    else:
        sys.stdout.write(msg + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
