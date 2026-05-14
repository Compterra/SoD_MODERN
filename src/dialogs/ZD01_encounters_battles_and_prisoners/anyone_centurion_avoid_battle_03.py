DIALOGS = [
[anyone, "centurion_avoid_battle", [
	(assign, ":enable", 0),
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_crusader),
		(assign, ":enable", 1),
		(str_store_string, s0, "@Why, {playername}, your time is the last thing I wish to waste. The first is your blood ! It would be definitely entertaining to watch your rabble of weaklings scurry away with their tails between their legs, but I had enough of playing 'cat-chasing-mice' with you. Know this: what must come to pass here this day is not 'just' a battle ! It is an enormous sacrifice in the name of Marsus ! War for the warrior god ! All of you heretics, lay down and DIE in his name !"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_liberator),
		(assign, ":enable", 1),
		(str_store_string, s0, "@To evacuate ? Where ? To slave themselves half-dead in your mines and manors ? No, {playername}, I won't fall for that trick ! And with that said, you wasted your opportunity to submit peacefully ! As my warriors of freedom and justice will be standing upon your broken bodies and raise the banners of victory high, remember: because of you, lies ended lives !"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_nihilistic),
		(assign, ":enable", 1),
		(str_store_string, s0, "@You can trust me when I say that I don't feel like it either. I planned your mutilation for a later date and I'd prefer to stick to my own deadlines. Hm, I like that word... DEAD-lines... eh, screw the calendar ! I feel inspired ! We'll erect statues from your corpses ! It will be an outstanding example of modern fine arts ! To arms, men ! We have a masterpiece of carnage to create !"),
	(try_end),
	(eq, ":enable", 1),
   ], "{s0}", "close_window", []],
]
