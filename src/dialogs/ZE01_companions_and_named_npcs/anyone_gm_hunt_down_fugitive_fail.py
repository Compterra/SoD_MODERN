DIALOGS = [
[anyone, "gm_hunt_down_fugitive_fail", [],
   "It is a sad day when that a thief manages to avoid the hand of justice yet again.\
 I thought you would be able to do this, {playername}. Clearly I was wrong.", "gm_pretalk",
   [
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", -1),
    (call_script, "script_fail_quest", "qst_elephant_guard_hunt_down_fugitive"),
    (call_script, "script_end_quest", "qst_elephant_guard_hunt_down_fugitive"),
    ]],
]
