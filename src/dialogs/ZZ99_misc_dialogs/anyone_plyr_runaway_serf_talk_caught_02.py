DIALOGS = [
[anyone|plyr, "runaway_serf_talk_caught", [], "Well, if you are that eager to go, then go.", "runaway_serf_let_go",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],
]
