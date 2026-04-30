from ID_items import *
from ID_quests import *
from ID_factions import *
from ID_troops import *
from header_operations import *
##############################################################
# These constants are used in various files.
# If you need to define a value that will be used in those files,
# just define it here rather than copying it across each file, so
# that it will be easy to change it if you need to.
##############################################################

white         = 0xFFFFFFFF
black         = 0xFF000000   # black comes out as white

light_gray    = 0xFFC0C0C0
gray          = 0xFFA0A0A0
dark_gray     = 0xFF808080

bright_red    = 0xFFFF0000
bright_green  = 0xFF00FF00
bright_blue   = 0xFF0000FF
red           = 0xFFA00000
green         = 0xFF00A000
blue          = 0xFF0000A0
dark_red      = 0xFF800000
dark_green    = 0xFF008000
dark_blue     = 0xFF000080

yellow        = 0xFFFFFF80
bannana       = 0xFFFFFF00
gold          = 0xFFF0C020
orange        = 0xFFFF8000
brown         = 0xFFC06000
dark_brown    = 0xFF804000
peach         = 0xFFFFB080
powder_blue   = 0xFF0080C0
cyan          = 0xFF00C0C0
teal          = 0xFF008080
dark_teal     = 0xFF004080
violet        = 0xFFC000C0
purple        = 0xFF8000C0
plum          = 0xFF800080
periwinkle    = 0xFF8080FF
pink          = 0xFFFF80FF
hot_pink      = 0xFFFF00FF
cobalt        = 0xFF004080
pastel_green  = 0xFF80FF80
dark_pastel_green = 0xFF20C020
maroon        = 0xFF800040

renown_color  = violet
lose_renown_color = plum
gain_relation_color = cyan
lose_relation_color = dark_teal
gain_morale_color = pastel_green
lose_morale_color = dark_pastel_green
debug_color = dark_gray
faith_color = hot_pink
money_color = gold
good_color = green
bad_color = red
build_color = peach
pop_color = peach
honor_color = cobalt
lose_honor_color = black
warning_color = orange
quest_success_color = green
quest_fail_color = maroon
trivia_color = dark_teal
important_color = pink

########################################################
##  Global Constants             #######################
########################################################

current_file_version            = 460

village_pop_min                 = 50
village_pop_max                 = 500
village_pop_ideal               = (village_pop_max-village_pop_min)/2+village_pop_min

town_pop_min                    = 500
town_pop_max                    = 3000
town_pop_ideal                  = (town_pop_max-town_pop_min)/2+town_pop_min

center_initial_reaction_low     = -5
center_initial_reaction_high    = 5

investment_min_risk             = 33

leadership_discount_multiplier  = 5

ideal_prosperity_rate           = 5     # this is the change, per week, that prosperity will move towards the ideal prosperity for that location (see script_get_center_ideal_prosperity)
ideal_health_rate               = 5     # this is the change, per week, that health will tend towards the ideal health for that location

# Population migration (weekly): centers with low prosperity can lose pop to higher-prosperity centers
sod_migration_prosperity_max     = 40    # only centers with prosperity below this can lose population to migration
sod_migration_pop_surplus_min   = 15    # need at least this many people above min before any can migrate
sod_migration_max_per_week      = 25    # max people leaving one center per week
# Desperation bandits (weekly): very low prosperity can cause some population to turn bandit
sod_desperation_prosperity_max  = 25    # below this prosperity, chance each week that some pop become bandits
sod_desperation_chance_percent  = 6     # chance per center per week (0-100)
sod_desperation_pop_surplus_min = 10    # need at least this surplus above min before desperation can trigger

# Ultimate troops (zealots): minimum effective faith required for the upgrade event to fire
sod_zealot_min_faith            = 100   # effective faith (global_faith - holy*10) must be >= this to get zealot event

# Nobles: population cap for immigration (nobles per run <= total_chapter_pop / divisor)
sod_noble_cap_pop_divisor        = 2000  # higher = fewer nobles for same population

# Economy: population-based scaling (tunable for balance)
sod_town_consumption_pop_divisor = 400   # weekly grain/flour consumption = town_pop / this (min 1)
sod_town_consumption_extra_pop_divisor = 800  # meat/ale consumption = town_pop / this (min 1), typically lower than grain
sod_cattle_production_pop_divisor = 200 # cattle meat production *= village_pop / this

# Caravan progression: profitable kingdom caravans can scale up over time.
sod_caravan_upgrade_profit_tier_1 = 250   # total realized trade profit needed for first upgrade
sod_caravan_upgrade_profit_tier_2 = 700   # total realized trade profit needed for second upgrade
sod_caravan_upgrade_profit_tier_3 = 1400  # total realized trade profit needed for third upgrade
sod_caravan_trade_percent_bonus_per_tier = 5  # extra trade intensity passed to script_do_party_center_trade per tier

# Nobles: happiness bonus from realm population (larger realm = more attractive to nobles)
sod_noble_happiness_pop_divisor  = 500  # bonus = total_chapter_pop / this, capped by _pop_bonus_max
sod_noble_happiness_pop_bonus_max = 15  # max happiness bonus from population

# Laws: safe range for globals when used in growth (avoid overflow/degenerate growth)
sod_law_tax_peasants_min         = 0
sod_law_tax_peasants_max         = 300
sod_law_town_population_modifier_min = 20
sod_law_town_population_modifier_max = 200
sod_law_village_population_modifier_min = 20
sod_law_village_population_modifier_max = 200
sod_law_nobles_happiness_min     = -100
sod_law_nobles_happiness_max     = 100
sod_law_max_active               = 10

# Law IDs. IDs 10, 20, and 30 are category spacers in the legacy presentation.
sod_law_none                     = 0
sod_law_village_fairs            = 1
sod_law_hunting_privileges       = 2
sod_law_access_to_woods          = 3
sod_law_brewing_privileges       = 4
sod_law_fair_trial               = 5
sod_law_enfranchisement          = 6
sod_law_high_capitation          = 7
sod_law_low_capitation           = 8
sod_law_representation           = 9
sod_law_spacer_villagers         = 10
sod_law_towns_mint               = 11
sod_law_tool_collecting          = 12
sod_law_sale_of_offices          = 13
sod_law_free_cities              = 14
sod_law_salt_mining              = 15
sod_law_mercantilism             = 16
sod_law_draft                    = 17
sod_law_low_town_taxes           = 18
sod_law_high_town_taxes          = 19
sod_law_spacer_townspeople       = 20
sod_law_inheritance              = 21
sod_law_tithe_from_villages      = 22
sod_law_tithe_from_towns         = 23
sod_law_clergy_immunity          = 24
sod_law_temple_supremacy         = 25
sod_law_royal_supremacy          = 26
sod_law_inquisition              = 27
sod_law_holy_war                 = 28
sod_law_theocracy                = 29
sod_law_spacer_clergy            = 30
sod_law_serfdom                  = 31
sod_law_noble_ransoms            = 32
sod_law_military_reimbursement   = 33
sod_law_nobles_domain            = 34
sod_law_economic_regulations     = 35
sod_law_arbitrary_edicts         = 36
sod_law_senate                   = 37
sod_law_absolute_monarchy        = 38
sod_law_elective_monarchy        = 39
sod_laws_begin                   = sod_law_village_fairs
sod_laws_end                     = 40
sod_law_category_villagers       = 1
sod_law_category_townspeople     = 2
sod_law_category_clergy          = 3
sod_law_category_nobility        = 4
sod_law_category_placeholder     = 99
sod_law_block_none               = 0
sod_law_block_invalid_law        = 1
sod_law_block_placeholder        = 2
sod_law_block_already_active     = 3
sod_law_block_capacity           = 4
sod_law_block_conflict           = 5
sod_law_block_missing_requirement = 6
sod_law_block_faction_ineligible = 7
sod_law_block_cooldown           = 8
sod_law_block_unrest             = 9
sod_law_ai_tag_economic          = 1
sod_law_ai_tag_military          = 2
sod_law_ai_tag_religious         = 4
sod_law_ai_tag_centralizing      = 8
sod_law_ai_tag_decentralizing    = 16
sod_law_ai_tag_populist          = 32
sod_law_ai_tag_aristocratic      = 64
sod_law_ai_tag_mercantile        = 128
sod_law_ai_tag_oppressive        = 256
sod_law_ai_tag_legitimizing      = 512
sod_law_ai_tag_destabilizing     = 1024
sod_law_ai_tag_expansionist      = 2048
sod_law_ai_tag_defensive         = 4096

# Native 1.011 engine flaw: bandit parties also absorb rescued prisoners and bloat (lords are already trimmed in trigger #131)
sod_bandit_party_bloat_max       = 120   # cap bandit/outlaw party size so they don't grow to 1000+

# Siege AI (trigger #27): assault vs retreat
sod_siege_assault_min_ratio      = 150   # attacker/defender strength ratio must exceed this (percent) to allow assault roll
sod_siege_retreat_ratio_base     = 200   # retreat roll uses max(0, this - strength_ratio) as chance

# castle_garrison_max             = 200   # when should garrisoning auto-stop
# town_garrison_max               = 350

castle_food_limit               =  1500  # how many units of food can be stored at this location to hold out during a siege
town_food_limit                 = 30000

chance_hero_party_gain_extra_xp = 75   # used to be 30
chance_garrison_gain_extra_xp   = 50   # used to be 10

recruited_lord_starting_funds   = 1000   # initial funds that a newly recruited lord starts with


########################################################
##  ITEM SLOTS             #############################
########################################################

