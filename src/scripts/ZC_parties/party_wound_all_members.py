SCRIPTS = [
("party_wound_all_members",
    [
      (store_script_param_1, ":party_no"),

      (call_script, "script_party_wound_all_members_aux", ":party_no"),
  ]),
]
