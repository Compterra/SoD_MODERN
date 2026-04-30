DIALOGS = [
[anyone , "village_elder_buy_cattle", [(party_get_slot, reg5, "$g_encountered_party", slot_village_number_of_cattle),
                                        (gt, reg5, 0),
                                        (store_item_value, ":cattle_cost", "itm_cattle_meat"),
                                        (call_script, "script_game_get_item_buy_price_factor", "itm_cattle_meat"),
                                        (val_mul, ":cattle_cost", reg0),
                                        #Multiplied by 2 and divided by 100
                                        (val_div, ":cattle_cost", 50),
                                        (assign, "$temp", ":cattle_cost"),
                                        (assign, reg6, ":cattle_cost"),
                                        ],
   "We have {reg5} heads of cattle, each for {reg6} denars. How many do you want to buy?", "village_elder_buy_cattle_2", []],
]
