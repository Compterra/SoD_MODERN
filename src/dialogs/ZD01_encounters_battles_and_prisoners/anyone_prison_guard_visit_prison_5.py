DIALOGS = [
[anyone, "prison_guard_visit_prison_5", [], "Ah! I was looking for this all day. How good of you to bring it back {sir/madam}.\
 Well, now that I know what an honest {man/lady} you are, there can be no harm in letting you inside. Go in.", "close_window", [(troop_remove_gold, "trp_player", 100), (play_sound, "snd_money_paid"), (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
]
