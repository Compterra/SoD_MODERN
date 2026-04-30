DIALOGS = [
[anyone, "gm_tell_mission", [
   (eq, "$random_quest_no", "qst_jotnar_clan_aid_warband"),
   (quest_get_slot, ":target_center", "qst_jotnar_clan_aid_warband", slot_quest_target_center),
   (str_store_party_name_link, s8, ":target_center"),
   ],
 "One of my Norn sisters just rushed to me and told that some of our brethren have been caught by an outnumbering enemy warband near {s8} and need help as soon as possible else they will be overwhelmed. We don't have many fighters to spare, and as such, your aid would be most welcome - help them win! Should you succeed, come back and we'll be more than eager to reward your help.", "gm_jc_aid_warband_quest_brief",
   []],
]
