from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *
from header_game_menus import *
from header_parties import *
from header_items import *
from header_terrain_types import *

####################################################################################################################
#   Each mission-template is a tuple that contains the following fields:
#  1) Mission-template id (string): used for referencing mission-templates in other files.
#     The prefix mt_ is automatically added before each mission-template id
#
#  2) Mission-template flags (int): See header_mission-templates.py for a list of available flags
#  3) Mission-type(int): Which mission types this mission template matches.
#     For mission-types to be used with the default party-meeting system,
#     this should be 'charge' or 'charge_with_ally' otherwise must be -1.
#
#  4) Mission description text (string).
#  5) List of spawn records (list): Each spawn record is a tuple that contains the following fields:
#    5.1) entry-no: Troops spawned from this spawn record will use this entry
#    5.2) spawn flags.
#    5.3) alter flags. which equipment will be overriden
#    5.4) ai flags.
#    5.5) Number of troops to spawn.
#    5.6) list of equipment to add to troops spawned from here (maximum 8).
#  6) List of triggers (list).
#     See module_triggers.py for infomation about triggers.
#
#  Please note that mission templates is work in progress and can be changed in the future versions.
#
####################################################################################################################

pilgrim_disguise = [itm_pilgrim_hood, itm_pilgrim_disguise, itm_practice_staff, itm_throwing_daggers]
af_castle_lord = af_override_horse | af_override_weapons| af_require_civilian


common_battle_mission_start = (
  ti_before_mission_start, 0, 0, [],
  [
    (team_set_relation, 0, 2, 1),
    (team_set_relation, 1, 3, 1),
    (call_script, "script_change_banners_and_chest"),
    (call_script, "script_sod_battle_initialize_morale_context"),
    (call_script, "script_sod_company_dialogue_process_battle_start_morale"),
    ])
	
common_battle_horse_health = (
  0, 0, ti_once, [],
  [
    (start_presentation, "prsnt_horse_health"),
    ])

sod_battle_commander_spawn_player_ally = (
  0, 0, ti_once, [],
  [
    (call_script, "script_sod_battle_commander_spawn_player_ally", 0),
    ])

sod_battle_commander_spawn_player_ally_dismounted = (
  0, 0, ti_once, [],
  [
    (call_script, "script_sod_battle_commander_spawn_player_ally", 1),
    ])

common_battle_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (call_script, "script_sod_post_defeat_count_casualties_once"),
      (call_script, "script_sod_post_defeat_clear"),
      (finish_mission, 0),
    (else_try),
#SoD begin
      (eq, "$pin_player_fallen", 1),
      (question_box, "str_do_you_want_to_retreat"),
    (else_try),
#SOD end
      (call_script, "script_cf_check_enemies_nearby"),
      (question_box, "str_do_you_want_to_retreat"),
    (else_try),
      (display_message, "str_can_not_retreat", red),
    (try_end),
    ])

common_arena_fight_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (question_box, "str_give_up_fight"),
    ])

common_custom_battle_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (try_begin),
      (neq, "$g_battle_result", 0),
      (call_script, "script_sod_post_defeat_clear"),
      (call_script, "script_custom_battle_end"),
      (finish_mission),
    (else_try),
      (question_box, "str_give_up_fight"),
    (try_end),
    ])

custom_battle_check_victory_condition = (
  1, 60, ti_once,
  [
    (store_mission_timer_a, reg(1)),
    (ge, reg(1), 10),
    (all_enemies_defeated, 2),
#    (neg|main_hero_fallen, 0),
    (set_mission_result, 1),
    (display_message, "str_msg_battle_won", bright_green),
    (assign, "$battle_won", 1),
    (assign, "$g_battle_result", 1),
    ],
  [
    (call_script, "script_sod_post_defeat_record_aftermath", 1),
    (call_script, "script_sod_post_defeat_clear"),
    (call_script, "script_custom_battle_end"),
    (finish_mission, 1),
    ])

custom_battle_check_defeat_condition = (
  1, 4, ti_once,
  [
    (store_mission_timer_a, reg(1)),
    (ge, reg(1), 10),
    (num_active_teams_le, 1),
    (neg|all_enemies_defeated, 2),
    (assign, "$g_battle_result", -1),
    ],
  [
    (call_script, "script_sod_post_defeat_record_aftermath", -1),
    (call_script, "script_sod_post_defeat_clear"),
    (call_script, "script_custom_battle_end"),
    (finish_mission),
    ])

common_battle_victory_display = (
  10, 0, 0, [],
  [
    (eq, "$battle_won", 1),
    (display_message, "str_msg_battle_won", bright_green),
    ])

common_siege_question_answered = (
  ti_question_answered, 0, 0, [],
   [
     (store_trigger_param_1, ":answer"),
     (eq, ":answer", 0),
     (assign, "$pin_player_fallen", 0),
     (get_player_agent_no, ":player_agent"),
     (agent_get_team, ":agent_team", ":player_agent"),
     (try_begin),
       (neq, "$attacker_team", ":agent_team"),
       (neq, "$attacker_team_2", ":agent_team"),
       (str_store_string, s5, "str_siege_continues"),
       (call_script, "script_simulate_retreat", 8, 15),
     (else_try),
       (str_store_string, s5, "str_retreat"),
       (call_script, "script_simulate_retreat", 5, 20),
     (try_end),
     (call_script, "script_sod_post_defeat_count_casualties_once"),
     (call_script, "script_sod_post_defeat_clear"),
     (finish_mission, 0),
     ])

common_custom_battle_question_answered = (
   ti_question_answered, 0, 0, [],
   [
     (store_trigger_param_1, ":answer"),
     (eq, ":answer", 0),
     (assign, "$g_battle_result", -1),
     (call_script, "script_sod_post_defeat_clear"),
     (call_script, "script_custom_battle_end"),
     (finish_mission),
     ])

