from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.troop_item_balance import troop_item_balance as balance


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8", errors="replace")


def require(text: str, token: str) -> None:
    assert token in text, f"Missing expected Imperial invasion contract: {token}"


def main() -> None:
    doctrine = read("src/scripts/_preamble/00_imports.py")
    party_templates = read("compile/module_party_templates.py")
    game_start = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    staging = read("src/triggers/ST03_daily/entry_0088.py")
    expedition = read("src/scripts/ZY_helper_scripts/sod_imperial_expedition.py")
    program = read("docs/tooling/TROOP_ITEM_REBALANCE_PROGRAM.md")

    require(doctrine, 'troop_name.startswith("ief_")')
    for template in (
        "kingdom_6_reinforcements_a",
        "kingdom_6_reinforcements_b",
        "kingdom_6_reinforcements_c",
    ):
        require(party_templates, f'"{template}"')
        require(game_start, f'"pt_{template}"')
    require(party_templates, '"legion_mercenaries"')
    for delta in ("90", "60", "30"):
        require(staging, f'(eq, ":delta", {delta})')
    require(staging, "pt_legion_mercenaries")
    require(staging, '(eq, ":cur_day", "$g_sod_invasion_begin")')
    for token in (
        '("sod_imperial_expedition_enforce_total_war"',
        '("sod_imperial_expedition_process_campaign"',
        "slot_faction_imperial_expedition_supply",
        '(lt, ":supply", 20)',
        '("sod_imperial_expedition_calculate_anti_legion_coalition"',
        "native_kingdoms_begin, native_kingdoms_end",
    ):
        require(expedition, token)
    require(program, "Campaign Cohorts and Comparison Boundaries")
    require(program, "imperial-invasion --include-auxiliaries")
    profile = balance.balance_imperial_invasion(balance.build_balance_index(ROOT), include_auxiliaries=True)
    staging_profile = profile["pre_invasion_staging"]
    assert staging_profile["status"] == "present"
    assert staging_profile["entry_range"]["entry_point_count"] == 8
    assert [stage["template_applications_per_successful_spawn"] for stage in staging_profile["stages"]] == [2, 3, 4]
    assert [stage["upper_bound_across_entry_range"]["expected"] for stage in staging_profile["stages"]] == [640, 960, 1280]
    assert staging_profile["cumulative_upper_bound_across_entry_range"]["expected"] == 2880
    print("test_imperial_invasion_static: OK")


if __name__ == "__main__":
    main()
