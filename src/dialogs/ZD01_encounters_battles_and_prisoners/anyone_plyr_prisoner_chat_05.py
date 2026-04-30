DIALOGS = [
[anyone|plyr, "prisoner_chat", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero), (call_script, "script_store_troop_name", s1, "$g_talk_troop"),(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_mercenary_lord)], "{s1}", "prisoner_chat_lord", []],
]