slot_item_is_checked              = 0
slot_item_food_bonus              = 1
slot_item_book_reading_progress   = 2
slot_item_book_read               = 3
slot_item_intelligence_requirement= 4

########################################################
##  AGENT SLOTS            #############################
########################################################

slot_agent_target_entry_point     = 0
slot_agent_target_x_pos           = 1
slot_agent_target_y_pos           = 2
slot_agent_is_alive_before_retreat= 3
slot_agent_is_in_scripted_mode    = 4
slot_agent_is_not_reinforcement   = 5
slot_agent_tournament_point       = 6
slot_agent_arena_team_set         = 7
slot_agent_map_overlay_id         = 10
slot_agent_target_entry_point     = 11
slot_agent_duel_faith_rank        = 20
slot_agent_duel_speed_limit       = 21
slot_agent_duel_pressure          = 22

########################################################
##  FACTION SLOTS          #############################
########################################################
slot_faction_ai_state                 = 4
slot_faction_ai_object                = 5
slot_faction_ai_last_offensive_time   = 6
slot_faction_marshall                 = 7
slot_faction_ai_offensive_max_followers = 8

slot_faction_culture              = 9
slot_faction_leader               = 10
##slot_faction_vassal_of            = 11

slot_faction_number_of_parties    = 20
slot_faction_state                = 21

slot_faction_player_alarm         = 30
slot_faction_last_mercenary_offer_time = 31

slot_faction_tier_1_troop         = 41
slot_faction_tier_2_troop         = 42
slot_faction_tier_3_troop         = 43
slot_faction_tier_4_troop         = 44
slot_faction_tier_5_troop         = 45
slot_faction_deserter_troop       = 48
slot_faction_guard_troop          = 49
slot_faction_messenger_troop      = 50
slot_faction_prison_guard_troop   = 51
slot_faction_castle_guard_troop   = 52

slot_faction_has_rebellion_chance = 60


#Rebellion changes
#slot_faction_rebellion_target                     = 65
#slot_faction_inactive_leader_location         = 66
#slot_faction_support_base                     = 67
#Rebellion changes



#slot_faction_deserter_party_template       = 62

slot_faction_reinforcements_a        = 77
slot_faction_reinforcements_b        = 78
slot_faction_reinforcements_c        = 79

slot_faction_num_armies              = 80
slot_faction_num_castles             = 81
slot_faction_num_towns               = 82

# KUBA - MERC GUILDS
slot_guild_deliver_message_text = 85
slot_guild_fugitive_text = 86
slot_guild_troublesome_bandits_text = 87
slot_guild_raise_troops_text = 88
slot_guild_fight_troops_text = 89

slot_faction_merc_pact     = 91
slot_guild_representative  = 92
slot_guild_tier_1_unit_1    = 93
slot_guild_tier_1_unit_2    = 94
slot_guild_noble            = 95
slot_guild_troop_proportion = 96
slot_guild_master           = 97
slot_guild_base             = 98
slot_faction_sod_mercs      = 99
slot_faction_mercs_noble    = 100
slot_faction_upgrade_permission = 101
slot_faction_pact_broken_day = 102

# KUBA TITLES
slot_faction_ruler_title = 120
slot_faction_marshal_title = 121
slot_faction_t1_title = 122
slot_faction_t2_title = 123
slot_faction_t3_title = 124
slot_faction_t4_title = 125

slot_faction_center_transfer_option = 199 #in a slot to avoid to break saves

# TWAN TRUCE SLOTS
slot_faction_truce_player_realm = 200   # slots faction truce = 101-107
slot_faction_truce_kingdom_1 = 201 # use script get_truce_day (faction, faction) to get the value
slot_faction_truce_kingdom_2 = 202 # they store truce end date (peace date + 31 days)
slot_faction_truce_kingdom_3 = 203
slot_faction_truce_kingdom_4 = 204
slot_faction_truce_kingdom_5 = 205
slot_faction_truce_kingdom_6 = 206
faction_truce_slots_begin = slot_faction_truce_player_realm
faction_truce_slots_end = 207

# TWAN AI
slot_faction_council_day = 208
slot_faction_last_refused_peace = 209
slot_faction_last_started_war = 210
slot_faction_last_started_war_date = 211
slot_faction_power_evolution = 212
slot_faction_central_center = 213        
slot_faction_defensive_objective = 214    
slot_faction_offensive_objective = 215
slot_faction_ambition = 216
slot_faction_current_power = 217
slot_faction_last_week_power = 218
slot_faction_old_power = 219
slot_faction_economic_strength = 220
slot_faction_badboy_rating = 221 # only used for player faction actually
slot_faction_last_big_offensive = 222

slot_faction_intelligence_report_day = 223
slot_faction_intelligence_score = 224
slot_faction_intelligence_pressure = 225
slot_faction_intelligence_power_rank = 226
slot_faction_intelligence_growth = 227
slot_faction_intelligence_center_count = 228
slot_faction_intelligence_enemy_count = 229
slot_faction_intelligence_truce_count = 230
slot_faction_intelligence_marshal_present = 231
slot_faction_intelligence_vassal_count = 232

# Faction-wide realm law state. These slots intentionally live after the
# intelligence block so they do not collide with old save-era faction slots.
slot_faction_law_1 = 240
slot_faction_law_2 = 241
slot_faction_law_3 = 242
slot_faction_law_4 = 243
slot_faction_law_5 = 244
slot_faction_law_6 = 245
slot_faction_law_7 = 246
slot_faction_law_8 = 247
slot_faction_law_9 = 248
slot_faction_law_10 = 249
faction_laws_begin = slot_faction_law_1
faction_laws_end = 250
slot_faction_sod_laws_migrated = 250
slot_faction_sod_law_cooldown_day = 251
slot_faction_law_tax_peasants = 252
slot_faction_law_tax_townspeople = 253
slot_faction_law_tax_nobles = 254
slot_faction_law_village_population_modifier = 255
slot_faction_law_town_population_modifier = 256
slot_faction_law_village_faith_modifier = 257
slot_faction_law_town_faith_modifier = 258
slot_faction_law_demesne_modifier = 259
slot_faction_law_ruler_party_size_modifier = 260
slot_faction_law_lord_party_size_modifier = 261
slot_faction_law_holy_modifier = 262
slot_faction_law_noble_happiness = 263
slot_faction_law_clergy_happiness = 264
slot_faction_law_commoner_happiness = 265
slot_faction_law_merchant_happiness = 266
slot_faction_law_centralization = 267
slot_faction_law_militarization = 268
slot_faction_law_legitimacy = 269
slot_faction_law_unrest = 270
slot_faction_law_village_relation_modifier = 271
slot_faction_law_town_relation_modifier = 272
slot_faction_law_village_prosperity_modifier = 273
slot_faction_law_town_prosperity_modifier = 274

########################################################
##  PARTY SLOTS            #############################
########################################################
slot_party_type                = 0  #spt_caravan, spt_town, spt_castle

slot_party_retreat_flag        = 2
slot_party_ignore_player_until = 3
slot_party_ai_state            = 4
slot_party_ai_object           = 5

slot_town_belongs_to_kingdom   = 6
slot_town_lord                 = 7
slot_party_ai_substate         = 8
slot_town_claimed_by_player    = 9

slot_cattle_driven_by_player = slot_town_lord #hack

slot_town_center        = 10
slot_town_castle        = 11
slot_town_prison        = 12
slot_town_tavern        = 13
slot_town_store         = 14
slot_town_arena         = 16
slot_town_alley         = 17
slot_town_walls         = 18
slot_center_culture     = 19

slot_town_tavernkeeper  = 20
slot_town_weaponsmith   = 21
slot_town_armorer       = 22
slot_town_merchant      = 23
slot_town_horse_merchant= 24
slot_town_elder         = 25
slot_center_player_relation = 26
slot_town_player_relation = slot_center_player_relation

slot_center_siege_with_belfry = 27
slot_center_last_taken_by_troop = 28


# party will follow this party if set:
slot_party_commander_party = 30 #default -1
slot_party_following_player    = 31
slot_party_follow_player_until_time = 32
slot_party_dont_follow_player_until_time = 33

slot_village_raided_by        = 34
slot_village_state            = 35 #svs_normal, svs_being_raided, svs_looted, svs_recovering, svs_deserted
slot_village_raid_progress    = 36
slot_village_recover_progress = 37
slot_village_smoke_added      = 38

slot_village_infested_by_bandits   = 39

slot_center_last_player_alarm_hour = 42

slot_village_land_quality          = 44
slot_village_number_of_cattle      = 45
slot_village_player_can_not_steal_cattle = 46

slot_center_accumulated_rents      = 47
slot_center_accumulated_tariffs    = 48
slot_town_wealth        = 49
slot_town_prosperity    = 50
slot_town_player_odds   = 51


slot_party_last_toll_paid_hours = 52
slot_party_food_store           = 53 #used for sieges
slot_town_food_store = slot_party_food_store
slot_center_is_besieged_by      = 54 #used for sieges
slot_center_last_spotted_enemy  = 55

slot_party_cached_strength      = 56
slot_party_nearby_friend_strength = 57
slot_party_nearby_enemy_strength = 58
slot_party_follower_strength = 59

slot_town_reinforcement_party_template = 60
slot_center_original_faction      = 61
slot_center_ex_faction            = 62

slot_party_follow_me              = 63
slot_center_siege_begin_hours     = 64 #used for sieges
slot_center_siege_hardness        = 65

slot_town_mercs                   = 66



#slot_town_rebellion_contact   = 76
#trs_not_yet_approached  = 0
#trs_approached_before   = 1
#trs_approached_recently = 2

