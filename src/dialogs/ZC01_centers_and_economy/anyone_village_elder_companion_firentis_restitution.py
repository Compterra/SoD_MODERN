DIALOGS = [
[anyone, "village_elder_companion_firentis_restitution",
  [
    (str_store_party_name_link, s3, "$current_town"),
  ],
  "{s3} has seen men call themselves protectors while counting what they could take. If your mailed man means repair, let him stand where people can answer him. Bread, coin, and restraint matter more when the village sees who carries them.",
  "village_elder_companion_firentis_restitution_choice",
  [
    (assign, "$g_sod_firentis_restitution_witnessed", 1),
    (quest_set_slot, "qst_companion_firentis_debt_restitution", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_firentis_debt_restitution", slot_quest_sod_runtime_last_center, "$current_town"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc6"),
    (display_message, "@A village elder gives Firentis' restitution a living witness. Debt of the Sword no longer rests only in camp.", 0x99CCFF),
  ]],

[anyone|plyr, "village_elder_companion_firentis_restitution_choice", [],
  "Leave guards, coin, and supplies. Protection is part of penance.",
  "village_elder_companion_firentis_restitution_protect",
  []],

[anyone, "village_elder_companion_firentis_restitution_protect", [],
  "Then stand by the fence when the claimants come back. Men who feed on villages love to test whether mercy brought steel with it.",
  "village_elder_talk",
  [
    (assign, "$g_sod_firentis_restitution_result_grade", 3),
    (quest_set_slot, "qst_companion_firentis_debt_restitution", slot_quest_sod_runtime_metadata, 3),
    (display_message, "@The elder names a public test for Firentis' restitution. Stand with the village before settling the debt.", 0x99CCFF),
    (jump_to_menu, "mnu_firentis_restitution_hearing"),
    (finish_mission),
  ]],

[anyone|plyr, "village_elder_companion_firentis_restitution_choice", [],
  "Let truth be spoken. Ask the village what justice can still mean.",
  "village_elder_companion_firentis_restitution_confess",
  []],

[anyone, "village_elder_companion_firentis_restitution_confess", [],
  "Truth is a harsh gift. Some will spit at it. Some will sleep easier because the wound was named instead of hidden under banners. If he will answer in public, let the village hear him before another armed man speaks over us.",
  "village_elder_talk",
  [
    (assign, "$g_sod_firentis_restitution_result_grade", 2),
    (quest_set_slot, "qst_companion_firentis_debt_restitution", slot_quest_sod_runtime_metadata, 2),
    (display_message, "@The elder asks Firentis to answer in public before restitution becomes another private comfort.", 0xCCCC66),
    (jump_to_menu, "mnu_firentis_restitution_hearing"),
    (finish_mission),
  ]],

[anyone|plyr, "village_elder_companion_firentis_restitution_choice", [],
  "Say nothing more. The village needed swords, not confession.",
  "village_elder_companion_firentis_restitution_silence",
  []],

[anyone, "village_elder_companion_firentis_restitution_silence", [],
  "Then we will take the victory and keep our own names for what it cost. Villages are practiced at swallowing words from armed men. It keeps the roofs standing, sometimes.",
  "village_elder_talk",
  [
    (assign, "$g_sod_firentis_restitution_confronted", 1),
    (assign, "$g_sod_firentis_restitution_result_grade", 1),
    (quest_set_slot, "qst_companion_firentis_debt_restitution", slot_quest_sod_runtime_progress, 75),
    (quest_set_slot, "qst_companion_firentis_debt_restitution", slot_quest_sod_runtime_metadata, 1),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_compromise, 2),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc6"),
    (display_message, "@The village is left with victory and silence. Firentis obeys, but Debt of the Sword waits for his answer.", 0xCC6666),
  ]],
]
