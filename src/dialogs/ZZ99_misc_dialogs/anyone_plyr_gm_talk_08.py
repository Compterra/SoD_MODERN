DIALOGS = [
[anyone|plyr, "gm_talk", [(store_partner_quest, ":partner_quest"),
                               (eq, ":partner_quest", "qst_serpent_host_free_spy"),
							   (check_quest_active, "qst_serpent_host_free_spy"),
							   (neg|main_party_has_troop, "trp_sh_spy"),
							   (check_quest_failed, "qst_serpent_host_free_spy"),
                               ],
   "Unfortunately I lost the spy on the way here...", "lost_sh_spy", []],
]