common_custom_siege_init = (
  0, 0, ti_once, [],
  [
    (assign, "$g_battle_result", 0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    ])

common_siege_init = (
  0, 0, ti_once, [],
  [
    (assign, "$battle_won", 0),
    (assign, "$defender_reinforcement_stage", 0),
    (assign, "$attacker_reinforcement_stage", 0),
    (assign, "$g_presentation_battle_active", 0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    ])

common_music_situation_update = (
  30, 0, 0, [],
  [
    (call_script, "script_combat_music_set_situation_with_culture"),
    ])

quest_battle_mission_start = (
  ti_before_mission_start, 0, 0, [],
  [
    (call_script, "script_sod_quest_battle_mission_start"),
    ])

quest_battle_agent_defeated = (
  1, 0, 0, [],
  [
    (call_script, "script_sod_quest_battle_scan_agents"),
    ])

quest_battle_tick = (
  2, 0, 0, [],
  [
    (call_script, "script_sod_quest_battle_tick"),
    ])

common_siege_ai_trigger_init = (
  0, 0, ti_once,
  [
    (assign, "$defender_team", 0),
    (assign, "$attacker_team", 1),
    (assign, "$defender_team_2", 2),
    (assign, "$attacker_team_2", 3),
    ], [])

common_siege_ai_trigger_init_2 = (
  0, 0, ti_once,
  [
    (set_show_messages, 0),
    (entry_point_get_position, pos10, 10),
    (team_give_order, "$defender_team", grc_infantry, mordr_hold),
    (team_give_order, "$defender_team", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team", grc_everyone, pos10),
    (team_give_order, "$defender_team_2", grc_infantry, mordr_hold),
    (team_give_order, "$defender_team_2", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team_2", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team_2", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team_2", grc_everyone, pos10),
    (set_show_messages, 1),
    ], [])

common_siege_ai_trigger_init_after_2_secs = (
  0, 2, ti_once, [],
  [
    (try_for_agents, ":agent_no"),
      (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),
    (try_end),
    ])

common_siege_defender_reinforcement_check = (
  3, 0, 5, [],
  [(lt, "$defender_reinforcement_stage", 7),
   (store_mission_timer_a, ":mission_time"),
   (ge, ":mission_time", 10),
   (store_normalized_team_count, ":num_defenders", 0),
   (lt, ":num_defenders", 10),
   (add_reinforcements_to_entry, 4, 7),
   (val_add, "$defender_reinforcement_stage", 1),
   (try_begin),
     (ge, "$defender_reinforcement_stage", 2),
     (set_show_messages, 0),
     (team_give_order, "$defender_team", grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
     (team_give_order, "$defender_team_2", grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
     (set_show_messages, 1),
     (ge, "$defender_reinforcement_stage", 4),
     (set_show_messages, 0),
     (team_give_order, "$defender_team", grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
     (team_give_order, "$defender_team_2", grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
     (set_show_messages, 1),
   (try_end),
   ])


common_siege_defender_reinforcement_archer_reposition = (
  2, 0, 0,
  [
    (gt, "$defender_reinforcement_stage", 0),
    ],
  [
    (call_script, "script_siege_move_archers_to_archer_positions"),
    ])

common_siege_attacker_reinforcement_check = (
  1, 0, 5,
  [
    (lt, "$attacker_reinforcement_stage", 5),
    (store_mission_timer_a, ":mission_time"),
    (ge, ":mission_time", 10),
    (store_normalized_team_count, ":num_attackers", 1),
    (lt, ":num_attackers", 6)
    ],
  [
    (add_reinforcements_to_entry, 1, 8),
    (val_add, "$attacker_reinforcement_stage", 1),
    ])

common_siege_attacker_do_not_stall = (
  5, 0, 0, [],
  [ #Make sure attackers do not stall on the ladders...
    (try_for_agents, ":agent_no"),
      (agent_is_human, ":agent_no"),
      (agent_is_alive, ":agent_no"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (this_or_next|eq, ":agent_team", "$attacker_team"),
      (eq, ":agent_team", "$attacker_team_2"),
##      (neg|agent_is_defender, ":agent_no"),
      (agent_ai_set_always_attack_in_melee, ":agent_no", 1),
    (try_end),
    ])

common_battle_check_friendly_kills = (
  2, 0, 0, [],
  [
    (call_script, "script_check_friendly_kills"),
    ])

common_battle_check_victory_condition = (
  1, 60, ti_once,
  [
    (store_mission_timer_a, reg(1)),
    (ge, reg(1), 10),
    (all_enemies_defeated, 5),
#SoD    (neg|main_hero_fallen, 0),
    (set_mission_result, 1),
    (display_message, "str_msg_battle_won", bright_green),
    (assign, "$battle_won", 1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_play_victorious_sound"),
    ],
  [
    (call_script, "script_sod_post_defeat_record_aftermath", 1),
    (call_script, "script_sod_post_defeat_count_casualties_once"),
    (call_script, "script_sod_post_defeat_clear"),
    (finish_mission, 1),
    ])

common_battle_victory_display = (
  10, 0, 0, [],
  [
    (eq, "$battle_won", 1),
    (display_message, "str_msg_battle_won", bright_green),
    ])

common_siege_refill_ammo = (
  60, 0, 0, [],
  [#refill ammo of defenders every minute.
    (get_player_agent_no, ":player_agent"),
    (try_for_agents, ":cur_agent"),
      (neq, ":cur_agent", ":player_agent"),
      (agent_is_alive, ":cur_agent"),
      (agent_is_human, ":cur_agent"),
##      (agent_is_defender, ":cur_agent"),
      (agent_get_team, ":agent_team", ":cur_agent"),
      (this_or_next|eq, ":agent_team", "$defender_team"),
      (eq, ":agent_team", "$defender_team_2"),
      (agent_refill_ammo, ":cur_agent"),
    (try_end),
    ])

common_siege_check_defeat_condition = (
  1, 4, ti_once,
  [
    (main_hero_fallen)
    ],
  [
    (assign, "$pin_player_fallen", 1),
#SoD    (get_player_agent_no, ":player_agent"),
#   (agent_get_team, ":agent_team", ":player_agent"),
#    (try_begin),
#      (neq, "$attacker_team", ":agent_team"),
#      (neq, "$attacker_team_2", ":agent_team"),
#      (str_store_string, s5, "str_siege_continues"),
#      (call_script, "script_simulate_retreat", 8, 15),
#    (else_try),
#      (str_store_string, s5, "str_retreat"),
#      (call_script, "script_simulate_retreat", 5, 20),
#    (try_end),
#    (assign, "$g_battle_result", -1),
#    (set_mission_result, -1),
#    (call_script, "script_count_mission_casualties_from_agents"),
#SoD    (finish_mission, 0),
    ])

common_battle_order_panel = (
  0, 0, 0, [],
  [
    (game_key_clicked, gk_view_orders),
    (start_presentation, "prsnt_battle"),
    ])

common_battle_order_panel_tick = (
  0.1, 0, 0, [],
  [
    (eq, "$g_presentation_battle_active", 1),
    (call_script, "script_update_order_panel_statistics_and_map"),
    ])

common_battle_inventory = (
  ti_inventory_key_pressed, 0, 0, [],
  [
    (display_message, "str_use_baggage_for_inventory", black),
    ])

common_inventory_not_available = (
  ti_inventory_key_pressed, 0, 0,
  [
    (display_message, "str_cant_use_inventory_now", red),
    ], [])

common_siege_init_ai_and_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_siege_init_ai_and_belfry"),
    ], [])

common_siege_move_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_cf_siege_move_belfry"),
    ], [])

common_siege_rotate_belfry = (
  0, 2, ti_once,
  [
    (call_script, "script_cf_siege_rotate_belfry_platform"),
    ],
  [
    (assign, "$belfry_positioned", 3),
    ])

common_siege_assign_men_to_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_cf_siege_assign_men_to_belfry"),
    ], [])

################################
### Jinnai's Free-Camera Kit ###
################################

## Allow the camera view to move after player death - Jinnai
## Extended with SoD post-defeat follow camera support.
camera_trigger_1 = (ti_before_mission_start, 0, 0, [], [
        (assign, "$camera_mode", 0),
        (call_script, "script_sod_post_defeat_init"),
        ])

camera_trigger_2 = (0, 0, 1, [(main_hero_fallen), (game_key_clicked, gk_jump)], [
        (try_begin),
          (eq, "$camera_mode", 0),
          (call_script, "script_sod_post_defeat_rebuild_watch_list"),
          (try_begin),
            (gt, "$sod_post_defeat_focus_count", 0),
            (assign, "$camera_mode", 2),
            (assign, "$sod_post_defeat_state", 3),
            (mission_cam_set_mode, 1),
            (call_script, "script_sod_post_defeat_show_focus_message"),
            (try_begin),
              (eq, "$sod_post_defeat_help_shown", 0),
              (display_message, "@You have fallen. Jump cycles follow/free/normal camera; mouse buttons switch focus.", 0xDDDDDD),
              (assign, "$sod_post_defeat_help_shown", 1),
            (try_end),
          (else_try),
            (assign, "$camera_mode", 1),
            (assign, "$sod_post_defeat_state", 2),
          (try_end),
          (set_fixed_point_multiplier, 100),
          (assign, "$camera_height", 250),
          (mission_cam_set_mode, 1),
          (mission_cam_get_position, pos1),
          (position_get_rotation_around_z, ":rot", pos1),
          (init_position, pos2),
          (position_copy_origin, pos2, pos1),
          (position_rotate_z, pos2, ":rot"),
          (position_rotate_x, pos2, -5),
          (position_set_z_to_ground_level, pos2),
          (position_move_z, pos2, "$camera_height"),
          (mission_cam_set_position, pos2),
          (mission_cam_set_aparture, 97),
        (else_try),
          (eq, "$camera_mode", 2),
          (assign, "$camera_mode", 1),
          (assign, "$sod_post_defeat_state", 2),
          (display_message, "@Free camera.", 0xDDDDDD),
        (else_try),
          (assign, "$camera_mode", 0),
          (assign, "$sod_post_defeat_state", 0),
          (mission_cam_set_mode, 0, 1000, 0),
        (try_end),
        ])

camera_trigger_3 = (0, 0, 0, [(main_hero_fallen)], [
        (try_begin),
          (eq, "$sod_post_defeat_state", 0),
          (call_script, "script_sod_post_defeat_on_player_fallen"),
        (try_end),
        (try_begin),
          (eq, "$camera_mode", 2),
          (call_script, "script_sod_post_defeat_focus_camera"),
        (else_try),
          (game_key_is_down, gk_move_forward),
          (eq, "$camera_mode", 1),
        (set_fixed_point_multiplier, 100),
        (mission_cam_get_position, pos1),
        (position_rotate_x, pos1, 5),
        (position_get_rotation_around_z, ":rot", pos1),
        (store_sin, reg0, ":rot"),
        (store_cos, reg1, ":rot"),
        (try_begin),
          (game_key_is_down, gk_zoom),
          (val_mul, reg0, 1),
          (val_mul, reg1, 1),
        (else_try),
          (val_div, reg0, 10),
          (val_div, reg1, 10),
        (try_end),
        (position_move_x, pos1, reg0),
        (position_move_y, pos1, reg1),
        (position_set_z_to_ground_level, pos1),
        (position_move_z, pos1, "$camera_height"),
        (position_rotate_x, pos1, -5),
        (mission_cam_animate_to_position, pos1, 10, 0),
        (try_end),
        ])

camera_trigger_4 = (0, 0, 0, [(main_hero_fallen), (game_key_is_down, gk_move_backward), (eq, "$camera_mode", 1)], [
        (set_fixed_point_multiplier, 100),
        (mission_cam_get_position, pos1),
        (position_rotate_x, pos1, 5),
        (position_get_rotation_around_z, ":rot", pos1),
        (store_sin, reg0, ":rot"),
        (store_cos, reg1, ":rot"),
        (try_begin),
          (game_key_is_down, gk_zoom),
          (val_mul, reg0, -1),
          (val_mul, reg1, -1),
        (else_try),
          (val_div, reg0, -10),
          (val_div, reg1, -10),
        (try_end),
        (position_move_x, pos1, reg0),
        (position_move_y, pos1, reg1),
        (position_set_z_to_ground_level, pos1),
        (position_move_z, pos1, "$camera_height"),
        (position_rotate_x, pos1, -5),
        (mission_cam_animate_to_position, pos1, 10, 0),
        ])

camera_trigger_5 = (0, 0, 0, [(main_hero_fallen)], [
        (try_begin),
          (eq, "$camera_mode", 2),
          (key_clicked, key_right_mouse_button),
          (call_script, "script_sod_post_defeat_select_next_agent", 1),
          (call_script, "script_sod_post_defeat_show_focus_message"),
        (else_try),
          (game_key_is_down, gk_move_right),
          (eq, "$camera_mode", 1),
        (set_fixed_point_multiplier, 100),
        (mission_cam_get_position, pos1),
        (position_rotate_x, pos1, 5),
        (try_begin),
          (game_key_is_down, gk_zoom),
          (position_rotate_z, pos1, -4),
        (else_try),
          (position_rotate_z, pos1, -2),
        (try_end),
        (position_rotate_x, pos1, -5),
        (mission_cam_animate_to_position, pos1, 10, 0),
        (try_end),
        ])

camera_trigger_6 = (0, 0, 0, [(main_hero_fallen)], [
        (try_begin),
          (eq, "$camera_mode", 2),
          (key_clicked, key_left_mouse_button),
          (call_script, "script_sod_post_defeat_select_next_agent", -1),
          (call_script, "script_sod_post_defeat_show_focus_message"),
        (else_try),
          (game_key_is_down, gk_move_left),
          (eq, "$camera_mode", 1),
        (set_fixed_point_multiplier, 100),
        (mission_cam_get_position, pos1),
        (position_rotate_x, pos1, 5),
        (try_begin),
          (game_key_is_down, gk_zoom),
          (position_rotate_z, pos1, 4),
        (else_try),
          (position_rotate_z, pos1, 2),
        (try_end),
        (position_rotate_x, pos1, -5),
        (mission_cam_animate_to_position, pos1, 10, 0),
        (try_end),
        ])

camera_trigger_7 = (0, 0, 0, [(main_hero_fallen), (game_key_is_down, gk_attack), (eq, "$camera_mode", 1)], [
        (set_fixed_point_multiplier, 100),
        (mission_cam_get_position, pos1),
        (position_rotate_x, pos1, 5),
        (val_add, "$camera_height", 10),
        (val_min, "$camera_height", 800),
        (position_set_z_to_ground_level, pos1),
        (position_move_z, pos1, "$camera_height"),
        (position_rotate_x, pos1, -5),
        (mission_cam_animate_to_position, pos1, 10, 0),
        ])

camera_trigger_8 = (0, 0, 0, [(main_hero_fallen), (game_key_is_down, gk_defend), (eq, "$camera_mode", 1)], [
        (set_fixed_point_multiplier, 100),
        (mission_cam_get_position, pos1),
        (position_rotate_x, pos1, 5),
        (val_sub, "$camera_height", 10),
        (val_max, "$camera_height", 10),
        (position_set_z_to_ground_level, pos1),
        (position_move_z, pos1, "$camera_height"),
        (position_rotate_x, pos1, -5),
        (mission_cam_animate_to_position, pos1, 10, 0),
        ])

### Jinnai's free-camera end ###


########Tactical triggers below##########

# initialize globals
formations_init = (ti_before_mission_start, 0, 0, [],
    [
      (assign, "$rout", 0),
      (assign, "$airout", 0),
      (assign, "$g_enemy_surrenders", 0),
      (assign, "$formation", 0),
      (assign, "$infantryformationtype", 0),
      (assign, "$archerformationtype", 0),
      (assign, "$cavalryformationtype", 0),
    ]
  )

# 1, 2, 3 - choose which troops to order
formations_1 = (0, 0, 0, [(neg|main_hero_fallen), (key_clicked, key_2), (assign, "$formation", grc_infantry), ], [])
formations_2 = (0, 0, 0, [(neg|main_hero_fallen), (key_clicked, key_3), (assign, "$formation", grc_archers), ], [])
formations_3 = (0, 0, 0, [(neg|main_hero_fallen), (key_clicked, key_4), (assign, "$formation", grc_cavalry), ], [])

# 1 - native everyone selection also releases scripted formation movement.
# This keeps normal orders from inheriting stale scripted destinations.
formations_0 = (0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (key_clicked, key_1),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (assign, reg1, grc_infantry),
      (call_script, "script_formation_end"),
      (assign, reg1, grc_archers),
      (call_script, "script_formation_end"),
      (assign, reg1, grc_cavalry),
      (call_script, "script_formation_end"),
      (assign, "$infantryformationtype", 0),
      (assign, "$archerformationtype", 0),
      (assign, "$cavalryformationtype", 0),
    ],
    []
  )

# J - ranks
formations_j =  (0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (key_clicked, key_j),
      (neg|key_is_down, key_left_control),
      (neg|key_is_down, key_right_control),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (assign, reg1, "$formation"),
      (call_script, "script_cf_formation"),
      (try_begin),
        (eq, "$formation", grc_infantry),
        (assign, "$infantryformationtype", 1),
      (else_try),
        (eq, "$formation", grc_archers),
        (assign, "$archerformationtype", 1),
      (else_try),
        (eq, "$formation", grc_cavalry),
        (assign, "$cavalryformationtype", 1),
      (end_try),
      (display_message, "@Forming_ranks.", blue),
    ],
    []
  )

# P - stagger
formations_p =  (0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (key_clicked, key_p),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (assign, reg1, "$formation"),
      (call_script, "script_cf_formation_stagger"),
      (call_script, "script_cf_formation"),
      (try_begin),
        (eq, "$formation", grc_infantry),
        (assign, "$infantryformationtype", 3),
      (else_try),
        (eq, "$formation", grc_archers),
        (assign, "$archerformationtype", 3),
      (else_try),
        (eq, "$formation", grc_cavalry),
        (assign, "$cavalryformationtype", 3),
      (end_try),
      (display_message, "@Forming_a_line.", blue),
    ],
    []
  )

# K - wedge
formations_k =  (0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (key_clicked, key_k),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (assign, reg1, "$formation"),
      (call_script, "script_cf_formation_wedge"),
      (call_script, "script_cf_formation"),
      (try_begin),
        (eq, "$formation", grc_infantry),
        (assign, "$infantryformationtype", 2),
      (else_try),
        (eq, "$formation", grc_archers),
        (assign, "$archerformationtype", 2),
      (else_try),
        (eq, "$formation", grc_cavalry),
        (assign, "$cavalryformationtype", 2),
      (end_try),
      (display_message, "@Forming_a_wedge.", blue),
    ],
    []
  )

