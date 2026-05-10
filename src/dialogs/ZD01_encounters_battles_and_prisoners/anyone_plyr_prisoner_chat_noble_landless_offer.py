DIALOGS = [
[anyone|plyr, "prisoner_chat_noble", [
    (call_script, "script_sod_lord_player_can_persuade_landless_to_reg", "$g_talk_troop", 2),
    (eq, reg0, 1),
    (str_store_party_name, s40, reg2),
  ],
   "Your ruler left you landless. I can give you {s40}. Swear to me, and leave this tent as a vassal, not a prisoner.", "prisoner_chat_noble_landless_offer", []],
]
