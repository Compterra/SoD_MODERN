DIALOGS = [
[anyone, "gm_good_guys_accepted", [
  ],"Good, {playername}.", "gm_pretalk", [
  (str_store_party_name_link, s4, "$g_encountered_party"),
  (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
  (setup_quest_text, "$random_quest_no"),
    (str_store_string, s2, "@{s9} of {s4} has asked you to deal with the rebellious peasants at {s14}."),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
  ]],
]
