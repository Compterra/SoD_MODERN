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

current_file_version            = 461

village_pop_min                 = 80
village_pop_max                 = 1000
village_pop_ideal               = (village_pop_max-village_pop_min)/2+village_pop_min

town_pop_min                    = 800
town_pop_max                    = 6000
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
sod_faith_ascension_local_min   = 35    # towns need this much local faith before manual faith ascension is allowed
sod_faith_ascension_holy_cost   = 20    # each faith elite adds this much holy burden, reducing future effective faith
sod_faith_ascension_event_bonus = 25    # chapel/temple support can push the rare daily calling event over the line

# Nobles: population cap for immigration (nobles per run <= total_chapter_pop / divisor)
sod_noble_cap_pop_divisor        = 2000  # higher = fewer nobles for same population

# Economy: population-based scaling (tunable for balance)
sod_town_consumption_pop_divisor = 400   # weekly grain/flour consumption = town_pop / this (min 1)
sod_town_consumption_extra_pop_divisor = 800  # meat/ale consumption = town_pop / this (min 1), typically lower than grain
sod_cattle_production_pop_divisor = 200 # cattle meat production *= village_pop / this

# Construction: weekly labor output from real population/support.
sod_village_construction_pop_divisor = 12
sod_town_construction_pop_divisor = 35
sod_castle_construction_bound_pop_divisor = 90
sod_castle_construction_support_divisor = 10
sod_castle_construction_garrison_divisor = 6
sod_castle_construction_min_garrison_labor = 6
sod_village_construction_workforce_cap = 75
sod_town_construction_workforce_cap = 180
sod_castle_construction_workforce_cap = 130

# Caravan progression: profitable kingdom caravans can scale up over time.
sod_caravan_upgrade_profit_tier_1 = 250   # total realized trade profit needed for first upgrade
sod_caravan_upgrade_profit_tier_2 = 700   # total realized trade profit needed for second upgrade
sod_caravan_upgrade_profit_tier_3 = 1400  # total realized trade profit needed for third upgrade
sod_caravan_trade_percent_bonus_per_tier = 5  # extra trade intensity passed to script_do_party_center_trade per tier

# Center modifier IDs. These are not slots; they are stable script selector IDs.
sod_center_modifier_none = 0
sod_center_modifier_trade_liquidity_flat = 1
sod_center_modifier_trade_volume_pct = 2
sod_center_modifier_tariff_income_pct = 3
sod_center_modifier_market_wealth_flat = 4
sod_center_modifier_market_wealth_pct = 5
sod_center_modifier_prosperity_cap_flat = 6
sod_center_modifier_prosperity_growth_flat = 7
sod_center_modifier_prosperity_growth_pct = 8
sod_center_modifier_production_output_pct = 9
sod_center_modifier_goods_import_demand_pct = 10
sod_center_modifier_goods_export_supply_pct = 11
sod_center_modifier_merchant_happiness_flat = 12
sod_center_modifier_tax_efficiency_pct = 13
sod_center_modifier_population_capacity_flat = 14
sod_center_modifier_population_growth_flat = 15
sod_center_modifier_population_growth_pct = 16
sod_center_modifier_population_recovery_flat = 17
sod_center_modifier_migration_attraction_flat = 18
sod_center_modifier_migration_retention_flat = 19
sod_center_modifier_health_cap_flat = 20
sod_center_modifier_health_recovery_flat = 21
sod_center_modifier_disease_resistance_pct = 22
sod_center_modifier_food_consumption_pct = 23
sod_center_modifier_food_store_capacity_flat = 24
sod_center_modifier_food_security_flat = 25
sod_center_modifier_cattle_growth_flat = 26
sod_center_modifier_cattle_output_pct = 27
sod_center_modifier_security_flat = 28
sod_center_modifier_raid_resistance_pct = 29
sod_center_modifier_raid_recovery_flat = 30
sod_center_modifier_threat_reduction_flat = 31
sod_center_modifier_bandit_spawn_reduction_pct = 32
sod_center_modifier_desperation_bandit_reduction_pct = 33
sod_center_modifier_unrest_flat = 34
sod_center_modifier_unrest_reduction_flat = 35
sod_center_modifier_prisoner_escape_reduction_pct = 36
sod_center_modifier_warning_range_flat = 37
sod_center_modifier_patrol_response_pct = 38
sod_center_modifier_infantry_training_flat = 39
sod_center_modifier_ranged_training_flat = 40
sod_center_modifier_cavalry_training_flat = 41
sod_center_modifier_garrison_recovery_flat = 42
sod_center_modifier_garrison_upkeep_pct = 43
sod_center_modifier_troop_upgrade_cost_pct = 44
sod_center_modifier_recruit_count_flat = 45
sod_center_modifier_recruit_tier_bonus_flat = 46
sod_center_modifier_noble_recruitment_flat = 47
sod_center_modifier_faith_troop_access_flat = 48
sod_center_modifier_faith_ascension_bonus_flat = 49
sod_center_modifier_construction_speed_pct = 50
sod_center_modifier_construction_cost_pct = 51
sod_center_modifier_weekly_upkeep_flat = 52
sod_center_modifier_demesne_cost_flat = 53
sod_center_modifier_renown_weekly_flat = 54
sod_center_modifier_relations_weekly_flat = 55
sod_center_modifier_administration_flat = 56
sod_center_modifier_law_compliance_flat = 57
sod_center_modifier_local_faith_growth_flat = 58
sod_center_modifier_global_faith_growth_flat = 59
sod_center_modifier_faith_stability_flat = 60
sod_center_modifier_cultural_assimilation_flat = 61
sod_center_modifier_begin = sod_center_modifier_trade_liquidity_flat
sod_center_modifier_end = sod_center_modifier_cultural_assimilation_flat + 1

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
sod_spawn_cap_generic_bandits    = 55
sod_spawn_cap_mountain_bandits   = 12
sod_spawn_cap_forest_bandits     = 12
sod_spawn_cap_sea_raiders        = 14
sod_spawn_cap_steppe_bandits     = 10
sod_spawn_cap_boar_raiders       = 7
sod_spawn_cap_boar_desert_bands  = 8

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
slot_agent_courage_score          = 23
slot_agent_is_hard_routed         = 24
slot_agent_sod_post_defeat_focus_index = 25

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

# Slaver black market web. Used by fac_sod_merc_guild6 only.
slot_faction_slaver_market_demand = 275
slot_faction_slaver_market_supply = 276
slot_faction_slaver_market_heat = 277
slot_faction_slaver_market_bases = 278
slot_faction_slaver_market_last_spawn_day = 279

# Elephant Guard sacred wardens. Used by fac_sod_merc_guild3 only.
slot_faction_elephant_guard_devotion = 280
slot_faction_elephant_guard_supplies = 281
slot_faction_elephant_guard_omens = 282
slot_faction_elephant_guard_active_parties = 283
slot_faction_elephant_guard_target_center = 284
slot_faction_elephant_guard_last_spawn_day = 285
slot_faction_elephant_guard_slaver_alarm = 294

# Jotnar Clan hearth camps. Used by fac_sod_merc_guild4 only.
slot_faction_jotnar_hearth_pressure = 286
slot_faction_jotnar_active_parties = 287
slot_faction_jotnar_target_center = 288
slot_faction_jotnar_last_spawn_day = 289
slot_faction_jotnar_slaver_pressure = 295

# Serpent Host route screens. Used by fac_sod_merc_guild5 only.
slot_faction_serpent_route_pressure = 290
slot_faction_serpent_active_parties = 291
slot_faction_serpent_target_center = 292
slot_faction_serpent_last_spawn_day = 293

# Boar Clan frontier toll bands. Used by fac_sod_merc_guild7 only.
slot_faction_boar_frontier_pressure = 296
slot_faction_boar_active_parties = 297
slot_faction_boar_target_center = 298
slot_faction_boar_tribute_stock = 299
slot_faction_boar_intimidation = 300

# Black Army road-security contracts. Used by fac_sod_merc_guild1 only.
slot_faction_black_army_security_fund = 301
slot_faction_black_army_contract_heat = 302

# Conquistador expedition logistics. Used by fac_sod_merc_guild2 only.
slot_faction_conquistador_supply_stock = 303
slot_faction_conquistador_requisition_heat = 304

# Serpent Host route intelligence. Used by fac_sod_merc_guild5 only.
slot_faction_serpent_intelligence = 305
slot_faction_serpent_safe_passage = 306

# Black Khergit moving horde. Used by fac_black_khergits only.
slot_faction_black_khergit_pressure = 307
slot_faction_black_khergit_camp_party = 308
slot_faction_black_khergit_target_center = 309
slot_faction_black_khergit_last_migration_day = 310
slot_faction_black_khergit_last_spawn_day = 311
slot_faction_black_khergit_tribute = 312
slot_faction_black_khergit_safe_passage_until = 313
slot_faction_black_khergit_camp_disrupted_until = 314
slot_faction_black_khergit_last_raid_report_day = 315
slot_faction_black_khergit_last_pressure_day = 316

# Imperial Expeditionary Force campaign state. Used by fac_kingdom_6 only.
slot_faction_imperial_expedition_pressure = 317
slot_faction_imperial_expedition_supply = 318
slot_faction_imperial_expedition_front = 319
slot_faction_imperial_expedition_enemy_realms = 320
slot_faction_imperial_expedition_last_update_day = 321
slot_faction_imperial_expedition_sabotage_until = 322

# Ponavosa diplomacy system. Normal kingdoms use these slots; fac_kingdom_6 is
# deliberately treated as an exception by the helper scripts.
slot_faction_diplomacy_temperament = 323
slot_faction_diplomacy_legitimacy = 324
slot_faction_diplomacy_fear = 325
slot_faction_diplomacy_grievance = 326
slot_faction_diplomacy_war_weariness = 327
slot_faction_diplomacy_trade_interest = 328
slot_faction_diplomacy_honor_stance = 329
slot_faction_diplomacy_slavery_stance = 330
slot_faction_diplomacy_border_stance = 331
slot_faction_diplomacy_religious_stance = 332
slot_faction_diplomacy_current_crisis = 333
slot_faction_diplomacy_last_envoy_day = 334
slot_faction_diplomacy_last_treaty_day = 335

slot_faction_diplomacy_policy_culture = 336
slot_faction_diplomacy_policy_border = 337
slot_faction_diplomacy_policy_slavery = 338
slot_faction_diplomacy_decree_war_taxes = 339
slot_faction_diplomacy_decree_reconstruction = 340
slot_faction_diplomacy_decree_anti_slaver = 341
slot_faction_diplomacy_decree_road_patrol = 342

slot_faction_treaty_partner_1 = 343
slot_faction_treaty_type_1 = 344
slot_faction_treaty_until_day_1 = 345
slot_faction_treaty_strength_1 = 346
slot_faction_treaty_partner_2 = 347
slot_faction_treaty_type_2 = 348
slot_faction_treaty_until_day_2 = 349
slot_faction_treaty_strength_2 = 350
slot_faction_treaty_partner_3 = 351
slot_faction_treaty_type_3 = 352
slot_faction_treaty_until_day_3 = 353
slot_faction_treaty_strength_3 = 354
slot_faction_treaty_partner_4 = 355
slot_faction_treaty_type_4 = 356
slot_faction_treaty_until_day_4 = 357
slot_faction_treaty_strength_4 = 358
faction_diplomacy_treaty_slots_begin = slot_faction_treaty_partner_1
faction_diplomacy_treaty_slots_end = 359

