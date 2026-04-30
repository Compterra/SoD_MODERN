DIALOGS = [
[anyone|plyr, "lady_restore_relation_4", [(store_troop_gold, ":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_1"),
                                           (assign, reg10, "$lady_restore_cost_1")],
   "I think a gift of {reg10} denars will do.", "lady_restore_relation_5", [(assign, "$temp", 1), (assign, "$temp_2", "$lady_restore_cost_1")]],
]
