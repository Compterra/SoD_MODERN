from module_constants import *
from header_items import  *
from header_operations import *
from header_triggers import *

####################################################################################################################
#  Each item record contains the following fields:
#  1) Item id: used for referencing items in other files.
#     The prefix itm_ is automatically added before each item id.
#  2) Item name. Name of item as it'll appear in inventory window
#  3) List of meshes.  Each mesh record is a tuple containing the following fields:
#    3.1) Mesh name.
#    3.2) Modifier bits that this mesh matches.
#     Note that the first mesh record is the default.
#  4) Item flags. See header_items.py for a list of available flags.
#  5) Item capabilities. Used for which animations this item is used with. See header_items.py for a list of available flags.
#  6) Item value.
#  7) Item stats: Bitwise-or of various stats about the item such as:
#      weight, abundance, difficulty, head_armor, body_armor, leg_armor, etc...
#  8) Modifier bits: Modifiers that can be applied to this item.
#  9) [Optional] Triggers: List of simple triggers to be associated with the item.
####################################################################################################################

# Some constants for ease of use.
imodbits_none = 0
imodbits_horse_basic = imodbit_swaybacked|imodbit_lame|imodbit_spirited|imodbit_heavy|imodbit_stubborn
imodbits_cloth  = imodbit_tattered | imodbit_ragged | imodbit_sturdy | imodbit_thick | imodbit_hardened
imodbits_armor  = imodbit_rusty | imodbit_battered | imodbit_crude | imodbit_thick | imodbit_reinforced |imodbit_lordly
imodbits_plate  = imodbit_cracked | imodbit_rusty | imodbit_battered | imodbit_crude | imodbit_thick | imodbit_reinforced |imodbit_lordly
imodbits_polearm = imodbit_cracked | imodbit_bent | imodbit_balanced
imodbits_shield  = imodbit_cracked | imodbit_battered |imodbit_thick | imodbit_reinforced
imodbits_sword   = imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered
imodbits_sword_high   = imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered|imodbit_masterwork
imodbits_axe   = imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_heavy
imodbits_mace   = imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_heavy
imodbits_pick   = imodbit_rusty | imodbit_chipped | imodbit_balanced | imodbit_heavy
imodbits_bow = imodbit_cracked | imodbit_bent | imodbit_strong |imodbit_masterwork
imodbits_crossbow = imodbit_cracked | imodbit_bent | imodbit_masterwork
imodbits_missile   = imodbit_bent | imodbit_large_bag
imodbits_thrown   = imodbit_bent | imodbit_heavy| imodbit_balanced| imodbit_large_bag

imodbits_horse_good = imodbit_spirited|imodbit_heavy
imodbits_good   = imodbit_sturdy | imodbit_thick | imodbit_hardened | imodbit_reinforced
imodbits_bad    = imodbit_rusty | imodbit_chipped | imodbit_tattered | imodbit_ragged | imodbit_cracked | imodbit_bent

###################################
# Define some custom abilities:
# (the general ruleset for the weapon types)
###################################
itc_2H_cleaver = itcf_slashright_twohanded | itcf_slashleft_twohanded | itcf_overswing_twohanded|itc_parry_two_handed
itc_heavy_swing_horseback = itcf_horseback_slashright_onehanded | itcf_horseback_slashleft_onehanded

itc_handaxe = itc_scimitar
itc_2H_axe = itc_parry_polearm| itcf_slashright_polearm| itcf_slashleft_polearm| itcf_overswing_twohanded | itc_heavy_swing_horseback
itc_big_2H_axe = itc_parry_polearm| itcf_slashright_polearm| itcf_slashleft_polearm| itcf_overswing_twohanded
itc_bastard_axe = itc_big_2H_axe|itc_cleaver
itc_2H_sword = itc_2H_cleaver | itcf_thrust_twohanded | itc_heavy_swing_horseback
itc_big_2H_sword = itc_2H_cleaver | itcf_thrust_polearm
itc_bastard_sword = itc_bastardsword
# itc_longsword = from the header, for 1H swing+thrust
# itc_spear = same as in header, add swing abilities explicitly!
itc_big_pike = itcf_thrust_polearm
# itc_nodachi = from header, use for 2H no-thrust weapons
# itc_poleaxe = for glaves, halberds, etc...
# itc_greatlance = same as header
# hammers and morningstars are too varied. Use discretion

itp_handaxe = itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield
itp_2H_axe = itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry
itp_big_2H_axe = itp_2H_axe | itp_cant_use_on_horseback
itp_bastard_axe = itp_type_two_handed_wpn|itp_primary|itp_bonus_against_shield|itp_wooden_parry
itp_longsword = itp_type_one_handed_wpn|itp_primary
itp_2H_sword = itp_type_two_handed_wpn|itp_two_handed|itp_primary
itp_big_2H_sword = itp_2H_sword|itp_cant_use_on_horseback
itp_bastard_sword = itp_type_two_handed_wpn|itp_primary
itp_warspear = itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry
itp_big_pike = itp_warspear|itp_two_handed|itp_cant_use_on_horseback | itp_no_parry
itp_poleaxe = itp_warspear|itp_two_handed|itp_cant_use_on_horseback
itp_greatlance = itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_no_parry
# hammers and morningstars too varied. Use discretion

