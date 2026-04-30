DIALOGS = [
[party_tpl|pt_runaway_slaves, "start",
   [(quest_get_slot, ":home_center", "qst_slavers_bring_back_runaway_slaves", slot_quest_target_center),
    (str_store_party_name, s5, ":home_center")], "We are on our way back to {s5} {sir/madam}.", "runaway_slave_talk_again_return", []],
]
