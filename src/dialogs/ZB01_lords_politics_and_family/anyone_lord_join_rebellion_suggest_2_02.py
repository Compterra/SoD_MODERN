DIALOGS = [
[anyone, "lord_join_rebellion_suggest_2", [
            (gt, "$rival_lord", 0),
      ], "{s43}", "lord_join_rebellion_suggest_2",
   [
            (call_script, "script_store_troop_name", 44, "$rival_lord"),
            (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_rival_default"),

            (assign, "$rival_lord", 0),

            (val_sub, "$rebellion_chance", 30),

            (assign, reg7, "$rebellion_chance", debug_color), #diagnostic only
            (display_message, "@Rebellion chance -30 from rival = {reg7}", debug_color), #diagnostic only

    ]],
]
