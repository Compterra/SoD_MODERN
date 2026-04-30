DIALOGS = [
[anyone, "town_dweller_ask_situation",
  [
    (party_slot_eq, "$current_town", slot_party_type, spt_village),
    (neg|party_slot_ge, "$current_town", slot_town_prosperity, 30),
  ],
   "Times are cruel here, {sir/madam}. The seed goes into thin soil, the rent still comes due, and by winter's end too many cottages are counting crusts instead of meals.", "town_dweller_talk", []],

[anyone, "town_dweller_ask_situation",
  [
    (party_slot_eq, "$current_town", slot_party_type, spt_town),
    (neg|party_slot_ge, "$current_town", slot_town_prosperity, 30),
  ],
   "Times are cruel here, {sir/madam}. Work is scarce, bread grows dear by the week, and whole streets are learning how long a family can stretch one loaf before hunger turns mean.", "town_dweller_talk", []],

[anyone, "town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 30)],
   "Times are hard, {sir/madam}. We work hard all day and yet we go to sleep hungry most nights.", "town_dweller_talk", []],
]