slot_faction_diplomacy_memory_player_trust = 359
slot_faction_diplomacy_memory_player_grievance = 360
slot_faction_diplomacy_memory_player_aid = 361
slot_faction_diplomacy_memory_player_slaver = 362
slot_faction_diplomacy_memory_player_anti_slaver = 363
slot_faction_diplomacy_memory_player_last_day = 364
slot_faction_diplomacy_war_reason = 365
slot_faction_diplomacy_war_reason_target = 366
slot_faction_diplomacy_policy_military_service = 367
slot_faction_diplomacy_policy_justice = 368
slot_faction_diplomacy_policy_reconstruction = 369
slot_faction_diplomacy_decree_emergency_conscription = 370
slot_faction_diplomacy_decree_imperial_defense = 371
slot_faction_diplomacy_decree_caravan_protection = 372
slot_faction_diplomacy_decree_fortress_restoration = 373
slot_faction_diplomacy_decree_grain_relief = 374
slot_faction_diplomacy_decree_public_executions = 375
slot_faction_diplomacy_decree_amnesty = 376
slot_faction_diplomacy_decree_start_day = 377
slot_faction_diplomacy_decree_cooldown_day = 378
slot_faction_diplomacy_ai_last_pulse_day = 379
slot_faction_diplomacy_internal_discontent = 380
slot_faction_diplomacy_lord_war_support = 381
slot_faction_diplomacy_last_incident_day = 382
slot_faction_diplomacy_telemetry_incidents = 383
slot_faction_diplomacy_telemetry_treaty_effects = 384
slot_faction_diplomacy_telemetry_tribute_pressure = 385
slot_faction_diplomacy_telemetry_imperial_coordination = 386
slot_faction_diplomacy_telemetry_discontent_delta = 387
slot_faction_diplomacy_telemetry_support_delta = 388

sod_diplomacy_temperament_expansionist = 1
sod_diplomacy_temperament_defensive = 2
sod_diplomacy_temperament_mercantile = 3
sod_diplomacy_temperament_honor_bound = 4
sod_diplomacy_temperament_predatory = 5
sod_diplomacy_temperament_isolationist = 6
sod_diplomacy_temperament_opportunist = 7
sod_diplomacy_temperament_anti_imperial = 8
sod_diplomacy_temperament_imperial_exception = 9

sod_diplomacy_crisis_none = 0
sod_diplomacy_crisis_imperial = 1
sod_diplomacy_crisis_black_khergit = 2
sod_diplomacy_crisis_slaver = 3
sod_diplomacy_crisis_multi_war = 4
sod_diplomacy_crisis_famine = 5
sod_diplomacy_crisis_succession = 6

sod_diplomacy_policy_trade = 1
sod_diplomacy_policy_balanced = 2
sod_diplomacy_policy_military = 3
sod_diplomacy_policy_open = 1
sod_diplomacy_policy_guarded = 2
sod_diplomacy_policy_sealed = 3
sod_diplomacy_policy_slavery_banned = 1
sod_diplomacy_policy_slavery_tolerated = 2
sod_diplomacy_policy_slavery_regulated = 3
sod_diplomacy_policy_slavery_accepted = 4
sod_diplomacy_policy_service_volunteer = 1
sod_diplomacy_policy_service_levy = 2
sod_diplomacy_policy_service_conscription = 3
sod_diplomacy_policy_service_forced_levy = 4
sod_diplomacy_policy_justice_merciful = 1
sod_diplomacy_policy_justice_balanced = 2
sod_diplomacy_policy_justice_severe = 3
sod_diplomacy_policy_justice_terror = 4
sod_diplomacy_policy_reconstruction_austerity = 1
sod_diplomacy_policy_reconstruction_normal = 2
sod_diplomacy_policy_reconstruction_rebuilding = 3
sod_diplomacy_policy_reconstruction_relief = 4

sod_diplomacy_treaty_none = 0
sod_diplomacy_treaty_truce = 1
sod_diplomacy_treaty_trade_accord = 2
sod_diplomacy_treaty_tribute = 3
sod_diplomacy_treaty_anti_imperial_league = 4
sod_diplomacy_treaty_demand_tribute = 5
sod_diplomacy_treaty_non_aggression = 6
sod_diplomacy_treaty_military_access = 7
sod_diplomacy_treaty_defensive_pact = 8
sod_diplomacy_treaty_prisoner_exchange = 9
sod_diplomacy_treaty_anti_slaver_compact = 10
sod_diplomacy_treaty_border_security_pact = 11

sod_diplomacy_memory_broken_truce = 1
sod_diplomacy_memory_released_lord = 2
sod_diplomacy_memory_executed_lord = 3
sod_diplomacy_memory_captive_freed = 4
sod_diplomacy_memory_slaver_cooperation = 5
sod_diplomacy_memory_anti_slaver_action = 6
sod_diplomacy_memory_anti_imperial_aid = 7
sod_diplomacy_memory_tribute_accepted = 8
sod_diplomacy_memory_tribute_refused = 9
sod_diplomacy_memory_envoy_failed = 10
sod_diplomacy_memory_border_raid = 11
sod_diplomacy_memory_caravan_attack = 12
sod_diplomacy_memory_shared_enemy = 13

sod_diplomacy_war_reason_unknown = 0
sod_diplomacy_war_reason_border_dispute = 1
sod_diplomacy_war_reason_retaliation = 2
sod_diplomacy_war_reason_conquest = 3
sod_diplomacy_war_reason_religious_hostility = 4
sod_diplomacy_war_reason_slaver_outrage = 5
sod_diplomacy_war_reason_imperial_crisis = 6
sod_diplomacy_war_reason_badboy_containment = 7
sod_diplomacy_war_reason_trade_route_conflict = 8
sod_diplomacy_war_reason_broken_treaty = 9
sod_diplomacy_war_reason_black_khergit_pressure = 10
sod_diplomacy_war_reason_mercenary_pact = 11

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
slot_center_construction_progress = 126
slot_center_construction_required = 127
slot_center_construction_weekly_workforce = 128
slot_center_construction_last_progress = 129

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
slot_center_has_militia_yard = 155        #village
slot_center_has_beacon_hill = 156         #village
slot_center_has_granary = 157             #village
slot_center_has_militia_armory = 158      #village
slot_center_has_mercenary_guild_hall = 159 #castle
#SoD BUILDINGS END

village_improvements_begin = slot_center_has_manor
village_improvements_end = slot_center_has_messenger_post+1

walled_center_improvements_begin = slot_center_has_messenger_post
walled_center_improvements_end = slot_center_has_university+1

#SoD Faith
slot_center_sod_local_faith = 245

sod_faiths_begin = 1
sod_faiths_end = 6
sod_faith_support_min = 0
sod_faith_support_max = 100
sod_faith_tension_soft_cap = 60

slot_center_sod_faith_1_support = 373
slot_center_sod_faith_2_support = 374
slot_center_sod_faith_3_support = 375
slot_center_sod_faith_4_support = 376
slot_center_sod_faith_5_support = 377
slot_center_sod_dominant_faith = 378
slot_center_sod_faith_tension = 379
slot_center_sod_faith_institution_strength = 380
slot_center_sod_faith_migrated = 381

slot_center_sod_security_cache_day = 382
slot_center_sod_security_cache_effective_threat = 383
slot_center_sod_security_cache_security = 384
slot_center_sod_security_cache_threat_reduction = 385
slot_center_sod_security_cache_raid_resistance = 386
slot_center_sod_security_cache_bandit_reduction = 387
slot_center_sod_security_cache_desperation_bandit_reduction = 388
slot_center_sod_security_cache_warning_range = 389
slot_center_sod_security_cache_patrol_response = 390
slot_center_sod_security_cache_unrest_pressure = 391
slot_center_sod_security_cache_base_threat = 392
slot_center_sod_security_cache_vulnerability = 393
slot_center_sod_security_cache_contract_security = 394
slot_center_sod_common_prisoners = 395
slot_center_sod_military_prisoners = 396
slot_center_sod_bandit_prisoners = 397
slot_center_sod_slave_laborers = 398
slot_center_sod_prisoner_unrest_pressure = 399
slot_center_sod_prisoner_escape_pressure = 413
slot_center_sod_prisoner_last_update_day = 414
slot_center_sod_prisoner_capacity = 415
slot_center_sod_prisoner_holding_policy = 416
slot_center_sod_patrol_road_preference = 417
slot_center_sod_patrol_recent_destroyed_day = 418
slot_center_sod_patrol_campaign_screen_request = 419
slot_center_sod_merc_hall_troop_type = 433
slot_center_sod_merc_hall_troop_amount = 434
slot_center_sod_merc_hall_guild = 435
slot_center_sod_merc_hall_last_refresh_day = 436
slot_center_sod_merc_hall_stock_quality = 437

slot_faction_sod_dominant_faith = 389
slot_faction_sod_player_faith_coverage = 390
slot_faction_sod_faith_tension = 391
slot_faction_sod_clergy_legitimacy = 392
slot_faction_sod_lord_morale_pressure = 393
slot_faction_sod_campaign_health = 394
slot_faction_sod_tired_lord_count = 395
slot_faction_sod_unpaid_lord_count = 396
slot_faction_sod_campaign_posture = 397
slot_faction_sod_campaign_posture_target = 398
slot_faction_sod_campaign_posture_day = 399
slot_faction_sod_campaign_posture_confidence = 400
slot_faction_sod_campaign_posture_reason = 401
slot_faction_sod_marshal_planning_score = 402
slot_faction_sod_marshal_coordination_score = 403
slot_faction_sod_marshal_logistics_score = 404
slot_faction_sod_marshal_aggression_score = 405
slot_faction_sod_marshal_caution_score = 406
slot_faction_sod_last_failed_siege_target = 407
slot_faction_sod_last_failed_siege_day = 408
slot_faction_sod_failed_siege_avoidance = 409
slot_faction_sod_marshal_current_followers = 410
slot_faction_sod_marshal_desired_followers = 411
slot_faction_sod_marshal_offensive_readiness = 412
slot_faction_sod_prisoner_supply = 413
slot_faction_sod_prisoner_demand = 414
slot_faction_sod_prisoner_labor_policy = 415
slot_faction_sod_prisoner_exchange_pressure = 416
slot_faction_sod_prisoner_abuse_heat = 417
slot_faction_sod_prisoner_mercy_reputation = 418
slot_faction_sod_active_prisoner_trains = 419
slot_faction_sod_landless_lord_count = 420
slot_faction_sod_disgruntled_lord_count = 421
slot_faction_sod_vassal_loyalty_health = 422

# Late mini-faction lock state. Kept high to avoid legacy faction slot ranges.
slot_faction_black_khergit_target_lock_until = 423
slot_faction_black_khergit_last_seen_center = 424
slot_faction_black_khergit_last_seen_day = 425
slot_faction_sod_merc_treasury = 426
slot_faction_sod_merc_manpower = 427
slot_faction_sod_merc_veterans = 428
slot_faction_sod_merc_elite_stock = 429
slot_faction_sod_merc_contract_load = 430
slot_faction_sod_merc_support_capacity = 431
slot_faction_sod_merc_active_contracts = 432
slot_faction_sod_merc_recovery_rate = 433
slot_faction_sod_merc_risk_tolerance = 434
slot_faction_sod_merc_market_reputation = 435
slot_faction_sod_merc_price_pressure = 436
slot_faction_sod_merc_last_market_day = 437
slot_faction_sod_merc_last_settlement_day = 438
slot_faction_sod_merc_last_report_flags = 439
slot_faction_sod_merc_demand_score = 440
slot_faction_sod_merc_budget = 441
slot_faction_sod_merc_max_bid = 442
slot_faction_sod_merc_preferred_guild = 443
slot_faction_sod_merc_contract_need_type = 444
slot_faction_sod_merc_contract_urgency = 445
slot_faction_sod_merc_last_bid_day = 446
slot_faction_sod_merc_last_hired_guild = 447

