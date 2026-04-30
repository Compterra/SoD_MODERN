DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     (call_script, "script_store_troop_name", s10, "$g_talk_troop"),
                     (eq, "$g_talk_troop_met", 0),
                     ],
   "Greetings, friend. You look like the kind of {man/person} who'd do well to know me.\
 I travel a lot all across Calradia and keep an open ear.\
 I can provide you information that you might find useful. For a meager price of course.", "tavern_traveler_talk", [(assign, "$traveler_land_asked", 0)]],
]
