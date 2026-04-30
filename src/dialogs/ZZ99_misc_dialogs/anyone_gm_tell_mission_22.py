DIALOGS = [
[anyone, "gm_tell_mission", [
  (eq, "$random_quest_no", "qst_slavers_deal_with_good_guys"),
  (quest_get_slot, ":village", "qst_slavers_deal_with_good_guys", slot_quest_target_center),
  (str_store_party_name_link, s14, ":village"),
  ],"We've been making some pretty flourishing profit out of the inhabitants of {s14}, but recently a band of self-proclaimed heroes have ruined our business there.  Such arrogance cannot be tolerated, don't you agree?  Sadly, we can't interfere, as employing too many men may catch the eye of the local lord, and we don't wish to complicate things if we don't have to.  Just take your own best men and set things wrong like they should be.  You can earn quite some respect from us with this job, if you get my drift...", "gm_good_guys_ask", []],
]
