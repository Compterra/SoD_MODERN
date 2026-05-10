"""Static checks for the JQ companion quickview presentation polish."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "src" / "presentations" / "0015_jq_companions_quickview" / "jq_companions_quickview.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str) -> None:
    assert needle in text, f"missing expected text: {needle}"


def assert_not_contains(text: str, needle: str) -> None:
    assert needle not in text, f"unexpected stale text: {needle}"


def main() -> None:
    source = read(PRESENTATION)

    assert_contains(source, '"$g_jq_selected_index"')
    assert_contains(source, '(create_mesh_overlay_with_tableau_material, "$jq_portrait", -1, "tableau_troop_note_mesh", "$jq_dude")')
    assert_contains(source, '(troop_get_slot, "$jq_dude", "trp_temp_array_c", "$g_jq_selected_index")')
    assert_contains(source, '(assign, ":selected_index", 19)')
    assert_contains(source, '(start_presentation, "prsnt_jq_companions_quickview")')
    assert_not_contains(source, "Doesn't clear previous mesh")

    return_branch = source.split('(eq, ":espresso", "$g_jq_Return_to_menu")', 1)[1]
    first_selector_branch = return_branch.split('(eq, ":espresso", "$g_jq_selector_1")', 1)[0]
    assert_contains(first_selector_branch, '(jump_to_menu, "mnu_camp")')
    assert_contains(first_selector_branch, '(jump_to_menu,"mnu_town_trade")')

    selector_reload_branch = source.split('(ge, ":selected_index", 0)', 1)[1]
    assert_contains(selector_reload_branch, '(lt, ":selected_index", "$jq_nr")')
    assert_contains(selector_reload_branch, '(assign, "$g_jq_selected_index", ":selected_index")')
    assert_contains(selector_reload_branch, '(start_presentation, "prsnt_jq_companions_quickview")')


if __name__ == "__main__":
    main()
