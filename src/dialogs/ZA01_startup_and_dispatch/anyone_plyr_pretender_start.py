DIALOGS = [
[anyone|plyr , "pretender_start",
   [
     (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
     (eq, "$pretender_told_story", 0)
     ],
   "What was your story again, {reg65?my lady:sir}?", "pretender_rebellion_cause_prelim", [
     ]],
]
