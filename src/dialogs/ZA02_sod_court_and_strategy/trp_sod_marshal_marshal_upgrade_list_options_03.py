DIALOGS = [
[trp_sod_marshal, "marshal_upgrade_list_options",
    [
      (str_store_troop_name_by_count, s68, "$g_upgrade_troop", "$upgrade_count"),
      (assign, reg1, "$upgrade_count"),
    ],
    "You currently have {reg60} denars.^^Promote your {reg1} {s68} into which troop?", "marshal_upgrade_choose", []],
]
