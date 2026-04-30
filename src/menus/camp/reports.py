try:
    from header_common import *  # noqa: F401,F403
    from header_operations import *  # noqa: F401,F403
except ImportError:
    pass

for _name in (
    "mnf_enable_hot_keys",
    "set_background_mesh",
    "store_add",
    "str_store_string",
    "store_current_day",
    "store_and",
    "str_store_faction_name",
    "assign",
    "call_script",
    "jump_to_menu",
    "change_screen_return",
    "start_presentation",
    "party_get_morale",
    "quest_get_slot",
    "quest_set_slot",
    "quest_slot_ge",
    "troop_get_slot",
    "check_quest_active",
    "check_quest_succeeded",
    "check_quest_failed",
    "gt",
    "ge",
    "eq",
    "le",
    "val_add",
    "val_or",
    "try_begin",
    "else_try",
    "try_end",
    "try_for_range",
    "this_or_next",
    "faction_slot_eq",
    "reg0",
    "reg1",
    "reg5",
    "reg6",
    "reg7",
    "reg8",
    "reg9",
    "s1",
    "s2",
    "s3",
    "s4",
    "s5",
    "s6",
    "s7",
    "s8",
    "s9",
    "p_main_party",
    "all_quests_begin",
    "all_quests_end",
    "slot_faction_leader",
    "slot_troop_renown",
    "slot_quest_sod_runtime_state",
    "slot_quest_sod_journal_flags",
    "slot_quest_sod_runtime_stage",
    "slot_quest_sod_journal_chain_progress",
    "slot_quest_expiration_days",
    "slot_quest_sod_runtime_last_day",
    "slot_quest_sod_journal_stage_progress",
    "slot_quest_sod_journal_category",
    "slot_quest_sod_journal_archive_day",
    "sod_quest_state_active",
    "sod_quest_state_completed",
    "sod_quest_state_failed",
    "sod_quest_journal_capacity_default",
    "sod_quest_journal_flag_pinned",
    "sod_quest_journal_flag_main",
    "sod_quest_journal_flag_urgent",
    "sod_quest_journal_flag_side",
    "sod_quest_journal_category_urgent",
    "sod_quest_journal_category_completed",
    "sod_quest_journal_category_failed",
):
    if _name not in globals():
        globals()[_name] = 0

MENUS = [
("reports", mnf_enable_hot_keys,
    "{playername} {s2}^Formerly of the {s1}^^{s3}^Honor: {reg6}^Renown: {reg5}^^Party Morale: {reg8}^Party Size Limit: {reg7}^^You've been in Calradia for a total of {reg9} days.",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      # get the name of their homeland faction
      (store_add, reg0, "str_sod_homeland_0", "$g_sod_country"),
      (str_store_string, s1, reg0),

      # add a suffix for what their faith is
      (store_add, reg0, "str_sod_faith_suffix_0", "$g_sod_faith"),
      (str_store_string, s2, reg0),

      # generate their full title (mercenary, vassal, king...)
      (try_begin),
        (gt, "$players_kingdom", 0),
        (str_store_faction_name, s8, "$players_kingdom"),
        (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
          (str_store_string, s2, "@{s2}^Ruler of the {s8}"),
        (else_try),
          (eq, "$player_has_homage", 1),
          (str_store_string, s2, "@{s2}^vassal of the {s8}"),
        (else_try),
          (str_store_string, s2, "@{s2}^mercenary for the {s8}"),
        (try_end),
      (try_end),

      # add an indication of their faith level
      (store_add, reg0, "str_sod_faith_level_0", "$g_sod_faith"),
      (assign, reg1, "$g_sod_global_faith"),
      (str_store_string, s3, reg0),

      # fill in the rest of our string info
      (call_script, "script_game_get_party_companion_limit"),
      (assign, ":party_size_limit", reg0),
      (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
      (assign, reg5, ":renown"),
      (assign, reg6, "$player_honor"),
      (assign, reg7, ":party_size_limit"),
      (party_get_morale, reg8, "p_main_party"),
      (store_current_day, reg9),
    ],
    [
	  ("view_sod_description", [], "Learn about Sword of Damocles.", [(assign, "$sod_description_page", 1),(change_screen_return),(start_presentation, "prsnt_sod_description"),]),
	  
      ("view_game_options", [], "Sword of Damocles - Options.", [(jump_to_menu, "mnu_game_options")]),
	  
      ("view_character_report", [], "View character report.", [(jump_to_menu, "mnu_character_report")]),

      ("view_mercenary_status_report", [], "View mercenary status report.", [(jump_to_menu, "mnu_mercenary_status_report")]),

      ("view_party_size_report", [], "View party size report.", [(jump_to_menu, "mnu_party_size_report")]),

      ("view_morale_report", [], "View party morale report.", [(jump_to_menu, "mnu_morale_report")]),

      ("view_companion_company_report", [], "View companion company report.", [(jump_to_menu, "mnu_companion_company_report")]),

      ("view_quest_journal_report", [], "View quest journal.", [(jump_to_menu, "mnu_quest_journal_report")]),

      ("view_elite_doctrine_report", [], "Review elite troop doctrines.", [(jump_to_menu, "mnu_elite_doctrine_report")]),

      ("view_realm_law_report", [], "Review realm laws and foreign edicts.", [(jump_to_menu, "mnu_realm_law_report")]),

      ("view_invasion_status_report", [], "Review Imperial invasion status.", [(jump_to_menu, "mnu_invasion_status_report")]),

      ("view_regional_threat_board", [], "View regional threat board.",
        [
          (call_script, "script_get_closest_center", "p_main_party"),
          (assign, "$g_sod_threat_board_context_center", reg0),
          (assign, "$g_sod_threat_board_return_menu", "mnu_reports"),
          (jump_to_menu, "mnu_regional_threat_board"),
        ]),

      ("view_royal_reliquary_report", [(eq, "$g_sod_king", 1)], "View royal reliquary report.", [(jump_to_menu, "mnu_royal_reliquary_report")]),
	  
      ("view_guild_relations_report", [], "View guild relations report.", [(jump_to_menu, "mnu_guilds_relations_report")]),

      ("view_faction_relations_report", [], "View faction relations report.", [(jump_to_menu, "mnu_faction_relations_report")]),

	  ("view_weekly_law_bonuses_report", [(eq, "$g_sod_king", 1)], "View weekly law bonuses report.", [(jump_to_menu, "mnu_weekly_bonuses_report")]),
	  
      ("view_lord_reports", [(gt, "$players_kingdom", 0)], "View lord reports...", [(jump_to_menu, "mnu_lord_reports")]),
     
      ("view_fief_reports", [(call_script, "script_get_number_of_hero_centers", "trp_player"), (gt, reg0, 0)], "View fief reports...", [(jump_to_menu, "mnu_fief_reports")]),

      ("resume_travelling", [], "Resume travelling.", [(change_screen_return)]),
    ]
  ),
]
