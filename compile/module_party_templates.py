from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *

pmf_is_prisoner = 0x0001

####################################################################################################################
#  Each party template record contains the following fields:
#  1) Party-template id: used for referencing party-templates in other files.
#     The prefix pt_ is automatically added before each party-template id.
#  2) Party-template name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Faction
#  6) Personality. See header_parties.py for an explanation of personality flags.
#  7) List of stacks. Each stack record is a tuple that contains the following fields:
#    7.1) Troop-id.
#    7.2) Minimum number of troops in the stack.
#    7.3) Maximum number of troops in the stack.
#    7.4) Member flags(optional). Use pmf_is_prisoner to note that this member is a prisoner.
#     Note: There can be at most 6 stacks.
####################################################################################################################


party_templates = [
  ("none","none",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("rescued_prisoners","Rescued Prisoners",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("enemy","Enemy",icon_gray_knight,0,fac_undeads,merchant_personality,[]),
  ("hero_party","Hero Party",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
####################################################################################################################
# Party templates before this point are hard-wired into the game and should not be changed.
####################################################################################################################
##  ("old_garrison","Old Garrison",icon_vaegir_knight,0,fac_neutral,merchant_personality,[]),
  ("village_defenders","Village Defenders",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,10,20),(trp_peasant_woman,0,4)]),

  ("cattle_herd","Cattle Herd",icon_cattle|carries_goods(10),0,fac_neutral,merchant_personality,[(trp_cattle,80,120)]),

  ("mercenaries", "Jobless Mercenaries", icon_vaegir_knight|carries_goods(3), 0, fac_commoners, soldier_personality, [(trp_watchman, 5, 10),(trp_refugee, 5, 10),(trp_manhunter, 5, 10)]),
  ("boar_clan_fighters","Boar Clan Fighters",icon_flagbearer_a|carries_goods(2),0,fac_sod_merc_guild7,soldier_personality,[(trp_boar_clan_tusk_rider, 1, 1),(trp_boar_clan_warrior,10,15),(trp_boar_clan_rider,7,12),(trp_boar_clan_vet_warrior,3,8),(trp_boar_clan_vet_rider,3,8), (trp_boar_clan_clansman, 0, 5),]),
  ("boar_clan_fighters_desert","Boar Clan Fighters",icon_flagbearer_a|carries_goods(2),0,fac_sod_merc_guild7,soldier_personality,[(trp_boar_clan_tusk_rider, 1, 1),(trp_boar_clan_warrior,10,15),(trp_boar_clan_rider,7,12),(trp_boar_clan_vet_warrior,3,8),(trp_boar_clan_vet_rider,3,8),(trp_boar_clan_clansman, 0, 5),]),
  ("boar_clan_reinforcements","Boar Clan Fighters",icon_flagbearer_a|carries_goods(2),0,fac_sod_merc_guild7,soldier_personality,[(trp_boar_clan_warrior,0,5),(trp_boar_clan_rider,0,5),(trp_boar_clan_vet_warrior,0,3),(trp_boar_clan_vet_rider,0,3)]),
  ("jotnar_clan_warriors","Jotnar Clan warriors",icon_axeman|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_no_faction,soldier_personality,[(trp_jotnar_clan_armsman,15,15)]),
  ("sod_deserters","Deserters",icon_vaegir_knight|carries_goods(3),0,fac_deserters,bandit_personality,[(trp_watchman,8,14),(trp_sod_mercenary_footman,4,9),(trp_mercenary_crossbowman,1,4)]),
  ("sod_merc_deserters","Deserters",icon_vaegir_knight|carries_goods(3),0,fac_deserters,bandit_personality,[(trp_mercenary_swordsman,6,12),(trp_mercenary_crossbowman,4,8),(trp_mercenary_cavalry,2,5),(trp_hired_blade,1,3)]),
  ("slavers_caravan","Slave Transport",icon_gray_knight|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,hold_personality,[(trp_slave_driver,3,3),(trp_slave,10,35,pmf_is_prisoner)]),
  ("black_army_caravan","Black Army Caravan",icon_mule|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,hold_personality,[(trp_black_army_raven_captain,1,1),(trp_black_army_fresh_blade,7,7),(trp_black_army_line_supporter,7,7)]),
  ("black_army_patrol","Black Army Patrol",icon_flagbearer_a|carries_goods(8),0,fac_sod_merc_guild1,merc_personality,[(trp_black_army_line_keeper,8,14),(trp_black_army_line_supporter,6,10),(trp_black_army_line_crusher,3,6),(trp_black_army_iron_guard,1,4),(trp_black_army_raven_captain,0,1)]),
  ("black_army_contract_column","Black Army Contract Column",icon_flagbearer_a|carries_goods(12),0,fac_sod_merc_guild1,merc_personality,[(trp_black_army_raven_captain,1,1),(trp_black_army_iron_guard,5,9),(trp_black_army_assaulter,5,9),(trp_black_army_ironside,3,6),(trp_black_army_ravager,2,5),(trp_black_army_fresh_blade,4,8)]),
  ("conquistador_procurement_column","Conquistador Procurement Column",icon_flagbearer_a|carries_goods(18),0,fac_sod_merc_guild2,merc_personality,[(trp_conquistador_lancer,1,2),(trp_conquistador_rodelero,5,9),(trp_conquistador_tercio_pikeman,5,9),(trp_conquistador_seasoned_crossbowman,4,8),(trp_conquistador_footman,4,8)]),
  ("conquistador_expeditionary_camp","Conquistador Expeditionary Camp",icon_flagbearer_a|carries_goods(24),0,fac_sod_merc_guild2,hold_personality,[(trp_conquistador_lancer,2,3),(trp_conquistador_tercio_pikeman,8,13),(trp_conquistador_rodelero,8,13),(trp_conquistador_seasoned_crossbowman,6,10),(trp_conquistador_pikeman,4,8),(trp_conquistador_crossbowman,4,8)]),
  ("ravaging_bandits","Ravaging Bandits",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_no_faction,bandit_personality,[]),
  ("elephant_guard_ravaging_bandits","Ravaging Bandits",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_no_faction,bandit_personality,[]),
  ("conquistadors_ravaging_bandits","Rogue Mercenaries",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_no_faction,bandit_personality,[]),
  ("serpent_host_ravaging_bandits","Deserters",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_no_faction,bandit_personality,[]),
  ("bc_bandits", "Bandits",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_no_faction,bandit_personality,[]),
  ("runaway_slaves","Runaway Slaves",icon_peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_slave,10,16)]),
  
  ("militia_awaiting_ransom","Militia Awaiting Ransom",icon_flagbearer_a|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac_neutral,soldier_personality,[(trp_watchman,24,58)]),
  ("sh_spy","Serpent Host Spy",icon_gray_knight|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_sh_spy,1,1)]),
  ("slaves_with_jotnar_clansmen","Slavers",icon_gray_knight|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_no_faction,escorted_merchant_personality,[(trp_slave_master,1,2),(trp_slave_crusher,2,4),(trp_slave_hunter,4,8),(trp_slave_driver,8,16),]),
  ("jotnar_clansmen","Jotnar Clansmen",icon_axeman|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,hold_personality,[(trp_jotnar_clan_armsman,10,30)]),
  ("mercenary_lord_party","War Party",icon_flagbearer_a,0,fac_commoners,soldier_personality,[]),
  ("legion_mercenaries","Legion Mercenaries",icon_flagbearer_a,0,fac_kingdom_6_mercenaries,soldier_personality,[(trp_ief_bastard_brothers,20,20),(trp_ief_sons_of_deer,20,20)]),
  ("jotnar_revenge","Jotnar Clansmen",icon_axeman|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,hold_personality,[(trp_jotnar_clan_einherjar,0,3),(trp_jotnar_clan_disir,0,3)]),
  
