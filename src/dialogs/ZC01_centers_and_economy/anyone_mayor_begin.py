DIALOGS = [
[anyone, "mayor_begin", [
    (check_quest_active, "qst_persuade_lords_to_make_peace"),
    (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_giver_troop, "$g_talk_troop"),
    (check_quest_succeeded, "qst_persuade_lords_to_make_peace"),
    (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
    (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
    (val_mul, ":quest_target_troop", -1),
    (val_mul, ":quest_object_troop", -1),
    (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
    (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
    (call_script, "script_store_troop_name", s12, ":quest_target_troop"),
    (call_script, "script_store_troop_name", s13, ":quest_object_troop"),
    (str_store_faction_name, s14, ":quest_target_faction"),
    (str_store_faction_name, s15, ":quest_object_faction"),
    (str_store_party_name, s19, "$current_town"),
  ],
  "{s1}", "lord_persuade_lords_to_make_peace_completed",
  [
    (call_script, "script_sod_quest_dialogue_describe_reaction", "$g_talk_troop"),
    (call_script, "script_sod_quest_dialogue_describe_stage", "$g_talk_troop"),
    (str_store_string, s1, "@{playername}, it was an incredible feat to get {s14} and {s15} make peace, and you made it happen.\
Your involvement has not only saved our town from disaster, but it has also saved thousands of lives, and put an end to all the grief this bitter war has caused.\
As the townspeople of {s19}, know that we'll be good on our word, and we are ready to pay the {reg12} denars we promised."),
    (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
    (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
    (assign, "$g_force_peace_faction_1", ":quest_target_faction"),
    (assign, "$g_force_peace_faction_2", ":quest_object_faction"),
    (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (assign, reg12, ":quest_reward"),
    (add_xp_as_reward, 4000),
  ]],
]
