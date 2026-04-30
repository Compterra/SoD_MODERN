DIALOGS = [
[anyone|plyr, "troublesome_bandits_intro_1", [],
   "Heh. For me, you are nothing more than walking money bags.\
 A merchant in {s1} offered me good money for your heads.",
   "troublesome_bandits_intro_2", [(quest_get_slot, ":quest_giver_center", "qst_troublesome_bandits", slot_quest_giver_center),
                                   (str_store_party_name, s1, ":quest_giver_center")
                                   ]],
]