##  ("vaegir_nobleman","Vaegir Nobleman",icon_vaegir_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_vaegir_knight,2,6),(trp_vaegir_horseman,4,12)]),
##  ("swadian_nobleman","Swadian Nobleman",icon_gray_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_swadian_knight,2,6),(trp_swadian_man_at_arms,4,12)]),

#PATROLS START
  ("player_patrol","Regiment",icon_flagbearer_a,0,fac_player_faction,hold_personality,[]),
  ("player_patrol_2","Regiment",icon_flagbearer_a,0,fac_player_faction,soldier_personality,[]),
  ("player_mercenaries","Mercenaries",icon_flagbearer_a,0,fac_player_faction,hold_personality,[]),
  ("sod_companion_retinue","Companion Retinue",icon_flagbearer_a|pf_no_label|pf_quest_party,0,fac_player_faction,hold_personality,[]),
#PATROLS END
  ("sod_mercs","Mercenaries",icon_flagbearer_a,0,fac_player_faction,merc_personality,[]),
  ("manhunters","Manhunters",icon_gray_knight,0,fac_manhunters,soldier_personality,[(trp_manhunter,9,40)]),
##  ("peasant","Peasant",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,1,6),(trp_peasant_woman,0,7)]),

  ("black_khergit_raiders","Black Khergit Raiders",icon_khergit_horseman_b|carries_goods(8),0,fac_black_khergits,bandit_personality,[(trp_black_khergit_guard,1,4),(trp_black_khergit_horseman,8,16)]),
  ("black_khergit_horde_camp","Black Khergit Horde Camp",icon_khergit_horseman_b|carries_goods(80),0,fac_black_khergits,hold_personality,[(trp_black_khergit_khan,1,1),(trp_black_khergit_guard,25,45),(trp_black_khergit_horseman,80,130)]),
  ("black_khergit_night_guard","Black Khergit Night Guard",icon_khergit_horseman_b|carries_goods(4),0,fac_black_khergits,bandit_personality,[(trp_black_khergit_guard,3,7),(trp_black_khergit_horseman,8,14)]),