slot_faction_sod_rebel_counterpart = 448
slot_faction_sod_parent_kingdom = 449
slot_faction_sod_claimant_pretender = 450
slot_faction_sod_claimant_old_ruler = 451
slot_faction_sod_civil_war_state = 452
slot_faction_sod_civil_war_started_day = 453
slot_faction_sod_civil_war_parent_fiefs = 454
slot_faction_sod_civil_war_rebel_fiefs = 455
slot_faction_sod_civil_war_last_resolution_day = 456
slot_faction_sod_merc_village_patrol_demand = 457
slot_faction_sod_merc_village_patrol_budget = 458
slot_faction_sod_merc_village_patrol_target = 459
slot_faction_sod_merc_village_patrol_urgency = 460
slot_faction_sod_merc_world_activity_pressure = 461
slot_faction_sod_merc_population_shortage = 470
slot_faction_sod_merc_lord_wealth_score = 471
slot_faction_sod_merc_gold_manpower_pressure = 472
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
slot_party_sod_slaver_web_activity = 348
slot_party_sod_slaver_origin = 349
slot_party_sod_slaver_destination = 350
slot_party_sod_elephant_guard_activity = 351
slot_party_sod_elephant_guard_origin = 352
slot_party_sod_elephant_guard_destination = 353
slot_party_sod_elephant_guard_activity_type = 354
slot_party_sod_jotnar_hearth_activity = 355
slot_party_sod_jotnar_hearth_origin = 356
slot_party_sod_jotnar_hearth_destination = 357
slot_party_sod_serpent_route_activity = 358
slot_party_sod_serpent_route_origin = 359
slot_party_sod_serpent_route_destination = 360
slot_party_sod_boar_frontier_activity = 361
slot_party_sod_boar_frontier_origin = 362
slot_party_sod_boar_frontier_destination = 363
slot_party_black_khergit_camp_activity = 364
slot_party_black_khergit_origin = 365
slot_party_black_khergit_target = 366
slot_party_black_khergit_role = 367
slot_party_sod_diplomacy_envoy_activity = 368
slot_party_sod_diplomacy_envoy_target = 369
slot_party_sod_diplomacy_envoy_treaty = 370
slot_party_sod_diplomacy_envoy_source = 371
slot_party_sod_diplomacy_envoy_start_day = 372
slot_party_sod_trade_origin = 373
slot_party_sod_trade_destination = 374
slot_party_sod_trade_cargo_focus = 375
slot_party_sod_trade_route_risk = 376
slot_party_sod_trade_last_result = 377
slot_party_sod_trade_contract = 378
slot_party_sod_trade_player_protection = 379
slot_party_sod_trade_recent_trouble = 380
slot_party_sod_trade_last_result_day = 381
slot_party_sod_trade_investment = 382
slot_party_sod_morale_snapshot = 383
slot_party_sod_pay_strain_snapshot = 384
slot_party_sod_campaign_fatigue_snapshot = 385
slot_party_sod_last_morale_snapshot_day = 386
slot_party_sod_supply_confidence_snapshot = 387
slot_party_sod_support_type = 388
slot_party_sod_prisoner_origin = 389
slot_party_sod_prisoner_destination = 390
slot_party_sod_prisoner_purpose = 391
slot_party_sod_prisoner_value = 392
slot_party_sod_prisoner_guard_quality = 393
slot_party_sod_prisoner_total_count = 394
slot_party_sod_prisoner_military_count = 395
slot_party_sod_prisoner_bandit_count = 396
slot_party_sod_prisoner_civilian_count = 397
slot_party_sod_prisoner_created_day = 398
slot_party_sod_prisoner_expected_arrival_day = 399
slot_party_sod_support_origin = 420
slot_party_sod_support_target = 421
slot_party_sod_support_commander = 422
slot_party_sod_support_expiry_day = 423
slot_party_sod_support_value = 424
slot_party_sod_patrol_role = 425
slot_party_sod_patrol_status = 426
slot_party_sod_patrol_radius = 427
slot_party_sod_patrol_quality = 428
slot_party_sod_patrol_created_day = 429
slot_party_sod_patrol_last_threat_check_day = 430
slot_party_sod_patrol_origin_castle = 431
slot_party_sod_patrol_route_endpoint = 432
slot_party_sod_retinue_owner_troop = 433
slot_party_sod_retinue_anchor_party = 434
slot_party_sod_retinue_last_sync_hour = 435
slot_party_sod_retinue_state = 436
slot_party_sod_looter_raid_state = 437
slot_party_sod_looter_raid_target = 438
slot_party_sod_looter_raid_start_time = 439
slot_party_sod_looter_raid_last_tick = 440
slot_party_sod_looter_raid_origin_region = 441
slot_party_sod_looter_recently_checked = 442
slot_party_sod_looter_raid_assault_resolved = 443
slot_party_sod_messenger_role = 444
slot_party_sod_tax_courier_origin_center = 445
slot_party_sod_tax_courier_recipient_troop = 446
slot_party_sod_tax_courier_destination_party = 447
slot_party_sod_tax_courier_amount = 448
slot_party_sod_tax_courier_rents = 449
slot_party_sod_tax_courier_tariffs = 450
slot_party_sod_tax_courier_created_day = 451
slot_party_sod_tax_courier_expiry_day = 452
slot_party_sod_tax_courier_status = 453
slot_party_sod_merc_contract_employer = 454
slot_party_sod_merc_contract_guild = 455
slot_party_sod_merc_contract_value = 456
slot_party_sod_merc_contract_wage_rate = 457
slot_party_sod_merc_contract_term_end = 458
slot_party_sod_merc_contract_role = 459
slot_party_sod_merc_contract_quality = 460
slot_party_sod_merc_contract_replenishment_level = 461
slot_party_sod_merc_contract_market_id = 462
slot_party_sod_merc_contract_start_day = 463
slot_party_sod_merc_contract_initial_size = 464
slot_party_sod_merc_contract_loss_score = 465
slot_party_black_khergit_response_until = 466
slot_party_black_khergit_response_target = 467
slot_party_sod_trade_captain_seed = 468
slot_party_sod_trade_house_style = 469
slot_party_sod_trade_player_trust = 470
slot_party_sod_trade_route_reputation = 471

slot_center_sod_looter_raid_cooldown_until = 420
slot_center_sod_looter_raid_pressure = 421
slot_center_sod_looter_last_raid_day = 422
slot_center_sod_looter_last_defense_day = 423
slot_center_sod_security_pressure = 424
slot_center_sod_looter_player_reward_cooldown_until = 425
slot_center_sod_looter_last_assault_day = 426
slot_center_sod_looter_last_assault_result = 427
slot_center_sod_looter_garrison_losses_recent = 428
slot_center_sod_looter_militia_losses_recent = 429
slot_center_sod_active_tax_courier = 430
slot_center_sod_last_tax_courier_day = 431
slot_center_sod_tax_courier_losses = 432

sod_looter_raid_state_none = 0
sod_looter_raid_state_gathering = 1
sod_looter_raid_state_moving_to_target = 2
sod_looter_raid_state_assaulting = 3
sod_looter_raid_state_plundering = 4
sod_looter_raid_state_fleeing = 5
sod_looter_raid_state_resolving = 6

sod_village_assault_result_none = 0
sod_village_assault_result_defender_rout = 1
sod_village_assault_result_defender_hold = 2
sod_village_assault_result_raider_costly = 3
sod_village_assault_result_raider_clean = 4
sod_village_assault_result_raider_overwhelming = 5

sod_merc_contract_role_none = 0
sod_merc_contract_role_field_company = 1
sod_merc_contract_role_patrol = 2
sod_merc_contract_role_escort = 3
sod_merc_contract_role_supply_column = 4
sod_merc_contract_role_mercenary_lord = 5
sod_merc_contract_role_garrison_support = 6
sod_merc_contract_role_special_world_activity = 7

sod_merc_buyer_player = 1
sod_merc_buyer_ai_lord = 2
sod_merc_buyer_ai_kingdom = 3
sod_merc_buyer_guild_internal = 4

sod_merc_contract_term_monthly = 1
sod_merc_contract_term_quarterly = 3
sod_merc_contract_term_campaign = 6

sod_merc_refusal_none = 0
sod_merc_refusal_no_capacity = 1
sod_merc_refusal_low_manpower = 2
sod_merc_refusal_low_treasury = 3
sod_merc_refusal_overextended = 4
sod_merc_refusal_bad_relations = 5
sod_merc_refusal_loss_shock = 6

sod_merc_access_outsider = 0
sod_merc_access_promotion = 1
sod_merc_access_elite = 2
sod_merc_access_service = 3
sod_merc_access_trusted = 4

sod_looter_raid_grace_days = 30
sod_looter_raid_min_party_size = 45
sod_looter_raid_global_cap = 1
sod_looter_raid_village_cooldown_days = 14
sod_looter_raid_defense_cooldown_days = 7
sod_looter_raid_player_reward_cooldown_days = 10
sod_looter_raid_target_radius = 18
sod_looter_raid_arrival_distance = 2
sod_looter_raid_tick_hours = 6
sod_looter_raid_pressure_stage_low = 35
sod_looter_raid_pressure_stage_mid = 65
sod_looter_raid_pressure_stage_high = 90
sod_looter_raid_success_pressure = 100
sod_looter_raid_player_report_radius = 15

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
spt_patrol              = 7
spt_messenger          = 8
##spt_raider             = 9
##spt_scout              = 10
spt_kingdom_caravan    = 11
spt_prisoner_train     = 12
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
spt_diplomatic_envoy   = 22
spt_companion_retinue  = 23

kingdom_party_types_begin = spt_kingdom_caravan
kingdom_party_types_end = spt_kingdom_hero_party + 1

sod_prisoner_category_common = 1
sod_prisoner_category_military = 2
sod_prisoner_category_bandit = 3
sod_prisoner_category_civilian = 4
sod_prisoner_category_mercenary = 5
sod_prisoner_category_elite = 6

sod_prisoner_train_purpose_ransom = 1
sod_prisoner_train_purpose_exchange = 2
sod_prisoner_train_purpose_imprisonment = 3
sod_prisoner_train_purpose_labor = 4
sod_prisoner_train_purpose_slaver_market = 5
sod_prisoner_train_purpose_trial = 6
sod_prisoner_train_purpose_liberation = 7

sod_prisoner_train_status_forming = 1
sod_prisoner_train_status_traveling = 2
sod_prisoner_train_status_delayed = 3
sod_prisoner_train_status_intercepted = 4
sod_prisoner_train_status_arrived = 5
sod_prisoner_train_status_disbanded = 6

sod_prisoner_labor_policy_none = 1
sod_prisoner_labor_policy_penal = 2
sod_prisoner_labor_policy_regulated = 3
sod_prisoner_labor_policy_unrestricted = 4
sod_prisoner_labor_policy_liberation = 5

sod_prisoner_holding_policy_balanced = 1
sod_prisoner_holding_policy_secure = 2
sod_prisoner_holding_policy_ransom = 3
sod_prisoner_holding_policy_labor = 4
sod_prisoner_holding_policy_liberation = 5

sod_prisoner_train_fail_none = 0
sod_prisoner_train_fail_invalid_origin = 1

sod_castle_patrol_max_active = 3
sod_castle_patrol_faction_min_soft_cap = 6

sod_support_type_none = 0
sod_support_type_castle_patrol = 1

sod_messenger_role_none = 0
sod_messenger_role_tax_courier = 1

sod_tax_courier_status_traveling = 1
sod_tax_courier_status_delivered = 2
sod_tax_courier_status_lost = 3
sod_tax_courier_status_expired = 4

