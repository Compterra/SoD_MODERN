SCRIPTS = [
("update_all_notes",
      [
        (call_script, "script_update_troop_notes", "trp_player"),
        (try_for_range, ":troop_no", kingdom_heroes_begin, "trp_knight_1_1_wife"),
          (call_script, "script_update_troop_notes", ":troop_no"),
        (try_end),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (call_script, "script_update_center_notes", ":center_no"),
        (try_end),
        (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
          (call_script, "script_update_faction_notes", ":faction_no"),
        (try_end),
		(try_for_range, ":faction_no", "fac_sod_merc_guild1", "fac_kingdom_6_mercenaries"),
          (call_script, "script_update_faction_notes", ":faction_no"),
        (try_end),
    ]),
]
