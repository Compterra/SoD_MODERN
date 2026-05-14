DIALOGS = [
[anyone, "militia_awaiting_ransom_fight", [],
   "You won't be demanding anything when you're dead.", "close_window", [
    (quest_get_slot, ":quest_target_party", "qst_serpent_host_free_spy", slot_quest_target_party),
    (set_spawn_radius, 1),
    (spawn_around_party, ":quest_target_party", "pt_sh_spy"),
    (assign, "$g_sh_spy", reg0),
    (try_begin),
      (gt, "$g_sh_spy", 0),
      (party_is_active, "$g_sh_spy"),
      (party_set_ai_behavior, "$g_sh_spy", ai_bhvr_hold),
      (party_set_flags, "$g_sh_spy", pf_default_behavior, 0),
      (quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1),
    (else_try),
      (assign, "$g_sh_spy", 0),
      (display_message, "@The freed spy could not be placed on the map. The fight can wait until the prisoner is located.", 0xFFCC66),
    (try_end),]],
]
