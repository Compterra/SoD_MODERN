# COST: low
SCRIPTS = [
("sod_threat_board_generate_offers",
 [
   (store_script_param_1, ":center_no"),

   (try_begin),
     (le, ":center_no", 0),
     (call_script, "script_get_closest_center", "p_main_party"),
    (assign, ":center_no", reg(0)),
   (try_end),

   (store_current_day, ":cur_day"),
   (store_sub, ":center_seed", ":center_no", centers_begin),
   (val_max, ":center_seed", 0),
   (store_add, ":seed", ":cur_day", ":center_seed"),

   (store_mod, ":offer_1", ":seed", 12),
   (val_add, ":offer_1", 1),
   (store_add, ":offer_2", ":offer_1", 4),
   (try_begin),
     (gt, ":offer_2", 12),
     (val_sub, ":offer_2", 12),
   (try_end),
   (store_add, ":offer_3", ":offer_1", 8),
   (try_begin),
     (gt, ":offer_3", 12),
     (val_sub, ":offer_3", 12),
   (try_end),

   (try_begin),
     (party_slot_eq, ":center_no", slot_party_type, spt_village),
     (assign, ":offer_3", sod_threat_archetype_cattle_raiders),
   (else_try),
     (party_slot_eq, ":center_no", slot_party_type, spt_castle),
     (assign, ":offer_2", sod_threat_archetype_army_deserters),
   (try_end),

   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_offer_1, ":offer_1"),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_offer_2, ":offer_2"),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_offer_3, ":offer_3"),
 ]),
]