# U - undo formations (allows troops to become a mob again)
formations_u = (0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (key_clicked, key_u),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (assign, reg1, "$formation"),
      (call_script, "script_formation_end"),
      (try_begin),
        (eq, "$formation", grc_infantry),
        (assign, "$infantryformationtype", 0),
      (else_try),
        (eq, "$formation", grc_archers),
        (assign, "$archerformationtype", 0),
      (else_try),
        (eq, "$formation", grc_cavalry),
        (assign, "$cavalryformationtype", 0),
      (end_try),
      (display_message, "@Formation_disassembled.", blue),
    ],
    []
  )

# stop moving ai units into formation
formations_ai_end = (5.0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (try_for_agents, ":agent"),
        (agent_is_human, ":agent"),
        (neg|agent_is_ally, ":agent"),
        (assign, ":enemy", ":agent"),
      (end_try),
      (gt, ":enemy", -1),
      (eq, "$airout", 0),
      (agent_get_team, reg0, ":enemy"),
      (assign, reg1, grc_cavalry),
      (call_script, "script_formation_end"),
      (assign, reg1, grc_infantry),
      (call_script, "script_formation_end"),
      (assign, reg1, grc_archers),
      (call_script, "script_formation_end"),
    ],
    []
  )

# order the ai's cavalry to dismount if they have less than 10 of them #SoD NEVER DISMOUNT!
formations_ai_dismount =  (5.0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
	  (neq, "$g_disable_formations_dismount", 1),
      (assign, ":enemy", -1),
      (assign, ":infantry", 0),
      (assign, ":cavalry", 0),
      (try_for_agents, ":agent"),
        (agent_is_human, ":agent"),
        (agent_is_alive, ":agent"),
        (neg|agent_is_ally, ":agent"),
        (assign, ":enemy", ":agent"),
        (agent_get_class , ":class", ":agent"),
        (try_begin),
          (eq, ":class", grc_cavalry),
          (val_add, ":cavalry", 1),
        (else_try),
          (val_add, ":infantry", 1),
        (end_try),
      (end_try),
      (gt, ":enemy", -1),
      (agent_get_team, reg0, ":enemy"),
      (assign, ":ratio", ":infantry"),
      (val_max, ":cavalry", 1),
      (val_div, ":ratio", ":cavalry"),
        (team_give_order, reg0, grc_cavalry, mordr_mount),
      ],
      []
    )

