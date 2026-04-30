DIALOGS = [
[trp_sod_marshal, "marshal_nobles",
    [
      (neq, "$g_sod_nobles_gather_at", 0),
      (str_store_party_name, s1, "$g_sod_nobles_gather_at"),
    ],
    "Your nobles are gathering at {s1}.  Where would you prefer that they gather?", "marshal_nobles_choose", []
  ],
]
