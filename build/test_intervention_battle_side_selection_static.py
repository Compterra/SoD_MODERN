from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRE_JOIN = ROOT / "src" / "menus" / "encounter" / "pre_join_help_attackers.py"
JOIN_BATTLE = ROOT / "src" / "menus" / "encounter" / "join_attack.py"
SIMPLE_ENCOUNTER = ROOT / "src" / "menus" / "0000_hardcoded_mb1011" / "simple_encounter.py"


def choices_after(source: str, marker: str) -> str:
    start = source.index(marker)
    return source[start:]


def main() -> None:
    pre_join = PRE_JOIN.read_text(encoding="utf-8")
    join_battle = JOIN_BATTLE.read_text(encoding="utf-8")
    simple_encounter = SIMPLE_ENCOUNTER.read_text(encoding="utf-8")

    # Each active side remains selectable when it is non-hostile to the player's
    # current political allegiance, rather than only to an independent realm.
    assert '(assign, ":player_faction", "fac_player_faction")' in pre_join
    assert '(assign, ":player_faction", "$players_kingdom")' in pre_join
    assert '(store_relation, ":attacker_relation", ":attacker_faction", ":player_faction")' in pre_join
    assert '(store_relation, ":defender_relation", ":defender_faction", ":player_faction")' in pre_join
    assert 'store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"' not in pre_join
    assert 'store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"' not in pre_join
    assert '(select_enemy, 0)' in pre_join
    assert '(select_enemy, 1)' in pre_join
    assert '(assign, "$g_enemy_party", "$g_encountered_party")' in pre_join
    assert '(assign, "$g_enemy_party", "$g_encountered_party_2")' in pre_join

    # Battle readiness is a snapshot for presentation and outcome handling; it
    # must not erase intervention actions while the selected party is active.
    join_choices = choices_after(join_battle, '        build_sod_battle_commander_change_option(')
    simple_choices = choices_after(simple_encounter, '      build_sod_battle_commander_change_option(')
    assert '$g_enemy_fit_for_battle' not in join_choices
    assert '$g_enemy_fit_for_battle' not in simple_choices

    for source in (join_choices, simple_choices):
        assert '(gt, "$g_enemy_party", 0)' in source
        assert '(party_is_active, "$g_enemy_party")' in source

    print("test_intervention_battle_side_selection_static: OK")


if __name__ == "__main__":
    main()
