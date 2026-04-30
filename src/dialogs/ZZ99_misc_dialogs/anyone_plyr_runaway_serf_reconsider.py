DIALOGS = [
[anyone|plyr, "runaway_serf_reconsider", [], "I have changed my mind. You must back to your village!", "runaway_serf_go_back",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 0),
    (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", -2)]],
]
