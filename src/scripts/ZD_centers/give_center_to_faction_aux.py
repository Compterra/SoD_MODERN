SCRIPTS = [
("give_center_to_faction_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      (store_faction_of_party, ":old_faction", ":center_no"),
      (party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party", 0),
        (party_is_active, ":farmer_party"),
        (party_set_faction, ":farmer_party", ":faction_no"),
      (try_end),

      (party_get_slot, ":old_town_lord", ":center_no", slot_town_lord),
      (party_set_slot, ":center_no", slot_town_lord, stl_unassigned),
      (party_set_banner_icon, ":center_no", 0), #Removing banner

      (call_script, "script_update_faction_notes", ":old_faction"),
      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),
      (try_begin),
        (ge, ":old_town_lord", 0),
        (call_script, "script_update_troop_notes", ":old_town_lord"),
      (try_end),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        (call_script, "script_give_center_to_faction_aux", ":other_center", ":faction_no"),
      (try_end),
  ]),
]
