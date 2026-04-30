DIALOGS = [
[anyone, "merchant_quest_persuade_peace_8", [], "Most of the merchants in the town will gladly open up their purses to support such a plan.\
 I think we can collect {reg12} denars between ourselves.\
 We will be happy to reward you with that sum, if you can work this out.\
 Convince {s12} and {s13} to accept a peace settlement,\
 and if either of them proves too stubborn, make sure he falls captive and can not be ransomed until a peace deal is settled.",
   "merchant_quest_persuade_peace_9", [
       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
       (call_script, "script_store_troop_name_link", s12, ":quest_object_troop"),
       (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
       (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
       (assign, reg12, ":quest_reward")]],
]
