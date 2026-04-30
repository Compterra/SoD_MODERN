DIALOGS = [
[anyone|plyr, "runaway_serf_intro_3", [], "Well, maybe you are right. All right then. If anyone asks, I haven't seen you.", "runaway_serf_let_go",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],
]
