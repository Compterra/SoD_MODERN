DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     (party_get_slot, ":info_faction", "$g_encountered_party", slot_center_traveler_info_faction),
                     (str_store_faction_name, s17, ":info_faction"),
                     ],
   "Greetings. They say you're the kind of {man/woman} who'd be interested to hear that I travel frequently to {s17}. I'll tell you all I know for a mere 100 denars.", "tavern_traveler_answer", []],
]
