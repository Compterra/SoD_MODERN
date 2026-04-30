DIALOGS = [
[anyone|plyr, "move_cattle_herd_quest_brief", [],  "Aye, I can take the herd to {s13}.",
   "move_cattle_herd_quest_taken",
   [
     (call_script, "script_create_cattle_herd", "$g_encountered_party", 0),
     (quest_set_slot, "qst_move_cattle_herd", slot_quest_target_party, reg0),
     (str_store_party_name_link, s10, "$g_encountered_party"),
     (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
     (str_store_party_name_link, s13, ":target_center"),
     (quest_get_slot, reg8, "qst_move_cattle_herd", slot_quest_gold_reward),
     (setup_quest_text, "qst_move_cattle_herd"),
     (str_store_string, s2, "@Guildmaster of {s10} asked you to move a cattle herd to {s13}. You will earn {reg8} denars in return."),
     (call_script, "script_start_quest", "qst_move_cattle_herd", "$g_talk_troop"),
     ]],
]
