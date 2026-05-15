DIALOGS = [
[anyone|plyr, "elephant_guard_world_rites_talk", [], "Stand aside. I mean to fight you.", "close_window", [
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
]],
]
