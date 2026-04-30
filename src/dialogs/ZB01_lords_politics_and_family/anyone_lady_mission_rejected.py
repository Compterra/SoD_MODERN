DIALOGS = [
[anyone, "lady_mission_rejected", [], "You'll not help a woman in need? You should be ashamed, {playername}...\
 Please leave me, I have some important embroidery to catch up.", "close_window",
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],
]
