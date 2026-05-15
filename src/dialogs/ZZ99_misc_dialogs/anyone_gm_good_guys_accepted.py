DIALOGS = [
[anyone, "gm_good_guys_accepted", [
  ],"Good. Make it clean enough that the road understands.", "gm_pretalk", [
  (str_store_party_name_link, s4, "$g_encountered_party"),
  (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
  (quest_get_slot, ":village", "$random_quest_no", slot_quest_target_center),
  (str_store_party_name_link, s14, ":village"),
  (setup_quest_text, "$random_quest_no"),
    (str_store_string, s2, "@{s9} of {s4} has asked you to deal with the rebellious peasants at {s14}."),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
  ]],
]
