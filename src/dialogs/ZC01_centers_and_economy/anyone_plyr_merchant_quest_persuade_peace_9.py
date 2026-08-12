DIALOGS = [
[anyone|plyr, "merchant_quest_persuade_peace_9", [], "I will carry the offer, but peace will need more than pretty words. Give me the names, and I will try to make them listen.", "merchant_quest_persuade_peace_10", [
    (setup_quest_text, "qst_persuade_lords_to_make_peace"),
    (call_script, "script_start_quest", "qst_persuade_lords_to_make_peace", "$g_talk_troop"),
]],
]
