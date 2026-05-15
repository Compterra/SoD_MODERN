DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker_2_fight", [
    (eq, "$g_sod_nemesis_actor_type", sod_nemesis_actor_lord),
    (ge, "$g_sod_nemesis_state", sod_nemesis_state_hunting),
    (eq, "$g_sod_nemesis_last_troop", "$g_talk_troop"),
    (neq, "$g_talk_troop_faction", "fac_kingdom_6"),
    (troop_get_slot, reg21, "$g_talk_troop", slot_troop_sod_nemesis_defeats),
    (troop_get_slot, reg22, "$g_talk_troop", slot_troop_sod_nemesis_duel_pressure),
  ],
  "No more court words. I have worn the shape of your victories into my bones, {playername}. Today every man here will see whether your name still fits in my mouth.", "close_window", [
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
