DIALOGS = [
[anyone|plyr, "merchant_quest_deal_with_night_bandits", [],
   "Killing bandits? Why, certainly!",
   "deal_with_night_bandits_quest_taken",
   [
     (str_store_party_name_link, s14, "$g_encountered_party"),
     (setup_quest_text, "qst_deal_with_night_bandits"),
     (str_store_string, s2, "@The Guildmaster of {s14} has asked you to deal with a group of bandits terrorising the streets of {s14}. They only come out at night, and only attack lone travellers on the streets."),
     (call_script, "script_start_quest", "qst_deal_with_night_bandits", "$g_talk_troop"),
     ]],
]
