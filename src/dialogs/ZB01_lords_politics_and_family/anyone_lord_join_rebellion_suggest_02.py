DIALOGS = [
[anyone, "lord_join_rebellion_suggest", [
                (lt, "$g_talk_troop_relation", -10),
      ], "I have no time to bandy words with the likes of you.", "lord_start",
   [
        (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
    ]],
]
