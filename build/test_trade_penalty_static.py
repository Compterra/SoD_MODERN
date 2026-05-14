from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "scripts" / "ZB_economy_and_trade" / "get_trade_penalty.py"


def main() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    assert '("get_trade_penalty",' in source
    assert '(party_get_skill_level, ":trade_skill", "p_main_party", skl_trade)' in source
    assert '(is_between, ":item_kind_id", trade_goods_begin, trade_goods_end)' in source
    assert '(assign, ":penalty_multiplier", 1000)' in source
    assert '(party_get_slot, ":center_relation", "$g_encountered_party", slot_center_player_relation)' in source
    assert '(call_script, "script_troop_get_player_relation", "$g_talk_troop")' in source
    assert '(assign, ":troop_reln", reg0)' in source
    assert '(assign, reg0, ":penalty")' in source

    stale_needles = [
        ":merchants_reln",
        ":merchants_relation_penalty",
        'fac_merchants", "fac_player_supporters_faction',
        'troop_get_slot, ":troop_reln"',
    ]
    for needle in stale_needles:
        assert needle not in source, needle

    print("test_trade_penalty_static: OK")


if __name__ == "__main__":
    main()
