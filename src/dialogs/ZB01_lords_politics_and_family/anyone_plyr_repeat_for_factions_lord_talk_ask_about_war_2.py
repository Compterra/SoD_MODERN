DIALOGS = [
[anyone|plyr|repeat_for_factions, "lord_talk_ask_about_war_2",
    [(store_repeat_object, ":faction_no"),
      (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
         (store_relation, ":cur_relation", ":faction_no", "$g_talk_troop_faction"),
         (lt, ":cur_relation", 0),
         (str_store_faction_name, s1, ":faction_no")],
   "Tell me more about the war with {s1}.", "lord_talk_ask_about_war_details", [(store_repeat_object, "$faction_requested_to_learn_more_details_about_the_war_against")]],
]
