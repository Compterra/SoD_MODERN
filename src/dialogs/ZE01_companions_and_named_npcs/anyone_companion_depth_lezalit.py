DIALOGS = [
[anyone, "companion_depth_lezalit_drill_pending",
  [
    (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
    (eq, "$g_sod_lezalit_ief_discipline_confronted", 1),
  ],
  "The soldier spoke correctly, and the trial has made the matter less theoretical. The Imperial drill contains useful order and stupid terror in the same hand. Our task is to keep the order and break the hand.",
  "companion_depth_lezalit_drill_choice",
  []],

[anyone, "companion_depth_lezalit_drill_pending",
  [
    (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
    (eq, "$g_sod_lezalit_ief_discipline_confronted", 0),
  ],
  "The soldier spoke correctly. Now run the captured drill trial before you decide doctrine from a complaint alone. Discipline must be witnessed under pressure, not merely described beside a fire.",
  "member_talk",
  []],

[anyone, "companion_depth_lezalit_drill_pending", [],
  "The Imperial notes are all punishments, marches, ration drills, and execution schedules. Fear is threaded through them, but so is useful order. Hear the line, then test the drill, and we may cut one from the other.",
  "member_talk",
  []],

[anyone|plyr, "companion_depth_lezalit_drill_choice",
  [
    (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
    (eq, "$g_sod_lezalit_ief_discipline_confronted", 1),
  ],
  "Reform the Imperial drill without chains or terror.", "member_talk",
  [
    (assign, "$g_sod_lezalit_ief_discipline_pending", 0),
    (assign, "$g_sod_lezalit_ief_discipline_result_grade", 3),
    (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_lezalit_ief_reform, 4),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc14", 1),
    (call_script, "script_sod_companion_lezalit_apply_discipline_payoff"),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
    (display_message, "@Lezalit breaks the captured Imperial drill and rebuilds it without cruelty. Ymira and Bunduk both notice.", 0x99CCFF),
  ]],

[anyone|plyr, "companion_depth_lezalit_drill_choice",
  [
    (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
    (eq, "$g_sod_lezalit_ief_discipline_confronted", 1),
  ],
  "Use fear. The line must obey before it understands.", "member_talk",
  [
    (assign, "$g_sod_lezalit_ief_discipline_pending", 0),
    (assign, "$g_sod_lezalit_ief_discipline_result_grade", 1),
    (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_lezalit_ief_harsh, 4),
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc14", 0),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
    (troop_set_slot, "trp_npc14", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
    (display_message, "@Lezalit turns victory over the Imperials into a hard discipline order. The lesson holds, but it chills the company.", 0xCCAA66),
  ]],

[anyone|plyr, "companion_depth_lezalit_drill_choice",
  [
    (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
    (eq, "$g_sod_lezalit_ief_discipline_confronted", 1),
  ],
  "Refuse the lesson. The Imperial method is poison.", "member_talk",
  [
    (assign, "$g_sod_lezalit_ief_discipline_pending", 0),
    (assign, "$g_sod_lezalit_ief_discipline_result_grade", 0),
    (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 100),
    (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
    (call_script, "script_sod_companion_shift_approval", "trp_npc14", -6),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
    (troop_set_slot, "trp_npc14", slot_troop_companion_warning_state, sod_companion_warning_pending),
    (display_message, "@Lezalit closes the captured manuals without comment. His warning waits behind the silence.", 0xCC6666),
  ]],

[anyone, "companion_depth_lezalit",
  [
    (troop_slot_ge, "trp_npc14", slot_troop_companion_warning_state, sod_companion_warning_pending),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc14"),
    (str_store_string, s2, s0),
  ],
  "Standards cannot exist only when they are pleasant. If you mean to command, command. If you mean to be liked, dismiss the army and hire flatterers. At present, my confidence is {s2}.",
  "member_talk",
  [
    (troop_set_slot, "trp_npc14", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
  ]],

[anyone, "companion_depth_lezalit",
  [
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_good),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc14"),
    (str_store_string, s2, s0),
  ],
  "The Imperial method was efficient because it was consistent, not because it was cruel. That distinction should have been obvious to me sooner. Your standards remain hard. They no longer need chains. At present, my confidence is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_lezalit",
  [
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc14"),
    (str_store_string, s2, s0),
  ],
  "The line obeys. It will march, wheel, strike, and hold. Do not confuse that with loyalty. Loyalty is slower to make and less predictable to use. At present, my confidence is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_lezalit",
  [
    (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc14"),
    (str_store_string, s2, s0),
  ],
  "The captured Imperial drill is waiting. Hear the men, run the trial, and then decide what survives. A commander who cannot separate poison from structure deserves neither mercy nor discipline. At present, my confidence is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_lezalit",
  [
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc14"),
    (str_store_string, s2, s0),
  ],
  "We are past theory. The question is whether discipline makes soldiers stronger or merely quieter. I am less certain than I was. That irritates me. At present, my confidence is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_lezalit",
  [
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc14"),
    (str_store_string, s2, s0),
  ],
  "The first lesson of command is that men will fail the standard unless the standard is made real. The second lesson, which I dislike, is that fear is not the only tool that makes it real. At present, my confidence is {s2}.",
  "member_talk",
  []],

[anyone, "companion_depth_lezalit",
  [
    (troop_slot_ge, "trp_npc14", slot_troop_companion_approval, 70),
    (call_script, "script_sod_companion_get_approval_band", "trp_npc14"),
    (str_store_string, s2, s0),
  ],
  "You do not always choose the method I would choose. Annoying. But the company still forms, marches, and survives. I am forced to respect evidence. At present, my confidence is {s2}.",
  "member_talk",
  [
    (call_script, "script_sod_companion_advance_personal_quest", "trp_npc14", 1),
  ]],

[anyone, "companion_depth_lezalit",
  [
    (call_script, "script_sod_companion_get_approval_band", "trp_npc14"),
    (str_store_string, s2, s0),
  ],
  "I see an army deciding whether it is a blade or a crowd with weapons. Discipline is not cruelty. Cruelty is what weak commanders use when discipline fails them. At present, my confidence is {s2}.",
  "member_talk",
  []],
]
