from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "scripts" / "ZY_helper_scripts" / "change_player_honor.py"


def main() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    assert '("change_player_honor",' in source
    assert '(store_script_param_1, ":honor_dif")' in source
    assert '(val_add, "$player_honor", ":honor_dif")' in source
    assert '(display_message, "@You gain honour.", honor_color)' in source
    assert '(display_message, "@You lose honour.", lose_honor_color)' in source

    stale_needles = [
        ":temp_honor",
        ":num_nonlinear_steps",
        "(val_mul, \":honor_dif\", 1000)",
        "(val_div, \":honor_dif\", 2)",
    ]
    for needle in stale_needles:
        assert needle not in source, needle

    print("test_change_player_honor_static: OK")


if __name__ == "__main__":
    main()
