DIALOGS = [
[anyone, "village_elder_mission_failed", [], "Ah, I am sorry to hear that {sir/madam}. I'll try to think of something else.", "village_elder_pretalk",
   [(store_partner_quest, ":elder_quest"),
    (call_script, "script_abort_quest", ":elder_quest", 1)]],
]
