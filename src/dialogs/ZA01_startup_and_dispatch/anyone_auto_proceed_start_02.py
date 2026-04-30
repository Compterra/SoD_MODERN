DIALOGS = [
[anyone|auto_proceed, "start", [(eq, "$talk_context", tc_hero_defeated),
                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),			
					(is_between, "$g_talk_troop", "trp_knight_6_01", "trp_black_army_leader_1"),
					(eq, "$g_talk_troop_faction", "fac_kingdom_6"),
					],
   "none", "cpdla_defeat_lord_answer",
   []],
]
