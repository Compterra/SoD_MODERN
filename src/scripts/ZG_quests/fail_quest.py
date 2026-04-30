SCRIPTS = [
("fail_quest",
      [(store_script_param, ":quest_no", 1),
        (fail_quest, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (call_script, "script_store_troop_name_link_fief", s59, ":quest_giver_troop"),
        (add_quest_note_from_sreg, ":quest_no", 7, "@This quest has failed. Talk to {s59} to explain the situation.", 0),
        (call_script, "script_sod_quest_runtime_fail", ":quest_no", ":quest_giver_troop"),
    ]),
]
