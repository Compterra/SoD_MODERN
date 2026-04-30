DIALOGS = [
[anyone, "start",
   [(eq, "$caravan_escort_state", 1),
    (eq, "$g_encountered_party", "$caravan_escort_party_id"),
    (le, "$talk_context", tc_party_encounter),
    (store_distance_to_party_from_party, reg(0), "$caravan_escort_destination_town", "$caravan_escort_party_id"),
    (lt, reg(0), 5),
    (str_store_party_name, s3, "$caravan_escort_destination_town"),
    (assign, reg(3), "$caravan_escort_agreed_reward"),
    ],
   "There! I can see the walls of {s3} in the distance. We've made it safely.\
 Here, take this purse of {reg3} denars, as I promised. I hope we can travel together again someday.", "close_window",
   [
    (assign, "$caravan_escort_state", 0),
    (call_script, "script_troop_add_gold", "trp_player", "$caravan_escort_agreed_reward"),
    (assign, reg(4), "$caravan_escort_agreed_reward"),
    (val_mul, reg(4), 1),
    (add_xp_as_reward, reg(4)),
    (assign, "$g_leave_encounter", 1),
    ]],
]
