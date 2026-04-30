DIALOGS = [
[anyone, "mayor_looters_quest_goods_2", [
      (neg|quest_slot_ge, "qst_deal_with_looters", slot_quest_target_item, 1),
      (quest_get_slot, ":xp_reward", "qst_deal_with_looters", slot_quest_xp_reward),
      (quest_get_slot, ":gold_reward", "qst_deal_with_looters", slot_quest_gold_reward),
      (add_xp_as_reward, ":xp_reward"),
      (call_script, "script_troop_add_gold", "trp_player", ":gold_reward"),
      (call_script, "script_change_player_relation_with_center", "$current_town", 3),
      (call_script, "script_end_quest", "qst_deal_with_looters"),
      (try_for_parties, ":cur_party_no"),
        (party_get_template_id, ":cur_party_template", ":cur_party_no"),
        (eq, ":cur_party_template", "pt_bandits"),
        (party_set_flags, ":cur_party_no", pf_quest_party, 0),
      (try_end),
  ],
   "Well done, {playername}, that's the last of the goods I need. Here is the money for your {s6}, and a small bonus for helping me out.\
 I'm afraid I won't be paying for any more goods, nor bounties on looters, but you're welcome to keep hunting the bastards if any remain.\
 Thank you for your help, I won't forget it.",
   "close_window", [
      ]],
]
