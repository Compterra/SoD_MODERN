DIALOGS = [
[anyone, "town_dweller_companion_ymira_refugee",
    [
        (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
        (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
        (store_add, reg1, ":male_slaves", ":female_slaves"),
        (val_max, reg1, "$g_sod_ymira_refugee_captive_count"),
    ],
    "One house cannot carry {reg1} souls. But one house can carry one name, one bowl, one warning shouted from the door. Tell the healer-woman not to leave them unnamed.",
    "town_dweller_talk",
    [
        (assign, "$g_sod_ymira_refugee_witnessed", 1),
        (quest_set_slot, "qst_companion_ymira_mercy_under_arms", slot_quest_sod_runtime_progress, 50),
        (quest_set_slot, "qst_companion_ymira_mercy_under_arms", slot_quest_sod_runtime_last_center, "$current_town"),
        (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 1),
        (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc3"),
        (display_message, "@A villager agrees to shelter one of Ymira's refugees. Mercy Under Arms now has a human witness.", 0x99CCFF),
    ]],
]
