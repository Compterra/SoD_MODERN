DIALOGS = [
[trp_sod_marshal, "marshal_upgrade_check",
    [
      # only present this if there are NO troops to upgrade at all...
      (assign, ":total", 0),
	  (try_for_range, ":troop_no", 0, "trp_last_troop"),
			(party_count_companions_of_type, ":troop_count", "p_main_party", ":troop_no"),
			(troop_get_slot, ":upgrade1", ":troop_no", slot_troop_sod_upgrade1),
			(troop_get_slot, ":upgrade2", ":troop_no", slot_troop_sod_upgrade2),
			(this_or_next|is_between, ":upgrade1", 1, "trp_last_troop"),
			(is_between, ":upgrade2", 1, "trp_last_troop"),
			(val_add, ":total", ":troop_count"),
	  (try_end),
      (eq, ":total", 0),
    ], "No troops in your party can be promoted, my liege. Bring me trained soldiers with a valid promotion path.", "marshal_talk_again", []],
]
