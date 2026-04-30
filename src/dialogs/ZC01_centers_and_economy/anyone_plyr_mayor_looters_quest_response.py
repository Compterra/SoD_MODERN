DIALOGS = [
[anyone|plyr, "mayor_looters_quest_response",
   [
     (store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_bandits"),
     (party_template_get_slot, ":previous_looters_destroyed", "pt_bandits", slot_party_template_num_killed),
     (val_sub, ":num_looters_destroyed", ":previous_looters_destroyed"),
     (quest_get_slot, ":looters_paid_for", "qst_deal_with_looters", slot_quest_current_state),
     (lt, ":looters_paid_for", ":num_looters_destroyed"),
     ],
   "I've killed some looters.", "mayor_looters_quest_destroyed", []],
]
