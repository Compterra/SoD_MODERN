DIALOGS = [
[trp_sod_chancellor|plyr, "chancellor_lord_action",  [(call_script, "script_sod_chancellor_lord_recruitment_refresh"), (ge, "$lords", 1), (ge, "$territory", 1)], "Send the summons. Bring a new lord into our service.", "chancellor_lord_recruited",
    [
      (call_script, "script_sod_chancellor_recruit_homeland_lord"),
    ]
  ],
]