argument_none    = 0
argument_claim   = 1
argument_ruler   = 2
argument_benefit = 3
argument_victory = 4

slot_town_rebellion_readiness = 77
#(readiness can be a negative number if the rebellion has been defeated)

slot_town_arena_melee_mission_tpl = 78
slot_town_arena_torny_mission_tpl = 79
slot_town_arena_melee_1_num_teams = 80
slot_town_arena_melee_1_team_size = 81
slot_town_arena_melee_2_num_teams = 82
slot_town_arena_melee_2_team_size = 83
slot_town_arena_melee_3_num_teams = 84
slot_town_arena_melee_3_team_size = 85
slot_town_arena_melee_cur_tier    = 86
##slot_town_arena_template    = 87

slot_center_npc_volunteer_troop_type   = 90
slot_center_npc_volunteer_troop_amount = 91
slot_center_mercenary_troop_type  = 90
slot_center_mercenary_troop_amount= 91
slot_center_volunteer_troop_type  = 92
slot_center_volunteer_troop_amount= 93

#slot_center_companion_candidate   = 94
slot_center_ransom_broker         = 95
slot_center_tavern_traveler       = 96
slot_center_traveler_info_faction = 97
slot_center_tavern_bookseller     = 98
slot_center_tavern_minstrel       = 99

num_party_loot_slots    = 5
slot_party_next_looted_item_slot  = 109
slot_party_looted_item_1          = 110
slot_party_looted_item_2          = 111
slot_party_looted_item_3          = 112
slot_party_looted_item_4          = 113
slot_party_looted_item_5          = 114
slot_party_looted_item_1_modifier = 115
slot_party_looted_item_2_modifier = 116
slot_party_looted_item_3_modifier = 117
slot_party_looted_item_4_modifier = 118
slot_party_looted_item_5_modifier = 119

slot_village_bound_center         = 120
slot_village_market_town          = 121
slot_village_farmer_party         = 122
slot_party_home_center            = 123

slot_center_current_improvement   = 124
slot_center_improvement_end_hour  = 125

slot_center_has_manor            = 130 #village
slot_center_has_mill             = 131 #village
slot_center_has_watch_tower      = 132 #village
slot_center_has_inn              = 133 #village

#slot_center_has_fish_pond        = 131 #village - same as mill!!!
#slot_center_has_school           = 133 #village - same as inn!!!

#SoD BUILDINGS BEGIN
slot_center_has_shrine = 134
slot_center_has_monastery = 135
slot_center_has_temple = 136      #town
slot_center_has_chapel = 137       #castle
slot_center_has_barracks = 138      #town, castle
slot_center_has_range = 139         #town, castle
slot_center_has_stables = 140        #town, castle
slot_center_has_chapter = 141        #castle
slot_center_has_blacksmith = 142      #castle, town

slot_center_has_messenger_post   = 143 #town, castle, village
slot_center_has_prisoner_tower   = 144 #town, castle

slot_center_has_guild = 145           #town
slot_center_has_university = 146      #town
slot_center_has_hospital = 147        #town
slot_center_has_canalization = 148    #town
slot_center_has_manufacture = 149     #town
slot_center_has_bank = 150            #town

slot_center_has_ambulatory = 151          #village
slot_center_has_water_supply = 152         #village
slot_center_has_clayworks = 153           #village
slot_center_has_rustic_blacksmith = 154   #village
#SoD BUILDINGS END

village_improvements_begin = slot_center_has_manor
village_improvements_end = slot_center_has_messenger_post+1

walled_center_improvements_begin = slot_center_has_messenger_post
walled_center_improvements_end = slot_center_has_university+1

#SoD Faith
slot_center_sod_local_faith = 245
#SoD Population
slot_center_sod_local_population = 246
slot_center_sod_local_health = 247
slot_center_sod_local_prosperity = 248
slot_center_health = slot_center_sod_local_health

slot_center_has_bandits                        = 249
slot_town_has_tournament                     = 250
slot_town_tournament_max_teams               = 251
slot_town_tournament_max_team_size           = 252

slot_center_faction_when_oath_renounced      = 255

slot_center_walker_0_troop                   = 260
slot_center_walker_1_troop                   = 261
slot_center_walker_2_troop                   = 262
slot_center_walker_3_troop                   = 263
slot_center_walker_4_troop                   = 264
slot_center_walker_5_troop                   = 265
slot_center_walker_6_troop                   = 266
slot_center_walker_7_troop                   = 267
slot_center_walker_8_troop                   = 268
slot_center_walker_9_troop                   = 269

slot_center_walker_0_dna                     = 270
slot_center_walker_1_dna                     = 271
slot_center_walker_2_dna                     = 272
slot_center_walker_3_dna                     = 273
slot_center_walker_4_dna                     = 274
slot_center_walker_5_dna                     = 275
slot_center_walker_6_dna                     = 276
slot_center_walker_7_dna                     = 277
slot_center_walker_8_dna                     = 278
slot_center_walker_9_dna                     = 279

slot_center_walker_0_type                    = 280
slot_center_walker_1_type                    = 281
slot_center_walker_2_type                    = 282
slot_center_walker_3_type                    = 283
slot_center_walker_4_type                    = 284
slot_center_walker_5_type                    = 285
slot_center_walker_6_type                    = 286
slot_center_walker_7_type                    = 287
slot_center_walker_8_type                    = 288
slot_center_walker_9_type                    = 289

slot_town_trade_route_1           = 290
slot_town_trade_route_2           = 291
slot_town_trade_route_3           = 292
slot_town_trade_route_4           = 293
slot_town_trade_route_5           = 294
slot_town_trade_route_6           = 295
slot_town_trade_route_7           = 296
slot_town_trade_route_8           = 297
slot_town_trade_route_9           = 298
slot_town_trade_route_10          = 299
slot_town_trade_route_11          = 300
slot_town_trade_route_12          = 301
slot_town_trade_route_13          = 302
slot_town_trade_route_14          = 303
slot_town_trade_route_15          = 304
slot_town_trade_routes_begin = slot_town_trade_route_1
slot_town_trade_routes_end = slot_town_trade_route_15 + 1





slot_party_merc_contract = 306   # KUBA SLOTS
slot_party_merc_asked    = 307
slot_party_leader        = 308
slot_party_boss          = 309
slot_party_starting_size = 310
slot_party_starting_base = 311
slot_party_caravan_trade_profit = 312
slot_party_caravan_upgrade_tier = 313

slot_party_orginal_faction = 320
slot_center_guard_0_troop = 321
slot_center_guard_1_troop = 322
slot_center_guard_2_troop = 323
slot_center_guard_3_troop = 324
slot_center_guard_4_troop = 325
slot_center_guard_5_troop = 326
slot_center_guard_6_troop = 327
slot_center_guard_7_troop = 328
slot_center_guard_8_troop = 329
slot_castle_exterior    = slot_town_center


slot_center_trainers = 330
slot_center_max_garrison = 331
slot_center_garrison_soldiers = 332
slot_center_garrison_ranged = 333
slot_town_slavers = 334  
slot_party_slaves_fleed = 335
slot_party_old_x = 336
slot_party_old_y = 337
slot_town_fgtq = 338

# Regional threat board parties. Kept below trade-good party slots.
slot_party_sod_threat_type = 340
slot_party_sod_threat_tier = 341
slot_party_sod_threat_sponsor_center = 342
slot_party_sod_threat_sponsor_faction = 343
slot_party_sod_threat_expiration_day = 344
slot_party_sod_threat_reward_seed = 345
slot_party_sod_threat_active_quest = 346
slot_party_sod_threat_archetype = 347

# KUBA SLOTS END

num_trade_goods = itm_tools+1 - itm_smoked_fish
slot_town_trade_good_productions_begin       = 400
slot_town_trade_good_prices_begin            = slot_town_trade_good_productions_begin + num_trade_goods + 1


#slot_party_type values
##spt_caravan            = 1
spt_castle             = 2
spt_town               = 3
spt_village            = 4
##spt_forager            = 5
##spt_war_party          = 6
##spt_patrol             = 7
##spt_messenger          = 8
##spt_raider             = 9
##spt_scout              = 10
spt_kingdom_caravan    = 11
##spt_prisoner_train     = 12
spt_kingdom_hero_party = 13
##spt_merchant_caravan   = 14
spt_village_farmer     = 15
spt_ship               = 16
spt_cattle_herd        = 17
#spt_deserter           = 20
spt_ai_mercenaries     = 18
spt_player_mercenaries = 19
spt_player_patrol      = 20
spt_merc_base          = 21

kingdom_party_types_begin = spt_kingdom_caravan
kingdom_party_types_end = spt_kingdom_hero_party + 1

#slot_faction_state values
sfs_active                     = 0
sfs_defeated                   = 1
sfs_inactive                   = 2
sfs_inactive_rebellion         = 3
sfs_beginning_rebellion        = 4


#slot_faction_ai_state values
sfai_default                   = 0
sfai_gathering_army            = 1
sfai_attacking_center          = 2
sfai_raiding_village           = 3
sfai_attacking_enemy_army      = 4
sfai_attacking_enemies_around_center = 5
#Rebellion system changes begin
sfai_nascent_rebellion          = 6
#Rebellion system changes end

#slot_party_ai_state values
spai_undefined                  = -1
spai_besieging_center           = 1
spai_patrolling_around_center   = 4
spai_raiding_around_center      = 5
##spai_raiding_village            = 6
spai_holding_center             = 7
##spai_helping_town_against_siege = 9
spai_engaging_army              = 10
spai_accompanying_army          = 11
spai_trading_with_town          = 13
spai_retreating_to_center       = 14
##spai_trading_within_kingdom     = 15
spai_recruiting_troops          = 16

