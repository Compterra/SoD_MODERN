DIALOGS = [
[anyone|plyr, "gm_talk", [(store_partner_quest, ":elder_quest"),
                                                 (eq, ":elder_quest", "qst_elephant_guard_capture_the_bastard"),
                                                 (party_count_prisoners_of_type, ":is_captured", "p_main_party", "trp_khergit_chieftain"),
												 (gt, ":is_captured", 0),
                                                 ],
   "I brought you this bloody bastard.", "gm_deliver_bastard_thank",
   []],
]
