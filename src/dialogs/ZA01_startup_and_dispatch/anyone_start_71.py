DIALOGS = [
[anyone, "start", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (le, "$talk_context", tc_siege_commander),
    (check_quest_active, "qst_rescue_lord_by_replace"),
    (check_quest_succeeded, "qst_rescue_lord_by_replace"),
    (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_giver_troop, "$g_talk_troop"),
    (troop_get_slot, ":cur_lord", "$g_talk_troop", slot_troop_father),
    (try_begin),
      (gt, ":cur_lord", 0),
      (str_store_string, s17, "str_father"),
    (else_try),
      (str_store_string, s17, "str_husband"),
    (try_end),
    ],
   "Oh, {playername}, you brought him back to me! Thank you ever so much for rescuing my {s17}.\
 Please, take this as some small repayment for your noble deed.", "lady_generic_mission_succeeded",
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 8),
     (add_xp_as_reward, 2000),
     (call_script, "script_troop_add_gold", "trp_player", 1500),
     (call_script, "script_end_quest", "qst_rescue_lord_by_replace"),
     ]],
]
