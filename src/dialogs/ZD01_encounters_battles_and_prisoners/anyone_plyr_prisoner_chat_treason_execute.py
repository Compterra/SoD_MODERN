DIALOGS = [
[anyone|plyr, "prisoner_chat_treason_execute", [],
    "(The prisoner struggles against his shackles, desperate to free himself and escape you, but to no avail. You slit his throat and watch, satisfied, as his corpse sags to the floor.)",
    "close_window",
    [
      # make sure we don't try to recruit this prisoner stack later!
      (troop_set_slot, "$g_talk_troop", slot_prisoner_agreed, 0),

      # "kill" the NPC - force the 48 hr respawn kingdom heros trigger to ignore this troop (no party will be created for this troop, ever again)
      # [q.v. script_create_kingdom_hero_party]
      (call_script, "script_sod_runtime_trace_event", 5, "$g_enemy_party", "$g_talk_troop"),
      (call_script, "script_kill_kingdom_hero", "$g_talk_troop"),

      # determine the penalty for this act (based on the honor of the troop they've killed)
      (troop_get_slot, ":renown", "$g_talk_troop", slot_troop_renown),
      (store_div, ":impact", ":renown", -33),  # native quirk: negative divisor => negative impact (relation penalty)
      (store_div, ":half", ":impact", 2),

      # don't overwhlem the display with too many messages, otherwise it won't show any of them
      (set_show_messages, 0),

      # reduce the player's relationship with every village, town, and castle
      (try_for_range, ":center", centers_begin, centers_end),
        (store_faction_of_party, ":faction", ":center"),
        (store_relation, ":relation", ":faction", "$g_talk_troop_faction"),
        (try_begin),
          (le, ":relation", -10),
          # enemies, half impact
          (call_script, "script_change_player_relation_with_center", ":center", ":half"),
        (else_try),
          # not at war, full impact
          (call_script, "script_change_player_relation_with_center", ":center", ":impact"),
        (try_end),
      (try_end),

      # reduce the player's relationship with every hero, companion, lady, and daughter
      (try_for_range, ":troop", trp_npc1, trp_heroes_end),
        # don't make the dead any angrier than they already are!
        (neg|troop_slot_eq, ":troop", slot_troop_occupation, slto_dead),
        (store_troop_faction, ":faction", ":troop"),
        (store_relation, ":relation", ":faction", "$g_talk_troop_faction"),
        (try_begin),
          (le, ":relation", -10),
          # enemies, half impact
          (call_script, "script_change_player_relation_with_troop", ":troop", ":half"),
        (else_try),
          # not at war, full impact
          (call_script, "script_change_player_relation_with_troop", ":troop", ":impact"),
        (try_end),
      (try_end),

      # don't overwhlem the display with too many messages, otherwise it won't show any of them
      (set_show_messages, 1),

      # reduce the player's relationship with every faction (enemies 1/2 as much)
      (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
        (store_relation, ":relation", ":faction", "$g_talk_troop_faction"),
        (try_begin),
          (le, ":relation", -10),
          # enemies, half impact
          (call_script, "script_change_player_relation_with_faction", ":faction", ":half"),
        (else_try),
          # not at war, full impact
          (call_script, "script_change_player_relation_with_faction", ":faction", ":impact"),
        (try_end),
      (try_end),

      # apply the honor hit
      (call_script, "script_change_player_honor", ":impact"),
      (call_script, "script_sod_diplomacy_record_event", "$g_talk_troop_faction", sod_diplomacy_memory_executed_lord, 1),
      (call_script, "script_sod_companion_apply_player_action", sod_companion_action_execute_lord, 6),

      # party morale takes a hit as well
      (call_script, "script_change_player_party_morale", ":half"),

      # but give them renown for this evil deed (their deed spreads upon every tongue, impressing some, and cowing others)
      (val_mul, ":impact", -1),
      (call_script, "script_change_troop_renown", "trp_player" , ":impact"),

      # no longer our prisoner
      (call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
      (remove_troops_from_prisoners, "$g_talk_troop", 1),
    ]
  ],
]
