DIALOGS = [
[anyone, "town_dweller_quest_meet_spy_in_enemy_town_ask_item", [
     (str_store_item_name, s5, "$spy_item_worn"),

     (try_begin),
     (troop_has_item_equipped, "$g_talk_troop", "$spy_item_worn"),
     (str_store_string, s6, "@A {s5}? Well... Yes, I suppose it is. What a strange thing to ask."),
     (else_try),
     (str_store_string, s6, "@Eh? No, it most certainly is not a {s5}. I'd start questioning my eyesight if I were you."),
     (try_end),
  ],
   "{s6}", "town_dweller_talk", []],
]
