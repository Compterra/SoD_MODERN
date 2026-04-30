DIALOGS = [
[anyone, "village_elder_tell_mission", [(eq, "$random_quest_no", "qst_deliver_cattle")],
   "Bandits have driven away our cattle. Our pastures are empty. If we had just a few heads of cattle we could start to raise a herd again.",
   "village_elder_tell_deliver_cattle_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link, s3, ":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s3} asked you to bring {reg5} heads of cattle to the village."),
   ]],
]
