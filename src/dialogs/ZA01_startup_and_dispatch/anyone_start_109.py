DIALOGS = [
[anyone , "start", [(store_conversation_troop, reg(1)), (ge, reg(1), tavernkeepers_begin), (lt, reg(1), tavernkeepers_end)],
   "Good day dear {sir/madam}. How can I help you?", "tavernkeeper_talk",
   [
   (store_encountered_party, reg(2)),
   (party_get_slot, "$tavernkeeper_party", reg(2), slot_town_mercs),
    ]],
]