#slot_village_state values
svs_normal                      = 0
svs_being_raided                = 1
svs_looted                      = 2
svs_recovering                  = 3
svs_deserted                    = 4
svs_under_siege                 = 5

#$g_player_icon_state values
pis_normal                      = 0
pis_camping                     = 1
pis_ship                        = 2


########################################################
##  SCENE SLOTS            #############################
########################################################
slot_scene_visited              = 0
slot_scene_belfry_props_begin   = 10


########################################################
##  TROOP SLOTS            #############################
########################################################
#slot_troop_role         = 0  # 10=Kingdom Lord

slot_troop_occupation          = 2  # 0 = free, 1 = merchant
slot_troop_state               = 3
slot_troop_last_talk_time      = 4
slot_troop_met                 = 5
slot_troop_party_template      = 6
slot_troop_renown              = 7
slot_troop_prisoner_of_party   = 8  # important for heroes only
#slot_troop_is_player_companion = 9  # important for heroes only:::USE  slot_troop_occupation = slto_player_companion

slot_troop_leaded_party        = 10 # important for kingdom heroes only
slot_troop_wealth              = 11 # important for kingdom heroes only
slot_troop_cur_center          = 12 # important for royal family members only (non-kingdom heroes)
slot_troop_banner_scene_prop   = 13 # important for kingdom heroes and player only
slot_troop_original_faction    = 14 # for pretenders
slot_troop_loyalty              = 15
slot_troop_player_order_state   = 16
slot_troop_player_order_object  = 17

#slot_troop_present_at_event    = 19 #defined below
slot_troop_does_not_give_quest = 20
slot_troop_player_debt         = 21
slot_troop_player_relation     = 22 # raw value, for cooked -> script_troop_get_player_relation
#slot_troop_player_favor        = 23
slot_troop_last_quest          = 24
slot_troop_last_quest_betrayed = 25
slot_troop_last_persuasion_time= 26
slot_troop_last_comment_time   = 27
slot_troop_spawned_before      = 28

#Post 0907 changes begin
slot_troop_last_comment_slot   = 29
slot_troop_present_at_event    = 19
#Post 0907 changes end

slot_troop_spouse              = 30
slot_troop_father              = 31
slot_troop_mother              = 32
slot_troop_daughter            = 33
slot_troop_son                 = 34
slot_troop_sibling             = 35
slot_troop_lover               = 36

slot_troop_trainer_met                       = 30
slot_troop_trainer_waiting_for_result        = 31
slot_troop_trainer_training_fight_won        = 32
slot_troop_trainer_num_opponents_to_beat     = 33
slot_troop_trainer_training_system_explained = 34
slot_troop_trainer_opponent_troop            = 35
slot_troop_trainer_training_difficulty       = 36
slot_troop_trainer_training_fight_won        = 37


slot_troop_family_begin        = 30
slot_troop_family_end          = 36

slot_troop_enemy_1             = 40
slot_troop_enemy_2             = 41
slot_troop_enemy_3             = 42
slot_troop_enemy_4             = 43
slot_troop_enemy_5             = 44

slot_troop_enemies_begin       = 40
slot_troop_enemies_end         = 45

slot_troop_honorable          = 50
#slot_troop_merciful          = 51
slot_lord_reputation_type     = 52

slot_troop_change_to_faction          = 55
slot_troop_readiness_to_join_army     = 57
slot_troop_readiness_to_follow_orders = 58

# NPC-related constants

#NPC companion changes begin
slot_troop_first_encountered          = 59
slot_troop_home                       = 60

slot_troop_morality_state       = 61
tms_no_problem         = 0
tms_acknowledged       = 1
tms_dismissed          = 2

slot_troop_morality_type = 62
tmt_aristocratic = 1
tmt_egalitarian = 2
tmt_humanitarian = 3
tmt_honest = 4
tmt_pious = 5

slot_troop_morality_value = 63

slot_troop_2ary_morality_type  = 64
slot_troop_2ary_morality_state = 65
slot_troop_2ary_morality_value = 66

slot_troop_morality_penalties =  69 ### accumulated grievances from morality conflicts


slot_troop_personalityclash_object     = 71
#(0 - they have no problem, 1 - they have a problem)
slot_troop_personalityclash_state    = 72 #1 = pclash_penalty_to_self, 2 = pclash_penalty_to_other, 3 = pclash_penalty_to_other,
pclash_penalty_to_self  = 1
pclash_penalty_to_other = 2
pclash_penalty_to_both  = 3
#(a string)
slot_troop_personalityclash2_object   = 73
slot_troop_personalityclash2_state    = 74

slot_troop_personalitymatch_object   =  75
slot_troop_personalitymatch_state   =  76

slot_troop_personalityclash_penalties = 77 ### accumulated grievances from personality clash

slot_troop_home_speech_delivered = 78
slot_troop_companion_cohesion = 79
slot_troop_companion_grievance = 18

COMPANION_COHESION_WEAK = 20
COMPANION_COHESION_NEUTRAL = 50
COMPANION_COHESION_STRONG = 80
COMPANION_GRIEVANCE_LOW = 30
COMPANION_GRIEVANCE_HIGH = 80

#NPC history slots

slot_troop_met_previously        = 80
slot_troop_turned_down_twice     = 81
slot_troop_playerparty_history   = 82

pp_history_scattered         = 1
pp_history_dismissed         = 2
pp_history_quit              = 3
pp_history_indeterminate     = 4

slot_troop_playerparty_history_string   = 83
slot_troop_return_renown        = 84

slot_troop_custom_banner_bg_color_1      = 85
slot_troop_custom_banner_bg_color_2      = 86
slot_troop_custom_banner_charge_color_1  = 87
slot_troop_custom_banner_charge_color_2  = 88
slot_troop_custom_banner_charge_color_3  = 89
slot_troop_custom_banner_charge_color_4  = 90
slot_troop_custom_banner_bg_type         = 91
slot_troop_custom_banner_charge_type_1   = 92
slot_troop_custom_banner_charge_type_2   = 93
slot_troop_custom_banner_charge_type_3   = 94
slot_troop_custom_banner_charge_type_4   = 95
slot_troop_custom_banner_flag_type       = 96
slot_troop_custom_banner_num_charges     = 97
slot_troop_custom_banner_positioning     = 98
slot_troop_custom_banner_map_flag_type   = 99

#conversation strings -- must be in this order!
slot_troop_intro = 101

slot_troop_intro_response_1 = 102
slot_troop_intro_response_2 = 103

slot_troop_backstory_a = 104
slot_troop_backstory_b = 105
slot_troop_backstory_c = 106

slot_troop_backstory_delayed = 107

slot_troop_backstory_response_1 = 108
slot_troop_backstory_response_2 = 109

slot_troop_signup   = 110
slot_troop_signup_2 = 111

slot_troop_signup_response_1 = 112
slot_troop_signup_response_2 = 113

slot_troop_mentions_payment = 114 #Not actually used
slot_troop_payment_response = 115 #Not actually used
slot_troop_morality_speech   = 116
slot_troop_2ary_morality_speech = 117
slot_troop_personalityclash_speech = 118
slot_troop_personalityclash_speech_b = 119
slot_troop_personalityclash2_speech = 120
slot_troop_personalityclash2_speech_b = 121
slot_troop_personalitymatch_speech = 122
slot_troop_personalitymatch_speech_b = 123
slot_troop_retirement_speech = 124
slot_troop_rehire_speech = 125
slot_troop_home_intro           = 126
slot_troop_home_description    = 127
slot_troop_home_description_2 = 128
slot_troop_home_recap         = 129
slot_troop_honorific   = 130
slot_troop_strings_end = 131
slot_troop_payment_request = 132

#Rebellion changes begin
slot_troop_discussed_rebellion = 140
slot_troop_support_base = 141
#Rebellion changes end

#MORDACHAI - to allow use of Leprechaun's prisoner text
slot_prisoner_agreed = 142
slot_prisoner_rejected_day = 143

#MORDACHAI - allow Lords to offer their allegience to the player
slot_lord_allegience_offered = 144
lao_never = 0
lao_offering = 1
lao_accepted = 2
lao_rejected = 3

#MORDACHAI - track when an NPC levels up
slot_troop_level_up         = 145

#MORDACHAI - TEMP - JUST TO FIX THE DUPLICATE HERO BUG
troop_slot_instances        = 146

#MORDACHAI - Autoloot - flag whether this unit should try to restict their upgrades to mount-compatible items only
slot_troop_restrict_mounted = 147

#AUTOLOOT - These are troops slots
slot_troop_upgrade_armor    = 153
slot_troop_upgrade_horse    = 154
slot_troop_upgrade_wpn_0    = 157
slot_troop_upgrade_wpn_1    = 158
slot_troop_upgrade_wpn_2    = 159
slot_troop_upgrade_wpn_3    = 160

#MORDACHAI - slots to hold a copy of what the companion had equipped prior to auto-looting, so we can tell what changed
slot_troop_item_0         = 162
slot_troop_item_1         = 163
slot_troop_item_2         = 164
slot_troop_item_3         = 165
slot_troop_head           = 166
slot_troop_body           = 167
slot_troop_foot           = 168
slot_troop_gloves         = 169
slot_troop_horse          = 170
slot_troop_item_0_imod    = 171
slot_troop_item_1_imod    = 172
slot_troop_item_2_imod    = 173
slot_troop_item_3_imod    = 174
slot_troop_head_imod      = 175
slot_troop_body_imod      = 176
slot_troop_foot_imod      = 177
slot_troop_gloves_imod    = 178
slot_troop_horse_imod     = 179

