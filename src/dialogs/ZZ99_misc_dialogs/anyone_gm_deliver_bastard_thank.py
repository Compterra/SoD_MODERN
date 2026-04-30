DIALOGS = [
[anyone, "gm_deliver_bastard_thank", [(str_store_party_name, s13, "$current_town")],
   "My good {lord/lady}. We cannot thank you enough.\
   Now he'll answer for his crimes.", "gm_pretalk",
   [
	(party_remove_prisoners,"p_main_party","trp_khergit_chieftain", 1),
    (add_xp_as_reward, 1000),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 8),
    (call_script, "script_succeed_quest", "qst_elephant_guard_capture_the_bastard"),
    (call_script, "script_end_quest", "qst_elephant_guard_capture_the_bastard"),
   ]],
]
