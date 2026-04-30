DIALOGS = [
[anyone, "boar_clan_introduce", [
    (store_random_in_range, ":rand", 0, 2),
	(try_begin),
		(eq, ":rand", 0),
		(store_party_size, reg5, "$g_encountered_party"),
		(val_mul, reg5, 10),
        (str_store_string, s5, "@Hold it there, wanderer! This territory is under our control. If you want to pass by, you have to pay a passage tax for using our roads - {reg5} denars to be exact."),
		(assign, "$g_sod_demand_money", "$g_encountered_party"),
	(else_try),
		(str_store_string, s5, "@Come on lads, to arms! These guys look like up for some brawlin'! Let's tear 'em limb from limb!"),
    (try_end),
	], "{s5}", "boar_clan_talk", [(play_sound, "snd_encounter_bandits")]],
]
