DIALOGS = [
[anyone, "town_dweller_companion_deshavi_survivor",
    [
        (try_begin),
            (eq, "$g_sod_deshavi_trail_warning_cause", 2),
            (str_store_string, s4, "@I saw wrists raw from rope, and riders asking after them like men asking after lost coin"),
        (else_try),
            (str_store_string, s4, "@I saw hungry folk cut through the fields by moonlight, too afraid to beg and too tired to hide well"),
        (try_end),
    ],
    "{s4}. Your tracker looked where others looked away.",
    "town_dweller_talk",
    [
        (assign, "$g_sod_deshavi_trail_witnessed", 1),
        (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_last_center, "$current_town"),
        (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 50),
        (call_script, "script_sod_companion_apply_player_action", sod_companion_action_scout_warning, 1),
        (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
        (display_message, "@A villager confirms Deshavi's trail signs. Tracks Through Ash now has a living witness.", 0x99CCFF),
    ]],
]