sod_castle_patrol_role_road = 1
sod_castle_patrol_role_village_shield = 2
sod_castle_patrol_role_border_harasser = 3
sod_castle_patrol_role_caravan_screen = 4
sod_castle_patrol_role_campaign_screen = 5
sod_castle_patrol_role_emergency_relief = 6

sod_castle_patrol_status_forming = 1
sod_castle_patrol_status_active = 2
sod_castle_patrol_status_returning = 3
sod_castle_patrol_status_damaged = 4
sod_castle_patrol_status_expired = 5
sod_castle_patrol_status_destroyed = 6
sod_castle_patrol_status_disbanded = 7

sod_castle_patrol_fail_none = 0
sod_castle_patrol_fail_not_castle = 1
sod_castle_patrol_fail_no_owner = 2
sod_castle_patrol_fail_besieged = 3
sod_castle_patrol_fail_garrison_low = 4
sod_castle_patrol_fail_food_low = 5
sod_castle_patrol_fail_no_capacity = 6
sod_castle_patrol_fail_no_demand = 7
sod_castle_patrol_fail_bad_target = 8
sod_castle_patrol_fail_support_cap = 9
sod_castle_patrol_fail_no_troops = 10
sod_prisoner_train_fail_invalid_destination = 2
sod_prisoner_train_fail_no_prisoners = 3
sod_prisoner_train_fail_policy_blocked = 4
sod_prisoner_train_fail_cap_reached = 5
sod_prisoner_train_fail_no_guards = 6

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

# Player external party order values.
# These cover SoD's player-owned detachments and hired guild companies.
sod_external_order_follow_player = 101
sod_external_order_hold_here     = 102
sod_external_order_patrol_here   = 103
sod_external_order_noop          = 104

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

# Companion depth system: player-facing approval, roles, warnings, and personal arcs.
slot_troop_companion_approval = 133
slot_troop_companion_trust_tier = 134
slot_troop_companion_personal_quest_stage = 135
slot_troop_companion_role = 136
slot_troop_companion_last_reaction_day = 137
slot_troop_companion_warning_state = 138
slot_troop_companion_loyalty_lock = 139
slot_troop_companion_core_value_proof = 146
slot_troop_sod_camp_job = 148
slot_troop_sod_camp_job_pressure = 149
slot_troop_sod_camp_job_pressure_max = 150
slot_troop_sod_camp_job_last_tick_hour = 151
slot_troop_sod_camp_job_last_result = 152

# Companion retinues: center-style internal troop containers commanded by companions.
slot_troop_sod_retinue_party = 318
slot_troop_sod_retinue_capacity = 319
slot_troop_sod_retinue_state = 320
slot_troop_sod_retinue_policy = 321
slot_troop_sod_retinue_last_size = 322
slot_troop_sod_retinue_last_wage = 323
slot_troop_sod_retinue_last_morale = 324
slot_troop_sod_retinue_warning_state = 325
slot_troop_sod_retinue_treasury = 326
slot_troop_sod_retinue_wage_reserve = 327
slot_troop_sod_retinue_strength_order = 328
slot_troop_sod_retinue_recruit_policy = 329
slot_troop_sod_retinue_last_recruit_hour = 330
slot_troop_sod_retinue_last_upgrade_hour = 331
slot_troop_sod_retinue_last_invoice = 332
slot_troop_sod_retinue_post_battle_policy = 333
slot_troop_sod_retinue_last_battle_hire_result = 334
slot_troop_sod_retinue_last_battle_hire_amount = 335
slot_troop_sod_retinue_last_battle_hire_troop = 336
slot_troop_sod_retinue_battle_store_party = 337
slot_troop_sod_retinue_last_shortage = 338
slot_troop_sod_retinue_supply_pressure = 339
slot_troop_sod_retinue_last_training_xp = 340
slot_troop_sod_retinue_last_training_hour = 341
slot_troop_sod_retinue_last_desertion_day = 342

sod_retinue_state_inactive = 0
sod_retinue_state_active = 1
sod_retinue_state_suspended = 2
sod_retinue_state_detached = 3
sod_retinue_state_pending_cleanup = 4

sod_retinue_wage_shortage_player_auto_cover = 1
sod_retinue_wage_shortage_purse_only = 2

sod_retinue_warning_none = 0
sod_retinue_warning_no_troops_returning = 1
sod_retinue_warning_over_capacity = 2
sod_retinue_warning_above_target = 3
sod_retinue_warning_full_refused = 4

sod_retinue_policy_balanced = 1
sod_retinue_policy_defensive = 2
sod_retinue_policy_aggressive = 3
sod_retinue_policy_training = 4
sod_retinue_policy_guard_companion = 5

sod_retinue_strength_none = 0
sod_retinue_strength_half = 1
sod_retinue_strength_full = 2

sod_retinue_recruit_policy_none = 0
sod_retinue_recruit_policy_cautious = 1
sod_retinue_recruit_policy_balanced = 2
sod_retinue_recruit_policy_eager = 3

sod_retinue_post_battle_enabled = 0
sod_retinue_post_battle_disabled = 1

sod_retinue_battle_hire_none = 0
sod_retinue_battle_hire_hired = 1
sod_retinue_battle_hire_opted_out = 2
sod_retinue_battle_hire_no_trust = 3
sod_retinue_battle_hire_no_capacity = 4
sod_retinue_battle_hire_no_gold = 5
sod_retinue_battle_hire_no_leftovers = 6
sod_retinue_battle_hire_no_order = 7

sod_retinue_departure_cleanup = 0
sod_retinue_departure_peaceful = 1
sod_retinue_departure_angry = 2
sod_retinue_departure_captured = 3

sod_retinue_max_command_purse = 200000
sod_retinue_half_strength_tolerance = 2

sod_retinue_pref_general = 0
sod_retinue_pref_scout_irregular = 1
sod_retinue_pref_trade_guard = 2
sod_retinue_pref_mercy_guard = 3
sod_retinue_pref_noble_guard = 4
sod_retinue_pref_horse_archer = 5
sod_retinue_pref_redeemed_infantry = 6
sod_retinue_pref_archer_tracker = 7
sod_retinue_pref_shield_wall = 8
sod_retinue_pref_field_captain = 9
sod_retinue_pref_crossbow_veteran = 10
sod_retinue_pref_household_guard = 11
sod_retinue_pref_healer_escort = 12
sod_retinue_pref_glory_cavalry = 13
sod_retinue_pref_drilled_infantry = 14
sod_retinue_pref_engineer_support = 15
sod_retinue_pref_skirmisher = 16

# Cassian Varro mentor system. This is separate from normal companion approval:
# he is a family mentor and strategic conscience, not a normal company recruit.
slot_troop_sod_mentor_trust = 306
slot_troop_sod_mentor_arc_stage = 307
slot_troop_sod_mentor_warning_state = 308
slot_troop_sod_mentor_last_reaction_day = 309
slot_troop_sod_mentor_legion_memory = 310
slot_troop_sod_mentor_first_imperial_victory = 311
slot_troop_sod_mentor_centurion_death = 312
slot_troop_sod_mentor_alliance_victory = 313
slot_troop_sod_mentor_ruthless_victory = 314
slot_troop_sod_mentor_final_closure = 315
slot_troop_sod_mentor_last_front_warning_day = 316
slot_troop_sod_mentor_last_treaty_comment_day = 317

sod_companion_approval_near_breaking = 0
sod_companion_approval_troubled = 1
sod_companion_approval_wary = 2
sod_companion_approval_steady = 3
sod_companion_approval_loyal = 4
sod_companion_approval_devoted = 5

sod_companion_warning_none = 0
sod_companion_warning_pending = 1
sod_companion_warning_acknowledged = 2
sod_companion_warning_final = 3
sod_companion_warning_redeemed = 4
sod_companion_warning_broken = 5

sod_companion_role_none = 0
sod_companion_role_quartermaster = 1
sod_companion_role_surgeon = 2
sod_companion_role_scout = 3
sod_companion_role_captain = 4
sod_companion_role_envoy = 5
sod_companion_role_engineer = 6
sod_companion_role_spymaster = 7

sod_companion_quest_none = 0
sod_companion_quest_trust_unlocked = 1
sod_companion_quest_test_started = 2
sod_companion_quest_resolved_good = 3
sod_companion_quest_resolved_hard = 4
sod_companion_quest_failed = 5

sod_companion_campaign_mode_dialog = 1
sod_companion_campaign_mode_travel = 2
sod_companion_campaign_mode_scene = 3
sod_companion_campaign_mode_battle = 4
sod_companion_campaign_mode_away_allowed = 5

sod_companion_focus_refugee_shelter = 1
sod_companion_focus_trail_pressure = 2
sod_companion_focus_restitution_village = 3

sod_companion_action_free_captives = 1
sod_companion_action_sell_prisoners = 2
sod_companion_action_buy_slaves = 3
sod_companion_action_carry_slaves = 4
sod_companion_action_execute_lord = 5
sod_companion_action_help_village = 6
sod_companion_action_abuse_village = 7
sod_companion_action_train_troops = 8
sod_companion_action_defeat_imperials = 9
sod_companion_action_retreat_or_fail = 10
sod_companion_action_black_khergit_tribute = 11
sod_companion_action_black_khergit_bribe = 12
sod_companion_action_jotnar_support = 13
sod_companion_action_elephant_guard_support = 14
sod_companion_action_safe_roadcraft = 15
sod_companion_action_costly_battle = 16
sod_companion_action_orderly_profit = 17
sod_companion_action_dirty_profit = 18
sod_companion_action_food_security = 19
sod_companion_action_hunger = 20
sod_companion_action_stealth_success = 21
sod_companion_action_betray_autonomy = 22
sod_companion_action_hard_victory = 23
sod_companion_action_cowardice = 24
sod_companion_action_trade_profit = 25
sod_companion_action_caravan_protection = 26
sod_companion_action_unpaid_wages = 27
sod_companion_action_honorable_peace = 28
sod_companion_action_diplomacy_betrayal = 29
sod_companion_action_siege_preparation = 30
sod_companion_action_scout_warning = 31
sod_companion_action_black_khergit_camp_defeat = 32
sod_companion_action_build_healing = 33
sod_companion_action_build_market = 34
sod_companion_action_black_army_security = 35
sod_companion_action_tournament_glory = 36
sod_companion_action_build_security = 37
sod_companion_action_efficient_construction = 38
sod_companion_action_ymira_refugee_mercy = 39
sod_companion_action_ymira_refugee_expedience = 40
sod_companion_action_lezalit_ief_reform = 41
sod_companion_action_lezalit_ief_harsh = 42
sod_companion_action_tavern_recreation = 43
sod_companion_action_religious_rites = 44
sod_companion_action_strict_discipline = 45
sod_companion_action_peaceful_desertion_allowed = 46
sod_companion_action_peaceful_desertion_forbidden = 47
sod_companion_action_threatened_troops = 48
sod_companion_action_mutiny_negotiated = 49
sod_companion_action_mutiny_suppressed = 50
sod_companion_action_fair_pay = 51
sod_companion_action_bonus_pay = 52
sod_companion_action_half_pay = 53
sod_companion_action_delayed_pay = 54
sod_companion_action_veteran_pay = 55
sod_companion_action_wounded_pay = 56
sod_companion_action_broken_pay_promise = 57
sod_companion_action_generous_rations = 58
sod_companion_action_thin_rations = 59
sod_companion_action_officer_austerity = 60
sod_companion_action_ration_feast = 61
sod_companion_action_petition_mediated = 62
sod_companion_action_drunken_disorder = 63
sod_companion_action_debt_honesty = 64
sod_companion_action_road_practicality = 65
sod_companion_action_empty_speech = 66
sod_companion_action_castle_patrol_village_shield = 67
sod_companion_action_castle_patrol_road_control = 68
sod_companion_action_castle_patrol_border_harass = 69
sod_companion_action_castle_patrol_caravan_screen = 70
sod_companion_action_castle_patrol_abuse = 71
sod_companion_action_castle_patrol_scout_report = 72
sod_companion_action_castle_patrol_quartermaster = 73
sod_companion_action_cassian_last_order_sabotage = 74
sod_companion_action_cassian_last_order_rescue = 75
sod_companion_action_cassian_last_order_expose = 76
sod_companion_action_cassian_last_order_burn = 77
sod_companion_action_battle_defeat = 78
sod_companion_action_morale_collapse = 79
sod_companion_action_commander_duel_won = 80
sod_companion_action_commander_duel_lost = 81
sod_companion_action_mutiny_battle = 82
sod_companion_action_hard_compromise = 83
sod_companion_action_trade_loss = 84

