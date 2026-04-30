DIALOGS = [
[anyone, "mayor_looters_quest_destroyed_2", [
      (quest_get_slot, ":total_looters", "qst_deal_with_looters", slot_quest_target_amount),
      (quest_slot_ge, "qst_deal_with_looters", slot_quest_current_state, ":total_looters"), # looters paid for >= total looters
      (quest_get_slot, ":xp_reward", "qst_deal_with_looters", slot_quest_xp_reward),
      (quest_get_slot, ":gold_reward", "qst_deal_with_looters", slot_quest_gold_reward),
      (add_xp_as_reward, ":xp_reward"),
      (call_script, "script_troop_add_gold", "trp_player", ":gold_reward"),
      (call_script, "script_change_troop_renown", "trp_player", 1),
      (call_script, "script_change_player_relation_with_center", "$current_town", 5),
      (call_script, "script_end_quest", "qst_deal_with_looters"),
      (try_for_parties, ":cur_party_no"),
        (party_get_template_id, ":cur_party_template", ":cur_party_no"),
        (eq, ":cur_party_template", "pt_bandits"),
        (party_set_flags, ":cur_party_no", pf_quest_party, 0),
      (try_end),
  ],
   "And that's not the only good news! Thanks to you, the looters have ceased to be a threat. We've not had a single attack reported for some time now.\
   If there are any of them left, they've either run off or gone deep into hiding. That's good for business,\
   and what's good for business is good for the town!\
   I think that concludes our arrangement, {playername}. Please accept this silver as a token of my gratitude. Thank you, and farewell.",
   "close_window", [
      ]],
]
