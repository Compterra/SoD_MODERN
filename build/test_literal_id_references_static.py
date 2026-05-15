from __future__ import annotations

import ast
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


ID_FILES = {
    "script_": "ID_scripts.py",
    "mnu_": "ID_menus.py",
    "prsnt_": "ID_presentations.py",
    "mst_": "ID_mission_templates.py",
    "qst_": "ID_quests.py",
    "trp_": "ID_troops.py",
    "itm_": "ID_items.py",
    "fac_": "ID_factions.py",
    "p_": "ID_parties.py",
    "pt_": "ID_party_templates.py",
    "scn_": "ID_scenes.py",
    "str_": "ID_strings.py",
    "snd_": "ID_sounds.py",
    "mesh_": "ID_meshes.py",
    "spr_": "ID_scene_props.py",
    "icon_": "ID_map_icons.py",
    "skl_": "ID_skills.py",
    "anim_": "ID_animations.py",
}


def _read_id_assignments(filename: str) -> set[str]:
    raw = (ROOT / "compile" / "ids" / filename).read_text(
        encoding="utf-8", errors="replace"
    )
    return {
        match.group(1)
        for match in re.finditer(r"(?m)^([A-Za-z0-9_]+)\s*=", raw)
    }


def _literal_to_generated_id(value: str) -> tuple[str, str] | None:
    if value.startswith("mnu_"):
        return f"menu_{value[4:]}", "mnu_"
    for prefix in ID_FILES:
        if value.startswith(prefix):
            return value, prefix
    return None


def _is_dynamic_id_template(value: str) -> bool:
    return (
        value in {"p_", "str_", "trp_"}
        or "%" in value
        or "{" in value
        or "}" in value
    )


def _is_operation_name(value: str) -> bool:
    return value.startswith("str_store_") or value == "str_clear"


def test_live_literal_module_system_ids_resolve_to_generated_ids() -> None:
    id_sets = {
        prefix: _read_id_assignments(filename)
        for prefix, filename in ID_FILES.items()
    }
    missing: list[str] = []

    for path in (ROOT / "src").rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(raw, filename=path.as_posix())
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            value = node.value
            if _is_dynamic_id_template(value) or _is_operation_name(value):
                continue
            resolved = _literal_to_generated_id(value)
            if resolved is None:
                continue
            generated_id, prefix = resolved
            if generated_id not in id_sets[prefix]:
                rel = path.relative_to(ROOT).as_posix()
                missing.append(f"{rel}:{node.lineno}: {value} -> {generated_id}")

    assert not missing, "missing live module-system literal ID(s):\n" + "\n".join(missing[:80])