# stop moving units into formations
formations_end = (5.0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (eq, "$rout", 0),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (val_add, reg0, 2),
      (assign, reg1, grc_cavalry),
      (call_script, "script_formation_end"),
      (assign, reg1, grc_infantry),
      (call_script, "script_formation_end"),
      (assign, reg1, grc_archers),
      (call_script, "script_formation_end"),
    ],
    []
  )

# order the player's cavalry to dismount if the the player has less than 10 of them
formations_dismount = (5.0, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
	  (neq, "$g_disable_formations_dismount", 1),
      (neg|main_hero_fallen),
      (neq, "$battle_won", 1),
      (assign, ":infantry", 0),
      (assign, ":cavalry", 0),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (val_add, reg0, 2),
      (try_for_agents, ":agent"),
        (agent_is_human, ":agent"),
        (agent_is_alive, ":agent"),
        (agent_get_team  , ":team", ":agent"),
        (eq, ":team", reg0),
        (agent_get_class , ":class", ":agent"),
        (try_begin),
          (eq, ":class", grc_cavalry),
          (val_add, ":cavalry", 1),
        (else_try),
          (val_add, ":infantry", 1),
        (end_try),
      (end_try),
      (assign, ":ratio", ":infantry"),
      (val_max, ":cavalry", 1),
      (val_div, ":ratio", ":cavalry"),
      (try_begin),
        (gt, ":ratio", 2),
        (lt, ":cavalry", 10),
        (team_give_order, reg0, grc_everyone, mordr_dismount),
      (else_try),
        (team_give_order, reg0, grc_everyone, mordr_mount),
      (end_try),
    ],
    []
  )

