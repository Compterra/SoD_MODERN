DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Let's settle the matter you raised.", "companion_quest_branch_prompt",
  []],

[anyone, "companion_quest_branch_prompt",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Tell me how you want it handled.", "companion_quest_branch_choice",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (main_party_has_troop, "trp_npc1"),
    (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc1", slot_troop_companion_approval, 45),
  ],
  "Borcha, tell me about The Road Keeps Its Own.", "companion_depth_borcha",
  [
    (troop_set_slot, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (main_party_has_troop, "trp_npc1"),
    (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Trust your read. Set scouts on the hidden route.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_start_borcha_road_incident", 1),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 3),
    (str_store_string, s68, "@Borcha nods once. 'Good. We ask who saw the road first. Bleed later, if bleeding has to happen.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (main_party_has_troop, "trp_npc1"),
    (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Use the route to bait raiders for plunder.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_start_borcha_road_incident", 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc1", 1),
    (str_store_string, s68, "@Borcha snorts. 'Dirty, but not stupid. Ask at the road town. Bait has a short life if the hook is slow.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (main_party_has_troop, "trp_npc1"),
    (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Drop it. The road can wait.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_shift_approval", "trp_npc1", -4),
    (assign, "$g_sod_borcha_road_result_grade", 1),
    (troop_set_slot, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
    (str_store_string, s68, "@Borcha smooths the dirt with his boot. 'Roads wait. Knives do not.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
    (main_party_has_troop, "trp_npc2"),
    (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc2", slot_troop_companion_approval, 45),
  ],
  "Marnid, tell me about The Honest Price.", "companion_depth_marnid",
  [
    (troop_set_slot, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
    (main_party_has_troop, "trp_npc2"),
    (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Back your clean trade contacts.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_start_marnid_market_incident", 1),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 3),
    (str_store_string, s68, "@Marnid marks three names and crosses out two. 'Good. Now we ask the market which names are missing.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
    (main_party_has_troop, "trp_npc2"),
    (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Use the contacts for dirtier prisoner profit.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_start_marnid_market_incident", 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_dirty_profit, 2),
    (str_store_string, s68, "@Marnid closes the ledger slowly. 'Profitable, yes. But some accounts charge interest in sleep. We ask the market before it collects.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (main_party_has_troop, "trp_npc3"),
    (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc3", slot_troop_companion_approval, 45),
  ],
  "Ymira, tell me about Mercy Under Arms.", "companion_depth_ymira",
  [
    (troop_set_slot, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc3"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (main_party_has_troop, "trp_npc3"),
    (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "The helpless will be protected.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_ymira_refugee_incident", 3),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_free_captives, 3),
    (str_store_string, s68, "@Ymira lets out a breath she had been holding. 'Then mercy has a place in this company, not just a corner where it hides.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (main_party_has_troop, "trp_npc3"),
    (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Mercy still answers to ransom and supply.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_ymira_refugee_incident", 3),
    (call_script, "script_sod_companion_shift_approval", "trp_npc3", -2),
    (str_store_string, s68, "@Ymira nods, but not happily. 'I know supplies matter. I only fear the day every person becomes a line in the stores.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (main_party_has_troop, "trp_npc3"),
    (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Not every wound can be my concern.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_shift_approval", "trp_npc3", -5),
    (assign, "$g_sod_ymira_refugee_result_grade", 1),
    (troop_set_slot, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc3"),
    (str_store_string, s68, "@Ymira looks back to the dark beyond camp. 'No. Only the ones we choose not to see.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (main_party_has_troop, "trp_npc4"),
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc4", slot_troop_companion_approval, 45),
  ],
  "Rolf, tell me about A Name Worth Wearing.", "companion_depth_rolf",
  [
    (troop_set_slot, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (main_party_has_troop, "trp_npc4"),
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "A name is proven by conduct.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_rolf_name_challenge_incident", 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
    (str_store_string, s68, "@Rolf begins to object, then smiles. 'Naturally. A great name improves the deeds beneath it.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (main_party_has_troop, "trp_npc4"),
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "I will defend your dignity in public.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_rolf_name_challenge_incident", 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc4", 3),
    (str_store_string, s68, "@Rolf's bow is magnificent. 'At last, someone here understands lineage as a civic necessity.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (main_party_has_troop, "trp_npc4"),
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Drop the performance.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_rolf_name_challenge_incident", 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc4", -5),
    (str_store_string, s68, "@Rolf's smile stays in place a moment too long. 'How brave, to strip a cloak and call the shivering man honest.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (main_party_has_troop, "trp_npc5"),
    (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc5", slot_troop_companion_approval, 45),
  ],
  "Baheshtur, tell me about The Unbroken Saddle.", "companion_depth_baheshtur",
  [
    (troop_set_slot, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (main_party_has_troop, "trp_npc5"),
    (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Ride hard before the rival gathers strength.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_baheshtur_saddle_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
    (str_store_string, s68, "@Baheshtur's nod is small and fierce. 'Good. Let him learn that open ground does not belong only to raiders.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (main_party_has_troop, "trp_npc5"),
    (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Free riders may swear, but only freely.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_baheshtur_saddle_incident", 1, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc5", 4),
    (str_store_string, s68, "@Baheshtur watches you carefully. 'An oath taken by a free man has weight. Anything else is rope.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (main_party_has_troop, "trp_npc5"),
    (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Buy peace and let the insult pass.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_baheshtur_saddle_incident", 2, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_black_khergit_tribute, 1),
    (str_store_string, s68, "@Baheshtur looks toward the horse lines. 'A paid wolf is still a wolf. He only learns your purse has meat in it.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (main_party_has_troop, "trp_npc6"),
    (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc6", slot_troop_companion_approval, 45),
  ],
  "Firentis, tell me about Debt of the Sword.", "companion_depth_firentis",
  [
    (troop_set_slot, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc6"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (main_party_has_troop, "trp_npc6"),
    (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Make restitution.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_firentis_restitution_incident", 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 2),
    (str_store_string, s68, "@Firentis bows his head. 'Restitution will not make the dead answer. It may still keep the living from joining them.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (main_party_has_troop, "trp_npc6"),
    (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Confess publicly and accept judgment.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_firentis_restitution_incident", 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc6", 2),
    (str_store_string, s68, "@Firentis looks afraid, then relieved by the fear. 'Then let truth do what steel cannot.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (main_party_has_troop, "trp_npc6"),
    (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Bury the past to preserve the company.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_firentis_restitution_incident", 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc6", -4),
    (str_store_string, s68, "@Firentis sheathes the blade carefully. 'A buried thing is not absolved. It is only waiting.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (main_party_has_troop, "trp_npc12"),
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc12", slot_troop_companion_approval, 45),
  ],
  "Jeremus, tell me about Hands That Will Not Harden.", "companion_depth_jeremus",
  [
    (troop_set_slot, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (main_party_has_troop, "trp_npc12"),
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Civilians and helpless wounded come first.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_jeremus_triage_incident", 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_free_captives, 3),
    (str_store_string, s68, "@Jeremus closes his eyes for a moment. 'Then we will still be an army, but not only an army.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (main_party_has_troop, "trp_npc12"),
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Use hard triage. Save who can still be saved.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_jeremus_triage_incident", 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc12", 1),
    (str_store_string, s68, "@Jeremus nods sadly. 'Cruel arithmetic, but not cruelty. I can work with that difference.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (main_party_has_troop, "trp_npc12"),
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Our soldiers come before all others.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_jeremus_triage_incident", 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc12", -4),
    (str_store_string, s68, "@Jeremus folds the clean cloth with care. 'Then I pray our banner never becomes the measure of a life.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (main_party_has_troop, "trp_npc10"),
    (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc10", slot_troop_companion_approval, 45),
  ],
  "Bunduk, tell me about The Men Who Hold the Line.", "companion_depth_bunduk",
  [
    (troop_set_slot, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc10"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (main_party_has_troop, "trp_npc10"),
    (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Speak for the common soldiers.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_bunduk_line_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 2),
    (str_store_string, s68, "@Bunduk nods. 'Good. They do not need soft words. They need boots, bolts, pay, and orders that are not stupid.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (main_party_has_troop, "trp_npc10"),
    (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Back fair stores and watches.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_bunduk_line_incident", 2, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 2),
    (str_store_string, s68, "@Bunduk gives a short laugh. 'Amazing thing, feeding men before asking them to die. Should write a book.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (main_party_has_troop, "trp_npc10"),
    (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "The line needs harsher discipline.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_bunduk_line_incident", 1, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc10", -5),
    (str_store_string, s68, "@Bunduk's face hardens. 'Aye. I have heard officers say that just before blaming dead men for obeying.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (main_party_has_troop, "trp_npc11"),
    (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc11", slot_troop_companion_approval, 45),
  ],
  "Katrin, tell me about The Last Coin in Camp.", "companion_depth_katrin",
  [
    (troop_set_slot, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (main_party_has_troop, "trp_npc11"),
    (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Spend it on stores, wages, and medicine.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_katrin_last_coin_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 3),
    (str_store_string, s68, "@Katrin sniffs. 'Sensible. Dangerous habit, that. Keep it up and the camp may start expecting to live.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (main_party_has_troop, "trp_npc11"),
    (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Stretch the stores to feed refugees too.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_katrin_last_coin_incident", 2, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 2),
    (str_store_string, s68, "@Katrin begins counting portions under her breath. 'Mercy with arithmetic. Harder than speeches, better for everyone.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (main_party_has_troop, "trp_npc11"),
    (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Spend it on the bold opportunity.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_katrin_last_coin_incident", 2, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc11", -5),
    (str_store_string, s68, "@Katrin folds her arms. 'Of course. A hungry man loves hearing he is part of history.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
    (main_party_has_troop, "trp_npc8"),
    (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc8", slot_troop_companion_approval, 45),
  ],
  "Matheld, tell me about No Backward Step.", "companion_depth_matheld",
  [
    (troop_set_slot, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
    (main_party_has_troop, "trp_npc8"),
    (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Stand firm and answer the threat.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_matheld_no_backward_step_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
    (str_store_string, s68, "@Matheld bares her teeth. 'Good. Let them see the shield before they feel it.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
    (main_party_has_troop, "trp_npc8"),
    (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Save lives without turning away.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_matheld_no_backward_step_incident", 1, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc8", 2),
    (str_store_string, s68, "@Matheld grunts. 'Planning is not cowardice if the shield still faces forward.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
    (main_party_has_troop, "trp_npc8"),
    (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Yield ground and avoid the challenge.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_matheld_no_backward_step_incident", 2, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_cowardice, 2),
    (str_store_string, s68, "@Matheld's voice drops. 'Every backward step teaches someone to chase.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (main_party_has_troop, "trp_npc9"),
    (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc9", slot_troop_companion_approval, 45),
  ],
  "Alayen, tell me about The Standard and the Self.", "companion_depth_alayen",
  [
    (troop_set_slot, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (main_party_has_troop, "trp_npc9"),
    (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Honor means duty beneath the banner.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_alayen_standard_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 2),
    (str_store_string, s68, "@Alayen inclines his head. 'Then nobility is not a height. It is a weight. Good.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (main_party_has_troop, "trp_npc9"),
    (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Keep the oath, even at real cost.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_alayen_standard_incident", 1, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc9", 4),
    (str_store_string, s68, "@Alayen's expression steadies. 'Cost is where oath becomes more than speech.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (main_party_has_troop, "trp_npc9"),
    (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Use the standard for prestige and obedience.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_alayen_standard_incident", 2, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc9", -4),
    (str_store_string, s68, "@Alayen goes very still. 'A banner used as ornament soon becomes a rag.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (main_party_has_troop, "trp_npc13"),
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc13", slot_troop_companion_approval, 45),
  ],
  "Nizar, tell me about The Impossible Charge.", "companion_depth_nizar",
  [
    (troop_set_slot, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (main_party_has_troop, "trp_npc13"),
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Take the daring rescue now.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_nizar_charge_incident", 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
    (str_store_string, s68, "@Nizar springs up smiling. 'At last, a decision with a pulse. I shall try not to improve it too much when I retell it.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (main_party_has_troop, "trp_npc13"),
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Plan the way out first.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_nizar_charge_incident", 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc13", 2),
    (str_store_string, s68, "@Nizar makes a face, then laughs. 'A cautious legend. Disgraceful. Useful. Possibly immortal.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (main_party_has_troop, "trp_npc13"),
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Refuse the charge as needless theater.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_nizar_charge_incident", 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_cowardice, 1),
    (str_store_string, s68, "@Nizar bows too deeply. 'Of course. We shall leave the impossible to poorer poets.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (main_party_has_troop, "trp_npc14"),
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc14", slot_troop_companion_approval, 45),
  ],
  "Lezalit, tell me about Discipline Without Chains.", "companion_depth_lezalit",
  [
    (troop_set_slot, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (main_party_has_troop, "trp_npc14"),
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Reform the drills without softening standards.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_lezalit_ief_discipline_incident", "trp_kingdom_6_lord"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 3),
    (str_store_string, s68, "@Lezalit studies you for a long moment. 'Good. Mercy that preserves standards is not weakness. It is efficiency with a conscience.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (main_party_has_troop, "trp_npc14"),
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Use harsh punishment to restore order.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_lezalit_ief_discipline_incident", "trp_kingdom_6_lord"),
    (call_script, "script_sod_companion_shift_approval", "trp_npc14", 2),
    (str_store_string, s68, "@Lezalit nods once. 'The line will hold. Whether it learns why is another matter.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (main_party_has_troop, "trp_npc14"),
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "The men need less discipline, not more.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_shift_approval", "trp_npc14", -5),
    (assign, "$g_sod_lezalit_ief_discipline_result_grade", 1),
    (troop_set_slot, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
    (str_store_string, s68, "@Lezalit's expression closes like a gate. 'Then pray sentiment can hold a shield wall.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (main_party_has_troop, "trp_npc15"),
    (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc15", slot_troop_companion_approval, 45),
  ],
  "Artimenner, tell me about The Siege That Should Have Worked.", "companion_depth_artimenner",
  [
    (troop_set_slot, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (main_party_has_troop, "trp_npc15"),
    (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Take the time and materials to do it properly.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_artimenner_siege_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 2),
    (str_store_string, s68, "@Artimenner blinks, as if bracing for argument that never comes. 'Good. Remarkable. We may yet defeat gravity and stupidity in the same week.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (main_party_has_troop, "trp_npc15"),
    (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Improvise with what the army has.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_artimenner_siege_incident", 1, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc15", 2),
    (str_store_string, s68, "@Artimenner pinches the bridge of his nose. 'Inferior, but possible. I prefer possible to glorious nonsense.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (main_party_has_troop, "trp_npc15"),
    (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "If the works fail, the blame is yours.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_artimenner_siege_incident", 2, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc15", -6),
    (str_store_string, s68, "@Artimenner's voice goes flat. 'Ah. So I am not an engineer. I am a bucket for falling stones.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (main_party_has_troop, "trp_npc7"),
    (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc7", slot_troop_companion_approval, 45),
  ],
  "Deshavi, tell me about Tracks Through Ash.", "companion_depth_deshavi",
  [
    (troop_set_slot, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (main_party_has_troop, "trp_npc7"),
    (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Follow the trail to rescue survivors.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_deshavi_trail_warning_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 3),
    (str_store_string, s68, "@Deshavi nods without smiling. 'Good. Poor folk leave signs because rich men do not leave help.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (main_party_has_troop, "trp_npc7"),
    (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Use the trail to ambush the raiders.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_deshavi_trail_warning_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 2),
    (str_store_string, s68, "@Deshavi checks her bowstring. 'Better to find wolves before they find doors.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (main_party_has_troop, "trp_npc7"),
    (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "The company cannot chase every burned trail.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_shift_approval", "trp_npc7", -5),
    (assign, "$g_sod_deshavi_trail_result_grade", 1),
    (troop_set_slot, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_resolved_hard),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
    (str_store_string, s68, "@Deshavi gathers the twigs back into her palm. 'No. Only the trails poor enough to be quiet.'"),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (main_party_has_troop, "trp_npc16"),
    (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
    (troop_slot_ge, "trp_npc16", slot_troop_companion_approval, 45),
  ],
  "Klethi, tell me about A Knife With a Name.", "companion_depth_klethi",
  [
    (troop_set_slot, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc16"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (main_party_has_troop, "trp_npc16"),
    (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "I will protect you from the old accusation.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_klethi_old_job_incident", 1, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_stealth_success, 3),
    (str_store_string, s68, "@Klethi's smile almost reaches her eyes. 'Careful. Protecting thieves is how honest people learn useful habits.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (main_party_has_troop, "trp_npc16"),
    (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Face the damage, but on your terms.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_klethi_old_job_incident", 1, 2),
    (call_script, "script_sod_companion_shift_approval", "trp_npc16", 2),
    (str_store_string, s68, "@Klethi pockets the knife. 'My terms, then. That is the part people forget when they say justice.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (main_party_has_troop, "trp_npc16"),
    (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Trade the old secret for leverage.", "companion_quest_branch_reply",
  [
    (call_script, "script_sod_companion_try_klethi_old_job_incident", 2, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_betray_autonomy, 2),
    (str_store_string, s68, "@Klethi laughs once. Small sound. No warmth. 'There it is. Belonging with a price tag.'"),
  ]],

[anyone|plyr, "companion_quest_branch_choice",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (troop_slot_eq, "$g_talk_troop", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
  ],
  "Not yet.", "member_talk",
  []],

[anyone, "companion_quest_branch_reply", [], "{s68}", "member_talk", []],
]
