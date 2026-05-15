DIALOGS = [
[anyone, "cp_liberator_5", [
	(store_random_in_range, ":rand", 0, 2),
	(try_begin),
		(eq, ":rand", 0),
		(str_store_string, s68, "@Order of the Hospitalier"),
	(else_try),
		(eq, ":rand", 1),
		(str_store_string, s68, "@Praetorian Guard"),
	(else_try),
		(str_store_string, s68, "@Akolouthos, also known as 'Acolytes of the Emperor'"),
	(try_end),
	], "So... it is you, the supreme overlord of the {s32} people. So to say, I imagined you differently. I expected someone... taller and more intimidating. Someone who actually does look and behave like a sworn enemy of the empire. However, I suppose looks are secondary in this situation. I am {s29}, a leader of the Imperial Legion and honorary member of the {s68}.", "cp_liberator_6", [] ],
]
