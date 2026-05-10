DIALOGS = [
[anyone|plyr, "prisoner_chat",
  [
    (store_conversation_troop, "$g_talk_troop"),

    (try_begin),
      (troop_is_hero, "$g_talk_troop"),
      (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
      (assign, "$g_talk_troop_relation", reg0),
      (store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
      (store_relation, "$g_talk_troop_faction_relation", "fac_player_supporters_faction", "$g_talk_troop_faction"),
    (else_try),

      # NOTE: as it turns out, non-heros don't have a meaningful faction, therefore they don't have a meaningful relationship with the player
      (try_begin),
        (is_between, "$g_talk_troop", "trp_swadian_recruit", "trp_vaegir_recruit"),
        (assign, "$g_talk_troop_faction", "fac_kingdom_1"),
      (else_try),
        (is_between, "$g_talk_troop", "trp_vaegir_recruit", "trp_khergit_tribesman"),
        (assign, "$g_talk_troop_faction", "fac_kingdom_2"),
      (else_try),
        (is_between, "$g_talk_troop", "trp_khergit_tribesman", "trp_nord_recruit"),
        (assign, "$g_talk_troop_faction", "fac_kingdom_3"),
      (else_try),
        (is_between, "$g_talk_troop", "trp_nord_recruit", "trp_rhodok_tribesman"),
        (assign, "$g_talk_troop_faction", "fac_kingdom_4"),
      (else_try),
        (is_between, "$g_talk_troop", "trp_rhodok_tribesman", "trp_ief_velites"),
        (assign, "$g_talk_troop_faction", "fac_kingdom_5"),
      (else_try),
        (is_between, "$g_talk_troop", "trp_ief_velites", "trp_sod_peasant1"),
        (assign, "$g_talk_troop_faction", "fac_kingdom_6"),
      (else_try),
        # simply treat everything else as outlaws for this purpose
        (assign, "$g_talk_troop_faction", "fac_outlaws"),
      (try_end),

      # so use our grunt's real faction to get faction relations
      (store_relation, "$g_talk_troop_faction_relation", "fac_player_supporters_faction", "$g_talk_troop_faction"),

      # don't generate a relation value more than once per individual
      (troop_get_slot, "$g_talk_troop_relation", "$g_talk_troop", slot_troop_player_relation),
      (eq, "$g_talk_troop_relation", 0),

      # and use a modified version of that as this individual's relation
      (store_random_in_range, ":roll", -20, +21),
      (store_add, "$g_talk_troop_relation", "$g_talk_troop_faction_relation", ":roll"),
      (val_clamp, "$g_talk_troop_relation", -100, 101),
      (troop_set_slot, "$g_talk_troop", slot_troop_player_relation, "$g_talk_troop_relation"),
    (try_end),

    # debug
    (try_begin),
      (eq, "$g_sod_debug", 1),

      (str_store_faction_name_link, s2, "$g_talk_troop_faction"),
      (assign, reg2, "$g_talk_troop_faction_relation"),
      (assign, reg4, "$g_talk_troop_faction"),
      (display_message, "@{s2} ({reg4}) relation = {reg2}", debug_color),

      (call_script, "script_store_troop_name_link", s1, "$g_talk_troop"),
      (assign, reg1, "$g_talk_troop_relation"),
      (display_message, "@{s1} relation = {reg1}", debug_color),
    (try_end),
    (call_script, "script_setup_talk_info"),
    (eq, 1, 0)
  ], "", "close_window", []],
]
