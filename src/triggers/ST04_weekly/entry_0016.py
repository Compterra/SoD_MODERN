SIMPLE_TRIGGERS = [
(24*7,
   [
       (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
         (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt), #Increasing debt
         (val_mul, ":cur_debt", 101),
         (val_div, ":cur_debt", 100),
         (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
         (call_script, "script_calculate_hero_weekly_net_income_and_add_to_wealth", ":troop_no"), #Adding net income
       (try_end),
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         #If non-player center, adding income to wealth (from population and prosperity, not thin air)
         (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
         (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
         (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
         (party_get_slot, ":center_population", ":center_no", slot_center_sod_local_population),
         (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
         (val_max, ":center_population", 0),
         (val_max, ":prosperity", 0),
         (store_mul, ":added_wealth", ":center_population", 2),
         (store_mul, ":prosperity_part", ":prosperity", 10),
         (val_add, ":added_wealth", ":prosperity_part"),
         (val_max, ":added_wealth", 50),
         (try_begin),
           (party_slot_eq, ":center_no", slot_party_type, spt_town),
           (val_mul, ":added_wealth", 3),
           (val_div, ":added_wealth", 2),
         (try_end),
         (val_add, ":cur_wealth", ":added_wealth"),
         (call_script, "script_calculate_weekly_party_wage", ":center_no"),
         (val_sub, ":cur_wealth", reg0),
         (val_max, ":cur_wealth", 0),
         (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
       (try_end),
    ]),
]
