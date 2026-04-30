DIALOGS = [
[anyone, "mayor_info_lord", [(party_get_slot, ":town_lord", "$current_town", slot_town_lord), (call_script, "script_store_troop_name", s10, ":town_lord")],
   "Our town's lord and protector is {s10}. He owns the castle and sometimes resides there, and collects taxes from the town.\
 However we regulate ourselves in most of the matters that concern ourselves.\
 As the town's guildmaster I have the authority to decide those things.", "mayor_info_talk", [(assign, "$mayor_info_lord_told", 1)]],
]