# Old Bandits (comment these out in order to start using Jason's)
  ("steppe_bandits","Steppe Bandits",icon_khergit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_steppe_bandit,20,58)]),
  ("forest_bandits","Forest Bandits",icon_axeman|carries_goods(2),0,fac_forest_bandits,bandit_personality,[(trp_forest_bandit,20,52)]),
  ("mountain_bandits","Mountain Bandits",icon_axeman|carries_goods(2),0,fac_mountain_bandits,bandit_personality,[(trp_mountain_bandit,20,60)]),
  ("sea_raiders","Sea Raiders",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_sea_raider,20,50)]),
  ("bandits","Bandits",icon_axeman|carries_goods(8),0,fac_outlaws,bandit_personality,[(trp_thug,3,7),(trp_reaver,3,7),(trp_cutthroat,5,15),(trp_brigand,5,15),(trp_bandit,10,20),(trp_looter,5,15),]),
  ("bandit_reinfocements","Bandits",icon_axeman|carries_goods(8),0,fac_outlaws,bandit_personality,[(trp_thug,1,2),(trp_reaver,1,2),(trp_cutthroat,2,3),(trp_brigand,2,3),(trp_bandit,2,3),]),

# Jason's Bandits
#  ("steppe_bandits","Steppe Bandits",icon_khergit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_steppe_bandit,5,40),(trp_steppe_horseman,5,12),(trp_rogue_lord,0,1)]),
#  ("forest_bandits","Forest Bandits",icon_axeman|carries_goods(2),0,fac_forest_bandits,bandit_personality,[(trp_forest_bandit,5,30),(trp_forest_archer,5,10),(trp_forest_sharpshooter,2,5),(trp_rogue_lord,0,1)]),
#  ("mountain_bandits","Mountain Bandits",icon_axeman|carries_goods(2),0,fac_mountain_bandits,bandit_personality,[(trp_mountain_bandit,5,30),(trp_mountain_elite_swordsman,2,5),(trp_mountain_swordsman,5,10),(trp_rogue_lord,0,1)]),
#  ("sea_raiders","Sea Raiders",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_sea_raider,5,30),(trp_berzerker,2,5),(trp_axeman,5,10),(trp_rogue_lord,0,1)]),

  ("deserters","Deserters",icon_vaegir_knight|carries_goods(3),0,fac_deserters,bandit_personality,[]),

  ("merchant_caravan","Merchant Caravan",icon_mule|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,5,25)]),
  ("troublesome_bandits","Troublesome Bandits",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_outlaws,bandit_personality,[(trp_bandit,14,55)]),
  ("bandits_awaiting_ransom","Bandits Awaiting Ransom",icon_axeman|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_bandit,24,58),(trp_kidnapped_girl,1,1,pmf_is_prisoner)]),
  ("kidnapped_girl","Kidnapped Girl",icon_woman|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_kidnapped_girl,1,1)]),

