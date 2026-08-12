# COST: O(centers + lords * centers) with expensive resilience profiles evaluated once per pass.
SCRIPTS = [
("sod_npc_invest_in_centers",
 [
   # Lords share a snapshot, then refresh only the center changed by each investment.
   (call_script, "script_sod_refresh_all_center_investment_profiles"),

   (try_for_range, ":lord_no", kingdom_heroes_begin, kingdom_heroes_end),
     (neq, ":lord_no", "trp_player"),
     (store_troop_faction, ":lord_faction", ":lord_no"),
     (is_between, ":lord_faction", kingdoms_begin, kingdoms_end),
     (troop_get_slot, ":wealth", ":lord_no", slot_troop_wealth),
     (ge, ":wealth", 2500),
     (assign, ":scope", 0),
     (try_begin),
       (faction_slot_eq, ":lord_faction", slot_faction_leader, ":lord_no"),
       (ge, ":wealth", 6000),
       (assign, ":scope", 1),
     (try_end),

     (call_script, "script_sod_find_cached_investment_target", ":lord_no", ":scope"),
     (assign, ":center_no", reg0),
     (assign, ":need_score", reg1),
     (assign, ":investment_mode", reg2),
     (gt, ":center_no", 0),
     (gt, ":need_score", 0),

     (assign, ":budget", 1200),
     (try_begin),
       (faction_slot_eq, ":lord_faction", slot_faction_leader, ":lord_no"),
       (assign, ":budget", 2500),
     (try_end),
     (store_div, ":extra_budget", ":wealth", 10),
     (val_add, ":budget", ":extra_budget"),
     (val_min, ":budget", 5000),
     (store_div, ":reserve", ":wealth", 2),
     (val_min, ":budget", ":reserve"),
     (ge, ":budget", 500),

     (val_sub, ":wealth", ":budget"),
     (troop_set_slot, ":lord_no", slot_troop_wealth, ":wealth"),
     (call_script, "script_sod_apply_center_investment", ":center_no", ":lord_no", ":budget", ":investment_mode"),
     (call_script, "script_sod_refresh_center_investment_profile", ":center_no"),
   (try_end),
 ]),
]
