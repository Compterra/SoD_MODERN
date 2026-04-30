DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_capture_enemy_hero")],
 "There is a difficult job I need done, {playername}, and you may be the {man/one} who can carry it off.\
 I need someone to capture one of the noble lords of {s13} and bring him to me.\
 Afterwards, I'll be able to exchange him in return for a relative of mine held by {s13}.\
 It is a simple enough job, but whomever you choose will be guarded by an elite band of personal retainers.\
 Are you up for a fight?", "lord_tell_mission_capture_enemy_hero",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (str_store_faction_name, s13, ":quest_target_faction"),
    ]],
]
