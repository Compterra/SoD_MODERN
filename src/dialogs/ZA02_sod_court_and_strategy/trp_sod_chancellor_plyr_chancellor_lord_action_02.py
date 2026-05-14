DIALOGS = [
[trp_sod_chancellor|plyr, "chancellor_lord_action", [(call_script, "script_sod_chancellor_lord_recruitment_refresh"), (lt, "$territory", 1)], "Then we wait. A title without land would shame the crown.", "chancellor_talk_again", []],
[trp_sod_chancellor|plyr, "chancellor_lord_action", [(call_script, "script_sod_chancellor_lord_recruitment_refresh"), (lt, "$lords", 1)], "Then there is no one left worth summoning.", "chancellor_talk_again", []],
[trp_sod_chancellor|plyr, "chancellor_lord_action", [], "Leave the summons for now. I have other business.", "chancellor_talk_again", []],
]
