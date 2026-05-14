from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def main() -> None:
    town_upgrade = read("src/menus/other/sod_upgrade.py")
    camp_upgrade = read("src/menus/camp/sod_upgrade_camp.py")
    upgrade_continue = read("src/menus/other/sod_upgrade_continue.py")

    assert_contains(town_upgrade, '("sod_upgrade", 0,\n\t"{s1}",')
    assert_contains(town_upgrade, "(str_clear, s1)")
    assert_contains(town_upgrade, "(str_clear, s20)")
    assert_contains(town_upgrade, "troops in your party can be promoted here.{s20}")
    assert_contains(town_upgrade, 'This center can train troops of {s5} and its old {s2} traditions.')
    assert_contains(town_upgrade, 'This center can train troops of {s5}.')
    assert_not_contains(town_upgrade, "{reg7?This center can train troops")
    assert_not_contains(town_upgrade, "{s5}{reg2?")
    assert_not_contains(town_upgrade, "promoted here.{s19}")
    assert_not_contains(town_upgrade, "(str_clear, s19)")
    assert_not_contains(town_upgrade, "(str_store_string, s19")

    assert_contains(camp_upgrade, '("sod_upgrade_camp", 0,\n\t"{s1}",')
    assert_contains(camp_upgrade, "(str_clear, s1)")
    assert_contains(camp_upgrade, "(str_clear, s20)")
    assert_contains(camp_upgrade, '(assign, "$g_sod_upgrade_center", -1)')
    assert_contains(camp_upgrade, "mercenaries in your party can be promoted from camp.{s20}")
    assert_not_contains(camp_upgrade, "camp.{s19}")
    assert_not_contains(camp_upgrade, "(str_store_string, s19")

    assert_contains(upgrade_continue, '("sod_upgrade_continue", 0,\n\t"{s1}",')
    assert_contains(upgrade_continue, '(assign, ":upgrade_center", "$g_sod_upgrade_center")')
    assert_contains(upgrade_continue, 'script_sod_can_upgrade_troops_here", ":upgrade1", "$g_sod_upgrade_center"')
    assert_contains(upgrade_continue, "(str_store_string, s1, \"@You have {reg4} denars.^^Selected troops: {reg5} {s3}.{s6}{s4}\")")
    assert_contains(upgrade_continue, "Path: {s7} - {s8}.")
    assert_contains(upgrade_continue, "denars total): (no charge)")
    assert_not_contains(upgrade_continue, 'script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", "$g_encountered_party"')
    assert_not_contains(upgrade_continue, "Choose a doctrine path for your {reg5}")

    preamble = read("src/menus/_preamble/00_imports.py")
    assert_contains(preamble, '(assign, ":upgrade_center", "$g_sod_upgrade_center")')
    assert_not_contains(preamble, 'script_sod_can_upgrade_troops_here", ":upgrade1", "$g_encountered_party"')

    print("test_sod_upgrade_menu_text_static: OK")


if __name__ == "__main__":
    main()
