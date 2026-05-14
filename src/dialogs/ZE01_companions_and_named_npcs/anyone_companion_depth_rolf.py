DIALOGS = [
[anyone, "companion_depth_rolf_name_pending",
  [
    (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
    (eq, "$g_sod_rolf_name_challenge_confronted", 1),
  ],
  "A crowd is a poor court, but it has asked a courtly question and then watched the public proof. What is a name worth when witnesses stop admiring it and start weighing it?",
  "companion_depth_rolf_name_choice",
  []],

[anyone, "companion_depth_rolf_name_pending",
  [
    (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
    (eq, "$g_sod_rolf_name_challenge_confronted", 0),
  ],
  "The town has weighed my name. Vulgar, yes, but not irrelevant. Stage the public proof before we decide whether the name should become service, dignity, or a smaller story.",
  "member_talk",
  []],

[anyone, "companion_depth_rolf_name_pending", [],
  "A name cannot be judged only by the person wearing it. Ask the town what it heard before we answer from a pose.",
  "member_talk",
  []],

[anyone|plyr, "companion_depth_rolf_name_choice",
  [
    (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
    (eq, "$g_sod_rolf_name_challenge_confronted", 1),
  ],
  "Answer with service, not embellishment.", "member_talk",
  [
    (assign, "$g_sod_rolf_name_challenge_pending", 0),
    (assign, "$g_sod_rolf_name_challenge_result_grade", 3),
    (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 2),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc4", 1),
    (call_script, "script_sod_companion_rolf_apply_name_payoff"),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
    (display_message, "@Rolf lets the crowd have a smaller story and the company a better man. A Name Worth Wearing remembers earned dignity.", 0x99CCFF),
  ]],

[anyone|plyr, "companion_depth_rolf_name_choice",
  [
    (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
    (eq, "$g_sod_rolf_name_challenge_confronted", 1),
  ],
  "I will defend your dignity without demanding proof.", "member_talk",
  [
    (assign, "$g_sod_rolf_name_challenge_pending", 0),
    (try_begin),
      (lt, "$g_sod_rolf_name_challenge_result_grade", 2),
      (assign, "$g_sod_rolf_name_challenge_result_grade", 2),
    (try_end),
    (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
    (call_script, "script_sod_companion_shift_approval", "trp_npc4", 3),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc4", 1),
    (call_script, "script_sod_companion_rolf_apply_name_payoff"),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
    (display_message, "@Rolf's bow is magnificent. The claim survives, but now it owes the company conduct worthy of it.", 0xCCCC66),
  ]],

[anyone|plyr, "companion_depth_rolf_name_choice",
  [
    (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
    (eq, "$g_sod_rolf_name_challenge_confronted", 1),
  ],
  "Strip away the performance in front of the company.", "member_talk",
  [
    (assign, "$g_sod_rolf_name_challenge_pending", 0),
    (assign, "$g_sod_rolf_name_challenge_result_grade", 1),
    (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc4", 0),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
    (troop_set_slot, "trp_npc4", slot_troop_companion_warning_state, sod_companion_warning_pending),
    (display_message, "@The story breaks loudly. Rolf keeps his posture, but every polished word costs him more.", 0xCC6666),
  ]],

[anyone, "companion_depth_rolf",
  [
    (troop_slot_ge, "trp_npc4", slot_troop_companion_warning_state, sod_companion_warning_pending),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc4"),
    (str_store_string_reg, s2, s0),
  ],
  "There is correction, and then there is public smallness dressed as honesty. My confidence in our grandeur is {s2}, though grandeur is presently nursing a bruise.",
  "member_talk",
  [
    (troop_set_slot, "trp_npc4", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
  ]],

[anyone, "companion_depth_rolf",
  [
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_good),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc4"),
    (str_store_string_reg, s2, s0),
  ],
  "A name earned in sight of witnesses has a sturdier ring than one shouted over objections. I knew this, naturally. My confidence in our grandeur is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_rolf",
  [
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc4"),
    (str_store_string_reg, s2, s0),
  ],
  "The claim is quieter now. Perhaps too quiet. Still, a bruised banner can be raised again if the hand holding it is not mocked for bleeding. My confidence in our grandeur is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_rolf",
  [
    (eq, "$g_sod_rolf_name_challenge_pending", 1),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc4"),
    (str_store_string_reg, s2, s0),
  ],
  "The crowd gave me applause and questions in equal measure. A vulgar exchange. Still, ask the town, stage the public proof, and then we may answer. My confidence in our grandeur is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_rolf",
  [
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc4"),
    (str_store_string_reg, s2, s0),
  ],
  "A Name Worth Wearing is more than cloth and vowels. Disappointing, perhaps, but occasionally useful. My confidence in our grandeur is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_rolf",
  [
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc4"),
    (str_store_string_reg, s2, s0),
  ],
  "There are men who inherit names, and lesser men who question them. Yet I begin to suspect a name can also be made heavier by conduct. My confidence in our grandeur is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_rolf",
  [
    (troop_slot_ge, "trp_npc4", slot_troop_companion_approval, 70),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc4"),
    (str_store_string_reg, s2, s0),
  ],
  "You understand that dignity is not an ornament. It is a weapon for keeping lesser rooms from becoming lesser men. My confidence in our grandeur is {s2}.",
  "member_talk",
  [
    (try_begin),
      (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
      (troop_set_slot, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
      (display_message, "@Rolf seems ready to speak at camp about names, dignity, and the exhausting burden of being Rolf.", 0x99CCFF),
    (try_end),
  ]],

[anyone, "companion_depth_rolf",
  [
    (call_script, "script_sod_companion_get_approval_band", "trp_npc4"),
    (str_store_string_reg, s2, s0),
  ],
  "A name of stature can endure mud, blood, and even poor tailoring. It cannot endure smallness forever. My confidence in our grandeur is {s2}.",
  "member_talk",
  []],
]
