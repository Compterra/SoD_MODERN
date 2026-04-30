DIALOGS = [
[anyone, "tavernkeeper_buy_peasants", [], "I know a few fellows who would follow you if you paid for their equipment.", "tavernkeeper_buy_peasants_2", [
    (set_mercenary_source_party, "$tavernkeeper_party"),
    (store_troop_gold, ":before", "trp_player"),
    (change_screen_buy_mercenaries),
    (store_troop_gold, ":after", "trp_player"),
    (store_sub, reg0, ":before", ":after"),
    # Safety: track only positive spending.
    (val_max, reg0, 0),
    (val_add, "$g_sod_weekly_troops_hired", reg0),
    (val_clamp, "$g_sod_weekly_troops_hired", 0, 2000001),
    #DEBUG
    #(display_message, "@Player spent {reg0} denars on hiring mercenaries.", debug_color),
  ]],
]
