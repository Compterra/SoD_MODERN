SCRIPTS = [
("sod_rtc_hounds_terms_handle_envoy",
    [
      (store_script_param, ":envoy_handling", 1),
      (quest_set_slot, "qst_rtc_hounds_terms", slot_quest_sod_chain_choice, ":envoy_handling"),

      (try_begin),
        (eq, ":envoy_handling", 1),
        (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 1),
        (str_store_string, s49, "@You released the Imperial envoy with your answer intact. Even enemies can carry useful witnesses."),
      (else_try),
        (eq, ":envoy_handling", 2),
        (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 1),
        (call_script, "script_sod_companion_apply_player_action", sod_companion_action_diplomacy_betrayal, 1),
        (str_store_string, s49, "@You detained the Imperial envoy. The Hound will call it lawlessness; harder captains will call it leverage."),
      (else_try),
        (eq, ":envoy_handling", 3),
        (call_script, "script_sod_companion_apply_player_action", sod_companion_action_scout_warning, 1),
        (str_store_string, s49, "@You sent the envoy back with a counter-demand. It buys no peace, but it makes the next Imperial move less clean."),
      (else_try),
        (call_script, "script_sod_companion_apply_player_action", sod_companion_action_retreat_or_fail, 1),
        (str_store_string, s49, "@The envoy left with confusion instead of a clean answer. Marius will decide what that means before you can."),
      (try_end),

      (add_quest_note_from_sreg, "qst_rtc_hounds_terms", 4, s49, 0),
  ]),
]
