DIALOGS = [
[anyone, "regular_member_companion_jeremus_wounded",
  [],
  "Seen? Men asking if enemies get bandages before friends. Camp followers holding shirts over wounds. A prisoner begging water from the same hand he tried to cut. The healer is still standing, but only because he has forgotten how to sit.",
  "regular_member_companion_jeremus_wounded_choice",
  [
    (assign, "$g_sod_jeremus_triage_witnessed", 1),
    (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
    (display_message, "@A wounded ranker gives Jeremus' triage a company witness. Hands That Will Not Harden now points toward the infirmary crisis.", 0x99CCFF),
  ]],

[anyone|plyr, "regular_member_companion_jeremus_wounded_choice", [],
  "Tell Jeremus I will face the infirmary before deciding triage.",
  "regular_member_companion_jeremus_wounded_infirmary",
  []],

[anyone, "regular_member_companion_jeremus_wounded_infirmary", [],
  "Good. The cloth is thin, tempers are thinner, and the wounded are learning whether their names matter before someone with clean boots gives an order.",
  "regular_member_talk",
  [
    (display_message, "@Jeremus' infirmary crisis can now be faced from camp actions.", 0x99CCFF),
  ]],
]
