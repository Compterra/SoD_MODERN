DIALOGS = [
[anyone, "militia_awaiting_ransom_fight", [],
   "You won't be demanding anything when you're dead.", "close_window", [
    (quest_get_slot, ":quest_target_party", "qst_serpent_host_free_spy", slot_quest_target_party),
    (set_spawn_radius, 1),
    (spawn_around_party, ":quest_target_party", "pt_sh_spy"),
    (assign, "$g_sh_spy", reg0),
    (party_set_ai_behavior, "$g_sh_spy", ai_bhvr_hold),
    (party_set_flags, "$g_sh_spy", pf_default_behavior, 0),
	(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1),]],
]
