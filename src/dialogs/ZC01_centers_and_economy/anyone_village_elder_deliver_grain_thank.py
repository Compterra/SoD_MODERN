DIALOGS = [
[anyone, "village_elder_deliver_grain_thank", [(str_store_party_name, s13, "$current_town")],
   "My good {lord/lady}. You have saved us from hunger and desperation. We cannot thank you enough, but you'll always be in our prayers.\
 The village of {s13} will not forget what you have done for us.", "village_elder_deliver_grain_thank_2",
   [(quest_get_slot, ":quest_target_amount", "qst_deliver_grain", slot_quest_target_amount),
    (call_script, "script_get_troop_item_amount", "trp_player", "itm_grain"),
    (try_begin),
      (check_quest_active, "qst_deliver_grain"),
      (ge, reg0, ":quest_target_amount"),
      (troop_remove_items, "trp_player", "itm_grain", ":quest_target_amount"),
      (add_xp_as_reward, 400),
      (call_script, "script_change_center_prosperity", "$current_town", 4),
      (call_script, "script_change_player_relation_with_center", "$current_town", 5),
      (call_script, "script_end_quest", "qst_deliver_grain"),
#Troop commentaries begin
      (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
#Troop commentaries end
    (else_try),
      (display_message, "@The village grain delivery could not be completed because the required grain was no longer in your inventory.", 0xFF6666),
    (try_end),
   ]],
]
