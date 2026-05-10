from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def extract_block(text: str, start: str, end_marker: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end_marker, start_index)
    return text[start_index:end_index]


def test_fgtq_perfect_rewards_use_total_rounds() -> None:
    text = read("src/scripts/ZZ_common_array_processing/fgtq_end.py")
    assert '(eq, ":num_won", ":completed")' not in text
    perfect_checks = text.count('(eq, ":num_won", ":num_rounds")')
    assert perfect_checks >= 7, perfect_checks


def test_adenian_knights_do_not_spawn_with_dismounted_war_axe() -> None:
    text = read("compile/module_troops.py")
    block = extract_block(text, '["sod_ade_knight"', '["sod_ade_magnate"')
    assert "itm_war_axe" not in block
    assert "itm_fighting_axe" in block
    assert "tf_mounted" in block


if __name__ == "__main__":
    test_fgtq_perfect_rewards_use_total_rounds()
    test_adenian_knights_do_not_spawn_with_dismounted_war_axe()
    print("guild gauntlet and Adenian equipment static checks passed")
