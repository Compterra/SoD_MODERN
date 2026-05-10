DIALOGS = [
[anyone, "start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_slavers_bring_back_runaway_slaves"),
						 (quest_slot_eq, ":lords_quest", slot_quest_giver_center, "$g_encountered_party"),
                         (check_quest_failed, "qst_slavers_bring_back_runaway_slaves"), ],
   "{playername}. I have been waiting patiently for my slaves, yet none have returned. Have you an explanation?\
 Were you outwitted by simple fieldhands, or are you merely incompetent?\
 Or perhaps you are plotting with my enemies, intending to ruin me...", "gm_bring_back_runaway_slaves_failed", []],
]
