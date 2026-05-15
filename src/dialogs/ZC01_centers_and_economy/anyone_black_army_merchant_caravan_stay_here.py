DIALOGS = [
[anyone, "black_army_merchant_caravan_stay_here", [], "We will hold here, wagons tight and guards awake.", "close_window", [(assign, "$black_army_escort_merchant_caravan_mode", 1),
                 (quest_get_slot, ":quest_target_party", "qst_black_army_escort_merchant_caravan", slot_quest_target_party),
                 (try_begin),
                   (gt, ":quest_target_party", 0),
                   (party_is_active, ":quest_target_party"),
                   (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
                   (party_set_ai_object, ":quest_target_party", "p_main_party"),
                   (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                   (quest_set_slot, "qst_black_army_escort_merchant_caravan", slot_quest_current_state, 1),
                 (try_end),
				 (assign, "$g_leave_encounter", 1)]],
]
