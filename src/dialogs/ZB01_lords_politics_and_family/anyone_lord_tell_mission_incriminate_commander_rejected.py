DIALOGS = [
[anyone, "lord_tell_mission_incriminate_commander_rejected", [], "Dishonourable? Bah!\
 I was hoping I could count on you, {playername}, but you've shown me what a fool I was.\
 I shall have to find someone whose loyalty I can trust.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
    (call_script, "script_change_player_honor", 2)]],
]
