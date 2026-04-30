DIALOGS = [
[anyone, "start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_serpent_host_raid_caravan"),
                         (check_quest_succeeded, "qst_serpent_host_raid_caravan"),
                         (quest_get_slot, ":quest_target_faction", "qst_serpent_host_raid_caravan", slot_quest_target_faction),
                         (str_store_faction_name, s13, ":quest_target_faction"),
                         ],
   "Brilliant work, {playername}! Your caravan raids really got their attention, I must say.", "gm_pretalk",
   [
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 5),
    (call_script, "script_troop_add_gold", "trp_player", 500),
    (add_xp_as_reward, 800),
    (call_script, "script_change_player_honor", -5),
    (call_script, "script_succeed_quest", "qst_serpent_host_raid_caravan"),
    (call_script, "script_end_quest", "qst_serpent_host_raid_caravan")
    ]],
]
