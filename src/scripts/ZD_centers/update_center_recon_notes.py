SCRIPTS = [
("update_center_recon_notes",
    [
      (store_script_param_1, ":center_no"),
      (str_clear, s49),
      (add_party_note_from_sreg, ":center_no", 1, s49, 0),
      (try_begin),
        (is_between, ":center_no", centers_begin, centers_end),
        # The encyclopedia note is a quick field read, not a simulation ledger.
        # Full owner-facing figures remain in the dedicated fief reports.
        (call_script, "script_sod_store_center_recon_brief_to_s68", ":center_no"),
        (str_store_string_reg, s49, s68),
        (add_party_note_from_sreg, ":center_no", 1, s49, 1),
      (try_end),
    ]),
]
