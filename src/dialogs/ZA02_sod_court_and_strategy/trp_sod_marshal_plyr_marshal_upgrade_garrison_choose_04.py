DIALOGS = [
[trp_sod_marshal|plyr, "marshal_upgrade_garrison_choose",
    [
      # disable this option if they don't meet the requirements!
      (eq, "$can_upgrade2", 1),

      # ensure we have enough to make this option make sense
      (ge, "$upgrade_count", 1),

      # get the troop type that this one upgrades to
      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),

      # get the center where this upgrade is being attempted at (so we can check its facilities)
      (troop_get_slot, ":center_no", "trp_sod_marshal", slot_troop_sod_court),

      # check if we can upgrade this unit type here
      (call_script, "script_sod_can_upgrade_troops_here", ":upgrade2", ":center_no"),
      (assign, "$can_upgrade2", reg0),

      # yes! load the needed strings
      (str_store_troop_name_by_count, s1, "$g_upgrade_troop", "$upgrade_count"),
      (str_store_troop_name_by_count, s2, ":upgrade2", "$upgrade_count"),

      # get the cost of upgrading this many units
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", ":center_no"),
      (val_mul, reg0, "$upgrade_count"),

      # only allow this if they can afford it
      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", reg0),
    ],
    "Promote all {s1} to {s2} ({reg0} denars)", "marshal_upgrade_garrison_check_again",
    [
      # get the location we're at to perform the upgrade
      (troop_get_slot, ":center_no", "trp_sod_marshal", slot_troop_sod_court),

      # get the new troop type
      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),

      # execute the upgrade of the specified amount of troops
      (call_script, "script_sod_upgrade_troop_count_to_at", "$g_upgrade_troop", "$upgrade_count", ":upgrade2", ":center_no", 1),

      # update how many remain
      (val_sub, "$upgrade_count", "$upgrade_count"),
    ]
  ],
]
