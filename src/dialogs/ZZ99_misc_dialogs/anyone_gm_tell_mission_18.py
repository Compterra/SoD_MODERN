DIALOGS = [
[anyone, "gm_tell_mission", [
   (eq, "$random_quest_no", "qst_jotnar_clan_revenge"),
   (quest_get_slot, ":target_center", "qst_jotnar_clan_revenge", slot_quest_target_center),
   (str_store_party_name_link, s8, ":target_center"),
   (try_begin),
		(quest_slot_eq, "qst_jotnar_clan_revenge", slot_quest_target_troop, "trp_slave_hunter"),
        (str_store_string, s5, "@vile Slavers"),
	(else_try),
		(quest_slot_eq, "qst_jotnar_clan_revenge", slot_quest_target_troop, "trp_black_army_line_keeper"),
        (str_store_string, s5, "@rogue mercenaries"),
	(else_try),
        (str_store_string, s5, "@back-stabbing Nord traitors"),
	(try_end),
   ],
 "It just happens that a small band of Disirs and Einherjars wish to take revenge on the same group of people for the loss of loved ones: a band of {s5}. We came to know that those folks are currently taking a rest in {s8}. Alas, alone, even the determined Einherjars and Disirs couldn't defeat them, and we may not help either for many of our brothers and sisters have to be mustered against other foes. But you could asisst them. Take them with you and show how the children of Fenrir deal with their enemies.", "gm_revange_quest_brief",
   []],
]
