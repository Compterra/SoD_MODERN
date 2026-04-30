DIALOGS = [
[anyone, "lord_start",
   [
     (check_quest_active, "qst_follow_army"),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
     (eq, "$g_random_army_quest", "qst_scout_waypoints"),
     (str_store_party_name, s13, "$qst_scout_waypoints_wp_1"),
     (str_store_party_name, s14, "$qst_scout_waypoints_wp_2"),
     (str_store_party_name, s15, "$qst_scout_waypoints_wp_3"),
     ],
   "{playername}, I need a volunteer to scout the area. We're sorely lacking on information,\
 and I simply must have a better picture of the situation before we can proceed.\
 I want you to go to {s13}, {s14} and {s15} and report back whatever you find.", "lord_mission_told_scout_waypoints",
   [
   ]],
]
