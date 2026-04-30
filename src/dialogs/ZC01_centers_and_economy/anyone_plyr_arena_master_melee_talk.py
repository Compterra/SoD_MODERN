DIALOGS = [
[anyone|plyr, "arena_master_melee_talk", [], "Good. That's what I am going to do.", "close_window",
   [
    (assign, "$last_training_fight_town", "$current_town"),
    (store_current_hours, "$training_fight_time"),
    (assign, "$g_mt_mode", abm_training),
    (party_get_slot, ":scene", "$current_town", slot_town_arena),
    (modify_visitors_at_site, ":scene"),
    (reset_visitors),
    (store_random_in_range, "$g_player_entry_point", 32, 40),
    (set_visitor, "$g_player_entry_point", "trp_player"),
    (set_jump_mission, "mt_arena_melee_fight"),
    (jump_to_scene, ":scene"),
    ]],
]
