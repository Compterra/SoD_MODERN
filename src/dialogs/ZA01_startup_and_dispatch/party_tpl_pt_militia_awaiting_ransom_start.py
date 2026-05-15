DIALOGS = [
[party_tpl|pt_militia_awaiting_ransom, "start", [(check_quest_active, "qst_serpent_host_free_spy"), 
		(neg|quest_slot_eq, "qst_serpent_host_free_spy", slot_quest_current_state, 1), ],
   "Are you the one with the ransom for this spy? Quick, give us the money.", "militia_awaiting_ransom_intro_1", []],
]
