DIALOGS = [
[anyone, "hostile_redirect_bribe_offer", [], "Now that is a road worth taking. Keep your silver hand open and your back turned.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 600),
    (play_sound, "snd_money_paid"),
    (call_script, "script_sod_redirect_hostile_party_for_bribe", "$g_encountered_party"),
    (call_script, "script_sod_note_hostile_reputation", 7),
]],
]
