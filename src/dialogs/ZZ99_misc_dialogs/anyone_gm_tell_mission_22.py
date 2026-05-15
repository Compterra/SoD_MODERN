DIALOGS = [
[anyone, "gm_tell_mission", [
  (eq, "$random_quest_no", "qst_slavers_deal_with_good_guys"),
  (quest_get_slot, ":village", "qst_slavers_deal_with_good_guys", slot_quest_target_center),
  (str_store_party_name_link, s14, ":village"),
  ],"The people of {s14} used to pay quietly. Now a band of locals playing hero has shut the road and made us look weak. We cannot send a column without drawing the lord's eye. Take your own men, break them, and the Slavers will remember it.", "gm_good_guys_ask", []],
]
