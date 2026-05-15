from __future__ import annotations

from collections import defaultdict
import importlib
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
for path in (
    ROOT / "compile" / "ids",
    ROOT / "compile",
    ROOT / "compile" / "headers",
    ROOT / "compile" / "process",
    ROOT,
):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from process_common import convert_to_identifier  # type: ignore  # noqa: E402


GENERATED_ID_SPECS = (
    ("animations", "module_animations", "animations", "anim_", "ID_animations.py", True),
    ("factions", "module_factions", "factions", "fac_", "ID_factions.py", True),
    ("items", "module_items", "items", "itm_", "ID_items.py", True),
    ("map icons", "module_map_icons", "map_icons", "icon_", "ID_map_icons.py", True),
    ("menus", "module_game_menus", "game_menus", "menu_", "ID_menus.py", True),
    ("meshes", "module_meshes", "meshes", "mesh_", "ID_meshes.py", True),
    ("mission templates", "module_mission_templates", "mission_templates", "mst_", "ID_mission_templates.py", True),
    ("music", "module_music", "tracks", "track_", "ID_music.py", True),
    ("particle systems", "module_particle_systems", "particle_systems", "psys_", "ID_particle_systems.py", True),
    ("parties", "module_parties", "parties", "p_", "ID_parties.py", True),
    ("party templates", "module_party_templates", "party_templates", "pt_", "ID_party_templates.py", True),
    ("presentations", "module_presentations", "presentations", "prsnt_", "ID_presentations.py", True),
    ("quests", "module_quests", "quests", "qst_", "ID_quests.py", True),
    ("scenes", "module_scenes", "scenes", "scn_", "ID_scenes.py", True),
    ("scene props", "module_scene_props", "scene_props", "spr_", "ID_scene_props.py", False),
    ("scripts", "module_scripts", "scripts", "script_", "ID_scripts.py", True),
    ("skills", "module_skills", "skills", "skl_", "ID_skills.py", True),
    ("sounds", "module_sounds", "sounds", "snd_", "ID_sounds.py", True),
    ("strings", "module_strings", "strings", "str_", "ID_strings.py", True),
    ("tableau materials", "module_tableau_materials", "tableaus", "tableau_", "ID_tableau_materials.py", True),
    ("troops", "module_troops", "troops", "trp_", "ID_troops.py", True),
)


def _generated_ids(module_name: str, attr_name: str, prefix: str, canonicalize: bool) -> list[str]:
    sys.modules.pop(module_name, None)
    module = importlib.import_module(module_name)
    ids: list[str] = []
    for entry in getattr(module, attr_name):
        raw_id = entry[0]
        if canonicalize:
            raw_id = convert_to_identifier(raw_id)
        ids.append(f"{prefix}{raw_id}")
    return ids


def _id_file_assignments(id_file: str) -> dict[str, int]:
    raw = (ROOT / "compile" / "ids" / id_file).read_text(
        encoding="utf-8", errors="replace"
    )
    return {
        match.group(1): int(match.group(2))
        for match in re.finditer(r"(?m)^([A-Za-z0-9_]+)\s*=\s*(\d+)\s*$", raw)
    }


def test_generated_module_ids_are_unique_after_process_canonicalization() -> None:
    issues: list[str] = []
    for label, module_name, attr_name, prefix, _id_file, canonicalize in GENERATED_ID_SPECS:
        ids = _generated_ids(module_name, attr_name, prefix, canonicalize)
        seen: dict[str, int] = {}
        duplicates: dict[str, list[int]] = defaultdict(list)
        for index, generated_id in enumerate(ids):
            if generated_id in seen:
                duplicates[generated_id].extend([seen[generated_id], index])
            else:
                seen[generated_id] = index
        for generated_id, indexes in sorted(duplicates.items()):
            unique_indexes = sorted(set(indexes))
            issues.append(f"{label}: {generated_id} appears at {unique_indexes}")

    assert not issues, "duplicate generated ID(s):\n" + "\n".join(issues[:80])


def test_generated_module_ids_match_checked_in_id_files() -> None:
    issues: list[str] = []
    for label, module_name, attr_name, prefix, id_file, canonicalize in GENERATED_ID_SPECS:
        ids = _generated_ids(module_name, attr_name, prefix, canonicalize)
        expected = {generated_id: index for index, generated_id in enumerate(ids)}
        actual = {
            generated_id: index
            for generated_id, index in _id_file_assignments(id_file).items()
            if generated_id.startswith(prefix)
        }
        if actual != expected:
            missing = [generated_id for generated_id in ids if generated_id not in actual]
            extra = [generated_id for generated_id in actual if generated_id not in expected]
            shifted = [
                f"{generated_id}: expected {expected[generated_id]}, got {actual.get(generated_id)}"
                for generated_id in ids
                if actual.get(generated_id) != expected[generated_id]
            ]
            issues.append(
                f"{label}: missing={missing[:5]} extra={extra[:5]} shifted={shifted[:5]}"
            )

    assert not issues, "generated module / ID file mismatch:\n" + "\n".join(issues[:40])
