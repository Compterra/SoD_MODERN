DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_raid_caravan_to_start_war"),
                         (check_quest_failed, "qst_raid_caravan_to_start_war"),
                         ],
   "You incompetent buffoon!\
 What in Hell made you think that getting yourself captured while trying to start a war was a good idea?\
 These plans took months to prepare, and now everything's been ruined! I will not forget this, {playername}.\
 Oh, be assured that I will not.", "lord_pretalk",
   [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -10),
    (call_script, "script_end_quest", "qst_raid_caravan_to_start_war")
    ]],
]
