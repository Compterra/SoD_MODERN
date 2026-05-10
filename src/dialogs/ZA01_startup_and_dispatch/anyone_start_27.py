DIALOGS = [
[anyone, "start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_serpent_host_raid_caravan"),
                         (check_quest_failed, "qst_serpent_host_raid_caravan"),
                         ],
   "You incompetent buffoon!\
 I will not forget this, {playername}.\
 Oh, be assured that I will not.", "gm_pretalk",
   [
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", -5),
    (call_script, "script_fail_quest", "qst_serpent_host_raid_caravan"),
    (call_script, "script_end_quest", "qst_serpent_host_raid_caravan")
    ]],
]
