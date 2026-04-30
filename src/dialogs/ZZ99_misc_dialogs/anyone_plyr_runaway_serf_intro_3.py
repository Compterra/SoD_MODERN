DIALOGS = [
[anyone|plyr, "runaway_serf_intro_3", [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (str_store_party_name, s1, ":quest_object_center"), ],
   "You have gone against our laws by running from your bondage. You will go back to {s1} now!", "runaway_serf_go_back",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", -1)]],
]
