DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_deliver_cattle_to_army"),
                         (check_quest_succeeded, "qst_deliver_cattle_to_army"),
                         (quest_get_slot, reg13, "qst_deliver_cattle_to_army", slot_quest_target_amount),
                         ],
   "Ah, {playername}. My quartermaster has informed me of your delivery, {reg13} heads of cattle, as I requested. I'm impressed.", "lord_deliver_cattle_to_army_thank",
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     (quest_get_slot, ":quest_target_amount", "qst_deliver_cattle_to_army", slot_quest_target_amount),
     #TODO: Change reward
     (store_mul, ":reward", ":quest_target_amount", 100),
     (call_script, "script_troop_add_gold", "trp_player", ":reward"),
     (val_div, ":reward", 5),
     (add_xp_as_reward, ":reward"),
     (call_script, "script_end_quest", "qst_deliver_cattle_to_army"),
     #Reactivating follow army quest
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@Your mission is complete, {s9} wants you to resume following his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
     (assign, "$g_player_follow_army_warnings", 0),
     ]],
]
