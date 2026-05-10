DIALOGS = [
[anyone|plyr, "regular_member_talk",
    [
      (is_between, "$g_talk_troop", companions_begin, companions_end),
      (main_party_has_troop, "$g_talk_troop"),
    ],
    "Let's speak about the troops under your command.", "regular_member_retinue_command",
    [
      (assign, "$g_sod_retinue_focus_companion", "$g_talk_troop"),
      (assign, "$g_sod_retinue_selected_troop", 0),
      (assign, "$g_sod_retinue_selected_count", 0),
    ]],

[anyone, "regular_member_retinue_command",
    [
      (call_script, "script_sod_companion_retinue_describe_dialogue_to_s28", "$g_talk_troop"),
    ],
    "{s28}", "regular_member_retinue_command_choice",
    []],

[anyone|plyr, "regular_member_retinue_command_choice", [],
    "Show me your command rolls.", "close_window",
    [
      (jump_to_menu, "mnu_companion_retinue_manage"),
    ]],

[anyone|plyr, "regular_member_retinue_command_choice", [],
    "That is enough for now.", "regular_member_talk",
    [
    ]],
]
