DIALOGS = [
[anyone, "runaway_serf_intro_2", [(quest_get_slot, ":target_center", "qst_bring_back_runaway_serfs", slot_quest_target_center),
                                   (str_store_party_name, s6, ":target_center"),
                                   (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                   (str_store_party_name, s1, ":quest_object_center")],
   "My good {sir/madam}. Life in {s1} was breaking us. We worked until dark and still slept hungry.\
 We are going to {s6} to start again, where a back bent from labor still belongs to a person.", "runaway_serf_intro_3", []],
]
