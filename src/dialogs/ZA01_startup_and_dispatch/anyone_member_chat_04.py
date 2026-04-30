DIALOGS = [
[anyone, "member_chat", [(store_conversation_troop, "$g_talk_troop"),
                          (troop_is_hero, "$g_talk_troop"),
                          (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                          (str_store_string, s5, ":honorific"),
                          ], "Yes, {playername}?", "member_talk", []],
]
