DIALOGS = [
[anyone, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
                    (check_quest_active, "qst_escort_lady"),
                    (eq, "$talk_context", tc_entering_center_quest_talk),
                    (quest_slot_eq, "qst_escort_lady", slot_quest_object_troop, "$g_talk_troop")],
   "Thank you for escorting me here, {playername}. Please accept this gift as a token of my gratitude.\
 I hope we shall meet again sometime in the future.", "lady_escort_lady_succeeded",
   [
     (quest_get_slot, ":cur_center", "qst_escort_lady", slot_quest_target_center),
     (add_xp_as_reward, 300),
     (call_script, "script_troop_add_gold", "trp_player", 250),
     (call_script, "script_end_quest", "qst_escort_lady"),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     (troop_set_slot, "$g_talk_troop", slot_troop_cur_center, ":cur_center"),
     (remove_member_from_party, "$g_talk_troop"),
     ]],
]
