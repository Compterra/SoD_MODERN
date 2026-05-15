from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_fief_management_presentation_uses_stable_display_strings() -> None:
    fief = read("src/presentations/0020_sod_fief_management/sod_fief_management.py")

    assert_contains(fief, "(str_store_string_reg, s68, s0)")
    assert_contains(fief, '(str_store_string, s68, "@you reckon")')
    assert_contains(fief, '(str_store_string, s68, "@{s33} reckons")')
    assert_contains(fief, '(str_store_string, s69, "@, for an estimated {reg12} week project")')
    assert_contains(fief, "highest engineer skill ({reg2}), {s68} that developing")
    assert_contains(fief, "labor per week{s69}.")
    assert_not_contains(fief, "{s0}")
    assert_not_contains(fief, "{reg3?you reckon:{s33} reckons}")
    assert_not_contains(fief, "{reg12?, for an estimated {reg12} week project:}")


def test_presentations_do_not_render_volatile_s0_directly() -> None:
    direct_s0_render = re.compile(r"\b(?:create_text_overlay|overlay_set_text)\b[^\n]*\bs0\b")
    offenders = []
    for path in (ROOT / "src" / "presentations").rglob("*.py"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(raw.splitlines(), start=1):
            if direct_s0_render.search(line):
                offenders.append(f"{path.relative_to(ROOT)}:{line_no}: {line.strip()}")
    assert not offenders, "presentation renders volatile s0 directly:\n" + "\n".join(offenders)


def main() -> None:
    test_fief_management_presentation_uses_stable_display_strings()
    test_presentations_do_not_render_volatile_s0_directly()
    print("test_presentation_text_placeholder_static: OK")


if __name__ == "__main__":
    main()
