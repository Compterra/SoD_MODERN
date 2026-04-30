DIALOGS = [
[anyone|plyr, "lord_talk", [(check_quest_active, "qst_slave_q1"),
                             (quest_get_slot, ":quest_target_troop", "qst_slave_q1", slot_quest_target_troop),
                             (eq, "$g_talk_troop", ":quest_target_troop"),],
   "Diego sent me. He's kept imprisoned unjustly by the Slavers in Jelkala.", "prison_break_lord_talk_1",
   []],
]
