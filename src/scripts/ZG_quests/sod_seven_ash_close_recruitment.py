SCRIPTS = [
("sod_seven_ash_close_recruitment",
    [
      (try_begin),
        (quest_get_slot, ":resolved", "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_resolved_count),
        (ge, ":resolved", 3),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_complete, 0),

        (call_script, "script_sod_seven_ash_set_defender_status", sod_seven_ash_defender_garric, sod_seven_ash_recruit_abandoned),
        (call_script, "script_sod_seven_ash_set_defender_status", sod_seven_ash_defender_oswin, sod_seven_ash_recruit_abandoned),
        (call_script, "script_sod_seven_ash_set_defender_status", sod_seven_ash_defender_aldrik, sod_seven_ash_recruit_abandoned),
        (call_script, "script_sod_seven_ash_set_defender_status", sod_seven_ash_defender_mirelle, sod_seven_ash_recruit_abandoned),
        (call_script, "script_sod_seven_ash_set_defender_status", sod_seven_ash_defender_tomas, sod_seven_ash_recruit_abandoned),
        (call_script, "script_sod_seven_ash_set_defender_status", sod_seven_ash_defender_beren, sod_seven_ash_recruit_abandoned),
        (call_script, "script_sod_seven_ash_set_defender_status", sod_seven_ash_defender_elianor, sod_seven_ash_recruit_abandoned),

        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_complete, 1),
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_return),
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_recruit_id, sod_seven_ash_defender_none),
        (str_store_string, s49, "@The search for defenders is closed. Unresolved roads are marked abandoned, and Ashwick waits for the player to return with whoever was won, paid, coerced, or spared."),
        (add_quest_note_from_sreg, "qst_seven_ash_return_to_ashwick", 1, s49, 0),
      (try_end),
  ]),
]
