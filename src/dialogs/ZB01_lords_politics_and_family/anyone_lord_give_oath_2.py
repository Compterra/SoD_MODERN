DIALOGS = [
[anyone, "lord_give_oath_2", [],  "Good. Then repeat the words of the oath with me: I swear homage to you as lawful ruler of the {s41}.", "lord_give_oath_3", [
            (str_store_faction_name, 41, "$g_talk_troop_faction"),
            (try_begin),
                (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
                (troop_get_slot, ":rebel_faction", "$g_talk_troop", slot_troop_original_faction),
                (str_store_faction_name, 41, ":rebel_faction"),
            (try_end),
      ]],
]
