DIALOGS = [
[trp_kidnapped_girl, "kidnapped_girl_liberated_battle_2a", [], "Oh really? Thank you so much!",
   "close_window", [(party_add_members, "p_main_party", "trp_kidnapped_girl", 1),
                   (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_free_captives, 1),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   ]],
]
