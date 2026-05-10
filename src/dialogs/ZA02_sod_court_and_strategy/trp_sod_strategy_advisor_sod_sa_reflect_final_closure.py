DIALOGS = [
[trp_sod_strategy_advisor, "sod_sa_reflect_final_closure", [
    (call_script, "script_sod_strategy_advisor_get_trust_band_to_reg"),
    (try_begin),
      (ge, reg0, sod_mentor_trust_confident),
      (str_store_string, s1, "@That you are no longer my student. I can still advise you, argue with you, and irritate you into better plans, but the war has stopped being your father's unfinished sentence. It is yours now, and you did not let the Legion write the ending."),
    (else_try),
      (str_store_string, s1, "@That victory is not absolution. The Legion is broken, yes. Now comes the harder proof. Whether the realm left behind needs fewer chains than the empire you destroyed. I can still advise you. I cannot carry that answer for you."),
    (try_end),
], "{s1}", "sod_sa_pretalk", []],
]
