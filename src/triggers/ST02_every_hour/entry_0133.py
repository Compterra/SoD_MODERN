SIMPLE_TRIGGERS = [
(12,
   [
     (call_script, "script_sod_company_accounts_accrue_wages"),
     (call_script, "script_sod_company_accounts_process_pay_promise"),
     (call_script, "script_sod_company_accounts_process_petition_check"),
     (call_script, "script_sod_company_accounts_process_desertion_check"),
     (call_script, "script_sod_company_accounts_process_mutiny_check"),
     (call_script, "script_sod_company_dialogue_schedule_spokesperson_incident"),
    ]),
]
