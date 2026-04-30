# COST: low
SCRIPTS = [
("sod_threat_board_init_registry",
 [
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_type, sod_threat_type_none),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_tier, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_archetype, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_target_party, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_sponsor_center, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_sponsor_faction, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_reward_gold, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_reward_relation, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_deadline_day, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_ready_to_claim, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_reward_xp, 0),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_offer_1, sod_threat_archetype_river_pirates),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_offer_2, sod_threat_archetype_army_deserters),
   (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_offer_3, sod_threat_archetype_cattle_raiders),
   (assign, "$g_sod_threat_board_context_center", 0),
   (assign, "$g_sod_threat_board_return_menu", 0),
 ]),
]
