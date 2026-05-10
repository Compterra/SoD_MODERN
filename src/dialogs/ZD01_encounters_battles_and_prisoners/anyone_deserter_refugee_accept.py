DIALOGS = [
[anyone, "deserter_refugee_offer", [], "Protection sounds like a word from another life. We will try to remember how it feels.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 1),
    (call_script, "script_sod_note_hostile_reputation", 9),
    (call_script, "script_change_player_honor", 1),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
    (display_message, "@The deserters abandon the road as refugees under your protection."),
]],
]
