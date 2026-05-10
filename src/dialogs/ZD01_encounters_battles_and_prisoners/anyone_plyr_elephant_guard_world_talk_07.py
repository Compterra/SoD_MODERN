DIALOGS = [
[anyone|plyr, "elephant_guard_world_talk", [
   (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
   (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
   (store_add, ":slave_count", ":male_slaves", ":female_slaves"),
   (gt, ":slave_count", 0),
  ], "The captives with me will be freed here.", "elephant_guard_world_free_slaves", [
    (call_script, "script_sod_elephant_guard_free_player_slaves"),
  ]],
]
