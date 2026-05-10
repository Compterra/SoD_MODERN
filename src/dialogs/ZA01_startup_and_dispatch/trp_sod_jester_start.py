DIALOGS = [
[trp_sod_jester, "start", [
   (this_or_next|eq, "$cheat_mode", 1),
   (eq, "$g_sod_cheat_mode", 1),
   (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
   ], "My, My, who the hell are You?", "jester_intro", [
   ]],
]
