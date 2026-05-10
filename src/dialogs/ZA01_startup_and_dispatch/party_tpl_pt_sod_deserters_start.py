DIALOGS = [
[party_tpl|pt_sod_deserters, "start", [(eq, "$talk_context", tc_party_encounter),
                                     (party_get_slot, ":protected_until_hours", "$g_encountered_party", slot_party_ignore_player_until),
                                     (store_current_hours, ":cur_hours"),
                                     (store_sub, ":protection_remaining", ":protected_until_hours", ":cur_hours"),
                                     (gt, ":protection_remaining", 0)], "Back again? Your silver still buys you quiet, for now. Unless you brought more coin to sweeten our memory.", "deserter_paid_talk", []],
]
