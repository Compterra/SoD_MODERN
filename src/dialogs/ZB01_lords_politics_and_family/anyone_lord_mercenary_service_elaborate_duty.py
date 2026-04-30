DIALOGS = [
[anyone, "lord_mercenary_service_elaborate_duty", [],
   "Duties... There are only a few, none of them difficult. The very first thing is to declare your allegiance.\
 An oath of loyalty to our cause. Once that's done, you shall be required to fulfill certain responsibilities.\
 You'll participate in military campaigns, fulfill any duties given to you by your commanders,\
 and most of all you shall attack the enemies of our kingdom wherever you might find them.", "lord_mercenary_elaborate_1",
   [(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
    (call_script, "script_store_troop_name", s10, ":faction_leader")]],
]
