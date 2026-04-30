DIALOGS = [
[anyone, "merchant_demand_toll_accept", [(assign, reg6, "$temp")], "Very well then. Here's {reg6} denars. ", "close_window",
   [(assign, "$g_leave_encounter", 1),
    (call_script, "script_troop_add_gold", "trp_player", "$temp"),
    (store_add, ":toll_finish_time", "$g_current_hours", merchant_toll_duration),
    (party_set_slot, "$g_encountered_party", slot_party_last_toll_paid_hours, ":toll_finish_time"),
    (try_begin),
      (ge, "$g_encountered_party_relation", -5),
      (store_relation, ":rel", "$g_encountered_party_faction", "fac_player_supporters_faction"),
      (try_begin),
        (gt, ":rel", 0),
        (val_sub, ":rel", 1),
      (try_end),
      (val_sub, ":rel", 1),
      (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
    (try_end),
### Troop commentaries changes begin
    (call_script, "script_add_log_entry", logent_caravan_accosted, "trp_player",  -1, -1, "$g_encountered_party_faction"),
### Troop commentaries changes end
    (assign, reg6, "$temp"),
    ]],
]
