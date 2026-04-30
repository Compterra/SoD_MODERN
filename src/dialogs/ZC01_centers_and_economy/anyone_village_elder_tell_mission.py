DIALOGS = [
[anyone, "village_elder_tell_mission", [(eq, "$random_quest_no", "qst_deliver_grain")],
   "{My good sir/My good lady}, our village has been going through such hardships lately.\
 The harvest has been bad, and recently some merciless bandits took away our seed grain that we had reserved for the planting season.\
 If we cannot find some grain soon, we will not be able to plant our fields and then we will have nothing to eat for the coming year.\
 If you can help us, we would be indebted to you forever.", "village_elder_tell_deliver_grain_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link, s3, ":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s3} asked you to bring {reg5} packs of wheat to the village."),
   ]],
]
