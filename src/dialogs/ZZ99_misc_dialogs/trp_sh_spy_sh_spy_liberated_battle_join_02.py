DIALOGS = [
[trp_sh_spy, "sh_spy_liberated_battle_join", [], "Then I am with you.",
   "close_window", [(party_add_members, "p_main_party", "trp_sh_spy", 1),
                    (quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1),
                    (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_free_captives, 1)]],
]
