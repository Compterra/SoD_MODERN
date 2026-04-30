DIALOGS = [
[anyone, "town_dweller_ask_situation",
  [
    (party_slot_eq, "$current_town", slot_party_type, spt_village),
    (neg|party_slot_ge, "$current_town", slot_town_prosperity, 70),
  ],
   "We manage as country folk always do, {sir/madam}. One season is kind, the next bites back, and most years are made of patching roofs, saving seed, and praying the levy leaves enough behind to live on.", "town_dweller_talk", []],

[anyone, "town_dweller_ask_situation",
  [
    (party_slot_eq, "$current_town", slot_party_type, spt_town),
    (neg|party_slot_ge, "$current_town", slot_town_prosperity, 70),
  ],
   "We are getting by, {sir/madam}, though never so easily as the merchants make it sound. A good market day keeps a family warm for a week, and a bad one can empty a table just as quickly.", "town_dweller_talk", []],

[anyone, "town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 70)],
   "Times are hard, {sir/madam}. But we must count our blessings.", "town_dweller_talk", []],
]
