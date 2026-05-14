DIALOGS = [
[anyone, "gm_mission_told_free_clansmen_taken", [
  (try_begin),
    (eq, "$g_sod_last_rescue_spawn_ok", 1),
    (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
    (str_store_party_name_link, s13, ":quest_target_center"),
    (str_store_string, s2, "@Good. I knew we could trust you at this. If you go now you should find them near {s13}."),
  (else_try),
    (str_store_string, s2, "@The slaver party has vanished from the route. I will not send you chasing smoke. Come back later and we will try again."),
  (try_end),
  ], "{s2}", "close_window",
   [
  (finish_mission),]],
]
