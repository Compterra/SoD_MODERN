MENUS = [
(
    "rtc_borrowed_names", mnf_disable_all_keys,
    "{s1}^^In the refugee camp, Lysara Veyne sits beside a crate with a torn ledger across her knees. 'What name should I write beside yours?'",
    "none",
    [
      (try_begin),
        (neq, "$g_sod_rtc_enabled", 1),
        (jump_to_menu, "mnu_start_phase_2"),
      (try_end),
      (set_background_mesh, "mesh_pic_chr2_faction"),
      (quest_get_slot, ":salvage", "qst_rtc_borrowed_names", slot_quest_rtc_salvage_choice),
      (try_begin),
        (eq, ":salvage", sod_rtc_salvage_wounded),
        (str_store_string, s1, "@The wounded you saved lie close enough to hear the answer. A name chosen here will be measured against mercy first."),
      (else_try),
        (eq, ":salvage", sod_rtc_salvage_baggage),
        (str_store_string, s1, "@The baggage and stores you saved sit behind Lysara's crate. A name chosen here will be measured against survival and accounts."),
      (else_try),
        (eq, ":salvage", sod_rtc_salvage_papers),
        (str_store_string, s1, "@The military papers you saved keep drawing Garran's eye. A name chosen here will be measured against proof and command."),
      (else_try),
        (eq, ":salvage", sod_rtc_salvage_abandoned),
        (str_store_string, s1, "@The road you abandoned has already become a silence in camp. A name chosen here will be measured against who did not reach the fire."),
      (else_try),
        (str_store_string, s1, "@The camp is still deciding what survived. A name chosen here may become the first answer."),
      (try_end),
    ],
    [
      ("rtc_identity_noble", [], "The name I was born with. Let them know what survived.", [
        (call_script, "script_sod_rtc_borrowed_names_choose_identity", sod_rtc_reputation_foreign_noble),
        (jump_to_menu, "mnu_rtc_hound_sign"),
      ]),
      ("rtc_identity_captain", [], "No house. No titles. Only the company I keep.", [
        (call_script, "script_sod_rtc_borrowed_names_choose_identity", sod_rtc_reputation_free_captain),
        (jump_to_menu, "mnu_rtc_hound_sign"),
      ]),
      ("rtc_identity_refugee", [], "Write nothing yet. Names are debts.", [
        (call_script, "script_sod_rtc_borrowed_names_choose_identity", sod_rtc_reputation_refugee),
        (jump_to_menu, "mnu_rtc_hound_sign"),
      ]),
      ("rtc_identity_avenger", [], "Write that I am owed blood.", [
        (call_script, "script_sod_rtc_borrowed_names_choose_identity", sod_rtc_reputation_avenger),
        (jump_to_menu, "mnu_rtc_hound_sign"),
      ]),
      ("rtc_identity_trader", [], "Write that I intend to buy us another morning.", [
        (call_script, "script_sod_rtc_borrowed_names_choose_identity", sod_rtc_reputation_trade_operator),
        (jump_to_menu, "mnu_rtc_hound_sign"),
      ]),
    ]
  ),
]
