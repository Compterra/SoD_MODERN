SCRIPTS = [
("game_get_party_companion_limit",
    [
      (assign, ":troop_no", "trp_player"),

      (assign, ":limit", 9),

      (store_skill_level, ":skill", "skl_leadership", ":troop_no"),
      (try_begin),
        #MORDACHAI - double their effective leadership if they're king
        (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
        (val_mul, ":skill", 2),
      (try_end),

      #MORDACHAI - increase troop limit by 10 x leadership skill (was 5x)
      (val_mul, ":skill", 10),
      (val_add, ":limit", ":skill"),

      # give them 1x CHA bonus to troop limit
      (store_attribute_level, ":charisma", ":troop_no", ca_charisma),
      (val_add, ":limit", ":charisma"),
	   #SoD Law
	  (val_add, ":limit", "$g_sod_pc_party_size_modifier"), #from laws


      # extra troop per 25 renown
      (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
      (store_div, ":renown_bonus", ":troop_renown", 25),
      (val_add, ":limit", ":renown_bonus"),

      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
  ]),
]
