DIALOGS = [
[anyone, "tavernkeeper_companion_klethi_contact",
    [
        (try_begin),
            (eq, "$g_sod_klethi_old_job_cause", 2),
            (str_store_string, s4, "@chain-buyers, the sort who drink cheap and count wrists before faces"),
        (else_try),
            (str_store_string, s4, "@road collectors, the sort who pay in horde coin and leave doors unlocked from the wrong side"),
        (try_end),
    ],
    "Quietly, then. The mark came with {s4}. They wanted the small woman with quick hands and quicker exits. I would not sell her name twice.",
    "tavernkeeper_talk",
    [
        (assign, "$g_sod_klethi_old_job_contacted", 1),
        (assign, "$g_sod_klethi_old_job_clue_bits", 1),
        (quest_set_slot, "qst_companion_klethi_knife_with_name", slot_quest_sod_runtime_progress, 50),
        (quest_set_slot, "qst_companion_klethi_knife_with_name", slot_quest_sod_runtime_last_center, "$current_town"),
        (call_script, "script_sod_companion_apply_player_action", sod_companion_action_scout_warning, 1),
        (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc16"),
        (display_message, "@A tavernkeeper confirms Klethi's old-job mark. A Knife With a Name now has an underworld witness.", 0x99CCFF),
    ]],
]
