DIALOGS = [
[party_tpl|pt_mercenary_lord_party, "start", [(eq, "$talk_context", tc_party_encounter), (neg|encountered_party_is_attacker)],
   "Yes?", "merc_lord_talk", []],
]
