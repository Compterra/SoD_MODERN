DIALOGS = [
[anyone, "gm_hire2", [
		(eq, "$g_talk_troop", slavers_rep),
		(assign, ":dist", 10000),
		(try_for_range, ":town", towns_begin, towns_end),
			(party_slot_ge, ":town", slot_town_slavers, 1),
			(store_distance_to_party_from_party, ":dist_2", ":town", "$g_encountered_party"),
			(lt, ":dist_2", ":dist"),
			(assign, ":dist", ":dist_2"),
			(str_store_party_name, s17, ":town"),
		(try_end),
   ],"We have some unemployed men in {s17}.^^How much soldiers do you want to hire?", "gm_hire3", []],
]
