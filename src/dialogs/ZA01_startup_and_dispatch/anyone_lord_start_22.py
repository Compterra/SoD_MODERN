DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_deal_with_bandits_at_lords_village"),
                         (check_quest_concluded, "qst_deal_with_bandits_at_lords_village")],
   "Damn it, {playername}. I heard that you were unable to drive off the bandits from my village of {s5}, and thanks to you, my village now lies in ruins.\
 Everyone said that you were a capable warrior, but appearently, they were wrong.", "lord_pretalk",
   [
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
       (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
       (quest_get_slot, ":village", "qst_deal_with_bandits_at_lords_village", slot_quest_target_center),
       (str_store_party_name, s5, ":village"),
       ]],
]
