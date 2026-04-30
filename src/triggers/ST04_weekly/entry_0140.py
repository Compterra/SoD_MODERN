SIMPLE_TRIGGERS = [
(24*7, [ (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
           (call_script, "script_calculate_badboy_decay"),
           (val_mul, reg0, -1),
           (call_script, "script_change_badboy_rating", reg0),
           ]),
]