#SoD Courtiers (records which town we're in, when we're talking to the given troop)
slot_troop_sod_court      = 180

#SoD ARMY MANAGEMENT BEGIN
slot_troop_sod_upgrade1   = 190
slot_troop_sod_upgrade2   = 191
slot_troop_sod_soldier    = 192
slot_troop_sod_upgrades   = 193
slot_troop_sod_doctrine_role = 194
slot_troop_sod_doctrine_tier = 195
slot_troop_sod_doctrine_facility = 196
slot_troop_sod_doctrine_flags = 197
slot_troop_sod_doctrine_cost_mult = 198
slot_troop_sod_doctrine_faith_upgrade = 199
#SoD ARMY MANAGEMENT END

sod_doctrine_role_unknown = 0
sod_doctrine_role_infantry = 1
sod_doctrine_role_ranged = 2
sod_doctrine_role_mounted = 3
sod_doctrine_role_noble = 4
sod_doctrine_role_faith = 5

sod_elite_tier_common = 0
sod_elite_tier_regular = 1
sod_elite_tier_veteran = 2
sod_elite_tier_elite = 3
sod_elite_tier_noble = 4
sod_elite_tier_faith = 5

sod_doctrine_facility_none = 0
sod_doctrine_facility_barracks = 1
sod_doctrine_facility_range = 2
sod_doctrine_facility_stables = 3
sod_doctrine_facility_chapter = 4
sod_doctrine_facility_temple = 5

sod_doctrine_flag_noble = 1
sod_doctrine_flag_faith = 2
sod_doctrine_flag_mercenary = 4
sod_doctrine_flag_commoner = 8

sod_upgrade_fail_none = 0
sod_upgrade_fail_not_sod = 1
sod_upgrade_fail_no_center = 2
sod_upgrade_fail_missing_facility = 3
sod_upgrade_fail_wrong_faction = 4
sod_upgrade_fail_blocked_troop = 5
sod_upgrade_fail_merc_permission = 6
sod_upgrade_fail_low_faith = 7

slot_troop_sod_doctrine_culture = 234
slot_troop_sod_doctrine_faction = 235
slot_troop_sod_doctrine_special_req = 236

sod_special_req_none = 0
sod_special_req_chapter = 1
sod_special_req_faith_ascension = 2
sod_special_req_merc_permission = 3


# SOD TWAN USED BY KT0 AUTORESOLVE SYSTEM (I've moved some slots to keep the numbers he given)
kt_slot_troop_1hprof = 200
kt_slot_troop_2hprof = 201
kt_slot_troop_poleprof = 202
kt_slot_troop_archprof = 203
kt_slot_troop_xbowprof = 204
kt_slot_troop_thrwprof = 205
kt_slot_troop_str = 206
kt_slot_troop_agi = 207
kt_slot_troop_int = 208
kt_slot_troop_cha = 209
kt_slot_troop_pstrike = 210
kt_slot_troop_pdraw = 211
kt_slot_troop_pthrow = 212
kt_slot_troop_shield = 213
kt_slot_troop_atheltics = 214
kt_slot_troop_ironflesh = 215
kt_slot_troop_o_val = 230
kt_slot_troop_d_val = 231
kt_slot_troop_h_val = 232
kt_slot_troop_type = 233

# SOD TWAN LORDS AI
slot_lord_raiding_factor = 250  
slot_lord_interception_factor = 251 
slot_lord_initiative = 252
slot_lord_personnal_objective = 253
slot_lord_self_confidence = 254  
slot_lord_pursuit_state = 255 #obsolete
slot_lord_ai_timer = 255


# KUBA SLOTS
slot_troop_merc_bought = 260
slot_troop_title       = 261
slot_troop_mercenaries = 262
slot_troop_d_leader    = 263
slot_troop_death_day   = 264
slot_troop_max_title   = 265
slot_troop_pretender   = 266
slot_root_troop = 267 
slot_troop_daily_quest = 268

# Centurion's personalities
slot_troop_centurion_personality = 270
slot_troop_sod_quest_memory_state = 271
slot_troop_sod_quest_memory_stage = 272
slot_troop_sod_quest_memory_chain = 273
slot_troop_sod_quest_memory_event = 274
slot_troop_sod_quest_memory_quest = 275
slot_troop_sod_quest_memory_day = 276
slot_troop_sod_quest_memory_actor = 277
slot_troop_sod_quest_memory_outcome = 278
slot_troop_sod_quest_memory_relation_delta = 279
slot_troop_sod_quest_memory_interactions = 280
slot_troop_sod_quest_memory_battle_action = 281
slot_troop_sod_quest_memory_summary = 282

slcp_sane = 1
slcp_respectful = 2
slcp_imperialist = 3
slcp_capitalist = 4
slcp_racist = 5
slcp_crusader = 6
slcp_liberator = 7
slcp_nihilistic = 8

# kt_slot_troop_type values
kt_troop_type_footsoldier = 0   # !tf_guarantee_horse AND !tf_guarantee_ranged
kt_troop_type_cavalry = 1      # !tf_guarantee_ranged AND tf_guarantee_horse
kt_troop_type_archer = 2      # tf_guarantee_ranged AND !tf_guarnatee_horse
kt_troop_type_mtdarcher = 3   # tf_guarantee_ranged AND tf_guarantee_horse

###################################################################################
# AutoLoot: Modified Constants
# Most of these are slot definitions, make sure they do not clash with your mod's other slot usage
# Autoloot improved by rubik
###################################################################################

auto_loot_version = 2     # increment this when you want to force autoloot to reinitialize itself for saved games

# this is the number of heros that appear as menu options on the autoloot menu per page
# NOTE: you must actually modify the source code in order to change this! (Its a goofy thing to have as a constant)
num_loot_management_menu_heroes = 4

# This is an item slot
slot_item_difficulty = 5

# armor
slot_item_head_armor      = 6
slot_item_body_armor      = 7
slot_item_leg_armor       = 8

# weapons
slot_item_cant_use_on_horseback = 6
slot_item_thrust_damage         = 7
slot_item_swing_damage          = 8
slot_item_thrust_damage_type    = 9
slot_item_swing_damage_type     = 10
slot_item_weapon_speed          = 11

# shields
#slot_item_cant_use_on_horseback = 6  # we use this for shields too
slot_item_shield_size     = 7
slot_item_shield_armor    = 8

# horses
slot_item_horse_speed     = 6
slot_item_horse_armor     = 7
slot_item_horse_charge    = 8

# MORDACHAI - further extensions to Autoloot

# damage types
idt_cut      = 0
idt_pierce   = 1
idt_blunt    = 2

# imod slots are really item slots!!!
# WARNING: do not let them overlap with any slot_item_xxx definition, or you will be sorry!
slot_item_imod_cost          =   100
slot_item_imod_require       =   101
slot_item_imod_speed         =   102
slot_item_imod_armor         =   103
slot_item_imod_damage        =   104

# Grounded royal artifact ecosystem. Keep above native/autoloot item slots.
slot_item_artifact_flags             = 160
slot_item_artifact_family            = 161
slot_item_artifact_tier              = 162
slot_item_artifact_provenance_rank   = 163
slot_item_artifact_technique_flags   = 164
slot_item_artifact_original_owner    = 165
slot_item_artifact_current_owner     = 166
slot_item_artifact_last_modifier     = 167
slot_item_artifact_set_piece         = 168

slot_item_artifact_progress_begin    = 180 # 8 modifier blocks, 3 slots each: kills, milestone, owner
artifact_progress_stride             = 3
artifact_modifier_blocks             = 8

artifact_flag_royal                  = 1
artifact_flag_weapon                 = 2
artifact_flag_set_piece              = 4
artifact_flag_bounty_reward          = 8

artifact_family_none                 = 0
artifact_family_antarian             = 1
artifact_family_marinian             = 2
artifact_family_adenian              = 3
artifact_family_villianese           = 4
artifact_family_zerrikanian          = 5
artifact_family_bounty_outlaw        = 6

artifact_piece_helm                  = 1
artifact_piece_body                  = 2
artifact_piece_boots                 = 3
artifact_piece_gloves                = 4
artifact_piece_weapon                = 5
artifact_piece_shield                = 6
artifact_piece_horse                 = 7
artifact_piece_ammo                  = 8

artifact_tech_folded_steel           = 1
artifact_tech_perfect_balance        = 2
artifact_tech_hardened_point         = 4
artifact_tech_reinforced_haft        = 8
artifact_tech_engraved_grip          = 16

###################################################################################
# End Autoloot
###################################################################################

# character backgrounds
cb_antares = 1
cb_marina = 2
cb_aden = 3
cb_villian = 4
cb_zerrikan = 5

cb_the_one = 1
cb_old_gods = 2
cb_the_void = 3
cb_enlightenment  = 4
cb_atheism = 5

cb3_merchant = 1
cb3_intrigues = 2
cb3_tourneys = 3
cb3_philosophy = 4

cb4_revenge = 1
cb4_peace    = 2
cb4_bloodlust =  3
cb4_riches  = 4

#NPC system changes end
#Encounter types
enctype_fighting_against_village_raid = 1
enctype_catched_during_village_raid   = 2


### Troop occupations slot_troop_occupation
##slto_merchant           = 1
slto_kingdom_hero       = 2
slto_player_companion   = 3
slto_kingdom_lady       = 4
slto_kingdom_seneschal  = 5
slto_robber_knight      = 6
slto_mercenary_lord = 15

#MORDACHAI - Prisoner Dialog (execute a prisoner)
slto_dead               = 86

