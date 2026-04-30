DIALOGS = [
[anyone, "start",
   [(eq, "$caravan_escort_state", 1),
    (eq, "$g_encountered_party", "$caravan_escort_party_id"),
    (eq, "$talk_context", tc_party_encounter),
    ],
   "We've made it this far... Is everything clear up ahead?", "talk_caravan_escort", []],
]