sod_mentor_trust_bitter = 0
sod_mentor_trust_strained = 1
sod_mentor_trust_watchful = 2
sod_mentor_trust_confident = 3
sod_mentor_trust_reverent = 4

sod_mentor_arc_none = 0
sod_mentor_arc_old_hand = 1
sod_mentor_arc_court_counsel = 2
sod_mentor_arc_shadow_legion = 3
sod_mentor_arc_last_order = 4

sod_mentor_warning_none = 0
sod_mentor_warning_watchful = 1
sod_mentor_warning_strained = 2
sod_mentor_warning_bitter = 3

sod_mentor_last_order_none = 0
sod_mentor_last_order_opened = 1
sod_mentor_last_order_network_found = 2
sod_mentor_last_order_sabotage = 3
sod_mentor_last_order_rescue = 4
sod_mentor_last_order_exposed = 5
sod_mentor_last_order_burned = 6

# Company accounts: manual payday foundation.
sod_company_troop_class_enlisted = 0
sod_company_troop_class_mercenary = 1
sod_company_troop_class_noble = 2
sod_company_troop_class_faith = 3

sod_company_pay_choice_full = 1
sod_company_pay_choice_half = 2
sod_company_pay_choice_bonus = 3
sod_company_pay_choice_delay = 4
sod_company_pay_choice_veterans = 5
sod_company_pay_choice_wounded = 6

sod_company_growth_recruit = 1
sod_company_growth_upgrade = 2

sod_company_promise_response_standard = 1
sod_company_threat_response_discipline = 1

sod_company_pay_confidence_trusted = 0
sod_company_pay_confidence_steady = 1
sod_company_pay_confidence_watchful = 2
sod_company_pay_confidence_doubtful = 3
sod_company_pay_confidence_angry = 4
sod_company_pay_confidence_broken = 5

sod_company_camp_strain_calm = 0
sod_company_camp_strain_frayed = 1
sod_company_camp_strain_bitter = 2
sod_company_camp_strain_dangerous = 3
sod_company_camp_strain_splintering = 4

sod_company_ration_policy_thin = 0
sod_company_ration_policy_standard = 1
sod_company_ration_policy_generous = 2
sod_company_ration_policy_officer_austerity = 3

sod_company_ration_confidence_well_fed = 0
sod_company_ration_confidence_adequate = 1
sod_company_ration_confidence_thin = 2
sod_company_ration_confidence_hungry = 3
sod_company_ration_confidence_starving = 4

sod_company_recreation_none = 0
sod_company_recreation_tavern_round = 1
sod_company_recreation_lodging = 2
sod_company_recreation_strict_discipline = 3
sod_company_recreation_arena_prestige = 4
sod_company_recreation_campfire = 5
sod_company_recreation_religious_rites = 6
sod_company_recreation_company_offering = 7
sod_company_recreation_wounded_care = 8
sod_company_recreation_tavern_rumors = 9
sod_company_recreation_own_coin = 10
sod_company_recreation_village_festival = 11

sod_company_recreation_incident_none = 0
sod_company_recreation_incident_drunken_brawl = 1
sod_company_recreation_incident_gambling_debt = 2
sod_company_recreation_incident_missing_soldier = 3
sod_company_recreation_incident_insulted_noble = 4
sod_company_recreation_incident_mercenary_overindulgence = 5
sod_company_recreation_incident_local_fine = 6

sod_company_prestige_none = 0
sod_company_prestige_battle = 1
sod_company_prestige_tournament = 2
sod_company_prestige_public_honor = 3

sod_company_noble_restlessness_calm = 0
sod_company_noble_restlessness_proud = 1
sod_company_noble_restlessness_restless = 2
sod_company_noble_restlessness_insulted = 3
sod_company_noble_restlessness_withdrawing = 4

sod_company_petition_none = 0
sod_company_petition_pay_arrears = 1
sod_company_petition_thin_rations = 2
sod_company_petition_noble_restlessness = 3
sod_company_petition_camp_strain = 4
sod_company_petition_wounded_care = 5

sod_company_petition_stage_none = 0
sod_company_petition_stage_murmur = 1
sod_company_petition_stage_formal = 2
sod_company_petition_stage_urgent = 3

sod_company_desertion_stage_none = 0
sod_company_desertion_stage_watching = 1
sod_company_desertion_stage_request = 2
sod_company_desertion_stage_urgent = 3

sod_company_desertion_response_paid = 1
sod_company_desertion_response_persuade = 2
sod_company_desertion_response_unpaid = 3
sod_company_desertion_response_forbid = 4
sod_company_desertion_response_battle_promise = 5

sod_company_mutiny_stage_none = 0
sod_company_mutiny_stage_warning = 1
sod_company_mutiny_stage_final_warning = 2
sod_company_mutiny_stage_breaking = 3

sod_company_mutiny_response_negotiate = 1
sod_company_mutiny_response_pay = 2
sod_company_mutiny_response_threaten = 3
sod_company_mutiny_response_drill = 4

sod_company_mutiny_resolution_none = 0
sod_company_mutiny_resolution_settlement = 1
sod_company_mutiny_resolution_ringleaders_expelled = 2
sod_company_mutiny_resolution_deferred = 3
sod_company_mutiny_resolution_battle = 4

sod_company_spokesperson_none = 0
sod_company_spokesperson_pay_arrears = 1
sod_company_spokesperson_thin_rations = 2
sod_company_spokesperson_wounded_care = 3
sod_company_spokesperson_hazard_pay = 4
sod_company_spokesperson_noble_honor = 5
sod_company_spokesperson_faith_rites = 6
sod_company_spokesperson_battle_promise_due = 7
sod_company_spokesperson_defeat_shock = 8
sod_company_spokesperson_victory_spoils = 9
sod_company_spokesperson_discipline_threat = 10

sod_company_spokesperson_response_pay_now = 1
sod_company_spokesperson_response_promise = 2
sod_company_spokesperson_response_battle_promise = 3
sod_company_spokesperson_response_ration_change = 4
sod_company_spokesperson_response_recreation = 5
sod_company_spokesperson_response_rites_wounded = 6
sod_company_spokesperson_response_public_honors = 7
sod_company_spokesperson_response_persuade = 8
sod_company_spokesperson_response_mediation = 9
sod_company_spokesperson_response_threaten = 10
sod_company_spokesperson_response_dismiss = 11
sod_company_spokesperson_response_hazard_pay = 12
sod_company_spokesperson_response_victory_feast = 13
sod_company_spokesperson_response_refuse_spectacle = 14
sod_company_spokesperson_response_company_offering = 15

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

# Lightweight NPC lord party morale. This is intentionally smaller than the
# player company accounts system; it feeds strategic caution and battle rout.
slot_troop_sod_lord_party_morale = 283
slot_troop_sod_lord_pay_strain = 284
slot_troop_sod_lord_campaign_fatigue = 285
slot_troop_sod_lord_last_pay_day = 286
slot_troop_sod_lord_last_victory_day = 287
slot_troop_sod_lord_last_defeat_day = 288
slot_troop_sod_lord_last_morale_update_day = 289
slot_troop_sod_lord_recent_battle_confidence = 290
slot_troop_sod_lord_supply_confidence = 291
slot_troop_sod_lord_last_desertion_day = 292
slot_troop_sod_lord_last_battle_refusal_day = 293
slot_troop_sod_lord_last_morale_broken_event_day = 294
slot_troop_sod_lord_last_home_morale_event_day = 295
slot_troop_sod_lord_last_pay_strain_event_day = 296
slot_troop_sod_lord_last_exhaustion_event_day = 297
slot_troop_sod_lord_last_confident_campaign_event_day = 298
slot_troop_sod_lord_strategic_intent = 299
slot_troop_sod_lord_last_intent_day = 300
slot_troop_sod_lord_intent_target = 301
slot_troop_sod_lord_last_dangerous_target = 302
slot_troop_sod_lord_last_failed_siege_day = 303
slot_troop_sod_lord_last_profitable_raid_target = 304
slot_troop_sod_lord_last_profitable_raid_day = 305
slot_troop_sod_lord_land_satisfaction = 343
slot_troop_sod_lord_ruler_confidence = 344
slot_troop_sod_lord_last_land_grievance_day = 345
slot_troop_sod_lord_fief_expectation = 346
slot_troop_sod_lord_patron_target_faction = 347
slot_troop_sod_lord_last_patron_seek_day = 348
slot_troop_sod_lord_last_patron_offer_day = 349
slot_troop_sod_lord_last_petition_day = 350
slot_troop_sod_lord_last_poached_day = 351
slot_troop_sod_nemesis_defeats = 352
slot_troop_sod_nemesis_strength = 353
slot_troop_sod_nemesis_duel_pressure = 354
slot_troop_sod_nemesis_last_duel_day = 355
slot_troop_sod_nemesis_duel_wins = 356
slot_troop_sod_nemesis_adaptation = 357
slot_troop_sod_nemesis_adaptation_count = 358
slot_troop_sod_nemesis_mercy_count = 359
slot_troop_sod_nemesis_capture_count = 360
slot_troop_sod_nemesis_humiliation_count = 361

# Black Khergit Khan personal scaling.
slot_troop_black_khergit_khan_duel_losses = 362

# Lightweight noble-house identity. This sits beside Native family slots
# instead of trying to turn one-spouse/one-child slots into a dynasty tree.
slot_troop_sod_house_id = 363
slot_troop_sod_house_rank = 364
slot_troop_sod_house_head = 365
slot_troop_sod_house_grievance = 366
slot_troop_sod_house_loyalty = 367
slot_troop_sod_house_claim_strength = 368
slot_troop_sod_pretender_claim_pressure = 369
slot_troop_sod_pretender_foothold_center = 370
slot_troop_sod_pretender_backer_lord = 371
slot_troop_sod_pretender_last_action_day = 372
slot_troop_sod_pretender_momentum = 373
slot_troop_sod_claimant_allegiance = 374
slot_troop_sod_claimant_parent_faction = 375
slot_troop_sod_claimant_rebel_faction = 376
slot_troop_sod_claimant_join_day = 377
slot_troop_sod_claimant_commitment = 378
slot_troop_sod_claimant_last_offer_day = 379
slot_troop_sod_claimant_old_ruler_status = 380
slot_troop_sod_claimant_old_ruler_defeated_day = 381
slot_troop_duel_won = 382
slot_troop_duel_lost = 383
slot_troop_duel_started = 384
slot_troop_duel_daily = 385
slot_troop_duel_daily_day = 386
slot_troop_sod_times_took_command = 387
slot_troop_sod_post_fall_victories = 388
slot_troop_sod_post_fall_failures = 389
slot_troop_sod_last_took_command_hours = 390
duel_daily_limit = 4

