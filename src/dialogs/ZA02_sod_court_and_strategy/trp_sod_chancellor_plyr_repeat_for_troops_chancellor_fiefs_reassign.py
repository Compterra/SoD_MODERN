DIALOGS = [
[trp_sod_chancellor|plyr|repeat_for_troops, "chancellor_fiefs_reassign",
    [
      (store_repeat_object, ":new_lord"),

      # only relevant to our lords
      (is_between, ":new_lord", kingdom_heroes_begin, kingdom_heroes_end),
      (troop_slot_eq, ":new_lord", slot_troop_occupation, slto_kingdom_hero),

      # don't allow us to assign a fief to a new_lord that hasn't officially joined us yet!
      (store_troop_faction, ":faction_no", ":new_lord"),
      (eq, ":faction_no", "fac_player_supporters_faction"),

      # don't give the player the option to give it to the lord that already owns it (pointless, one less menu to scroll through)
      (neg|party_slot_eq, "$assign_fief", slot_town_lord, ":new_lord"),

      # generate the talk text
#      (str_store_party_name, s1, "$assign_fief"),
#      (try_begin),
#        (party_slot_eq, "$assign_fief", slot_party_type, spt_village),
#        (party_get_slot, ":bound_to", "$assign_fief", slot_village_bound_center),
#        (str_store_party_name, s2, ":bound_to"),
#        (str_store_string, s1, "@The village of {s1} bound to {s2}"),
#      (try_end),

      (call_script, "script_store_troop_name", s2, ":new_lord"),
      (call_script, "script_troop_get_player_relation", ":new_lord"),
      (call_script, "script_describe_troop_relation", s3, reg0),
      (call_script, "script_get_number_of_hero_centers", ":new_lord"),
    ],
#    "Assign {s1} to {s2} ({reg0?{reg0}:no} fiefs, {s3})", "chancellor_fiefs_prelude",
    "Assign to {s2} ({reg0?{reg0}:no} fiefs, {s3})", "chancellor_fiefs_prelude",
    [
      (store_repeat_object, "$temp_lord"),

      (assign, ":count", 1),
      (try_begin),
        # adjust relations for stripping the previous owner of their fief
        (party_get_slot, ":old_lord", "$assign_fief", slot_town_lord),
        (gt, ":old_lord", "trp_player"),
        (call_script, "script_change_player_relation_with_troop", ":old_lord", -10),
        # take each of the bound villages away from their lords (and determine the count of centers that we're giving to this lord in total)
        (try_for_range, ":village", villages_begin, villages_end),
          (party_slot_eq, ":village", slot_village_bound_center, "$assign_fief"),
          (party_get_slot, ":old_lord", ":village", slot_town_lord),
          (gt, ":old_lord", "trp_player"),
          (neq, ":old_lord", "$temp_lord"),
          (call_script, "script_change_player_relation_with_troop", ":old_lord", -10),
          (val_add, ":count", 1),
        (try_end),
      (try_end),

      # give it to selected lord (and all bound villages)
      (call_script, "script_give_center_to_lord", "$assign_fief",  "$temp_lord", 0),

      # positive relation for giving new owner the fief
      (val_mul, ":count", 10),
      (call_script, "script_change_player_relation_with_troop", "$temp_lord", ":count"),
	  (call_script, "script_update_titles"),
    ]
  ],
]