stl_unassigned          = -1
stl_reserved_for_player = -2
stl_rejected_by_player  = -3

#NPC changes begin
slto_retirement      = 11
#slto_retirement_medium    = 12
#slto_retirement_short     = 13
#NPC changes end

# KUBA troop titles
stt_none     = 0
stt_king   	 = 1
stt_marshall = 2
stt_knight   = 3
stt_baron    = 4
stt_viscount = 5
stt_count    = 6
stt_margrave = 7
stt_duke     = 8
stt_infante  = 9
stt_prince   = 10
stt_titles_end = 11

########################################################
##  QUEST SLOTS            #############################
########################################################

slot_quest_target_center            = 1
slot_quest_target_troop             = 2
slot_quest_target_faction           = 3
slot_quest_object_troop             = 4
##slot_quest_target_troop_is_prisoner = 5
slot_quest_giver_troop              = 6
slot_quest_object_center            = 7
slot_quest_target_party             = 8
slot_quest_target_party_template    = 9
slot_quest_target_amount            = 10
slot_quest_current_state            = 11
slot_quest_giver_center             = 12
slot_quest_target_dna               = 13
slot_quest_target_item              = 14
slot_quest_object_faction           = 15

slot_quest_convince_value           = 19
slot_quest_importance               = 20
slot_quest_xp_reward                = 21
slot_quest_gold_reward              = 22
slot_quest_expiration_days          = 23
slot_quest_dont_give_again_period   = 24
slot_quest_dont_give_again_remaining_days = 25
slot_quest_bandits_eliminated_by_player = 26  #kuba
slot_quest_rounds_completed = 27
slot_quest_num_rounds = 28
slot_quest_apply = 29
slot_quest_yes = 30
slot_quest_no = 31
slot_quest_r1 = 32
slot_quest_rounds_won = 33
slot_quest_denial = 44
slot_quest_o2 = 45

# Regional threat board contract state.
slot_quest_sod_threat_type = 46
slot_quest_sod_threat_tier = 47
slot_quest_sod_threat_archetype = 48
slot_quest_sod_threat_target_party = 49
slot_quest_sod_threat_sponsor_center = 50
slot_quest_sod_threat_sponsor_faction = 51
slot_quest_sod_threat_reward_gold = 52
slot_quest_sod_threat_reward_relation = 53
slot_quest_sod_threat_deadline_day = 54
slot_quest_sod_threat_ready_to_claim = 55
slot_quest_sod_threat_reward_xp = 56
slot_quest_sod_threat_offer_1 = 57
slot_quest_sod_threat_offer_2 = 58
slot_quest_sod_threat_offer_3 = 59

# Structured quest runtime adapter state.
slot_quest_sod_runtime_state = 60
slot_quest_sod_runtime_stage = 61
slot_quest_sod_runtime_template = 62
slot_quest_sod_runtime_chain = 63
slot_quest_sod_runtime_flags = 64
slot_quest_sod_runtime_last_event = 65
slot_quest_sod_runtime_last_actor = 66
slot_quest_sod_runtime_last_party = 67
slot_quest_sod_runtime_last_center = 68
slot_quest_sod_runtime_last_day = 69
slot_quest_sod_runtime_progress = 70
slot_quest_sod_runtime_target = 71
slot_quest_sod_runtime_metadata = 72
slot_quest_sod_battle_action = 73
slot_quest_sod_battle_target_troop = 74
slot_quest_sod_battle_target_party = 75
slot_quest_sod_battle_required = 76
slot_quest_sod_battle_progress = 77
slot_quest_sod_battle_timer_start = 78
slot_quest_sod_battle_timer_duration = 79
slot_quest_sod_battle_flags = 80
slot_quest_sod_journal_flags = 81
slot_quest_sod_journal_priority = 82
slot_quest_sod_journal_chain_progress = 83
slot_quest_sod_journal_stage_progress = 84
slot_quest_sod_journal_category = 85
slot_quest_sod_journal_archive_day = 86
slot_quest_sod_journal_sort_key = 87
slot_quest_sod_chain_id = 88
slot_quest_sod_chain_step = 89
slot_quest_sod_chain_branch = 90
slot_quest_sod_chain_choice = 91
slot_quest_sod_chain_lock_state = 92
slot_quest_sod_chain_resume_day = 93
slot_quest_sod_chain_ending = 94
slot_quest_sod_chain_flags = 95
slot_quest_sod_chain_next_quest = 96
slot_quest_sod_chain_previous_quest = 97
slot_quest_sod_reward_gold = 98
slot_quest_sod_reward_xp = 99
slot_quest_sod_reward_relation_troop = 100
slot_quest_sod_reward_relation_troop_value = 101
slot_quest_sod_reward_faction = 102
slot_quest_sod_reward_faction_value = 103
slot_quest_sod_reward_center = 104
slot_quest_sod_reward_center_value = 105
slot_quest_sod_reward_renown = 106
slot_quest_sod_reward_honor = 107
slot_quest_sod_reward_troop = 108
slot_quest_sod_reward_troop_amount = 109
slot_quest_sod_reward_item = 110
slot_quest_sod_reward_item_modifier = 111
slot_quest_sod_reward_prisoner = 112
slot_quest_sod_reward_prisoner_amount = 113
slot_quest_sod_reward_access_flags = 114
slot_quest_sod_reward_title = 115
slot_quest_sod_reward_discount = 116
slot_quest_sod_reward_followup_quest = 117
slot_quest_sod_reward_world_center = 118
slot_quest_sod_reward_world_prosperity = 119
slot_quest_sod_consequence_reputation = 120
slot_quest_sod_consequence_regional_instability = 121
slot_quest_sod_consequence_lockout_days = 122
slot_quest_sod_outcome_flags = 123
slot_quest_sod_outcome_applied = 124

sod_quest_state_inactive = 0
sod_quest_state_offered = 1
sod_quest_state_accepted = 2
sod_quest_state_active = 3
sod_quest_state_paused = 4
sod_quest_state_stage_complete = 5
sod_quest_state_completed = 6
sod_quest_state_failed = 7
sod_quest_state_aborted = 8
sod_quest_state_expired = 9
sod_quest_state_hidden = 10
sod_quest_state_locked = 11
sod_quest_state_revealed = 12

sod_quest_event_none = 0
sod_quest_event_accept = 1
sod_quest_event_update = 2
sod_quest_event_complete = 3
sod_quest_event_fail = 4
sod_quest_event_abort = 5
sod_quest_event_stage_enter = 6
sod_quest_event_stage_complete = 7
sod_quest_event_battle_start = 8
sod_quest_event_battle_update = 9
sod_quest_event_battle_end = 10
sod_quest_event_map_conversation = 11
sod_quest_event_camp_conversation = 12
sod_quest_event_dialogue = 13
sod_quest_event_mission = 14
sod_quest_event_trigger = 15
sod_quest_event_battle = 16
sod_quest_event_map_encounter = 17
sod_quest_event_center_visit = 18
sod_quest_event_party_movement = 19
sod_quest_event_time_passed = 20
sod_quest_event_agent_defeated = 21
sod_quest_event_prisoner_freed = 22
sod_quest_event_wave_progress = 23
sod_quest_event_position_held = 24

sod_quest_battle_action_none = 0
sod_quest_battle_action_kill_target = 1
sod_quest_battle_action_capture_target = 2
sod_quest_battle_action_protect_target = 3
sod_quest_battle_action_survive_timer = 4
sod_quest_battle_action_break_siege_line = 5
sod_quest_battle_action_hold_position = 6
sod_quest_battle_action_destroy_force = 7
sod_quest_battle_action_escort_during_battle = 8
sod_quest_battle_action_free_prisoner = 9
sod_quest_battle_action_rescue_allied_captain = 10
sod_quest_battle_action_defeat_wave = 11

sod_quest_journal_capacity_default = 8
sod_quest_journal_flag_pinned = 1
sod_quest_journal_flag_main = 2
sod_quest_journal_flag_side = 4
sod_quest_journal_flag_urgent = 8
sod_quest_journal_flag_archived = 16

sod_quest_journal_category_unknown = 0
sod_quest_journal_category_main = 1
sod_quest_journal_category_side = 2
sod_quest_journal_category_urgent = 3
sod_quest_journal_category_completed = 4
sod_quest_journal_category_failed = 5
# Compatibility buckets used by the quest journal report for live active-log grouping.
sod_quest_journal_category_active = 6
sod_quest_journal_category_pinned = 7

sod_quest_chain_branch_none = 0
sod_quest_chain_branch_success = 1
sod_quest_chain_branch_failure = 2
sod_quest_chain_branch_choice = 3
sod_quest_chain_branch_faction = 4
sod_quest_chain_branch_hidden = 5
sod_quest_chain_branch_alternate_ending = 6

sod_quest_chain_lock_none = 0
sod_quest_chain_lock_locked = 1
sod_quest_chain_lock_resuming = 2
sod_quest_chain_lock_completed = 3
sod_quest_chain_lock_failed = 4

sod_quest_chain_flag_hidden_unlocked = 1
sod_quest_chain_flag_resettable = 2
sod_quest_chain_flag_lockout = 4
sod_quest_chain_flag_resume_pending = 8

sod_quest_outcome_flag_reward_configured = 1
sod_quest_outcome_flag_consequence_configured = 2
sod_quest_outcome_flag_world_change = 4
sod_quest_outcome_flag_followup = 8
sod_quest_outcome_flag_access_unlock = 16