sod_house_rank_none = 0
sod_house_rank_ruler = 1
sod_house_rank_lord = 2
sod_house_rank_lady = 3
sod_house_rank_pretender = 4
sod_house_rank_named_actor = 5

sod_claimant_allegiance_none = 0
sod_claimant_allegiance_secret_sympathizer = 1
sod_claimant_allegiance_open_rebel = 2
sod_claimant_allegiance_defeated_loyalist = 3
sod_claimant_allegiance_reconciled = 4
sod_claimant_allegiance_old_ruler_remnant = 5

sod_old_ruler_status_none = 0
sod_old_ruler_status_exiled = 1
sod_old_ruler_status_remnant_claimant = 2
sod_old_ruler_status_reconciled = 3

sod_civil_war_none = 0
sod_civil_war_shadow_court = 1
sod_civil_war_open_rebellion = 2
sod_civil_war_rebel_victory = 3
sod_civil_war_loyalist_victory = 4
sod_civil_war_cooldown = 5

sod_pretender_pressure_quiet = 34
sod_pretender_pressure_stirring = 49
sod_pretender_pressure_foothold = 64
sod_pretender_pressure_dangerous = 100

sod_repair_service_all = 0
sod_repair_service_weapons = 1
sod_repair_service_armor = 2
sod_repair_service_horses = 3
sod_repair_service_ranged = 4
sod_repair_service_melee = 5
sod_repair_service_heavy_armor = 6
sod_repair_service_light_clothes = 7

sod_camp_job_none = 0
sod_camp_job_scout_route = 1
sod_camp_job_forage_hunt = 2
sod_camp_job_repair_gear = 3
sod_camp_job_ration_stores = 4
sod_camp_job_tend_mounts = 5
sod_camp_job_end = 6

sod_camp_job_result_none = 0
sod_camp_job_result_success = 1
sod_camp_job_result_no_effect = 2
sod_camp_job_result_cancelled = 3

sod_camp_passive_job_none = 0
sod_camp_passive_job_scout_route = 1
sod_camp_passive_job_count_stores = 2
sod_camp_passive_job_hold_rites = 3
sod_camp_passive_job_enforce_order = 4
sod_camp_passive_job_tend_mounts = 5
sod_camp_passive_job_patrol_pickets = 6
sod_camp_passive_job_hunt_game = 7
sod_camp_passive_job_repair_heavy_armor = 8
sod_camp_passive_job_restore_discipline = 9
sod_camp_passive_job_repair_ranged = 10
sod_camp_passive_job_mend_clothes = 11
sod_camp_passive_job_treat_wounded = 12
sod_camp_passive_job_probe_openings = 13
sod_camp_passive_job_repair_melee = 14
sod_camp_passive_job_prepare_siege = 15
sod_camp_passive_job_study_gates = 16
sod_camp_passive_job_end = 17

sod_camp_pressure_scout_route = 40
sod_camp_pressure_count_stores = 80
sod_camp_pressure_hold_rites = 200
sod_camp_pressure_enforce_order = 100
sod_camp_pressure_tend_mounts = 140
sod_camp_pressure_patrol_pickets = 60
sod_camp_pressure_hunt_game = 50
sod_camp_pressure_repair_heavy_armor = 180
sod_camp_pressure_restore_discipline = 120
sod_camp_pressure_repair_ranged = 110
sod_camp_pressure_mend_clothes = 70
sod_camp_pressure_treat_wounded = 90
sod_camp_pressure_probe_openings = 100
sod_camp_pressure_repair_melee = 120
sod_camp_pressure_prepare_siege = 220
sod_camp_pressure_study_gates = 160

sod_lord_morale_broken_max = 19
sod_lord_morale_shaken_max = 39
sod_lord_morale_wary_max = 59
sod_lord_morale_steady_max = 79
sod_lord_morale_confident_max = 100

sod_lord_intent_none = 0
sod_lord_intent_recovering = 1
sod_lord_intent_defending_home = 2
sod_lord_intent_seeking_pay = 3
sod_lord_intent_raiding_for_cash = 4
sod_lord_intent_following_marshal = 5
sod_lord_intent_patrolling_border = 6
sod_lord_intent_hunting_weak_party = 7
sod_lord_intent_siege_ready = 8
sod_lord_intent_independent_campaign = 9
sod_lord_intent_disgruntled_landless = 10
sod_lord_intent_seeking_patron = 11

sod_campaign_posture_none = 0
sod_campaign_posture_offensive_siege = 1
sod_campaign_posture_defensive_rally = 2
sod_campaign_posture_recovery = 3
sod_campaign_posture_raiding = 4
sod_campaign_posture_hunting = 5
sod_campaign_posture_border_patrol = 6
sod_campaign_posture_gathering = 7

sod_campaign_reason_none = 0
sod_campaign_reason_high_health = 1
sod_campaign_reason_threatened_center = 2
sod_campaign_reason_low_health = 3
sod_campaign_reason_unpaid_tired_lords = 4
sod_campaign_reason_enemy_weakness = 5
sod_campaign_reason_poor_economy = 6
sod_campaign_reason_recent_failed_siege = 7
sod_campaign_reason_marshal_opportunity = 8

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
slot_item_sod_auto_loot_protected    = 169

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

# Lightweight Nemesis Memory. True named nemeses should point at existing
# non-Imperial lords; hostile-road parties remain anonymous grudge pressure.
sod_nemesis_actor_none = 0
sod_nemesis_actor_outlaw = 1
sod_nemesis_actor_deserter = 2
sod_nemesis_actor_contract_threat = 3
sod_nemesis_actor_lord = 4
sod_nemesis_actor_companion_rival = 5

sod_nemesis_reason_none = 0
sod_nemesis_reason_mercy = 1
sod_nemesis_reason_recruitment = 2
sod_nemesis_reason_prisoners = 3
sod_nemesis_reason_informants = 4
sod_nemesis_reason_humiliation = 5
sod_nemesis_reason_robbed = 6
sod_nemesis_reason_paid_tolls = 7
sod_nemesis_reason_deserter_killer = 8
sod_nemesis_reason_refugee_shelter = 9
sod_nemesis_reason_battle_defeat = 10
sod_nemesis_reason_lord_defeat = 11

sod_nemesis_adaptation_none = 0
sod_nemesis_adaptation_anti_cavalry = 1
sod_nemesis_adaptation_anti_ranged = 2
sod_nemesis_adaptation_anti_duel = 3
sod_nemesis_adaptation_anti_melee = 4

sod_nemesis_lord_resolution_capture = 1
sod_nemesis_lord_resolution_mercy = 2
sod_nemesis_lord_resolution_humiliation = 3

sod_nemesis_state_none = 0
sod_nemesis_state_watching = 1
sod_nemesis_state_hunting = 2
sod_nemesis_state_spent = 3

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

# Road to the Crown campaign state.
# These are quest-owned slots used by the first campaign slice. Starting
# identity still comes from the existing character creation globals.
slot_quest_rtc_campaign_id = 125
slot_quest_rtc_act = 126
slot_quest_rtc_chapter = 127
slot_quest_rtc_origin = 128
slot_quest_rtc_faith = 129
slot_quest_rtc_life = 130
slot_quest_rtc_motive = 131
slot_quest_rtc_reputation = 132
slot_quest_rtc_commoner_trust = 133
slot_quest_rtc_merchant_trust = 134
slot_quest_rtc_noble_trust = 135
slot_quest_rtc_imperial_pressure = 136
slot_quest_rtc_salvage_choice = 137
slot_quest_rtc_method_seed = 138
slot_quest_rtc_branch_seed = 139
slot_quest_rtc_companion_pressure = 140
slot_quest_rtc_flags = 141
slot_quest_rtc_social_contact = 142
slot_quest_rtc_final_ending = 143
slot_quest_rtc_successor_unlock = 144

# The Seven Oaths of Ash campaign state.
# Quest-owned slots for the Ashwick village-defense campaign.
slot_quest_seven_ash_campaign_status = 145
slot_quest_seven_ash_active_stage = 146
slot_quest_seven_ash_active_recruit_id = 147
slot_quest_seven_ash_act2_board_open = 148
slot_quest_seven_ash_act2_resolved_count = 149
slot_quest_seven_ash_act2_complete = 150
slot_quest_seven_ash_act3_pressure_started = 151
slot_quest_seven_ash_days_remaining = 152
slot_quest_seven_ash_wulfred_pressure = 153
slot_quest_seven_ash_settlement_strain = 154
slot_quest_seven_ash_player_strength_ultimatum = 155
slot_quest_seven_ash_player_strength_siege = 156
slot_quest_seven_ash_wulfred_host_strength = 157
slot_quest_seven_ash_wulfred_elite_core = 158
slot_quest_seven_ash_morale = 159
slot_quest_seven_ash_food = 160
slot_quest_seven_ash_labor = 161
slot_quest_seven_ash_fortification = 162
slot_quest_seven_ash_training = 163
slot_quest_seven_ash_intelligence = 164
slot_quest_seven_ash_civilian_safety = 165
slot_quest_seven_ash_elder_trust = 166
slot_quest_seven_ash_youth_trust = 167
slot_quest_seven_ash_farmer_trust = 168
slot_quest_seven_ash_refugee_trust = 169
slot_quest_seven_ash_recruited_bitmask = 170
slot_quest_seven_ash_survival_bitmask = 171
slot_quest_seven_ash_companion_unlock_bitmask = 172
slot_quest_seven_ash_companion_refusal_bitmask = 173
slot_quest_seven_ash_defender_bond_flags = 174
slot_quest_seven_ash_defender_conflict_flags = 175
slot_quest_seven_ash_final_plan = 176
slot_quest_seven_ash_result_grade = 177
slot_quest_seven_ash_garric_status = 178
slot_quest_seven_ash_oswin_status = 179
slot_quest_seven_ash_aldrik_status = 180
slot_quest_seven_ash_mirelle_status = 181
slot_quest_seven_ash_tomas_status = 182
slot_quest_seven_ash_beren_status = 183
slot_quest_seven_ash_elianor_status = 184
slot_quest_seven_ash_garric_route = 185
slot_quest_seven_ash_oswin_route = 186
slot_quest_seven_ash_garric_evidence = 187
slot_quest_seven_ash_oswin_evidence = 188
slot_quest_seven_ash_garric_return_applied = 189
slot_quest_seven_ash_oswin_return_applied = 190
slot_quest_seven_ash_garric_trust = 191
slot_quest_seven_ash_garric_fear = 192
slot_quest_seven_ash_oswin_trust = 193
slot_quest_seven_ash_oswin_debt = 194
slot_quest_seven_ash_oswin_fear = 195
slot_quest_seven_ash_aldrik_route = 196
slot_quest_seven_ash_aldrik_evidence = 197
slot_quest_seven_ash_aldrik_return_applied = 198
slot_quest_seven_ash_aldrik_trust = 199
slot_quest_seven_ash_aldrik_pride = 200
slot_quest_seven_ash_aldrik_debt = 201
slot_quest_seven_ash_aldrik_fear = 202
slot_quest_seven_ash_mirelle_route = 203
slot_quest_seven_ash_mirelle_evidence = 204
slot_quest_seven_ash_mirelle_return_applied = 205
slot_quest_seven_ash_mirelle_trust = 206
slot_quest_seven_ash_mirelle_debt = 207
slot_quest_seven_ash_mirelle_fear = 208
slot_quest_seven_ash_mirelle_spy_support = 209
slot_quest_seven_ash_tomas_route = 210
slot_quest_seven_ash_tomas_evidence = 211
slot_quest_seven_ash_tomas_return_applied = 212
slot_quest_seven_ash_tomas_trust = 213
slot_quest_seven_ash_tomas_respect = 214
slot_quest_seven_ash_tomas_fear = 215
slot_quest_seven_ash_tomas_discipline_support = 216
slot_quest_seven_ash_beren_route = 217
slot_quest_seven_ash_beren_evidence = 218
slot_quest_seven_ash_beren_return_applied = 219
slot_quest_seven_ash_beren_trust = 220
slot_quest_seven_ash_beren_pride = 221
slot_quest_seven_ash_beren_fear = 222
slot_quest_seven_ash_beren_breach_support = 223
slot_quest_seven_ash_elianor_route = 224
slot_quest_seven_ash_elianor_evidence = 225
slot_quest_seven_ash_elianor_return_applied = 226
slot_quest_seven_ash_elianor_trust = 227
slot_quest_seven_ash_elianor_refugee_trust = 228
slot_quest_seven_ash_elianor_fear = 229
slot_quest_seven_ash_elianor_infirmary_support = 230
slot_quest_seven_ash_pressure_interlude_active = 231
slot_quest_seven_ash_pressure_interlude_resolved_bits = 232
slot_quest_seven_ash_sector_outer_fields = 233
slot_quest_seven_ash_sector_palisade = 234
slot_quest_seven_ash_sector_gate_reserve = 235
slot_quest_seven_ash_sector_inner_streets = 236
slot_quest_seven_ash_sector_churchyard = 237
slot_quest_seven_ash_sector_evacuation = 238
slot_quest_seven_ash_sector_commitment_locked = 239
slot_quest_seven_ash_siege_phase_active = 240
slot_quest_seven_ash_outer_wave_count = 241
slot_quest_seven_ash_outer_enemy_committed = 242
slot_quest_seven_ash_outer_result = 243
slot_quest_seven_ash_outer_casualty_pressure = 244
slot_quest_seven_ash_palisade_wave_count = 245
slot_quest_seven_ash_palisade_enemy_committed = 246
slot_quest_seven_ash_palisade_result = 247
slot_quest_seven_ash_palisade_breach_pressure = 248
slot_quest_seven_ash_breach_wave_count = 249
slot_quest_seven_ash_breach_enemy_committed = 250
slot_quest_seven_ash_breach_result = 251
slot_quest_seven_ash_breach_street_pressure = 252
slot_quest_seven_ash_inner_wave_count = 253
slot_quest_seven_ash_inner_enemy_committed = 254
slot_quest_seven_ash_inner_result = 255
slot_quest_seven_ash_inner_churchyard_pressure = 256
slot_quest_seven_ash_churchyard_wave_count = 257
slot_quest_seven_ash_churchyard_enemy_committed = 258
slot_quest_seven_ash_churchyard_result = 259
slot_quest_seven_ash_wulfred_outcome = 260
slot_quest_seven_ash_civilian_deaths = 261
slot_quest_seven_ash_burned_homes = 262
slot_quest_seven_ash_surviving_defender_count = 263
slot_quest_seven_ash_promises_kept = 264
slot_quest_seven_ash_prisoner_treatment = 265
slot_quest_seven_ash_settlement_outcome = 266
slot_quest_seven_ash_companion_joined_bitmask = 267
slot_quest_seven_ash_companion_stayed_bitmask = 268
slot_quest_seven_ash_act2_pacing_flags = 269
slot_quest_seven_ash_act2_last_tick_day = 270
slot_quest_seven_ash_sector_leader_bitmask = 271
slot_quest_seven_ash_memorial_bitmask = 272
slot_quest_seven_ash_ending_flags = 273

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

