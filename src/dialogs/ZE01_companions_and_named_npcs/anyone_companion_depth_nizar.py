DIALOGS = [
[anyone, "companion_depth_nizar_charge_pending", [
    (eq, "$g_sod_nizar_charge_witnessed", 1),
    (eq, "$g_sod_nizar_charge_confronted", 1),
  ],
  "The shape of it is speed, surprise, applause if we live, and very stern poetry if we do not. I ask only that we choose the sort of beautiful danger we can afford.",
  "companion_depth_nizar_charge_choice",
  []],

[anyone, "companion_depth_nizar_charge_pending", [
    (eq, "$g_sod_nizar_charge_witnessed", 1),
    (eq, "$g_sod_nizar_charge_confronted", 0),
  ],
  "The route is marked. Now we test the charge lane before the poets improve our mistakes.",
  "member_talk",
  []],

[anyone, "companion_depth_nizar_charge_pending", [
    (eq, "$g_sod_nizar_charge_witnessed", 0),
  ],
  "Before it becomes a charge, it must become a route. Let me mark the dust, the blind turn, and the way home.",
  "member_talk",
  []],

[anyone|plyr, "companion_depth_nizar_charge_choice", [
    (eq, "$g_sod_nizar_charge_witnessed", 1),
    (eq, "$g_sod_nizar_charge_confronted", 1),
  ],
  "Make the charge work by planning the way out first.", "member_talk",
  [
    (assign, "$g_sod_nizar_charge_pending", 0),
    (assign, "$g_sod_nizar_charge_result_grade", 3),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 2),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc13", 1),
    (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
    (call_script, "script_sod_companion_nizar_apply_charge_payoff"),
    (display_message, "@The charge keeps its drama and gains an exit. The Impossible Charge remembers glory with survivors.", 0x99CCFF),
  ]],

[anyone|plyr, "companion_depth_nizar_charge_choice", [
    (eq, "$g_sod_nizar_charge_witnessed", 1),
    (eq, "$g_sod_nizar_charge_confronted", 1),
  ],
  "Take the dazzling charge before anyone can make it sensible.", "member_talk",
  [
    (assign, "$g_sod_nizar_charge_pending", 0),
    (try_begin),
      (lt, "$g_sod_nizar_charge_result_grade", 2),
      (assign, "$g_sod_nizar_charge_result_grade", 2),
    (try_end),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc13", 2),
    (try_begin),
      (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
      (troop_set_slot, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    (else_try),
      (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
      (call_script, "script_sod_companion_advance_personal_quest", "trp_npc13", 1),
      (call_script, "script_sod_companion_nizar_apply_charge_payoff"),
    (try_end),
    (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
    (display_message, "@Nizar laughs like a banner in high wind. The charge will need luck, speed, and a better ending than most songs earn.", 0xCCCC66),
  ]],

[anyone|plyr, "companion_depth_nizar_charge_choice", [
    (eq, "$g_sod_nizar_charge_witnessed", 1),
    (eq, "$g_sod_nizar_charge_confronted", 1),
  ],
  "Spend blood for a legend no one can ignore.", "member_talk",
  [
    (assign, "$g_sod_nizar_charge_pending", 0),
    (assign, "$g_sod_nizar_charge_result_grade", 1),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc13", 0),
    (troop_set_slot, "trp_npc13", slot_troop_companion_warning_state, sod_companion_warning_pending),
    (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
    (display_message, "@The story will travel farther than the burial count. Nizar smiles late, as if hearing the cost arrive after the applause.", 0xCC6666),
  ]],

[anyone, "companion_depth_nizar",
  [
    (troop_slot_ge, "trp_npc13", slot_troop_companion_warning_state, sod_companion_warning_pending),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "A legend that spends everyone else first is only vanity with better horses. My faith in our legend is {s2}, though the poets are being kept outside until further notice.",
  "member_talk",
  [
    (troop_set_slot, "trp_npc13", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
  ]],

[anyone, "companion_depth_nizar",
  [
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_good),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "The charge broke them, and the living came home. A rare triumph: the song need not lie about the ending. My faith in our legend is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_nizar",
  [
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "The story will travel. So will the names of those who did not. I am discovering that applause can echo like an accusation. My faith in our legend is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_nizar",
  [
    (eq, "$g_sod_nizar_charge_pending", 1),
    (eq, "$g_sod_nizar_charge_witnessed", 1),
    (eq, "$g_sod_nizar_charge_confronted", 0),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "The field setup is drawn. Run the charge lane with me, then we decide whether the song deserves survivors. My faith in our legend is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_nizar",
  [
    (eq, "$g_sod_nizar_charge_pending", 1),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "There is a charge waiting outside camp, beautiful enough to be dangerous and dangerous enough to be memorable. First mark it in the field, then test the lane. My faith in our legend is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_nizar",
  [
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "The Impossible Charge asks its question with spurs. Is this courage, theater, or blood pretending to be both? My faith in our legend is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_nizar",
  [
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "There is a charge men call impossible because they lack imagination. There is also the other kind. I would prefer we learn the difference before dawn. My faith in our legend is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_nizar",
  [
    (troop_slot_ge, "trp_npc13", slot_troop_companion_approval, 70),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "You have the rare gift of making danger feel chosen instead of merely suffered. Try not to become too sensible; I am attached to my work. My faith in our legend is {s2}.",
  "member_talk",
  [
    (try_begin),
      (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
      (troop_set_slot, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
      (display_message, "@Nizar seems ready to speak at camp about The Impossible Charge and the difference between courage and theater.", 0x99CCFF),
    (try_end),
  ]],

[anyone, "companion_depth_nizar",
  [
    (call_script, "script_sod_companion_get_approval_band", "trp_npc13"),
    (str_store_string, s2, s0),
  ],
  "Worthy? It has moments. A charge here, a rumor there, a few silences I would edit before the poets arrive. My faith in our legend is {s2}.",
  "member_talk",
  []],
]
