DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_kill_local_merchant")],
   "The wretched truth is that I owe a considerable sum of money to one of the merchants here in {s3}.\
 I've no intention of paying it back, of course, but that loud-mouthed fool is making a terrible fuss about it.\
 He even had the audacity to come and threaten me -- me! --\
 with a letter of complaint to the trade guilds and bankers. Why, he'd ruin my good reputation!\
 So I need a {man/woman} I can trust, someone who will guarantee the man's silence. For good.", "lord_mission_told_kill_local_merchant",
   [
       (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
       (str_store_party_name_link, s3, "$current_town"),
       (setup_quest_text, "$random_quest_no"),
       (str_store_string, s2, "@{s9} asked you to assassinate a local merchant in {s3}."),
   ]],
]