# update infantry to the chosen formation
formations_move_infantry = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (eq, "$rout", 0),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (assign, reg1, grc_infantry),
      (try_begin),
        (eq, "$infantryformationtype", 1),
        (call_script, "script_cf_formation"),
      (else_try),
        (eq, "$infantryformationtype", 2),
        (call_script, "script_cf_formation_wedge"),
      (else_try),
        (eq, "$infantryformationtype", 3),
        (call_script, "script_cf_formation_stagger"),
      (else_try),
        (call_script, "script_formation_end"),
      (end_try),
    ],
    []
  )

# update archers to the chosen formation
formations_move_archers = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (eq, "$rout", 0),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (assign, reg1, grc_archers),
      (try_begin),
        (eq, "$archerformationtype", 1),
        (call_script, "script_cf_formation"),
      (else_try),
        (eq, "$archerformationtype", 2),
        (call_script, "script_cf_formation_wedge"),
      (else_try),
        (eq, "$archerformationtype", 3),
        (call_script, "script_cf_formation_stagger"),
      (else_try),
        (call_script, "script_formation_end"),
      (end_try),
    ],
    []
  )

# update cavalry to the chosen formation
formations_move_cavalry = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (eq, "$rout", 0),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (assign, reg1, grc_cavalry),
      (try_begin),
        (eq, "$cavalryformationtype", 1),
        (call_script, "script_cf_formation"),
      (else_try),
        (eq, "$cavalryformationtype", 2),
        (call_script, "script_cf_formation_wedge"),
      (else_try),
        (eq, "$cavalryformationtype", 3),
        (call_script, "script_cf_formation_stagger"),
      (else_try),
        (call_script, "script_formation_end"),
      (end_try),
    ],
    []
  )

# update ai infantry to line
formations_update_ai_infantry = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (eq, "$airout", 0),
      (try_for_agents, ":agent"),
        (agent_is_human, ":agent"),
        (neg|agent_is_ally, ":agent"),
        (assign, ":enemy", ":agent"),
      (end_try),
      (gt, ":enemy", -1),
      (agent_get_team, reg0, ":enemy"),
      (store_normalized_team_count, ":num", reg0),
      (gt, ":num", 5),
      (assign, reg1, grc_infantry),
      (call_script, "script_cf_formation"),
    ],
    []
  )

# update ai archers to staggered
formations_update_ai_archers = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (eq, "$airout", 0),
      (try_for_agents, ":agent"),
        (agent_is_human, ":agent"),
        (neg|agent_is_ally, ":agent"),
        (assign, ":enemy", ":agent"),
      (end_try),
      (gt, ":enemy", -1),
      (agent_get_team, reg0, ":enemy"),
      (store_normalized_team_count, ":num", reg0),
      (gt, ":num", 5),
      (assign, reg1, grc_archers),
      (call_script, "script_cf_formation_stagger"),
    ],
    []
  )

# update ai cavalry to wedge
formations_update_ai_cavalry = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (eq, "$airout", 0),
      (try_for_agents, ":agent"),
        (agent_is_human, ":agent"),
        (neg|agent_is_ally, ":agent"),
        (assign, ":enemy", ":agent"),
      (end_try),
      (gt, ":enemy", -1),
      (agent_get_team, reg0, ":enemy"),
      (store_normalized_team_count, ":num", reg0),
      (gt, ":num", 5),
      (assign, reg1, grc_cavalry),
      (call_script, "script_cf_formation_wedge"),
    ],
    []
  )

# default infantry to line formation
formations_update_ally_infantry = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (eq, "$rout", 0),
      (neq, "$battle_won", 1),
      (eq, "$rout", 0),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (val_add, reg0, 2),
      (store_normalized_team_count, ":num", reg0),
      (gt, ":num", 5),
      (assign, reg1, grc_infantry),
      (call_script, "script_cf_formation"),
    ],
    []
  )

# default archers to staggered formation
formations_update_ally_archers = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (eq, "$rout", 0),
      (neq, "$battle_won", 1),
      (eq, "$rout", 0),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (val_add, reg0, 2),
      (store_normalized_team_count, ":num", reg0),
      (gt, ":num", 5),
      (assign, reg1, grc_archers),
      (call_script, "script_cf_formation_stagger"),
    ],
    []
  )

# default cavalry to wedge formation
formations_update_ally_cavalry = (0.2, 0, 0,
    [
      (neq, "$g_disable_formations", 1),
      (neg|main_hero_fallen),
      (eq, "$rout", 0),
      (neq, "$battle_won", 1),
      (eq, "$rout", 0),
      (get_player_agent_no, ":player"),
      (agent_get_team, reg0, ":player"),
      (val_add, reg0, 2),
      (store_normalized_team_count, ":num", reg0),
      (gt, ":num", 5),
      (assign, reg1, grc_cavalry),
      (call_script, "script_cf_formation_wedge"),
    ],
    []
  )

# initialize kill count
formations_init_kill_count = (1, 0, ti_once, [],
    [
      (get_player_agent_kill_count, "$base_kills", 0),
      (assign, "$new_kills_a", 0),
      (assign, "$new_kills", 0),
      (assign, "$sod_artifact_last_player_kills", 0),
    ]
  )

# update kill count
formations_update_kill_count = (3, 0, 3, [(neg|main_hero_fallen)],
    [
      (get_player_agent_kill_count, ":more_kills", 0),
      (val_sub, ":more_kills", "$base_kills"),
      (try_begin),
        (gt, ":more_kills", "$new_kills_a"),
        (assign, "$new_kills_a", ":more_kills"),
        (assign, "$new_kills", ":more_kills"),
        (val_div, "$new_kills", 2),
        (store_sub, ":artifact_delta", ":more_kills", "$sod_artifact_last_player_kills"),
        (try_begin),
          (gt, ":artifact_delta", 0),
          (get_player_agent_no, ":player_agent"),
          (agent_get_wielded_item, ":artifact_item", ":player_agent", 0),
          (gt, ":artifact_item", 0),
          (call_script, "script_sod_artifact_add_kill", ":artifact_item", 0, "trp_player", ":artifact_delta"),
          (assign, "$sod_artifact_last_player_kills", ":more_kills"),
        (try_end),
        (assign, reg1, ":more_kills"),
        (display_message, "@You have killed {reg1} enemies in this battle!", 0x6495ed),
        (neq, "$g_disable_morale", 1),
        (display_message, "@Your bravery inspires your troops!", 0x6495ed),
      (try_end),
    ]
  )

