DIALOGS = [
[anyone, "convince_friendship_go_on", [], "All right then, {playername}, I will accept this for your sake. But remember, you owe me for this.", "convince_accept",
   [(store_sub, ":relation_change", 0, "$convince_relation_penalty"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", ":relation_change")]],
]