# Fauchard (majowski glaive)
items = [
# item_name, mesh_name, item_properties, item_capabilities, slot_no, cost, bonus_flags, weapon_flags, scale, view_dir, pos_offset
 ["no_item", "INVALID ITEM", [("practice_sword", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_longsword, 3, weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(16, blunt)|thrust_damage(10, blunt), imodbits_none],
 ["horse_meat", "Horse Meat", [("raw_meat", 0)], itp_type_goods|itp_consumable|itp_food, 0, 12, weight(40)|food_quality(30)|max_ammo(40), imodbits_none],
# Items before this point are hardwired and their order should not be changed!
 ["practice_sword", "Practice Sword", [("practice_sword", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_wooden_parry|itp_wooden_attack, itc_longsword, 3, weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(20, blunt)|thrust_damage(14, blunt), imodbits_none],
 ["heavy_practice_sword", "Heavy Practice Sword", [("heavy_practicesword", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_greatsword,
    21, weight(6.25)|spd_rtng(94)|weapon_length(128)|swing_damage(30, blunt)|thrust_damage(22, blunt), imodbits_none],
 ["practice_axe", "Practice Axe", [("hatchet", 0)], itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 24 , weight(2) | spd_rtng(95) | weapon_length(75) | swing_damage(20, blunt) | thrust_damage(0, pierce), imodbits_axe],
 ["arena_axe", "Axe", [("arena_axe", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
 137 , weight(1.5)|spd_rtng(100) | weapon_length(69)|swing_damage(23 , blunt) | thrust_damage(0 ,  pierce), imodbits_axe ],
 ["arena_sword", "Sword", [("arena_sword_one_handed", 0), ("sword_medieval_b_scabbard", ixmesh_carry), ], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 243 , weight(1.5)|spd_rtng(99) | weapon_length(95)|swing_damage(21 , blunt) | thrust_damage(20 ,  blunt), imodbits_sword_high ],
 ["arena_sword_two_handed",  "Two Handed Sword", [("arena_sword_two_handed", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back,
 670 , weight(2.75)|spd_rtng(93) | weapon_length(110)|swing_damage(29 , blunt) | thrust_damage(24 ,  blunt), imodbits_sword_high ],
 ["arena_lance",         "Lance", [("arena_lance", 0)], itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
 90 , weight(2.5)|spd_rtng(96) | weapon_length(150)|swing_damage(20 , blunt) | thrust_damage(25 ,  blunt), imodbits_polearm ],
 ["practice_staff", "Practice Staff", [("wooden_staff", 0)], itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_carry_sword_back, 9, weight(2.5)|spd_rtng(103) | weapon_length(118)|swing_damage(18, blunt) | thrust_damage(18, blunt), imodbits_none],
 ["practice_lance", "Practice Lance", [("joust_of_peace", 0)], itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_greatlance, 18, weight(4.25)|spd_rtng(58)|weapon_length(218)|swing_damage(0, blunt)|thrust_damage(20, blunt), imodbits_none],
 ["practice_shield", "Practice Shield", [("shield_round_a", 0)], itp_type_shield|itp_wooden_parry|itp_wooden_attack, 0, 20, weight(3.5)|body_armor(1)|hit_points(200)|spd_rtng(100)|weapon_length(50), imodbits_none],
 ["practice_bow", "Practice Bow", [("hunting_bow", 0), ("hunting_bow_carry", ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed, itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1.5)|spd_rtng(90) | shoot_speed(40) | thrust_damage(22, blunt), imodbits_bow ],
##                                                     ("hunting_bow", 0)],                  itp_type_bow|itp_two_handed|itp_primary|itp_attach_left_hand, itcf_shoot_bow, 4, weight(1.5)|spd_rtng(90)|shoot_speed(40)|thrust_damage(19, blunt), imodbits_none],
 ["practice_crossbow", "Practice Crossbow", [("crossbow", 0)], itp_type_crossbow |itp_primary|itp_two_handed , itcf_shoot_crossbow|itcf_carry_crossbow_back, 0, weight(3)|spd_rtng(42)| shoot_speed(68) | thrust_damage(34, blunt)|max_ammo(1), imodbits_crossbow],
 ["practice_javelin", "Practice Javelin", [("javelin", 0), ("javelins_quiver", ixmesh_carry)], itp_type_thrown |itp_primary|itp_bonus_against_shield , itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 0, weight(5) | spd_rtng(91) | shoot_speed(28) | thrust_damage(30, blunt) | max_ammo(40) | weapon_length(75), imodbits_thrown],
 ["practice_throwing_daggers", "Throwing Daggers", [("throwing_dagger", 0)], itp_type_thrown |itp_primary , itcf_throw_knife, 0 , weight(3.5)|spd_rtng(102) | shoot_speed(25) | thrust_damage(16, blunt)|max_ammo(10)|weapon_length(0), imodbits_thrown ],
 ["practice_throwing_daggers_100_amount", "Throwing Daggers", [("throwing_dagger", 0)], itp_type_thrown |itp_primary , itcf_throw_knife, 0 , weight(3.5)|spd_rtng(102) | shoot_speed(25) | thrust_damage(16, blunt)|max_ammo(100)|weapon_length(0), imodbits_thrown ],
# ["cheap_shirt", "Cheap Shirt", [("shirt", 0)], itp_type_body_armor|itp_covers_legs, 0, 4, weight(1.25)|body_armor(3), imodbits_none],
 ["practice_horse", "Practice Horse", [("saddle_horse", 0)], itp_type_horse, 0, 37, body_armor(10)|horse_speed(40)|horse_maneuver(40)|horse_charge(14), imodbits_none],
 ["practice_arrows", "Practice Arrows", [("arena_arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0, weight(1.5)|weapon_length(95)|max_ammo(80), imodbits_missile],
## ["practice_arrows", "Practice Arrows", [("arrow", 0), ("flying_missile", ixmesh_flying_ammo)], itp_type_arrows, 0, 31, weight(1.5)|weapon_length(95)|max_ammo(80), imodbits_none],
 ["practice_bolts", "Practice Bolts", [("bolt", 0), ("flying_missile", ixmesh_flying_ammo), ("bolt_bag", ixmesh_carry), ("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0, weight(2.25)|weapon_length(55)|max_ammo(49), imodbits_missile],
 ["practice_arrows_10_amount", "Practice Arrows", [("arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0, weight(1.5)|weapon_length(95)|max_ammo(10), imodbits_missile],
 ["practice_arrows_100_amount", "Practice Arrows", [("arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0, weight(1.5)|weapon_length(95)|max_ammo(100), imodbits_missile],
 ["practice_bolts_9_amount", "Practice Bolts", [("bolt", 0), ("flying_missile", ixmesh_flying_ammo), ("bolt_bag", ixmesh_carry), ("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0, weight(2.25)|weapon_length(55)|max_ammo(9), imodbits_missile],
 ["practice_boots", "Practice Boots", [("boot_nomad_a", 0)], itp_type_foot_armor |itp_civilian  | itp_attach_armature, 0, 11 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10), imodbits_cloth ],
 ["red_tourney_armor", "Red Tourney Armor", [("tourn_armor_a", 0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none],
 ["blue_tourney_armor", "Blue Tourney Armor", [("mail_shirt", 0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none],
 ["green_tourney_armor", "Green Tourney Armor", [("leather_vest", 0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none],
 ["gold_tourney_armor", "Gold Tourney Armor", [("padded_armor", 0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none],
 ["red_tourney_helmet", "Red Tourney Helmet", [("flattop_helmet", 0)], itp_type_head_armor, 0, 126, weight(2)|head_armor(16), imodbits_none],
 ["blue_tourney_helmet", "Blue Tourney Helmet", [("segmented_helm", 0)], itp_type_head_armor, 0, 126, weight(2)|head_armor(16), imodbits_none],
 ["green_tourney_helmet", "Green Tourney Helmet", [("hood_c", 0)], itp_type_head_armor, 0, 126, weight(2)|head_armor(16), imodbits_none],
 ["gold_tourney_helmet", "Gold Tourney Helmet", [("hood_a", 0)], itp_type_head_armor, 0, 126, weight(2)|head_armor(16), imodbits_none],

["arena_shield_red", "Shield", [("arena_shield_red", 0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(250)|body_armor(1)|spd_rtng(100)|weapon_length(60), imodbits_shield ],
["arena_shield_blue", "Shield", [("arena_shield_blue", 0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(250)|body_armor(1)|spd_rtng(100)|weapon_length(60), imodbits_shield ],
["arena_shield_green", "Shield", [("arena_shield_green", 0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(250)|body_armor(1)|spd_rtng(100)|weapon_length(60), imodbits_shield ],
["arena_shield_yellow", "Shield", [("arena_shield_yellow", 0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(250)|body_armor(1)|spd_rtng(100)|weapon_length(60), imodbits_shield ],

["arena_armor_white", "Arena Armor White", [("arena_armorW", 0)], itp_type_body_armor  |itp_covers_legs , 0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_red", "Arena Armor Red", [("arena_armorR", 0)], itp_type_body_armor  |itp_covers_legs , 0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_blue", "Arena Armor Blue", [("arena_armorB", 0)], itp_type_body_armor  |itp_covers_legs , 0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_green", "Arena Armor Green", [("arena_armorG", 0)], itp_type_body_armor  |itp_covers_legs , 0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_yellow", "Arena Armor Yellow", [("arena_armorY", 0)], itp_type_body_armor  |itp_covers_legs , 0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_tunic_white", "Arena Tunic White ", [("arena_tunicW", 0)], itp_type_body_armor |itp_covers_legs , 0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_red", "Arena Tunic Red", [("arena_tunicR", 0)], itp_type_body_armor |itp_covers_legs , 0, 27 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_blue", "Arena Tunic Blue", [("arena_tunicB", 0)], itp_type_body_armor |itp_covers_legs , 0, 27 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_green", "Arena Tunic Green", [("arena_tunicG", 0)], itp_type_body_armor |itp_covers_legs , 0, 27 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_yellow", "Arena Tunic Yellow", [("arena_tunicY", 0)], itp_type_body_armor |itp_covers_legs , 0, 27 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
#headwear
["arena_helmet_red", "Arena Helmet Red", [("arena_helmetR", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_blue", "Arena Helmet Blue", [("arena_helmetB", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_green", "Arena Helmet Green", [("arena_helmetG", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_yellow", "Arena Helmet Yellow", [("arena_helmetY", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_white", "Steppe Helmet White", [("steppe_helmetW", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_red", "Steppe Helmet Red", [("steppe_helmetR", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_blue", "Steppe Helmet Blue", [("steppe_helmetB", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_green", "Steppe Helmet Green", [("steppe_helmetG", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_yellow", "Steppe Helmet Yellow", [("steppe_helmetY", 0)], itp_type_head_armor|itp_fit_to_head , 0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_white", "Tourney Helm White", [("tourney_helmR", 0)], itp_type_head_armor|itp_covers_head, 0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_red", "Tourney Helm Red", [("tourney_helmR", 0)], itp_type_head_armor|itp_covers_head, 0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_blue", "Tourney Helm Blue", [("tourney_helmB", 0)], itp_type_head_armor|itp_covers_head, 0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_green", "Tourney Helm Green", [("tourney_helmG", 0)], itp_type_head_armor|itp_covers_head, 0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_yellow", "Tourney Helm Yellow", [("tourney_helmY", 0)], itp_type_head_armor|itp_covers_head, 0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],


#This book must be at the beginning of readable books
 ["book_tactics", "De Re Militari", [("book_a", 0)], itp_type_book, 0, 4000, weight(2)|abundance(100), imodbits_none],
 ["book_persuasion", "Rhetorica ad Herennium", [("book_b", 0)], itp_type_book, 0, 5000, weight(2)|abundance(100), imodbits_none],
 ["book_leadership", "The Life of Alixenus the Great", [("book_d", 0)], itp_type_book, 0, 4200, weight(2)|abundance(100), imodbits_none],
 ["book_intelligence", "Essays on Logic", [("book_e", 0)], itp_type_book, 0, 2900, weight(2)|abundance(100), imodbits_none],
 ["book_trade", "A Treatise on the Value of Things", [("book_f", 0)], itp_type_book, 0, 3100, weight(2)|abundance(100), imodbits_none],
 ["book_weapon_mastery", "On the Art of Fighting with Swords", [("book_d", 0)], itp_type_book, 0, 4200, weight(2)|abundance(100), imodbits_none],
 ["book_engineering", "Method of Mechanical Theorems", [("book_open", 0)], itp_type_book, 0, 4000, weight(2)|abundance(100), imodbits_none],

#Reference books
#This book must be at the beginning of reference books
 ["book_wound_treatment_reference", "The Book of Healing", [("book_c", 0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none],
 ["book_training_reference", "Manual of Arms", [("book_open", 0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none],
 ["book_surgery_reference", "The Great Book of Surgery", [("book_c", 0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none],

# ["dry_bread", "wheat_sack", itp_type_goods|itp_consumable, 0, slt_none, view_goods, 95, weight(2), max_ammo(50), imodbits_none],
#foods (first one is smoked_fish)
 ["smoked_fish", "Smoked Fish", [("smoked_fish", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 59, weight(15)|abundance(110)|food_quality(50)|max_ammo(50), imodbits_none],
 ["dried_meat", "Dried Meat", [("smoked_meat", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 72, weight(15)|abundance(100)|food_quality(70)|max_ammo(50), imodbits_none],
 ["cattle_meat", "Beef", [("raw_meat", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 103, weight(20)|abundance(100)|food_quality(80)|max_ammo(70), imodbits_none],
 ["pork", "Pork", [("fried_pig", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 85, weight(15)|abundance(100)|food_quality(70)|max_ammo(50), imodbits_none],
 ["bread", "Bread", [("bread_a", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 32, weight(20)|abundance(110)|food_quality(40)|max_ammo(50), imodbits_none],
 ["apples", "Apples", [("apple_basket", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 44, weight(20)|abundance(110)|food_quality(40)|max_ammo(50), imodbits_none],
 ["cheese", "Cheese", [("cheese_b", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 95, weight(6)|abundance(110)|food_quality(40)|max_ammo(30), imodbits_none],
 ["chicken", "Chicken", [("chicken_roasted", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 75, weight(10)|abundance(110)|food_quality(40)|max_ammo(50), imodbits_none],
 ["honey", "Honey", [("honey_pot", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 136, weight(5)|abundance(110)|food_quality(40)|max_ammo(30), imodbits_none],
 ["sausages", "Sausages", [("sausages", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 60, weight(10)|abundance(110)|food_quality(40)|max_ammo(40), imodbits_none],
 ["cabbages", "Cabbages", [("cabbage", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 30, weight(15)|abundance(110)|food_quality(40)|max_ammo(50), imodbits_none],
 ["butter", "Butter", [("butter_pot", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 150, weight(6)|abundance(110)|food_quality(40)|max_ammo(30), imodbits_none],
 ["wine", "Wine", [("amphora_slim", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 250, weight(30)|abundance(60)|food_quality(50)|max_ammo(10), imodbits_none],
 ["ale", "Ale", [("ale_barrel", 0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 200, weight(30)|abundance(70)|food_quality(50)|max_ammo(20), imodbits_none],

#other trade goods (first one is wine)
 ["spice", "Spice", [("spice_sack", 0)], itp_merchandise|itp_type_goods, 0, 880, weight(40)|abundance(25), imodbits_none],
 ["salt", "Salt", [("salt_sack", 0)], itp_merchandise|itp_type_goods, 0, 255, weight(50)|abundance(95), imodbits_none],
 ["grain", "Wheat", [("wheat_sack", 0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 77, weight(50)|abundance(110)|food_quality(40)|max_ammo(50), imodbits_none],
 ["flour", "Flour", [("salt_sack", 0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 91, weight(50)|abundance(100)|food_quality(45)|max_ammo(50), imodbits_none],
 ["iron", "Iron", [("iron", 0)], itp_merchandise|itp_type_goods, 0, 264, weight(60)|abundance(60), imodbits_none],
 ["oil", "Oil", [("oil", 0)], itp_merchandise|itp_type_goods, 0, 484, weight(50)|abundance(60), imodbits_none],
 ["pottery", "Pottery", [("jug", 0)], itp_merchandise|itp_type_goods, 0, 126, weight(50)|abundance(90), imodbits_none],
 ["linen", "Linen", [("linen", 0)], itp_merchandise|itp_type_goods, 0, 250, weight(40)|abundance(90), imodbits_none],
 ["furs", "Furs", [("fur_pack", 0)], itp_merchandise|itp_type_goods, 0, 391, weight(40)|abundance(90), imodbits_none],
 ["wool", "Wool", [("wool_sack", 0)], itp_merchandise|itp_type_goods, 0, 130, weight(40)|abundance(90), imodbits_none],
 ["velvet", "Velvet", [("velvet", 0)], itp_merchandise|itp_type_goods, 0, 1025, weight(40)|abundance(30), imodbits_none],
 ["tools", "Tools", [("iron_hammer", 0)], itp_merchandise|itp_type_goods, 0, 410, weight(50)|abundance(90), imodbits_none],


#************************************************************************************************
# ITEMS before this point are hardcoded into item_codes.h and their order should not be changed!
#************************************************************************************************

# Quest Items

 # ["siege_supply", "Supplies", [("ale_barrel", 0)], itp_type_goods, 0, 96, weight(40)|abundance(70), imodbits_none],
 # ["quest_wine", "Wine", [("amphora_slim", 0)], itp_type_goods, 0, 46, weight(40)|abundance(60)|max_ammo(50), imodbits_none],
 # ["quest_ale", "Ale", [("ale_barrel", 0)], itp_type_goods, 0, 31, weight(40)|abundance(70)|max_ammo(50), imodbits_none],


# Tutorial Items (Since SOD does not have a tutorial, can we remove these items?)
["tutorial_sword", "Sword", [("long_sword", 0), ("scab_longsw_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 
	0 , weight(1.5)|difficulty(0)|spd_rtng(100) | weapon_length(102)|swing_damage(18 , cut) | thrust_damage(15 ,  pierce), imodbits_sword ],
["tutorial_axe", "Axe", [("iron_ax", 0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 
	0 , weight(4)|difficulty(0)|spd_rtng(91) | weapon_length(108)|swing_damage(19 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["tutorial_spear", "Spear", [("spear", 0)], itp_type_polearm| itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear, 
	0 , weight(4.5)|difficulty(0)|spd_rtng(80) | weapon_length(158)|swing_damage(0 , cut) | thrust_damage(19 ,  pierce), imodbits_polearm ],
["tutorial_club", "Club", [("club", 0)], itp_type_one_handed_wpn| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 
	0 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(95)|swing_damage(11 , blunt) | thrust_damage(0 ,  pierce), imodbits_none ],
["tutorial_battle_axe", "Battle Axe", [("battle_ax", 0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 
	0 , weight(5)|difficulty(0)|spd_rtng(88) | weapon_length(108)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["tutorial_arrows", "Arrows", [("arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 
	0, weight(3)|abundance(160)|weapon_length(95)|thrust_damage(0, pierce)|max_ammo(20), imodbits_missile],
["tutorial_bolts", "Bolts", [("bolt", 0), ("flying_missile", ixmesh_flying_ammo), ("bolt_bag", ixmesh_carry), ("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 
	0, weight(2.25)|abundance(90)|weapon_length(55)|thrust_damage(0, pierce)|max_ammo(18), imodbits_missile],
["tutorial_short_bow", "Short Bow", [("short_bow", 0), ("short_bow_carry", ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed , itcf_shoot_bow|itcf_carry_bow_back, 
	0 , weight(1)|difficulty(0)|spd_rtng(98) | shoot_speed(49) | thrust_damage(12 ,  pierce  ), imodbits_bow ],
["tutorial_crossbow", "Crossbow", [("crossbow", 0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_reload_on_horseback , itcf_shoot_crossbow|itcf_carry_crossbow_back, 
	0 , weight(3)|difficulty(0)|spd_rtng(42)|  shoot_speed(68) | thrust_damage(32, pierce)|max_ammo(1), imodbits_crossbow ],
["tutorial_throwing_daggers", "Throwing Daggers", [("throwing_dagger", 0)], itp_type_thrown |itp_primary , itcf_throw_knife, 
	0 , weight(3.5)|difficulty(0)|spd_rtng(102) | shoot_speed(25) | thrust_damage(16 ,  cut)|max_ammo(14)|weapon_length(0), imodbits_missile ],
["tutorial_saddle_horse", "Saddle Horse", [("saddle_horse", 0)], itp_type_horse, 0, 
	0, abundance(90)|body_armor(3)|difficulty(0)|horse_speed(40)|horse_maneuver(38)|horse_charge(8), imodbits_horse_basic],
["tutorial_shield", "Kite Shield", [("shield_kite_a", 0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(150), imodbits_shield ],
["tutorial_staff_no_attack", "Staff", [("wooden_staff", 0)], itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_parry_polearm|itcf_carry_sword_back, 
	9, weight(3.5)|spd_rtng(120) | weapon_length(115)|swing_damage(0, blunt) | thrust_damage(0, blunt), imodbits_none],
["tutorial_staff", "Staff", [("wooden_staff", 0)], itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_carry_sword_back, 
	9, weight(3.5)|spd_rtng(120) | weapon_length(115)|swing_damage(16, blunt) | thrust_damage(16, blunt), imodbits_none],

# SoD books live after the M&B 1.011 item_codes.h block so the Native hardcoded
# item indices remain stable.
["book_administration", "Administration of the Rhodok Republik", [("book_open", 0)], itp_type_book, 0, 4000, weight(2)|abundance(100), imodbits_none],
["book_chirurgeons_ledger", "The Chirurgeon's Ledger", [("book_c", 0)], itp_type_book, 0, 4300, weight(2)|abundance(100), imodbits_none],
["book_anatomy_of_mercy", "The Anatomy of Mercy", [("book_c", 0)], itp_type_book, 0, 4800, weight(2)|abundance(100), imodbits_none],
["book_drill_camp_company", "Drill, Camp, and Company", [("book_open", 0)], itp_type_book, 0, 3600, weight(2)|abundance(100), imodbits_none],
["book_roads_before_armies", "Roads Before Armies", [("book_f", 0)], itp_type_book, 0, 3900, weight(2)|abundance(100), imodbits_none],
["book_quartermasters_burden", "The Quartermaster's Burden", [("book_b", 0)], itp_type_book, 0, 3700, weight(2)|abundance(100), imodbits_none],
["book_embassies_in_wartime", "Embassies in Wartime", [("book_e", 0)], itp_type_book, 0, 4600, weight(2)|abundance(100), imodbits_none],
["book_pathfinding_reference", "Cartography", [("book_c", 0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none],


##############
#HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES HORSES
##############

#Camels (Boar Clan)
["camel_1", "Camel", [("camel_1", 0)], itp_merchandise|itp_type_horse, 0, 
	435, abundance(12)|hit_points(115)|body_armor(20)|difficulty(1)|horse_speed(37)|horse_maneuver(35)|horse_charge(12), imodbits_horse_basic],
["camel_2", "Camel", [("camel_2", 0)], itp_merchandise|itp_type_horse, 0, 
	435, abundance(12)|hit_points(115)|body_armor(20)|difficulty(1)|horse_speed(37)|horse_maneuver(35)|horse_charge(12), imodbits_horse_basic],
["war_camel_1", "War Camel", [("camel_3", 0)], itp_merchandise|itp_type_horse, 0, 
	1425, abundance(8)|hit_points(145)|body_armor(32)|difficulty(3)|horse_speed(38)|horse_maneuver(35)|horse_charge(20), imodbits_horse_basic|imodbit_champion],
["war_camel_2", "War Camel", [("camel_4", 0)], itp_merchandise|itp_type_horse, 0, 
	1425, abundance(8)|hit_points(145)|body_armor(32)|difficulty(3)|horse_speed(38)|horse_maneuver(35)|horse_charge(20), imodbits_horse_basic|imodbit_champion],


#Saddleless Horses (Boar Clan)
["saddleless_hunter_1", "Saddleless Hunter", [("saddleless_horse_1", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(12)|hit_points(140)|body_armor(25)|difficulty(4)|horse_speed(41)|horse_maneuver(35)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["saddleless_hunter_2", "Saddleless Hunter", [("saddleless_horse_2", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(12)|hit_points(140)|body_armor(25)|difficulty(4)|horse_speed(41)|horse_maneuver(35)|horse_charge(18), imodbits_horse_basic|imodbit_champion],


#Sumpter / Saddle Horses
["sumpter_horse", "Sumpter Horse", [("sumpter_horse", 0)], itp_merchandise|itp_type_horse, 0, 
	192, abundance(90)|hit_points(110)|body_armor(17)|difficulty(1)|horse_speed(34)|horse_maneuver(33)|horse_charge(9), imodbits_horse_basic],
["saddle_horse", "Saddle Horse", [("saddle_horse", 0), ("horse_c", imodbits_horse_good)], itp_merchandise|itp_type_horse, 0, 
	336, abundance(90)|body_armor(14)|difficulty(1)|horse_speed(39)|horse_maneuver(36)|horse_charge(8), imodbits_horse_basic],
["rok_saddle_horse2", "Saddle_Horse", [("rok_saddle_horse2", 0)], itp_type_horse|itp_merchandise, 0, 
	336, abundance(90)|body_armor(14)|difficulty(1)|horse_speed(39)|horse_maneuver(36)|horse_charge(8), imodbits_horse_basic],


#Steppe Horses
["steppe_horse", "Steppe Horse", [("steppe_horse", 0)], itp_merchandise|itp_type_horse, 0, 
	276, abundance(80)|body_armor(15)|difficulty(2)|horse_speed(37)|horse_maneuver(41)|horse_charge(7), imodbits_horse_basic|imodbit_champion],
["steppe_horse_b", "Steppe Horse", [("steppe_horse_b", 0)], itp_merchandise|itp_type_horse, 0, 
	276, abundance(80)|body_armor(15)|difficulty(2)|horse_speed(37)|horse_maneuver(41)|horse_charge(7), imodbits_horse_basic|imodbit_champion],
["steppe_horse_lv", "Steppe Horse", [("steppe_horse_lv", 0)], itp_merchandise|itp_type_horse, 0, 
	276, abundance(80)|body_armor(15)|difficulty(2)|horse_speed(37)|horse_maneuver(41)|horse_charge(7), imodbits_horse_basic|imodbit_champion],


#Courser Horses
["courser", "Courser", [("courser", 0)], itp_merchandise|itp_type_horse, 0, 
	969, abundance(70)|body_armor(16)|difficulty(2)|horse_speed(43)|horse_maneuver(37)|horse_charge(11), imodbits_horse_basic|imodbit_champion],


#Hunter Horses
["hunter", "Hunter", [("hunting_horse", 0), ("hunting_horse", imodbits_horse_good)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["brown_hunter", "Hunter", [("hunting_horse_b", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["hunter_c", "Hunter", [("hunting_horse_c", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["hunting_horse_seven", "Hunter", [("hunting_horse_seven", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],


#War Horses
["warhorse", "Warhorse", [("warhorse", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_b", "Warhorse", [("warhorse_b", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_den_rtw2", "Warhorse", [("warhorse_den_rtw2", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_hre_rtw3", "Warhorse", [("warhorse_hre_rtw3", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_maw_b05", "Warhorse", [("warhorse_maw_b05", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_maw_b08", "Warhorse", [("warhorse_maw_b08", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_po2_rtw3", "Warhorse", [("warhorse_po2_rtw3", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_po1_rtw3", "Warhorse", [("warhorse_po1_rtw3", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_sc2_rtw2", "Warhorse", [("warhorse_sc2_rtw2", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_sc2_rtw3", "Warhorse", [("warhorse_sc2_rtw3", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["warhorse_black", "Warhorse", [("warhorse_black", 0)], itp_type_horse|itp_merchandise, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion ],
["anthorse1", "Warhorse", [("anthorse1", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["khergitnoblehorse", "Warhorse", [("KhergitNobleHorse", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion ],


#Charger Horses
["charger", "Charger", [("charger", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["charger_black", "Charger", [("charger_black", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["heraldicchargerone", "Charger", [("heraldicchargerone", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["scorpioncharger", "Charger", [("scorpioncharger", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["whitebirdongreencharger", "Charger", [("whitebirdongreencharger", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["whitedeercharger", "Charger", [("whitedeercharger", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["redandyellowbgnorthbow", "Charger", [("redandyellowbgnorthbow", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["darktealthreecircle", "Charger", [("darktealthreecircle", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["blueflamemoon", "Charger", [("blueflamemoon", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["blackdotwhitered", "Charger", [("blackdotwhitered", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["tribowred", "Charger", [("tribowred", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["goldbaseblackorament", "Charger", [("goldbaseblackorament", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["ravisaris", "Charger", [("ravisaris", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["whisparia", "Charger", [("whisparia", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["goldturqoisehorsebanner", "Charger", [("goldturqoisehorsebanner", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["lazarith", "Charger", [("lazarith", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["nishra", "Charger", [("Nishra", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["yixis", "Charger", [("Yixis", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["asizar", "Charger", [("Asizar", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["makar", "Charger", [("Makar", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["garail", "Charger", [("Garail", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["kali", "Charger", [("Kali", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["leeko", "Charger", [("Leeko", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(5)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],

#Faith Horse
["rok_black_general_horse", "Dark_General_Warhorse", [("rok_black_general_horse", 0)], itp_type_horse, 0, #Cannot be puchased ("Faithless" religious mounted unit only)
	3100, abundance(5)|hit_points(135)|body_armor(80)|difficulty(4)|horse_speed(30)|horse_maneuver(28)|horse_charge(42), imodbits_horse_basic|imodbit_champion],

##############
#HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR HANDWEAR
##############
["leather_gloves", "Leather Gloves", [("lthr_glove_L", 0)], itp_merchandise|itp_type_hand_armor, 0, 
	72, weight(0.25)|abundance(100)|body_armor(2)|difficulty(0), imodbits_cloth],
["mail_mittens", "Mail Mittens", [("mail_mitten_L", 0)], itp_merchandise|itp_type_hand_armor, 0, 
	288, weight(0.5)|abundance(100)|body_armor(4)|difficulty(0), imodbits_armor],
["scale_gauntlets", "Scale Gauntlets", [("scale_gaunt_L", 0)], itp_merchandise|itp_type_hand_armor, 0, 
	450, weight(0.75)|abundance(100)|body_armor(5)|difficulty(0), imodbits_armor],
["gauntlets", "Gauntlets", [("gauntlet_a_L", 0), ("gauntlet_b_L", imodbit_reinforced)], itp_merchandise|itp_type_hand_armor, 0, 
	648, weight(1)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor],
["darkgauntlets", "Dark Gauntlets", [("darkgauntlet_a_L", 0), ("darkgauntlet_b_L", imodbit_reinforced)], itp_merchandise|itp_type_hand_armor, 0, 
	1800, weight(1.25)|abundance(80)|body_armor(12)|difficulty(0), imodbits_armor],

##############
#FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR FOOTWEAR
##############
["wrapping_boots", "Wrapping Boots", [("cyc_shoe_fur", 0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature , 0,
	10 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(3)|difficulty(0) , imodbits_cloth ],
["woolen_hose", "Woolen Hose", [("cyc_woolen_hose", 0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature , 0,
	18 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(4)|difficulty(0) , imodbits_cloth ],
["blue_hose", "Blue Hose", [("cyc_blue_leggings", 0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature , 0,
	28 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(5)|difficulty(0) , imodbits_cloth ],
["khergit_guard_boots",  "Khergit Guard Boots", [("lamellar_boots_a", 0)], itp_merchandise|itp_type_foot_armor | itp_attach_armature, 0, 
	459 , weight(1)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0) , imodbits_cloth ],
["light_leather_boots",  "Light Leather Boots", [("light_leather_boots", 0)], itp_type_foot_armor |itp_merchandise| itp_attach_armature, 0, 
	258 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0) , imodbits_cloth ],
["hunter_boots", "Hunter Boots", [("cyc_boot_hunter", 0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature, 0,
	93 , weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(9)|difficulty(0) , imodbits_cloth ],
["hide_boots", "Hide Boots", [("cyc_boot_nomad_a", 0)], itp_merchandise| itp_type_foot_armor |itp_civilian  | itp_attach_armature, 0,
	114 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) , imodbits_cloth ],
["ankle_boots", "Ankle Boots", [("ankle_boots_a", 0)], itp_merchandise| itp_type_foot_armor |itp_civilian  | itp_attach_armature, 0,
	165 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) , imodbits_cloth ],
["nomad_boots", "Nomad Boots", [("cyc_boot_nomad_b", 0)], itp_merchandise| itp_type_foot_armor  |itp_civilian | itp_attach_armature, 0,
	225 , weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(14)|difficulty(0) , imodbits_cloth ],
["leather_boots", "Leather Boots", [("cyc_boot_khergit", 0)], itp_merchandise| itp_type_foot_armor  |itp_civilian | itp_attach_armature, 0,
	294 , weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(16)|difficulty(0) , imodbits_cloth ],
["mail_chausses", "Mail Chausses", [("cyc_chausses_cm", 0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature  , 0,
	507 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(21)|difficulty(0) , imodbits_armor ],
["splinted_leather_greaves", "Splinted Leather Greaves", [("cyc_lthr_greaves", 0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature, 0,
	662 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) , imodbits_armor ],
["splinted_greaves", "Splinted Greaves", [("cyc_spl_greaves", 0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature, 0,
	1531 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(7) , imodbits_armor ],
["mail_boots", "Mail Boots", [("cyc_shoe_cm", 0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature  , 0,
	1825 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(8) , imodbits_armor ],
["iron_greaves", "Iron Greaves", [("cyc_iron_greaves", 0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature, 0,
	2560 , weight(3.5)|abundance(80)|head_armor(0)|body_armor(0)|leg_armor(38)|difficulty(10) , imodbits_armor ],
["darkboots", "Dark Greaves", [("darkboots", 0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature, 0, 
	2560 , weight(3.75)|abundance(80)|head_armor(0)|body_armor(0)|leg_armor(38)|difficulty(10) , imodbits_armor ],
["black_greaves", "Black Greaves", [("cyc_black_greaves", 0)], itp_merchandise|itp_type_foot_armor|itp_attach_armature, 0,
	2062 , weight(3.5)|abundance(80)|head_armor(0)|body_armor(0)|leg_armor(33)|difficulty(9) , imodbits_armor ],
#Noble Boots
["dynasty_oufit_greaves", "Nobleman_Boots", [("dynasty_oufit_greaves", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	459, weight(1.25)|abundance(25)|leg_armor(20), imodbits_cloth ],
["nobleman_greaves", "Nobleman_Boots", [("nobleman_greaves", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	459, weight(1.25)|abundance(25)|leg_armor(20), imodbits_cloth ],


##############
#BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR BODYWEAR
#Organized primarily by weight
##############

#Dresses and Noble Wear
["dress", "Dress", [("dress", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian , 0, 
	153 , weight(1)|abundance(5)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) , imodbits_cloth ],
["blue_dress", "Blue Dress", [("blue_dress", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian , 0, 
	153 , weight(1)|abundance(5)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) , imodbits_cloth ],
["peasant_dress", "Peasant Dress", [("peasant_dress_b", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian , 0, 
	153 , weight(1)|abundance(5)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) , imodbits_cloth ],
["woolen_dress", "Woolen Dress", [("woolen_dress", 0)], itp_merchandise| itp_type_body_armor|itp_civilian  |itp_covers_legs , 0,
	240 , weight(1.75)|abundance(5)|head_armor(0)|body_armor(8)|leg_armor(2)|difficulty(0) , imodbits_cloth ],
["lady_dress_ruby", "Lady Dress", [("lady_dress_r", 0)], itp_merchandise|itp_type_body_armor  |itp_covers_legs|itp_civilian , 0, 
	960 , weight(3)|abundance(5)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) , imodbits_cloth],
["lady_dress_green", "Lady Dress", [("lady_dress_g", 0)], itp_merchandise|itp_type_body_armor  |itp_covers_legs|itp_civilian , 0, 
	960 , weight(3)|abundance(5)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) , imodbits_cloth],
["lady_dress_blue", "Lady Dress", [("lady_dress_b", 0)], itp_merchandise|itp_type_body_armor  |itp_covers_legs|itp_civilian , 0, 
	960 , weight(3)|abundance(5)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) , imodbits_cloth],
["court_outfit", "Court Outfit", [("steppe_dav_031", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian   , 0, 
	1749 , weight(4)|abundance(10)|head_armor(0)|body_armor(15)|leg_armor(12)|difficulty(0) , imodbits_cloth ],
["courtly_outfit", "Courtly Outfit", [("cyc_nobleman_outf", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian   , 0, 
	1382 , weight(4)|abundance(10)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) , imodbits_cloth ],
["court_dress", "Court Dress", [("court_dress", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian   , 0, 
	777 , weight(4)|abundance(5)|head_armor(0)|body_armor(14)|leg_armor(4)|difficulty(0) , imodbits_cloth ],
["rich_outfit", "Rich Outfit", [("cyc_merchant_outf", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian   , 0, 
	960 , weight(4)|abundance(25)|head_armor(0)|body_armor(16)|leg_armor(4)|difficulty(0) , imodbits_cloth ],
["nobleman_outfit", "Nobleman Outfit", [("nobleman_outfit_b", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian   , 0, 
	1749 , weight(4)|abundance(25)|head_armor(0)|body_armor(15)|leg_armor(12)|difficulty(0) , imodbits_cloth ],
["dynasty_outfit", "Nobleman_Outfit", [("dynasty_outfit", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	1749, weight(4)|abundance(25)|body_armor(15)|leg_armor(12), imodbits_cloth ],
["nobleman_outfit6", "Nobleman_Outfit", [("nobleman_outfit6", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	1749, weight(4)|abundance(25)|body_armor(15)|leg_armor(12), imodbits_cloth ],


#Very Light Armors
["shirt", "Shirt", [("shirt", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian , 0,
	60 , weight(1)|abundance(100)|head_armor(0)|body_armor(5)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["linen_tunic", "Linen Tunic", [("linen_tunic", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	117 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(1)|difficulty(0) , imodbits_cloth ],
["short_tunic", "Rich Tunic", [("cvl_costume_a", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	153 , weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0) , imodbits_cloth ],
["robe", "Robe", [("robe", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs |itp_civilian, 0,
	470 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(6)|difficulty(0) , imodbits_cloth ],
["coarse_tunic", "Coarse Tunic", [("coarse_tunic", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	693 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) , imodbits_cloth ],
["khergit_armor", "Khergit Armor", [("cyc_armor_nomad_b", 0)], itp_merchandise| itp_type_body_armor , 0, 
	470 , weight(2)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["leather_apron", "Leather Apron", [("leather_apron", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	866 , weight(3)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(7)|difficulty(0) , imodbits_cloth ],
["leather_jacket", "Leather Jacket", [("cyc_leather_jacket", 0)], itp_merchandise| itp_type_body_armor  |itp_civilian , 0, 
	540 , weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["tabard", "Tabard", [("tabard_a", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs |itp_civilian, 0,
	1058 , weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(6)|difficulty(0) , imodbits_cloth ],


#Light Armors
["leather_vest", "Leather Vest", [("cyc_leather_vest", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian , 0,
	2160 , weight(4)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(7)|difficulty(0) , imodbits_cloth ],
["nomad_armor", "Nomad Armor", [("cyc_armor_nomad", 0)], itp_merchandise| itp_type_body_armor   , 0, 
	1382 , weight(4)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["rawhide_coat", "Rawhide Coat", [("cyc_tunic_fur", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0, 
	240 , weight(5)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["steppe_armor", "Steppe Armor", [("lamellar_leather", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	2306 , weight(5)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(8)|difficulty(0) , imodbits_cloth ],
["gambeson", "Gambeson", [("white_gambeson", 0)], itp_merchandise| itp_type_body_armor|itp_covers_legs|itp_civilian, 0,
	1881 , weight(5)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(5)|difficulty(0) , imodbits_cloth ],
["blue_gambeson", "Blue Gambeson", [("blue_gambeson", 0)], itp_merchandise| itp_type_body_armor|itp_covers_legs|itp_civilian, 0,
	1881 , weight(5)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(5)|difficulty(0) , imodbits_cloth ],
["red_gambeson", "Red Gambeson", [("red_gambeson", 0)], itp_merchandise| itp_type_body_armor|itp_covers_legs|itp_civilian, 0,
	1881 , weight(5)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(5)|difficulty(0) , imodbits_cloth ],
["light_leather", "Light Leather", [("light_leather", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise   , 0, 
	2613 , weight(5)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(7)|difficulty(0) , imodbits_cloth ],
["leather_jerkin", "Leather Jerkin", [("cyc_leather_jerkin", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	2018 , weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) , imodbits_cloth ],
["fur_coat", "Fur Coat", [("fur_coat", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs |itp_civilian, 0, 
	866 , weight(6)|abundance(100)|head_armor(0)|body_armor(13)|leg_armor(6)|difficulty(0) , imodbits_cloth ],
["nomad_vest", "Nomad Vest", [("nomad_vest_a", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian , 0,
	2306 , weight(7)|abundance(50)|head_armor(0)|body_armor(23)|leg_armor(8)|difficulty(0) , imodbits_cloth ],
["ragged_outfit", "Ragged Outfit", [("ragged_outfit_a", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	2457 , weight(7)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(9)|difficulty(0) , imodbits_cloth ],
["leather_armor", "Leather Armor", [("cyc_lthr_armor_a", 0)], itp_merchandise| itp_type_body_armor |itp_covers_legs  , 0, 
	777 , weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) , imodbits_cloth ],


#Medium / Light Armors
["padded_cloth", "Padded Cloth", [("cyc_aketon_a", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	2018 , weight(11)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) , imodbits_cloth ],
["padded_leather", "Padded Leather", [("cyc_padded_leather", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian, 0,
	3840 , weight(12)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) , imodbits_cloth ],
["tribal_warrior_outfit", "Tribal Warrior Outfit", [("tribal_warrior_outfit_a", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian , 0,
	3840 , weight(14)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) , imodbits_cloth ],
["studded_leather_coat", "Studded Leather Coat", [("cyc_std_lthr_coat", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	5067 , weight(14)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(11)|difficulty(7) , imodbits_cloth ],
["nomad_robe", "Nomad Robe", [("nomad_robe_a", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs |itp_civilian, 0,
	3840 , weight(15)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) , imodbits_cloth ],


#Medium Armors
["byrnie", "Byrnie", [("byrnie_a", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	4664 , weight(17)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(6)|difficulty(7) , imodbits_armor ],
["haubergeon", "Haubergeon", [("cyc_haubergeon_a", 0), ("cyc_haubergeon_b", imodbits_good)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	4574 , weight(18)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(6)|difficulty(6) , imodbits_armor ],
["lamellar_vest", "Lamellar Vest", [("cyc_nmd_warrior_a", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	4977 , weight(18)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(6) , imodbits_armor ],
["mail_shirt", "Mail Shirt", [("cyc_mail_shirt", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	5841 , weight(19)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(12)|difficulty(6) , imodbits_armor ],
["mail_hauberk", "Mail Hauberk", [("hauberk_a", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	5841 , weight(19)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(12)|difficulty(6) , imodbits_armor ],
["brigandine_a", "Brigandine", [("cyc_brigandine_a", 0)], itp_merchandise| itp_type_body_armor|itp_covers_legs, 0,
	7029 , weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(6) , imodbits_armor ],
["khergit_guard_armor", "Khergit Guard Armor", [("lamellar_armor_a", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs   , 0, 
	6540 , weight(19)|abundance(25)|head_armor(0)|body_armor(42)|leg_armor(8)|difficulty(6) , imodbits_armor ],


#Heavy Armors
["mail_with_surcoat", "Mail with Surcoat", [("mail_long_surcoat", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	6302, weight(22)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(14)|difficulty(6) , imodbits_armor ],
["surcoat_over_mail", "Surcoat over Mail", [("surcoat_over_mail", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	7628, weight(22)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(7) , imodbits_armor ],
["red_surcoat_over_mail", "Surcoat over Mail", [("red_surcoat_over_mail", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	7628, weight(22)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(7) , imodbits_armor ],
["light_mail_and_plate", "Light Mail and Plate", [("light_mail_and_plate", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	7628 , weight(19)|abundance(25)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(7) , imodbits_armor],
["mail_and_plate", "Mail and Plate", [("mail_and_plate", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs   , 0,
	8607, weight(22)|abundance(25)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(9) , imodbits_armor ],


#Very Heavy Armors
["banded_armor", "Banded Armor", [("cyc_reinf_jerkin", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	9164 , weight(23)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(14)|difficulty(9) , imodbits_armor ],
["cuir_bouilli", "Cuir Bouilli", [("cyc_hard_lthr_a", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	9450 , weight(24)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(9) , imodbits_armor ],
["lamellar_armor", "Lamellar Armor", [("lamellar_armor_b", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	8883 , weight(25)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(9) , imodbits_armor ],
["coat_of_plates", "Coat of Plates", [("cyc_coat_of_plates", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	9740 , weight(25)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(16)|difficulty(9) , imodbits_armor ],
["plate_armor", "Plate Armor", [("cyc_plate_armor", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	13251 , weight(27)|abundance(50)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["plate_armor2", "Plate Armor", [("plate_armor2", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	13251 , weight(27)|abundance(50)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(9) , imodbits_plate ],

#Heraldic Armors
["heraldic_studded_leather_coat", "Heraldic_Studded_Leather_Coat", [("new_std_lthr_coat",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs ,0,
	5067 , weight(14)|abundance(75)|head_armor(0)|body_armor(32)|leg_armor(11)|difficulty(7), imodbits_armor,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_studded_leather_coat", ":agent_no", ":troop_no")])]],
["heraldic_haubergeon", "Heraldic_Haubergeon", [("new_haubergeon_a",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs ,0,
	4574 , weight(18)|abundance(75)|head_armor(0)|body_armor(35)|leg_armor(6)|difficulty(6), imodbits_armor,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_haubergeon", ":agent_no", ":troop_no")])]],
["heraldic_mail_shirt", "Heraldic_Mail_Shirt", [("new_mail_shirt",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs ,0,
	5841 , weight(19)|abundance(75)|head_armor(0)|body_armor(35)|leg_armor(12)|difficulty(6), imodbits_armor,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_mail_shirt", ":agent_no", ":troop_no")])]],
["heraldic_mail_hauberk", "Heraldic_Mail_Hauberk", [("new_hauberk_a",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs ,0,
	5841 , weight(19)|abundance(75)|head_armor(0)|body_armor(35)|leg_armor(12)|difficulty(6), imodbits_armor,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_mail_hauberk", ":agent_no", ":troop_no")])]],
["heraldic_brigandine_a", "Heraldic_Brigandine", [("brigandine_new",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0,
	7029 , weight(19)|abundance(75)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(6), imodbits_armor,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_brigandine_new", ":agent_no", ":troop_no")])]],
["heraldic_mail_with_tabard", "Heraldic_Mail_with_Tabard", [("heraldic_armor_d", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	9450, weight(21)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(9) , imodbits_armor,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_d", ":agent_no", ":troop_no")])]],
["heraldic_mail_with_surcoat", "Heraldic Mail with Surcoat", [("heraldic_armor_a", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	10035, weight(22)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(17)|difficulty(9) , imodbits_armor,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_a", ":agent_no", ":troop_no")])]],
["heraldic_banded_armor", "Heraldic_Banded_Armor", [("new_reinf_jerkin",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs ,0,
	9164 , weight(23)|abundance(75)|head_armor(0)|body_armor(45)|leg_armor(14)|difficulty(9), imodbits_armor ,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_banded_armor", ":agent_no", ":troop_no")])]], 
["heraldic_cuir_bouilli", "Heraldic_Cuir_Bouilli", [("new_hard_lthr_a",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0,
	9450 , weight(24)|abundance(40)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(9), imodbits_armor,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_cuir_bouilli", ":agent_no", ":troop_no")])]],
["heraldic_plate_armor", "Heraldic_Plate_Armor", [("new_plate_armor",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs, 0,
	13251 , weight(27)|abundance(35)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_plate,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_plate_armor", ":agent_no", ":troop_no")])]], 
["heraldic_black_armor", "Heraldic_Black_Armor", [("new_black_armor",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs ,0,
	13251 , weight(27)|abundance(35)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_plate,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_black_armor", ":agent_no", ":troop_no")])]],


 #Faith Armors
["faith_enlightenment_armor_1", "Exquisite Light Plate", [("faith_enlightenment_armor_1", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	10460, weight(20)|abundance(10)|head_armor(0)|body_armor(50)|leg_armor(14)|difficulty(7) , imodbits_plate ],
["faith_enlightenment_armor_2", "Exquisite Light Plate", [("faith_enlightenment_armor_2", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	10460, weight(20)|abundance(10)|head_armor(0)|body_armor(50)|leg_armor(14)|difficulty(7) , imodbits_plate ],
["faith_old_gods_armor_1", "Ornate Plate Armor", [("faith_old_gods_armor_1", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	14310, weight(27)|abundance(10)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["faith_old_gods_armor_2", "Ornate Plate Armor", [("faith_old_gods_armor_2", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	14310, weight(27)|abundance(10)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["faith_old_gods_armor_3", "Ornate Plate Armor", [("faith_old_gods_armor_3", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	14310, weight(27)|abundance(10)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["faith_old_gods_armor_4", "Ornate Plate Armor", [("faith_old_gods_armor_4", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	14310, weight(27)|abundance(10)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["faith_the_one_armor_1", "Exquisite Plate Armor", [("faith_the_one_armor_1", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	14310, weight(27)|abundance(10)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["faith_the_one_armor_2", "Elite Plate Armor", [("faith_the_one_armor_2", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	14310, weight(27)|abundance(10)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["faith_void_armor_1", "Dark Plate", [("faith_void_armor_1", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	23000 , weight(28)|abundance(10)|head_armor(0)|body_armor(72)|leg_armor(24)|difficulty(10) , imodbits_plate ],
["faith_void_armor_2", "Exquisite Light Plate", [("faith_void_armor_2", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	10460, weight(20)|abundance(10)|head_armor(0)|body_armor(50)|leg_armor(14)|difficulty(7) , imodbits_plate ],
["faith_void_armor_3", "Exquisite Light Plate", [("faith_void_armor_3", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	10460, weight(20)|abundance(10)|head_armor(0)|body_armor(50)|leg_armor(14)|difficulty(7) , imodbits_plate ],

##############
#HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR HEADGEAR
#Organized primarily by weight
##############

#Very Light Helmets
["turret_hat_ruby", "Turret Hat", [("turret_hat_r", 0)], itp_merchandise|itp_type_head_armor  |itp_civilian|itp_fit_to_head , 0, 
	86 ,weight(0.5)|abundance(5)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["turret_hat_blue", "Turret Hat", [("turret_hat_b", 0)], itp_merchandise|itp_type_head_armor  |itp_civilian|itp_fit_to_head , 0, 
	86 , weight(0.5)|abundance(5)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["turret_hat_green", "Barbette", [("turret_hat_g", 0)], itp_merchandise|itp_type_head_armor|itp_civilian|itp_fit_to_head, 0, 
	48, weight(0.5)|abundance(100)|head_armor(6)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth],
["head_wrappings", "head_wrapping", [("head_wrapping", 0)], itp_merchandise|itp_type_head_armor|itp_fit_to_head, 0, 
	12, weight(0.25)|abundance(5)|head_armor(3), imodbit_tattered | imodbit_ragged | imodbit_sturdy | imodbit_thick],
["court_hat", "Turret Hat", [("court_hat", 0)], itp_merchandise|itp_type_head_armor  |itp_civilian|itp_fit_to_head , 0, 
	86 , weight(0.5)|abundance(5)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["wimple_a", "Wimple", [("wimple_a", 0)], itp_merchandise|itp_type_head_armor|itp_civilian|itp_fit_to_head, 0, 
	21, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth],
["headcloth", "Headcloth", [("headcloth", 0)], itp_merchandise| itp_type_head_armor  |itp_civilian , 0, 
	21 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["fur_hat", "Fur Hat", [("hat_fur_a", 0)], itp_merchandise| itp_type_head_armor |itp_civilian  , 0, 
	86 , weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["helmet_fur_a", "Nomad Cap", [("helmet_fur_a", 0), ("helmet_fur_a", imodbits_good)], itp_merchandise| itp_type_head_armor |itp_civilian  , 0, 
	135 , weight(0.75)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["straw_hat", "Straw Hat", [("straw_hat", 0)], itp_merchandise|itp_type_head_armor|itp_civilian, 0, 
	5, weight(1)|abundance(100)|head_armor(2)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth],
["common_hood", "Hood", [("hood_a", 0), ("hood_b", 0), ("hood_c", 0), ("hood_d", 0)], itp_merchandise|itp_type_head_armor|itp_civilian, 0, 
	135, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth],
["woolen_hood", "Woolen Hood", [("woolen_hood", 0)], itp_merchandise| itp_type_head_armor |itp_civilian  , 0, 
	86 , weight(1)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["steppe_cap", "Steppe Cap", [("helmet_fur_b", 0)], itp_merchandise| itp_type_head_armor  |itp_civilian , 0, 
	194 , weight(1)|abundance(100)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["padded_coif", "Padded Coif", [("padded_coif", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	163 , weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["woolen_cap", "Woolen Cap", [("woolen_cap", 0)], itp_merchandise| itp_type_head_armor  |itp_civilian , 0, 
	48 , weight(1)|abundance(100)|head_armor(6)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["felt_hat", "Felt Hat", [("felt_hat_a", 0), ("felt_hat_b", imodbits_good)], itp_merchandise| itp_type_head_armor |itp_civilian, 0, 
	86 , weight(1)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["female_hood", "Lady's Hood", [("woolen_hood", 0)], itp_merchandise| itp_type_head_armor |itp_civilian  , 0, 
	135 , weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],


#Light Helmets
["leather_cap", "Leather Cap", [("leather_cap", 0)], itp_merchandise| itp_type_head_armor|itp_civilian , 0, 
	540 , weight(1)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["arming_cap", "Arming Cap", [("linen_arming_cap", 0)], itp_merchandise| itp_type_head_armor  |itp_civilian , 0, 
	540 , weight(1)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["nomad_cap_a", "Leather Steppe Cap", [("nomad_cap_a", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	540 , weight(1)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["leather_steppe_cap_a", "Leather Steppe Cap", [("cyc_leather_steppe_cap_a", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	540 , weight(1)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["leather_steppe_cap_b", "Leather Steppe Cap", [("cyc_leather_steppe_cap_b", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	540 , weight(1)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["leather_steppe_cap_c", "Leather Steppe Cap", [("cyc_leather_steppe_cap_c", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	540 , weight(1)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["leather_warrior_cap", "Leather Warrior Cap", [("skull_cap_new_b", 0)], itp_merchandise| itp_type_head_armor  |itp_civilian , 0, 
	540 , weight(1)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["skullcap", "Skullcap", [("skull_cap_new_a", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	540 , weight(1)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_plate ],
["black_hood", "Black Hood", [("hood_black", 0)], itp_type_head_armor|itp_merchandise   , 0, 
	540 , weight(2)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["shahi", "Shahi", [("shahi", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	540 , weight(2)|abundance(25)|head_armor(20)|body_armor(0)|leg_armor(0) , imodbits_cloth ],


#Medium Helmets
["mail_coif", "Mail Coif", [("mail_coif", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	1170 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_armor ],
["nasal_helmet", "Nasal Helmet", [("nasal_helmet_b", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	2012 , weight(1.25)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["norman_helmet", "Helmet with Cap", [("norman_helmet_a", 0)], itp_merchandise| itp_type_head_armor|itp_fit_to_head , 0, 
	2012 , weight(1.25)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["segmented_helmet", "Segmented Helmet", [("segmented_helm_new", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	2012 , weight(1.25)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["footman_helmet", "Footman's_Helmet", [("skull_cap_new", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	540 , weight(1.5)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_plate ],
["kettle_hat", "Kettle Hat", [("kettle_hat_new", 0)], itp_merchandise| itp_type_head_armor, 0, 
	2012 , weight(1.5)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["helmet_with_neckguard", "Helmet with Neckguard", [("neckguard_helm_new", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	2012 , weight(1.75)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["rus_helmet_a", "Rus Helmet", [("cyc_rus_helmet_a", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	1215 , weight(2)|abundance(25)|head_armor(30)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["spiked_helmet", "Spiked Helmet", [("spiked_helmet_new", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	2012 , weight(2)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["khergit_guard_helmet", "Khergit Guard Helmet", [("lamellar_helmet_a", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	1749 , weight(2)|abundance(25)|head_armor(36)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["khergit_cavalry_helmet", "Khergit Cavalry Helmet", [("lamellar_helmet_b", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	1749 , weight(2)|abundance(25)|head_armor(36)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["kettle_hat_b", "Kettle Hat", [("kettlehelm", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	2102 , weight(2.25)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(8) , imodbits_plate ],

#Heavy Helmets
["khergit_helmet", "Khergit Helmet", [("khergit_guard_helmet", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	2700 , weight(2)|abundance(25)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(6) , imodbits_cloth ],
["byzantion_helmet_a", "Byzantion Helmet", [("cyc_byzantion_helmet_a", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	3243 , weight(2)|abundance(25)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["nordic_helmet", "Nordic Helmet", [("helmet_w_eyeguard_new", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3011 , weight(2)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["flat_topped_helmet", "Flat Topped Helmet", [("flattop_helmet_new", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3101 , weight(2)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(8) , imodbits_plate ],
["bascinet", "Bascinet", [("bascinet_avt_new", 0), ("bascinet_avt_new1", imodbit_crude|imodbit_rusty), ("bascinet_avt_new2", imodbits_good)], itp_merchandise|itp_type_head_armor   , 0, 
	3101 , weight(2.25)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(8) , imodbits_plate ],
["guard_helmet", "Guard Helmet", [("reinf_helmet_new", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3191 , weight(2.5)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
 
 
#Very Heavy Helmets
["saladed", "Salade", [("realsaladed", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4185 , weight(2.25)|abundance(75)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["pigfacec", "Pigface", [("realbascinete", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4185 , weight(2.25)|abundance(75)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["war_helm", "War Helmet", [("war_helm", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4185 , weight(2.25)|abundance(75)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["plain_great_helm", "Great Helmet", [("maciejowskihelm", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4185 , weight(2.25)|abundance(75)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["great_helmet_master", "Ornate Great Helmet", [("maciejowskihelm_m", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4275 , weight(2.25)|abundance(75)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["old_great_helm", "Great Helmet", [("great_helm", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4185 , weight(2.25)|abundance(75)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],


#Elite Helmets
["talak_great_helm", "Great Helmet", [("sugarloaf_helm", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4983 , weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["black_helmet", "Black Helmet", [("black_helm", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4983 , weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["great_helmet", "Great Helmet", [("great_helm_a", 0)], itp_merchandise| itp_type_head_armor|itp_covers_head, 0, 
	4983 , weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["crown", "Iron Crown", [("crown", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head   , 0, 
	4983 , weight(2.25)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["crown2", "Iron_Crown", [("crown_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4983, weight(3.25)|abundance(15)|head_armor(55)|difficulty(10), imodbits_armor|imodbit_cracked ],
["crown3", "Iron_Ornate_Crown", [("crown_helmet_ornate", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4983, weight(3)|abundance(15)|head_armor(55)|difficulty(10), imodbits_armor|imodbit_cracked ],
["crown_ornate", "Ornate Crown", [("crown_ornate", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head   , 0, 
	4983 , weight(2.25)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["winged_great_helmet", "Winged Great Helmet", [("maciejowski_helmet_new", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head, 0, 
	4275 , weight(2.75)|abundance(30)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],


#Faith Helmets
["faith_old_gods_helm_1", "Ceremonial Helmet", [("faith_old_gods_helm_1", 0)], itp_merchandise|itp_type_head_armor, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate],
["faith_old_gods_helm_2", "Ceremonial Helmet", [("faith_old_gods_helm_2", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate],
["faith_old_gods_helm_3", "Ceremonial Helmet", [("faith_old_gods_helm_3", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate],
["faith_old_gods_helm_4", "Ceremonial Helmet", [("faith_old_gods_helm_4", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["faith_old_gods_helm_5", "Ceremonial Helmet", [("faith_old_gods_helm_5", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["faith_old_gods_helm_6", "Ceremonial Helmet", [("faith_old_gods_helm_6", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["faith_the_one_helm_1", "Dull Greathelm", [("faith_the_one_helm_1", 0)], itp_merchandise|itp_type_head_armor|itp_fit_to_head, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate],
["faith_void_helm_1", "Dark Helmet", [("faith_void_helm_1", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate],
["faith_void_helm_2", "Dark Helmet", [("faith_void_helm_2", 0)], itp_merchandise| itp_type_head_armor|itp_fit_to_head, 0, 
	4983, weight(2.75)|abundance(15)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate],


##############
#MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     MISSLES     
##############
["arrows", "Arrows", [("arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver", ixmesh_carry)], itp_merchandise|itp_type_arrows, itcf_carry_quiver_back, 
	216, weight(3)|abundance(160)|weapon_length(95)|thrust_damage(1, pierce)|max_ammo(40), imodbits_missile],
["khergit_arrows", "Khergit Arrows", [("arrow_b", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver_b", ixmesh_carry)], itp_merchandise|itp_type_arrows, itcf_carry_quiver_back_right, 
	423, weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(3, pierce)|max_ammo(40), imodbits_missile],
["barbed_arrows", "Barbed Arrows", [("barbed_arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver_d", ixmesh_carry)], itp_merchandise|itp_type_arrows, itcf_carry_quiver_back_right, 
	372, weight(3)|abundance(70)|weapon_length(95)|thrust_damage(2, pierce)|max_ammo(40), imodbits_missile],
["bodkin_arrows", "Bodkin Arrows", [("piercing_arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("quiver_c", ixmesh_carry)], itp_merchandise|itp_type_arrows, itcf_carry_quiver_back_right, 
	330, weight(3)|abundance(50)|weapon_length(91)|thrust_damage(3, pierce)|max_ammo(35), imodbits_missile],
["bolts", "Bolts", [("bolt", 0), ("flying_missile", ixmesh_flying_ammo), ("bolt_bag", ixmesh_carry), ("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_merchandise|itp_type_bolts, itcf_carry_quiver_right_vertical, 
	192, weight(2.25)|abundance(90)|weapon_length(55)|thrust_damage(4, pierce)|max_ammo(40), imodbits_missile],
["steel_bolts", "Steel Bolts", [("bolt", 0), ("flying_missile", ixmesh_flying_ammo), ("bolt_bag_c", ixmesh_carry)], itp_merchandise|itp_type_bolts, itcf_carry_quiver_right_vertical, 
	394, weight(2.5)|abundance(20)|weapon_length(55)|thrust_damage(7, pierce)|max_ammo(40), imodbits_missile],
["cartridges", "Cartridges", [("cartridge_a", 0)], itp_merchandise|itp_type_bullets, 0, 
	41, weight(2.25)|abundance(90)|weapon_length(3)|thrust_damage(1, pierce)|max_ammo(40), imodbits_missile],


##############
#RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS  RANGED WEAPONS
##############
#THROWING
["jarid", "Jarid", [("jarid_new", 0), ("jarid_quiver", ixmesh_carry)], itp_merchandise|itp_type_thrown |itp_primary|itp_bonus_against_shield , itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 
	627 , weight(4)|difficulty(2)|spd_rtng(89) | shoot_speed(28) | thrust_damage(36 ,  pierce)|max_ammo(12)|weapon_length(65), imodbits_thrown ],
["javelin", "Javelin", [("javelin", 0), ("javelins_quiver", ixmesh_carry)], itp_merchandise|itp_type_thrown |itp_primary|itp_bonus_against_shield , itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 
	225 , weight(5)|difficulty(1)|spd_rtng(91) | shoot_speed(29) | thrust_damage(34 ,  pierce)|max_ammo(12)|weapon_length(75), imodbits_thrown ],
["gold_jarid", "Decorated_Jarid", [("gold_jarid", 0, 0), ("gold_jarid_quiver", ixmesh_carry)], itp_type_thrown|itp_bonus_against_shield|itp_merchandise|itp_primary, itcf_carry_quiver_back|itcf_throw_javelin|itcf_show_holster_when_drawn, 
	1290, weight(4.5)|abundance(25)|difficulty(2)|spd_rtng(84)|shoot_speed(28)|weapon_length(65)|max_ammo(12)|thrust_damage(38, pierce), imodbits_thrown ],
["throwing_spear", "Throwing_Spear", [("throwing_spear", 0), ("throwing_spear_quiver", ixmesh_carry)], itp_merchandise|itp_type_thrown |itp_primary|itp_bonus_against_shield , itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 
	345, weight(6.5)|abundance(25)|difficulty(2)|spd_rtng(85)|shoot_speed(25)|thrust_damage(45 , pierce)|max_ammo(8)|weapon_length(98), imodbits_thrown ],
["stones", "Stones", [("throwing_stone", 0)], itp_merchandise|itp_type_thrown |itp_primary , itcf_throw_stone, 
	3 , weight(4)|difficulty(0)|spd_rtng(97) | shoot_speed(30) | thrust_damage(11 ,  blunt)|max_ammo(24)|weapon_length(8), imodbit_large_bag ],
["throwing_knives", "Throwing Knives", [("throwing_knife", 0)], itp_merchandise|itp_type_thrown |itp_primary , itcf_throw_knife, 
	228 , weight(3.5)|difficulty(0)|spd_rtng(121) | shoot_speed(25) | thrust_damage(19 ,  cut)|max_ammo(20)|weapon_length(0), imodbits_thrown ],
["throwing_daggers", "Throwing Daggers", [("throwing_dagger", 0)], itp_merchandise|itp_type_thrown |itp_primary , itcf_throw_knife, 
	579 , weight(3.5)|difficulty(0)|spd_rtng(110) | shoot_speed(24) | thrust_damage(25 ,  cut)|max_ammo(19)|weapon_length(0), imodbits_thrown ],
["throwing_axes", "Throwing Axes", [("francisca", 0)], itp_merchandise|itp_type_thrown |itp_primary|itp_bonus_against_shield, itcf_throw_axe, 
	723, weight(5)|difficulty(1)|spd_rtng(99) | shoot_speed(20) | thrust_damage(38, cut)|max_ammo(12)|weapon_length(53), imodbits_thrown ],
["throwing_hammers1", "Throwing_Hammers", [("throwing_hammer1", 0)], itp_type_thrown|itp_bonus_against_shield|itp_merchandise|itp_primary, itcf_throw_knife|itcf_throw_stone|itcf_throw_axe, 
	450, weight(2.5)|abundance(25)|spd_rtng(104)|shoot_speed(21)|weapon_length(39)|max_ammo(6)|thrust_damage(20, blunt), imodbits_thrown ],
["throwing_hammers2", "Throwing_Hammers", [("throwing_hammer2", 0)], itp_type_thrown|itp_bonus_against_shield|itp_merchandise|itp_primary, itcf_throw_knife|itcf_throw_stone|itcf_throw_axe, 
	435, weight(2.25)|abundance(25)|spd_rtng(104)|shoot_speed(22)|weapon_length(39)|max_ammo(6)|thrust_damage(18, blunt), imodbits_thrown ],
["throwing_military_hammers", "Throwing_Military_Hammers", [("throwing_military_hammer", 0)], itp_type_thrown|itp_bonus_against_shield|itp_merchandise|itp_primary, itcf_throw_knife|itcf_throw_stone|itcf_throw_axe, 
	1232, weight(5)|abundance(25)|difficulty(1)|spd_rtng(96)|shoot_speed(20)|weapon_length(41)|max_ammo(8)|thrust_damage(32, blunt), imodbits_thrown ],
["throwing_decor_hammer", "Throwing_Decorated_Hammers", [("decor_hammer", 0)], itp_type_thrown|itp_bonus_against_shield|itp_merchandise|itp_primary, itcf_throw_knife|itcf_throw_stone|itcf_throw_axe, 
	1287, weight(5)|abundance(25)|difficulty(1)|spd_rtng(98)|shoot_speed(20)|weapon_length(55)|max_ammo(8)|thrust_damage(33, blunt), imodbits_thrown ],

#BOWS
["hunting_bow", "Hunting Bow", [("hunting_bow", 0), ("hunting_bow_carry", ixmesh_carry)], itp_merchandise|itp_type_bow |itp_primary|itp_two_handed, itcf_shoot_bow|itcf_carry_bow_back, 
	51 , weight(1)|difficulty(0)|spd_rtng(100) | shoot_speed(48) | thrust_damage(15 ,  pierce), imodbits_bow ],
["short_bow", "Short Bow", [("short_bow", 0), ("short_bow_carry", ixmesh_carry)], itp_merchandise|itp_type_bow |itp_primary|itp_two_handed , itcf_shoot_bow|itcf_carry_bow_back, 
	174 , weight(1)|difficulty(1)|spd_rtng(98) | shoot_speed(52) | thrust_damage(18 ,  pierce  ), imodbits_bow ],
["nomad_bow", "Nomad Bow", [("nomad_bow", 0), ("nomad_bow_case", ixmesh_carry)], itp_merchandise|itp_type_bow |itp_primary|itp_two_handed , itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 
	492 , weight(1.25)|difficulty(2)|spd_rtng(96) | shoot_speed(53) | thrust_damage(20 ,  pierce), imodbits_bow ],
["long_bow", "Long Bow", [("long_bow", 0), ("long_bow_carry", ixmesh_carry)], itp_merchandise|itp_type_bow |itp_primary|itp_two_handed , itcf_shoot_bow|itcf_carry_bow_back, 
	435 , weight(1.75)|difficulty(3)|spd_rtng(82) | shoot_speed(54) | thrust_damage(22 ,  pierce), imodbits_bow ],
["khergit_bow", "Khergit Bow", [("khergit_bow", 0), ("khergit_bow_case", ixmesh_carry)], itp_merchandise|itp_type_bow |itp_primary|itp_two_handed, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 
	807 , weight(1.25)|difficulty(3)|spd_rtng(95) | shoot_speed(56) | thrust_damage(21 , pierce), imodbits_bow ],
["strong_bow", "Strong Bow", [("strong_bow", 0), ("strong_bow_case", ixmesh_carry)], itp_merchandise|itp_type_bow |itp_primary|itp_two_handed , itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 
	1311 , weight(1.25)|difficulty(3)|spd_rtng(94) | shoot_speed(57) | thrust_damage(23 , pierce), imodbit_cracked | imodbit_bent | imodbit_masterwork ],
["war_bow", "War Bow", [("war_bow", 0), ("war_bow_carry", ixmesh_carry)], itp_merchandise|itp_type_bow|itp_primary|itp_two_handed , itcf_shoot_bow|itcf_carry_bow_back, 
	1538 , weight(1.5)|difficulty(4)|spd_rtng(93) | shoot_speed(58) | thrust_damage(25 , pierce), imodbits_bow ],


#CROSSBOWS
["hunting_crossbow", "Hunting Crossbow", [("crossbow", 0)], itp_merchandise|itp_type_crossbow |itp_primary|itp_two_handed , itcf_shoot_crossbow|itcf_carry_crossbow_back, 
	66 , weight(2.25)|difficulty(0)|spd_rtng(47) | shoot_speed(65) | thrust_damage(32 ,  pierce)|max_ammo(1), imodbits_crossbow ],
["light_crossbow", "Light Crossbow", [("light_crossbow", 0)], itp_merchandise|itp_type_crossbow |itp_primary|itp_two_handed , itcf_shoot_crossbow|itcf_carry_crossbow_back, 
	201 , weight(2.5)|difficulty(8)|spd_rtng(45) | shoot_speed(78) | thrust_damage(42 ,  pierce)|max_ammo(1), imodbits_crossbow ],
["crossbow", "Crossbow", [("crossbow", 0)], itp_merchandise|itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_use_on_horseback , itcf_shoot_crossbow|itcf_carry_crossbow_back, 
	546 , weight(3)|difficulty(8)|spd_rtng(43) | shoot_speed(88) | thrust_damage(48, pierce)|max_ammo(1), imodbits_crossbow ],
["heavy_crossbow", "Heavy Crossbow", [("heavy_crossbow", 0)], itp_merchandise|itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_use_on_horseback , itcf_shoot_crossbow|itcf_carry_crossbow_back, 
	1047 , weight(3.5)|difficulty(9)|spd_rtng(41) | shoot_speed(96) | thrust_damage(58 , pierce)|max_ammo(1), imodbits_crossbow ],
["sniper_crossbow", "Siege Crossbow", [("heavy_crossbow", 0)], itp_merchandise|itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_use_on_horseback , itcf_shoot_crossbow|itcf_carry_crossbow_back, 
	2049 , weight(3.75)|difficulty(10)|spd_rtng(37) | shoot_speed(104) | thrust_damage(64 , pierce)|max_ammo(1), imodbits_crossbow ],


#GUNS
["musket_1", "Handgonne", [("rrr_handgonne",0)], itp_type_pistol|itp_primary|itp_two_handed|itp_cant_use_on_horseback|itp_bonus_against_shield, itcf_shoot_musket|itcf_reload_musket, 
	800 , weight(2)|difficulty(0)|spd_rtng(45) | shoot_speed(160) | thrust_damage(60 ,pierce)|max_ammo(1)|accuracy(75),imodbits_none,
 [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,27),(position_move_y, pos1,36),(particle_system_burst, "psys_musket_smoke", pos1, 15)])]],#no merchandise (no gun)
["musket_2", "Arquebuse", [("rrr_arquebuse",0)], itp_type_pistol|itp_primary|itp_two_handed|itp_cant_use_on_horseback|itp_bonus_against_shield, itcf_shoot_musket|itcf_reload_musket, 
	800 , weight(2)|difficulty(0)|spd_rtng(40) | shoot_speed(160) | thrust_damage(65 ,pierce)|max_ammo(1)|accuracy(75),imodbits_none,
 [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,27),(position_move_y, pos1,36),(particle_system_burst, "psys_musket_smoke", pos1, 15)])]],#no merchandise (no gun)
["flintlock_pistol", "Flintlock Pistol", [("flintlock_pistol", 0)], itp_type_pistol|itp_primary , itcf_shoot_pistol|itcf_reload_pistol, 
	530 , weight(1.5)|difficulty(0)|spd_rtng(45) | shoot_speed(160) | thrust_damage(40 , pierce)|max_ammo(1)|accuracy(75), imodbits_none,
 [(ti_on_weapon_attack, [(play_sound, "snd_pistol_shot"), (position_move_x, pos1, 27), (position_move_y, pos1, 36), (particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],#no merchandise (no gun)
 
 
##############
#MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS  MELEE WEAPONS
##############

#ONE-HANDED BLUNT
["wooden_stick", "Wooden Stick", [("wooden_stick", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 
	12 , weight(2.5)|difficulty(0)|spd_rtng(99) | weapon_length(90)|swing_damage(13 , blunt) | thrust_damage(0 ,  pierce), imodbits_none ],
["cudgel", "Cudgel", [("club", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 
	12 , weight(2.5)|difficulty(0)|spd_rtng(99) | weapon_length(66)|swing_damage(13 , blunt) | thrust_damage(0 ,  pierce), imodbits_none ],
["hammer", "Hammer", [("iron_hammer", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry, itc_scimitar, 
	21 , weight(2)|difficulty(0)|spd_rtng(100) | weapon_length(55)|swing_damage(14 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ],
["club", "Club", [("club", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 
	33 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(66)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce), imodbits_none ],
["winged_mace", "Winged Mace", [("winged_mace", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 
	366 , weight(3.5)|difficulty(0)|spd_rtng(99) | weapon_length(65)|swing_damage(21 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ],
["spiked_mace", "Spiked Mace", [("spiked_mace", 0), ("mace_spiked", imodbits_good)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 
	431 , weight(3.5)|difficulty(0)|spd_rtng(95) | weapon_length(72)|swing_damage(22 , blunt) | thrust_damage(0 ,  pierce), imodbits_pick ], #
["military_hammer", "Military Hammer", [("iron_hammer", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 
	462 , weight(4)|difficulty(0)|spd_rtng(92) | weapon_length(58)|swing_damage(25 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ], #
["mace_2", "Knobbed_Mace", [("mace_a", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,
	294 , weight(2.5)|difficulty(0)|spd_rtng(98) | weapon_length(60)|swing_damage(23 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ],
["mace_3", "Spiked Mace", [("mace_c", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,
	456 , weight(2.5)|difficulty(0)|spd_rtng(98) | weapon_length(62)|swing_damage(23 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ],
["mace_4", "Winged_Mace", [("mace_b", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,
	495 , weight(2.5)|difficulty(0)|spd_rtng(98) | weapon_length(60)|swing_damage(24 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ],
["mace_6", "Spiked_Club", [("rrr_mace2", 0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_merchandise|itp_primary, itcf_carry_mace_left_hip|itc_scimitar|itcf_horseback_overswing_left_onehanded|itcf_horseback_overswing_right_onehanded, 
	255, weight(2.5)|abundance(50)|difficulty(7)|spd_rtng(95)|weapon_length(65)|swing_damage(25, blunt), imodbits_pick ],
["mace_7", "Scepter", [("rrr_mace1", 0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_merchandise|itp_primary, itcf_carry_mace_left_hip|itc_scimitar|itcf_horseback_overswing_left_onehanded|itcf_horseback_overswing_right_onehanded, 
	135, weight(1.75)|abundance(25)|spd_rtng(97)|weapon_length(65)|swing_damage(24, blunt), imodbits_pick ],
["talak_mace", "Flanged_Mace", [("talak_mace", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_mace_left_hip,
	598 , weight(2.5)|difficulty(0)|spd_rtng(92) | weapon_length(72)|swing_damage(28 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ],
["mace_pear", "Pear_Mace", [("pear_mace", 0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_merchandise|itp_primary, itcf_carry_mace_left_hip|itc_scimitar, 
	1045, weight(3)|abundance(25)|difficulty(10)|spd_rtng(75)|weapon_length(74)|swing_damage(30, blunt), imodbits_pick ],

#ONE-HANDED BLUNT:  With Pierce
["talak_warhammer", "Warhammer", [("talak_warhammer", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_mace_left_hip,
	957 , weight(2.5)|difficulty(9)|spd_rtng(82) | weapon_length(60)|swing_damage(28 , blunt) | thrust_damage(21 ,  pierce), imodbits_mace ],
["onehandedwarhammer", "Warhammer", [("realhammer", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_longsword|itcf_carry_mace_left_hip, 
	951, weight(3)|difficulty(10)|spd_rtng(90)|weapon_length(52)|swing_damage(27, blunt)|thrust_damage(23, pierce), imodbits_mace ],
["mace_5", "Mace", [("lui_mace", 0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_merchandise|itp_primary, itcf_carry_mace_left_hip|itc_longsword|itcf_horseback_thrust_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_overswing_right_onehanded, 
	366, weight(2.5)|abundance(25)|spd_rtng(99)|weapon_length(65)|thrust_damage(15, pierce)|swing_damage(24, blunt), imodbits_pick ],


#TWO-HANDED BLUNT
["maul", "Maul", [("maul_b", 0)], itp_merchandise|itp_big_2H_axe|itp_wooden_attack, itc_nodachi|itcf_carry_spear, 
	291 , weight(6)|difficulty(11)|spd_rtng(84) | weapon_length(68)|swing_damage(33 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ],
["sledgehammer", "Sledgehammer", [("maul_c", 0)], itp_merchandise|itp_big_2H_axe|itp_wooden_attack, itc_nodachi|itcf_carry_spear, 
	303 , weight(7)|difficulty(12)|spd_rtng(82) | weapon_length(70)|swing_damage(35 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ],
["warhammer", "Wahammer", [("maul_d", 0)], itp_merchandise|itp_type_two_handed_wpn|itp_wooden_attack|itp_two_handed|itp_wooden_parry|itp_bonus_against_shield|itp_primary, itcf_carry_spear|itc_nodachi, 
	927 , weight(9)|difficulty(14)|spd_rtng(85) | weapon_length(65)|swing_damage(38 , blunt) | thrust_damage(0 ,  pierce), imodbits_mace ], #Can be used on horseback
["polehammer", "Polehammer", [("polehammer_1", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe,
	507 , weight(6)|difficulty(14)|spd_rtng(73) | weapon_length(130)|swing_damage(36 , blunt) | thrust_damage(18 ,  blunt), imodbits_polearm ],
["polehammer2", "Polehammer", [("rrr_polehammer2", 0)], itp_merchandise|itp_type_polearm|itp_penalty_with_shield|itp_two_handed|itp_cant_use_on_horseback|itp_wooden_parry|itp_primary|itp_spear, itc_poleaxe, 
	447, weight(3.75)|abundance(30)|difficulty(8)|spd_rtng(90)|weapon_length(90)|thrust_damage(18, blunt)|swing_damage(30, blunt), imodbits_polearm ],
["greathammer", "Great_Hammer", [("greathammer", 0)], itp_merchandise|itp_bonus_against_shield|itp_poleaxe, itc_poleaxe,
	1251, weight(7)|abundance(30)|difficulty(14)|spd_rtng(63)|weapon_length(122)|swing_damage(45, blunt) | thrust_damage(23 ,  blunt), imodbits_polearm ],
["twohandedmace", "Slaver_Chief_Iron", [("lui_twohandedmace", 0)], itp_type_two_handed_wpn|itp_penalty_with_shield|itp_wooden_parry|itp_merchandise|itp_primary, itcf_carry_spear|itc_nodachi|itcf_thrust_onehanded|itcf_overswing_onehanded|itcf_slashright_onehanded|itcf_thrust_twohanded|itcf_slashleft_onehanded, 
	1188, weight(4.5)|abundance(25)|difficulty(12)|spd_rtng(68)|weapon_length(110)|thrust_damage(21, blunt)|swing_damage(30, blunt), imodbits_pick ],

#Kanobou (removed 4 versions without ring to save item space)
["kanobou_wood_stud_ring", "Studded_Wooden_Kanobou", [("kanobou_wood_stud_ring", 0)], itp_merchandise|itp_bonus_against_shield|itp_type_polearm|itp_spear|itp_primary|itp_wooden_parry|itp_wooden_attack|itp_two_handed|itp_cant_use_on_horseback, itc_poleaxe,
	1200, weight(6)|abundance(20)|difficulty(13)|spd_rtng(60)|weapon_length(130)|thrust_damage(30, blunt)|swing_damage(40, blunt), imodbit_cracked|imodbit_balanced|imodbit_heavy ],
["kanobou_wood_spike_ring", "Spiked_Wooden_Kanobou", [("kanobou_wood_spike_ring", 0)], itp_merchandise|itp_bonus_against_shield|itp_type_polearm|itp_spear|itp_primary|itp_wooden_parry|itp_wooden_attack|itp_two_handed|itp_cant_use_on_horseback, itc_poleaxe,
	1350, weight(6.25)|abundance(20)|difficulty(13)|spd_rtng(56)|weapon_length(130)|thrust_damage(30, blunt)|swing_damage(42, blunt), imodbit_cracked|imodbit_balanced|imodbit_heavy ],
["kanobou_iron_stud_ring", "Studded_Iron_Kanobou", [("kanobou_iron_stud_ring", 0)], itp_merchandise|itp_bonus_against_shield|itp_type_polearm|itp_spear|itp_primary|itp_two_handed|itp_cant_use_on_horseback, itc_poleaxe,
	1500, weight(7.25)|abundance(15)|difficulty(14)|spd_rtng(54)|weapon_length(130)|thrust_damage(32, blunt)|swing_damage(44, blunt), imodbit_rusty|imodbit_balanced|imodbit_heavy ],
["kanobou_iron_spike_ring", "Spiked_Iron_Kanobou", [("kanobou_iron_spike_ring", 0)], itp_merchandise|itp_bonus_against_shield|itp_type_polearm|itp_spear|itp_primary|itp_two_handed|itp_cant_use_on_horseback, itc_poleaxe,
	1482, weight(7.5)|abundance(15)|difficulty(14)|spd_rtng(50)|weapon_length(130)|thrust_damage(32, blunt)|swing_damage(46, blunt), imodbit_rusty|imodbit_balanced|imodbit_heavy ],

#TWO-HANDED BLUNT:  With Pierce
["small_pole_hammer", "Pole_Hammer", [("realpolehammerb", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe, 
	1245, weight(5)|difficulty(10)|spd_rtng(72)|weapon_length(165)|swing_damage(32, blunt)|thrust_damage(32, pierce), imodbits_polearm ],
["realtwohandedwarhammer", "Two_Handed_Warhammer", [("realtwohandedwarhammer", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_thrust_polearm|itcf_carry_axe_back, 
	1140, weight(4.5)|difficulty(12)|spd_rtng(82)|weapon_length(75)|swing_damage(36, blunt)|thrust_damage(30, pierce), imodbits_mace ],
["spikepolehammer1", "Polehammer", [("lui_knightpolehammer", 0)], itp_type_polearm|itp_penalty_with_shield|itp_two_handed|itp_cant_use_on_horseback|itp_wooden_parry|itp_merchandise|itp_primary|itp_spear, itc_poleaxe, 
	1707, weight(6)|abundance(25)|difficulty(14)|spd_rtng(60)|weapon_length(225)|thrust_damage(26, pierce)|swing_damage(32, blunt), imodbits_polearm ],
["spikepolehammer2", "Polehammer", [("lui_manhunterpolehammer", 0)], itp_type_polearm|itp_penalty_with_shield|itp_two_handed|itp_cant_use_on_horseback|itp_wooden_parry|itp_merchandise|itp_primary|itp_spear, itc_poleaxe, 
	1107, weight(4)|abundance(25)|difficulty(11)|spd_rtng(80)|weapon_length(140)|thrust_damage(21, pierce)|swing_damage(30, blunt), imodbits_polearm ],
["spikepolehammer3", "Polehammer", [("rrr_polehammer1", 0)], itp_type_polearm|itp_penalty_with_shield|itp_two_handed|itp_cant_use_on_horseback|itp_wooden_parry|itp_merchandise|itp_primary|itp_spear, itc_poleaxe, 
	1107, weight(4.75)|abundance(25)|difficulty(12)|spd_rtng(75)|weapon_length(120)|thrust_damage(18, pierce)|swing_damage(34, blunt), imodbits_polearm ],
["spikepolehammer4", "Polehammer", [("rrr_polehammer3", 0)], itp_type_polearm|itp_penalty_with_shield|itp_two_handed|itp_cant_use_on_horseback|itp_wooden_parry|itp_merchandise|itp_primary|itp_spear, itc_poleaxe, 
	1357, weight(4)|abundance(25)|difficulty(11)|spd_rtng(73)|weapon_length(130)|thrust_damage(18, pierce)|swing_damage(33, blunt), imodbits_polearm ],


#ONE OR TWO-HANDED BLUNT WEAPONS
["club_with_spike_head", "Club_with_Spike", [("mace_e", 0)],  itp_merchandise|itp_type_two_handed_wpn| itp_primary|itp_wooden_parry, itc_bastardsword|itcf_carry_axe_back,
	216 , weight(3.5)|difficulty(9)|spd_rtng(100) | weapon_length(80)|swing_damage(30 , blunt) | thrust_damage(28 ,  pierce), imodbits_mace ],


#ONE-HANDED PIERCE
["pickaxe", "Pickaxe", [("rusty_pick", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 
	81 , weight(3)|difficulty(0)|spd_rtng(96) | weapon_length(65)|swing_damage(21 , pierce) | thrust_damage(0 ,  pierce), imodbits_pick ],
["spiked_club", "Spiked Club", [("spiked_club", 0), ("club_spiked", imodbits_good)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_longsword|itcf_carry_mace_left_hip, 
	249 , weight(3)|difficulty(0)|spd_rtng(97) | weapon_length(68)|swing_damage(21 , pierce) | thrust_damage(21 ,  pierce), imodbits_mace ],
["fighting_pick", "Fighting Pick", [("rusty_pick", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 
	324 , weight(3.5)|difficulty(0)|spd_rtng(94) | weapon_length(65)|swing_damage(26 , pierce) | thrust_damage(0 ,  pierce), imodbits_pick ],
["military_pick", "Military Pick", [("steel_pick", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 
	426 , weight(4)|difficulty(0)|spd_rtng(90) | weapon_length(65)|swing_damage(27 , pierce) | thrust_damage(0 ,  pierce), imodbits_pick ],
["morningstar", "Morningstar", [("mace_morningstar", 0), ("morningstar_mace", imodbits_good)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 
	615 , weight(5.5)|difficulty(13)|spd_rtng(75) | weapon_length(63)|swing_damage(30 , pierce) | thrust_damage(0 ,  pierce), imodbits_mace ],
["mace_1", "Spiked_Club", [("mace_d", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,
	135 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(62)|swing_damage(22 , pierce) | thrust_damage(0 ,  pierce), imodbits_mace ],
["foil", "Foil", [("foil", 0), ("scab_foil", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_parry_onehanded|itcf_thrust_onehanded|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	1214 , weight(0.75)|difficulty(0)|spd_rtng(110) | weapon_length(116)|swing_damage(0 , cut) | thrust_damage(32 ,  pierce), imodbits_sword_high ],


#ONE-HANDED SWORDS
["sickle", "Sickle", [("sickle", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_parry, itc_cleaver, 
	3 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(40)|swing_damage(20 , cut) | thrust_damage(0 ,  pierce), imodbits_none ],
["cleaver", "Cleaver", [("cleaver", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_parry, itc_cleaver, 
	9 , weight(1.5)|difficulty(0)|spd_rtng(103) | weapon_length(30)|swing_damage(24 , cut) | thrust_damage(0 ,  pierce), imodbits_none ],
["knife", "Knife", [("peasant_knife", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left, 
	12 , weight(0.5)|difficulty(0)|spd_rtng(110) | weapon_length(40)|swing_damage(21 , cut) | thrust_damage(13 ,  pierce), imodbits_sword ],
["butchering_knife", "Butchering Knife", [("khyber_knife", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_right, 
	39 , weight(0.75)|difficulty(0)|spd_rtng(108) | weapon_length(60)|swing_damage(24 , cut) | thrust_damage(17 ,  pierce), imodbits_sword ],
["dagger", "Dagger", [("dagger", 0), ("scab_dagger", ixmesh_carry), ("dagger_b", imodbits_good), ("dagger_b_scabbard", ixmesh_carry|imodbits_good)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn, 
	51 , weight(0.75)|difficulty(0)|spd_rtng(112) | weapon_length(47)|swing_damage(19 , cut) | thrust_damage(23 ,  pierce), imodbits_sword_high ],
["falchion", "Falchion", [("falchion", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 
	315 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(73)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce), imodbits_sword ],
["scimitar", "Scimitar", [("scimeter", 0), ("scab_scimeter", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 
	324 , weight(1.5)|difficulty(0)|spd_rtng(105) | weapon_length(97)|swing_damage(29 , cut) | thrust_damage(0 ,  pierce), imodbits_sword_high ],
["katzbalger", "Katzbalger", [("katzbalger", 0), ("scab_katzbalger", ixmesh_carry)], itp_merchandise|itp_longsword, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	712 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(84)|swing_damage(27 , cut) | thrust_damage(25 ,  pierce), imodbits_sword_high ],
["nordic_sword", "Northman's_Short_Sword", [("talak_nordic_sword", 0), ("scab_talak_nordic_sword", ixmesh_carry)], itp_merchandise|itp_longsword, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	712, weight(1.25)|difficulty(0)|spd_rtng(101)|weapon_length(75)|swing_damage(28, cut)|thrust_damage(23, pierce), imodbits_sword_high ],
["seax", "Seax", [("seax", 0), ("scab_seax", ixmesh_carry)], itp_merchandise|itp_longsword, itc_longsword|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn,
	300, weight(0.75)|difficulty(0)|spd_rtng(108)|weapon_length(47)|swing_damage(22, cut)|thrust_damage(24, pierce), imodbits_sword_high ],
["sword_medieval_a", "Sword", [("sword_medieval_a", 0), ("sword_medieval_a_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	489 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(27 , cut) | thrust_damage(23 ,  pierce), imodbits_sword_high ],
["sword_medieval_b", "Sword", [("sword_medieval_b", 0), ("sword_medieval_b_scabbard", ixmesh_carry), ("sword_rusty_a", imodbit_rusty), ("sword_rusty_a_scabbard", ixmesh_carry|imodbit_rusty)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	729 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(28 , cut) | thrust_damage(24 ,  pierce), imodbits_sword_high ],
["sword_medieval_b_small", "Short Sword", [("sword_medieval_b_small", 0), ("sword_medieval_b_small_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	456 , weight(1.5)|difficulty(0)|spd_rtng(102) | weapon_length(85)|swing_damage(26, cut) | thrust_damage(25, pierce), imodbits_sword_high ],
["sword_medieval_c", "Arming Sword", [("sword_medieval_c", 0), ("sword_medieval_c_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	794 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(29 , cut) | thrust_damage(24 ,  pierce), imodbits_sword_high ],
["sword_medieval_c_small", "Short Arming Sword", [("sword_medieval_c_small", 0), ("sword_medieval_c_small_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	673 , weight(1.5)|difficulty(0)|spd_rtng(103) | weapon_length(86)|swing_damage(26, cut) | thrust_damage(25 ,  pierce), imodbits_sword_high ],
["sword_viking_1", "Nordic Sword", [("sword_viking_c", 0), ("sword_viking_c_scabbard ", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	441 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(94)|swing_damage(28 , cut) | thrust_damage(22 ,  pierce), imodbits_sword_high ] ,
["sword_viking_2", "Nordic Sword", [("sword_viking_b", 0), ("sword_viking_b_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	794 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(29 , cut) | thrust_damage(23 ,  pierce), imodbits_sword_high ],
["sword_viking_2_small", "Nordic Short Sword", [("sword_viking_b_small", 0), ("sword_viking_b_small_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	486 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(85)|swing_damage(28 , cut) | thrust_damage(24 ,  pierce), imodbits_sword_high ],
["sword_viking_3", "Nordic Sword", [("sword_viking_a", 0), ("sword_viking_a_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	836 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(30 , cut) | thrust_damage(23 ,  pierce), imodbits_sword_high ],
["sword_viking_3_small", "Nordic Sword", [("sword_viking_a_small", 0), ("sword_viking_a_small_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	794 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(86)|swing_damage(29 , cut) | thrust_damage(24 ,  pierce), imodbits_sword_high ],
["sword_khergit_1", "Nomad Sabre", [("khergit_sword_b", 0), ("khergit_sword_b_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	315 , weight(1.25)|difficulty(0)|spd_rtng(100) | weapon_length(97)|swing_damage(29 , cut), imodbits_sword_high ],
["sword_khergit_2", "Sabre", [("khergit_sword_c", 0), ("khergit_sword_c_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	573 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(97)|swing_damage(30 , cut), imodbits_sword_high ],
["sword_khergit_3", "Sabre", [("khergit_sword_a", 0), ("khergit_sword_a_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	880 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(98)|swing_damage(31 , cut), imodbits_sword_high ],
["sword_khergit_4", "Heavy Sabre", [("khergit_sword_d", 0), ("khergit_sword_d_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	880 , weight(1.75)|difficulty(0)|spd_rtng(96) | weapon_length(96)|swing_damage(32 , cut), imodbits_sword_high ],


#TWO-HANDED SWORDS
["sword_of_war", "Sword of War", [("b_bastard_sword", 0), ("scab_bastardsw_b", ixmesh_carry)], itp_merchandise|itp_2H_sword, itc_2H_sword|itcf_carry_sword_back|itcf_show_holster_when_drawn,
	1572 , weight(3)|difficulty(11)|spd_rtng(93) | weapon_length(122)|swing_damage(40 , cut) | thrust_damage(31 ,  pierce), imodbits_sword_high ],
["sword_two_handed_b", "Two Handed Sword", [("sword_two_handed_b", 0)], itp_merchandise|itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back,
	1817 , weight(2.75)|difficulty(10)|spd_rtng(93) | weapon_length(110)|swing_damage(40 , cut) | thrust_damage(27 ,  pierce), imodbits_sword_high ],
["sword_two_handed_a", "Great Sword", [("sword_two_handed_a", 0)], itp_merchandise|itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back,
	1870 , weight(2.75)|difficulty(10)|spd_rtng(89) | weapon_length(120)|swing_damage(42 , cut) | thrust_damage(29 ,  pierce), imodbits_sword_high ],
["realknightgreatsword", "Knight_Great_Sword", [("realknightgreatsword", 0)], itp_merchandise|itp_2H_sword, itc_2H_sword|itcf_carry_sword_back, 
	1709, weight(2.75)|difficulty(9)|spd_rtng(90)|weapon_length(128)|swing_damage(38, cut)|thrust_damage(29, pierce), imodbits_sword_high ],
["noble_greatsword", "Noble_Great_Sword", [("realgreatsworde", 0)], itp_merchandise|itp_2H_sword, itc_2H_sword|itcf_carry_sword_back, 
	1762, weight(3)|difficulty(9)|spd_rtng(88)|weapon_length(128)|swing_damage(40, cut)|thrust_damage(29, pierce), imodbits_sword_high ],
#TWO-HANDED SWORDS:  Pierce Only
["estoc", "Estoc", [("estoc", 0), ("scab_estoc", ixmesh_carry)], itp_merchandise|itp_big_2H_sword, itc_parry_two_handed|itcf_thrust_onehanded|itcf_carry_sword_back|itcf_show_holster_when_drawn,
	1214 , weight(1.8)|difficulty(0)|spd_rtng(98) | weapon_length(135)|swing_damage(0 , cut) | thrust_damage(34 ,  pierce), imodbits_sword_high ],
#TWO-HANDED SWORDS - BIG
["realtwohander", "Veteran_Great_Sword", [("realtwohander", 0)], itp_merchandise|itp_big_2H_sword, itc_big_2H_sword|itcf_carry_sword_back, 
	1658, weight(2.75)|difficulty(9)|spd_rtng(86)|weapon_length(137)|swing_damage(38, cut)|thrust_damage(27, pierce), imodbits_sword_high ],
["realcrusadersword", "Crusader_Great_Sword", [("realcrusadersword", 0), ("realcrusaderswordscaba", ixmesh_carry)], itp_merchandise|itp_big_2H_sword, itc_big_2H_sword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 
	1713, weight(2.75)|difficulty(10)|spd_rtng(86)|weapon_length(138)|swing_damage(37, cut)|thrust_damage(28, pierce), imodbits_sword_high ],
["espadona", "Espadon", [("realespadona", 0)], itp_merchandise|itp_big_2H_sword, itc_big_2H_sword|itcf_carry_sword_back, 
	1614, weight(3.5)|difficulty(10)|spd_rtng(78)|weapon_length(160)|swing_damage(36, cut)|thrust_damage(35, pierce), imodbits_sword_high ],
["swadianespadon", "Espadon", [("swadianespadon", 0)], itp_merchandise|itp_big_2H_sword, itc_big_2H_sword|itcf_carry_sword_back, 
	1614, weight(3.75)|difficulty(10)|spd_rtng(79)|weapon_length(155)|swing_damage(36, cut)|thrust_damage(35, pierce), imodbits_sword_high ],
["darkespadon", "Dark_Knight_Espadon", [("darkknightsword", 0)], itp_merchandise|itp_big_2H_sword, itc_big_2H_sword|itcf_carry_sword_back, 
	1663, weight(3.5)|difficulty(10)|spd_rtng(79)|weapon_length(163)|swing_damage(36, cut)|thrust_damage(35, pierce), imodbits_sword_high ],
["flamberge", "Flamberge", [("realflamberge", 0)], itp_merchandise|itp_big_2H_sword, itc_big_2H_sword|itcf_carry_sword_back, 
	1817, weight(3)|difficulty(10)|spd_rtng(83)|weapon_length(150)|swing_damage(40, cut)|thrust_damage(30, pierce), imodbits_sword_high ],
["flambergec", "Flamberge", [("realflambergeb", 0)], itp_merchandise|itp_big_2H_sword, itc_big_2H_sword|itcf_carry_sword_back, 
	1925, weight(3)|difficulty(11)|spd_rtng(80)|weapon_length(158)|swing_damage(41, cut)|thrust_damage(30, pierce), imodbits_sword_high ],
["mountainlordsword", "Mountain_Lord_Great_Sword", [("mountainlordsword", 0)], itp_merchandise|itp_big_2H_sword, itc_big_2H_sword|itcf_carry_sword_back, 
	1709, weight(2.75)|difficulty(9)|spd_rtng(81)|weapon_length(155)|swing_damage(39, cut)|thrust_damage(30, pierce), imodbits_sword_high ],


#ONE OR TWO-HANDED SWORDS
["bastard_sword_a", "Bastard Sword", [("bastard_sword_a", 0), ("bastard_sword_a_scabbard", ixmesh_carry)], itp_merchandise|itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	882 , weight(2.25)|difficulty(9)|spd_rtng(98) | weapon_length(101)|swing_damage(37 , cut) | thrust_damage(27 ,  pierce), imodbits_sword_high ],
["bastard_sword_b", "Heavy Bastard Sword", [("bastard_sword_b", 0), ("bastard_sword_b_scabbard", ixmesh_carry)], itp_merchandise|itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	1578 , weight(2.25)|difficulty(9)|spd_rtng(96) | weapon_length(105)|swing_damage(37 , cut) | thrust_damage(28 ,  pierce), imodbits_sword_high ],
["cimitar", "Cimitar", [("cimitarb", 0)], itp_merchandise|itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_sword_back, 
	1663, weight(3.25)|abundance(15)|difficulty(10)|spd_rtng(85)|weapon_length(128)|swing_damage(38, cut)|thrust_damage(19, pierce), imodbits_sword_high ],
["talak_bastard_sword", "Hand_and_a_Half_Sword", [("talak_bastard_sword", 0), ("scab_bastard_sword", ixmesh_carry)], itp_merchandise|itp_bastard_sword, itc_bastard_sword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	1163 , weight(2.25)|difficulty(0)|spd_rtng(98) | weapon_length(100)|swing_damage(37 , cut) | thrust_damage(27 ,  pierce), imodbits_sword_high ],
["realbastarda", "Sergent_Bastard_Sword", [("realbastard", 0), ("realbastardscaba", ixmesh_carry)], itp_merchandise|itp_bastard_sword, itc_bastard_sword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 
	1559, weight(2.25)|difficulty(9)|spd_rtng(98)|weapon_length(102)|swing_damage(35, cut)|thrust_damage(28, pierce), imodbits_sword_high ],
["realbastarde", "Baron_Bastard_Sword", [("realbastarde", 0), ("realbastardescaba", ixmesh_carry)], itp_merchandise|itp_bastard_sword, itc_bastard_sword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 
	1658, weight(2.25)|difficulty(9)|spd_rtng(99)|weapon_length(104)|swing_damage(36, cut)|thrust_damage(27, pierce), imodbits_sword_high ],
["goldscimitar", "Cimitar", [("goldscimitar", 0)], itp_merchandise|itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_sword_back, 
	1663, weight(2.5)|abundance(9)|difficulty(10)|spd_rtng(94)|weapon_length(110)|swing_damage(36, cut)|thrust_damage(24, pierce), imodbits_sword_high ],


#ONE-HANDED AXES
["hatchet", "Hatchet", [("hatchet", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 
	9 , weight(2)|difficulty(0)|spd_rtng(97) | weapon_length(60)|swing_damage(23 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["hand_axe", "Hand Axe", [("hatchet", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 
	72 , weight(2)|difficulty(7)|spd_rtng(95) | weapon_length(75)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["one_handed_war_axe_a", "One Handed War Axe", [("one_handed_war_axe_a", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
	261 , weight(1.5)|difficulty(9)|spd_rtng(100) | weapon_length(60)|swing_damage(33 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["one_handed_war_axe_b", "One Handed War Axe", [("one_handed_war_axe_b", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
	411 , weight(1.5)|difficulty(9)|spd_rtng(98) | weapon_length(61)|swing_damage(34 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["one_handed_battle_axe_a", "One Handed Battle Axe", [("one_handed_battle_axe_a", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
	306 , weight(1.5)|difficulty(9)|spd_rtng(97) | weapon_length(69)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["one_handed_battle_axe_b", "One Handed Battle Axe", [("one_handed_battle_axe_b", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
	513 , weight(1.75)|difficulty(9)|spd_rtng(96) | weapon_length(70)|swing_damage(36 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["one_handed_battle_axe_c", "One Handed Battle Axe", [("one_handed_battle_axe_c", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
	882 , weight(2)|difficulty(9)|spd_rtng(95) | weapon_length(72)|swing_damage(36 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["jomsviking_axe", "Jomsviking_Axe", [("jomsviking_axe", 0)], itp_merchandise|itp_handaxe, itc_handaxe|itcf_carry_mace_left_hip,
	794 , weight(1.5)|difficulty(0)|spd_rtng(97) | weapon_length(55)|swing_damage(34 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],


#TWO-HANDED AXES
["battle_axe", "Battle Axe", [("battle_ax", 0)], itp_merchandise|itp_2H_axe, itc_2H_axe|itcf_carry_axe_back, 
	720 , weight(3.75)|difficulty(9)|spd_rtng(90) | weapon_length(91)|swing_damage(44 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["two_handed_axe",  "Two_Handed_Axe", [("two_handed_battle_axe_a", 0)], itp_merchandise|itp_2H_axe, itc_2H_axe|itcf_carry_axe_back,
	330 , weight(3.5)|difficulty(10)|spd_rtng(95) | weapon_length(90)|swing_damage(42 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["two_handed_battle_axe_2", "Two_Handed_War_Axe", [("two_handed_battle_axe_b", 0)], itp_merchandise|itp_2H_axe, itc_2H_axe|itcf_carry_axe_back,
	606 , weight(4)|difficulty(10)|spd_rtng(92) | weapon_length(92)|swing_damage(47 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["axe", "Axe", [("iron_ax", 0)], itp_merchandise|itp_2H_axe, itc_2H_axe|itcf_carry_axe_back, 
	195 , weight(4)|difficulty(8)|spd_rtng(88) | weapon_length(92)|swing_damage(36 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["nord_battle_axe", "Northman's_War_Axe", [("vikingaxeb", 0)], itp_merchandise|itp_2H_axe, itc_2H_axe|itcf_carry_axe_back, 
	1800, weight(3.25)|difficulty(9)|spd_rtng(94)|weapon_length(105)|swing_damage(46, cut)|thrust_damage(0, pierce), imodbits_axe ],
#TWO-HANDED AXES - BIG     itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry| itp_cant_use_on_horseback
["war_axe", "War Axe", [("war_ax", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_carry_axe_back, 
	792 , weight(4.25)|difficulty(10)|spd_rtng(87) | weapon_length(115)|swing_damage(47 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["great_axe", "Great_Axe", [("two_handed_battle_axe_e", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_carry_axe_back,
	1338 , weight(4.5)|difficulty(12)|spd_rtng(85) | weapon_length(91)|swing_damage(50 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["executionner_axe_", "Two_Handed_Battle_Axe", [("realbattleaxe", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_thrust_polearm|itcf_carry_axe_back, 
	1320, weight(4)|difficulty(10)|spd_rtng(88)|weapon_length(98)|swing_damage(49, cut)|thrust_damage(21, pierce), imodbits_axe ],
["footmen_battle_axe", "Footmen_Battle_Axe", [("realbattleaxeb", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_thrust_polearm|itcf_carry_axe_back, 
	1800, weight(4.5)|difficulty(10)|spd_rtng(88)|weapon_length(105)|swing_damage(47, cut)|thrust_damage(29, pierce), imodbits_axe ],
["dblhead_axe_2", "Double_Sided_Axe", [("dblhead_axe_2", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_cant_use_on_horseback|itp_wooden_parry|itp_bonus_against_shield|itp_merchandise|itp_primary, itcf_carry_axe_back|itc_parry_polearm|itcf_overswing_twohanded|itcf_slashleft_polearm|itcf_slashright_polearm, 
	1392, weight(6)|abundance(25)|difficulty(12)|spd_rtng(87)|weapon_length(89)|swing_damage(45, cut), imodbits_axe ],
["berdiche_axe", "Double_Sided_Axe", [("dblhead_axe_3", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_cant_use_on_horseback|itp_wooden_parry|itp_bonus_against_shield|itp_merchandise|itp_primary, itcf_carry_axe_back|itc_parry_polearm|itcf_overswing_twohanded|itcf_slashleft_polearm|itcf_slashright_polearm, 
	1392, weight(6.5)|abundance(25)|difficulty(12)|spd_rtng(85)|weapon_length(95)|swing_damage(46, cut), imodbits_pick ],

#ONE OR TWO-HANDED AXES
["fighting_axe", "Fighting Axe", [("fighting_ax", 0)], itp_merchandise|itp_bastard_axe, itc_bastard_axe|itcf_carry_axe_left_hip, 
	531 , weight(2.5)|difficulty(9)|spd_rtng(95) | weapon_length(90)|swing_damage(41 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["nordic_axe", "Nordic_Axe", [("nordic_axe", 0)], itp_merchandise|itp_bastard_axe, itc_bastard_axe|itcf_carry_mace_left_hip,
	1092 , weight(3)|difficulty(9)|spd_rtng(95) | weapon_length(70)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["raider_battle_axe", "Raider_War_Axe", [("vikingaxe", 0)], itp_merchandise|itp_bastard_axe, itc_bastard_axe|itcf_carry_mace_left_hip, 
	900, weight(2.5)|difficulty(10)|spd_rtng(96)|weapon_length(62)|swing_damage(41, cut)|thrust_damage(0, pierce), imodbits_axe ],
["dblhead_axe_1", "Double_Sided_Riders_Axe", [("dblhead_axe_1", 0)], itp_merchandise|itp_bastard_axe, itc_bastard_axe|itcf_carry_mace_left_hip, 
	1520, weight(3.5)|abundance(50)|difficulty(10)|spd_rtng(85)|weapon_length(87)|swing_damage(39, cut)|thrust_damage(0, pierce), imodbits_axe ],


#POLE-ARMS AND AXE VARIENTS
["voulge", "Voulge", [("voulge", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_carry_axe_back, 
	387 , weight(4.5)|difficulty(8)|spd_rtng(87) | weapon_length(119)|swing_damage(45 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["two_handed_battle_axe_3", "Short_Voulge", [("two_handed_battle_axe_c", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_carry_axe_back,
	774 , weight(4.25)|difficulty(10)|spd_rtng(87) | weapon_length(100)|swing_damage(48 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["bardiche", "Bardiche", [("two_handed_battle_axe_d", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_carry_axe_back,
	933 , weight(4.5)|difficulty(10)|spd_rtng(84) | weapon_length(102)|swing_damage(49 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["great_bardiche", "Great_Bardiche", [("two_handed_battle_axe_f", 0)], itp_merchandise|itp_big_2H_axe, itc_big_2H_axe|itcf_carry_axe_back,
	1851 , weight(4.75)|difficulty(11)|spd_rtng(83) | weapon_length(116)|swing_damage(48 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["shortened_military_scythe",   "Shortened Military Scythe", [("two_handed_battle_scythe_a", 0)], itp_merchandise|itp_type_two_handed_wpn|itp_always_loot| itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back,
	792 , weight(3)|difficulty(10)|spd_rtng(90) | weapon_length(112)|swing_damage(44 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],


#Similar to Two-Handed Axe but deals piercing damage
["talak_morningstar", "Two-Handed_Morningstar", [("talak_morningstar", 0)], itp_merchandise|itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_cant_use_on_horseback|itp_bonus_against_shield, itc_nodachi|itcf_carry_spear,
	903 , weight(5)|difficulty(13)|spd_rtng(75) | weapon_length(70)|swing_damage(38 , pierce) | thrust_damage(0 ,  pierce), imodbits_mace ],


#POLEAXES: Non Horseback, No parry, Penalty with Shields
["scythe", "Scythe", [("scythe", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe|itcf_carry_spear, 
	129 , weight(3.5)|difficulty(0)|spd_rtng(79) | weapon_length(182)|swing_damage(29 , cut) | thrust_damage(18 ,  pierce), imodbits_polearm ],
["realhalberda", "Hallberd", [("realhalberd", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe, 
	1050, weight(4)|difficulty(9)|spd_rtng(81)|weapon_length(166)|swing_damage(37, cut)|thrust_damage(32, pierce), imodbits_polearm ],
["realhalberdb", "Hallberd", [("realhalberdb", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe, 
	1056, weight(4)|difficulty(9)|spd_rtng(83)|weapon_length(156)|swing_damage(37, cut)|thrust_damage(32, pierce), imodbits_polearm ],
["realhalberdc", "Hallberd", [("realhalberdc", 0)], itp_merchandise|itp_poleaxe, itc_big_pike|itcf_overswing_polearm|itc_parry_polearm, 
	1086, weight(4.75)|difficulty(10)|spd_rtng(79)|weapon_length(207)|swing_damage(34, cut)|thrust_damage(32, pierce), imodbits_polearm ],
["realhalberdd", "Hallberd", [("realhalberdd", 0)], itp_merchandise|itp_poleaxe, itc_big_pike|itcf_overswing_polearm|itc_parry_polearm, 
	1056, weight(4.5)|difficulty(9)|spd_rtng(80)|weapon_length(192)|swing_damage(35, cut)|thrust_damage(32, pierce), imodbits_polearm ],
["realhalberde", "Hallberd", [("realhalberde", 0)], itp_merchandise|itp_poleaxe|itp_no_parry, itc_big_pike|itcf_overswing_polearm|itc_parry_polearm, 
	1116, weight(4.75)|difficulty(10)|spd_rtng(79)|weapon_length(232)|swing_damage(34, cut)|thrust_damage(32, pierce), imodbits_polearm ],
["realhalberdf", "Hallberd", [("realhalberdf", 0)], itp_merchandise|itp_poleaxe, itc_big_pike|itcf_overswing_polearm|itc_parry_polearm, 
	1056, weight(4.5)|difficulty(9)|spd_rtng(80)|weapon_length(195)|swing_damage(35, cut)|thrust_damage(19, pierce), imodbits_polearm ],
["realglaive", "Glaive", [("realglaive", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe,
   1356, weight(4.5)|difficulty(9)|spd_rtng(81)|weapon_length(240)|swing_damage(36, cut)|thrust_damage(21, pierce), imodbits_polearm ],
["glaive", "Glaive", [("glaive", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe,
	1056 , weight(4)|difficulty(0)|spd_rtng(83) | weapon_length(157)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce), imodbits_polearm ],
["talak_halberd", "Halberd", [("talak_halberd", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe,
	1214 , weight(4.5)|difficulty(0)|spd_rtng(85) | weapon_length(155)|swing_damage(37 , cut) | thrust_damage(32 ,  pierce), imodbits_polearm ],
["small_pole_axe", "Pole_Axe", [("realpoleaxe", 0)], itp_merchandise|itp_poleaxe, itc_poleaxe, 
	1245, weight(5)|difficulty(9)|spd_rtng(75)|weapon_length(157)|swing_damage(38, cut)|thrust_damage(32, pierce), imodbits_polearm ],


#STAFFS
["staff", "Staff", [("wooden_staff", 0)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_carry_sword_back,
	108 , weight(1.5)|difficulty(0)|spd_rtng(102) | weapon_length(130)|swing_damage(22 , blunt) | thrust_damage(18 ,  blunt), imodbits_polearm ],
["quarter_staff", "Quarter Staff", [("quarter_staff", 0)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_carry_sword_back,
	180 , weight(2)|difficulty(0)|spd_rtng(104) | weapon_length(140)|swing_damage(25 , blunt) | thrust_damage(20 ,  blunt), imodbits_polearm ],
["iron_staff", "Iron Staff", [("iron_staff", 0), ("staff_iron", imodbits_bad)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_penalty_with_shield, itc_staff|itcf_carry_sword_back,
	606 , weight(2)|difficulty(0)|spd_rtng(97) | weapon_length(140)|swing_damage(27 , blunt) | thrust_damage(22 ,  blunt), imodbits_polearm ],


#PIKES: 2H, No parry, Non Horseback, Penalty with Shields
["realpikec", "Large_Hook_Pike", [("realspearg", 0)], itp_merchandise|itp_big_pike, itc_big_pike, 
	636, weight(5.5)|difficulty(9)|spd_rtng(82)|weapon_length(400)|swing_damage(0, cut)|thrust_damage(35, pierce), imodbits_polearm ],
["realpiked", "Pike", [("realpoleaxeb", 0)], itp_merchandise|itp_big_pike, itc_big_pike, 
	666, weight(5.75)|difficulty(9)|spd_rtng(80)|weapon_length(440)|swing_damage(0, cut)|thrust_damage(35, pierce), imodbits_polearm ],
["realpike", "Pike", [("realspearc", 0)], itp_merchandise|itp_big_pike, itc_big_pike, 
	696, weight(5.75)|difficulty(9)|spd_rtng(79)|weapon_length(450)|swing_damage(0, cut)|thrust_damage(36, pierce), imodbits_polearm ],
["realpikeb", "Elite_Pike", [("realspeard", 0)], itp_merchandise|itp_big_pike, itc_big_pike, 
	756, weight(6)|difficulty(9)|spd_rtng(75)|weapon_length(500)|swing_damage(0, cut)|thrust_damage(37, pierce), imodbits_polearm ],


#PIKES: Can Parry
["pike", "Pike", [("spear_a_3m", 0)], itp_merchandise|itp_type_polearm| itp_cant_use_on_horseback|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,
	375 , weight(3)|difficulty(0)|spd_rtng(85) | weapon_length(245)|swing_damage(22 , blunt) | thrust_damage(32 ,  pierce), imodbits_polearm ],


#SPEARS
["pitch_fork", "Pitch Fork", [("pitch_fork_1", 0)], itp_merchandise|itp_warspear, itc_spear|itcf_overswing_polearm, 
	57 , weight(3.5)|difficulty(0)|spd_rtng(88) | weapon_length(154)|swing_damage(20 , blunt) | thrust_damage(24, pierce), imodbits_polearm ],
["military_fork_1", "Military Fork", [("military_fork_1", 0)], itp_merchandise|itp_warspear, itc_spear|itcf_overswing_polearm, 
	459 , weight(3.5)|difficulty(0)|spd_rtng(91) | weapon_length(135)|swing_damage(23 , blunt) | thrust_damage(32, pierce), imodbits_polearm ],
["battle_fork_1", "Battle Fork", [("battle_fork_1", 0)], itp_merchandise|itp_warspear, itc_spear|itcf_overswing_polearm, 
	846 , weight(3.75)|difficulty(0)|spd_rtng(90) | weapon_length(142)|swing_damage(23 , pierce) | thrust_damage(32, pierce), imodbits_polearm ],
["trident_1", "Trident", [("trident_1", 0)], itp_merchandise|itp_warspear, itc_spear|itcf_overswing_polearm, 
	846 , weight(4)|difficulty(0)|spd_rtng(89) | weapon_length(152)|swing_damage(23 , blunt) | thrust_damage(30, pierce), imodbits_polearm ],
["boar_spear", "Broadhead Spear", [("spear", 0)], itp_merchandise|itp_warspear, itc_spear|itcf_overswing_polearm, 
	228 , weight(3)|difficulty(0)|spd_rtng(95) | weapon_length(157)|swing_damage(23 , blunt) | thrust_damage(34 ,  pierce), imodbits_polearm ],
["ashwood_pike", "Ashwood Pike", [("pike", 0)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_cutting_spear,
	615 , weight(3.25)|difficulty(11)|spd_rtng(92) | weapon_length(170)|swing_damage(23 , blunt) | thrust_damage(32,  pierce), imodbits_polearm ],
["awlpike", "Awlpike", [("pike", 0)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_cutting_spear,
	1134 , weight(3.5)|difficulty(12)|spd_rtng(90) | weapon_length(170)|swing_damage(23 , blunt) | thrust_damage(33 ,  pierce), imodbits_polearm ],
["shortened_spear", "Shortened_Spear", [("spear_g_1-9m", 0)], itp_merchandise|itp_warspear, itc_staff|itcf_carry_spear,
	159 , weight(2)|difficulty(0)|spd_rtng(102) | weapon_length(120)|swing_damage(22 , blunt) | thrust_damage(34 ,  pierce), imodbits_polearm ],
["spear", "Spear", [("spear_h_2-15m", 0)], itp_merchandise|itp_warspear, itc_staff,
	225 , weight(2.25)|difficulty(0)|spd_rtng(98) | weapon_length(135)|swing_damage(23 , blunt) | thrust_damage(34 ,  pierce), imodbits_polearm ],
["war_spear", "War_Spear", [("spear_i_2-3m", 0)], itp_merchandise|itp_warspear, itc_staff,
	270 , weight(2.5)|difficulty(0)|spd_rtng(96) | weapon_length(150)|swing_damage(24 , blunt) | thrust_damage(35 ,  pierce), imodbits_polearm ],
["double_sided_lance", "Double Sided Lance", [("lance_dblhead", 0)], itp_warspear|itp_merchandise, itc_staff, 
	873 , weight(2.75)|difficulty(0)|spd_rtng(99) | weapon_length(130)|swing_damage(25 , blunt) | thrust_damage(32 ,  pierce), imodbits_polearm ],
["boar_scythe", "Military Scythe", [("spear_e_2-5m", 0), ("spear_c_2-5m", imodbits_bad)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
	435 , weight(2.5)|difficulty(10)|spd_rtng(89) | weapon_length(155)|swing_damage(36 , cut) | thrust_damage(25 ,  pierce), imodbits_polearm ],
["light_lance", "Light Lance", [("spear_b_2-75m", 0)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,
	267 , weight(2.5)|difficulty(0)|spd_rtng(90) | weapon_length(175)|swing_damage(22 , blunt) | thrust_damage(29 ,  pierce), imodbits_polearm ],
["lance", "Lance", [("spear_d_2-8m", 0)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,
	330 , weight(2.75)|difficulty(0)|spd_rtng(88) | weapon_length(180)|swing_damage(22 , blunt) | thrust_damage(29 ,  pierce), imodbits_polearm ],
["heavy_lance", "Heavy Lance", [("spear_f_2-9m", 0)], itp_merchandise|itp_type_polearm| itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,
	390 , weight(3)|difficulty(10)|spd_rtng(85) | weapon_length(190)|swing_damage(24 , blunt) | thrust_damage(29 ,  pierce), imodbits_polearm ],


#GREAT LANCES
["jousting_lance", "Blunt Lance", [("jousting_lance_new", 0)], itp_type_polearm|itp_merchandise|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance, 
	504 , weight(5)|difficulty(0)|spd_rtng(61) | weapon_length(218)|swing_damage(0 , cut) | thrust_damage(20 ,  blunt), imodbits_polearm ],
["talak_lance", "Great_Lance", [("talak_lance", 0)], itp_merchandise|itp_greatlance, itc_greatlance,
	1050, weight(3)|difficulty(10)|spd_rtng(85)|weapon_length(235)|swing_damage(0, cut)|thrust_damage(28, pierce), imodbits_polearm ],
["great_lanceb", "Young_Knight_Great_Lance", [("heavylanceb", 0)], itp_merchandise|itp_greatlance, itc_greatlance, 
	666, weight(5)|difficulty(10)|spd_rtng(55)|weapon_length(416)|swing_damage(0, cut)|thrust_damage(29, pierce), imodbits_polearm ],
["great_lancec", "Old_Realm_Great_Lance", [("heavy_lanceb", 0)], itp_merchandise|itp_greatlance, itc_greatlance, 
	711, weight(6)|difficulty(11)|spd_rtng(50)|weapon_length(530)|swing_damage(0, cut)|thrust_damage(29, pierce), imodbits_polearm ],


##############
#Miscellaneous
##############
# ["torch", "Torch", [("club", 0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar, 
	# 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(95)|swing_damage(11 , blunt) | thrust_damage(0 ,  pierce), imodbits_none,
 # [(ti_on_init_item, [(set_position_delta, 0, 60, 0), (particle_system_add_new, "psys_torch_fire"), (particle_system_add_new, "psys_torch_smoke"), (set_current_color, 150, 130, 70), (add_point_light, 10, 30), #No merchandise (will cause game to crash if put in inventory)
# ])]],
# This is not a fauchard. Kept to prevent compatibility problems. Is not merchandise, not for sale.
# ["fauchard", "Fauchard", [("fauchard", 0), ("fauchardscaba", ixmesh_carry)], itp_2H_sword, itc_2H_sword|itcf_carry_mask, 
	# 1150, weight(3)|difficulty(10)|spd_rtng(88)|weapon_length(130)|swing_damage(40, cut)|thrust_damage(28, pierce), imodbits_sword_high ],


##############
#SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS SHIELDS
##############

#Native Shields in the CommonRes folder:  Shielfs.brf
["wooden_shield", "Wooden Shield", [("shield_round_a", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	126 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(50), imodbits_shield ],
["nordic_shield", "Nordic Shield", [("shield_round_b", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	254 , weight(2)|hit_points(440)|body_armor(1)|spd_rtng(100)|weapon_length(50), imodbits_shield ],
["fur_covered_shield",  "Fur Covered Shield", [("shield_kite_m", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	461 , abundance(25)|weight(3.5)|hit_points(600)|body_armor(1)|spd_rtng(76)|weapon_length(81), imodbits_shield ],
["steel_shield", "Steel Shield", [("shield_dragon", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  
	642 , weight(4)|hit_points(700)|body_armor(17)|spd_rtng(61)|weapon_length(40), imodbits_shield ],
["plate_covered_round_shield", "Plate_Covered_Round_Shield", [("shield_round_e", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  
	420 , abundance(25)|weight(4)|hit_points(330)|body_armor(16)|spd_rtng(90)|weapon_length(40), imodbits_shield ],
["leather_covered_round_shield", "Leather_Covered_Round_Shield", [("shield_round_d", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	240 , abundance(25)|weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40), imodbits_shield ],
["hide_covered_round_shield", "Hide_Covered_Round_Shield", [("shield_round_f", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	120 , abundance(25)|weight(2)|hit_points(260)|body_armor(3)|spd_rtng(100)|weapon_length(40), imodbits_shield ],
["shield_heater_c", "Heater Shield", [("shield_heater_c", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	245 , weight(3.5)|hit_points(410)|body_armor(2)|spd_rtng(80)|weapon_length(50), imodbits_shield ],

#Some cool Native Shields in the CommonRes folder:  Shielfs_b.brf
["norman_shield_1", "Kite Shield", [("norman_shield_1", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	354 , abundance(25)|weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90), imodbits_shield ],
["norman_shield_3", "Kite Shield", [("norman_shield_3", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	354 , abundance(25)|weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90), imodbits_shield ],
["norman_shield_6", "Kite Shield", [("norman_shield_6", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	354 , abundance(25)|weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90), imodbits_shield ],
["norman_shield_7", "Kite Shield", [("norman_shield_7", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	354 , abundance(25)|weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90), imodbits_shield ],
["norman_shield_8", "Kite Shield", [("norman_shield_8", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	354 , abundance(25)|weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90), imodbits_shield ],

["tab_shield_round_a", "Old Round Shield", [("tableau_shield_round_5", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	78 , weight(2.5)|hit_points(350)|body_armor(0)|spd_rtng(93)|weapon_length(50), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_5", ":agent_no", ":troop_no")])]],
["tab_shield_round_b", "Plain Round Shield", [("tableau_shield_round_3", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	195 , weight(3)|hit_points(460)|body_armor(2)|spd_rtng(90)|weapon_length(50), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_3", ":agent_no", ":troop_no")])]],
["tab_shield_round_c", "Round_Shield", [("tableau_shield_round_2", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	315 , weight(3.5)|hit_points(540)|body_armor(4)|spd_rtng(87)|weapon_length(50), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_round_d", "Heavy Round_Shield", [("tableau_shield_round_1", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	414 , weight(4)|hit_points(600)|body_armor(6)|spd_rtng(84)|weapon_length(50), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_round_e", "Huscarl's Round_Shield", [("tableau_shield_round_4", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  
	506 , weight(4.5)|hit_points(690)|body_armor(8)|spd_rtng(81)|weapon_length(50), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_round_shield_4", ":agent_no", ":troop_no")])]],

["tab_shield_kite_a", "Old Kite Shield",   [("tableau_shield_kite_1" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	99 , weight(2)|hit_points(285)|body_armor(0)|spd_rtng(96)|weapon_length(60), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_kite_b", "Plain Kite Shield",   [("tableau_shield_kite_3" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	210 , weight(2.5)|hit_points(365)|body_armor(2)|spd_rtng(93)|weapon_length(60), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_3", ":agent_no", ":troop_no")])]],
["tab_shield_kite_c", "Kite Shield",   [("tableau_shield_kite_2" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	368 , weight(3)|hit_points(435)|body_armor(5)|spd_rtng(90)|weapon_length(60), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_kite_d", "Heavy Kite Shield",   [("tableau_shield_kite_2" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	469 , weight(3.5)|hit_points(515)|body_armor(8)|spd_rtng(87)|weapon_length(60), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_kite_cav_a", "Horseman's Kite Shield",   [("tableau_shield_kite_4" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	341 , weight(2)|hit_points(310)|body_armor(10)|spd_rtng(103)|weapon_length(40), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_4", ":agent_no", ":troop_no")])]],
["tab_shield_kite_cav_b", "Knightly Kite Shield",   [("tableau_shield_kite_4" , 0)], itp_merchandise|itp_type_shield, itcf_carry_kite_shield,  
	491 , weight(2.5)|hit_points(370)|body_armor(16)|spd_rtng(100)|weapon_length(40), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_kite_shield_4", ":agent_no", ":troop_no")])]],

["tab_shield_heater_a", "Old Heater Shield",   [("tableau_shield_heater_1" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	108 , weight(2)|hit_points(280)|body_armor(1)|spd_rtng(96)|weapon_length(60), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_heater_b", "Plain Heater Shield",   [("tableau_shield_heater_1" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	222 , weight(2.5)|hit_points(360)|body_armor(3)|spd_rtng(93)|weapon_length(60), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_heater_c", "Heater Shield",   [("tableau_shield_heater_1" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	390 , weight(3)|hit_points(430)|body_armor(6)|spd_rtng(90)|weapon_length(60), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_heater_d", "Heavy Heater Shield",   [("tableau_shield_heater_1" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	491 , weight(3.5)|hit_points(510)|body_armor(9)|spd_rtng(87)|weapon_length(60), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_heater_cav_a", "Horseman's Heater Shield",   [("tableau_shield_heater_2" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	377 , weight(2)|hit_points(300)|body_armor(12)|spd_rtng(103)|weapon_length(40), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heater_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_heater_cav_b", "Knightly Heater Shield",   [("tableau_shield_heater_2" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	529 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_heater_shield_2", ":agent_no", ":troop_no")])]],

["tab_shield_pavise_a", "Old Board Shield",   [("tableau_shield_pavise_2" , 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  
	180 , weight(3.5)|hit_points(510)|body_armor(0)|spd_rtng(89)|weapon_length(84), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_pavise_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_pavise_b", "Plain Board Shield",   [("tableau_shield_pavise_2" , 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  
	342 , weight(4)|hit_points(640)|body_armor(1)|spd_rtng(85)|weapon_length(84), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_pavise_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_pavise_c", "Board Shield",   [("tableau_shield_pavise_1" , 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  
	607 , weight(4.5)|hit_points(760)|body_armor(2)|spd_rtng(81)|weapon_length(84), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_pavise_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_pavise_d", "Heavy Board Shield",   [("tableau_shield_pavise_1" , 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  
	777 , weight(5)|hit_points(980)|body_armor(3)|spd_rtng(78)|weapon_length(84), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_pavise_shield_1", ":agent_no", ":troop_no")])]],

["tab_shield_small_round_a", "Plain Cavalry Shield", [("tableau_shield_small_round_3", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	208 , weight(2)|hit_points(310)|body_armor(3)|spd_rtng(105)|weapon_length(40), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_small_round_shield_3", ":agent_no", ":troop_no")])]],
["tab_shield_small_round_b", "Round Cavalry Shield", [("tableau_shield_small_round_1", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  
	346 , weight(2.5)|hit_points(370)|body_armor(9)|spd_rtng(103)|weapon_length(40), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_small_round_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_small_round_c", "Elite Cavalry Shield", [("tableau_shield_small_round_2", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  
	472 , weight(3)|hit_points(420)|body_armor(14)|spd_rtng(100)|weapon_length(40), imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"), (call_script, "script_shield_item_set_banner", "tableau_small_round_shield_2", ":agent_no", ":troop_no")])]],

["jomsviking_shield", "Ancient Shield", [("jomsviking_shield", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  
	654 , weight(3)|hit_points(600)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],


##############
#CIVILIZATION ITEMS  CIVILIZATION ITEMS  CIVILIZATION ITEMS  CIVILIZATION ITEMS  CIVILIZATION ITEMS  CIVILIZATION ITEMS  CIVILIZATION ITEMS  CIVILIZATION ITEMS  CIVILIZATION ITEMS  CIVILIZATION ITEMS
##############

#ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN ADENIAN
#Adenian Helmets
["bascinetnasal", "Bascinet with Nasal", [("bascinet_nasal", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	3423, weight(2.5)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["pigface", "Pigface", [("pigface", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4185, weight(2.25)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["pigfaceb", "Pigface", [("realbascinetd", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4460, weight(2.25)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["toadhelmet", "Knight Helmet", [("newhelmet", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	4185, weight(2.25)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],

#Adenian Shields
["shield_heater_generic_a", "Knightly Heater Shield",   [("shield_heater_generic_a" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	529, weight(2.5)|abundance(25)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],
["shield_heater_generic_c", "Knightly Heater Shield",   [("shield_heater_generic_c" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	529 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],
["shield_heater_generic_d", "Knightly Heater Shield",   [("shield_heater_generic_d" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	529 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],
["shield_heater_generic_g", "Knightly Heater Shield",   [("shield_heater_generic_g" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	529 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],
["shield_heater_generic_j", "Knightly Heater Shield",   [("shield_heater_generic_j" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	529 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],
["shield_heater_lionel", "Knightly Heater Shield",   [("shield_heater_lionel" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	529 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],
["shield_heater_normandy", "Knightly Heater Shield",   [("shield_heater_normandy" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	529 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],
["shield_kite_bors", "Knightly Heater Shield", [("shield_kite_2_bors" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	529 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],
["shield_heater_anklin", "Knightly Heater Shield",   [("shield_heater_anklin" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	529, weight(2.5)|abundance(25)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],


#ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN ANTARIAN
#Antarian Helmets
["anthelm1", "Salade with Coif", [("anthelm1", 0)], itp_merchandise|itp_type_head_armor, 0, 
	4185 , weight(2.25)|abundance(25)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],

#Antarian Armor
["antplate1", "Plate Armor", [("antplate1", 0)],  itp_merchandise|itp_type_body_armor|itp_covers_legs , 0,
	10245 , weight(25.5)|abundance(25)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(8) , imodbits_plate ],
["antplate2", "Plate Armor", [("antplate2", 0)],  itp_merchandise|itp_type_body_armor|itp_covers_legs , 0,
	11583 , weight(26)|abundance(25)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["antplate3", "Plate Armor", [("antplate3", 0)],  itp_merchandise|itp_type_body_armor|itp_covers_legs , 0,
	13251 , weight(27)|abundance(25)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["antplate4", "Plate Armor", [("antplate4", 0)],  itp_merchandise|itp_type_body_armor|itp_covers_legs , 0,
	13251 , weight(27)|abundance(25)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["antplate6", "Old Plate Armor", [("antplate6", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	9450 , weight(27)|abundance(75)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(9) , imodbits_plate ],
["ant_lthr_coat", "Heavy Studded Leather Coat", [("ant_lthr_coat", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	5708 , weight(17)|abundance(25)|head_armor(0)|body_armor(35)|leg_armor(11)|difficulty(7) , imodbits_cloth ],

#Antarian Gloves
["antgaunt2", "Gauntlets", [("antgaunt2_L", 0), ("gauntlet_b_L", imodbit_reinforced)], itp_merchandise|itp_type_hand_armor, 0, 
	648, weight(1)|abundance(25)|body_armor(6)|difficulty(0), imodbits_armor],

#Antarian Boots
["antboots2", "Iron Greaves", [("antboots2", 0)], itp_merchandise|itp_type_foot_armor|itp_attach_armature, 0,
	2062 , weight(3.5)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(33)|difficulty(9) , imodbits_armor ],

#Antarian Shields
["antshield", "Antarian Infantry Shield", [("antshield1" , 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback, itcf_carry_board_shield,
	630 , weight(4.5)|abundance(25)|hit_points(880)|body_armor(2)|spd_rtng(81)|weapon_length(84), imodbits_shield, ],
["antshield2", "Antarian Cavalry Shield", [("antshield2" , 0)], itp_merchandise|itp_type_shield, itcf_carry_kite_shield,
	642 , weight(4)|abundance(25)|hit_points(700)|body_armor(17)|spd_rtng(61)|weapon_length(40), imodbits_shield, ],

#Antarian Horses
["anthorse2", "Warhorse", [("anthorse2", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(15)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],

#Antarian Weapons
["ant_angon", "Antarian Angon", [("ant_angon", 0), ("ant_angon_quiver", ixmesh_carry)], itp_merchandise|itp_type_thrown |itp_primary|itp_bonus_against_shield , itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 
	1227 , weight(5)|difficulty(3)|spd_rtng(95) | shoot_speed(30) | thrust_damage(38 ,  pierce)|max_ammo(15)|weapon_length(65), imodbits_thrown ],


#LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION LEGION 
#Legion Helmets
["legion_helm_01", "Spangehelm", [("legion_helm_01", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3920 , weight(2.25)|abundance(25)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["legion_helm_02", "Emperor War Helmet", [("legion_helm_02", 0)], itp_type_head_armor, 0, 
	4240 , weight(2.5)|abundance(25)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate], #Cannot be purchased in stores
["legion_helm_03", "Legionnaire Akolouthos Helmet", [("legion_helm_03", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	4095 , weight(2.5)|abundance(25)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(8) , imodbits_plate ],
["legion_helm_04", "Legionnaire Helmet", [("legion_helm_04", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3011 , weight(2)|abundance(25)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["legion_helm_05", "Legionnaire Helmet", [("legion_helm_05", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3486 , weight(2.25)|abundance(25)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["legion_helm_06", "Leather_Mask", [("legion_helm_06", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2579, weight(2.5)|abundance(25)|head_armor(38)|difficulty(7), imodbits_cloth ],
["legion_helm_07", "Decorative_Mask", [("legion_helm_07", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2579, weight(2.5)|abundance(25)|head_armor(38)|difficulty(7), imodbits_armor ],
["legion_helm_08", "Legionnaire Helmet", [("legion_helm_08", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3243 , weight(2)|abundance(25)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["legion_helm_09", "Legionnaire Helmet", [("legion_helm_09", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3486 , weight(2)|abundance(25)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["legion_helm_10", "Legionnaire Hospitalier Helmet", [("legion_helm_10", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	4005 , weight(2.5)|abundance(10)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["legion_helm_11", "Legionnaire Helmet", [("legion_helm_11", 0)], itp_merchandise| itp_type_head_armor   , 0, 
	3011 , weight(2)|abundance(25)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["legion_helm_12", "Centurion Helmet", [("legion_helm_12", 0)], itp_type_head_armor, 0, 
	2240 , weight(2.25)|abundance(25)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate], #Cannot be purchased in stores
["iron_helm", "Iron_Helm", [("faceplate", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(3.25)|abundance(75)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],

#Legion Armors
["legion_armor_1", "Linothorax", [("legion_armor_1", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	3110 , weight(10)|abundance(25)|head_armor(0)|body_armor(30)|leg_armor(6)|difficulty(0), imodbits_cloth],
["legion_armor_2", "Leather Spolas", [("legion_armor_2", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	22106 , weight(20)|abundance(25)|head_armor(0)|body_armor(70)|leg_armor(24)|difficulty(10), imodbits_armor],
["legion_armor_3", "Cuirass", [("legion_armor_3", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	22106 , weight(24)|abundance(25)|head_armor(0)|body_armor(70)|leg_armor(24)|difficulty(10), imodbits_armor],
["legion_armor_4", "Bronze Cuirass", [("legion_armor_4", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	21213, weight(24)|abundance(25)|head_armor(0)|body_armor(68)|leg_armor(24)|difficulty(10) , imodbits_plate],
["legion_chiton_red", "Chilton", [("legion_chiton_red", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	194 , weight(1)|abundance(25)|head_armor(0)|body_armor(8)|leg_armor(1)|difficulty(0) , imodbits_cloth ],
["legion_chiton_half_red", "Half Chilton", [("legion_chiton_half_red", 0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs , 0,
	86 , weight(.5)|abundance(25)|head_armor(0)|body_armor(5)|leg_armor(1)|difficulty(0) , imodbits_cloth ],

#Legion Boots
["legion_greaves", "Bronze Greaves", [("legion_greaves", 0)], itp_merchandise|itp_type_foot_armor|itp_attach_armature, 0, 
	2062 , weight(3.5)|abundance(10)|head_armor(0)|body_armor(0)|leg_armor(33)|difficulty(9) , imodbits_armor ],

#Legion Shields
["legion_shield_1", "Brass Round Shield", [("legion_shield_1", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield, 
	629, weight(4)|abundance(5)|hit_points(650)|body_armor(15)|spd_rtng(68)|weapon_length(50), imodbits_shield],
["legion_shield_2", "Brass Pavise Shield", [("legion_shield_2", 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback, itcf_carry_board_shield, 
	1135, weight(5.5)|abundance(5)|hit_points(1000)|body_armor(16)|spd_rtng(65)|weapon_length(84), imodbits_shield],

#Legion Horses
["legion_horse_1", "Armored Hunter", [("legion_horse_1", 0)], itp_merchandise|itp_type_horse, 0, 
	2202, abundance(20)|hit_points(130)|body_armor(38)|difficulty(3)|horse_speed(38)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["legion_horse_2", "Armored Hunter", [("legion_horse_2", 0)], itp_merchandise|itp_type_horse, 0, 
	2202, abundance(20)|hit_points(130)|body_armor(38)|difficulty(3)|horse_speed(38)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["legion_horse_3", "Hunter", [("legion_horse_3", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(25)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["legion_horse_4", "Warhorse", [("legion_horse_4", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["legion_horse_5", "Charger", [("legion_horse_5", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["legion_horse_6", "Charger", [("legion_horse_6", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["legion_horse_7", "Charger", [("legion_horse_7", 0)], itp_merchandise|itp_type_horse, 0, 
	3444, abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25), imodbits_horse_basic|imodbit_champion],

#Legion Weapons
["legion_dagger", "Legionnaire Short Sword", [("legion_dagger", 0), ("legion_dagger_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 
	495 , weight(1)|abundance(15)|difficulty(0)|spd_rtng(115)|weapon_length(44)|swing_damage(22, cut) | thrust_damage(18, pierce), imodbits_sword_high ],
["legion_sword_centurion", "Centurion Sword", [("legion_sword_centurion", 0), ("legion_sword_centurion_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_always_loot|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	880 , weight(1.5)|abundance(5)|difficulty(0)|spd_rtng(110) | weapon_length(75)|swing_damage(30, cut) | thrust_damage(24,  pierce), imodbits_sword_high ],
["legion_sword_sica", "Sica", [("legion_sword_sica", 0), ("legion_sword_sica_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	729 , weight(1.5)|abundance(15)|difficulty(0)|spd_rtng(105) |weapon_length(90)|swing_damage(29, cut), imodbits_sword_high ],
["legion_sword_hoplite", "Legionnaire Sword", [("legion_sword_hoplite", 0), ("legion_sword_hoplite_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	752 , weight(1.5)|abundance(15)|difficulty(0)|spd_rtng(110)|weapon_length(60)|swing_damage(28, cut) | thrust_damage(22, pierce), imodbits_sword_high ],
["legion_sword_kopis", "Kopis", [("legion_sword_kopis", 0), ("legion_sword_kopis_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
	673 , weight(1.25)|abundance(15)|difficulty(0)|spd_rtng(110)|weapon_length(64)|swing_damage(26, cut) | thrust_damage(22,  pierce), imodbits_sword_high ],
["legion_spear_kamax", "Kamax", [("legion_spear_kamax", 0)], itp_merchandise|itp_warspear, itc_staff,
	720 , weight(3)|abundance(15)|difficulty(0)|spd_rtng(89)|weapon_length(231)|swing_damage(24, blunt) | thrust_damage(30,  pierce), imodbits_polearm ],
["legion_spear_palton", "Palton", [("legion_spear_palton", 0)], itp_merchandise|itp_warspear, itc_staff,
	270 , weight(2)|abundance(15)|difficulty(0)|spd_rtng(110)|weapon_length(119)|swing_damage(19, blunt) | thrust_damage(22,  pierce), imodbits_polearm ],
["legion_axe", "Legionnaire Axe", [("legion_axe", 0)], itp_merchandise|itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
	1289 , weight(1.5)|abundance(15)|difficulty(9)|spd_rtng(94) | weapon_length(70)|swing_damage(33 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],


#MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN MARINIAN
#Marinians Helmets
["marhelm1", "Segmented Helmet", [("marhelm1", 0)],  itp_merchandise|itp_type_head_armor, 0, 
	2579, weight(1.25)|abundance(25)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["marhelm2", "Guard Helmet", [("marhelm2", 0)],  itp_merchandise|itp_type_head_armor, 0, 
	3191, weight(2.5)|abundance(25)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["marhelm3", "Bascinet with Nasal", [("marhelm3", 0)], itp_merchandise|itp_type_head_armor, 0, 
	4275, weight(2.75)|abundance(25)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],

#Marinians Armor
["marchain1", "Mail Shirt", [("marchain1", 0)],  itp_merchandise|itp_type_body_armor|itp_covers_legs , 0, 
	7029, weight(19)|abundance(25)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(6) , imodbits_armor ],
["marchain2", "Light Mail and Plate", [("marchain2", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs   , 0, 
	11084, weight(12)|abundance(25)|head_armor(0)|body_armor(50)|leg_armor(16)|difficulty(7) , imodbits_armor ],
["marchain3", "Light Mail and Plate", [("marchain3", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs   , 0, 
	22106, weight(15)|abundance(25)|head_armor(0)|body_armor(70)|leg_armor(24)|difficulty(10) , imodbits_plate ],

#Marinians Gloves
["margloves2", "Gauntlets", [("margloves2_L", 0)], itp_type_hand_armor, 0, 
	2040, weight(1)|abundance(25)|body_armor(8)|difficulty(0), itp_merchandise|imodbits_armor],

#Marinians Boots
["marboots1", "Mail Boots", [("marboots1", 0)],  itp_merchandise|itp_type_foot_armor|itp_attach_armature  , 0,
	1825, weight(3)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(8) , imodbits_armor ],
["marboots3", "Iron Greaves", [("marboots3", 0)],  itp_merchandise|itp_type_foot_armor|itp_attach_armature  , 0,
	2390, weight(3.5)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(36)|difficulty(10) , imodbits_armor ],


#VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE VILLIANESE 
#Villianese Helmets
["villhelm1", "Villianese Helmet", [("vilhelm1", 0)],  itp_type_head_armor|itp_merchandise, 0, 
	2463 , weight(1.5)|abundance(15)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["villhelm2", "Villianese Chieftan Helmet", [("vilhelm2", 0)],  itp_type_head_armor|itp_merchandise, 0, 
	3423 , weight(2.5)|abundance(25)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["villhelm4", "Villianese High Chieftan Helmet", [("vilhelm4", 0)],  itp_type_head_armor|itp_merchandise, 0, 
	4185 , weight(2.75)|abundance(25)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) , imodbits_plate ],
["vilhelm5", "Villianese Hood", [("vilhelm5", 0)], itp_type_head_armor|itp_merchandise   , 0, 
	437 , weight(2)|abundance(25)|head_armor(18)|body_armor(0)|leg_armor(0) , imodbits_cloth ],

#Villianese Armor
["vilarmor_1", "Villianese Outfit", [("vilarmor_01", 0)], itp_merchandise| itp_type_body_armor |itp_covers_legs , 0,
	2306 , weight(7.25)|abundance(25)|head_armor(0)|body_armor(24)|leg_armor(7)|difficulty(0) , imodbits_cloth ],
["vilarmor_2", "Villianese Robe", [("vilarmor_02", 0)], 0| itp_merchandise|itp_type_body_armor |itp_covers_legs , 0, 
	2613 , weight(7.5)|abundance(25)|head_armor(0)|body_armor(25)|leg_armor(8)|difficulty(0) , imodbits_cloth ],
["vilarmor_3", "Villianese Padded Leather", [("vilarmor_03", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs, 0,
	3840 , weight(12)|abundance(25)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) , imodbits_cloth ],
["vilarmor_4", "Villianese Mail", [("vilarmor_04", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	5841 , weight(19)|abundance(25)|head_armor(0)|body_armor(35)|leg_armor(12)|difficulty(6) , imodbits_armor ],
["vilarmor_5", "Villianese Outfit", [("vilarmor_05", 0)], itp_merchandise| itp_type_body_armor |itp_covers_legs , 0,
	2306 , weight(7.25)|abundance(25)|head_armor(0)|body_armor(24)|leg_armor(7)|difficulty(0) , imodbits_cloth ],
["vilarmor_6", "Villianese Robe", [("vilarmor_06", 0)], 0| itp_merchandise|itp_type_body_armor |itp_covers_legs , 0, 
	2613 , weight(7.5)|abundance(25)|head_armor(0)|body_armor(25)|leg_armor(8)|difficulty(0) , imodbits_cloth ],
["vilarmor_7", "Villianese Padded Leather", [("vilarmor_07", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs, 0,
	3840 , weight(12)|abundance(25)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) , imodbits_cloth ],
["vilarmor_8", "Villianese Mail", [("vilarmor_08", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	5841 , weight(19)|abundance(25)|head_armor(0)|body_armor(35)|leg_armor(12)|difficulty(6) , imodbits_armor ],
["vilarmor_9", "Villianese Haubergeon", [("vilarmor_09", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0,
	4574 , weight(18)|abundance(25)|head_armor(0)|body_armor(35)|leg_armor(6)|difficulty(6) , imodbits_plate ],
["vilarmor_10", "Villianese Banded Armor", [("vilarmor_10", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	9164 , weight(23)|abundance(25)|head_armor(0)|body_armor(45)|leg_armor(14)|difficulty(9) , imodbits_armor ],
["vilarmor_11", "Villianese Chieftain Armor", [("vilarmor_11", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	10035 , weight(25)|abundance(25)|head_armor(0)|body_armor(46)|leg_armor(16)|difficulty(9) , imodbits_armor ],
["vilarmor_12", "Villianese Chieftain Armor", [("vilarmor_12", 0)],  itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	10035 , weight(25)|abundance(25)|head_armor(0)|body_armor(46)|leg_armor(16)|difficulty(9) , imodbits_armor ],

#Villianese Gloves
["villgloves1", "Mail_Mittens", [("vilgloves3_L", 0)], itp_type_hand_armor|itp_merchandise, 0, 
	288, weight(0.5)|abundance(25)|body_armor(4)|difficulty(0), imodbits_armor],
["villgloves2", "Mail_Mittens", [("vilgloves2_L", 0)], itp_type_hand_armor|itp_merchandise, 0, 
	450, weight(0.5)|abundance(10)|body_armor(5)|difficulty(0), imodbits_armor],

#Villianese Boots
["villboots1", "Villianese Boots", [("vilboots1", 0)],  itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	1777, weight(2.75)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(29)|difficulty(9) , imodbits_armor ],
["villboots2", "Villianese War Boots", [("vilboots2", 0)],  itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	1987, weight(3.25)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(32)|difficulty(9) , imodbits_armor ],

#Villianese Shields
["villshield", "Villianese Shield",  [("vilshield1" , 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
	222 , weight(2.5)|abundance(25)|hit_points(360)|body_armor(15)|spd_rtng(93)|weapon_length(60), imodbits_shield,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"), (store_trigger_param_2, ":troop_no"),
  (call_script, "script_shield_item_set_banner", "tableau_vilshield1", ":agent_no", ":troop_no")])]],

#Villianese Horse
["vilhorse1", "Warhorse", [("vilhorse1", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],


#ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN ZERRIKANIAN 
#Starting Equipment (there are other items used, but these are only assigned here)
["noble_spiked_helm", "Noble_Spiked_Helm", [("noble_spiked_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2790, weight(2.25)|abundance(25)|head_armor(40)|difficulty(7), imodbits_armor ],
["noble_start_boots", "Nobleman_Boots", [("noble_start_boots", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	459, weight(1.25)|abundance(25)|leg_armor(20), imodbits_cloth ],
["noble_charger", "Warhorse", [("noble_charger", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],

#Zerrikanian Peasant
["slave_neck_chain", "Slave_Neck_Chain", [("slave_neck_chain", 0)], itp_type_head_armor|itp_merchandise|itp_doesnt_cover_hair, 0, 
	5, weight(25)|abundance(25)|head_armor(1), imodbit_crude|imodbit_cracked|imodbit_rusty|imodbit_thick|imodbit_battered ],

#Zerrikanian Militia Items
["magyar_helmet_a", "Magyar Helmet", [("magyar_helmet_a", 0)], itp_merchandise|itp_type_head_armor, 0, 
	1215, weight(2)|abundance(25)|head_armor(30)|body_armor(0)|leg_armor(0) , imodbits_cloth ],

#Zerrikanian Axemen Items
["helm_rajput_c", "Rajput", [("helm_rajput_c", 0)], itp_merchandise|itp_type_head_armor, 0, 
	1560, weight(2)|abundance(25)|head_armor(34), imodbits_cloth ],
["rabati", "Rabati", [("brown_rabati", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	1653 , weight(2)|abundance(25)|head_armor(35)|body_armor(0)|leg_armor(0) , imodbits_cloth ],

#Zerrikanian Hardened Axemen Items
["zerk_red_helm", "Spiked_Helm", [("zerk_red_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3011, weight(2)|abundance(25)|head_armor(42)|difficulty(7), imodbits_armor ],
["zerk_redmask", "Zerrikanian_Mask", [("zerk_redmask", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(2.75)|abundance(25)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],
["zerk_red_armor", "Leather_over_Mail", [("zerk_red_armor", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8073, weight(18.25)|abundance(25)|body_armor(42)|leg_armor(16), imodbits_armor ],
["zerk_red_boot", "Mail_Chausses", [("zerk_red_boot", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	459, weight(2.25)|abundance(25)|leg_armor(20), imodbits_armor ],

#Zerrikanian Short Bowman Items
["sipahi_helmet_b", "Sipahi_Helmet", [("sipahi_helmet_b", 0)], itp_merchandise| itp_type_head_armor, 0, 
	540, weight(2)|abundance(25)|head_armor(20), imodbits_cloth ],

#Zerrikanian Dvor Archer Items
["dvor_archer_mask1", "Dvor_Archer_Mask", [("dvor_archer_mask1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2160, weight(2.5)|abundance(25)|head_armor(40), imodbits_armor ],
["dvor_archer_helm_1", "Dvor_Archer_Helm", [("dvor_archer_helm_1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	1382, weight(1.5)|abundance(25)|head_armor(32), imodbits_cloth ],
["dvor_archer_helm_2", "Dvor_Archer_Helm", [("dvor_archer_helm_2", 0)], itp_type_head_armor|itp_merchandise, 0, 
	1749, weight(1.75)|abundance(25)|head_armor(36), imodbits_armor ],
["dvor_archer_armor", "Dvor_Archer_Armor", [("dvor_archer_armor", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	4437, weight(12.5)|abundance(25)|body_armor(35)|leg_armor(8), imodbits_cloth|imodbit_crude|imodbit_rusty|imodbit_battered ],
["dvor_archer_boot", "Dvor_Archer_Boots", [("dvor_archer_boot", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	372, weight(1)|abundance(25)|leg_armor(18), imodbits_cloth ],

#Zerrikanian Scout Items
["cossack_helm", "Lamellar_Helm", [("cossack_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2012, weight(1.5)|abundance(25)|head_armor(32)|difficulty(7), imodbits_cloth ],
["cossack_armor", "Padded_Leather_Armor", [("cossack_armor", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	3840, weight(12)|abundance(25)|body_armor(30)|leg_armor(10), imodbits_armor|imodbit_cracked ],
["straw_shield", "Straw_Shield", [("cossack_straw_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
	195, weight(1.5)|abundance(25)|body_armor(1)|hit_points(200)|spd_rtng(96)|weapon_length(60), imodbits_shield ],
["rok_saddle_horse1", "Saddle_Horse", [("rok_saddle_horse1", 0)], itp_type_horse|itp_merchandise, 0, 
	336, abundance(90)|body_armor(14)|difficulty(1)|horse_maneuver(36)|horse_speed(39)|horse_charge(8), imodbits_horse_basic],

#Zerrikanian Mounted Archer Items
["bashkir_helm1", "Horned_Decorated_Helmet", [("bashkir_helm1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3486, weight(3)|abundance(25)|head_armor(46)|difficulty(7), imodbits_armor|imodbit_cracked ],
["bashkir_helm2", "Decorated_Helmet", [("bashkir_helm2", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3363, weight(3)|abundance(25)|head_armor(45)|difficulty(7), imodbits_armor|imodbit_cracked ],
["bashkir_helm3", "Lamellar_Helmet", [("bashkir_helm3", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3363, weight(3)|abundance(25)|head_armor(45)|difficulty(7), imodbits_armor|imodbit_cracked ],
["bashkir_armor", "Lamellar_Armor", [("bashkir_armor", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8883, weight(25)|abundance(25)|body_armor(45)|leg_armor(13)|difficulty(9), imodbits_armor ],
["bashkir_boots", "Lamellar_Boots", [("bashkir_boots", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	459, weight(1.25)|abundance(25)|leg_armor(20), imodbits_cloth ],
["bashkir_shield", "Decorative_Shield", [("bashkir_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
	566, weight(3)|abundance(15)|body_armor(4)|hit_points(580)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["rok_bashkir_hunter", "Hunter", [("rok_bashkir_hunter", 0)], itp_type_horse|itp_merchandise, 0, 
	1302, abundance(25)|body_armor(29)|difficulty(3)|hit_points(130)|horse_maneuver(36)|horse_speed(40)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["rok_bashkir_courser", "Courser", [("rok_bashkir_courser", 0)], itp_type_horse|itp_merchandise, 0, 
	969, abundance(25)|body_armor(16)|difficulty(2)|hit_points(100)|horse_maneuver(37)|horse_speed(43)|horse_charge(11), imodbits_horse_basic|imodbit_champion],

#Zerrikanian Harvester Items
["white_mask", "Zerrikanian_Mask", [("white_mask", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(2.75)|abundance(25)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],
["white_helm", "Lamellar_Helmet", [("white_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2160, weight(1.5)|abundance(25)|head_armor(40), imodbits_cloth ],
["white_armor", "White_Armor", [("white_armor", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	7526, weight(18)|abundance(25)|body_armor(40)|leg_armor(16), imodbits_cloth|imodbit_crude|imodbit_rusty|imodbit_battered ],
["white_boots", "White_Boots", [("white_boots", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	459, weight(1.25)|abundance(25)|leg_armor(20), imodbits_cloth ],
["rok_kalmuck_horse", "Hunter", [("rok_kalmuck_horse", 0)], itp_type_horse|itp_merchandise, 0, 
	1602, abundance(25)|body_armor(29)|difficulty(3)|hit_points(130)|horse_maneuver(36)|horse_speed(40)|horse_charge(18), imodbits_horse_basic|imodbit_champion],

#Zerrikanian Reaper Items
["oprichnik_mask1", "Zerrikanian_Mask", [("oprichnik_mask1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(2.75)|abundance(25)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],
["oprichnik_mask2", "Zerrikanian_Mask", [("oprichnik_mask2", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(2.75)|abundance(25)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],
["oprichnik_helm", "Lamellar_Helmet", [("oprichnik_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2613, weight(2.5)|abundance(25)|head_armor(44), imodbits_cloth ],
["oprichnik_armor", "Lamellar_Armor", [("oprichnik_armor", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8883, weight(25)|abundance(25)|body_armor(45)|leg_armor(13)|difficulty(9), imodbits_armor ],
["oprichnik_boots", "Lamellar_Boots", [("oprichnik_boots", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	718, weight(3)|abundance(25)|leg_armor(25), imodbits_cloth ],
["rok_oprichnik_charger", "Charger", [("rok_oprichnik_charger", 0)], itp_type_horse|itp_merchandise, 0, 
	4117, abundance(10)|body_armor(65)|difficulty(4)|hit_points(140)|horse_maneuver(33)|horse_speed(36)|horse_charge(30), imodbits_horse_basic|imodbit_champion],

#Zerrikanian Boyar Son Items
["zerrikanian_noble_helmet", "Noble_Helmet", [("boyar_son_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	1215, weight(1.75)|abundance(25)|head_armor(30), imodbits_cloth ],
["boyar_son_armor1", "Nobleman_Padded_Leather", [("boyar_son_armor1", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	5078, weight(13)|abundance(25)|body_armor(34)|leg_armor(12), imodbits_cloth ],
["noble_padded_leather", "Nobleman_Padded_Leather", [("noble_padded_leather", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	5078, weight(13)|abundance(25)|body_armor(34)|leg_armor(12), imodbits_cloth ],
["dynasty_tabard", "Nobleman_Padded_Leather", [("dynasty_tabard", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	5078, weight(13)|abundance(25)|body_armor(34)|leg_armor(12), imodbits_cloth ],
["rok_boyar_son_warhorse", "Warhorse", [("rok_boyar_son_warhorse", 0)], itp_type_horse|itp_merchandise, 0, 
	2574, abundance(25)|body_armor(52)|difficulty(4)|hit_points(135)|horse_maneuver(34)|horse_speed(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["decor_aqua_shield", "Decorative_Shield", [("decor_aqua_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["decor_bluegreen_shield", "Decorative_Shield", [("decor_bluegreen_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["decor_redblue_shield", "Decorative_Shield", [("decor_redblue_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["decor_red1_shield", "Decorative_Shield", [("decor_red1_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["decor_red2_shield", "Decorative_Shield", [("decor_red2_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["decor_colors1_shield", "Decorative_Shield", [("decor_colors1_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["decor_colors2_shield", "Decorative_Shield", [("decor_colors2_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["decor_colors3_shield", "Decorative_Shield", [("decor_colors3_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],

#Zerrikanian Boyar Items
["boyar_helm", "Boyar_Helm", [("boyar_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4280, weight(2.25)|abundance(25)|head_armor(52)|difficulty(7), imodbits_armor|imodbit_cracked ],
["boyar_armor1", "Lamellar_Armor", [("boyar_armor1", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	9164, weight(25)|abundance(25)|body_armor(46)|leg_armor(13)|difficulty(9), imodbits_armor ],
["boyar_armor2", "Padded_Mail", [("boyar_armor2", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8793, weight(22)|abundance(25)|body_armor(46)|leg_armor(12)|difficulty(8), imodbits_cloth ],
["boyar_shield", "Decorative_Shield", [("boyar_shield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	208, weight(2)|abundance(25)|body_armor(3)|hit_points(310)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["rok_boyar_warhorse", "Warhorse", [("rok_boyar_warhorse", 0)], itp_type_horse|itp_merchandise, 0, 
	2574, abundance(25)|body_armor(52)|difficulty(4)|hit_points(135)|horse_maneuver(34)|horse_speed(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["rok_boyar_charger", "Charger", [("rok_boyar_charger", 0)], itp_type_horse|itp_merchandise, 0, 
	3444, abundance(25)|body_armor(65)|difficulty(4)|hit_points(140)|horse_maneuver(32)|horse_speed(35)|horse_charge(25), imodbits_horse_basic|imodbit_champion],

#Zerrikanian Dvor Items
["dvor1_mask", "Zerrikanian_Mask", [("dvor1_mask", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4005, weight(2.75)|abundance(25)|head_armor(50)|difficulty(7), imodbits_armor|imodbit_cracked ],
["dvor2_mask", "Zerrikanian_Mask", [("dvor2_mask", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4005, weight(2.75)|abundance(25)|head_armor(50)|difficulty(7), imodbits_armor|imodbit_cracked ],
["dvor_lamellar1", "Lamellar_Armor", [("dvor_lamellar1", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	9164, weight(25)|abundance(25)|body_armor(46)|leg_armor(13)|difficulty(9), imodbits_armor ],
["dvor_lamellar2", "Lamellar_Armor", [("dvor_lamellar2", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	9164, weight(25)|abundance(25)|body_armor(46)|leg_armor(13)|difficulty(9), imodbits_armor ],
["rok_dvor1_charger", "Charger", [("rok_dvor1_charger", 0)], itp_type_horse|itp_merchandise, 0, 
	3444, abundance(25)|body_armor(65)|difficulty(4)|hit_points(140)|horse_maneuver(32)|horse_speed(35)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["rok_dvor2_charger", "Charger", [("rok_dvor2_charger", 0)], itp_type_horse|itp_merchandise, 0, 
	3444, abundance(25)|body_armor(65)|difficulty(4)|hit_points(140)|horse_maneuver(32)|horse_speed(35)|horse_charge(25), imodbits_horse_basic|imodbit_champion],
["rok_dvor3_charger", "Charger", [("rok_dvor3_charger", 0)], itp_type_horse|itp_merchandise, 0, 
	3444, abundance(25)|body_armor(65)|difficulty(4)|hit_points(140)|horse_maneuver(32)|horse_speed(35)|horse_charge(25), imodbits_horse_basic|imodbit_champion],


##############
#ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS  ROYAL ITEMS
#None of these items can be purchased in the shops
##############
#ADENIAN
["blacksmith_adenian_armor", "Champion Adenian Plate", [("blacksmith_adenian_armor", 0)],  itp_type_body_armor|itp_covers_legs , 0,
	1 , weight(25)|abundance(0)|head_armor(0)|body_armor(62)|leg_armor(24)|difficulty(15) , 0 ],
["blacksmith_adenian_boots", "Champion Adenian Greaves", [("blacksmith_adenian_boots", 0)],  itp_type_foot_armor|itp_attach_armature, 0,
	1 , weight(3)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(40)|difficulty(15) , 0 ],
["blacksmith_adenian_crown", "Adenian Knightly Crown", [("blacksmith_adenian_crown", 0)], itp_type_head_armor|itp_fit_to_head, 0,
	1 , weight(2.75)|abundance(0)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(15) , 0 ],
["blacksmith_adenian_horse", "Avalanche of Aden", [("blacksmith_adenian_horse", 0)], itp_type_horse, 0, 
	1, abundance(0)|body_armor(75)|difficulty(5)|hit_points(150)|horse_maneuver(31)|horse_speed(36)|horse_charge(40), 0 ],
["blacksmith_adenian_lance", "Adenian Dragonlance", [("blacksmith_adenian_lance", 0)], itp_greatlance, itc_greatlance,
	1, weight(6)|abundance(0)|difficulty(15)|spd_rtng(70)|weapon_length(540)|swing_damage(0, cut)|thrust_damage(40, pierce), 0 ],
["blacksmith_adenian_shield", "Adenian Phoenix Shield", [("blacksmith_adenian_shield", 0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	1, weight(3.5)|abundance(0)|body_armor(20)|hit_points(500)|spd_rtng(100)|weapon_length(55), imodbits_shield ],

#ANTARIAN:
["blacksmith_antarian_armor", "Antarian Behemoth Armor", [("blacksmith_antarian_armor", 0)],  itp_type_body_armor|itp_covers_legs , 0,
	1 , weight(25)|abundance(0)|head_armor(0)|body_armor(62)|leg_armor(24)|difficulty(15) , 0 ],
["blacksmith_antarian_boots", "Antarian Avenger Greaves", [("blacksmith_antarian_boots", 0)],  itp_type_foot_armor|itp_attach_armature, 0,
	1 , weight(3)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(40)|difficulty(15) , 0 ],
["blacksmith_antarian_crown", "Antarian Reunited Crown", [("blacksmith_antarian_crown", 0)], itp_type_head_armor|itp_fit_to_head, 0,
	1 , weight(2.75)|abundance(0)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(15) , 0 ],
["blacksmith_antarian_gauntlets", "Antarian Avenger Gauntlets", [("blacksmith_antarian_gauntlets_L", 0)], itp_type_hand_armor, 0, 
	1, weight(1)|abundance(0)|body_armor(12)|difficulty(0), 0],
["blacksmith_antarian_sword",  "Antarian Behemoth Sword", [("blacksmith_antarian_sword", 0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back,
	1 , weight(3.25)|abundance(0)|difficulty(15)|spd_rtng(85) | weapon_length(145)|swing_damage(48 , cut) | thrust_damage(36 ,  pierce), 0],
["blacksmith_antarian_angon", "Shafts of the Antarian Titan", [("blacksmith_antarian_angon", 0), ("blacksmith_antarian_angon_quiver", ixmesh_carry)], itp_type_thrown |itp_primary|itp_bonus_against_shield, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 
	1 , weight(5)|difficulty(3)|spd_rtng(97) | shoot_speed(30) | thrust_damage(46 ,  pierce)|max_ammo(20)|weapon_length(65), imodbits_thrown ],

#MARINIAN:
["blacksmith_marinian_armor", "Marinian Feather Armor", [("blacksmith_marinian_armor", 0)],  itp_type_body_armor|itp_covers_legs , 0,
	1 , weight(25)|abundance(0)|head_armor(0)|body_armor(62)|leg_armor(24)|difficulty(15) , 0 ],
["blacksmith_marinian_boots", "Marinian Glorious Marching Greaves", [("blacksmith_marinian_boots", 0)],  itp_type_foot_armor|itp_attach_armature, 0,
	1 , weight(1.25)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(38)|difficulty(15) , 0 ],
["blacksmith_marinian_crown", "Marinian Lord Protector Crown", [("blacksmith_marinian_crown", 0)], itp_type_head_armor|itp_fit_to_head|itp_covers_head, 0,
	1 , weight(2.75)|abundance(0)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(15) , 0 ],
["blacksmith_marinian_bolt", "One-Life Marinian Bolts", [("blacksmith_marinian_bolt", 0), ("flying_missile", ixmesh_flying_ammo), ("blacksmith_marinian_bolt_bag", ixmesh_carry)], itp_type_bolts, itcf_carry_quiver_right_vertical, 
	1, weight(2.5)|abundance(0)|weapon_length(55)|thrust_damage(10, pierce)|max_ammo(50), 0],
["blacksmith_marinian_crossbow", "Marinian Widowmaker", [("blacksmith_marinian_crossbow", 0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_use_on_horseback , itcf_shoot_crossbow|itcf_carry_crossbow_back, 
	1 , weight(3.75)|abundance(0)|difficulty(10)|spd_rtng(50) | shoot_speed(120) | thrust_damage(72 , pierce)|max_ammo(1), 0 ],
["blacksmith_marinian_glaive", "Marinian Giantslayer", [("blacksmith_marinian_glaive", 0)], itp_warspear|itp_two_handed, itc_staff,
	1, weight(4.5)|abundance(0)|difficulty(15)|spd_rtng(99)|weapon_length(240)|swing_damage(50, cut)|thrust_damage(30, pierce), 0 ],

#VILLIANESE:
["blacksmith_villianese_armor", "Villianese Silvery Cloud Armor", [("blacksmith_villianese_armor", 0)],  itp_type_body_armor|itp_covers_legs , 0,
	1 , weight(25)|abundance(0)|head_armor(0)|body_armor(62)|leg_armor(24)|difficulty(15) , 0 ],
["blacksmith_villianese_crown", "Villianese Golden Peak Crown", [("blacksmith_villianese_crown", 0)], itp_type_head_armor|itp_fit_to_head, 0,
	1 , weight(2.75)|abundance(0)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(15) , 0 ],
["blacksmith_villianese_arrow", "Mountain Heart Villianese Arrows", [("blacksmith_villianese_arrow", 0), ("flying_missile", ixmesh_flying_ammo), ("blacksmith_villianese_quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back_right, 
	1, weight(3)|abundance(0)|weapon_length(95)|thrust_damage(5, pierce)|max_ammo(50), 0],
["blacksmith_villianese_bow", "Villianese Rock Crusher", [("blacksmith_villianese_bow", 0), ("blacksmith_villianese_bow_carry", ixmesh_carry)], itp_type_bow|itp_primary|itp_two_handed , itcf_shoot_bow|itcf_carry_bow_back, 
	1 , weight(1)|abundance(0)|difficulty(6)|spd_rtng(110) | shoot_speed(65) | thrust_damage(30 , pierce), 0 ],
["blacksmith_villianese_scimitar", "Villianese Cliffcarver", [("blacksmith_villianese_scimitar", 0, 0), ("blacksmith_villianese_scab_scimeter", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itcf_carry_sword_left_hip|itc_scimitar|itcf_show_holster_when_drawn, 
	1, weight(1.5)|abundance(0)|spd_rtng(105)|weapon_length(98)|swing_damage(33, cut), 0 ],
["blacksmith_villianese_shield", "Villianese Ancestral Ore Shield", [("blacksmith_villianese_shield", 0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	1, weight(3)|abundance(0)|body_armor(18)|hit_points(500)|spd_rtng(110)|weapon_length(45), imodbits_shield ],

#ZERRIKANIAN
["blacksmith_zerrikanian_armor", "Zerrikanian Grand Ruler Armor", [("blacksmith_zerrikanian_armor", 0)],  itp_type_body_armor|itp_covers_legs , 0,
	1 , weight(25)|abundance(0)|head_armor(0)|body_armor(62)|leg_armor(24)|difficulty(15) , 0 ],
["blacksmith_zerrikanian_crown", "Zerrikanian Grand Ruler Crown", [("blacksmith_zerrikanian_crown", 0)], itp_type_head_armor|itp_fit_to_head, 0,
	1 , weight(2.75)|abundance(0)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(15) , 0 ],
["blacksmith_zerrikanian_jarid", "Steelpiercer Zerrikanian Javelins", [("blacksmith_zerrikanian_jarid", 0, 0), ("blacksmith_zerrikanian_jarid_quiver", ixmesh_carry)], itp_type_thrown|itp_bonus_against_shield|itp_primary, itcf_carry_quiver_back|itcf_throw_javelin|itcf_show_holster_when_drawn, 
	1, weight(4.5)|abundance(0)|difficulty(2)|spd_rtng(90)|shoot_speed(30)|weapon_length(65)|max_ammo(20)|thrust_damage(45, pierce), 0 ],
["blacksmith_zerrikanian_scepter", "Zerrikanian Rule Maker", [("blacksmith_zerrikanian_scepter", 0)], itp_type_two_handed_wpn|itp_penalty_with_shield|itp_wooden_parry|itp_primary, itcf_carry_spear|itc_nodachi|itcf_thrust_onehanded|itcf_overswing_onehanded|itcf_slashright_onehanded|itcf_thrust_twohanded|itcf_slashleft_onehanded, 
	1, weight(4.5)|abundance(0)|difficulty(12)|spd_rtng(70)|weapon_length(117)|thrust_damage(25, pierce)|swing_damage(34, blunt), 0 ],
["blacksmith_zerrikanian_horse", "Golden Wind of Zerrikania", [("blacksmith_zerrikanian_horse", 0)], itp_type_horse, 0, 
	1, abundance(0)|hit_points(140)|body_armor(65)|difficulty(5)|horse_speed(38)|horse_maneuver(34)|horse_charge(26), 0],
["blacksmith_zerrikanian_bow", "Zerrikanian Blood Debt", [("blacksmith_zerrikanian_bow", 0), ("blacksmith_zerrikanian_bow_case", ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 
	1 , weight(1)|difficulty(6)|spd_rtng(115) | shoot_speed(66) | thrust_damage(27 , pierce), imodbits_bow ],


##############
#ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  ITEM SETS  
##############

#Dull Set
["dullboots", "Dull Greaves", [("dullboots", 0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature, 0, 
	2062 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(33)|difficulty(9) , imodbits_armor ],
["dullgauntlets", "Dull Gauntlets", [("dullgauntlet_a_L", 0), ("dullgauntlet_b_L", imodbit_reinforced)], itp_merchandise|itp_type_hand_armor, 0, 
	648, weight(1)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor],
["dullplate", "Dull Plate Armor", [("dullplate", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0, 
	14310, weight(27)|abundance(100)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["dullhelm", "Dull Helm", [("dullhelm", 0)], itp_merchandise| itp_type_head_armor| itp_fit_to_head, 0, 
	4983 , weight(2.75)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],

#Eagle Set
["eagleplate", "Eagle Plate Armor", [("eagleplate", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs , 0, 
	13251, weight(27)|abundance(20)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_plate],
["eagleboots", "Eagle Armor Greaves", [("eagleboots", 0)], itp_merchandise| itp_type_foot_armor|itp_attach_armature, 0, 
	1882, weight(3.5)|abundance(20)|head_armor(0)|body_armor(0)|leg_armor(33)|difficulty(7), imodbits_armor],
["eaglehelm", "Eagle Armor Helm", [("eaglehelm", 0)], itp_merchandise|itp_type_head_armor|itp_fit_to_head, 0, 
	3363, weight(3)|abundance(20)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate],
["eaglegauntlets", "Eagle Armor Gauntlets", [("eaglegauntlet_a_L", 0)], itp_merchandise|itp_type_hand_armor, 0, 
	648, weight(1)|abundance(20)|body_armor(6)|difficulty(0), imodbits_armor],

#Brass Set
["brassarmor", "Brass Armor", [("brassarmor", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0, 
	14310 , weight(27)|abundance(100)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["brasshelm", "Brass Helm", [("brasshelm", 0)], itp_merchandise| itp_type_head_armor|itp_covers_head, 0, 
	4983 , weight(2.75)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],
["brassboots", "Brass Greaves", [("brassboots", 0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature, 0, 
	2062 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(33)|difficulty(9) , imodbits_armor ],
["brassgauntlets", "Brass Gauntlets", [("brassgauntlet_a_L", 0), ("brassgauntlet_b_L", imodbit_reinforced)], itp_merchandise|itp_type_hand_armor, 0, 
	648, weight(1)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor],

#Jester Items
["jester_tunic", "Jester_Tunic", [("jester_tunic", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	1161, weight(2)|abundance(25)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth],
["jester_hat_large", "Jester_Hat", [("jester_hat_large", 0)], itp_merchandise| itp_type_head_armor|itp_civilian|itp_fit_to_head, 0, 
	86, weight(0.5)|abundance(25)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth],
["jester_hat_small", "Jester_Hat", [("jester_hat_small", 0)], itp_type_head_armor|itp_civilian|itp_fit_to_head, 0, 
	70, weight(0.5)|abundance(0)|head_armor(99)|body_armor(99)|leg_armor(99)|difficulty(0), imodbits_cloth],
["jester_gloves", "Jester_Gloves", [("jester_glove_L", 0)], itp_merchandise|itp_type_hand_armor, 0, 
	72, weight(0.25)|abundance(25)|body_armor(2)|difficulty(0), imodbits_cloth],
["jester_boot", "Jester_Boots", [("jester_boot", 0)], itp_merchandise|itp_type_foot_armor|itp_civilian|itp_attach_armature, 0,
	294 , weight(1.25)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(16)|difficulty(0), imodbits_cloth],

#Pilgrim Set
["pilgrim_disguise", "Pilgrim Disguise", [("cyc_pilgrim_outfit", 0)], 0| itp_merchandise|itp_type_body_armor |itp_covers_legs |itp_civilian , 0, 
	1749 , weight(2)|abundance(10)|head_armor(0)|body_armor(19)|leg_armor(8)|difficulty(0) , imodbits_cloth ],
["pilgrim_hood", "Pilgrim Hood", [("pilgrim_hood", 0)], 0| itp_merchandise|itp_type_head_armor |itp_civilian  , 0, 
	264 , weight(1.25)|abundance(10)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],

#Strange Item Set (Samurai)
["strange_helmet", "Ronin Helmet", [("cyc_samurai_helmet", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	3243, weight(2)|abundance(5)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["strange_armor",  "Ronin Armor", [("cyc_samurai_armor", 0)], itp_merchandise|itp_type_body_armor  |itp_covers_legs , 0, 
	12200, weight(19)|abundance(5)|head_armor(0)|body_armor(50)|leg_armor(22)|difficulty(9) , imodbits_armor ],
["strange_boots",  "Ronin Boots", [("cyc_samurai_boots", 0)], itp_merchandise|itp_type_foot_armor | itp_attach_armature, 0, 
	507, weight(1)|abundance(5)|head_armor(0)|body_armor(0)|leg_armor(21)|difficulty(0) , imodbits_cloth ],
["strange_sword", "Katana", [("cyc_katana", 0), ("katana_scabbard", ixmesh_carry)], itp_merchandise|itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_katana|itcf_show_holster_when_drawn, 
	1559, weight(2)|abundance(5)|difficulty(9)|spd_rtng(108) | weapon_length(95)|swing_damage(32 , cut) | thrust_damage(18 ,  pierce), imodbits_sword ],
["strange_great_sword",  "Nodachi", [("cyc_no_dachi", 0), ("no_dachi_scabbard", ixmesh_carry)], itp_merchandise|itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back|itcf_show_holster_when_drawn, 
	1819, weight(3.5)|abundance(5)|difficulty(11)|spd_rtng(92) | weapon_length(125)|swing_damage(38 , cut) | thrust_damage(0 ,  pierce), imodbits_axe ],
["strange_short_sword", "Wakizashi", [("cyc_wakizashi", 0), ("wakizashi_scabbard", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn, 
	635, weight(1.25)|abundance(5)|difficulty(0)|spd_rtng(108) | weapon_length(65)|swing_damage(25 , cut) | thrust_damage(19 ,  pierce), imodbits_sword ],


##############
#MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS  MERCENARY GUILD ITEMS
##############

#BLACK ARMY MERCENARY GUILD ITEMS
#Black Army Helmets
["black_army_helm_1", "Nasal Helmet", [("black_army_helm_1", 0)], itp_merchandise|itp_type_head_armor, 0, 
	1845 , weight(1.25)|abundance(25)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["black_army_helm_2", "Nasal Helmet with Coif", [("black_army_helm_2", 0)], itp_merchandise|itp_type_head_armor, 0, 
	2283 , weight(2.25)|abundance(25)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["black_army_helm_3", "Nasal Helmet with Coif", [("black_army_helm_3", 0)], itp_merchandise|itp_type_head_armor, 0, 
	3011 , weight(2.25)|abundance(25)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["black_army_helm_4", "Dark Helmet", [("black_army_helm_4", 0)], itp_merchandise|itp_type_head_armor, 0, 
	3486 , weight(2.25)|abundance(25)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["black_army_helm_5", "Dark Helmet", [("black_army_helm_5", 0)], itp_merchandise|itp_type_head_armor, 0, 
	3740 , weight(2.25)|abundance(25)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(7) , imodbits_plate ],
["black_general_helm", "Dark_General_Helm", [("black_general_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4983, weight(2.75)|abundance(10)|head_armor(55)|difficulty(10), imodbits_armor|imodbit_cracked ],

#Black Army Armor
["black_army_armor_1", "Padded Leather", [("black_army_armor_1", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian, 0,
	3840 , weight(12)|abundance(25)|body_armor(30)|leg_armor(10)|difficulty(0) , imodbits_cloth ],
["black_army_armor_2", "Studded Padded Leather", [("black_army_armor_2", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian, 0,
	5078 , weight(16)|abundance(25)|body_armor(34)|leg_armor(12)|difficulty(0) , imodbits_cloth ],
["black_army_armor_3", "Plate_Armor", [("black_army_armor_3", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	11264, weight(25)|abundance(25)|body_armor(50)|leg_armor(16)|difficulty(9), imodbits_armor|imodbit_cracked ],
["black_army_armor_4", "Plate_Armor", [("black_army_armor_4", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	11264, weight(25)|abundance(25)|body_armor(50)|leg_armor(16)|difficulty(9), imodbits_armor|imodbit_cracked ],
["black_army_armor_5", "Breast_Plate_with_Mail", [("black_army_armor_5", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8517, weight(24)|abundance(25)|body_armor(45)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],
["black_army_armor_6", "Breast_Plate_with_Mail", [("black_army_armor_6", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8517, weight(24)|abundance(25)|body_armor(45)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],
["black_army_armor_7", "Breast_Plate_with_Mail", [("black_army_armor_7", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8517, weight(24)|abundance(25)|body_armor(45)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],
["black_armor", "Black Armor", [("cyc_black_armor", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs , 0,
	13251 , weight(27)|abundance(25)|body_armor(55)|leg_armor(17)|difficulty(9) , imodbits_plate ],
["black_general_armor", "Dark_General_Armor", [("black_general_armor", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	15591, weight(30)|abundance(10)|body_armor(60)|leg_armor(18)|difficulty(11), imodbits_armor|imodbit_cracked ],

#Black Army Gloves
["black_army_leather_gloves", "Black Leather Gloves", [("black_army_lthr_glove_L", 0)], itp_merchandise|itp_type_hand_armor, 0, 
	72, weight(0.25)|abundance(25)|body_armor(2)|difficulty(0), imodbits_cloth],

#Black Army Boots
["black_army_boot_1", "Black Leather Boots", [("black_army_boot_1", 0)], itp_merchandise|itp_type_foot_armor|itp_civilian|itp_attach_armature, 0,
	294 , weight(1.25)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(16)|difficulty(0), imodbits_cloth],

#Black Army Shields
["black_army_shield_1", "Old Kite Shield", [("black_army_shield_1" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	99, weight(2)|abundance(25)|hit_points(285)|body_armor(0)|spd_rtng(96)|weapon_length(60), imodbits_shield],
["black_army_shield_2", "Plain Kite Shield", [("black_army_shield_2" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	210, weight(2.5)|abundance(25)|hit_points(365)|body_armor(2)|spd_rtng(93)|weapon_length(60), imodbits_shield],
["black_army_shield_3", "Old Board Shield", [("black_army_shield_3" , 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  
	180, weight(3.5)|abundance(25)|hit_points(510)|body_armor(0)|spd_rtng(89)|weapon_length(84), imodbits_shield],
["black_army_shield_4", "Board Shield", [("black_army_shield_4" , 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  
	607, weight(4.5)|abundance(25)|hit_points(760)|body_armor(2)|spd_rtng(81)|weapon_length(84), imodbits_shield],
["black_army_shield_5", "Heavy Board Shield", [("black_army_shield_5" , 0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  
	777, weight(5)|abundance(25)|hit_points(980)|body_armor(3)|spd_rtng(78)|weapon_length(84), imodbits_shield],


#CONQUISTADOR MERCENARY GUILD ITEMS
#Conquistador Helmets
["conquistador_helm1", "Curved_Helm", [("conquistador_helm1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	1749, weight(2.25)|abundance(25)|head_armor(36), imodbits_armor|imodbit_cracked ],
["conquistador_helm2", "Curved_Helm", [("conquistador_helm2", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2160, weight(2.25)|abundance(25)|head_armor(40), imodbits_armor|imodbit_cracked ],
["conquistador_helm3", "Curved_Helm", [("conquistador_helm3", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3486, weight(2.75)|abundance(25)|head_armor(46)|difficulty(7), imodbits_armor|imodbit_cracked ],

#Conquistador Armors
["conquistador_plate_1", "Plate_Armor", [("conquistador_plate_1", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	13251, weight(27)|abundance(25)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_armor|imodbit_cracked ],
["conquistador_plate_2", "Plate_Armor", [("conquistador_plate_2", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	13251, weight(27)|abundance(25)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_armor|imodbit_cracked ],
["conquistador_breast_plate_1", "Breast_Plate_with_Mail", [("conquistador_breast_plate_1", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8793, weight(24)|abundance(25)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],
["conquistador_breast_plate_2", "Breast_Plate_with_Mail", [("conquistador_breast_plate_2", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8793, weight(24)|abundance(25)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],
["conquistador_breast_plate_3", "Breast_Plate_with_Mail", [("conquistador_breast_plate_3", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8793, weight(24)|abundance(25)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],
["conquistador_breast_plate_4", "Breast_Plate_with_Mail", [("conquistador_breast_plate_4", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8793, weight(24)|abundance(25)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],

#Conquistador Shields
["buckler_1", "Wood_Buckler", [("buckler_1", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  
	180 , weight(1)|abundance(25)|hit_points(260)|body_armor(9)|spd_rtng(200)|weapon_length(20), imodbits_shield],
["buckler_2", "Steel_Buckler", [("buckler_2", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  
	539 , weight(1.25)|abundance(25)|hit_points(400)|body_armor(18)|spd_rtng(190)|weapon_length(20), imodbits_shield],

#Conquistador Horses
["conquistador_horse_1", "Warhorse", [("conquistador_horse_1", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["conquistador_horse_2", "Warhorse", [("conquistador_horse_2", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],


#ELEPHANT GUARD MERCENARY GUILD ITEMS
#Elephant Gaurd Helmets
["elephant_guard_helm_1", "Elephant_Guard_Helm", [("elephant_guard_helm_1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3243, weight(2.5)|abundance(25)|head_armor(44)|difficulty(7), imodbits_armor|imodbit_cracked ],
["elephant_guard_helm_2", "Elephant_Guard_Helm", [("elephant_guard_helm_2", 0)], itp_type_head_armor|itp_merchandise, 0, 
	2790, weight(2)|abundance(25)|head_armor(40)|difficulty(7), imodbits_armor|imodbit_cracked ],
["elephant_guard_priestess_wig", "Elephant_Guard_Priestess_Wig", [("elephant_guard_priestess_wig", 0)], itp_type_head_armor|itp_merchandise, 0, 
	5, weight(0.25)|abundance(0)|head_armor(1), imodbit_thick ],
["elephant_guard_shaman_helm", "Battle_Shaman_Helm", [("elephant_guard_shaman_helm", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4005, weight(3.75)|abundance(5)|head_armor(50)|difficulty(7), imodbits_armor|imodbit_cracked ],

#Elephant Gaurd Armors
["elephant_guard_tribesman_body_01", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_01", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(12)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_02", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_02", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(12)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_03", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_03", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(18)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_04", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_04", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(18)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_05", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_05", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(26)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_06", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_06", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(26)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_07", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_07", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(32)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_08", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_08", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(32)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_09", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_09", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(12)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_10", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_10", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(12)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_11", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_11", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(18)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_tribesman_body_12", "Elephant_Guard_Tribesman_Body", [("elephant_guard_tribesman_body_12", 0)], itp_type_body_armor|itp_covers_legs, 0, 
	25, weight(1)|abundance(0)|body_armor(18)|leg_armor(18), imodbits_cloth ],#No merchandise, this is to simulate body paint
["elephant_guard_priestess_body", "Elephant_Guard_Priestess_Body", [("elephant_guard_priestess_body", 0)], itp_type_body_armor|itp_covers_legs, 0, #No merchandise, this is to simulate sexy body
	1975, weight(0.25)|abundance(0)|body_armor(20)|leg_armor(0)|head_armor(20), imodbits_cloth ],
["elephant_guard_shaman_body_1", "Battle_Shaman_Body", [("elephant_guard_shaman_body_1", 0)], itp_type_body_armor|itp_covers_legs, 0, #No merchandise, this is to simulate body paint
	175, weight(0.25)|abundance(0)|body_armor(40)|leg_armor(20)|difficulty(6), imodbits_cloth ],
["elephant_guard_shaman_body_2", "Battle_Shaman_Body", [("elephant_guard_shaman_body_2", 0)], itp_type_body_armor|itp_covers_legs, 0, #No merchandise, this is to simulate body paint
	175, weight(1)|abundance(0)|body_armor(40)|leg_armor(20)|difficulty(6), imodbits_cloth ],

#Elephant Gaurd Gloves
["elephant_guard_gloves", "Leather Gloves", [("elephant_guard_glove_L", 0)], itp_merchandise|itp_type_hand_armor, 0, 
	72, weight(0.25)|abundance(25)|body_armor(2)|difficulty(0), imodbits_cloth],

#Elephant Gaurd Boots
["elephant_guard_shaman_boots", "Battle_Shaman_Boots", [("elephant_guard_shaman_boots", 0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 
	459, weight(1.25)|abundance(25)|leg_armor(20), imodbits_cloth ],

#Elephant Gaurd Weapons
["elephant_tribe_two_side_spear", "Double Sided Spear", [("elephant_double_spear", 0)], itp_warspear|itp_two_handed|itp_merchandise, itc_staff, 
	993, weight(3)|abundance(10)|difficulty(0)|spd_rtng(99)|weapon_length(130)|swing_damage(36 , cut)|thrust_damage(34 , pierce), imodbits_polearm ],
["elephant_guard_sickle_1", "Battle_Sickle", [("elephant_guard_sickle_1", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_parry, itc_cleaver, 
	525, weight(2)|difficulty(0)|spd_rtng(100) | weapon_length(60)|swing_damage(27, cut)|thrust_damage(0 , pierce), imodbits_none ],
["elephant_guard_sickle_2", "Shaman_Sickle", [("elephant_guard_sickle_2", 0)], itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_parry, itc_cleaver, 
	1005, weight(2.5)|abundance(10)|difficulty(0)|spd_rtng(105) | weapon_length(80)|swing_damage(35 , cut)|thrust_damage(0 , pierce), imodbits_none ],

#Elephant Gaurd Shields
["elephant_hide_round_shield_1", "Hide_Covered_Round_Shield", [("elephant_round_hide_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	120, weight(2)|abundance(25)|body_armor(3)|hit_points(260)|spd_rtng(100)|weapon_length(40), imodbits_shield ],
["elephant_hide_round_shield_2", "Hide_Covered_Round_Shield", [("elephant_round_hide_2", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	120, weight(2)|abundance(25)|body_armor(3)|hit_points(260)|spd_rtng(100)|weapon_length(40), imodbits_shield ],
["elephant_kite_hide_1", "Fur_Covered_Shield", [("elephant_kite_hide_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
	461, weight(3.5)|abundance(25)|body_armor(1)|hit_points(600)|spd_rtng(76)|weapon_length(81), imodbits_shield ],
["elephant_kite_hide_2", "Fur_Covered_Shield", [("elephant_kite_hide_2", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
	461, weight(3.5)|abundance(25)|body_armor(1)|hit_points(600)|spd_rtng(76)|weapon_length(81), imodbits_shield ],
["elephant_heater_1", "Heater Shield", [("elephant_heater_1", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	245 , weight(3.5)|abundance(25)|hit_points(410)|body_armor(2)|spd_rtng(80)|weapon_length(50), imodbits_shield ],
["elephant_heater_2", "Heater Shield", [("elephant_heater_2", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	245 , weight(3.5)|abundance(25)|hit_points(410)|body_armor(2)|spd_rtng(80)|weapon_length(50), imodbits_shield ],
["elephant_heater_3", "Heater Shield", [("elephant_heater_3", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	287 , weight(3)|abundance(15)|hit_points(500)|body_armor(2)|spd_rtng(85)|weapon_length(50), imodbits_shield ],


#JOTNAR CLAN MERCENARY GUILD ITEMS
#Jotnar Clan Helmets
["jotnar_clan_helm_1", "Wolf_Helm", [("jotnar_clan_helm_1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	1215, weight(2.75)|abundance(25)|head_armor(30), imodbits_cloth ],
["jotnar_clan_helm_2", "Nordic Helmet with Coif", [("jotnar_clan_helm_2", 0)], itp_merchandise|itp_type_head_armor, 0, 
	3612, weight(2.5)|abundance(25)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["jotnar_clan_helm_3", "Nordic Helmet", [("jotnar_clan_helm_3", 0)], itp_merchandise|itp_type_head_armor, 0, 
	3740, weight(2.5)|abundance(25)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["jotnar_clan_helm_4", "Horned Nordic Helmet", [("jotnar_clan_helm_4", 0)], itp_merchandise|itp_type_head_armor, 0, 
	3011, weight(2.25)|abundance(25)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["jotnar_clan_helm_5", "Horned Nordic Helmet", [("jotnar_clan_helm_5", 0)], itp_merchandise|itp_type_head_armor, 0, 
	3011, weight(2.25)|abundance(25)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["jotnar_clan_helm_6", "Decorated Nordic_Helmet", [("jotnar_clan_helm_6", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3486, weight(2.25)|abundance(25)|head_armor(46)|difficulty(7), imodbits_plate ],
["jotnar_clan_helm_7", "Decorated Nordic_Helmet", [("jotnar_clan_helm_7", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3830, weight(2.5)|abundance(25)|head_armor(48)|difficulty(8), imodbits_plate ],
["jotnar_clan_helm_8", "Winged_Helmet", [("jotnar_clan_helm_8", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3830, weight(2)|abundance(15)|head_armor(48)|difficulty(8), imodbits_plate ],
["jotnar_clan_helm_9", "Winged Great Helmet", [("jotnar_clan_helm_9", 0)], itp_merchandise|itp_type_head_armor|itp_covers_head, 0, 
	4275 , weight(2.75)|abundance(25)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10) , imodbits_plate ],

#Jotnar Clan Armors
["jotnar_clan_armor_1", "Haubergeon", [("jotnar_clan_armor_1", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	4574 , weight(18)|abundance(25)|head_armor(0)|body_armor(35)|leg_armor(6)|difficulty(6) , imodbits_armor ],
["jotnar_clan_armor_2", "Light Leather", [("jotnar_clan_armor_2", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	2613 , weight(5)|abundance(25)|head_armor(0)|body_armor(26)|leg_armor(7)|difficulty(0) , imodbits_cloth ],
["jotnar_clan_armor_3", "Cuir Bouilli", [("jotnar_clan_armor_3", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	9450 , weight(24)|abundance(25)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(9) , imodbits_armor ],
["jotnar_clan_armor_4", "Banded Armor", [("jotnar_clan_armor_4", 0)], itp_merchandise| itp_type_body_armor|itp_covers_legs, 0,
	9450 , weight(23)|abundance(25)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(9) , imodbits_armor ],
["jotnar_clan_armor_5", "Padded Leather", [("jotnar_clan_armor_5", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian, 0,
	3840 , weight(12)|abundance(25)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) , imodbits_cloth ],
["jotnar_clan_armor_6", "Haubergeon", [("jotnar_clan_armor_6", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0,
	4773 , weight(18)|abundance(25)|head_armor(0)|body_armor(36)|leg_armor(6)|difficulty(6) , imodbits_armor ],
["jotnar_clan_armor_7", "Mail Dress with Breast Plate", [("jotnar_clan_armor_7", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs , 0,
	10550 , weight(25)|abundance(15)|head_armor(0)|body_armor(44)|leg_armor(20)|difficulty(8) , imodbits_armor ],
["jotnar_clan_armor_8", "Mail Dress with Breast Plate", [("jotnar_clan_armor_8", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs , 0,
	10550 , weight(25)|abundance(15)|head_armor(0)|body_armor(44)|leg_armor(20)|difficulty(8) , imodbits_armor ],

#Jotnar Clan Boots
["jotnar_clan_boots_1", "Wolf Boots", [("jotnar_clan_boots_1", 0)], itp_merchandise| itp_type_foot_armor |itp_civilian  | itp_attach_armature, 0,
	114 , weight(1)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) , imodbits_cloth ],

#Jotnar Clan Shields
["jotnar_clan_shield_1", "Wolf_Hide_Covered_Round_Shield", [("jotnar_clan_shield_1", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	120, weight(2)|abundance(25)|body_armor(3)|hit_points(260)|spd_rtng(100)|weapon_length(40), imodbits_shield ],
["jotnar_clan_shield_2", "Wolf_Hide_Covered_Shield", [("jotnar_clan_shield_2", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
	461, weight(3.5)|abundance(25)|body_armor(1)|hit_points(600)|spd_rtng(76)|weapon_length(81), imodbits_shield ],
["jotnar_clan_shield_3", "Jotnar Clan Plain Round Shield", [("jotnar_clan_shield_3", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,  
	195 , weight(3)|abundance(25)|body_armor(2)|hit_points(460)|spd_rtng(90)|weapon_length(50), imodbits_shield ],
["jotnar_clan_shield_4", "Jotnar Clan Plain Round Shield", [("jotnar_clan_shield_4", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,  
	195 , weight(3)|abundance(25)|body_armor(2)|hit_points(460)|spd_rtng(90)|weapon_length(50), imodbits_shield ],
["jotnar_clan_shield_5", "Jotnar Clan Plain Round Shield", [("jotnar_clan_shield_5", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield,  
	195 , weight(3)|abundance(25)|body_armor(2)|hit_points(460)|spd_rtng(90)|weapon_length(50), imodbits_shield ],

#Jotnar Clan Horses
["jotnar_clan_horse_1", "Hunter", [("jotnar_clan_horse_1", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["jotnar_clan_horse_2", "Warhorse", [("jotnar_clan_horse_2", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["jotnar_clan_horse_3", "Warhorse", [("jotnar_clan_horse_3", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],


#SERPENT HOST MERCENARY GUILD ITEMS
#Serpent Host Helmets
["serpent_host_helm_1", "Basilisk_Helm", [("serpent_host_helm_1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(2.75)|abundance(25)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],
["serpent_host_helm_2", "Basilisk_Helm", [("serpent_host_helm_2", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3486, weight(2.75)|abundance(25)|head_armor(46)|difficulty(7), imodbits_armor|imodbit_cracked ],
["serpent_host_helm_3", "Athanatoi_Helm", [("serpent_host_helm_3", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3243, weight(2.5)|abundance(25)|head_armor(44)|difficulty(7), imodbits_armor|imodbit_cracked ],
["khergit_war_helmet", "Khergit War Helmet", [("serpent_host_helm_4", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	2700 , weight(2)|abundance(25)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(6) , imodbits_armor|imodbit_cracked ], #Changed mesh from base native item to match guild theme
["serpent_host_rabati_1", "Rabati", [("serpent_host_rabati_1", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	1653 , weight(2)|abundance(25)|head_armor(35)|body_armor(0)|leg_armor(0) , imodbits_cloth ],
["serpent_host_turban_1", "Turban", [("cyc_turban_helmet", 0)], itp_merchandise|itp_type_head_armor   , 0, 
	653 , weight(1.5)|abundance(25)|head_armor(22)|body_armor(0)|leg_armor(0) , imodbits_cloth ],


#Serpent Host Armors
["serpent_host_armor_1", "Lamellar_Armor", [("serpent_host_armor_1", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8883, weight(25)|abundance(25)|body_armor(45)|leg_armor(13)|difficulty(9), imodbits_armor ],
["serpent_host_armor_2", "Mail Shirt with Lamellar", [("serpent_host_armor_2", 0)], itp_merchandise|itp_type_body_armor|itp_covers_legs   , 0, 
	7119 , weight(19)|abundance(25)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7) , imodbits_armor ],
["serpent_host_armor_3", "Lamellar Armor", [("serpent_host_armor_3", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	8883 , weight(25)|abundance(25)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(9) , imodbits_armor ],
["serpent_host_armor_4", "Lamellar Armor", [("serpent_host_armor_4", 0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs , 0,
	8883 , weight(25)|abundance(25)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(9) , imodbits_armor ],
["serpent_host_armor_5", "Plate_Armor", [("serpent_host_armor_5", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	13251, weight(27)|abundance(25)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_armor|imodbit_cracked ],
["serpent_host_armor_6", "Plate_Armor", [("serpent_host_armor_6", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	13251, weight(27)|abundance(25)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_armor|imodbit_cracked ],
["serpent_host_armor_7", "Scale_Mail_Armor", [("serpent_host_armor_7", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	11264, weight(26)|abundance(20)|head_armor(0)|body_armor(50)|leg_armor(16)|difficulty(9), imodbits_armor ],

#Serpent Host Boots
["serpent_host_boots_1",  "Lamellar Boots", [("serpent_host_boots_1", 0)], itp_merchandise|itp_type_foot_armor | itp_attach_armature, 0, 
	777 , weight(1.5)|abundance(25)|head_armor(0)|body_armor(0)|leg_armor(26)|difficulty(0) , imodbits_cloth ],

#Serpent Host Shields
["serpent_host_shield_round_1", "Wooden Shield", [("serpent_host_shield_round_1", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 
	126 , weight(2)|abundance(25)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(50), imodbits_shield ],
["serpent_host_shield_round_2", "Plate_Covered_Round_Shield", [("serpent_host_shield_round_2", 0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield, 
	464 , weight(4)|abundance(25)|hit_points(330)|body_armor(16)|spd_rtng(90)|weapon_length(40), imodbits_shield ],
["serpent_host_shield_heater_1", "Heater Shield", [("serpent_host_shield_heater_1", 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  
	245 , weight(3.5)|hit_points(410)|body_armor(2)|spd_rtng(80)|weapon_length(50), imodbits_shield ],

#Serpent Host Horses
["courser_gray", "Courser", [("serpent_horse_1", 0)], itp_merchandise|itp_type_horse, 0, 
	969, abundance(70)|body_armor(16)|difficulty(2)|horse_speed(43)|horse_maneuver(37)|horse_charge(11), imodbits_horse_basic|imodbit_champion],
["courser_black", "Courser", [("serpent_horse_2", 0)], itp_merchandise|itp_type_horse, 0, 
	969, abundance(70)|body_armor(16)|difficulty(2)|horse_speed(43)|horse_maneuver(37)|horse_charge(11), imodbits_horse_basic|imodbit_champion],
["hunter_white", "Hunter", [("serpent_horse_3", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["hunter_white_brown", "Hunter", [("serpent_horse_4", 0)], itp_merchandise|itp_type_horse, 0, 
	1302, abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["serpent_horse_5", "Warhorse", [("serpent_horse_5", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["serpent_horse_6", "Warhorse", [("serpent_horse_6", 0)], itp_merchandise|itp_type_horse, 0, 
	2574, abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["serpent_horse_7", "Hunter Warhorse", [("serpent_horse_7", 0)], itp_merchandise|itp_type_horse, 0, 
	2349, abundance(20)|hit_points(135)|body_armor(35)|difficulty(4)|horse_speed(38)|horse_maneuver(35)|horse_charge(18), imodbits_horse_basic|imodbit_champion],
["serpent_horse_8", "Hunter Warhorse", [("serpent_horse_8", 0)], itp_merchandise|itp_type_horse, 0, 
	2349, abundance(20)|hit_points(135)|body_armor(35)|difficulty(4)|horse_speed(38)|horse_maneuver(35)|horse_charge(18), imodbits_horse_basic|imodbit_champion],


#SLAVER MERCENARY GUILD ITEMS
#Slaver Helmets
["iron_skull_mask", "Iron_Skull_Mask", [("slaver_helm_1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3243, weight(2.5)|abundance(25)|head_armor(44)|difficulty(7), imodbits_armor ],
["horned_helm1", "Horned_Helm", [("slaver_helm_2", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4275, weight(2.75)|abundance(20)|head_armor(50)|difficulty(10), imodbits_armor ],
["horned_helm2", "Horned_Helm", [("slaver_helm_3", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4275, weight(2.75)|abundance(20)|head_armor(50)|difficulty(10), imodbits_armor ],
["horned_helm3", "Horned_Helm", [("slaver_helm_4", 0)], itp_type_head_armor|itp_merchandise, 0, 
	4275, weight(2.75)|abundance(20)|head_armor(50)|difficulty(10), imodbits_armor ],
["slaver_helm_5", "Slaver_Helm", [("slaver_helm_5", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(3.25)|abundance(25)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],
["slaver_helm_6", "Slaver_Helm", [("slaver_helm_6", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(3.25)|abundance(25)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],
["slaver_helm_7", "Slaver_Helm", [("slaver_helm_7", 0)], itp_type_head_armor|itp_merchandise, 0, 
	3740, weight(3.25)|abundance(25)|head_armor(48)|difficulty(7), imodbits_armor|imodbit_cracked ],
["skull_helm1", "Skull_Helm", [("slaver_skull_helm_1", 0)], itp_type_head_armor|itp_merchandise, 0, 
	1215, weight(1.5)|abundance(5)|head_armor(30), imodbits_armor ],
["skull_helm2", "Skull_Helm", [("slaver_skull_helm_2", 0)], itp_type_head_armor|itp_merchandise, 0, 
	1215, weight(1.5)|abundance(5)|head_armor(30), imodbits_armor ],
["fur_hat_scarf", "Fur_Hat_with_Scarf", [("steam_punk_fur_hat_scarf", 0)], itp_type_head_armor|itp_civilian|itp_merchandise, 0, 
	86, weight(0.5)|head_armor(8), imodbits_cloth ],

#Slaver Armors
["padded_leather2", "Padded_Leather", [("slaver_leather_1", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 
	3840, weight(12)|abundance(25)|body_armor(30)|leg_armor(10), imodbits_cloth ],
["padded_leather3", "Padded_Leather", [("slaver_leather_2", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 
	3840, weight(12)|abundance(25)|body_armor(30)|leg_armor(10), imodbits_cloth ],
["breast_plate_mail5", "Breast_Plate_with_Mail", [("slaver_armor_2", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8793, weight(24)|abundance(25)|body_armor(46)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],
["dark_plate2", "Plate_Armor", [("slaver_armor_3", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	13251, weight(27)|abundance(25)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_armor|imodbit_cracked ],
["padded_mail_2", "Padded_Mail", [("slaver_armor_4", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	7209, weight(20)|abundance(25)|body_armor(40)|leg_armor(12)|difficulty(8), imodbits_cloth ],
["padded_mail_3", "Padded_Mail", [("slaver_armor_5", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	7209, weight(20)|abundance(25)|body_armor(40)|leg_armor(12)|difficulty(8), imodbits_cloth ],
["slaver_armor_6", "Breast_Plate_with_Mail", [("slaver_armor_6", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8793, weight(24)|abundance(25)|body_armor(46)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],
["slaver_armor_7", "Breast_Plate_with_Mail", [("slaver_armor_7", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8793, weight(24)|abundance(25)|body_armor(46)|leg_armor(12)|difficulty(8), imodbits_armor|imodbit_cracked ],

#Slaver Shields
["dragonshield", "Dragon_Shield", [("dragonshield", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	242, weight(2)|abundance(20)|body_armor(3)|hit_points(400)|spd_rtng(105)|weapon_length(40), imodbits_shield ],
["slaver_shield_kite", "Kite_Shield", [("slaver_shield_kite", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
	354, weight(2.5)|abundance(25)|body_armor(1)|hit_points(480)|spd_rtng(82)|weapon_length(90), imodbits_shield ],
["slaver_shield_round_hide", "Hide_Covered_Round_Shield", [("slaver_shield_round_hide", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_round_shield, 
	120, weight(2)|abundance(25)|body_armor(3)|hit_points(260)|spd_rtng(100)|weapon_length(40), imodbits_shield ],
["slaver_shield_kite_hide", "Fur_Covered_Shield", [("slaver_shield_kite_hide", 0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
	461, weight(3.5)|abundance(25)|body_armor(1)|hit_points(600)|spd_rtng(76)|weapon_length(81), imodbits_shield ],


#BOAR CLAN MINI-GUILD (RANDOM MERCENARIES AND BANDITS)
#Boar Clan Helmets
["gladiator_helmet", "Gladiator Helmet", [("lobster_helm", 0)], itp_merchandise|itp_type_head_armor, 0, 
	1749 , weight(2)|abundance(25)|head_armor(36)|body_armor(0)|leg_armor(0), imodbits_plate ],
["gladiator_mask", "Gladiator Mask", [("lobster_mask", 0)], itp_merchandise|itp_type_head_armor, 0, 
	3011 , weight(2.5)|abundance(25)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],

#Boar Clan Armor
["padded_mail_4", "Padded_Mail", [("maille_orn_131", 0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 
	8246, weight(22)|abundance(25)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(8), imodbits_cloth ],

#Boar Clan Shields
["shield_heater_boar", "Boar Heater Shield", [("shield_heater_boar" , 0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
	529, weight(2.5)|abundance(25)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40), imodbits_shield],



#AUTOLOOT: Need this dummy item here to mark end of file
#######
 ["items_end", "INVALID ITEM", [("practice_sword", 0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_longsword, 3, weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(16, blunt)|thrust_damage(10, blunt), imodbits_none],

]

###############################################ITEM MODIFIERS#######################################################
#  Each imod_attributes contains the following elements
#  0) imod
#  1) cost % multiplier for the base item if it has this imod.             (item_get_slot, <dest>, <imod>, slot_item_imod_cost)
#  2) difficulty (skill) adjustment that this imod requires.               (item_get_slot, <dest>, <imod>, slot_item_imod_require)
#  3) imod use effect speed (effects horse speed as well).                 (item_get_slot, <dest>, <imod>, slot_item_imod_speed)
#  4) imod use effect armor rating (effects sheilds & barding too).        (item_get_slot, <dest>, <imod>, slot_item_imod_armor)
#  5) imod use effect weapon damage.                                       (item_get_slot, <dest>, <imod>, slot_item_imod_damage)
#
# These values are stuffed into item slots, via the script_init_auto_loot
# You can then access these values using code such as (item_get_slot, ":cost_multiplier", ":imod", slot_item_imod_cost),
# See module_constants.py for a list of slot_item_imod_xxx slot definitions
#
# NOTE: modifying the values here is to allow the module code to access this information that the module system fails
#       to provide.  chaning these values won't actually cause the game to change its understanding of what the imod
#       does - it will only change *your* code's understanding - making it effectively *WRONG*.
#       Only add new values (columns of data) that the game exe doesn't use.  The ones I've provided should be
#       considered constant / read-only / etc.
####################################################################################################################
imod_effects = [
  #    ID                COST   DFCLT SPD  ARMR DMG
  (imod_plain,           100,     0,   0,   0,   0),
  (imod_cracked,          50,     0,   0,  -4,  -5),
  (imod_rusty,            55,     0,   0,  -3,  -3),
  (imod_bent,             65,     0,  -3,   0,  -3),
  (imod_chipped,          72,     0,   0,   0,  -1),
  (imod_battered,         75,     0,   0,  -2,   0),
  (imod_poor,             80,     0,   0,   0,   0),
  (imod_crude,            83,     0,   0,  -1,   0),
  (imod_old,              86,     0,   0,   0,   0),
  (imod_cheap,            90,     0,   0,   0,   0),
  (imod_fine,            190,     0,   0,   0,   0),
  (imod_well_made,       250,     0,   0,   0,   0),
  (imod_sharp,           160,     0,   0,   0,   0),
  (imod_balanced,        350,     0,   3,   0,   3),
  (imod_tempered,        670,     0,  -1,   0,   4),
  (imod_deadly,          850,     0,   0,   0,   0),
  (imod_exquisite,      1450,     0,   0,   0,   0),
  (imod_masterwork,     1750,     4,   1,   0,   5),
  (imod_heavy,           190,     0,  -2,   3,   2),
  (imod_strong,          490,     2,  -3,   0,   3),
  (imod_powerful,        320,     0,   0,   0,   0),
  (imod_tattered,         50,     0,   0,  -3,   0),
  (imod_ragged,           70,     0,   0,  -2,   0),
  (imod_rough,            60,     0,   0,   0,   0),
  (imod_sturdy,          170,     0,   0,   1,   0),
  (imod_thick,           260,     0,   0,   2,   0),
  (imod_hardened,        390,     0,   0,   3,   0),
  (imod_reinforced,      650,     0,   0,   4,   0),
  (imod_superb,          250,     0,   0,   0,   0),
  (imod_lordly,         1150,     0,   0,   6,   0),
  (imod_lame,             40,     0,  -5,   0,   0),
  (imod_swaybacked,       60,     0,  -2,   0,   0),
  (imod_stubborn,         90,     1,   0,   0,   0),
  (imod_timid,           180,     1,   0,   0,   0),
  (imod_meek,            180,     0,   0,   0,   0),
  (imod_spirited,        650,     0,   1,   0,   0),
  (imod_champion,       1450,     0,   2,   0,   0),
  (imod_fresh,           100,     0,   0,   0,   0),
  (imod_day_old,         100,     0,   0,   0,   0),
  (imod_two_day_old,      90,     0,   0,   0,   0),
  (imod_smelling,         40,     0,   0,   0,   0),
  (imod_rotten,            5,     0,   0,   0,   0),
  (imod_large_bag,       190,     0,   0,   0,   0)
]
