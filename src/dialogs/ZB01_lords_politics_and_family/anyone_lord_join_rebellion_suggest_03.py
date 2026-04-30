DIALOGS = [
[anyone, "lord_join_rebellion_suggest",
   [
     (assign, "$g_rebellion_suggest_friends_stronger", 0),
     (call_script, "script_init_ai_calculation"), #recalculating friend and enemy strengths
     (troop_get_slot, ":leaded_party", "$g_talk_troop", slot_troop_leaded_party),
     (gt, ":leaded_party", 0),
     (party_get_slot, ":friend_strength", ":leaded_party", slot_party_nearby_friend_strength),
     (party_get_slot, ":enemy_strength", ":leaded_party", slot_party_nearby_enemy_strength),
     (party_get_slot, ":cached_strength", ":leaded_party", slot_party_cached_strength),
     (val_sub, ":friend_strength", ":cached_strength"),
     (val_add, ":enemy_strength", ":cached_strength"),
     (gt, ":friend_strength", ":enemy_strength"),
     (assign, "$g_rebellion_suggest_friends_stronger", 1),
     (encountered_party_is_attacker),
     ], "{s43}", "party_encounter_lord_hostile_attacker_2", #This is hardly the time or the place for such a discussion.
   [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_talk_later_default"),
    ]],
]
