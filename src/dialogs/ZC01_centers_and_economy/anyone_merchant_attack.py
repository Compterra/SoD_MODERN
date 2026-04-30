DIALOGS = [
[anyone, "merchant_attack", [], "Damn you, you won't get anything from us without a fight!", "close_window",
   [(store_relation, ":rel", "$g_encountered_party_faction", "fac_player_supporters_faction"),
    (try_begin),
      (gt, ":rel", 0),
      (val_sub, ":rel", 10),
    (try_end),
    (val_sub, ":rel", 5),
    (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
### Troop commentaries changes begin
    (call_script, "script_add_log_entry", logent_caravan_accosted, "trp_player",  -1, -1, "$g_encountered_party_faction"),
### Troop commentaries changes end
    ]],
]
