SCRIPTS = [
("jq_extra_stats",
                      [
                        (store_script_param, ":jq_troop_no", 1),
                        (call_script, "script_store_troop_name_link", s9, ":jq_troop_no"),
                        (store_troop_health , reg2, ":jq_troop_no"),
                        (store_character_level, reg3, ":jq_troop_no"),
                        (call_script, "script_npc_morale", ":jq_troop_no"),
                        (assign, ":troop_morale", reg0),
                        (assign, reg1, ":troop_morale"),
                        (str_store_string, s1, "@{s9}^^^Level: {reg3}^Health: {reg2}%^Morale: {reg1}"),
                        (overlay_set_text, "$g_jq_equipment_status", s1),

                        (try_for_range, ":jq_cur_slot", 0, 8), #equipment slots
                          (troop_get_inventory_slot, reg1, ":jq_troop_no", ":jq_cur_slot"),
                          (try_begin),
                            (lt, reg1, 1), # if item slot is empty...
                            (str_store_string, s8, "@________________n/a________________"),
                          (else_try),
                            (str_store_item_name, s8, reg1),
                          (try_end),
                          (try_begin),
                            (eq, ":jq_cur_slot", 0),
                            (overlay_set_text, "$g_jq_equipment_item0", s8),
                          (else_try),
                            (eq, ":jq_cur_slot", 1),
                            (overlay_set_text, "$g_jq_equipment_item1", s8),
                          (else_try),
                            (eq, ":jq_cur_slot", 2),
                            (overlay_set_text, "$g_jq_equipment_item2", s8),
                          (else_try),
                            (eq, ":jq_cur_slot", 3),
                            (overlay_set_text, "$g_jq_equipment_item3", s8),
                          (else_try),
                            (eq, ":jq_cur_slot", 4),
                            (overlay_set_text, "$g_jq_equipment_item4", s8), #head
                          (else_try),
                            (eq, ":jq_cur_slot", 5),
                            (overlay_set_text, "$g_jq_equipment_item5", s8), #body
                          (else_try),
                            (eq, ":jq_cur_slot", 6),
                            (overlay_set_text, "$g_jq_equipment_item6", s8), #feet
                          (else_try),
                            (eq, ":jq_cur_slot", 7),
                            (overlay_set_text, "$g_jq_equipment_item7", s8), #hands
                          (try_end),
                        (try_end), # try-for-range-loop-end
                        (set_result_string, s8),
                    ]),
]
