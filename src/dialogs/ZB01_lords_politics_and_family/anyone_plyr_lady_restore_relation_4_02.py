DIALOGS = [
[anyone|plyr, "lady_restore_relation_4", [(store_troop_gold, ":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_2"),
                                           (assign, reg11, "$lady_restore_cost_2")],
   "Maybe I can afford {reg11} denars.", "lady_restore_relation_5", [(assign, "$temp", 2), (assign, "$temp_2", "$lady_restore_cost_2")]],
]
