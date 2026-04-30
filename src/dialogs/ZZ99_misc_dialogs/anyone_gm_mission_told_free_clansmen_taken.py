DIALOGS = [
[anyone, "gm_mission_told_free_clansmen_taken", [
  (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
 (str_store_party_name_link, s13, ":quest_target_center")
  ], "Good. I knew we could trust you at this. If you go now you should find them near {s13}.", "close_window",
   [
  (finish_mission),]],
]
