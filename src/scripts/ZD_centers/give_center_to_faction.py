SCRIPTS = [
("give_center_to_faction",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),
      (try_begin),
        (check_quest_active, "qst_join_siege_with_army"),
        (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, ":center_no"),
        (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
        #Reactivating follow army quest
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (call_script, "script_store_troop_name_link_fief", s9, ":faction_marshall"),
        (setup_quest_text, "qst_follow_army"),
        (str_store_string, s2, "@{s9} wants you to resume following his army until further notice."),
        (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
        (assign, "$g_player_follow_army_warnings", 0),
      (try_end),
      (store_faction_of_party, ":old_faction", ":center_no"),
      (call_script, "script_give_center_to_faction_aux", ":center_no", ":faction_no"),
      (call_script, "script_sod_handle_center_faction_change_castle_patrols", ":center_no", ":old_faction", ":faction_no"),
      (call_script, "script_update_village_market_towns"),

      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":cur_faction"),
      (try_end),
      (assign, "$g_recalculate_ais", 1),

      (call_script, "script_activate_deactivate_player_faction", ":old_faction"),
      (try_begin),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        (call_script, "script_give_center_to_lord", ":center_no", "trp_player", 0),
        (try_for_range, ":cur_village", villages_begin, villages_end),
          (store_faction_of_party, ":cur_village_faction", ":cur_village"),
          (eq, ":cur_village_faction", "fac_player_supporters_faction"),
          (neg|party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
          #SoD Fief begin
          # don't take a village away from one of our own lords
          (party_get_slot, ":center_lord", ":cur_village", slot_town_lord),

          #MORDACHAI - SOD BUG FIX: a center may not necessarily have a lord, in which case we can't ask the lord's faction
          (try_begin),
            (ge, ":center_lord", 0),
            (store_troop_faction, ":kingdom_hero_faction", ":center_lord"),
          (else_try),
            (assign, ":kingdom_hero_faction", "fac_commoners"),
          (try_end),
          (neq, ":kingdom_hero_faction", "fac_player_supporters_faction"),
          #SoD Fief end
          (call_script, "script_give_center_to_lord", ":cur_village", "trp_player", 0),
        (try_end),
      (try_end),
  ]),
]
