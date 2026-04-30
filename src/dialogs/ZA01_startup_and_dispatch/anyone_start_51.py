DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_hero_freed),
                      (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero)],
   "I am in your debt for freeing me, friend.", "freed_lord_answer",
   [
    (call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
   ]],
]
