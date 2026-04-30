DIALOGS = [
[anyone|plyr, "freed_hero_answer", [],
   "You're not going anywhere. You'll be my prisoner now!", "freed_hero_answer_1",
   [
     (store_conversation_troop, ":cur_troop_id"),
     (party_add_prisoners, "p_main_party", ":cur_troop_id", 1), #take prisoner
    ]],
]
