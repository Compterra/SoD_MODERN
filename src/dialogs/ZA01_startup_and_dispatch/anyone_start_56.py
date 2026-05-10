DIALOGS = [
[anyone , "start",
   [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (eq, "$g_talk_troop", "$supported_pretender"),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_state, sfs_inactive),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     ],
   "[Our first task is to seize a fortress. Then other lords will join us.]", "pretender_start", [
     ]],
]
