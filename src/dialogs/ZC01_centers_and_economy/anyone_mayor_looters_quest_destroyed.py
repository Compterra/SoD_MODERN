DIALOGS = [
[anyone, "mayor_looters_quest_destroyed", [],
   "Aye, my scouts saw the whole thing. That should make anyone else think twice before turning outlaw!\
 The bounty is 40 denars for every band, so that makes {reg1} in total. Here is your money, as promised.",
   "mayor_looters_quest_destroyed_2", [
      (store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_bandits"),
      (party_template_get_slot, ":previous_looters_destroyed", "pt_bandits", slot_party_template_num_killed),
      (val_sub, ":num_looters_destroyed", ":previous_looters_destroyed"),
      (quest_get_slot, ":looters_paid_for", "qst_deal_with_looters", slot_quest_current_state),
      (store_sub, ":looter_bounty", ":num_looters_destroyed", ":looters_paid_for"),
      (val_mul, ":looter_bounty", 40),
      (assign, reg1, ":looter_bounty"),
      (call_script, "script_troop_add_gold", "trp_player", ":looter_bounty"),
      (assign, ":looters_paid_for", ":num_looters_destroyed"),
      (quest_set_slot, "qst_deal_with_looters", slot_quest_current_state, ":looters_paid_for"),
      ]],
]
