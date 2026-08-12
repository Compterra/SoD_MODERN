"""Fixture tests for the LLM-first M&B 1.011 troop/item Balance Lab.

The fixture is intentionally a tiny legacy compile authoring surface.  It
proves that the Lab reads evaluated bit-packed data, keeps source/ID evidence
separate, follows explicit upgrade declarations, generates a deterministic
patch plan, rehearses without mutation, and only writes after all legacy
authoring acknowledgements are supplied.
"""

from __future__ import annotations

import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from devkit.troop_item_balance import troop_item_balance as balance


HEADER_COMMON = "bignum = 0x40000000000000000000000000000000\n"

HEADER_ITEMS = '''from header_common import *
itp_type_horse = 1
itp_type_one_handed_wpn = 2
itp_type_two_handed_wpn = 3
itp_type_polearm = 4
itp_type_arrows = 5
itp_type_bolts = 6
itp_type_shield = 7
itp_type_bow = 8
itp_type_crossbow = 9
itp_type_thrown = 10
itp_type_head_armor = 12
itp_type_body_armor = 13
itp_type_foot_armor = 14
itp_type_hand_armor = 15
itp_type_pistol = 16
itp_type_musket = 17
itp_type_bullets = 18
itp_merchandise = 0x10000
itp_unique = 0x1000
cut = 0
pierce = 1
blunt = 2
def weight(value): return (int(value * 4) & 0xff) << 24
def head_armor(value): return (value & 0xff) << 0
def body_armor(value): return (value & 0xff) << 8
def leg_armor(value): return (value & 0xff) << 16
def difficulty(value): return (value & 0xff) << 32
def hit_points(value): return (value & 0xffff) << 40
def spd_rtng(value): return (value & 0xff) << 80
def shoot_speed(value): return (value & 0x3ff) << 90
def weapon_length(value): return (value & 0x3ff) << 70
def max_ammo(value): return (value & 0xff) << 100
def abundance(value): return (value & 0xff) << 110
def accuracy(value): return leg_armor(value)
def swing_damage(value, kind): return (((kind << 8) | (value & 0xff)) & 0x3ff) << 50
def thrust_damage(value, kind): return (((kind << 8) | (value & 0xff)) & 0x3ff) << 60
def horse_speed(value): return shoot_speed(value)
def horse_maneuver(value): return spd_rtng(value)
def horse_charge(value): return thrust_damage(value, 0)
'''

HEADER_TROOPS = '''from header_common import *
tf_hero = 0x10
tf_mounted = 0x400
tf_guarantee_boots = 0x00100000
tf_guarantee_armor = 0x00200000
tf_guarantee_helmet = 0x00400000
tf_guarantee_gloves = 0x00800000
tf_guarantee_horse = 0x01000000
tf_guarantee_shield = 0x02000000
tf_guarantee_ranged = 0x04000000
for prefix, shift in (("str", 0), ("agi", 8), ("int", 16), ("cha", 24)):
    for value in range(3, 31):
        globals()[f"{prefix}_{value}"] = bignum | (value << shift)
def level(value): return (bignum | value) << 32
def wp_one_handed(value): return (bignum | value) << 0
def wp_two_handed(value): return (bignum | value) << 10
def wp_polearm(value): return (bignum | value) << 20
def wp_archery(value): return (bignum | value) << 30
def wp_crossbow(value): return (bignum | value) << 40
def wp_throwing(value): return (bignum | value) << 50
def wp_firearm(value): return (bignum | value) << 60
knows_power_strike_1 = 1 << (35 * 4)
knows_shield_1 = 1 << (26 * 4)
knows_riding_1 = 1 << (24 * 4)
'''

