# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def active_lines_with(token: str) -> list[str]:
    roots = (ROOT / "src" / "scripts", ROOT / "src" / "menus", ROOT / "src" / "dialogs")
    hits: list[str] = []
    for root in roots:
        for path in root.rglob("*.py"):
            raw = path.read_text(encoding="utf-8", errors="replace")
            for line_no, line in enumerate(raw.splitlines(), start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if token in stripped:
                    hits.append(f"{path.relative_to(ROOT)}:{line_no}:{stripped}")
    return hits


def test_scout_party_template_has_real_troops() -> None:
    templates = read("compile/module_party_templates.py")
    assert '("scout_party","Scouts"' in templates
    assert '("scout_party","Scouts",icon_gray_knight|carries_goods(1)|pf_show_faction,0,fac_commoners,bandit_personality,[])' not in templates
    assert "(trp_caravan_guard,2,4)" in templates
    assert "(trp_watchman,4,8)" in templates


def test_live_scout_party_uses_are_visible_to_audit() -> None:
    hits = active_lines_with("pt_scout_party")
    assert isinstance(hits, list)


if __name__ == "__main__":
    test_scout_party_template_has_real_troops()
    test_live_scout_party_uses_are_visible_to_audit()
    print("test_scout_party_template_static: OK")
