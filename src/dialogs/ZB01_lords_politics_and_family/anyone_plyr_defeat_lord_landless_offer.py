DIALOGS = [
[anyone|plyr, "defeat_lord_answer", [
    (call_script, "script_sod_lord_player_can_persuade_landless_to_reg", "$g_talk_troop", 1),
    (eq, reg0, 1),
    (str_store_party_name, s40, reg2),
  ],
   "You are landless, beaten, and still worth more than chains. Swear to me, and I will give you {s40} to hold.", "sod_landless_lord_offer_postbattle", []],
]
