DIALOGS = [
[anyone|plyr, "member_talk",
    [
      # display a slightly smarter message to the player if the NPC has leveled up since last time...
      (str_store_string, s1, "@Tell me about your skills."),
      (try_begin),
        # only track level ups for NPC companions
        (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
        (troop_get_slot, ":last", "$g_talk_troop", slot_troop_level_up),
        (store_character_level, ":current", "$g_talk_troop"),
        (try_begin),
          (lt, ":last", ":current"),
          (str_store_string, s1, "@Level Up! Review skills."),
        (try_end),
      (try_end),
    ],
    "{s1}", "member_anything_else",
    [
      # record that this is no longer a level up
      (store_character_level, ":current", "$g_talk_troop"),
      (troop_set_slot, "$g_talk_troop", slot_troop_level_up, ":current"),
      (change_screen_view_character),
    ]],
]