##  ("farmers","Farmers",icon_peasant,0,fac_innocents,merchant_personality,[(trp_farmer,11,22),(trp_peasant_woman,16,44)]),
  ("village_farmers","Village Farmers",icon_peasant,0,fac_innocents,merchant_personality,[(trp_farmer,5,10),(trp_peasant_woman,3,8)]),
##  ("refugees","Refugees",icon_woman_b,0,fac_innocents,merchant_personality,[(trp_refugee,19,48)]),
##  ("dark_hunters","Dark Hunters",icon_gray_knight,0,fac_dark_knights,soldier_personality,[(trp_dark_knight,4,42),(trp_dark_hunter,13,25)]),

  ("spy_partners", "Unremarkable Travellers", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner,1,1),(trp_caravan_guard,5,11)]),
  ("runaway_serfs","Runaway Serfs",icon_peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_farmer,6,7), (trp_peasant_woman,3,3)]),
  ("spy", "Ordinary Townsman", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy,1,1)]),
  ("sacrificed_messenger", "Sacrificed Messenger", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[]),
  ("sod_diplomatic_envoy", "Diplomatic Envoy", icon_gray_knight|carries_goods(6)|pf_default_behavior|pf_quest_party,0,fac_player_supporters_faction,merchant_personality,[(trp_swadian_messenger,1,1),(trp_caravan_guard,3,6)]),
##  ("conspirator", "Conspirators", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator,3,4)]),
##  ("conspirator_leader", "Conspirator Leader", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator_leader,1,1)]),
##  ("peasant_rebels", "Peasant Rebels", icon_peasant,0,fac_peasant_rebels,bandit_personality,[(trp_peasant_rebel,33,97)]),
##  ("noble_refugees", "Noble Refugees", icon_gray_knight|carries_goods(12)|pf_quest_party,0,fac_noble_refugees,merchant_personality,[(trp_noble_refugee,3,5),(trp_noble_refugee_woman,5,7)]),



  ("forager_party","Foraging Party",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("scout_party","Scouts",icon_gray_knight|carries_goods(1)|pf_show_faction,0,fac_commoners,bandit_personality,[(trp_caravan_guard,2,4),(trp_watchman,4,8)]),
  ("patrol_party","Patrol",icon_gray_knight|carries_goods(2)|pf_show_faction,0,fac_commoners,soldier_personality,[]),
#  ("war_party", "War Party",icon_gray_knight|carries_goods(3),0,fac_commoners,soldier_personality,[]),
  ("messenger_party","Messenger",icon_gray_knight|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("raider_party","Raiders",icon_gray_knight|carries_goods(16)|pf_quest_party,0,fac_commoners,bandit_personality,[]),
  ("raider_captives","Raider Captives",0,0,fac_commoners,0,[(trp_peasant_woman,6,30,pmf_is_prisoner)]),
  ("kingdom_caravan_party","Caravan",icon_mule|carries_goods(25)|pf_show_faction,0,fac_commoners,merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,12,40)]),
  ("prisoner_train_party","Prisoner Train",icon_mule|carries_goods(12)|pf_show_faction|pf_default_behavior,0,fac_commoners,escorted_merchant_personality,[]),
  ("default_prisoners","Default Prisoners",0,0,fac_commoners,0,[(trp_bandit,5,10,pmf_is_prisoner)]),
##  ("merchant_party","Merchant",icon_mule|carries_goods(25)|pf_show_faction,0,fac_merchants,merchant_personality,[(trp_caravan_guard,12,40)]),
##  ("merchant_party_reinforcement","Merchant Party Reinforcement",icon_mule|carries_goods(25),0,fac_merchants,merchant_personality,[(trp_caravan_guard,6,20)]),

# Caravans

  ("center_reinforcements","Reinforcements",icon_axeman|carries_goods(16),0,fac_commoners,soldier_personality,[(trp_townsman,5,30),(trp_watchman,4,20)]),

  ("kingdom_hero_party","War Party",icon_flagbearer_a|pf_show_faction|pf_default_behavior,0,fac_commoners,soldier_personality,[]),
  ("kingdom_hero_party_2","War Party",icon_flagbearer_a|pf_show_faction|pf_default_behavior,0,fac_commoners,hold_personality,[]),



