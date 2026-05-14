DIALOGS = [
[trp_npc12, "member_chat", [
    (main_party_has_troop, "trp_npc12"),
    (eq, "$g_talk_troop", "trp_npc12"),
    (eq, "$g_sod_tax_courier_last_social_event", 1),
    (ge, "$g_sod_tax_courier_nonhostile_coercions", 1),
    (store_current_day, ":cur_day"),
    (neq, "$g_sod_tax_courier_companion_rumor_seen_day", ":cur_day"),
    (store_sub, ":age", ":cur_day", "$g_sod_tax_courier_last_social_event_day"),
    (is_between, ":age", 0, 10),
    (try_begin),
      (is_between, "$g_sod_tax_courier_last_social_event_center", centers_begin, centers_end),
      (str_store_party_name, s13, "$g_sod_tax_courier_last_social_event_center"),
    (else_try),
      (str_store_string, s13, "@that estate"),
    (try_end),
  ],
  "Captain. About the courier from {s13}. There is still a difference between defeating an enemy and teaching harmless men to fear our shadow. I hope we remember which road we meant to walk.",
  "member_talk",
  [
    (store_current_day, "$g_sod_tax_courier_companion_rumor_seen_day"),
    (call_script, "script_sod_companion_shift_approval", "trp_npc12", -1),
  ]],
]
