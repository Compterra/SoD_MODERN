DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
                    (store_partner_quest, ":elder_quest"),
                    (eq, ":elder_quest", "qst_deliver_cattle"),
                    (check_quest_succeeded, ":elder_quest"),
                    (quest_get_slot, reg5, "qst_deliver_cattle", slot_quest_target_amount)],
   "My good {sir/madam}. Our village is grateful for your help. Thanks to the {reg5} heads of cattle you have brought, we can now raise our own herd.", "village_elder_deliver_cattle_thank",
   [(add_xp_as_reward, 400),
    (quest_get_slot, ":num_cattle", "qst_deliver_cattle", slot_quest_target_amount),
    (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),
    (call_script, "script_change_center_prosperity", "$current_town", 4),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_end_quest", "qst_deliver_cattle"),
#Troop commentaries begin
    (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
#Troop commentaries end

    ]],
]
