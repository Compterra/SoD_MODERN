DIALOGS = [
[trp_sod_marshal, "marshal_field_marshall_direct3", [
  (faction_get_slot, ":new_marshall", "fac_player_supporters_faction", slot_faction_marshall),
  (call_script, "script_store_troop_name", s31, ":new_marshall"),
  (str_store_faction_name, s32, "fac_player_supporters_faction"),
  ], "Very well, {s31} is the new Field Marshall of {s32}.", "marshal_talk_again", []],
]
