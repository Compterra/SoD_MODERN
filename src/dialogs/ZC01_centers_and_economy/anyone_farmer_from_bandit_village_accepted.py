DIALOGS = [
[anyone, "farmer_from_bandit_village_accepted", [],
   "God bless you, {sir/madam}. Our village is {s7}. It is not too far from here.", "close_window",
   [(quest_get_slot, ":target_center", "qst_eliminate_bandits_infesting_village", slot_quest_target_center),
    (str_store_party_name_link, s7, ":target_center"),
    (setup_quest_text, "qst_eliminate_bandits_infesting_village"),
    (str_store_string, s2, "@A villager from {s7} begged you to save their village from the bandits that took refuge there."),
    (call_script, "script_start_quest", "qst_eliminate_bandits_infesting_village", "$g_talk_troop"),
    ]],
]
