DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_bring_back_runaway_serfs"),
                         (check_quest_failed, "qst_bring_back_runaway_serfs"), ],
   "{playername}. I have been waiting patiently for my serfs, yet none have returned. Have you an explanation?\
 Were you outwitted by simple fieldhands, or are you merely incompetent?\
 Or perhaps you are plotting with my enemies, intending to ruin me...", "lord_bring_back_runaway_serfs_failed", []],
]
