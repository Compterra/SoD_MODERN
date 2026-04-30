DIALOGS = [
[anyone, "lord_mercenary_elaborate_pay", [(assign, reg12, "$temp")],
   "I can offer you a contract for three months. At the end of those three, it can be extended month by month.\
 An initial sum of {reg12} denars will be paid to you to seal the contract.\
 After that, you'll receive wages from {s10} each week, according to the number and quality of the soldiers in your company.\
 You still have your rights to battlefield loot and salvage, as well as any prisoners you capture.\
 War can be very profitable at times...", "lord_mercenary_elaborate_1",
   [(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
    (call_script, "script_store_troop_name", s10, ":faction_leader")]],
]