# health bars (T)
formations_t = (0, 0, 2,
    [
      (neq, "$g_disable_morale", 1),
      (key_clicked, key_t),
      (assign, ":allow_healthbars", 1),
      (try_begin),
        (eq, "$ponavosa_duel_disabled_this_battle", 0),
        (eq, "$ponavosa_duel_active", 0),
        (store_mission_timer_a, ":now"),
        (ge, ":now", "$ponavosa_duel_cooldown_until"),
        (call_script, "script_ponavosa_duel_find_commander_pair", 1),
        (eq, reg0, 1),
        (assign, ":allow_healthbars", 0),
      (try_end),
      (eq, ":allow_healthbars", 1),
    ],
    [
      (call_script, "script_coherence"),
      (call_script, "script_healthbars"),
    ]
  )

# rally troops (Y)
formations_y = (0, 0, ti_once,
    [
      (neq, "$g_disable_morale", 1),
      (key_clicked, key_y)
    ],
    [
      (display_message, "@You rally your men!", 0x7ccd7c),
      (call_script, "script_battle_cry"),
      (call_script, "script_hero_exp_penalty"),
    ]
  )

# spontaneous rally
formations_rally = (10, 0, 20,
    [
      (neq, "$g_disable_morale", 1),
    ],
    [
      (call_script, "script_rally"),
    ]
  )

# call for reinforcements
formations_v = (0, 10, 100,
    [
	#Always ON, player is not forced to anything he can click V or not.
     # (neq, "$g_disable_formations", 1),
      (key_clicked, key_v),
    ],
    [
      (display_message, "@You call for reinforcements!", 0x6495ed),
      (display_message, "@Reinforcements arrive!", 0x6495ed),
      (add_reinforcements_to_entry, 0, 7),
      (add_reinforcements_to_entry, 3, 7),
      (call_script, "script_hero_exp_penalty"),
    ]
  )

commander_duel_init = (ti_before_mission_start, 0, 0, [],
    [
      (assign, "$ponavosa_duel_active", 0),
      (assign, "$ponavosa_duel_ally_agent", -1),
      (assign, "$ponavosa_duel_enemy_agent", -1),
      (assign, "$ponavosa_duel_ally_team", -1),
      (assign, "$ponavosa_duel_enemy_team", -1),
      (assign, "$ponavosa_duel_start_time", 0),
      (assign, "$ponavosa_duel_cooldown_until", 90),
      (assign, "$ponavosa_duel_player_involved", 0),
      (assign, "$ponavosa_duel_camera_active", 0),
      (assign, "$ponavosa_duel_nemesis", 0),
      (assign, "$ponavosa_duel_disabled_this_battle", 0),
      (try_begin),
        (eq, "$g_sod_joined_ongoing_ai_battle", 1),
        (assign, "$ponavosa_duel_disabled_this_battle", 1),
      (try_end),
      (assign, "$g_sod_battle_ally_duel_momentum", 0),
      (assign, "$g_sod_battle_enemy_duel_momentum", 0),
      (assign, "$g_sod_battle_player_morale_wavered", 0),
      (assign, "$g_sod_battle_player_morale_collapsed", 0),
    ]
  )

commander_duel_player_challenge = (0, 0, 1,
    [
      (eq, "$ponavosa_duel_disabled_this_battle", 0),
      (eq, "$ponavosa_duel_active", 0),
      (store_mission_timer_a, ":now"),
      (ge, ":now", "$ponavosa_duel_cooldown_until"),
      (key_clicked, key_t),
      (call_script, "script_ponavosa_duel_find_commander_pair", 1),
      (eq, reg0, 1),
    ],
    [
      (call_script, "script_ponavosa_duel_begin", reg1, reg2),
    ]
  )

commander_duel_player_feedback = (0, 0, 1,
    [
      (eq, "$ponavosa_duel_disabled_this_battle", 0),
      (eq, "$ponavosa_duel_active", 0),
      (key_clicked, key_t),
    ],
    [
      (store_mission_timer_a, ":now"),
      (try_begin),
        (lt, ":now", "$ponavosa_duel_cooldown_until"),
        (store_sub, reg1, "$ponavosa_duel_cooldown_until", ":now"),
        (display_message, "@The field is not ready for another commander duel. Wait {reg1} seconds.", 0xFFD27A),
      (else_try),
        (call_script, "script_ponavosa_duel_find_commander_pair", 1),
        (eq, reg0, 0),
        (call_script, "script_ponavosa_duel_explain_challenge"),
      (try_end),
    ]
  )

