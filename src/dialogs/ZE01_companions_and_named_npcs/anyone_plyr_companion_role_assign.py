DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
  ],
  "Let's talk company duties.", "companion_role_discuss",
  []],

[anyone, "companion_role_discuss",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_companion_approval, 45),
    (troop_slot_eq, "$g_talk_troop", slot_troop_companion_role, sod_companion_role_none),
  ],
  "Not while this sits between us. Mend that first, then ask me for an office.", "member_talk",
  []],

[anyone, "companion_role_discuss",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_companion_approval, 45),
    (troop_slot_ge, "$g_talk_troop", slot_troop_companion_role, 1),
  ],
  "Trust is thin. I can stand down from this office, but I will not pretend it is sound.", "companion_role_low_trust_options",
  []],

[anyone, "companion_role_discuss",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (troop_slot_ge, "$g_talk_troop", slot_troop_companion_approval, 45),
  ],
  "What do you need from me?", "companion_role_options",
  []],

[anyone|plyr, "companion_role_low_trust_options",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_companion_approval, 45),
    (troop_slot_ge, "$g_talk_troop", slot_troop_companion_role, 1),
  ],
  "Stand down until trust is repaired.", "companion_role_stood_down",
  [
    (call_script, "script_sod_companion_assign_role", "$g_talk_troop", sod_companion_role_none),
  ]],

