DIALOGS = [
[anyone|plyr, "prisoner_chat_menu", [(store_current_day, ":today"), (troop_slot_eq, "$g_talk_troop", slot_prisoner_rejected_day, ":today")],
    "Are you sure you will not reconsider my offer?", "prisoner_chat_offer_again", [(store_random_in_range, reg60, 0, 100), (store_skill_level, reg61, "skl_persuasion", "trp_player"), ]],
]
