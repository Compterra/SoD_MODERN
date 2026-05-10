DIALOGS = [
[trp_sod_chancellor, "chancellor_landless_report",
    [
      (call_script, "script_sod_faction_update_campaign_health", "fac_player_supporters_faction"),
      (call_script, "script_sod_lord_describe_landless_politics_to_s68", "fac_player_supporters_faction"),
    ],
    "{s60}", "chancellor_talk_again", []],
]
