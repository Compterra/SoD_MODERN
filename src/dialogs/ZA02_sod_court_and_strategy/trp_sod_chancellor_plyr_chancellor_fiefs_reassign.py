DIALOGS = [
[trp_sod_chancellor|plyr, "chancellor_fiefs_reassign",
    [
      # don't include ourselves as an option if we already own it
      (neg|party_slot_eq, "$assign_fief", slot_town_lord, "trp_player"),
    ],
    "I want it for Myself.", "chancellor_fiefs_prelude",
    [
      # adjust relations for stripping them of their fief
      (try_begin),
        # take this center away from the old lord
        (party_get_slot, ":old_lord", "$assign_fief", slot_town_lord),
        (gt, ":old_lord", "trp_player"),
        (call_script, "script_change_player_relation_with_troop", ":old_lord", -10),
        # take each of the bound villages away from their lords
        (try_for_range, ":village", villages_begin, villages_end),
          (party_slot_eq, ":village", slot_village_bound_center, "$assign_fief"),
          (party_get_slot, ":old_lord", ":village", slot_town_lord),
          (gt, ":old_lord", "trp_player"),
          (call_script, "script_change_player_relation_with_troop", ":old_lord", -10),
        (try_end),
      (try_end),
      # give it and all of its bound villages to the player
      (call_script, "script_give_center_to_lord", "$assign_fief",  "trp_player", 0),
    ]
  ],
]
