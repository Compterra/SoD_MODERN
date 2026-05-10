DIALOGS = [
[anyone, "regular_member_companion_lezalit_drill",
  [],
  "Like good boots with nails inside them. The marches make sense. The ration counts make sense. The punishments make men stop thinking and start measuring where the lash will fall.",
  "regular_member_companion_lezalit_drill_choice",
  [
    (assign, "$g_sod_lezalit_ief_discipline_witnessed", 1),
    (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
    (display_message, "@A ranker weighs Lezalit's captured Imperial drill. Discipline Without Chains now has a troop witness and a trial to run.", 0x99CCFF),
  ]],

[anyone|plyr, "regular_member_companion_lezalit_drill_choice", [],
  "Tell Lezalit the line will test the drill before I decide doctrine.",
  "regular_member_companion_lezalit_drill_trial",
  []],

[anyone, "regular_member_companion_lezalit_drill_trial", [],
  "Good. Hard drill I can respect. Blind fear just teaches a man to hide his mistakes. Let the trial show which lesson the Imperial notes really carry.",
  "regular_member_talk",
  [
    (display_message, "@Lezalit's captured drill trial can now be run from camp actions.", 0x99CCFF),
  ]],
]
