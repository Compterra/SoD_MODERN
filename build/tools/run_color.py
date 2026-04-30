#!/usr/bin/env python3
"""run_color.py - run a python script and colorize its output.

This wrapper is intentionally simple and self-contained:
- Runs target script in-process via runpy (so PYTHONPATH from .bat applies).
- Wraps stdout/stderr so lines can be colorized by pattern.
- Returns the target script's exit code.

Respects NO_COLOR=1 to disable color.

Usage:
  python build/tools/run_color.py path\\to\\script.py [-- arg1 arg2]
"""

from __future__ import annotations

import argparse
import os
import re
import runpy
import sys
from typing import Optional

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
    return _c_init is not None


def _wrap(style: str, text: str) -> str:
    if not _colors_enabled():
        return text
    return style + text + _S.RESET_ALL


# Patterns tuned for your build output.
_PATTERNS = [
    (re.compile(r"^\[doctor\]"), "doctor"),
    (re.compile(r"^\[build_[^\]]+\]"), "tag"),
    (re.compile(r"\b(fatal mod error|fatal error)\b", re.I), "error"),
    (re.compile(r"\b(error|failed|traceback)\b", re.I), "error"),
    (re.compile(r"\b(warn|warning)\b", re.I), "warn"),
    (re.compile(r"\b(ok:)\b", re.I), "ok"),
    (re.compile(r"\bwrote\b", re.I), "ok"),
    (re.compile(r"\bnote:\b", re.I), "info"),
]


def _style_map():
    if not _colors_enabled():
        return {}
    return {
        "doctor": _F.CYAN,
        "tag": _F.BLUE + _S.BRIGHT,
        "ok": _F.GREEN + _S.BRIGHT,
        "warn": _F.YELLOW + _S.BRIGHT,
        "error": _F.RED + _S.BRIGHT,
        "info": _F.WHITE + _S.DIM,
        "plain": "",
    }


class _LineBufferWriter:
    """Buffers partial writes into full lines, then colorizes."""

    _FAIL_RE = re.compile(r"^(?:Error:|ERROR:|Traceback\b)|\b(?:Build failed|FAIL:|Illegal Identifier)\b", re.I)

    def __init__(self, underlying):
        self._u = underlying
        self._buf = ""
        self._styles = _style_map()
        self.saw_failure = False

    def write(self, s: str):
        if not s:
            return
        self._buf += s
        while True:
            idx = self._buf.find("\n")
            if idx == -1:
                break
            line = self._buf[: idx + 1]
            self._buf = self._buf[idx + 1 :]
            self._write_line(line)

    def flush(self):
        if self._buf:
            self._write_line(self._buf)
            self._buf = ""
        try:
            self._u.flush()
        except Exception:
            pass

    def _pick_style_key(self, line: str) -> str:
        raw = line.rstrip("\r\n")
        for rx, key in _PATTERNS:
            if rx.search(raw):
                return key
        return "plain"

    def _write_line(self, line: str):
        if self._FAIL_RE.search(line.rstrip("\r\n")):
            self.saw_failure = True
        key = self._pick_style_key(line)
        style = self._styles.get(key, "")
        if style:
            self._u.write(_wrap(style, line.rstrip("\r\n")) + "\n")
        else:
            self._u.write(line)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("script")
    ap.add_argument("args", nargs=argparse.REMAINDER)
    ns = ap.parse_args(argv)

    if _colors_enabled():
        _c_init(autoreset=True)

    script_path = ns.script
    # Support "--" separator: python run_color.py script.py -- arg1 arg2
    args = ns.args
    if args and args[0] == "--":
        args = args[1:]

    # Make script path absolute for nicer tracebacks.
    script_path = os.path.abspath(script_path)

    # Ensure the target script can import its sibling modules.
    # Example: build/build_all.py imports doctor.py and other build_*.py next to it.
    script_dir = os.path.dirname(script_path)
    if script_dir and script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    # Also add the current working directory (project root in our .bat chain)
    # so scripts can do simple imports when run from the root.
    cwd = os.path.abspath(os.getcwd())
    if cwd and cwd not in sys.path:
        sys.path.insert(0, cwd)

    # Redirect stdout/stderr with line buffering.
    orig_out, orig_err = sys.stdout, sys.stderr
    wrapped_out = _LineBufferWriter(orig_out)
    wrapped_err = _LineBufferWriter(orig_err)
    sys.stdout = wrapped_out  # type: ignore
    sys.stderr = wrapped_err  # type: ignore

    # Prepare argv for the target script.
    old_argv = sys.argv
    sys.argv = [script_path] + args

    try:
        runpy.run_path(script_path, run_name="__main__")
        return 1 if wrapped_out.saw_failure or wrapped_err.saw_failure else 0
    except SystemExit as e:
        # Normalize sys.exit() values.
        code = e.code
        if code is None:
            return 1 if wrapped_out.saw_failure or wrapped_err.saw_failure else 0
        if isinstance(code, int):
            if code == 0 and (wrapped_out.saw_failure or wrapped_err.saw_failure):
                return 1
            return code
        # Non-int exits treated as error.
        return 1
    finally:
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception:
            pass
        sys.stdout, sys.stderr = orig_out, orig_err
        sys.argv = old_argv


if __name__ == "__main__":
    raise SystemExit(main())
