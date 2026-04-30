DIALOGS = [
[anyone, "gm_tell_mission", [
   (eq, "$random_quest_no", "qst_black_army_aid_warband"),
   (quest_get_slot, ":target_center", "qst_black_army_aid_warband", slot_quest_target_center),
   (str_store_party_name_link, s8, ":target_center"),
   ],
 "As much as I'd like to believe, even the Black Army isn't capable of doing everything by itself.  Especially when the logistics are screwed up... but let's get to the point.  A pidgeon arrived with a letter, saying that immediate reinforcements are needed in {s8} to counter a bypassing enemy group.  The problem?  The letter is at least a week old, meaning it arrived late and it's questionable if there is anything left to reinforce.  Take your own warband and check out the place.  If there are any survivors left, help them out.  If not but the enemy is there... well, I'll leave that decision up to you.  In either case, report back afterwards.  Got it?  Good.  Then get to work!", "gm_aid_warband_quest_brief",
   []],
]
