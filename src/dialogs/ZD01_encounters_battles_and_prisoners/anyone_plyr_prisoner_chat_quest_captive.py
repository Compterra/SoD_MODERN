DIALOGS = [
[anyone|plyr, "prisoner_chat", [
  (eq, "$g_talk_troop", "trp_khergit_chieftain"),
  (check_quest_active, "qst_elephant_guard_capture_the_bastard"),
  ], "You will be delivered to the Elephant Guard. There will be no bargain.", "close_window", []],
]
