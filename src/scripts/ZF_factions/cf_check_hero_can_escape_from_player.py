SCRIPTS = [
("cf_check_hero_can_escape_from_player",
        [
          (store_script_param_1, ":troop_no"),
          (assign, ":quest_target", 0),
          (try_begin),
            (check_quest_active, "qst_persuade_lords_to_make_peace"),
            (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
            (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
            (assign, ":quest_target", 1),
          (try_end),
          (eq, ":quest_target", 0),
          (store_random_in_range, ":rand", 0, 100),
          (lt, ":rand", hero_escape_after_defeat_chance),
      ]),
]
