DIALOGS = [
[anyone, "companion_depth_jeremus_triage_pending",
  [
    (eq, "$g_sod_jeremus_triage_witnessed", 1),
    (eq, "$g_sod_jeremus_triage_confronted", 1),
  ],
  "You heard the wounded and saw the infirmary under pressure. Now choose the rule I follow when blood outruns clean cloth.",
  "companion_depth_jeremus_triage_choice",
  []],

[anyone, "companion_depth_jeremus_triage_pending",
  [
    (eq, "$g_sod_jeremus_triage_witnessed", 1),
    (eq, "$g_sod_jeremus_triage_confronted", 0),
  ],
  "The wounded have spoken, but the infirmary is still only held together by tired hands and hope. Face that crisis with me before you turn one frightened report into doctrine.",
  "companion_depth_jeremus_infirmary_choice",
  []],

[anyone, "companion_depth_jeremus_triage_pending", [],
  "Then look at them before you answer. Company men, enemies, frightened camp followers, people whose names no report will carry. There are too many wounded and too little time.",
  "member_talk",
  []],

[anyone|plyr, "companion_depth_jeremus_infirmary_choice",
  [
    (main_party_has_troop, "trp_npc12"),
    (eq, "$g_sod_jeremus_triage_pending", 1),
    (eq, "$g_sod_jeremus_triage_witnessed", 1),
    (eq, "$g_sod_jeremus_triage_confronted", 0),
  ],
  "Face the infirmary now.", "close_window",
  [
    (jump_to_menu, "mnu_jeremus_triage_infirmary"),
    (finish_mission),
  ]],

[anyone|plyr, "companion_depth_jeremus_infirmary_choice",
  [
    (main_party_has_troop, "trp_npc12"),
  ],
  "Not yet.", "member_talk", []],

[anyone|plyr, "companion_depth_jeremus_triage_choice",
  [
    (main_party_has_troop, "trp_npc12"),
    (eq, "$g_sod_jeremus_triage_witnessed", 1),
    (eq, "$g_sod_jeremus_triage_confronted", 1),
  ],
  "Treat the helpless and enemy wounded by need, not banner.", "member_talk",
  [
    (assign, "$g_sod_jeremus_triage_pending", 0),
    (assign, "$g_sod_jeremus_triage_result_grade", 3),
    (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_free_captives, 3),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc12", 3),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc12", 1),
    (call_script, "script_sod_companion_jeremus_apply_triage_payoff"),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
    (display_message, "@The wounded are sorted without rank deciding who deserves breath. Jeremus looks exhausted, but not defeated.", 0x99CCFF),
  ]],

[anyone|plyr, "companion_depth_jeremus_triage_choice",
  [
    (main_party_has_troop, "trp_npc12"),
    (eq, "$g_sod_jeremus_triage_witnessed", 1),
    (eq, "$g_sod_jeremus_triage_confronted", 1),
  ],
  "Use hard triage. Save those most likely to survive.", "member_talk",
  [
    (assign, "$g_sod_jeremus_triage_pending", 0),
    (try_begin),
      (lt, "$g_sod_jeremus_triage_result_grade", 2),
      (assign, "$g_sod_jeremus_triage_result_grade", 2),
    (try_end),
    (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
    (call_script, "script_sod_companion_shift_approval", "trp_npc12", 1),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc12", 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
    (display_message, "@Jeremus accepts the cruel arithmetic because it is not cruelty. The living are pulled back from the edge.", 0xCCCC66),
  ]],

[anyone|plyr, "companion_depth_jeremus_triage_choice",
  [
    (main_party_has_troop, "trp_npc12"),
    (eq, "$g_sod_jeremus_triage_witnessed", 1),
    (eq, "$g_sod_jeremus_triage_confronted", 1),
  ],
  "Save company strength first. Others wait.", "member_talk",
  [
    (assign, "$g_sod_jeremus_triage_pending", 0),
    (assign, "$g_sod_jeremus_triage_result_grade", 1),
    (call_script, "script_sod_companion_shift_approval", "trp_npc12", -4),
    (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc12", 0),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
    (troop_set_slot, "trp_npc12", slot_troop_companion_warning_state, sod_companion_warning_pending),
    (display_message, "@The company recovers faster. Jeremus does not argue with the result. He only asks who will heal what the result did to you.", 0xCC6666),
  ]],

[anyone, "companion_depth_jeremus",
  [
    (troop_slot_ge, "trp_npc12", slot_troop_companion_warning_state, sod_companion_warning_pending),
    (neg|troop_slot_ge, "trp_npc12", slot_troop_companion_warning_state, sod_companion_warning_redeemed),
    (call_script, "script_sod_companion_get_approval_band_to_s68", "trp_npc12"),
    (str_store_string_reg, s2, s68),
  ],
  "I can bind wounds made by steel. I do not know how to bind the habit of deciding some lives are easier to leave behind. My faith in this company is {s2}.",
  "member_talk",
  [
    (troop_set_slot, "trp_npc12", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
  ]],

[anyone, "companion_depth_jeremus",
  [
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_good),
    (call_script, "script_sod_companion_get_approval_band_to_s68", "trp_npc12"),
    (str_store_string_reg, s2, s68),
  ],
  "We did not save everyone. We never do. But rank and usefulness did not decide who deserved breath. My faith in this company is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_jeremus",
  [
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
    (call_script, "script_sod_companion_get_approval_band_to_s68", "trp_npc12"),
    (str_store_string_reg, s2, s68),
  ],
  "The company recovered. That matters. So do the people left waiting. My faith in this company is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_jeremus",
  [
    (eq, "$g_sod_jeremus_triage_pending", 1),
    (call_script, "script_sod_companion_get_approval_band_to_s68", "trp_npc12"),
    (str_store_string_reg, s2, s68),
  ],
  "There are too many wounded and too little time. Hear them, face the infirmary crisis, then choose what guides my hands. My faith in this company is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_jeremus",
  [
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    (call_script, "script_sod_companion_get_approval_band_to_s68", "trp_npc12"),
    (str_store_string_reg, s2, s68),
  ],
  "I used to think hard choices changed a healer into something else. Now I fear refusing to choose can do the same. My faith in this company is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_jeremus",
  [
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_get_approval_band_to_s68", "trp_npc12"),
    (str_store_string_reg, s2, s68),
  ],
  "There will be a day when we have too many wounded and too little time. I fear what that day will teach us. My faith in this company is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_jeremus",
  [
    (troop_slot_ge, "trp_npc12", slot_troop_companion_approval, 70),
    (call_script, "script_sod_companion_get_approval_band_to_s68", "trp_npc12"),
    (str_store_string_reg, s2, s68),
  ],
  "You still look for another way before ordering blood. That is not softness. It is discipline of another kind. My faith in this company is {s2}.",
  "member_talk",
  [
    (try_begin),
      (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
      (troop_set_slot, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
      (display_message, "@Jeremus seems ready to speak at camp about a day when there may not be enough hands to save everyone.", 0x99CCFF),
    (try_end),
  ]],

[anyone, "companion_depth_jeremus",
  [
    (call_script, "script_sod_companion_get_approval_band_to_s68", "trp_npc12"),
    (str_store_string_reg, s2, s68),
  ],
  "The wounded mend slowly, honestly, and never as cleanly as reports suggest. My faith in this company is {s2}.",
  "member_talk",
  []],
]
