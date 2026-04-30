DIALOGS = [
[anyone|plyr, "lady_restore_relation_4", [(store_troop_gold, ":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_3"),
                                           (assign, reg12, "$lady_restore_cost_3")],
   "In that case, I am ready to spend {reg12} denars.", "lady_restore_relation_5", [(assign, "$temp", 3), (assign, "$temp_2", "$lady_restore_cost_3")]],
]