commander_duel_ai_challenge = (15, 0, 30,
    [
      (eq, "$ponavosa_duel_disabled_this_battle", 0),
      (eq, "$ponavosa_duel_active", 0),
      (store_mission_timer_a, ":now"),
      (ge, ":now", "$ponavosa_duel_cooldown_until"),
      (store_random_in_range, ":roll", 0, 100),
      (assign, ":challenge_chance", 18),
      (try_begin),
        (eq, "$g_sod_nemesis_actor_type", sod_nemesis_actor_lord),
        (ge, "$g_sod_nemesis_state", sod_nemesis_state_hunting),
        (is_between, "$g_sod_nemesis_last_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (assign, ":nemesis_present", 0),
        (try_for_agents, ":nemesis_agent"),
          (agent_is_alive, ":nemesis_agent"),
          (agent_is_human, ":nemesis_agent"),
          (neg|agent_is_ally, ":nemesis_agent"),
          (agent_get_troop_id, ":nemesis_troop", ":nemesis_agent"),
          (eq, ":nemesis_troop", "$g_sod_nemesis_last_troop"),
          (assign, ":nemesis_present", 1),
        (try_end),
        (eq, ":nemesis_present", 1),
        (troop_get_slot, ":duel_pressure", "$g_sod_nemesis_last_troop", slot_troop_sod_nemesis_duel_pressure),
        (troop_get_slot, ":defeats", "$g_sod_nemesis_last_troop", slot_troop_sod_nemesis_defeats),
        (val_mul, ":duel_pressure", 5),
        (val_mul, ":defeats", 3),
        (val_add, ":challenge_chance", ":duel_pressure"),
        (val_add, ":challenge_chance", ":defeats"),
        (val_min, ":challenge_chance", 65),
      (try_end),
      (lt, ":roll", ":challenge_chance"),
      (call_script, "script_ponavosa_duel_find_commander_pair", 0),
      (eq, reg0, 1),
    ],
    [
      (call_script, "script_ponavosa_duel_begin", reg1, reg2),
    ]
  )

commander_duel_tick = (1, 0, 0,
    [
      (eq, "$ponavosa_duel_active", 1),
    ],
    [
      (store_mission_timer_a, ":now"),
      (store_sub, ":elapsed", ":now", "$ponavosa_duel_start_time"),
      (try_begin),
        (this_or_next|neg|agent_is_alive, "$ponavosa_duel_enemy_agent"),
        (neg|agent_is_human, "$ponavosa_duel_enemy_agent"),
        (call_script, "script_ponavosa_duel_resolve", 1),
      (else_try),
        (this_or_next|neg|agent_is_alive, "$ponavosa_duel_ally_agent"),
        (neg|agent_is_human, "$ponavosa_duel_ally_agent"),
        (call_script, "script_ponavosa_duel_resolve", 2),
      (else_try),
        (gt, ":elapsed", 180),
        (call_script, "script_ponavosa_duel_resolve", 4),
      (else_try),
        (agent_get_position, pos1, "$ponavosa_duel_ally_agent"),
        (agent_get_position, pos2, "$ponavosa_duel_enemy_agent"),
        (get_distance_between_positions, ":dist", pos1, pos2),
        (gt, ":dist", 3000),
        (call_script, "script_ponavosa_duel_resolve", 3),
      (try_end),
    ]
  )

commander_duel_camera_tick = (0, 0, 0,
    [
      (eq, "$ponavosa_duel_active", 1),
      (eq, "$ponavosa_duel_player_involved", 0),
      (ge, "$ponavosa_duel_ally_agent", 0),
      (ge, "$ponavosa_duel_enemy_agent", 0),
      (agent_is_human, "$ponavosa_duel_ally_agent"),
      (agent_is_human, "$ponavosa_duel_enemy_agent"),
    ],
    [
      (assign, "$ponavosa_duel_camera_active", 1),
      (agent_get_position, pos1, "$ponavosa_duel_ally_agent"),
      (agent_get_position, pos2, "$ponavosa_duel_enemy_agent"),
      (position_get_x, ":x1", pos1),
      (position_get_y, ":y1", pos1),
      (position_get_x, ":x2", pos2),
      (position_get_y, ":y2", pos2),
      (store_add, ":mx", ":x1", ":x2"),
      (store_add, ":my", ":y1", ":y2"),
      (val_div, ":mx", 2),
      (val_div, ":my", 2),
      (position_set_x, pos3, ":mx"),
      (position_set_y, pos3, ":my"),
      (position_set_z_to_ground_level, pos3),
      (position_move_y, pos3, -650),
      (position_move_z, pos3, 520),
      (mission_cam_set_mode, 1),
      (mission_cam_set_position, pos3),
    ]
  )

# coherence start
formations_start_coherence = (1, 0, ti_once,
    [
      (neq, "$g_disable_morale", 1),
    ],
    [
      (call_script, "script_coherence"),
    ]
  )

# morale check
formations_update_morale = (15, 0, 10,
    [
      (neq, "$g_disable_morale", 1),
    ],
    [
      (call_script, "script_coherence"),
      (call_script, "script_morale_check"),
    ]
  )

# route check
formations_update_route = (5, 0, 3,
    [
      (neq, "$g_disable_morale", 1),
    ],
    [
      (call_script, "script_coherence"),
      (call_script, "script_rout_check"),
    ]
  )

common_battle_enemy_surrender_check = (5, 0, 5,
    [
      (neq, "$g_disable_morale", 1),
      (eq, "$battle_won", 0),
    ],
    [
      (call_script, "script_coherence"),
      (call_script, "script_sod_battle_enemy_surrender_check"),
      (try_begin),
        (eq, reg0, 1),
        (call_script, "script_sod_post_defeat_record_aftermath", 1),
        (call_script, "script_sod_post_defeat_count_casualties_once"),
        (call_script, "script_sod_post_defeat_clear"),
        (finish_mission, 1),
      (try_end),
    ]
  )

# Siege wall assaults use limited morale pressure. The attacker can waver on
# the approach, but defenders should not be routed through siege walls.
common_siege_attacker_morale_pressure = (15, 0, 10,
    [
      (neq, "$g_disable_morale", 1),
    ],
    [
      (call_script, "script_coherence"),
      (try_begin),
        (lt, "$allies_coh", 450),
        (store_random_in_range, ":routed", 1, 101),
        (assign, ":chance_ply", 91),
        (assign, ":allymod", "$allies_coh"),
        (val_div, ":allymod", 5),
        (val_sub, ":chance_ply", ":allymod"),
        (le, ":routed", ":chance_ply"),
        (display_message, "@Your assault wavers under the walls!", red),
        (assign, "$g_sod_battle_player_morale_wavered", 1),
        (call_script, "script_flee_allies"),
      (try_end),
    ]
  )

##########Tactical triggers above#########



tournament_triggers = [
  (ti_before_mission_start, 0, 0, [],
    [(call_script, "script_change_banners_and_chest"),
     (assign, "$g_arena_training_num_agents_spawned", 0)]),

  (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_arena", red)], []),

  (ti_tab_pressed, 0, 0, [],
   [(try_begin),
      (eq, "$g_mt_mode", abm_visit),
      (set_trigger_result, 1),
    (else_try),
      (question_box, "str_give_up_fight"),
    (try_end),
    ]),
  (ti_question_answered, 0, 0, [],
   [(store_trigger_param_1, ":answer"),
    (eq, ":answer", 0),
    (try_begin),
      (eq, "$g_mt_mode", abm_tournament),
      (call_script, "script_end_tournament_fight", 0),
    (else_try),
      (eq, "$g_mt_mode", abm_training),
      (get_player_agent_no, ":player_agent"),
      (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1), #use this for conversation
    (try_end),
    (finish_mission, 0),
    ]),

  (1, 0, ti_once, [], [
      (eq, "$g_mt_mode", abm_visit),
      (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
      (store_current_scene, reg(1)),
      (scene_set_slot, reg(1), slot_scene_visited, 1),
      (mission_enable_talk),
      (get_player_agent_no, ":player_agent"),
      (assign, ":team_set", 0),
      (try_for_agents, ":agent_no"),
        (neq, ":agent_no", ":player_agent"),
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (is_between, ":troop_id", regular_troops_begin, regular_troops_end),
        (eq, ":team_set", 0),
        (agent_set_team, ":agent_no", 1),
        (assign, ":team_set", 1),
      (try_end),
    ]),

  (0, 0, ti_once, [],
   [
     (eq, "$g_mt_mode", abm_tournament),
     (play_sound, "snd_arena_ambiance", sf_looping),
     (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
     ]),

  (1, 4, ti_once, [(eq, "$g_mt_mode", abm_tournament),
                   (this_or_next|main_hero_fallen),
                   (num_active_teams_le, 1)],
   [
       (try_begin),
         (neg|main_hero_fallen),
         (call_script, "script_end_tournament_fight", 1),
         (call_script, "script_play_victorious_sound"),
         (finish_mission),
       (else_try),
         (call_script, "script_end_tournament_fight", 0),
         (finish_mission),
       (try_end),
       ]),

  (0, 0, ti_once, [], [(eq, "$g_mt_mode", abm_training), (start_presentation, "prsnt_arena_training")]),
  (0, 0, ti_once, [], [(eq, "$g_mt_mode", abm_training),
                       (assign, "$g_arena_training_max_opponents", 40),
                       (assign, "$g_arena_training_num_agents_spawned", 0),
                       (assign, "$g_arena_training_kills", 0),
                       (assign, "$g_arena_training_won", 0),
                       (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
                       ]),

  (1, 4, ti_once, [(eq, "$g_mt_mode", abm_training),
                   (store_mission_timer_a, ":cur_time"),
                   (gt, ":cur_time", 3),
                   (assign, ":win_cond", 0),
                   (try_begin),
                     (ge, "$g_arena_training_num_agents_spawned", "$g_arena_training_max_opponents"), #spawn at most 40 agents
                     (num_active_teams_le, 1),
                     (assign, ":win_cond", 1),
                   (try_end),
                   (this_or_next|eq, ":win_cond", 1),
                   (main_hero_fallen)],
   [
       (get_player_agent_no, ":player_agent"),
       (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1), #use this for conversation
       (assign, "$g_arena_training_won", 0),
       (try_begin),
         (neg|main_hero_fallen),
         (assign, "$g_arena_training_won", 1), #use this for conversation
       (try_end),
       (assign, "$g_mt_mode", abm_visit),
       (set_jump_mission, "mt_arena_melee_fight"),
       (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
       (modify_visitors_at_site, ":arena_scene"),
       (reset_visitors),
       (set_visitor, 35, "trp_veteran_fighter"),
       (set_visitor, 36, "trp_hired_blade"),
       (set_jump_entry, 50),
       (jump_to_scene, ":arena_scene"),
       ]),


  (0.2, 0, 0,
   [
       (eq, "$g_mt_mode", abm_training),
       (assign, ":num_active_fighters", 0),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (agent_get_team, ":team_no", ":agent_no"),
         (is_between, ":team_no", 0 , 7),
         (val_add, ":num_active_fighters", 1),
       (try_end),
       (lt, ":num_active_fighters", 7),
       (neg|main_hero_fallen),
       (store_mission_timer_a, ":cur_time"),
       (this_or_next|ge, ":cur_time", "$g_arena_training_next_spawn_time"),
       (this_or_next|lt, "$g_arena_training_num_agents_spawned", 6),
       (num_active_teams_le, 1),
       (lt, "$g_arena_training_num_agents_spawned", "$g_arena_training_max_opponents"),
      ],
    [
       (assign, ":added_troop", "$g_arena_training_num_agents_spawned"),
       (store_div,  ":added_troop", "$g_arena_training_num_agents_spawned", 6),
       (assign, ":added_troop_sequence", "$g_arena_training_num_agents_spawned"),
       (val_mod, ":added_troop_sequence", 6),
       (val_add, ":added_troop", ":added_troop_sequence"),
       (val_min, ":added_troop", 9),
       (val_add, ":added_troop", "trp_arena_training_fighter_1"),
       (assign, ":end_cond", 10000),
       (get_player_agent_no, ":player_agent"),
       (agent_get_position, pos5, ":player_agent"),
       (try_for_range, ":unused", 0, ":end_cond"),
         (store_random_in_range, ":random_entry_point", 32, 40),
         (neq, ":random_entry_point", "$g_player_entry_point"), # make sure we don't overwrite player
         (entry_point_get_position, pos1, ":random_entry_point"),
         (get_distance_between_positions, ":dist", pos5, pos1),
         (gt, ":dist", 1200), #must be at least 12 meters away from the player
         (assign, ":end_cond", 0),
       (try_end),
       (add_visitors_to_current_scene, ":random_entry_point", ":added_troop", 1),
       (store_add, ":new_spawned_count", "$g_arena_training_num_agents_spawned", 1),
       (store_mission_timer_a, ":cur_time"),
       (store_add, "$g_arena_training_next_spawn_time", ":cur_time", 14),
       (store_div, ":time_reduction", ":new_spawned_count", 3),
       (val_sub, "$g_arena_training_next_spawn_time", ":time_reduction"),
       ]),

  (0, 0, 0,
   [
       (eq, "$g_mt_mode", abm_training)
       ],
    [
       (assign, ":max_teams", 6),
       (val_max, ":max_teams", 1),
       (get_player_agent_no, ":player_agent"),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (agent_slot_eq, ":agent_no", slot_agent_arena_team_set, 0),
         (agent_get_team, ":team_no", ":agent_no"),
         (is_between, ":team_no", 0 , 7),
         (try_begin),
           (eq, ":agent_no", ":player_agent"),
           (agent_set_team, ":agent_no", 6), #player is always team 6.
         (else_try),
           (store_random_in_range, ":selected_team", 0, ":max_teams"),
          # find strongest team
           (try_for_range, ":t", 0, 6),
             (troop_set_slot, "trp_temp_array_a", ":t", 0),
           (try_end),
           (try_for_agents, ":other_agent_no"),
             (agent_is_human, ":other_agent_no"),
             (agent_is_alive, ":other_agent_no"),
             (neq, ":agent_no", ":player_agent"),
             (agent_slot_eq, ":other_agent_no", slot_agent_arena_team_set, 1),
             (agent_get_team, ":other_agent_team", ":other_agent_no"),
             (troop_get_slot, ":count", "trp_temp_array_a", ":other_agent_team"),
             (val_add, ":count", 1),
             (troop_set_slot, "trp_temp_array_a", ":other_agent_team", ":count"),
           (try_end),
           (assign, ":strongest_team", 0),
           (troop_get_slot, ":strongest_team_count", "trp_temp_array_a", 0),
           (try_for_range, ":t", 1, 6),
             (troop_slot_ge, "trp_temp_array_a", ":t", ":strongest_team_count"),
             (troop_get_slot, ":strongest_team_count", "trp_temp_array_a", ":t"),
             (assign, ":strongest_team", ":t"),
           (try_end),
           (store_random_in_range, ":rand", 5, 100),
           (try_begin),
             (lt, ":rand", "$g_arena_training_num_agents_spawned"),
             (assign, ":selected_team", ":strongest_team"),
           (try_end),
           (agent_set_team, ":agent_no", ":selected_team"),
         (try_end),
         (agent_set_slot, ":agent_no", slot_agent_arena_team_set, 1),
         (try_begin),
           (neq, ":agent_no", ":player_agent"),
           (val_add, "$g_arena_training_num_agents_spawned", 1),
         (try_end),
       (try_end),
       ]),
  ]
  
fgtq_triggers = [
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_arena_fight_tab_press, 

	  (ti_question_answered, 0, 0, [],
       [
         (store_trigger_param_1, ":answer"),
         (eq, ":answer", 0),
		 (call_script, "script_fgtq_end", 0),
         ]),
		 
      (1, 3, ti_once, [(main_hero_fallen)],
       [
		 (call_script, "script_fgtq_end", 0),
         ]),
		 
      (1, 3, ti_once,
       [
         (store_mission_timer_a, reg1),
         (ge, reg1, 1),
         (num_active_teams_le, 1),
         (neg|main_hero_fallen),
         ],
       [
		 (call_script, "script_fgtq_end", 1),
         ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_arena", red)], []),
    ]
