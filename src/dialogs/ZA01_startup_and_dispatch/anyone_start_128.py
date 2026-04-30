DIALOGS = [
[anyone , "start", [(is_between, "$g_talk_troop", mayors_begin, mayors_end)],
   "Good day, {playername}.", "mayor_begin",
   [
     #Delete last offered quest if peace is formed.
     (try_begin),
       (eq, "$merchant_offered_quest", "qst_persuade_lords_to_make_peace"),
       (party_get_slot, ":target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
       (party_get_slot, ":object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
       (store_relation, ":reln", ":target_faction", ":object_faction"),
       (ge, ":reln", 0),
       (assign, "$merchant_quest_last_offerer", -1),
       (assign, "$merchant_offered_quest", -1),
     (try_end),
     ]],
]
