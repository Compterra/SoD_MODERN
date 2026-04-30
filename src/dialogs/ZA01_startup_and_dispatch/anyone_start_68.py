DIALOGS = [
[anyone, "start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (check_quest_active, "qst_duel_for_lady"),
    (check_quest_succeeded, "qst_duel_for_lady"),
    (quest_slot_eq, "qst_duel_for_lady", slot_quest_giver_troop, "$g_talk_troop"),
    (le, "$talk_context", tc_siege_commander),
    (quest_get_slot, ":quest_target_troop", "qst_duel_for_lady", slot_quest_target_troop),
    (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
    ],
   "My dear {playername}, how joyous to see you again! I heard you gave that vile {s13} a well-deserved lesson.\
 I hope he never forgets his humiliation.\
 I've a reward for you, but I fear it's little compared to what you've done for me.", "lady_qst_duel_for_lady_succeeded_1", []],
]