sod_rtc_campaign_none = 0
sod_rtc_campaign_road_to_crown = 1

sod_rtc_act_none = 0
sod_rtc_act_ashes = 1
sod_rtc_act_choice = 2
sod_rtc_act_standing = 3
sod_rtc_act_crown = 4
sod_rtc_act_shadow = 5

sod_rtc_chapter_none = 0
sod_rtc_chapter_last_smoke = 1
sod_rtc_chapter_borrowed_names = 2
sod_rtc_chapter_hound_sign = 3
sod_rtc_chapter_door_into_calradia = 4
sod_rtc_chapter_price_of_bread = 5
sod_rtc_chapter_three_offers = 6
sod_rtc_chapter_companions_take_sides = 7
sod_rtc_chapter_first_recognition = 8
sod_rtc_chapter_crown_council = 9
sod_rtc_chapter_hounds_terms = 10
sod_rtc_chapter_war_of_witnesses = 11
sod_rtc_chapter_last_road = 12
sod_rtc_chapter_final_confrontation = 13

sod_rtc_reputation_none = 0
sod_rtc_reputation_refugee = 1
sod_rtc_reputation_foreign_noble = 2
sod_rtc_reputation_free_captain = 3
sod_rtc_reputation_trade_operator = 4
sod_rtc_reputation_avenger = 5
sod_rtc_reputation_unproven = 6

sod_rtc_pressure_none = 0
sod_rtc_pressure_low = 1
sod_rtc_pressure_rising = 2
sod_rtc_pressure_open = 3
sod_rtc_pressure_invasion = 4

sod_rtc_salvage_none = 0
sod_rtc_salvage_wounded = 1
sod_rtc_salvage_baggage = 2
sod_rtc_salvage_papers = 3
sod_rtc_salvage_abandoned = 4

sod_rtc_method_none = 0
sod_rtc_method_honor = 1
sod_rtc_method_intrigue = 2
sod_rtc_method_trade = 3
sod_rtc_method_counsel = 4
sod_rtc_method_faith = 5

sod_rtc_branch_none = 0
sod_rtc_branch_legitimacy = 1
sod_rtc_branch_mercenary = 2
sod_rtc_branch_conquest = 3
sod_rtc_branch_coalition = 4
sod_rtc_branch_restoration = 5
sod_rtc_branch_imperial = 6
sod_rtc_branch_regime_maker = 7
sod_rtc_branch_fractured_claim = 8

sod_rtc_council_answer_bread_witness = 101
sod_rtc_council_answer_merchant_books = 102

sod_rtc_stop_none = 0
sod_rtc_stop_act_01_survived = 1
sod_rtc_stop_act_01_poor_start = 2

sod_rtc_contact_none = 0
sod_rtc_contact_noble = 1
sod_rtc_contact_merchant = 2
sod_rtc_contact_gate_captain = 3
sod_rtc_contact_village = 4
sod_rtc_contact_road_scout = 5

sod_rtc_flag_origin_set = 1
sod_rtc_flag_faith_set = 2
sod_rtc_flag_life_set = 4
sod_rtc_flag_motive_set = 8
sod_rtc_flag_campaign_started = 16
sod_rtc_flag_companion_wary_mercy = 32
sod_rtc_flag_commoner_trust_high = 64
sod_rtc_flag_commoner_trust_low = 128
sod_rtc_flag_merchant_trust_high = 256
sod_rtc_flag_merchant_trust_low = 512
sod_rtc_flag_noble_trust_high = 1024
sod_rtc_flag_noble_trust_low = 2048
sod_rtc_flag_village_fear = 4096
sod_rtc_flag_route_reform = 8192
sod_rtc_flag_route_betrayal = 16384
sod_rtc_flag_route_hidden_regime_maker = 32768
sod_rtc_flag_witness_noble = 65536
sod_rtc_flag_witness_commoner = 131072
sod_rtc_flag_witness_company = 262144
sod_rtc_flag_witness_fourth = 524288
sod_rtc_flag_challenge_maeron = 1048576
sod_rtc_flag_offer_septima = 2097152
sod_rtc_flag_leverage_vaska = 4194304
sod_rtc_flag_route_locked = 8388608
sod_rtc_flag_envoy_accusation_turned = 16777216

sod_rtc_offer_none = 0
sod_rtc_offer_noble_protection = 1
sod_rtc_offer_paid_steel = 2
sod_rtc_offer_peoples_road = 3
sod_rtc_offer_hard_claim = 4
sod_rtc_offer_quiet_ledger = 5
sod_rtc_offer_bread_oath = 101
sod_rtc_offer_books_oath = 102
sod_rtc_offer_witness_oath = 103

sod_rtc_recognition_none = 0
sod_rtc_recognition_lawful_claimant = 1
sod_rtc_recognition_free_captain = 2
sod_rtc_recognition_trade_power = 3
sod_rtc_recognition_people_defender = 4
sod_rtc_recognition_dangerous_warlord = 5
sod_rtc_recognition_shadow_operator = 6

sod_rtc_terms_none = 0
sod_rtc_terms_rejected = 1
sod_rtc_terms_delay_negotiated = 2
sod_rtc_terms_accepted = 3
sod_rtc_terms_collapsed = 4

sod_rtc_witness_war_none = 0
sod_rtc_witness_war_protect = 1
sod_rtc_witness_war_sacrifice = 2
sod_rtc_witness_war_route_variant = 3
sod_rtc_witness_war_side_crisis = 4
sod_rtc_witness_war_envoy_leverage = 5

sod_rtc_last_road_none = 0
sod_rtc_last_road_hold_line = 1
sod_rtc_last_road_strike_hound = 2
sod_rtc_last_road_starve_empire = 3
sod_rtc_last_road_break_seal = 4
sod_rtc_last_road_accept_collar = 5
sod_rtc_last_road_catastrophic_loss = 6
sod_rtc_last_road_turn_accusation = 7

sod_rtc_final_none = 0
sod_rtc_final_marius_defeated = 1
sod_rtc_final_marius_forced_back = 2
sod_rtc_final_marius_overlord = 3
sod_rtc_final_unworn_crown = 4
sod_rtc_final_claim_collapse = 5

sod_rtc_ending_none = 0
sod_rtc_ending_crown_of_law = 1
sod_rtc_ending_crown_of_iron = 2
sod_rtc_ending_crown_of_coin = 3
sod_rtc_ending_crown_of_ashes = 4
sod_rtc_ending_crown_of_faith = 5
sod_rtc_ending_crown_of_vengeance = 6
sod_rtc_ending_crown_of_return = 7
sod_rtc_ending_crown_of_empire = 8
sod_rtc_ending_unworn_crown = 9

sod_rtc_successor_none = 0
sod_rtc_successor_governance_campaign = 1
sod_rtc_successor_rebellion_reform = 2
sod_rtc_successor_merchant_league = 3
sod_rtc_successor_exile_redemption = 4
sod_rtc_successor_schism_reform = 5
sod_rtc_successor_survivor_reckoning = 6
sod_rtc_successor_homeland_restoration = 7
sod_rtc_successor_imperial_civil_war = 8
sod_rtc_successor_league_protector = 9

sod_seven_ash_status_inactive = 0
sod_seven_ash_status_active = 1
sod_seven_ash_status_suspended = 2
sod_seven_ash_status_completed = 3
sod_seven_ash_status_failed = 4
sod_seven_ash_status_archived = 5

sod_seven_ash_stage_none = 0
sod_seven_ash_stage_ultimatum = 1
sod_seven_ash_stage_audit = 2
sod_seven_ash_stage_recruitment = 3
sod_seven_ash_stage_return = 4
sod_seven_ash_stage_pressure = 5
sod_seven_ash_stage_oath_council = 6
sod_seven_ash_stage_siege = 7
sod_seven_ash_stage_aftermath = 8

sod_seven_ash_defender_none = 0
sod_seven_ash_defender_garric = 1
sod_seven_ash_defender_oswin = 2
sod_seven_ash_defender_aldrik = 4
sod_seven_ash_defender_mirelle = 8
sod_seven_ash_defender_tomas = 16
sod_seven_ash_defender_beren = 32
sod_seven_ash_defender_elianor = 64
sod_seven_ash_defender_all = 127

