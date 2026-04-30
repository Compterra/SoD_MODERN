DIALOGS = [
[trp_sod_marshal, "marshal_upgrade_garrison_list_options",
    [
      (str_store_troop_name_by_count, s1, "$g_upgrade_troop", "$upgrade_count"),
      (assign, reg1, "$upgrade_count"),
    ],
    "You currently have {reg60} denars.^^What should your {reg1} {s1} train to become?", "marshal_upgrade_garrison_choose", []],
]
