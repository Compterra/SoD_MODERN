DIALOGS = [
[trp_sod_marshal, "marshal_upgrade_garrison_list_options",
    [
      (troop_get_slot, ":center_no", "trp_sod_marshal", slot_troop_sod_court),
      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),
      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),

      # reg61 = cost to upgrade one unit to upgrade1
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", ":center_no"),
      (assign, reg61, reg0),

      # reg62 = cost to upgrade one unit to upgrade2
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", ":center_no"),
      (assign, reg62, reg0),

      # reg60 = player's available cash
      (store_troop_gold, reg60, "trp_player"),

      #(display_message, "@upgrade1 = {reg61} denars, uprgade2 = {reg62} denars", debug_color),

      # check if the player cannot afford even one upgrade
      (this_or_next|lt, reg60, reg61),(eq, "$can_upgrade1", 0),
      (this_or_next|lt, reg60, reg62),(eq, "$can_upgrade2", 0),
    ], "My apologies, my {Lord/Lady}, but you haven't the necessary funds to upgrade any of those troops.", "marshal_upgrade_garrison_sorry2", []],
]
