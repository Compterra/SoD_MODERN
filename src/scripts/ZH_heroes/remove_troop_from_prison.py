SCRIPTS = [
("remove_troop_from_prison",
                    [
                      (store_script_param, ":troop_no", 1),
                      (call_script, "script_sod_quest_battle_note_prisoner_freed", ":troop_no"),
                      (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
                      (try_begin),
                        (check_quest_active, "qst_rescue_lord_by_replace"),
                        (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, ":troop_no"),
                        (call_script, "script_cancel_quest", "qst_rescue_lord_by_replace"),
                      (try_end),
                      (try_begin),
                        (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
                        (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, ":troop_no"),
                        (call_script, "script_cancel_quest", "qst_deliver_message_to_prisoner_lord"),
                      (try_end),
                  ]),
]
