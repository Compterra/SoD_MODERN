DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_deal_with_bandits_at_lords_village"),
                         (check_quest_succeeded, "qst_deal_with_bandits_at_lords_village")],
   "{playername}, I was told that you have crushed the bandits at my village of {s5}. Please know that I am most grateful to you for that.\
 Please, let me pay the expenses of your campaign. Here, I hope these {reg14} denars will be adequate.", "lord_deal_with_bandits_completed",
   [
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
       (store_character_level, ":level", "trp_player"),
       (store_mul, ":reward", ":level", 20),
       (val_add, ":reward", 300),
       (call_script, "script_troop_add_gold", "trp_player", ":reward"),
       (add_xp_as_reward, 350),
       (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
       (assign, reg14, ":reward"),
       (quest_get_slot, ":village", "qst_deal_with_bandits_at_lords_village", slot_quest_target_center),
       (str_store_party_name, s5, ":village"),
       ]],
]