MODULE_ITEMS = '''from header_items import *
items = [
    ["no_item", "Invalid", [("invalid", 0)], itp_type_one_handed_wpn, 0, 3, weight(1)|spd_rtng(100)|weapon_length(90)|swing_damage(16, blunt), 0],
    ["horse_meat", "Horse Meat", [("meat", 0)], itp_type_one_handed_wpn, 0, 12, weight(40), 0],
    ["fixture_sword", "Fixture Sword", [("sword", 0)], itp_type_one_handed_wpn|itp_merchandise, 0, 1, weight(2.0)|spd_rtng(100)|weapon_length(100)|swing_damage(40, cut)|thrust_damage(24, pierce), 0],
    ["fixture_boots", "Fixture Boots", [("boots", 0)], itp_type_foot_armor, 0, 50, weight(1)|leg_armor(10), 0],
    ["fixture_shield", "Fixture Shield", [("shield", 0)], itp_type_shield, 0, 100, weight(3)|hit_points(300)|body_armor(6)|spd_rtng(90), 0],
    ["fixture_handgonne", "Fixture Handgonne", [("handgonne", 0)], itp_type_pistol, 0, 400, weight(2)|spd_rtng(45)|shoot_speed(160)|max_ammo(1)|accuracy(75)|thrust_damage(60, pierce), 0],
]
'''

MODULE_TROOPS = '''from header_troops import *
from ID_items import *
from ID_troops import *
from ID_factions import *
troops = [
    ["player", "Player", "Player", tf_hero, 0, 0, 0, [], str_4|agi_4|int_4|cha_4|level(1), wp_one_handed(20), 0, 0],
    ["temp_troop", "Temp", "Temp", tf_hero, 0, 0, 0, [], str_4|agi_4|int_4|cha_4|level(1), wp_one_handed(20), 0, 0],
    ["game", "Game", "Game", tf_hero, 0, 0, 0, [], str_4|agi_4|int_4|cha_4|level(1), wp_one_handed(20), 0, 0],
    ["unarmed_troop", "Unarmed", "Unarmed", tf_hero, 0, 0, 0, [], str_4|agi_4|int_4|cha_4|level(1), wp_one_handed(20), 0, 0],
    ["fixture_recruit", "Fixture Recruit", "Fixture Recruits", tf_guarantee_armor|tf_guarantee_shield, 0, 0, 0, [itm_fixture_sword, itm_fixture_boots], str_6|agi_6|int_4|cha_4|level(5), wp_one_handed(50)|wp_two_handed(20)|wp_polearm(20)|wp_archery(15)|wp_crossbow(15)|wp_throwing(15)|wp_firearm(0), knows_power_strike_1, 0],
    ["fixture_gunner", "Fixture Gunner", "Fixture Gunners", tf_guarantee_armor|tf_guarantee_ranged, 0, 0, 0, [itm_fixture_handgonne, itm_fixture_boots], str_8|agi_7|int_4|cha_4|level(10), wp_one_handed(30)|wp_two_handed(20)|wp_polearm(20)|wp_archery(15)|wp_crossbow(15)|wp_throwing(15)|wp_firearm(140), knows_power_strike_1, 0],
    ["fixture_veteran", "Fixture Veteran", "Fixture Veterans", tf_guarantee_armor|tf_guarantee_shield, 0, 0, 0, [itm_fixture_sword, itm_fixture_boots, itm_fixture_shield], str_10|agi_8|int_4|cha_4|level(12), wp_one_handed(100)|wp_two_handed(40)|wp_polearm(40)|wp_archery(20)|wp_crossbow(20)|wp_throwing(20)|wp_firearm(0), knows_power_strike_1|knows_shield_1, 0],
    ["fixture_veteran1", "Fixture Zealous Veteran*", "Fixture Zealous Veterans*", tf_guarantee_armor|tf_guarantee_shield, 0, 0, 0, [itm_fixture_sword, itm_fixture_boots, itm_fixture_shield], str_12|agi_9|int_4|cha_4|level(16), wp_one_handed(125)|wp_two_handed(50)|wp_polearm(50)|wp_archery(25)|wp_crossbow(25)|wp_throwing(25)|wp_firearm(0), knows_power_strike_1|knows_shield_1, 0],
    ["fixture_faith", "Fixture Faith", "Fixture Faith", tf_guarantee_armor|tf_guarantee_shield, 0, 0, 0, [itm_fixture_sword, itm_fixture_boots, itm_fixture_shield], str_14|agi_10|int_4|cha_4|level(20), wp_one_handed(150)|wp_two_handed(60)|wp_polearm(60)|wp_archery(30)|wp_crossbow(30)|wp_throwing(30)|wp_firearm(0), knows_power_strike_1|knows_shield_1, 0],
    ["sod_ant_fixture", "Antarian Fixture", "Antarian Fixtures", tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_player_supporters_faction, [itm_fixture_sword, itm_fixture_boots, itm_fixture_shield], str_8|agi_7|int_4|cha_4|level(10), wp_one_handed(80)|wp_two_handed(30)|wp_polearm(30)|wp_archery(20)|wp_crossbow(20)|wp_throwing(20)|wp_firearm(0), knows_power_strike_1|knows_shield_1, 0],
    ["ief_fixture", "Imperial Fixture", "Imperial Fixtures", tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_kingdom_6, [itm_fixture_sword, itm_fixture_boots, itm_fixture_shield], str_12|agi_9|int_4|cha_4|level(16), wp_one_handed(130)|wp_two_handed(50)|wp_polearm(50)|wp_archery(25)|wp_crossbow(25)|wp_throwing(25)|wp_firearm(0), knows_power_strike_1|knows_shield_1, 0],
]
def upgrade(troops, source, target):
    return None
upgrade(troops, "fixture_recruit", "fixture_veteran")
sod_noble_troops = [trp_fixture_veteran]
sod_faith_troops = [trp_fixture_faith]
'''

