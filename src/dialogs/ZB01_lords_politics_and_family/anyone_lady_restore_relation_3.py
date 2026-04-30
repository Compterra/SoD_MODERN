DIALOGS = [
[anyone, "lady_restore_relation_3", [(call_script, "script_store_troop_name", s10, "$troop_to_restore_relations_with"),
                                      (assign, "$lady_restore_cost_1", 1000),
                                      (assign, "$lady_restore_cost_2", 2000),
                                      (assign, "$lady_restore_cost_3", 3000),
                                      (assign, reg10, "$lady_restore_cost_1"),
                                      (assign, reg11, "$lady_restore_cost_2"),
                                      (assign, reg12, "$lady_restore_cost_3"),
                                      (troop_get_type, reg4, "$troop_to_restore_relations_with"),
                                      ],
   "You can improve your relation with {s10} by sending {reg4?her:him} a gift worth {reg10} denars.\
 But if you can afford spending {reg11} denars on the gift, it would make a good impression on {reg4?her:him}.\
 And if you can go up to {reg12} denars, that would really help smooth things out.", "lady_restore_relation_4", []],
]
