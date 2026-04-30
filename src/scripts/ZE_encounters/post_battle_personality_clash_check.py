SCRIPTS = [
("post_battle_personality_clash_check",
        [



          #            (display_message, "@Post-victory personality clash check", debug_color),
          (try_for_range, ":npc", companions_begin, companions_end),
            (eq, "$disable_npc_complaints", 0),

            (main_party_has_troop, ":npc"),
            (neg|troop_is_wounded, ":npc"),

            (troop_get_slot, ":other_npc", ":npc", slot_troop_personalityclash2_object),
            (main_party_has_troop, ":other_npc"),
            (neg|troop_is_wounded, ":other_npc"),

            #                (store_random_in_range, ":random", 0, 3),
            (try_begin),
              (troop_slot_eq, ":npc", slot_troop_personalityclash2_state, 0),
              (try_begin),
                #                        (eq, ":random", 0),
                (assign, "$npc_with_personality_clash_2", ":npc"),
              (try_end),
            (try_end),

          (try_end),

          (try_for_range, ":npc", companions_begin, companions_end),
            (troop_slot_eq, ":npc", slot_troop_personalitymatch_state, 0),
            (eq, "$disable_npc_complaints", 0),

            (main_party_has_troop, ":npc"),
            (neg|troop_is_wounded, ":npc"),

            (troop_get_slot, ":other_npc", ":npc", slot_troop_personalitymatch_object),
            (main_party_has_troop, ":other_npc"),
            (neg|troop_is_wounded, ":other_npc"),
            (assign, "$npc_with_personality_match", ":npc"),
          (try_end),


          (try_begin),
            (gt, "$npc_with_personality_clash_2", 0),
            (assign, "$npc_map_talk_context", slot_troop_personalityclash2_state),
            (start_map_conversation, "$npc_with_personality_clash_2"),
          (else_try),
            (gt, "$npc_with_personality_match", 0),
            (assign, "$npc_map_talk_context", slot_troop_personalitymatch_state),
            (start_map_conversation, "$npc_with_personality_match"),
          (try_end),


      ]),
]
