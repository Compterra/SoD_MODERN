from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    hire = read("src/scripts/ZI_campaign_ai/ai_hire_mercenaries.py")
    spawn = read("src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py")
    sanitizer = read("src/scripts/ZC_parties/sod_sanitize_unique_hero_party_stacks.py")

    assert '(assign, ":faction", ":troop_faction")' not in hire, "AI merc hire can still use kingdom faction as roster"
    assert '(is_between, ":faction", guilds_begin, guilds_end)' in hire, "AI merc hire must require a guild roster"
    assert '(lt, ":rand", 75)' in hire, "AI merc hire should only use the active merc pact branch"

    assert '(is_between, ":faction", guilds_begin, guilds_end)' in spawn, "cf_spawn_ai_mercs must reject non-guild factions"
    assert '(party_set_name, ":mercs", "str_s5_mercs")' not in spawn, "AI merc party names must not keep a live {s5} template"
    assert "(str_store_string, s60, \"@{s61}'s Mercenaries\")" in spawn, "AI merc party names must be resolved before party_set_name"
    assert '(party_set_name, ":mercs", s60)' in spawn, "AI merc party names should use a resolved string register"
    for token in [
        '(gt, ":t1_1", 0)',
        '(gt, ":t1_2", 0)',
        '(gt, ":noble", 0)',
        '(neq, ":t1_1", "trp_player")',
        '(neq, ":t1_2", "trp_player")',
        '(neq, ":noble", "trp_player")',
    ]:
        assert token in spawn, f"missing roster guard: {token}"

    assert '(eq, ":stack_troop", "trp_player")' in sanitizer, "sanitizer must remove player clone stacks"
    assert '(remove_party, ":party_no")' in sanitizer, "sanitizer must remove emptied corrupt merc parties"

    update_names = read("src/scripts/ZY_helper_scripts/update_merc_names.py")
    assert '(party_set_name, ":cur_party", "str_s5_mercs")' not in update_names, "merc name refresh must not reintroduce live {s5}"
    assert '(party_set_name, ":cur_party", s60)' in update_names, "merc name refresh should use a resolved string register"

    print("AI mercenary clone regression static checks passed")


if __name__ == "__main__":
    main()