sod_threat_type_none = 0
sod_threat_type_pirates = 1
sod_threat_type_deserters = 2
sod_threat_type_relic_thieves = 3
sod_threat_type_rogue_company = 4
sod_threat_type_cattle_raiders = 5
sod_threat_type_faction_problem = 6

sod_threat_archetype_river_pirates = 1
sod_threat_archetype_coastal_smugglers = 2
sod_threat_archetype_army_deserters = 3
sod_threat_archetype_noble_deserters = 4
sod_threat_archetype_relic_thieves = 5
sod_threat_archetype_tomb_robbers = 6
sod_threat_archetype_rogue_company = 7
sod_threat_archetype_guild_traitors = 8
sod_threat_archetype_cattle_raiders = 9
sod_threat_archetype_herd_rustlers = 10
sod_threat_archetype_invader_scouts = 11
sod_threat_archetype_raiding_captain = 12
sod_threat_archetypes_begin = sod_threat_archetype_river_pirates
sod_threat_archetypes_end = sod_threat_archetype_raiding_captain + 1


########################################################
##  PARTY TEMPLATE SLOTS   #############################
########################################################

# Ryan BEGIN
slot_party_template_num_killed   = 1
# Ryan END

########################################################
rel_enemy   = 0
rel_neutral = 1
rel_ally    = 2


#Talk contexts
tc_town_talk                  = 0
tc_court_talk           = 1
tc_party_encounter            = 2
tc_castle_gate                = 3
tc_siege_commander            = 4
tc_join_battle_ally           = 5
tc_join_battle_enemy          = 6
tc_castle_commander           = 7
tc_hero_freed                 = 8
tc_hero_defeated              = 9
tc_entering_center_quest_talk = 10
tc_back_alley                 = 11
tc_siege_won_seneschal        = 12
tc_ally_thanks                = 13
tc_tavern_talk                = 14
tc_rebel_thanks               = 15
tc_mercenary_base             = 16



#Troop Commentaries begin
#Log entry types
#civilian
logent_village_raided            = 1
logent_village_extorted          = 2
logent_caravan_accosted          = 3
logent_helped_peasants           = 4

logent_castle_captured_by_player              = 10
logent_lord_defeated_by_player                = 11
logent_lord_captured_by_player                = 12
logent_lord_defeated_but_let_go_by_player     = 13
logent_player_defeated_by_lord                = 14
logent_player_retreated_from_lord             = 15
logent_player_retreated_from_lord_cowardly    = 16
logent_lord_helped_by_player                  = 17
logent_player_participated_in_siege           = 18
logent_player_participated_in_major_battle    = 19

logent_pledged_allegiance        = 21
logent_fief_granted_village      = 22
logent_renounced_allegiance      = 23

logent_game_start                           = 31
logent_poem_composed                        = 32 ##Not added
logent_tournament_distinguished             = 33 ##Not added
logent_tournament_won                       = 34 ##Not added


#lord reputation type, for commentaries
#"Martial" will be twice as common as the other types
lrep_none          = 0
lrep_martial       = 1 #chivalrous but not terribly empathetic or introspective, - eg Richard Lionheart, your average 14th century French baron
lrep_quarrelsome   = 2 #spiteful, cynical, a bit paranoid, possibly hotheaded - eg Robert Graves' Tiberius, Shakespeare's Richard III
lrep_selfrighteous = 3 #coldblooded, moralizing, often cruel - eg William the Conqueror, Timur, Octavian, Aurangzeb (although he borders on upstanding)
lrep_cunning       = 4 #coldblooded, pragmatic, amoral - eg Louis XI, Guiscard, Akbar Khan, Abd al-Aziz Ibn Saud
lrep_debauched     = 5 #spiteful, amoral, sadistic, - eg Caligula, Tuchman's Charles of Navarre
lrep_goodnatured   = 6 #chivalrous, benevolent, perhaps a little too decent to be a good warlord - eg Hussein, poss Ranjit Singh (although roguish), Humayun
lrep_upstanding    = 7 #moralizing, benevolent, pragmatic, - eg Bernard Cornwell's Alfred, Charlemagne, Sher Shah Suri

#Troop Commentaries end

#Walker types:
walkert_default            = 0
walkert_needs_money        = 1
walkert_needs_money_helped = 2
walkert_spy                = 3
num_town_walkers = 8
town_walker_entries_start = 32

reinforcement_cost            = 400

merchant_toll_duration        = 72 #Tolls are valid for 72 hours

hero_escape_after_defeat_chance = 50


raid_distance = 4

surnames_begin = "str_surname_1"
surnames_end = "str_surnames_end"
names_begin = "str_name_1"
names_end = surnames_begin
countersigns_begin = "str_countersign_1"
countersigns_end = names_begin
secret_signs_begin = "str_secret_sign_1"
secret_signs_end = countersigns_begin

kingdoms_begin = "fac_player_supporters_faction"
kingdoms_end = "fac_kingdoms_end"

guilds_begin = "fac_sod_merc_guild1"
guilds_end = "fac_kingdom_6_mercenaries"

kingdom_ladies_begin = "trp_knight_1_1_wife"
kingdom_ladies_end = "trp_heroes_end"

kings_begin = "trp_kingdom_1_lord"
kings_end = "trp_knight_1_1"

kingdom_heroes_begin = "trp_kingdom_1_lord"
kingdom_heroes_end = "trp_black_army_guild_master"

guild_masters_begin = "trp_black_army_guild_master"
guild_masters_end = "trp_knight_1_1_wife"

heroes_begin = kingdom_heroes_begin
heroes_end = kingdom_ladies_end

companions_begin = "trp_npc1"
companions_end = "trp_kingdom_heroes_including_player_begin"

active_npcs_begin = companions_begin

active_npcs_end = companions_end

soldiers_begin = "trp_farmer"
soldiers_end = "trp_town_walker_1"

#Rebellion changes

##rebel_factions_begin = "fac_kingdom_1_rebels"
##rebel_factions_end =   "fac_kingdoms_end"

pretenders_begin = "trp_kingdom_1_pretender"
pretenders_end = kingdom_heroes_end
#Rebellion changes

tavern_minstrels_begin = "trp_tavern_minstrel_1"
tavern_minstrels_end   = companions_begin

tavern_booksellers_begin = "trp_tavern_bookseller_1"
tavern_booksellers_end   = tavern_minstrels_begin

tavern_travelers_begin = "trp_tavern_traveler_1"
tavern_travelers_end   = tavern_booksellers_begin

ransom_brokers_begin = "trp_ransom_broker_1"
ransom_brokers_end   = tavern_travelers_begin

mercenary_troops_begin = "trp_watchman"
mercenary_troops_end = "trp_mercenaries_end"

lord_quests_begin = "qst_deliver_message"
lord_quests_end   = "qst_follow_army"

enemy_lord_quests_begin = "qst_lend_surgeon"
enemy_lord_quests_end   = lord_quests_end

village_elder_quests_begin = "qst_deliver_grain"
village_elder_quests_end = "qst_eliminate_bandits_infesting_village"

mayor_quests_begin  = "qst_move_cattle_herd"
mayor_quests_end    = village_elder_quests_begin

lady_quests_begin = "qst_rescue_lord_by_replace"
lady_quests_end   = mayor_quests_begin

army_quests_begin = "qst_deliver_cattle_to_army"
army_quests_end   = lady_quests_begin


all_quests_begin = 0
all_quests_end = "qst_quests_end"
quests_begin = all_quests_begin  # legacy compatibility for generated scripts
quests_end = all_quests_end

towns_begin = "p_town_1"
castles_begin = "p_castle_1"
villages_begin = "p_village_1"

towns_end = castles_begin
castles_end = villages_begin
villages_end   = "p_salt_mine"

walled_centers_begin = towns_begin
walled_centers_end   = castles_end

centers_begin = towns_begin
centers_end   = villages_end

training_grounds_begin   = "p_training_ground_1"
training_grounds_end     = "p_Bridge_1"

scenes_begin = "scn_town_1_center"
scenes_end = "scn_castle_1_exterior"

spawn_points_begin = "p_zendar"
spawn_points_end = "p_spawn_points_end"

regular_troops_begin       = "trp_novice_fighter"
regular_troops_end         = "trp_tournament_master"

swadian_merc_parties_begin = "p_town_1_mercs"
swadian_merc_parties_end   = "p_town_8_mercs"

vaegir_merc_parties_begin  = "p_town_8_mercs"
vaegir_merc_parties_end    = "p_zendar"

arena_masters_begin    = "trp_town_1_arena_master"
arena_masters_end      = "trp_town_1_armorer"

training_gound_trainers_begin    = "trp_trainer_1"
training_gound_trainers_end      = "trp_ransom_broker_1"

town_walkers_begin = "trp_town_walker_1"
town_walkers_end = "trp_village_walker_1"

village_walkers_begin = "trp_village_walker_1"
village_walkers_end   = "trp_spy_walker_1"

spy_walkers_begin = "trp_spy_walker_1"
spy_walkers_end = "trp_tournament_master"

walkers_begin = town_walkers_begin
walkers_end   = spy_walkers_end

armor_merchants_begin  = "trp_town_1_armorer"
armor_merchants_end    = "trp_town_1_weaponsmith"

weapon_merchants_begin = "trp_town_1_weaponsmith"
weapon_merchants_end   = "trp_town_1_tavernkeeper"

tavernkeepers_begin    = "trp_town_1_tavernkeeper"
tavernkeepers_end      = "trp_town_1_merchant"

goods_merchants_begin  = "trp_town_1_merchant"
goods_merchants_end    = "trp_town_1_horse_merchant"

horse_merchants_begin  = "trp_town_1_horse_merchant"
horse_merchants_end    = "trp_town_1_mayor"

