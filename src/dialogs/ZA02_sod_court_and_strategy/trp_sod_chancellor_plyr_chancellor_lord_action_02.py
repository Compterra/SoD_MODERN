DIALOGS = [
[trp_sod_chancellor|plyr, "chancellor_lord_action", [(call_script, "script_sod_chancellor_lord_recruitment_refresh"), (lt, "$territory", 1)], "I understand. We need more fiefs before we can support another lord.", "chancellor_talk_again", []],
[trp_sod_chancellor|plyr, "chancellor_lord_action", [(call_script, "script_sod_chancellor_lord_recruitment_refresh"), (lt, "$lords", 1)], "I understand. There are no homeland lords left to recruit.", "chancellor_talk_again", []],
[trp_sod_chancellor|plyr, "chancellor_lord_action", [], "Let's look at other topics to make decisions about.", "chancellor_talk_again", []],
]
