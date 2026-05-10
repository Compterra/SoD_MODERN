SCRIPTS = [
("succeed_quest",
      [(store_script_param, ":quest_no", 1),
        (succeed_quest, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (call_script, "script_store_troop_name_link_fief", s59, ":quest_giver_troop"),
        (str_store_string, s49, "@This quest has been successfully completed. Talk to {s59} to claim your reward."),

        (add_quest_note_from_sreg, ":quest_no", 7, s49, 0),
        (call_script, "script_sod_quest_runtime_complete", ":quest_no", ":quest_giver_troop"),
    ]),
]