mayors_begin           = "trp_town_1_mayor"
mayors_end             = "trp_village_1_elder"

village_elders_begin   = "trp_village_1_elder"
village_elders_end     = "trp_merchants_end"


average_price_factor = 1000
minimum_price_factor = 100
maximum_price_factor = 10000

village_prod_min = -5
village_prod_max = 18

trade_goods_begin = "itm_smoked_fish"
trade_goods_end = "itm_tutorial_sword"
food_begin = "itm_smoked_fish"
#food_end = "itm_wine"
food_end = "itm_spice"
reference_books_begin = "itm_book_wound_treatment_reference"
reference_books_end   = trade_goods_begin
readable_books_begin = "itm_book_tactics"
readable_books_end   = reference_books_begin
books_begin = readable_books_begin
books_end = reference_books_end
horses_begin = "itm_sumpter_horse"
horses_end = "itm_arrows"
weapons_begin = "itm_wooden_stick"
weapons_end = "itm_wooden_shield"
ranged_weapons_begin = "itm_jarid"
ranged_weapons_end = "itm_great_lancec"
armors_begin = "itm_leather_gloves"
armors_end = "itm_wooden_stick"
shields_begin = "itm_wooden_shield"
shields_end = "itm_jarid"

# Banner constants

banner_meshes_begin = "mesh_banner_a01"
banner_meshes_end_minus_one = "mesh_banner_n21"

arms_meshes_begin = "mesh_arms_a01"
arms_meshes_end_minus_one = "mesh_arms_n21"

custom_banner_charges_begin = "mesh_custom_banner_charge_01"
custom_banner_charges_end = "mesh_tableau_mesh_custom_banner"

custom_banner_backgrounds_begin = "mesh_custom_banner_bg"
custom_banner_backgrounds_end = custom_banner_charges_begin

custom_banner_flag_types_begin = "mesh_custom_banner_01"
custom_banner_flag_types_end = custom_banner_backgrounds_begin

custom_banner_flag_map_types_begin = "mesh_custom_map_banner_01"
custom_banner_flag_map_types_end = custom_banner_flag_types_begin

custom_banner_flag_scene_props_begin = "spr_custom_banner_01"
custom_banner_flag_scene_props_end = "spr_banner_a"

custom_banner_map_icons_begin = "icon_custom_banner_01"
custom_banner_map_icons_end = "icon_banner_01"

banner_map_icons_begin = "icon_banner_01"
banner_map_icons_end_minus_one = "icon_banner_304"

banner_scene_props_begin = "spr_banner_a"
banner_scene_props_end_minus_one = "spr_banner_n21"

khergit_banners_begin_offset = 63
khergit_banners_end_offset = 84

# Some constants for merchant invenotries
merchant_inventory_space = 30
num_merchandise_goods = 40

num_max_river_pirates = 25
num_max_zendar_peasants = 25
num_max_zendar_manhunters = 10

num_max_dp_bandits = 10
num_max_refugees = 10
num_max_deserters = 10

num_max_militia_bands = 15
num_max_armed_bands = 12

num_max_vaegir_punishing_parties = 20
num_max_rebel_peasants = 25

num_max_frightened_farmers = 50
num_max_undead_messengers  = 20

num_forest_bandit_spawn_points = 1
num_mountain_bandit_spawn_points = 1
num_steppe_bandit_spawn_points = 1
num_black_khergit_spawn_points = 1
num_sea_raider_spawn_points = 2

peak_prisoner_trains = 4
peak_kingdom_caravans = 12
peak_kingdom_messengers = 3


# Note positions
note_troop_location = 3

#battle tactics
btactic_hold = 1
btactic_follow_leader = 2
btactic_charge = 3
btactic_stand_ground = 4

#default right mouse menu orders
cmenu_move = -7

# Town center modes
tcm_default = 0
tcm_disguised = 1

# Arena battle modes
#abm_fight = 0
abm_training = 1
abm_visit = 2
abm_tournament = 3

# Camp training modes
ctm_melee    = 1
ctm_ranged   = 2
ctm_mounted  = 3
ctm_training = 4

# Village bandits attack modes
vba_normal          = 1
vba_after_training  = 2

arena_tier1_opponents_to_beat = 3
arena_tier1_prize = 10
arena_tier2_opponents_to_beat = 6
arena_tier2_prize = 50
arena_tier3_opponents_to_beat = 10
arena_tier3_prize = 100
arena_tier4_opponents_to_beat = 20
arena_tier4_prize = 300
arena_grand_prize = 500

#Tavern recruitment and ale
merc_parties_begin = "p_town_merc_1"
merc_parties_end = "p_zendar"

#SoD - Kuba: mercenary guild troops
black_army_guild_master      = "trp_black_army_guild_master" 
boar_clan_guild_master       = "trp_boar_clan_guild_master"
conquistadors_guild_master   = "trp_conquistador_guild_master"
elephant_guard_guild_master  = "trp_elephant_guard_guild_master"
jotnar_clan_guild_master     = "trp_jotnar_clan_guild_master"
serpent_host_guild_master    = "trp_serpent_host_guild_master"
slavers_guild_master         = "trp_slaver_guild_master"


black_army_rep      = "trp_black_army_rep_1" 
boar_clan_rep       = "trp_boar_clan_representative"
conquistadors_rep   = "trp_conquistador_rep_1"
elephant_guard_rep  = "trp_elephant_guard_rep_1"
jotnar_clan_rep     = "trp_jotnar_clan_rep_1" 
serpent_host_rep    = "trp_serpent_host_rep_1"
slavers_rep         = "trp_slaver_rep_1"

black_army_tier_1_unit_1      = "trp_black_army_fresh_blade" 
conquistadors_tier_1_unit_1   = "trp_conquistador_footman"
elephant_guard_tier_1_unit_1  = "trp_elephant_guard_tribesman"
jotnar_clan_tier_1_unit_1     = "trp_jotnar_clan_volva" 
serpent_host_tier_1_unit_1    = "trp_serpent_host_akinci"
slavers_tier_1_unit_1         = "trp_henchman"

black_army_tier_1_unit_2      = "trp_black_army_line_supporter" 
conquistadors_tier_1_unit_2   = "trp_conquistador_crossbowman"
elephant_guard_tier_1_unit_2  = "trp_elephant_guard_tribesman"
jotnar_clan_tier_1_unit_2     = "trp_jotnar_clan_armsman" 
serpent_host_tier_1_unit_2    = "trp_serpent_host_kapikulu"
slavers_tier_1_unit_2         = "trp_slave"

black_army_tier_1_unit_3      = "trp_black_army_line_crusher" 

black_army_noble      = "trp_black_army_raven_captain" 
conquistadors_noble   = "trp_conquistador_lancer"
elephant_guard_noble  = "trp_elephant_guard_battle_shaman"
jotnar_clan_noble     = "trp_jotnar_clan_norn_mistress" 
serpent_host_noble    = "trp_serpent_host_basilisk_knight"
slavers_noble         = "trp_tormenter"

slavers_mercs_noble = "p_sod_merc_6_elite"
slavers_sod_mercs   = "p_sod_merc_6"

hero_death_after_defeat_chance = 2
king_death_after_defeat_chance = 1

player_debt_to_faction = 90
spt_mercenary_lord_party = 25

fgtq_end = 5
fgtq_next = 4
fgtq_eg_special = 3
fgtq_sh_2_next = 2

#SoD - Kuba: Laws
law_backgrounds_begin = "mesh_sod_law_bgmesh_1"
law_meshes_begin = "mesh_sod_law_mesh_blank"
law_names_begin = "str_sod_law_name_blank"
law_descriptions_begin = "str_sod_law_description_blank"

enacted_laws_begin = 10
enacted_laws_end = 20

#SoD - Kuba: Buildings
village_buildings = [slot_center_has_manor, slot_center_has_mill, slot_center_has_watch_tower,
slot_center_has_inn, slot_center_has_shrine, slot_center_has_monastery, slot_center_has_messenger_post,
slot_center_has_ambulatory, slot_center_has_water_supply, slot_center_has_clayworks, slot_center_has_rustic_blacksmith]

town_buildings = [slot_center_has_temple, slot_center_has_barracks, slot_center_has_range,
slot_center_has_stables, slot_center_has_blacksmith, slot_center_has_messenger_post,
slot_center_has_prisoner_tower, slot_center_has_guild, slot_center_has_university, slot_center_has_hospital,
slot_center_has_canalization, slot_center_has_manufacture, slot_center_has_bank]

castle_buildings = [slot_center_has_chapel, slot_center_has_barracks, slot_center_has_range,
slot_center_has_stables, slot_center_has_chapter, slot_center_has_blacksmith, slot_center_has_messenger_post,
slot_center_has_prisoner_tower]

buildings_initialization = []

	#village:
buildings_initialization.append((troop_set_slot, trp_village, 0, len(village_buildings)))
count = 1
for vb in village_buildings:
	buildings_initialization.append((troop_set_slot, trp_village, count, vb))
	count = count+1
	#town:
buildings_initialization.append((troop_set_slot, trp_town, 0, len(town_buildings)))
count = 1
for tb in town_buildings:
	buildings_initialization.append((troop_set_slot, trp_town, count, tb))
	count = count+1
	#castle:
buildings_initialization.append((troop_set_slot, trp_castle, 0, len(castle_buildings)))
count = 1
for cb in castle_buildings:
	buildings_initialization.append((troop_set_slot, trp_castle, count, cb))
	count = count+1
	

sod_upgrade_command_list = []
#----------------------------------------------------------------------------------
