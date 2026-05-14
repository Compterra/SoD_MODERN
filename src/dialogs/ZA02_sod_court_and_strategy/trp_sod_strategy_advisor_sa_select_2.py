DIALOGS = [
[trp_sod_strategy_advisor, "sa_select_2", [
	(try_begin),
		(eq, "$g_sod_sa_talk_subject", 1),
		(str_store_string, s1, "@I can tell you about Swadians, Vaegirs, Khergits, Nords, and Rhodoks."),
	(else_try),
		(eq, "$g_sod_sa_talk_subject", 2),
		(str_store_string, s1, "@I can tell you about Antares, Marina, Aden, Villian, and Zerrikania."),
	(else_try),
		(eq, "$g_sod_sa_talk_subject", 3),
		(str_store_string, s1, "@I can tell you about the Black Army, Boar Clan, Conquistadors, Elephant Guard, Jotnar Clan, Serpent Host, and Slavers."),
	(else_try),
		(str_store_string, s1, "@Which culture do you mean, my liege?"),
	(try_end),
], "{s1}", "sa_select_2_answer", []],
]
