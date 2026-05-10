DIALOGS = [
[anyone|plyr, "jotnar_world_hearth_talk", [
   (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
   (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
   (store_add, ":slave_count", ":male_slaves", ":female_slaves"),
   (gt, ":slave_count", 0),
  ], "The captives with me can take shelter by your fires.", "jotnar_world_hearth_free_captives", [
    (call_script, "script_sod_jotnar_free_player_captives"),
  ]],
]
