DIALOGS = [
[anyone|plyr, "runaway_serf_intro_1", [(quest_get_slot, ":lord", "qst_bring_back_runaway_serfs", slot_quest_giver_troop),
                                        (call_script, "script_store_troop_name", s4, ":lord")],
   "I have been sent by your {s4} whom you are running from. He will not punish you if you return now.", "runaway_serf_intro_2", []],
]
