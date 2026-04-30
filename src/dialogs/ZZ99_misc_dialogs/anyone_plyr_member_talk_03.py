DIALOGS = [
[anyone|plyr, "member_talk", [
  (neq, "$g_talk_troop", "trp_sod_strategy_advisor"),
  (eq, "$g_camp_talk", 0), #Autoloot: don't allow separation during loot-management conversations.
  ], "We need to separate for a while.", "member_separate", [
            (call_script, "script_npc_morale", "$g_talk_troop"),
            (assign, "$npc_quit_morale", reg0),
      ]],
]