sod_seven_ash_recruit_unknown = 0
sod_seven_ash_recruit_available = 1
sod_seven_ash_recruit_in_progress = 2
sod_seven_ash_recruit_recruited = 3
sod_seven_ash_recruit_refused = 4
sod_seven_ash_recruit_alienated = 5
sod_seven_ash_recruit_lost = 6
sod_seven_ash_recruit_abandoned = 7

sod_seven_ash_route_none = 0
sod_seven_ash_route_best = 1
sod_seven_ash_route_hard = 2
sod_seven_ash_route_legal_promise = 3
sod_seven_ash_route_blackmail = 4
sod_seven_ash_route_forced_service = 5
sod_seven_ash_route_refusal = 6

sod_seven_ash_evidence_none = 0
sod_seven_ash_evidence_witness = 1
sod_seven_ash_evidence_physical = 2
sod_seven_ash_evidence_public_truth = 3
sod_seven_ash_interlude_none = 0
sod_seven_ash_interlude_burned_cow = 1
sod_seven_ash_interlude_knife_marked_door = 2
sod_seven_ash_interlude_grain_riot = 4
sod_seven_ash_interlude_wulfred_offer = 8
sod_seven_ash_interlude_first_funeral = 16
sod_seven_ash_pacing_courier_10 = 1
sod_seven_ash_pacing_courier_6 = 2
sod_seven_ash_pacing_courier_3 = 4
sod_seven_ash_pacing_scout_rumor_9 = 8
sod_seven_ash_pacing_scout_rumor_5 = 16
sod_seven_ash_pacing_slow_warning = 32
sod_seven_ash_pacing_emergency_return = 64

sod_seven_ash_method_none = 0
sod_seven_ash_method_common_defense = 1
sod_seven_ash_method_public_oaths = 2
sod_seven_ash_method_paid_contracts = 3
sod_seven_ash_method_blackmail = 4
sod_seven_ash_method_hostage_surety = 5
sod_seven_ash_method_civilian_first = 6
sod_seven_ash_method_no_quarter = 7
sod_seven_ash_method_wulfred_bargain = 8

sod_seven_ash_posture_none = 0
sod_seven_ash_posture_prepare_alone = 1
sod_seven_ash_posture_find_defenders = 2
sod_seven_ash_posture_lordly_aid = 3
sod_seven_ash_posture_bargain = 4
sod_seven_ash_posture_evacuate = 5
sod_seven_ash_posture_kill_messengers = 6

sod_seven_ash_priority_none = 0
sod_seven_ash_priority_repair_palisade = 1
sod_seven_ash_priority_dig_ditch = 2
sod_seven_ash_priority_secure_granary = 3
sod_seven_ash_priority_train_militia = 4
sod_seven_ash_priority_evacuate_farms = 5
sod_seven_ash_priority_scout_road = 6

sod_seven_ash_plan_none = 0
sod_seven_ash_plan_hold_palisade = 1
sod_seven_ash_plan_defense_in_depth = 2
sod_seven_ash_plan_counterstroke = 3
sod_seven_ash_plan_cut_head = 4
sod_seven_ash_plan_empty_village = 5
sod_seven_ash_sector_none = 0
sod_seven_ash_sector_outer_fields = 1
sod_seven_ash_sector_palisade = 2
sod_seven_ash_sector_gate_reserve = 3
sod_seven_ash_sector_inner_streets = 4
sod_seven_ash_sector_churchyard = 5
sod_seven_ash_sector_evacuation = 6
sod_seven_ash_siege_phase_none = 0
sod_seven_ash_siege_phase_outer_fields = 1
sod_seven_ash_siege_phase_palisade = 2
sod_seven_ash_siege_phase_breach = 3
sod_seven_ash_siege_phase_inner_streets = 4
sod_seven_ash_siege_phase_churchyard = 5
sod_seven_ash_siege_result_unresolved = 0
sod_seven_ash_siege_result_held = 1
sod_seven_ash_siege_result_bloodied = 2
sod_seven_ash_siege_result_lost = 3
sod_seven_ash_wulfred_unresolved = 0
sod_seven_ash_wulfred_killed = 1
sod_seven_ash_wulfred_captured = 2
sod_seven_ash_wulfred_escaped = 3
sod_seven_ash_wulfred_wins = 4
sod_seven_ash_prisoners_none = 0
sod_seven_ash_prisoners_bound_for_trial = 1
sod_seven_ash_prisoners_executed = 2
sod_seven_ash_prisoners_scattered = 3
sod_seven_ash_settlement_village = 1
sod_seven_ash_settlement_fortified = 2
sod_seven_ash_settlement_refugee_camp = 3
sod_seven_ash_settlement_ruined = 4

sod_seven_ash_result_none = 0
sod_seven_ash_result_clean_victory = 1
sod_seven_ash_result_hard_victory = 2
sod_seven_ash_result_pyrrhic = 3
sod_seven_ash_result_bargain = 4
sod_seven_ash_result_evacuation = 5
sod_seven_ash_result_failed = 6

sod_seven_ash_ending_seven_oaths_kept = 1
sod_seven_ash_ending_ashwick_stands = 2
sod_seven_ash_ending_wall_of_names = 4
sod_seven_ash_ending_empty_houses = 8
sod_seven_ash_ending_wulfred_broken = 16
sod_seven_ash_ending_wulfred_escaped = 32
sod_seven_ash_ending_bargain_brand = 64
sod_seven_ash_ending_blood_for_ash = 128
sod_seven_ash_ending_long_road_from_ashwick = 256
sod_seven_ash_ending_palisade_grave = 512
sod_seven_ash_ending_new_wolf = 1024
sod_seven_ash_ending_common_bell = 2048

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
companions_end = "trp_diego_companion"

special_companions_begin = "trp_diego_companion"
special_companions_end = "trp_kingdom_heroes_including_player_begin"

active_npcs_begin = companions_begin

active_npcs_end = companions_end

soldiers_begin = "trp_farmer"
soldiers_end = "trp_town_walker_1"

#Rebellion changes

rebel_factions_begin = "fac_kingdom_1_rebels"
rebel_factions_end =   "fac_kingdoms_end"

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
boar_clan_tier_1_unit_1       = "trp_boar_clan_clansman"

black_army_tier_1_unit_2      = "trp_black_army_line_supporter" 
conquistadors_tier_1_unit_2   = "trp_conquistador_crossbowman"
elephant_guard_tier_1_unit_2  = "trp_elephant_guard_spearman"
jotnar_clan_tier_1_unit_2     = "trp_jotnar_clan_armsman" 
serpent_host_tier_1_unit_2    = "trp_serpent_host_kapikulu"
slavers_tier_1_unit_2         = "trp_slave"
boar_clan_tier_1_unit_2       = "trp_boar_clan_rider"

black_army_tier_1_unit_3      = "trp_black_army_line_crusher" 

black_army_noble      = "trp_black_army_raven_captain" 
conquistadors_noble   = "trp_conquistador_lancer"
elephant_guard_noble  = "trp_elephant_guard_battle_shaman"
jotnar_clan_noble     = "trp_jotnar_clan_norn_mistress" 
serpent_host_noble    = "trp_serpent_host_basilisk_knight"
slavers_noble         = "trp_tormenter"
boar_clan_noble       = "trp_boar_clan_tusk_rider"

slavers_mercs_noble = "p_sod_merc_6_elite"
slavers_sod_mercs   = "p_sod_merc_6"

sod_slaver_action_trade_prisoners = 1
sod_slaver_action_escort_caravan = 2
sod_slaver_action_return_runaways = 3
sod_slaver_action_free_runaways = 4
sod_slaver_action_captivity = 5
sod_slaver_action_hostile = 6
sod_slaver_action_buy_slaves = 7
sod_slaver_action_carry_slaves = 8

sod_elephant_guard_activity_patrol = 1
sod_elephant_guard_activity_procession = 2

sod_boar_action_pay_toll = 1
sod_boar_action_hire_band = 2
sod_boar_action_defy_toll = 3
sod_boar_action_frontier_tribute = 4

sod_black_army_action_security_contract = 1
sod_black_army_action_hire_patrol = 2
sod_black_army_action_attack_patrol = 3
sod_black_army_action_interdict_road_threats = 4

sod_conquistador_action_fund_supplies = 1
sod_conquistador_action_take_stores = 2
sod_conquistador_action_delivery_contract = 3

sod_serpent_action_buy_intel = 1
sod_serpent_action_safe_passage = 2
sod_serpent_action_attack_screen = 3
sod_serpent_action_track_horde = 4

sod_black_khergit_role_camp = 1
sod_black_khergit_role_raider = 2
sod_black_khergit_role_guard = 3

sod_black_khergit_action_tribute = 1
sod_black_khergit_action_bribe_target = 2
sod_black_khergit_action_persuade_enemy = 3
sod_black_khergit_action_attack_camp = 4
sod_black_khergit_action_defeat_raiders = 5
sod_black_khergit_action_defeat_guards = 6
sod_black_khergit_action_duel_victory = 7
sod_black_khergit_action_duel_defeat = 8

sod_mini_faction_incident_none = 0
sod_mini_faction_incident_slaver_heat = 1
sod_mini_faction_incident_jotnar_hearth = 2
sod_mini_faction_incident_elephant_alarm = 3
sod_mini_faction_incident_black_khergit_raid = 4
sod_mini_faction_incident_boar_tolls = 5
sod_mini_faction_incident_serpent_warning = 6
sod_mini_faction_incident_black_army_contract = 7
sod_mini_faction_incident_conquistador_requisition = 8

sod_imperial_expedition_action_sabotage_supply = 1
sod_imperial_expedition_action_delay_invasion = 2

sod_trade_cargo_unknown = 0
sod_trade_cargo_food = 1
sod_trade_cargo_raw = 2
sod_trade_cargo_strategic = 3
sod_trade_cargo_luxury = 4

sod_trade_route_safe = 1
sod_trade_route_watched = 2
sod_trade_route_toll = 3
sod_trade_route_raider = 4
sod_trade_route_luxury = 5
sod_trade_route_grain = 6
sod_trade_route_strategic = 7
sod_trade_route_starving = 8

sod_trade_contract_none = 0
sod_trade_contract_guards = 1
sod_trade_contract_cargo_space = 2
sod_trade_contract_insurance = 3
sod_trade_contract_relief = 4
sod_trade_contract_profit = 5

sod_trade_result_none = 0
sod_trade_result_profitable = 1
sod_trade_result_delayed = 2
sod_trade_result_protected = 3
sod_trade_result_dangerous = 4
sod_trade_result_shortage_supplied = 5
sod_trade_result_taxed = 6
sod_trade_result_raided = 7
sod_trade_result_exploited = 8

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
slot_center_has_ambulatory, slot_center_has_water_supply, slot_center_has_clayworks, slot_center_has_rustic_blacksmith,
slot_center_has_militia_yard, slot_center_has_beacon_hill, slot_center_has_granary, slot_center_has_militia_armory]

town_buildings = [slot_center_has_temple, slot_center_has_barracks, slot_center_has_range,
slot_center_has_stables, slot_center_has_blacksmith, slot_center_has_messenger_post,
slot_center_has_prisoner_tower, slot_center_has_guild, slot_center_has_university, slot_center_has_hospital,
slot_center_has_canalization, slot_center_has_manufacture, slot_center_has_bank]

castle_buildings = [slot_center_has_chapel, slot_center_has_barracks, slot_center_has_range,
slot_center_has_stables, slot_center_has_chapter, slot_center_has_blacksmith, slot_center_has_messenger_post,
slot_center_has_prisoner_tower, slot_center_has_mercenary_guild_hall]

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
