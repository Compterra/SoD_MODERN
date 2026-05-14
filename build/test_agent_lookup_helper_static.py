from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "scripts" / "ZH_heroes" / "cf_get_first_agent_with_troop_id.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected agent lookup behavior: {needle}"


def main() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    assert_contains(source, '("cf_get_first_agent_with_troop_id",')
    assert_contains(source, '(store_script_param_1, ":troop_no")')
    assert_contains(source, '(try_for_agents, ":cur_agent")')
    assert_contains(source, '(eq, ":result", -1)')
    assert_contains(source, '(agent_get_troop_id, ":cur_troop_no", ":cur_agent")')
    assert_contains(source, '(eq, ":cur_troop_no", ":troop_no")')
    assert_contains(source, '(assign, reg0, ":result")')
    assert_contains(source, '(neq, reg0, -1)')

    assert ":agent_no_to_begin_searching_after" not in source
    assert "store_script_param_2" not in source

    print("test_agent_lookup_helper_static: OK")


if __name__ == "__main__":
    main()
