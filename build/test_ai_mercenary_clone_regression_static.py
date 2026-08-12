from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    hire = read("src/scripts/ZI_campaign_ai/ai_hire_mercenaries.py")
    pulse = read("src/scripts/ZY_helper_scripts/sod_merc_market_weekly_pulse.py")
    bid = read("src/scripts/ZY_helper_scripts/sod_merc_market_generate_bid.py")
    accept = read("src/scripts/ZY_helper_scripts/sod_merc_market_try_accept_bid.py")
    spawn = read("src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py")
    sanitizer = read("src/scripts/ZC_parties/sod_sanitize_unique_hero_party_stacks.py")

    assert '(assign, ":faction", ":troop_faction")' not in hire, "AI merc hire can still use kingdom faction as roster"
    assert "script_sod_merc_market_weekly_pulse" in hire, "AI merc hire must delegate to the market pulse"
    assert "script_cf_spawn_ai_mercs" not in hire, "AI merc hire must not spawn directly"
    assert "(try_for_range, \":guild_faction\", guilds_begin, guilds_end)" in pulse, "AI merc market pulse must bid only over guild rosters"
    assert "script_sod_merc_market_generate_bid" in pulse, "AI merc market pulse must generate guild bids"
    assert "script_sod_merc_market_try_accept_bid" in pulse, "AI merc market pulse must accept through the guarded contract path"
    assert '(call_script, "script_cf_sod_faction_is_merc_guild", ":guild_faction")' in bid, "bid generation must validate guild factions"
    assert '(call_script, "script_cf_sod_faction_is_merc_guild", ":guild_faction")' in accept, "bid acceptance must validate guild factions"
    assert "script_sod_merc_market_resolve_ai_contract_role" in accept, "accepted bids must resolve a deployable role before formation"
    assert '(call_script, "script_cf_spawn_ai_mercs", ":boss_troop", ":guild_faction", ":boss_party", ":company_size", ":kingdom_faction", ":effective_demand_type")' in accept, "accepted bids must pass the selected guild roster and resolved live role to spawning"

    assert '(is_between, ":faction", guilds_begin, guilds_end)' in spawn, "cf_spawn_ai_mercs must reject non-guild factions"
    assert "script_sod_merc_guild_get_contract_roster" in spawn, "AI merc parties must resolve a role-aware roster before spawning"
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
