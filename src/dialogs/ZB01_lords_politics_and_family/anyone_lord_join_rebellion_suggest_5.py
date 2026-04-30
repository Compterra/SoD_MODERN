DIALOGS = [
[anyone, "lord_join_rebellion_suggest_5", [
        (lt, "$rebellion_check", "$rebellion_chance"),
      ], "{s43}", "lord_join_rebellion_ask_for_order",
   [

        (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_agree_default"),

        (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
        (call_script, "script_change_troop_faction", "$g_talk_troop", "$players_kingdom"),
        (troop_get_slot, ":lords_party", "$g_talk_troop", slot_troop_leaded_party),
        (party_set_faction, ":lords_party", "$players_kingdom"),
        (assign, "$g_leave_encounter", 1),
    ]],
]
