DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_raid_caravan_to_start_war"),
                         (check_quest_succeeded, "qst_raid_caravan_to_start_war"),
                         (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
                         (str_store_faction_name, s13, ":quest_target_faction"),
                         ],
   "Brilliant work, {playername}! Your caravan raids really got their attention, I must say.\
 I've just received word that {s13} has declared war!\
 Now the time has come for us to reap the benefits of our hard work, {playername}.\
 And by that I of course mean taking and plundering {s13} land!\
 This war is going to make us rich {men/souls}, mark my words!", "lord_pretalk",
   [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
    (try_for_range, ":vassal", kingdom_heroes_begin, kingdom_heroes_end),
      (store_troop_faction, ":vassal_fac", ":vassal"),
      (eq, ":vassal_fac", "$players_kingdom"),
      (neq,  ":vassal", "$g_talk_troop"),
      (store_random_in_range, ":rel_change", -5, 4),
      (call_script, "script_change_player_relation_with_troop", ":vassal", ":rel_change"),
    (try_end),
    #TODO: Add gold reward notification before the quest is given. 500 gold is not mentioned anywhere.
    (call_script, "script_troop_add_gold", "trp_player", 500),
    (add_xp_as_reward, 2000),
    (call_script, "script_change_player_honor", -5),
    (call_script, "script_end_quest", "qst_raid_caravan_to_start_war")
    ]],
]
