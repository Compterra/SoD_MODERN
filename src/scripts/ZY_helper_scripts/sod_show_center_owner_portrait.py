# COST: trivial
SCRIPTS = [
("sod_show_center_owner_portrait",
  [
    (store_script_param, ":center_no", 1),

    (try_begin),
      (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
      (is_between, ":center_lord", 0, "trp_last_troop"),
      (call_script, "script_sod_show_troop_portrait", ":center_lord"),
    (try_end),
  ]),
]