# Reinforcements
#  ("default_reinforcements_a","default_reinforcements_a",0,0,fac_commoners,0,[(trp_caravan_guard,1,10),(trp_watchman,3,16),(trp_farmer,9,24)]),
#  ("default_reinforcements_b","default_reinforcements_b",0,0,fac_commoners,0,[(trp_mercenary,1,7),(trp_caravan_guard,3,10),(trp_watchman,3,15)]),
#  ("default_reinforcements_c","default_reinforcements_c",0,0,fac_commoners,0,[(trp_hired_blade,1,7),(trp_mercenary,3,10),(trp_caravan_guard,3,15)]),

  ("kingdom_1_reinforcements_a", "kingdom_1_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_swadian_militia,2,6),(trp_swadian_recruit,4,7)]),
  ("kingdom_1_reinforcements_b", "kingdom_1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_swadian_crossbowman,2,6),(trp_swadian_skirmisher,4,7)]),
  ("kingdom_1_reinforcements_c", "kingdom_1_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_swadian_man_at_arms,3,6)]),

  ("kingdom_2_reinforcements_a", "kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_vaegir_footman,2,6),(trp_vaegir_recruit,4,7)]),
  ("kingdom_2_reinforcements_b", "kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_vaegir_archer,2,6),(trp_vaegir_skirmisher,3,5),(trp_vaegir_footman,1,3)]),
  ("kingdom_2_reinforcements_c", "kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_vaegir_horseman,3,6)]),

  ("kingdom_3_reinforcements_a", "kingdom_3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_khergit_skirmisher,2,6),(trp_khergit_tribesman,4,7)]),
  ("kingdom_3_reinforcements_b", "kingdom_3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_khergit_horse_archer,2,6),(trp_khergit_skirmisher,4,7)]),
  ("kingdom_3_reinforcements_c", "kingdom_3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_khergit_lancer,3,6)]),

  ("kingdom_4_reinforcements_a", "kingdom_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_nord_footman,4,8),(trp_nord_recruit,2,4)]),
  ("kingdom_4_reinforcements_b", "kingdom_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_nord_archer,1,3),(trp_nord_huntsman,3,5),(trp_nord_footman,2,5)]),
  ("kingdom_4_reinforcements_c", "kingdom_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_nord_warrior,3,6)]),

  ("kingdom_5_reinforcements_a", "kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_rhodok_spearman,3,7),(trp_rhodok_tribesman,3,6)]),
  ("kingdom_5_reinforcements_b", "kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_rhodok_trained_crossbowman,2,6),(trp_rhodok_crossbowman,4,7)]),
  ("kingdom_5_reinforcements_c", "kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_rhodok_sergeant,3,6)]),
#SOD BEGIN
  ("kingdom_6_reinforcements_a", "kingdom_6_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_ief_velites,5,10),(trp_ief_hestati,4,5),(trp_ief_principes,2,3),(trp_ief_triarii,1,2),(trp_ief_akolouthos,1,2)]),#infantry heavy
  ("kingdom_6_reinforcements_b", "kingdom_6_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_ief_velites,5,10),(trp_ief_sons_of_deer,0,2),(trp_ief_arcus,2,4),(trp_ief_akritoi,2,3),(trp_ief_vexillatio,1,2),(trp_ief_praetorian,1,2)]), #ranged heavy
  ("kingdom_6_reinforcements_c", "kingdom_6_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_ief_velites,5,10),(trp_ief_sons_of_deer,2,3),(trp_ief_speculatores,2,4),(trp_ief_clibanarii,2,3),(trp_ief_pronoiar,1,2),(trp_ief_hospitalier,1,2)]), #cavalry heavy
  #Must include Legion nobles above or they will never spawn (trp_ief_akolouthos, trp_ief_praetorian, trp_ief_hospitalier)

  ("sod_1_reinforcements_a", "sod_1_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sod_ant_regular,5,10),(trp_sod_ant_veteran,2,5),(trp_sod_ant_javelinman,1,5),(trp_sod_ant_elite,0,1)]),
  ("sod_1_reinforcements_b", "sod_1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_sod_ant_javelinman,5,10),(trp_sod_ant_trained_javelinman,1,3),(trp_sod_ant_regular,2,5),(trp_sod_ant_veteran,1,2),(trp_sod_ant_elite,0,1)]),
  ("sod_1_reinforcements_c", "sod_1_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_sod_ant_scout,2,6),(trp_sod_ant_cavalry,1,4),(trp_sod_ant_guard,0,1),(trp_sod_ant_noble,1,2)]),

  ("sod_2_reinforcements_a", "sod_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sod_mar_conscript,5,10),(trp_sod_mar_regular,2,5),(trp_sod_mar_veteran,1,3),(trp_sod_mar_elite,1,2),(trp_sod_mar_crossbowman,1,3)]),
  ("sod_2_reinforcements_b", "sod_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_sod_mar_crossbowman,5,10),(trp_sod_mar_trained_crossbowman,3,7),(trp_sod_mar_elite_crossbowman,2,5),(trp_sod_mar_sharpshooter,1,2),(trp_sod_mar_mercenary,1,2)]),
  ("sod_2_reinforcements_c", "sod_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_sod_mar_scout,1,5),(trp_sod_mar_mercenary,1,3),(trp_sod_mar_landsknecht,1,2),(trp_sod_mar_elite_crossbowman,1,2),(trp_sod_mar_elite,1,2)]),

  ("sod_3_reinforcements_a", "sod_3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sod_ade_regular,5,10),(trp_sod_ade_veteran,2,5),(trp_sod_ade_elite,1,5),(trp_sod_ade_light,0,1),(trp_sod_ade_medium,0,1)]),
  ("sod_3_reinforcements_b", "sod_3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_sod_ade_archer,5,10),(trp_sod_ade_veteran_archer,1,3),(trp_sod_ade_elite_archer,2,5),(trp_sod_ade_elite,1,2),(trp_sod_ade_light,0,1)]),
  ("sod_3_reinforcements_c", "sod_3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_sod_ade_light,5,10),(trp_sod_ade_medium,4,7),(trp_sod_ade_heavy,2,5),(trp_sod_ade_sqire,3,5),(trp_sod_ade_knight,1,4)]),

  ("sod_4_reinforcements_a", "sod_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sod_vil_regular,5,10),(trp_sod_vil_veteran,2,5),(trp_sod_vil_elite,1,5),(trp_sod_vil_longbowman,1,4),(trp_sod_vil_veteran_longbowman,1,4)]),
  ("sod_4_reinforcements_b", "sod_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_sod_vil_longbowman,5,10),(trp_sod_vil_veteran_longbowman,3,7),(trp_sod_vil_elite_longbowman,2,5),(trp_sod_vil_sharpshooter,1,2),(trp_sod_vil_noble,0,1)]),
  ("sod_4_reinforcements_c", "sod_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_sod_vil_scout,2,6),(trp_sod_vil_noble,1,4),(trp_sod_vil_chief,1,2),(trp_sod_vil_sharpshooter,0,1)]),  #twan456 removed obsolete units

  ("sod_5_reinforcements_a", "sod_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sod_zer_1_cavalry,5,10),(trp_sod_zer_2_cavalry,2,5),(trp_sod_zer_1_cavalry_archer,1,5),(trp_sod_zer_3_cavalry,1,4),(trp_sod_zer_1_noble,1,4)]),
  ("sod_5_reinforcements_b", "sod_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_sod_zer_1_infantry,5,10),(trp_sod_zer_2_infantry,1,3),(trp_sod_zer_1_archer,2,5),(trp_sod_zer_2_archer,1,2),(trp_sod_zer_3_infantry,0,1)]),
  ("sod_5_reinforcements_c", "sod_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_sod_zer_2_cavalry,2,6),(trp_sod_zer_1_cavalry_archer,1,4),(trp_sod_zer_3_cavalry,1,4),(trp_sod_zer_1_noble,1,4),(trp_sod_zer_2_noble,1,3)]),

  ("sod_merc_1_reinf", "sod_merc_1_reinf", 0, 0, fac_commoners, 0, [(trp_black_army_fresh_blade,0,2),(trp_black_army_line_supporter,0,2),(trp_black_army_line_crusher,0,2)]),
  ("sod_merc_2_reinf", "sod_merc_2_reinf", 0, 0, fac_commoners, 0, [(trp_conquistador_footman,0,3),(trp_conquistador_crossbowman,0,3)]),
  ("sod_merc_3_reinf", "sod_merc_3_reinf", 0, 0, fac_commoners, 0, [(trp_elephant_guard_tribesman,0,6)]),
  ("sod_merc_4_reinf", "sod_merc_4_reinf", 0, 0, fac_commoners, 0, [(trp_jotnar_clan_volva,0,3),(trp_jotnar_clan_armsman,0,3)]),
  ("sod_merc_5_reinf", "sod_merc_5_reinf", 0, 0, fac_commoners, 0, [(trp_serpent_host_akinci,0,3),(trp_serpent_host_kapikulu,0,3)]),  
  
  ("sod_foot_1", "sod_foot_1", 0, 0, fac_commoners, 0, [(trp_sod_ant_regular,1,1)]),
  ("sod_foot_2", "sod_foot_2", 0, 0, fac_commoners, 0, [(trp_sod_mar_conscript,1,1)]),
  ("sod_foot_3", "sod_foot_3", 0, 0, fac_commoners, 0, [(trp_sod_ade_regular,1,1)]),
  ("sod_foot_4", "sod_foot_4", 0, 0, fac_commoners, 0, [(trp_sod_vil_regular,1,1)]),
  ("sod_foot_5", "sod_foot_5", 0, 0, fac_commoners, 0, [(trp_sod_zer_1_infantry,1,1)]),

  ("sod_ranged_1", "sod_ranged_1", 0, 0, fac_commoners, 0, [(trp_sod_ant_javelinman,1,1)]),
  ("sod_ranged_2", "sod_ranged_2", 0, 0, fac_commoners, 0, [(trp_sod_mar_crossbowman,1,1)]),
  ("sod_ranged_3", "sod_ranged_3", 0, 0, fac_commoners, 0, [(trp_sod_ade_archer,1,1)]),
  ("sod_ranged_4", "sod_ranged_4", 0, 0, fac_commoners, 0, [(trp_sod_vil_longbowman,1,1)]),
  ("sod_ranged_5", "sod_ranged_5", 0, 0, fac_commoners, 0, [(trp_sod_zer_1_archer,1,1)]),

  ("sod_noble_1", "sod_noble_1", 0, 0, fac_commoners, 0, [(trp_sod_ant_noble,1,1)]),
  ("sod_noble_2", "sod_noble_2", 0, 0, fac_commoners, 0, [(trp_sod_mar_mercenary,1,1)]),
  ("sod_noble_3", "sod_noble_3", 0, 0, fac_commoners, 0, [(trp_sod_ade_sqire,1,1)]),
  ("sod_noble_4", "sod_noble_4", 0, 0, fac_commoners, 0, [(trp_sod_vil_noble,1,1)]),
  ("sod_noble_5", "sod_noble_5", 0, 0, fac_commoners, 0, [(trp_sod_zer_1_noble,1,1)]),
  ("elephant_guard_sanctuary_patrol","Elephant Guard Sanctuary Patrol",icon_flagbearer_a|carries_goods(10),0,fac_sod_merc_guild3,merc_personality,[(trp_elephant_guard_battle_shaman,1,1),(trp_elephant_guard_champion,2,4),(trp_elephant_guard_warrior,5,9),(trp_elephant_guard_fighter,6,10),(trp_elephant_guard_spearman,3,7)]),
  ("elephant_guard_relic_procession","Elephant Guard Relic Procession",icon_flagbearer_a|carries_goods(18),0,fac_sod_merc_guild3,hold_personality,[(trp_elephant_guard_battle_shaman,1,2),(trp_elephant_guard_penetrator,2,4),(trp_elephant_guard_spearman,5,9),(trp_elephant_guard_tribesman,8,14)]),
  ("jotnar_hearth_guard","Jotnar Hearth Guard",icon_axeman|carries_goods(14),0,fac_sod_merc_guild4,merc_personality,[(trp_jotnar_clan_jarl,1,2),(trp_jotnar_clan_armsman,8,14),(trp_jotnar_clan_volva,2,4),(trp_jotnar_clan_shield_maiden,2,5)]),
  ("jotnar_wintering_camp","Jotnar Wintering Camp",icon_axeman|carries_goods(26),0,fac_sod_merc_guild4,hold_personality,[(trp_jotnar_clan_armsman,10,18),(trp_jotnar_clan_volva,3,6),(trp_jotnar_clan_shield_maiden,3,6),(trp_jotnar_clan_jarl,1,1)]),
  ("serpent_host_route_screen","Serpent Host Route Screen",icon_khergit_horseman_b|carries_goods(8),0,fac_sod_merc_guild5,merc_personality,[(trp_serpent_host_akinci,5,9),(trp_serpent_host_timariot,3,6),(trp_serpent_host_sipahi,2,5),(trp_serpent_host_kapikulu,2,4)]),
  ("serpent_host_courier_lance","Serpent Host Courier Lance",icon_khergit_horseman_b|carries_goods(12),0,fac_sod_merc_guild5,merc_personality,[(trp_serpent_host_basilisk_knight,0,1),(trp_serpent_host_cataphract,1,3),(trp_serpent_host_sipahi,4,7),(trp_serpent_host_akinci,6,10),(trp_serpent_host_timariot,2,5)]),
#SOD END
##  ("kingdom_1_reinforcements_a", "kingdom_1_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_swadian_footman,3,7),(trp_swadian_skirmisher,5,10),(trp_swadian_militia,11,26)]),
##  ("kingdom_1_reinforcements_b", "kingdom_1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_swadian_man_at_arms,5,10),(trp_swadian_infantry,5,10),(trp_swadian_crossbowman,3,8)]),
##  ("kingdom_1_reinforcements_c", "kingdom_1_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_swadian_knight,2,6),(trp_swadian_sergeant,2,5),(trp_swadian_sharpshooter,2,5)]),
##
##  ("kingdom_2_reinforcements_a", "kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_vaegir_veteran,3,7),(trp_vaegir_skirmisher,5,10),(trp_vaegir_footman,11,26)]),
##  ("kingdom_2_reinforcements_b", "kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_vaegir_horseman,4,9),(trp_vaegir_infantry,5,10),(trp_vaegir_archer,3,8)]),
##  ("kingdom_2_reinforcements_c", "kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_vaegir_knight,3,7),(trp_vaegir_guard,2,5),(trp_vaegir_marksman,2,5)]),
##
##  ("kingdom_3_reinforcements_a", "kingdom_3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_khergit_horseman,3,7),(trp_khergit_skirmisher,5,10),(trp_khergit_tribesman,11,26)]),
##  ("kingdom_3_reinforcements_b", "kingdom_3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_khergit_veteran_horse_archer,4,9),(trp_khergit_horse_archer,5,10),(trp_khergit_horseman,3,8)]),
##  ("kingdom_3_reinforcements_c", "kingdom_3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_khergit_lancer,3,7),(trp_khergit_veteran_horse_archer,2,5),(trp_khergit_horse_archer,2,5)]),
##
##  ("kingdom_4_reinforcements_a", "kingdom_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_nord_trained_footman,3,7),(trp_nord_footman,5,10),(trp_nord_recruit,11,26)]),
##  ("kingdom_4_reinforcements_b", "kingdom_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_nord_veteran,4,9),(trp_nord_warrior,5,10),(trp_nord_footman,3,8)]),
##  ("kingdom_4_reinforcements_c", "kingdom_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_nord_champion,1,3),(trp_nord_veteran,2,5),(trp_nord_warrior,2,5)]),
##
##  ("kingdom_5_reinforcements_a", "kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_rhodok_spearman,3,7),(trp_rhodok_crossbowman,5,10),(trp_rhodok_tribesman,11,26)]),
##  ("kingdom_5_reinforcements_b", "kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_rhodok_trained_spearman,4,9),(trp_rhodok_spearman,5,10),(trp_rhodok_crossbowman,3,8)]),
##  ("kingdom_5_reinforcements_c", "kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_rhodok_sergeant,3,7),(trp_rhodok_veteran_spearman,2,5),(trp_rhodok_veteran_crossbowman,2,5)]),
]
