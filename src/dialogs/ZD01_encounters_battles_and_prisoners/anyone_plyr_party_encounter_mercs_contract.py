DIALOGS = [
[anyone|plyr, "party_encounter_mercs", [
  (store_encountered_party, ":cur_party"),
  (party_is_active, ":cur_party"),
  (party_slot_eq, ":cur_party", slot_party_type, spt_ai_mercenaries),
  (call_script, "script_sod_merc_market_describe_ai_contract_to_s68", ":cur_party"),
  (eq, reg0, 1),
  ], "What work are you doing?", "party_encounter_mercs_contract", []],
]