[anyone|plyr, "companion_role_low_trust_options",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
  ],
  "Leave it for now.", "member_talk",
  []],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (main_party_has_troop, "trp_npc1"),
    (neg|troop_slot_eq, "trp_npc1", slot_troop_companion_role, sod_companion_role_scout),
  ],
  "Borcha, scout ahead for the company.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc1", sod_companion_role_scout),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (main_party_has_troop, "trp_npc1"),
    (neg|troop_slot_eq, "trp_npc1", slot_troop_companion_role, sod_companion_role_quartermaster),
  ],
  "Borcha, watch the road stores.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc1", sod_companion_role_quartermaster),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
    (main_party_has_troop, "trp_npc2"),
    (neg|troop_slot_eq, "trp_npc2", slot_troop_companion_role, sod_companion_role_quartermaster),
  ],
  "Marnid, take charge of the stores.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc2", sod_companion_role_quartermaster),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
    (main_party_has_troop, "trp_npc2"),
    (neg|troop_slot_eq, "trp_npc2", slot_troop_companion_role, sod_companion_role_envoy),
  ],
  "Marnid, speak for us as envoy.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc2", sod_companion_role_envoy),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (main_party_has_troop, "trp_npc3"),
    (neg|troop_slot_eq, "trp_npc3", slot_troop_companion_role, sod_companion_role_surgeon),
  ],
  "Ymira, tend the wounded as surgeon.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc3", sod_companion_role_surgeon),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (main_party_has_troop, "trp_npc3"),
    (neg|troop_slot_eq, "trp_npc3", slot_troop_companion_role, sod_companion_role_envoy),
  ],
  "Ymira, speak softly where steel would fail.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc3", sod_companion_role_envoy),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (main_party_has_troop, "trp_npc4"),
    (neg|troop_slot_eq, "trp_npc4", slot_troop_companion_role, sod_companion_role_envoy),
  ],
  "Rolf, lend your name as envoy.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc4", sod_companion_role_envoy),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (main_party_has_troop, "trp_npc4"),
    (neg|troop_slot_eq, "trp_npc4", slot_troop_companion_role, sod_companion_role_captain),
  ],
  "Rolf, command a section of the line.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc4", sod_companion_role_captain),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (main_party_has_troop, "trp_npc5"),
    (neg|troop_slot_eq, "trp_npc5", slot_troop_companion_role, sod_companion_role_scout),
  ],
  "Baheshtur, scout the open ground.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc5", sod_companion_role_scout),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (main_party_has_troop, "trp_npc5"),
    (neg|troop_slot_eq, "trp_npc5", slot_troop_companion_role, sod_companion_role_captain),
  ],
  "Baheshtur, command the riders.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc5", sod_companion_role_captain),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (main_party_has_troop, "trp_npc6"),
    (neg|troop_slot_eq, "trp_npc6", slot_troop_companion_role, sod_companion_role_captain),
  ],
  "Firentis, keep discipline in the line.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc6", sod_companion_role_captain),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (main_party_has_troop, "trp_npc6"),
    (neg|troop_slot_eq, "trp_npc6", slot_troop_companion_role, sod_companion_role_envoy),
  ],
  "Firentis, carry our word as envoy.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc6", sod_companion_role_envoy),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (main_party_has_troop, "trp_npc7"),
    (neg|troop_slot_eq, "trp_npc7", slot_troop_companion_role, sod_companion_role_scout),
  ],
  "Deshavi, read the tracks for us.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc7", sod_companion_role_scout),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (main_party_has_troop, "trp_npc7"),
    (neg|troop_slot_eq, "trp_npc7", slot_troop_companion_role, sod_companion_role_spymaster),
  ],
  "Deshavi, keep the quiet roads watched.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc7", sod_companion_role_spymaster),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
    (main_party_has_troop, "trp_npc8"),
    (neg|troop_slot_eq, "trp_npc8", slot_troop_companion_role, sod_companion_role_captain),
  ],
  "Matheld, take command where the line must hold.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc8", sod_companion_role_captain),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (main_party_has_troop, "trp_npc9"),
    (neg|troop_slot_eq, "trp_npc9", slot_troop_companion_role, sod_companion_role_envoy),
  ],
  "Alayen, bear our standard as envoy.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc9", sod_companion_role_envoy),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (main_party_has_troop, "trp_npc9"),
    (neg|troop_slot_eq, "trp_npc9", slot_troop_companion_role, sod_companion_role_captain),
  ],
  "Alayen, command with the standard in mind.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc9", sod_companion_role_captain),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (main_party_has_troop, "trp_npc13"),
    (neg|troop_slot_eq, "trp_npc13", slot_troop_companion_role, sod_companion_role_captain),
  ],
  "Nizar, lead the charge when courage matters.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc13", sod_companion_role_captain),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (main_party_has_troop, "trp_npc13"),
    (neg|troop_slot_eq, "trp_npc13", slot_troop_companion_role, sod_companion_role_scout),
  ],
  "Nizar, scout for bold openings.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc13", sod_companion_role_scout),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (main_party_has_troop, "trp_npc10"),
    (neg|troop_slot_eq, "trp_npc10", slot_troop_companion_role, sod_companion_role_captain),
  ],
  "Bunduk, command for the common soldiers.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc10", sod_companion_role_captain),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (main_party_has_troop, "trp_npc10"),
    (neg|troop_slot_eq, "trp_npc10", slot_troop_companion_role, sod_companion_role_quartermaster),
  ],
  "Bunduk, watch the soldiers' stores.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc10", sod_companion_role_quartermaster),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (main_party_has_troop, "trp_npc11"),
    (neg|troop_slot_eq, "trp_npc11", slot_troop_companion_role, sod_companion_role_quartermaster),
  ],
  "Katrin, keep the stores honest.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc11", sod_companion_role_quartermaster),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (main_party_has_troop, "trp_npc11"),
    (neg|troop_slot_eq, "trp_npc11", slot_troop_companion_role, sod_companion_role_surgeon),
  ],
  "Katrin, help tend the camp as surgeon.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc11", sod_companion_role_surgeon),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (main_party_has_troop, "trp_npc12"),
    (neg|troop_slot_eq, "trp_npc12", slot_troop_companion_role, sod_companion_role_surgeon),
  ],
  "Jeremus, take charge of the wounded.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc12", sod_companion_role_surgeon),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (main_party_has_troop, "trp_npc12"),
    (neg|troop_slot_eq, "trp_npc12", slot_troop_companion_role, sod_companion_role_envoy),
  ],
  "Jeremus, speak for restraint when tempers rise.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc12", sod_companion_role_envoy),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (main_party_has_troop, "trp_npc16"),
    (neg|troop_slot_eq, "trp_npc16", slot_troop_companion_role, sod_companion_role_spymaster),
  ],
  "Klethi, keep the quiet doors open.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc16", sod_companion_role_spymaster),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (main_party_has_troop, "trp_npc16"),
    (neg|troop_slot_eq, "trp_npc16", slot_troop_companion_role, sod_companion_role_scout),
  ],
  "Klethi, scout the road no one admits using.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc16", sod_companion_role_scout),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (main_party_has_troop, "trp_npc14"),
    (neg|troop_slot_eq, "trp_npc14", slot_troop_companion_role, sod_companion_role_captain),
  ],
  "Lezalit, drill the line as captain.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc14", sod_companion_role_captain),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (main_party_has_troop, "trp_npc14"),
    (neg|troop_slot_eq, "trp_npc14", slot_troop_companion_role, sod_companion_role_engineer),
  ],
  "Lezalit, oversee the works as engineer.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc14", sod_companion_role_engineer),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (main_party_has_troop, "trp_npc15"),
    (neg|troop_slot_eq, "trp_npc15", slot_troop_companion_role, sod_companion_role_engineer),
  ],
  "Artimenner, inspect the works as engineer.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc15", sod_companion_role_engineer),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (main_party_has_troop, "trp_npc15"),
    (neg|troop_slot_eq, "trp_npc15", slot_troop_companion_role, sod_companion_role_quartermaster),
  ],
  "Artimenner, organize the tools and stores.", "companion_role_assigned",
  [
    (call_script, "script_sod_companion_assign_role", "trp_npc15", sod_companion_role_quartermaster),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (troop_slot_ge, "$g_talk_troop", slot_troop_companion_role, 1),
  ],
  "Stand down from your camp office for now.", "companion_role_stood_down",
  [
    (call_script, "script_sod_companion_assign_role", "$g_talk_troop", sod_companion_role_none),
  ]],

[anyone|plyr, "companion_role_options",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
  ],
  "Leave the offices as they are.", "member_talk",
  []],

[anyone, "companion_role_assigned",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (troop_slot_ge, "$g_talk_troop", slot_troop_companion_approval, 45),
    (troop_slot_ge, "$g_talk_troop", slot_troop_companion_role, 1),
  ],
  "Understood. I will see it done.", "member_talk",
  []],

[anyone, "companion_role_stood_down",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_companion_role, sod_companion_role_none),
  ],
  "Understood. I will stand down for now.", "member_talk",
  []],
]
