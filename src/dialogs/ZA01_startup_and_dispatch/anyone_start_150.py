DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter), (store_encountered_party, reg(5)), (party_get_template_id, reg(7), reg(5)), (eq, reg(7), "pt_sea_raiders")],
   "I will drink from your skull!", "battle_reason_stated", [(play_sound, "snd_encounter_sea_raiders")]],
]