MODULE_PARTY_TEMPLATES = '''party_templates = [
    ("kingdom_6_reinforcements_a", "Imperial infantry", 0, 0, fac_commoners, 0, [(trp_ief_fixture, 2, 4)]),
    ("kingdom_6_reinforcements_b", "Imperial ranged", 0, 0, fac_commoners, 0, [(trp_ief_fixture, 1, 3)]),
    ("kingdom_6_reinforcements_c", "Imperial cavalry", 0, 0, fac_commoners, 0, [(trp_ief_fixture, 3, 5)]),
    ("legion_mercenaries", "Imperial auxiliaries", 0, 0, fac_commoners, 0, [(trp_ief_fixture, 1, 2)]),
]
'''

FAITH_ASCENSION_SCRIPT = '''SCRIPTS = [
("sod_troop_get_faith_upgrade", [
    (eq, ":noble_candidate", "trp_fixture_veteran1"),
    (assign, ":faith_upgrade", "trp_fixture_faith"),
]),
]
'''

FAITH_CANDIDATE_SCRIPT = '''SCRIPTS = [
("sod_troop_find_faith_candidate", [
    (assign, ":base_noble", "trp_fixture_veteran"),
    (assign, ":candidate", "trp_fixture_veteran1"),
]),
]
'''


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_workspace(root: Path) -> None:
    write(root / "compile/headers/header_common.py", HEADER_COMMON)
    write(root / "compile/headers/header_items.py", HEADER_ITEMS)
    write(root / "compile/headers/header_troops.py", HEADER_TROOPS)
    write(root / "compile/module_items.py", MODULE_ITEMS)
    write(root / "compile/module_troops.py", MODULE_TROOPS)
    write(root / "compile/module_party_templates.py", MODULE_PARTY_TEMPLATES)
    write(
        root / "compile/module_factions.py",
        'factions = [["commoners", "Commoners", 0, 0.0, []], ["player_supporters_faction", "Player Faction", 0, 0.0, []], ["kingdom_6", "Imperial Expeditionary Force", 0, 0.0, []]]\n',
    )
    write(root / "compile/module_constants.py", "")
    write(root / "compile/ids/ID_items.py", "itm_no_item = 0\nitm_horse_meat = 1\nitm_fixture_sword = 2\nitm_fixture_boots = 3\nitm_fixture_shield = 4\nitm_fixture_handgonne = 5\n")
    write(root / "compile/ids/ID_troops.py", "trp_player = 0\ntrp_temp_troop = 1\ntrp_game = 2\ntrp_unarmed_troop = 3\ntrp_fixture_recruit = 4\ntrp_fixture_gunner = 5\ntrp_fixture_veteran = 6\ntrp_fixture_veteran1 = 7\ntrp_fixture_faith = 8\ntrp_sod_ant_fixture = 9\ntrp_ief_fixture = 10\n")
    write(root / "compile/ids/ID_factions.py", "fac_commoners = 0\nfac_player_supporters_faction = 1\nfac_kingdom_6 = 2\n")
    write(root / "compile/ids/ID_parties.py", "p_village_16 = 100\np_village_67 = 108\n")
    write(root / "src/scripts/ZY_helper_scripts/sod_troop_get_faith_upgrade.py", FAITH_ASCENSION_SCRIPT)
    write(root / "src/scripts/ZY_helper_scripts/sod_troop_find_faith_candidate.py", FAITH_CANDIDATE_SCRIPT)
    write(root / "src/constants/module_constants.py", 'imperial_invasion_entry_villages_begin = "p_village_16"\nimperial_invasion_entry_villages_end = "p_village_67"\n')
    write(
        root / "src/triggers/ST03_daily/entry_0088.py",
        '''(try_begin),
  (eq, ":delta", 90),
  (spawn_around_party, ":center", "pt_legion_mercenaries"),
  (party_add_template, ":party", "pt_legion_mercenaries"),
(else_try),
  (eq, ":delta", 60),
  (spawn_around_party, ":center", "pt_legion_mercenaries"),
  (party_add_template, ":party", "pt_legion_mercenaries"),
  (party_add_template, ":party", "pt_legion_mercenaries"),
(else_try),
  (eq, ":delta", 30),
  (spawn_around_party, ":center", "pt_legion_mercenaries"),
  (party_add_template, ":party", "pt_legion_mercenaries"),
  (party_add_template, ":party", "pt_legion_mercenaries"),
  (party_add_template, ":party", "pt_legion_mercenaries"),
(try_end),
$g_sod_invasion_begin
fac_kingdom_6
''',
    )
    write(root / "src/scripts/ZA_hardcoded_game_scripts/game_start.py", "pt_kingdom_6_reinforcements_a\npt_kingdom_6_reinforcements_b\npt_kingdom_6_reinforcements_c\n")
    write(root / "src/scripts/ZY_helper_scripts/sod_imperial_expedition.py", 'sod_imperial_expedition_process_campaign\nslot_faction_imperial_expedition_supply\n(lt, ":supply", 20)\nsod_imperial_expedition_calculate_anti_legion_coalition\nnative_kingdoms_begin, native_kingdoms_end\nfac_sod_merc_guild7\n')
    write(root / "src/scripts/_preamble/00_imports.py", 'troop_name.startswith("ief_")\n')
    write(root / "build_module.bat", "process_items.py\nprocess_troops.py\n")
    write(root / "build/build_all.py", "# Fixture deliberately has no item/troop fragment builder.\n")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="troop-item-balance-") as temporary:
        root = Path(temporary)
        make_workspace(root)
        index = balance.build_balance_index(root)
        assert balance.build_balance_index(root) is index
        summary = balance.balance_summary(index)
        assert summary["authoring"]["confirmed"] is True
        assert summary["items"]["id_contract"]["passed"] is True
        assert summary["troops"]["id_contract"]["passed"] is True
        assert summary["troops"]["elite_tracks"]["noble_runtime_list_count"] == 1
        assert summary["troops"]["elite_tracks"]["faith_runtime_list_count"] == 1
        assert summary["troops"]["elite_tracks"]["faith_candidate_route_edge_count"] == 1
        assert summary["troops"]["elite_tracks"]["faith_ascension_edge_count"] == 1

        found_items = balance.balance_find_items(index, query="fixture", limit=10)
        assert found_items["match_count"] == 4
        item = balance.balance_item(index, "itm_fixture_sword", troop_limit=5)
        assert item["item"]["stats"]["swing_damage"]["amount"] == 40
        assert item["item"]["troop_use_count"] == 6
        firearm_item = balance.balance_item(index, "itm_fixture_handgonne", troop_limit=5)
        assert firearm_item["item"]["combat_score"] > 100

        troop = balance.balance_troop(index, "trp_fixture_recruit", item_limit=5)
        assert troop["troop"]["kit_analysis"]["status"] in {"under_equipped", "within_band", "over_equipped"}
        assert troop["troop"]["upgrades_to"] == ["trp_fixture_veteran"]
        gunner = balance.balance_troop(index, "trp_fixture_gunner", item_limit=5)
        assert gunner["troop"]["role"] == "Firearm"
        assert gunner["troop"]["kit_analysis"]["ranged_weapon"] > 0
        tree = balance.balance_upgrade_tree(index, "trp_fixture_recruit", depth=2)
        assert {node["code"] for node in tree["nodes"]} >= {"fixture_recruit", "fixture_veteran"}
        roster_catalog = balance.balance_roster_inventory(index)
        assert roster_catalog["mode"] == "catalog"
        roster_inventory = balance.balance_roster_inventory(index, roster="Faction: Commoners", troop_limit=10, item_limit=10)
        assert roster_inventory["mode"] == "inventory"
        assert roster_inventory["summary"]["rank_counts"]["Noble"] == 3
        assert roster_inventory["summary"]["rank_counts"]["Faith/Zealot"] == 1
        assert any(item["item_id"] == "itm_fixture_sword" for item in roster_inventory["items"])
        progression = balance.balance_progression(index, roster="Faction: Commoners", troop_limit=10, edge_limit=10)
        assert progression["mode"] == "progression"
        assert progression["explicit_upgrade_edge_count"] == 1
        assert progression["faith_candidate_route_count"] == 1
        assert progression["faith_ascension_count"] == 1
        assert progression["faith_ascensions"][0]["faith_target_id"] == "trp_fixture_faith"
        cohort_catalog = balance.balance_campaign_cohorts(index)
        assert cohort_catalog["mode"] == "catalog"
        assert any(row["cohort"]["id"] == "campaign:player-start:antarian" for row in cohort_catalog["cohorts"])
        antarian_cohort = balance.balance_campaign_cohorts(index, cohort="Player start: Antarian", troop_limit=10)
        assert antarian_cohort["mode"] == "cohort"
        assert antarian_cohort["cohort"]["campaign_role"] == "mutually_exclusive_player_start"
        assert [troop["troop_id"] for troop in antarian_cohort["troops"]] == ["trp_sod_ant_fixture"]
        invasion = balance.balance_imperial_invasion(index, include_auxiliaries=True)
        assert invasion["readiness"] == "source_contracts_present"
        assert invasion["core_wave_count"] == 3
        assert invasion["missing_core_template_ids"] == []
        assert invasion["auxiliary_staging"]["template_id"] == "pt_legion_mercenaries"
        assert invasion["core_waves"][0]["stacks"][0]["troop_id"] == "trp_ief_fixture"
        assert invasion["pre_invasion_staging"]["entry_range"]["entry_point_count"] == 8
        assert invasion["pre_invasion_staging"]["stages"][0]["template_applications_per_successful_spawn"] == 2
        assert invasion["pre_invasion_staging"]["cumulative_upper_bound_across_entry_range"]["expected"] == 108
        player_start_profile = balance.balance_player_start_factions(index)
        assert player_start_profile["mode"] == "player_start_faction_profile"
        assert player_start_profile["player_start_culture_count"] == 5
        assert player_start_profile["state"] == "needs_source_review"
        native_profile = balance.balance_native_kingdoms(index)
        assert native_profile["mode"] == "native_kingdom_profile"
        assert native_profile["kingdom_count"] == 5
        assert native_profile["state"] == "needs_source_review"
        faith_profile = balance.balance_faith_ascensions(index)
        assert faith_profile["mode"] == "faith_ascension_profile"
        assert faith_profile["state"] == "within_static_tier_targets"
        assert faith_profile["route_count"] == 1
        assert faith_profile["expected_route_count"] == 1
        assert balance.balance_outliers(index, domain="items", limit=20)["finding_count"] >= 1

        item_plan = balance.balance_patch(
            index,
            "item",
            "itm_fixture_sword",
            changes={"price": 125, "stats": {"weight": 2.5, "swing_damage": {"value": 42, "damage_type": "pierce"}}},
        )
        assert item_plan["plan_kind"] == "legacy_compile_balance_patch"
        assert "125" in item_plan["unified_diff"]
        before = (root / "compile/module_items.py").read_text(encoding="utf-8")
        rehearsal = balance.balance_apply(
            index,
            "item",
            "itm_fixture_sword",
            changes={"price": 125, "stats": {"weight": 2.5, "swing_damage": {"value": 42, "damage_type": "pierce"}}},
            expected_sha256=item_plan["target"]["base_sha256"],
            expected_plan_sha256=item_plan["plan_sha256"],
        )
        assert rehearsal["applied"] is False
        assert (root / "compile/module_items.py").read_text(encoding="utf-8") == before
        try:
            balance.balance_apply(
                index,
                "item",
                "itm_fixture_sword",
                changes={"price": 125, "stats": {"weight": 2.5, "swing_damage": {"value": 42, "damage_type": "pierce"}}},
                expected_sha256=item_plan["target"]["base_sha256"],
                expected_plan_sha256=item_plan["plan_sha256"],
                dry_run=False,
            )
        except balance.BalanceError as error:
            assert "allow_legacy_compile_authoring" in str(error)
        else:
            raise AssertionError("Non-dry legacy apply must require an explicit acknowledgement.")
        applied = balance.balance_apply(
            index,
            "item",
            "itm_fixture_sword",
            changes={"price": 125, "stats": {"weight": 2.5, "swing_damage": {"value": 42, "damage_type": "pierce"}}},
            expected_sha256=item_plan["target"]["base_sha256"],
            expected_plan_sha256=item_plan["plan_sha256"],
            dry_run=False,
            allow_legacy_compile_authoring=True,
        )
        assert applied["applied"] is True
        refreshed = balance.build_balance_index(root)
        assert balance.balance_item(refreshed, "fixture_sword")["item"]["price"] == 125

        troop_plan = balance.balance_patch(
            refreshed,
            "troop",
            "fixture_recruit",
            changes={
                "attributes": {"level": 6},
                "proficiencies": {"one_handed": 55},
                "skills": {"power_strike": 2},
                "inventory": ["itm_fixture_sword", "itm_fixture_boots", "itm_fixture_shield"],
            },
        )
        assert len(troop_plan["replacements"]) == 4
        assert "wp_one_handed(55)" in troop_plan["unified_diff"]
        protected = balance.balance_patch(refreshed, "item", "no_item", changes={"price": 4})
        assert protected["apply_contract"]["allow_protected_legacy_record_change_required_for_non_dry"] is True
        verification = balance.balance_verify(refreshed)
        assert verification["state"] == "ready_for_build_review"

    print("test_troop_item_balance: OK")


if __name__ == "__main__":
    main()
