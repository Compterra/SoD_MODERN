DIALOGS = [
[trp_sod_strategy_advisor, "member_chat", [
                          (main_party_has_troop, "trp_sod_strategy_advisor"),
                          ], "The map is still open. Choose the next thread, and I will pull it straight.", "startegy_advisor_continue", [
                          (assign, "$sa_talk_after_siege", 0),
                          ]],
[anyone, "member_chat", [(store_conversation_troop, "$g_talk_troop"),
                          (neq, "$g_talk_troop", "trp_sod_strategy_advisor"),
                          (troop_is_hero, "$g_talk_troop"),
                          (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                          (str_store_string, s5, ":honorific"),
                          ], "Yes, {playername}?", "member_talk", []],
]
