from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "src" / "presentations" / "0014_retirement" / "retirement.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected retirement presentation behavior: {needle}"


def test_retirement_presentation_flow_and_text_are_stable() -> None:
    source = PRESENTATION.read_text(encoding="utf-8")

    assert_contains(source, '("retirement", 0, mesh_load_window,')
    assert_contains(source, '(create_button_overlay, "$g_presentation_obj_1", "@Remain in retirement.", tf_center_justify)')
    assert_contains(source, '(create_button_overlay, "$g_presentation_obj_2", "@Go back to the adventuring.", tf_center_justify)')
    assert_contains(source, '(create_text_overlay, reg1, "@You have retired at level {reg4} after {reg5} days of adventuring.", tf_center_justify)')
    assert_contains(source, '(create_text_overlay, reg2, "@Effect on Score", tf_center_justify)')
    assert_contains(source, '(create_text_overlay, reg1, "@TOTAL SCORE: {reg0}", tf_center_justify)')
    assert_contains(source, '(create_text_overlay, reg1, s68, tf_double_space|tf_scrollable)')
    assert_contains(source, '(start_presentation, "prsnt_game_credits")')
    assert_contains(source, '(change_screen_return)')

    assert "(create_text_overlay, reg1, s0" not in source
    assert "##        (overlay_set_color, reg1, 0)" not in source


def main() -> None:
    test_retirement_presentation_flow_and_text_are_stable()
    print("test_retirement_presentation_static: OK")


if __name__ == "__main__":
    main()
