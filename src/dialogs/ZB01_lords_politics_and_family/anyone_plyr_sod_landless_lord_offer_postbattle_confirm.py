DIALOGS = [
[anyone|plyr, "sod_landless_lord_offer_postbattle_confirm", [],
   "Then rise as my vassal. Betray that oath, and the next defeat will not be so generous.", "close_window",
   [
     (call_script, "script_sod_lord_apply_player_landless_persuasion", "$g_talk_troop", 1),
     (assign, ":center_no", reg1),
     (try_begin),
       (is_between, ":center_no", walled_centers_begin, walled_centers_end),
       (str_store_party_name, s40, ":center_no"),
       (display_message, "@A landless lord has sworn to you and taken {s40} as a fief.", 0x99CCFF),
     (try_end),
   ]],
]
