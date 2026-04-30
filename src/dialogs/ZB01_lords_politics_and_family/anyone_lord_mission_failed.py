DIALOGS = [
[anyone, "lord_mission_failed", [], "{s43}", "lord_pretalk",
   [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_mission_failed_default"),
    (store_partner_quest, ":lords_quest"),
    (call_script, "script_abort_quest", ":lords_quest", 1)]],
]
