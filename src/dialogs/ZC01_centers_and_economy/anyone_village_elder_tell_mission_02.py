DIALOGS = [
[anyone, "village_elder_tell_mission", [(eq, "$random_quest_no", "qst_train_peasants_against_bandits")],
   "We are suffering greatly at the hands of a group of bandits. They take our food and livestock,\
 and kill anyone who doesn't obey them immediately. Our men are angry that we cannot defend ourselves, but we are only simple farmers...\
 However, with some help, I think that some of the people here could be more than that.\
 We just need an experienced warrior to teach us how to fight.",
   "village_elder_tell_train_peasants_against_bandits_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link, s13, ":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s13} asked you to train {reg5} peasants to fight local bandits."),
   ]],
]
