DIALOGS = [
[party_tpl|pt_sod_deserters, "start", [
      (eq, "$talk_context", tc_party_encounter),
      (call_script, "script_sod_store_hostile_greeting"),
                    ], "{s5}", "deserter_talk", []],
]
