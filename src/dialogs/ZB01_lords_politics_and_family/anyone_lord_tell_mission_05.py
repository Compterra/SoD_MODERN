DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_raise_troops")],
   "No lord should have to admit this, {playername}, but I was inspecting my soldiers the other day\
 and there are men here who don't know which end of a sword to hold.\
 {s44}\
 You are a warrior of renown, {playername}. Will you train some troops for me?\
 I would be grateful to you.", "lord_tell_mission_raise_troops", [
    (troop_get_slot, ":training_string", "$g_talk_troop", slot_lord_reputation_type),
    (val_add, ":training_string", "str_troop_train_request_default"),
    (str_store_string, 44, ":training_string")
     ]],
]
