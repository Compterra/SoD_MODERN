SIMPLE_TRIGGERS = [
(2,
   [
       # Campaign AI cadence: every 2 hours. Processes already-decided party
       # AI; high-frequency party operations are covered by modernization tests.
       (call_script, "script_process_kingdom_parties_ai"),
    ]),
]
