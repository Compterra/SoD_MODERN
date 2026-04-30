DIALOGS = [
[trp_sod_marshal|plyr|repeat_for_troops, "marshal_upgrade_which",
    [
      (store_repeat_object, ":troop_no"),
	(troop_get_slot, ":upgrade1", ":troop_no", slot_troop_sod_upgrade1),
	(troop_get_slot, ":upgrade2", ":troop_no", slot_troop_sod_upgrade2),
	(this_or_next|is_between, ":upgrade1", 1, "trp_last_troop"),
	(is_between, ":upgrade2", 1, "trp_last_troop"),
      (party_count_companions_of_type, ":troop_count", "p_main_party", ":troop_no"),
      (gt, ":troop_count", 0),
      (str_store_troop_name_by_count, s1, ":troop_no", ":troop_count"),
      (assign, reg1, ":troop_count"),
      (str_store_string, s2, "@{reg1}"),
    ],
    "{s2} {s1}", "marshal_upgrade_list_options",
    [
      (assign, "$can_upgrade1", 0),
      (assign, "$can_upgrade2", 0),

      # store which troop we're upgrading
      (store_repeat_object, "$g_upgrade_troop"),
      (party_count_companions_of_type, ":troop_count", "p_main_party", "$g_upgrade_troop"),
      (assign, "$upgrade_count", ":troop_count"),

      # and determine whether this center has the facilities to upgrade this unit at all...
      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),
      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),
      (troop_get_slot, ":center_no", "trp_sod_marshal", slot_troop_sod_court),
      (call_script, "script_sod_can_upgrade_troops_here", ":upgrade1", ":center_no"),
      (assign, "$can_upgrade1", reg0),
      (call_script, "script_sod_can_upgrade_troops_here", ":upgrade2", ":center_no"),
      (assign, "$can_upgrade2", reg0),

      (assign, reg1, "$can_upgrade1"),
      (assign, reg2, "$can_upgrade2"),

      ### DEBUG ###
      (try_begin),
        (eq, "$g_sod_debug", 1),
        (eq, 1, 0), # DISABLE
        (call_script, "script_store_troop_name", s1, ":upgrade1"),
        (assign, reg0, ":upgrade1"),
        (display_message, "@upgrade1 = {s1} ({reg0})", debug_color),
        (call_script, "script_store_troop_name", s1, ":upgrade2"),
        (assign, reg0, ":upgrade2"),
        (display_message, "@upgrade2 = {s1} ({reg0})", debug_color),
        (display_message, "@$can_upgrade1 = {reg1}, $can_upgrade2 = {reg2}", debug_color),
      (try_end),
    ]
  ],
]
