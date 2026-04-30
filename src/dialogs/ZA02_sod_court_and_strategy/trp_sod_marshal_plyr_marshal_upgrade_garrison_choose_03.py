DIALOGS = [
[trp_sod_marshal|plyr, "marshal_upgrade_garrison_choose",
    [
      # disable this option if they don't meet the requirements!
      (eq, "$can_upgrade1", 1),
      #(eq, "$can_upgrade2", 1), #doesn't make sense to upgrade less than all, if this is the only upgrade path available

      # ensure we have enough to make this option make sense
      (gt, "$upgrade_count", 1),

      # get the troop type that this one upgrades to
      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),

      # get the center where this upgrade is being attempted at (so we can check its facilities)
      (troop_get_slot, ":center_no", "trp_sod_marshal", slot_troop_sod_court),

      # check if we can upgrade this unit type here
      (call_script, "script_sod_can_upgrade_troops_here", ":upgrade1", ":center_no"),
      (assign, "$can_upgrade1", reg0),

      # yes! load the needed strings
      (str_store_troop_name_by_count, s1, "$g_upgrade_troop", 1),
      (str_store_troop_name_by_count, s2, ":upgrade1", 1),

      # get the cost of upgrading this many units
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", ":center_no"),

      # only allow this if they can afford it
      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", reg0),
    ],
    "Promote one {s1} to {s2} ({reg0} denars)", "marshal_upgrade_garrison_list_options",
    [
      # get the location we're at to perform the upgrade
      (troop_get_slot, ":center_no", "trp_sod_marshal", slot_troop_sod_court),

      # get the new troop type
      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),

      # execute the upgrade of the specified amount of troops
      (call_script, "script_sod_upgrade_troop_count_to_at", "$g_upgrade_troop", 1, ":upgrade1", ":center_no", 1),

      # update how many remain
      (val_sub, "$upgrade_count", 1),
    ]
  ],
]
