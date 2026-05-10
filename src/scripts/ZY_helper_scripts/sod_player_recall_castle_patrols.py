# COST: party scan
SCRIPTS = [
("sod_player_recall_castle_patrols",
 [
   (store_script_param, ":castle_no", 1),
   (assign, reg0, 0),
   (call_script, "script_sod_player_can_order_castle_patrols", ":castle_no"),
   (try_begin),
     (eq, reg0, 1),
     (assign, reg0, 0),
     (try_for_parties, ":cur_party"),
       (party_slot_eq, ":cur_party", slot_party_sod_support_type, sod_support_type_castle_patrol),
       (party_slot_eq, ":cur_party", slot_party_sod_patrol_origin_castle, ":castle_no"),
       (party_set_slot, ":cur_party", slot_party_sod_patrol_status, sod_castle_patrol_status_returning),
       (party_set_ai_behavior, ":cur_party", ai_bhvr_travel_to_party),
       (party_set_ai_object, ":cur_party", ":castle_no"),
       (val_add, reg0, 1),
     (try_end),
   (else_try),
     (assign, reg0, 0),
   (try_end),
 ]),
]
