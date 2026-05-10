# COST: light
SCRIPTS = [
("sod_store_hostile_negotiation_options",
 [
   (store_script_param, ":party_no", 1),
   (assign, reg30, 0), # food passage available
   (assign, reg31, 0), # prisoner exchange available
   (assign, reg32, 0), # redirect bribe available
   (assign, reg33, 0), # faction credential available
   (assign, reg34, 0), # leader challenge available
   (try_begin),
     (gt, ":party_no", 0),
     (party_is_active, ":party_no"),
     (party_get_num_companions, ":enemy_size", ":party_no"),
     (try_begin),
       (le, ":enemy_size", 12),
       (call_script, "script_get_troop_item_amount", "trp_player", "itm_bread"),
       (assign, ":bread", reg0),
       (call_script, "script_get_troop_item_amount", "trp_player", "itm_dried_meat"),
       (assign, ":meat", reg0),
       (store_add, ":food", ":bread", ":meat"),
       (gt, ":food", 0),
       (assign, reg30, 1),
     (try_end),
     (try_begin),
       (party_get_num_prisoners, ":prisoners", "p_main_party"),
       (gt, ":prisoners", 0),
       (assign, reg31, 1),
     (try_end),
     (try_begin),
       (store_troop_gold, ":gold", "trp_player"),
       (ge, ":gold", 600),
       (assign, reg32, 1),
     (try_end),
     (try_begin),
       (gt, "$players_kingdom", 0),
       (assign, reg33, 1),
     (try_end),
     (try_begin),
       (ge, ":enemy_size", 6),
       (assign, reg34, 1),
     (try_end),
   (try_end),
 ]),
]
