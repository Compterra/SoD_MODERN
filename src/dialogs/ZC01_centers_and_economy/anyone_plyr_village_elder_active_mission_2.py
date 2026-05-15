DIALOGS = [
[anyone|plyr, "village_elder_active_mission_2", [(store_partner_quest, ":elder_quest"),
                                                 (eq, ":elder_quest", "qst_deliver_grain"),
                                                 (check_quest_active, "qst_deliver_grain"),
                                                 (quest_get_slot, ":quest_target_amount", "qst_deliver_grain", slot_quest_target_amount),
                                                 (call_script, "script_get_troop_item_amount", "trp_player", "itm_grain"),
                                                 (assign, ":cur_amount", reg0),
                                                 (ge, ":cur_amount", ":quest_target_amount"),
                                                 (assign, reg5, ":quest_target_amount"),
                                                 ],
   "Indeed. I brought you {reg5} packs of wheat.", "village_elder_deliver_grain_thank",
   []],
]
