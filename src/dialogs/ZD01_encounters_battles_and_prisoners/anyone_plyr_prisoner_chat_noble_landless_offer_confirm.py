DIALOGS = [
[anyone|plyr, "prisoner_chat_noble_landless_offer_confirm", [],
   "Then swear it now. Your chains come off when your oath is spoken.", "close_window",
   [
     (call_script, "script_sod_lord_apply_player_landless_persuasion", "$g_talk_troop", 2),
     (assign, ":center_no", reg1),
     (try_begin),
       (is_between, ":center_no", walled_centers_begin, walled_centers_end),
       (str_store_party_name, s40, ":center_no"),
       (display_message, "@A former prisoner has sworn to you and taken {s40} as a fief.", 0x99CCFF),
     (try_end),
   ]],
]
