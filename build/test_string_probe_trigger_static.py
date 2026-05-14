# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError(f"Unexpected stale token: {needle}")


def main() -> int:
    trigger = read("src/triggers/ST02_every_hour/entry_0173_string_probe.py")
    order = read("src/triggers/_order_simple_triggers.txt")
    doctor = read("build/doctor.py")

    assert_contains(order, "ST02_every_hour/entry_0173_string_probe.py")
    assert_contains(doctor, "entry_0173_string_probe.py")
    assert_contains(doctor, "runtime experiment")
    assert_contains(trigger, "(2,")
    assert_contains(trigger, '(eq, "$g_sod_debug", 1)')
    assert_contains(trigger, "$g_sod_string_probe_page")
    assert_contains(trigger, '(ge, "$g_sod_string_probe_page", 11)')
    for reg_no in range(0, 68):
        assert_contains(trigger, f"(str_store_string, s{reg_no}, \"@{reg_no:02d}\"),")
    for reg_no in range(68, 100):
        assert_contains(trigger, f"(str_store_string, s{reg_no}, \"@{reg_no}\"),")
    for reg_no in range(100, 128):
        assert_contains(trigger, f"(str_store_string, {reg_no}, \"@{reg_no}\"),")
    for reg_no in range(100, 128):
        scratch = reg_no - 100
        if reg_no >= 108:
            scratch = reg_no - 108
        if reg_no >= 120:
            scratch = reg_no - 120
        assert_contains(trigger, f"(str_store_string_reg, s{scratch}, {reg_no}),")
    for label in (
        "s00-s11",
        "s12-s23",
        "s24-s35",
        "s36-s47",
        "s48-s59",
        "s60-s71",
        "s72-s83",
        "s84-s95",
        "s96-s99 direct",
        "s100-s107 copy",
        "s108-s119 copy",
        "s120-s127 copy",
    ):
        assert_contains(trigger, f"String Probe {label}:")
    assert_contains(trigger, "{s0}, {s1}, {s2}, {s3}, {s4}, {s5}, {s6}, {s7}, {s8}, {s9}, {s10}, {s11}")
    assert_contains(trigger, "{s96}, {s97}, {s98}, {s99}")
    for reg_no in range(100, 128):
        assert_not_contains(trigger, f"{{s{reg_no}}}")
    assert_contains(trigger, "String Probe s120-s127 copy: {s0}, {s1}, {s2}, {s3}, {s4}, {s5}, {s6}, {s7}")
    print("[string_probe_trigger_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
