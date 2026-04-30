DIALOGS = [
[anyone, "gm_hire12", [
   ],"All right. They will do that.", "gm_pretalk",[
   (troop_set_slot, "$g_talk_troop", slot_troop_merc_bought, 1),
   (call_script, "script_merc_spawn_player_company", "$g_talk_troop_faction", "$temp1", "$temp_proportion", "$temp2", "$temp3", "$temp4", "$temp6"),
   ]],
]
