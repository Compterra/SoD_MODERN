DIALOGS = [
[anyone, "merchant_demand_toll", [(gt, "$g_strength_ratio", 70),
                                        (store_div, reg6, "$g_ally_strength", 2),
                                        (val_add, reg6, 40),
                                        (assign, "$temp", reg6),
                                        ], "Please, I don't want any trouble. I can give you {reg6} denars, just let us go.", "merchant_demand_toll_2", []],
]
