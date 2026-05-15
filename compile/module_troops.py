from header_common import *
from header_operations import *
from header_items import *
from header_troops import *
from header_skills import *
from ID_factions import *
from ID_items import *
from ID_scenes import *
from ID_troops import *

from module_constants import *

####################################################################################################################
#  Each troop contains the following fields:
#  1) Troop id (string): used for referencing troops in other files. The prefix trp_ is automatically added before each troop-id .
#  2) Toop name (string).
#  3) Plural troop name (string).
#  4) Troop flags (int). See header_troops.py for a list of available flags
#  5) Scene (int) (only applicable to heroes) For example: scn_reyvadin_castle|entry(1) puts troop in reyvadin castle's first entry point
#  6) Reserved (int). Put constant "reserved" or 0.
#  7) Faction (int)
#  8) Inventory (list): Must be a list of items
#  9) Attributes (int): Example usage:
#           str_6|agi_6|int_4|cha_5|level(5)
# 10) Weapon proficiencies (int): Example usage:
#           wp_one_handed(55)|wp_two_handed(90)|wp_polearm(36)|wp_archery(80)|wp_crossbow(24)|wp_throwing(45)
#     The function regular_melee(x) will create random weapon proficiencies close to value x.
#     To make an expert archer with other weapon proficiencies close to 60 you can use something like:
#           wp_archery(160) | regular_melee(60)
# 11) Skills (int): See header_skills.py to see a list of skills. Example:
#           knows_ironflesh_3|knows_power_strike_2|knows_athletics_2|knows_riding_2
# 12) Face code (int): You can obtain the face code by pressing ctrl+E in face generator screen
# 13) Face code (int)(2) (only applicable to regular troops, can be omitted for heroes):
#     The game will create random faces between Face code 1 and face code 2 for generated troops
#  town_1   Sargoth
#  town_2   Tihr
#  town_3   Veluca
#  town_4   Suno
#  town_5   Jelkala
#  town_6   Praven
#  town_7   Uxkhal
#  town_8   Reyvadin
#  town_9   Khudan
#  town_10  Tulga
#  town_11  Curaw
#  town_12  Wercheg
#  town_13  Rivacheg
#  town_14  Halmar
####################################################################################################################

# Some constant and function declarations to be used below...

# skill points per level
wp_anemic = 4
wp_weak = 6
wp_regular = 8
wp_expert = 10

# variability of skill level (+/- this amount per skill)
wp_rand = 0
	
def wp_all(x):
  n = 0
  n |= wp_archery(x)
  n |= wp_crossbow(x)
  n |= wp_throwing(x)
  n |= wp_one_handed(x)
  n |= wp_two_handed(x)
  n |= wp_polearm(x)
  return n

def wp_bow(x):
  n = wp_archery(x)
  return n

def wp_xbow(x):
  n = wp_crossbow(x)
  return n

def wp_thrown(x):
  n = wp_throwing(x)
  return n

def wp_ranged(x):
  n = 0
  n |= wp_archery(x)
  n |= wp_crossbow(x)
  n |= wp_throwing(x)
  return n

def wp_melee(x):
  n = 0
  n |= wp_one_handed(x)
  n |= wp_two_handed(x)
  n |= wp_polearm(x)
  return n

# melee troops

def weak_melee(lvl):
  return wp_melee(lvl*wp_weak)|wp_ranged(lvl*wp_anemic)

def regular_melee(lvl):
  return wp_melee(lvl*wp_regular)|wp_ranged(lvl*wp_weak)

def expert_melee(lvl):
  return wp_melee(lvl*wp_expert)|wp_ranged(lvl*wp_regular)

# archers

def weak_archer(lvl):
  return wp_bow(lvl*wp_weak)|wp_xbow(lvl*wp_anemic)|wp_thrown(lvl*wp_anemic)|wp_melee(lvl*wp_anemic)

def regular_archer(lvl):
  return wp_bow(lvl*wp_regular)|wp_xbow(lvl*wp_weak)|wp_thrown(lvl*wp_weak)|wp_melee(lvl*wp_weak)

def expert_archer(lvl):
  return wp_bow(lvl*wp_expert)|wp_xbow(lvl*wp_regular)|wp_thrown(lvl*wp_regular)|wp_melee(lvl*wp_regular)

# crossbowman

def weak_crossbow(lvl):
  return wp_xbow(lvl*wp_weak)|wp_bow(lvl*wp_anemic)|wp_thrown(lvl*wp_anemic)|wp_melee(lvl*wp_anemic)

def regular_crossbow(lvl):
  return wp_xbow(lvl*wp_regular)|wp_bow(lvl*wp_weak)|wp_thrown(lvl*wp_weak)|wp_melee(lvl*wp_weak)

def expert_crossbow(lvl):
  return wp_xbow(lvl*wp_expert)|wp_bow(lvl*wp_regular)|wp_thrown(lvl*wp_regular)|wp_melee(lvl*wp_regular)

# javelinmen (or any throwing weapon unit)

def weak_javelinmen(lvl):
  return wp_thrown(lvl*wp_weak)|wp_xbow(lvl*wp_anemic)|wp_bow(lvl*wp_anemic)|wp_melee(lvl*wp_anemic)

def regular_javelinmen(lvl):
  return wp_thrown(lvl*wp_regular)|wp_xbow(lvl*wp_weak)|wp_bow(lvl*wp_weak)|wp_melee(lvl*wp_weak)

def expert_javelinmen(lvl):
  return wp_thrown(lvl*wp_expert)|wp_xbow(lvl*wp_regular)|wp_bow(lvl*wp_regular)|wp_melee(lvl*wp_regular)

# mixed troops

def weak_all(lvl):
  return wp_melee(lvl*wp_weak)|wp_ranged(lvl*wp_weak)

def regular_all(lvl):
  return wp_melee(lvl*wp_regular)|wp_ranged(lvl*wp_regular)

def expert_all(lvl):
  return wp_melee(lvl*wp_expert)|wp_ranged(lvl*wp_expert)


#Skills
knows_common = knows_riding_1|knows_trade_2|knows_inventory_management_2|knows_prisoner_management_1|knows_leadership_1
def_attrib = str_7 | agi_5 | int_4 | cha_4

knows_lord_1 = knows_riding_3|knows_trade_2|knows_inventory_management_2|knows_tactics_4|knows_prisoner_management_4|knows_leadership_7
knows_lord_2 = knows_riding_10|knows_trade_2|knows_inventory_management_10|knows_tactics_10|knows_prisoner_management_10|knows_leadership_10

knows_warrior_npc = knows_weapon_master_2|knows_ironflesh_1|knows_athletics_1|knows_power_strike_2|knows_riding_2|knows_shield_1|knows_inventory_management_2
knows_merchant_npc = knows_riding_2|knows_trade_3|knows_inventory_management_3 #knows persuasion
knows_tracker_npc = knows_weapon_master_1|knows_athletics_2|knows_spotting_2|knows_pathfinding_2|knows_tracking_2|knows_ironflesh_1|knows_inventory_management_2

lord_attrib = str_20|agi_20|int_20|cha_20|level(38)
lord_attrib2 = str_30|agi_30|int_30|cha_30|level(50)

knight_attrib_1 = str_15|agi_14|int_8|cha_16|level(22)
knight_attrib_2 = str_16|agi_16|int_10|cha_18|level(26)
knight_attrib_3 = str_18|agi_17|int_12|cha_20|level(30)
knight_attrib_4 = str_19|agi_19|int_13|cha_22|level(35)
knight_attrib_5 = str_20|agi_20|int_15|cha_25|level(41)

knight_skills_1 = knows_riding_3|knows_ironflesh_2|knows_power_strike_3|knows_athletics_1|knows_tactics_2|knows_prisoner_management_1|knows_leadership_3
knight_skills_2 = knows_riding_4|knows_ironflesh_3|knows_power_strike_4|knows_athletics_2|knows_tactics_3|knows_prisoner_management_2|knows_leadership_5
knight_skills_3 = knows_riding_5|knows_ironflesh_4|knows_power_strike_5|knows_athletics_3|knows_tactics_4|knows_prisoner_management_2|knows_leadership_6
knight_skills_4 = knows_riding_6|knows_ironflesh_5|knows_power_strike_6|knows_athletics_4|knows_tactics_5|knows_prisoner_management_3|knows_leadership_7
knight_skills_5 = knows_riding_7|knows_ironflesh_6|knows_power_strike_7|knows_athletics_5|knows_tactics_6|knows_prisoner_management_3|knows_leadership_9

#These face codes are generated by the in-game face generator.
#Enable edit mode and press ctrl+E in face generator screen to obtain face codes.


reserved = 0

no_scene = 0

swadian_face_younger_1 = 0x0000000000000001124000000020000000000000001c00800000000000000000
swadian_face_young_1   = 0x0000000400000001124000000020000000000000001c00800000000000000000
swadian_face_middle_1  = 0x0000000800000001124000000020000000000000001c00800000000000000000
swadian_face_old_1     = 0x0000000d00000001124000000020000000000000001c00800000000000000000
swadian_face_older_1   = 0x0000000fc0000001124000000020000000000000001c00800000000000000000

swadian_face_younger_2 = 0x00000000000062c76ddcdf7feefbffff00000000001efdbc0000000000000000
swadian_face_young_2   = 0x00000003c00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
swadian_face_middle_2  = 0x00000007c00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
swadian_face_old_2     = 0x0000000bc00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
swadian_face_older_2   = 0x0000000fc00062c76ddcdf7feefbffff00000000001efdbc0000000000000000

vaegir_face_younger_1 = 0x0000000000000001124000000020000000000000001c00800000000000000000
vaegir_face_young_1   = 0x0000000400000001124000000020000000000000001c00800000000000000000
vaegir_face_middle_1  = 0x0000000800000001124000000020000000000000001c00800000000000000000
vaegir_face_old_1     = 0x0000000d00000001124000000020000000000000001c00800000000000000000
vaegir_face_older_1   = 0x0000000fc0000001124000000020000000000000001c00800000000000000000

vaegir_face_younger_2 = 0x000000003f00230c4deeffffffffffff00000000001efff90000000000000000
vaegir_face_young_2   = 0x00000003bf00230c4deeffffffffffff00000000001efff90000000000000000
vaegir_face_middle_2  = 0x00000007bf00230c4deeffffffffffff00000000001efff90000000000000000
vaegir_face_old_2     = 0x0000000cbf00230c4deeffffffffffff00000000001efff90000000000000000
vaegir_face_older_2   = 0x0000000ff100230c4deeffffffffffff00000000001efff90000000000000000

khergit_face_younger_1 = 0x0000000009003109207000000000000000000000001c80470000000000000000
khergit_face_young_1   = 0x00000003c9003109207000000000000000000000001c80470000000000000000
khergit_face_middle_1  = 0x00000007c9003109207000000000000000000000001c80470000000000000000
khergit_face_old_1     = 0x0000000b89003109207000000000000000000000001c80470000000000000000
khergit_face_older_1   = 0x0000000fc9003109207000000000000000000000001c80470000000000000000

khergit_face_younger_2 = 0x000000003f0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
khergit_face_young_2   = 0x00000003bf0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
khergit_face_middle_2  = 0x000000077f0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
khergit_face_old_2     = 0x0000000b3f0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
khergit_face_older_2   = 0x0000000fff0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000

nord_face_younger_1 = 0x0000000000000001124000000020000000000000001c00800000000000000000
nord_face_young_1   = 0x0000000400000001124000000020000000000000001c00800000000000000000
nord_face_middle_1  = 0x0000000800000001124000000020000000000000001c00800000000000000000
nord_face_old_1     = 0x0000000d00000001124000000020000000000000001c00800000000000000000
nord_face_older_1   = 0x0000000fc0000001124000000020000000000000001c00800000000000000000

nord_face_younger_2 = 0x00000000310023084deeffffffffffff00000000001efff90000000000000000
nord_face_young_2   = 0x00000003b10023084deeffffffffffff00000000001efff90000000000000000
nord_face_middle_2  = 0x00000008310023084deeffffffffffff00000000001efff90000000000000000
nord_face_old_2     = 0x0000000c710023084deeffffffffffff00000000001efff90000000000000000
nord_face_older_2   = 0x0000000ff10023084deeffffffffffff00000000001efff90000000000000000

rhodok_face_younger_1 = 0x0000000009002003140000000000000000000000001c80400000000000000000
rhodok_face_young_1   = 0x0000000449002003140000000000000000000000001c80400000000000000000
rhodok_face_middle_1  = 0x0000000849002003140000000000000000000000001c80400000000000000000
rhodok_face_old_1     = 0x0000000cc9002003140000000000000000000000001c80400000000000000000
rhodok_face_older_1   = 0x0000000fc9002003140000000000000000000000001c80400000000000000000

rhodok_face_younger_2 = 0x00000000000062c76ddcdf7feefbffff00000000001efdbc0000000000000000
rhodok_face_young_2   = 0x00000003c00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
rhodok_face_middle_2  = 0x00000007c00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
rhodok_face_old_2     = 0x0000000bc00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
rhodok_face_older_2   = 0x0000000fc00062c76ddcdf7feefbffff00000000001efdbc0000000000000000

man_face_younger_1 = 0x0000000000000001124000000020000000000000001c00800000000000000000
man_face_young_1   = 0x0000000400000001124000000020000000000000001c00800000000000000000
man_face_middle_1  = 0x0000000800000001124000000020000000000000001c00800000000000000000
man_face_old_1     = 0x0000000d00000001124000000020000000000000001c00800000000000000000
man_face_older_1   = 0x0000000fc0000001124000000020000000000000001c00800000000000000000

man_face_younger_2 = 0x000000003f0052064deeffffffffffff00000000001efff90000000000000000
man_face_young_2   = 0x00000003bf0052064deeffffffffffff00000000001efff90000000000000000
man_face_middle_2  = 0x00000007bf0052064deeffffffffffff00000000001efff90000000000000000
man_face_old_2     = 0x0000000bff0052064deeffffffffffff00000000001efff90000000000000000
man_face_older_2   = 0x0000000fff0052064deeffffffffffff00000000001efff90000000000000000

merchant_face_1    = man_face_young_1
merchant_face_2    = man_face_older_2

woman_face_1    = 0x0000000000000001000000000000000000000000001c00000000000000000000
woman_face_2    = 0x00000003bf0030067ff7fbffefff6dff00000000001f6dbf0000000000000000


refugee_face1 = woman_face_1
refugee_face2 = woman_face_2
girl_face1    = woman_face_1
girl_face2    = woman_face_2

mercenary_face_1 = 0x0000000000000000000000000000000000000000001c00000000000000000000
mercenary_face_2 = 0x0000000cff00730b6db6db6db7fbffff00000000001efffe0000000000000000

vaegir_face1  = vaegir_face_young_1
vaegir_face2  = vaegir_face_older_2

bandit_face1  = man_face_young_1
bandit_face2  = man_face_older_2

undead_face1  = 0x00000000002000000000000000000000
undead_face2  = 0x000000000020010000001fffffffffff

#Cyclohexane Faces
#Villianese
#The paints are arranged in "module_skins.py" so many variations of paint will show up on each unit
# 1 is bald, no beard, and first skin tone   2 is last hair, last beard, and last skin tone (opposite first)
villianese_green_young_1  = 0x000000000001a10036db6db6db6db6db00000000001db6db0000000000000000
villianese_green_young_2  = 0x000000003f01e38b36db6db6db6db6db00000000001db6db0000000000000000
villianese_green_middle_1  = 0x00000007c001a10036db6db6db6db6db00000000001db6db0000000000000000
villianese_green_middle_2  = 0x000000073f01e38b36db6db6db6db6db00000000001db6db0000000000000000
villianese_green_old_1  = 0x0000000fc001a10036db6db6db6db6db00000000001db6db0000000000000000
villianese_green_old_2  = 0x0000000fff01e38b36db6db6db6db6db00000000001db6db0000000000000000
villianese_black_young_1  = 0x000000000001f10036db6db6db6db6db00000000001db6db0000000000000000
villianese_black_young_2  = 0x000000003f02338b36db6db6db6db6db00000000001db6db0000000000000000
villianese_black_middle_1  = 0x000000074001f10036db6db6db6db6db00000000001db6db0000000000000000
villianese_black_middle_2  = 0x00000007bf02338b36db6db6db6db6db00000000001db6db0000000000000000
villianese_black_old_1  = 0x0000000fc001f10036db6db6db6db6db00000000001db6db0000000000000000
villianese_black_old_2  = 0x0000000fff02338b36db6db6db6db6db00000000001db6db0000000000000000
villianese_blue_young_1  = 0x000000000002410036db6db6db6db6db00000000001db6db0000000000000000
villianese_blue_young_2  = 0x000000003f02838b36db6db6db6db6db00000000001db6db0000000000000000
villianese_blue_middle_1  = 0x00000007c002410036db6db6db6db6db00000000001db6db0000000000000000
villianese_blue_middle_2  = 0x00000007bf02838b36db6db6db6db6db00000000001db6db0000000000000000
villianese_blue_old_1  = 0x0000000fc002410036db6db6db6db6db00000000001db6db0000000000000000
villianese_blue_old_2  = 0x0000000fff02838b36db6db6db6db6db00000000001db6db0000000000000000

#Elephant Guard
elephant_guard_face_young_1  = 0x00000001ff00834948db8eb6ed7277fb00000000001e471c0000000000000000 #tribe
elephant_guard_face_young_2  = 0x00000001ff00930748db8eb6ed7277fb00000000001e471c0000000000000000 #tribe
elephant_guard_face_young_3  = 0x000000047f00a30748db8eb6ed7277fb00000000001e471c0000000000000000 #fighter
elephant_guard_face_young_4  = 0x000000047f00b28948db8eb6ed7277fb00000000001e471c0000000000000000 #fighter
elephant_guard_face_young_5  = 0x000000047f01230048db8eb6ed7277fb00000000001e471c0000000000000000 #spearman
elephant_guard_face_young_6  = 0x000000047f01328048db8eb6ed7277fb00000000001e471c0000000000000000 #spearman
elephant_guard_face_middle_1  = 0x00000008bf00c00048db8eb6ed7277fb00000000001e471c0000000000000000 #warrior
elephant_guard_face_middle_2  = 0x00000008bf00d00048db8eb6ed7277fb00000000001e471c0000000000000000 #warrior
elephant_guard_face_middle_3  = 0x00000008bf01400048db8eb6ed7277fb00000000001e471c0000000000000000 #spearman
elephant_guard_face_middle_4  = 0x00000008bf01500048db8eb6ed7277fb00000000001e471c0000000000000000 #spearman
elephant_guard_face_old_1  = 0x0000000fff00e00048db8eb6ed7277fb00000000001e471c0000000000000000 #champion
elephant_guard_face_old_2  = 0x0000000fff00f00048db8eb6ed7277fb00000000001e471c0000000000000000 #champion
elephant_guard_shaman_1  = 0x00000006ff01000048db8eb6ed7277fb00000000001e471c0000000000000000
elephant_guard_shaman_2  = 0x00000006ff01100048db96b6f5b277fb00000000001e471c0000000000000000
elephant_guard_priestess  = 0x000000002510400235a46055048341dc00000000001ea84d0000000000000000

#Jotnar Clan
#The paints are arranged in "module_skins.py" so many variations of paint will show up on each unit
jotnar_clan_female_young_1  = 0x000000000000500136db6db6db6db6db00000000001db6db0000000000000000
jotnar_clan_female_young_2  = 0x000000003f00d00136db6db6db6db6db00000000001db6db0000000000000000
jotnar_clan_female_middle_1  = 0x00000008c000500136db6db6db6db6db00000000001db6db0000000000000000
jotnar_clan_female_middle_2  = 0x00000008ff00d00136db6db6db6db6db00000000001db6db0000000000000000
jotnar_clan_female_old_1  = 0x0000000fff00d00136db6db6db6db6db00000000001db6db0000000000000000

#Boar Clan
#The paints are arranged in "module_skins.py" so many variations of paint will show up on each unit
boar_clan_1  = 0x000000019c04f340493289e72265469600000000001e268d0000000000000000
boar_clan_2  = 0x0000000fee0101544524aebb215a325000000000001e3a5a0000000000000000

#Slave faces
slave_1  = 0x000000000000000036aa9627998eb2dc00000000001d961a0000000000000000
slave_2  = 0x0000000fff0075d436aa9627998eb2dc00000000001d961a0000000000000000
slave_female_1  = 0x000000000000000036db6db6db6db6db00000000001db6db0000000000000000
slave_female_2  = 0x0000000fff00400a36db6db6db6db6db00000000001db6db0000000000000000

#NAMES:
#


troops = [
  ["player", "Player", "Player", tf_hero|tf_unmoveable_in_party_window, no_scene, reserved, fac_player_faction, [],
   str_4|agi_4|int_4|cha_4, wp_all(20), 0, 0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],
  ["temp_troop", "Temp Troop", "Temp Troop", tf_hero, no_scene, reserved, fac_commoners, [], def_attrib, 0, knows_inventory_management_10, 0],
  ["game", "Game", "Game", tf_hero, no_scene, reserved, fac_commoners, [], def_attrib, 0, knows_common, 0],
  ["unarmed_troop", "Unarmed Troop", "Unarmed Troops", tf_hero, no_scene, reserved, fac_commoners, [itm_arrows, itm_short_bow], def_attrib|str_14, 0, knows_power_draw_2, 0],
####################################################################################################################
# Troops before this point are hardwired into the game and their order should not be changed!
####################################################################################################################
  ["random_town_sequence", "Random Town Sequence", "Random Town Sequence", tf_hero, no_scene, reserved, fac_commoners, [], def_attrib, 0, knows_common|knows_inventory_management_10, 0],
  ["tournament_participants", "Tournament Participants", "Tournament Participants", tf_hero, no_scene, reserved, fac_commoners, [], def_attrib, 0, knows_common|knows_inventory_management_10, 0],
  ["tutorial_maceman", "Maceman", "Maceman", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_tutorial_club, itm_leather_jerkin, itm_hide_boots],
   str_6|agi_6|level(1), regular_melee(1), 0, mercenary_face_1, mercenary_face_2],
  ["tutorial_archer", "Archer", "Archer", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, no_scene, reserved, fac_commoners,
   [itm_tutorial_short_bow, itm_tutorial_arrows, itm_linen_tunic, itm_hide_boots],
   str_6|agi_6|level(5), regular_archer(5), knows_power_draw_4, mercenary_face_1, mercenary_face_2],
  ["tutorial_swordsman", "Swordsman", "Swordsman", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_tutorial_sword, itm_leather_vest, itm_hide_boots],
   str_6|agi_6|level(5), regular_melee(5), 0, mercenary_face_1, mercenary_face_2],
   
  ["wine_recipient", "Tavern Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face,           scn_town_1_tavern|entry(9), 0,   fac_commoners, [itm_leather_apron,       itm_wrapping_boots], def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["khergit_chieftain", "Khergit Chieftain", "Khergit Chieftains", tf_randomize_face|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_shield|tf_hero, 0, 0, fac_kingdom_3,
   [itm_arrows, itm_sword_khergit_4, itm_winged_mace, itm_spear, itm_lance, itm_lance, itm_khergit_bow, itm_strong_bow, itm_short_bow, itm_khergit_arrows, itm_arrows, itm_tab_shield_small_round_b, itm_tab_shield_small_round_c,
    itm_khergit_guard_helmet, itm_khergit_cavalry_helmet, itm_lamellar_armor, itm_hide_boots, itm_leather_gloves,
    itm_courser],
   def_attrib|level(23), regular_all(23), knows_riding_6|knows_power_strike_4|knows_power_draw_3|knows_power_throw_2|knows_ironflesh_4|knows_horse_archery_1, khergit_face_middle_1, khergit_face_older_2],
   ["fugitive2", "Nervous Man", "Nervous Men", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_short_tunic, itm_linen_tunic, itm_coarse_tunic, itm_tabard, itm_leather_vest, itm_woolen_hose, itm_nomad_boots, itm_blue_hose, itm_wrapping_boots, itm_fur_hat, itm_leather_cap, itm_sword_medieval_b, itm_throwing_daggers],
   def_attrib|str_24|agi_25|level(26), regular_melee(26), knows_common|knows_power_throw_6|knows_power_strike_6|knows_ironflesh_9, man_face_middle_1, man_face_old_2],
	["sh_spy", "Serpent Host Spy", "Serpent Host Spy", tf_randomize_face|tf_hero|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse, 0, 0, fac_neutral,
   [itm_sword_viking_1, itm_leather_jerkin, itm_leather_boots, itm_courser, itm_leather_gloves],
   def_attrib|agi_11|level(20), regular_melee(20), knows_common, man_face_middle_1, man_face_older_2],
	

   #twan456 made tournament/arena default fighters better
  ["novice_fighter", "Novice Fighter", "Novice Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_6|agi_6|level(5), regular_melee(5), 0, mercenary_face_1, mercenary_face_2],
  ["regular_fighter", "Regular Fighter", "Regular Fighters", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_8|agi_8|level(11), regular_melee(11), knows_ironflesh_1|knows_power_strike_2|knows_athletics_1|knows_riding_2|knows_shield_2, mercenary_face_1, mercenary_face_2],
  ["veteran_fighter", "Veteran Fighter", "Veteran Fighters", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, no_scene, 0, fac_commoners,
   [itm_hide_boots],
   str_10|agi_10|level(17), regular_all(17), knows_ironflesh_5|knows_power_strike_4|knows_athletics_2|knows_riding_4|knows_horse_archery_3|knows_power_draw_2|knows_shield_3, mercenary_face_1, mercenary_face_2],
  ["champion_fighter", "Champion Fighter", "Champion Fighters", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_12|agi_11|level(24), expert_all(24), knows_ironflesh_6|knows_power_strike_5|knows_athletics_4|knows_riding_5|knows_horse_archery_4|knows_power_draw_3|knows_shield_4, mercenary_face_1, mercenary_face_2],

  ["arena_training_fighter_1", "Novice Fighter", "Novice Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_6|agi_6|level(5), regular_melee(5), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_2", "Novice Fighter", "Novice Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_7|agi_6|level(7), regular_melee(7), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_3", "Regular Fighter", "Regular Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_8|agi_7|level(9), regular_melee(9), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_4", "Regular Fighter", "Regular Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_8|agi_8|level(11), regular_melee(11), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_5", "Regular Fighter", "Regular Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_9|agi_8|level(13), regular_melee(13), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_6", "Veteran Fighter", "Veteran Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_10|agi_9|level(15), regular_melee(15), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_7", "Veteran Fighter", "Veteran Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_10|agi_10|level(17), regular_melee(17), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_8", "Veteran Fighter", "Veteran Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_11|agi_10|level(19), regular_melee(19), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_9", "Champion Fighter", "Champion Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_12|agi_11|level(21), regular_melee(21), 0, mercenary_face_1, mercenary_face_2],
  ["arena_training_fighter_10", "Champion Fighter", "Champion Fighters", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_hide_boots],
   str_12|agi_12|level(23), regular_melee(23), 0, mercenary_face_1, mercenary_face_2],

  ["cattle", "Cattle", "Cattle", 0, no_scene, reserved, fac_neutral, [], def_attrib|level(1), 0, 0, mercenary_face_1, mercenary_face_2],


#soldiers:
#This troop is the troop marked as soldiers_begin
  ["farmer", "Farmer", "Farmers", tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones,
    itm_leather_cap, itm_felt_hat, itm_felt_hat, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
   def_attrib|level(4), weak_melee(4), 0, man_face_middle_1, man_face_old_2],
  ["townsman", "Townsman", "Townsmen", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_cleaver, itm_knife, itm_club, itm_quarter_staff, itm_dagger, itm_stones,
    itm_leather_cap, itm_linen_tunic, itm_coarse_tunic, itm_leather_apron, itm_nomad_boots, itm_wrapping_boots],
   def_attrib|level(5), weak_melee(5), 0, mercenary_face_1, mercenary_face_2],
#MERCENARY TROOPS BEGIN    MERCENARY TROOPS BEGIN    MERCENARY TROOPS BEGIN    MERCENARY TROOPS BEGIN    MERCENARY TROOPS BEGIN    MERCENARY TROOPS BEGIN    MERCENARY TROOPS BEGIN    
#Troops placed between "MERCENARY TROOPS BEGIN" and "MERCENARY TROOPS END" will randomly spawn in taverns
  ["watchman", "Watchman", "Watchmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, no_scene, reserved, fac_commoners,
   [itm_padded_coif, itm_footman_helmet, itm_leather_cap, itm_padded_cloth, itm_leather_jerkin, itm_nomad_boots, itm_wrapping_boots, itm_tab_shield_round_a, itm_tab_shield_round_b, 
    itm_spiked_club, itm_fighting_pick, itm_sword_medieval_a, itm_boar_spear, itm_hunting_crossbow, itm_light_crossbow, itm_bolts],
   def_attrib|level(9), regular_melee(9), knows_shield_1, mercenary_face_1, mercenary_face_2],
  ["caravan_guard", "Caravan Guard", "Caravan Guards", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_shield, no_scene, 0, fac_commoners,
   [itm_padded_coif, itm_nasal_helmet, itm_footman_helmet, itm_leather_jerkin, itm_leather_vest, itm_hide_boots, itm_tab_shield_round_b, itm_tab_shield_round_c, 
    itm_spear, itm_fighting_pick, itm_sword_medieval_a, itm_battle_axe, 
    itm_saddle_horse],
   def_attrib|level(14), regular_melee(14), knows_riding_2|knows_ironflesh_1|knows_shield_3, mercenary_face_1, mercenary_face_2],
  ["mercenary_horseman", "Mercenary Horseman", "Mercenary Horsemen", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_commoners,
   [itm_norman_helmet, itm_mail_coif, itm_helmet_with_neckguard, itm_mail_shirt, itm_haubergeon, itm_hide_boots, itm_tab_shield_heater_c, 
    itm_lance, itm_bastard_sword_a, itm_sword_medieval_b, 
    itm_saddle_horse, itm_courser, itm_hunter],
   def_attrib|level(19), regular_melee(19), knows_riding_4|knows_ironflesh_2|knows_shield_2|knows_power_strike_2, mercenary_face_1, mercenary_face_2],
  ["mercenary_cavalry", "Mercenary Cavalry", "Mercenary Cavalry", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_commoners,
   [itm_kettle_hat, itm_mail_coif, itm_flat_topped_helmet, itm_helmet_with_neckguard, itm_mail_hauberk, itm_banded_armor, itm_hide_boots, 
    itm_lance, itm_bastard_sword_a, itm_sword_medieval_b, itm_tab_shield_heater_c, 
    itm_saddle_horse, itm_courser, itm_hunter],
   def_attrib|level(24), regular_melee(24), knows_riding_5|knows_ironflesh_3|knows_shield_3|knows_power_strike_3, mercenary_face_1, mercenary_face_2],
  ["sod_mercenary_footman", "Mercenary Footman", "Mercenary Footmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, no_scene, reserved, fac_commoners,
   [itm_leather_cap, itm_padded_coif, itm_footman_helmet, itm_mail_hauberk, itm_mail_hauberk, itm_nomad_boots, itm_wrapping_boots, itm_tab_shield_round_a, itm_tab_shield_round_b,
    itm_hunting_crossbow, itm_light_crossbow, itm_bolts, itm_spiked_club, itm_fighting_pick, itm_sword_medieval_a, itm_boar_spear],
   def_attrib|level(14), regular_melee(14), knows_shield_1, mercenary_face_1, mercenary_face_2],
  ["mercenary_swordsman", "Mercenary Swordsman", "Mercenary Swordsmen", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_commoners,
   [itm_kettle_hat, itm_mail_coif, itm_flat_topped_helmet, itm_helmet_with_neckguard, itm_mail_hauberk, itm_haubergeon, itm_hide_boots, 
    itm_bastard_sword_a, itm_sword_medieval_b, itm_sword_medieval_b_small, itm_tab_shield_heater_c,
    itm_hunter],
   def_attrib|level(19), regular_melee(19), knows_riding_3|knows_ironflesh_2|knows_shield_3|knows_power_strike_2, mercenary_face_1, mercenary_face_2],
  ["hired_blade", "Hired Blade", "Hired Blades", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_commoners,
   [itm_guard_helmet, itm_great_helmet, itm_bascinet, itm_haubergeon, itm_mail_chausses, itm_iron_greaves, itm_leather_gloves, 
    itm_bastard_sword_b, itm_sword_medieval_c, itm_tab_shield_heater_cav_a,
    itm_warhorse],
   def_attrib|level(24), regular_melee(24), knows_riding_3|knows_athletics_5|knows_shield_4|knows_power_strike_4|knows_ironflesh_3, mercenary_face_1, mercenary_face_2],
  ["mercenary_crossbowman", "Mercenary Crossbowman", "Mercenary Crossbowmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, no_scene, reserved, fac_commoners,
   [itm_leather_cap, itm_padded_coif, itm_footman_helmet, itm_padded_cloth, itm_leather_jerkin, itm_gold_tourney_armor, itm_nomad_boots, itm_wrapping_boots, 
    itm_spiked_club, itm_fighting_pick, itm_sword_medieval_a, itm_boar_spear, itm_crossbow, itm_bolts, itm_tab_shield_pavise_a, itm_tab_shield_round_b],
   def_attrib|level(19), regular_crossbow(19), knows_athletics_2|knows_shield_1, mercenary_face_1, mercenary_face_2],
  ["sod_mercenary_sharpshooter", "Mercenary Sharpshooter", "Mercenary Sharpshooters", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, no_scene, reserved, fac_commoners,
   [itm_leather_cap, itm_padded_coif, itm_footman_helmet, itm_padded_cloth, itm_leather_jerkin, itm_nomad_boots, itm_wrapping_boots, 
    itm_spiked_club, itm_fighting_pick, itm_sword_medieval_a, itm_boar_spear, itm_heavy_crossbow, itm_steel_bolts, itm_tab_shield_pavise_a, itm_tab_shield_round_b],
   def_attrib|level(24), regular_crossbow(24), knows_athletics_2|knows_shield_1, mercenary_face_1, mercenary_face_2],


# MERCENARY GUILD - BLACK ARMY
#Melee Infantry
  ["black_army_fresh_blade", "Black Army Fresh Blade", "Black Army Fresh Blades", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild1,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_hand_axe, itm_one_handed_war_axe_a, itm_winged_mace, itm_spiked_mace, itm_hunting_crossbow, itm_bolts, itm_black_army_shield_1,
    itm_black_army_helm_1, itm_black_army_armor_1, itm_leather_boots, itm_black_army_boot_1, itm_black_army_leather_gloves],
   def_attrib|level(7), regular_melee(7), knows_athletics_1|knows_shield_1, mercenary_face_1, mercenary_face_2],

  ["black_army_line_keeper", "Black Army Line Keeper", "Black Army Line Keepers", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild1,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_hand_axe, itm_one_handed_war_axe_a, itm_mace_2, itm_mace_3, itm_light_crossbow, itm_bolts, itm_black_army_shield_3,
    itm_black_army_helm_2, itm_black_army_armor_2, itm_black_army_boot_1, itm_black_army_leather_gloves],
   def_attrib|level(14), regular_melee(14), knows_athletics_2|knows_shield_2|knows_power_strike_2, mercenary_face_1, mercenary_face_2],

  ["black_army_iron_guard", "Black Army Iron Guard", "Black Army Iron Guards", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild1,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_mace_2, itm_mace_3, itm_mace_4, itm_mace_5, itm_mace_6, itm_black_army_shield_4, itm_black_army_shield_5,
    itm_black_army_helm_4, itm_black_army_helm_5, itm_black_army_armor_3, itm_black_army_armor_4, itm_black_greaves, itm_darkboots, itm_darkgauntlets],
   def_attrib|level(21), weak_melee(21), knows_athletics_1|knows_ironflesh_3|knows_shield_4|knows_power_strike_1, mercenary_face_1, mercenary_face_2],

  ["black_army_ravager", "Black Army Ravager", "Black Army Ravagers", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild1,
   [itm_katzbalger, itm_scimitar, itm_sword_two_handed_a, itm_estoc, itm_one_handed_battle_axe_c, itm_one_handed_battle_axe_a, itm_executionner_axe_, itm_club_with_spike_head, itm_mace_7, itm_spikepolehammer1, itm_spikepolehammer2, itm_spikepolehammer3, itm_spikepolehammer4, itm_realtwohandedwarhammer, itm_realglaive, itm_glaive, itm_jarid, itm_throwing_axes, itm_light_crossbow, itm_bolts, itm_black_army_shield_4, 
    itm_black_army_helm_4, itm_black_army_helm_5, itm_black_army_armor_5, itm_black_army_armor_6, itm_black_army_armor_7, itm_black_army_boot_1, itm_black_army_leather_gloves],
   def_attrib|level(21), regular_all(21), knows_athletics_4|knows_ironflesh_1|knows_shield_2|knows_power_strike_4, mercenary_face_1, mercenary_face_2],

#Ranged Infantry
  ["black_army_line_supporter", "Black Army Line Supporter", "Black Army Line Supporters", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield|tf_guarantee_ranged, no_scene, reserved, fac_sod_merc_guild1,
   [itm_crossbow, itm_bolts, itm_nomad_bow, itm_arrows, itm_dagger, itm_seax, itm_black_army_shield_1,
    itm_black_army_helm_1, itm_black_army_armor_1, itm_leather_boots, itm_black_army_boot_1, itm_black_army_leather_gloves],
   def_attrib|level(13), regular_crossbow(13)|regular_archer(13)|weak_melee(13), knows_athletics_1|knows_ironflesh_1|knows_shield_2, mercenary_face_1, mercenary_face_2],

  ["black_army_assaulter", "Black Army Assaulter", "Black Army Assaulters", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield|tf_guarantee_ranged, no_scene, reserved, fac_sod_merc_guild1,
   [itm_sniper_crossbow, itm_heavy_crossbow, itm_steel_bolts, itm_strong_bow, itm_bodkin_arrows, itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_sword_khergit_1, itm_sword_khergit_2, itm_black_army_shield_3, itm_black_army_shield_4,
    itm_black_army_helm_2, itm_black_army_armor_2, itm_black_army_boot_1, itm_black_army_leather_gloves],
   def_attrib|level(23), regular_crossbow(23)|regular_archer(23)|weak_melee(23), knows_athletics_3|knows_ironflesh_3|knows_shield_2|knows_power_strike_2, mercenary_face_1, mercenary_face_2],

#Melee Cavalry
   ["black_army_line_crusher", "Black Army Line Crusher", "Black Army Line Crushers", tf_guarantee_horse|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild1,
    [itm_falchion, itm_bastard_sword_a, itm_talak_bastard_sword, itm_black_army_shield_1, itm_black_army_shield_2, 
     itm_black_army_helm_3, itm_black_army_armor_1, itm_black_army_armor_2, itm_black_army_boot_1, itm_black_army_leather_gloves,
     itm_hunter, itm_brown_hunter, itm_hunting_horse_seven],
    def_attrib|level(12), regular_melee(12), knows_riding_3|knows_ironflesh_2|knows_power_strike_3, mercenary_face_1, mercenary_face_2],

   ["black_army_ironside", "Black Army Ironside", "Black Army Ironsides", tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, no_scene, reserved, fac_sod_merc_guild1,
    [itm_sword_of_war, itm_sword_two_handed_a, itm_sword_two_handed_b, itm_bastard_sword_b, itm_black_army_shield_1, itm_black_army_shield_2,
     itm_black_army_helm_4, itm_black_army_helm_5, itm_black_army_armor_5, itm_black_army_armor_6, itm_black_army_armor_7, itm_black_greaves, itm_darkboots, itm_darkgauntlets,
     itm_hunter, itm_brown_hunter, itm_hunting_horse_seven, itm_charger_black, itm_warhorse_black],
    def_attrib|level(22), regular_melee(22), knows_riding_4|knows_ironflesh_4|knows_power_strike_4, mercenary_face_1, mercenary_face_2],


# MERCENARY GUILD - CONQUISTADORS
#Melee Infantry
  ["conquistador_footman", "Conquistador Footman", "Conquistador Footmen", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild2,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_buckler_1,
    itm_conquistador_helm1, itm_light_leather, itm_light_leather_boots, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(14), regular_melee(14), knows_athletics_1|knows_shield_2, mercenary_face_1, mercenary_face_2],

  ["conquistador_pikeman", "Conquistador Pikeman", "Conquistador Pikemen", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_boots, no_scene, reserved, fac_sod_merc_guild2,
   [itm_realpikeb,
    itm_conquistador_helm1, itm_mail_shirt, itm_mail_hauberk, itm_splinted_leather_greaves, itm_mail_chausses, itm_leather_gloves],
   def_attrib|level(18), regular_melee(18), knows_athletics_3|knows_power_strike_4|knows_ironflesh_2, mercenary_face_1, mercenary_face_2],

  ["conquistador_tercio_pikeman", "Conquistador Tercio Pikeman", "Conquistador Tercio Pikemen", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_boots, no_scene, reserved, fac_sod_merc_guild2,
   [itm_realpikeb,
    itm_conquistador_helm2, itm_conquistador_breast_plate_3, itm_conquistador_breast_plate_4, itm_mail_boots, itm_mail_mittens],
   def_attrib|level(23), expert_melee(23), knows_athletics_4|knows_power_strike_5|knows_ironflesh_3, mercenary_face_1, mercenary_face_2],

  ["conquistador_swordsman", "Conquistador Swordsmen", "Conquistador Swordsmen", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild2,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_buckler_1, itm_buckler_2,
    itm_conquistador_helm1, itm_mail_shirt, itm_mail_hauberk, itm_splinted_leather_greaves, itm_mail_chausses, itm_leather_gloves],
   def_attrib|level(18), regular_melee(18), knows_athletics_3|knows_power_strike_2|knows_ironflesh_2|knows_shield_3, mercenary_face_1, mercenary_face_2],

  ["conquistador_rodelero", "Conquistador Rodelero", "Conquistador Rodeleros", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild2,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_buckler_2,
    itm_conquistador_helm2, itm_conquistador_breast_plate_1, itm_conquistador_breast_plate_2, itm_mail_boots, itm_mail_mittens],
   def_attrib|level(20), expert_melee(20), knows_athletics_5|knows_power_strike_4|knows_ironflesh_3|knows_shield_5, mercenary_face_1, mercenary_face_2],

#Ranged Infantry
  ["conquistador_crossbowman", "Conquistador Crossbowman", "Conquistador Crossbowmen", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield|tf_guarantee_ranged, no_scene, reserved, fac_sod_merc_guild2,
   [itm_crossbow, itm_bolts, itm_sword_medieval_b_small, itm_buckler_1,
    itm_conquistador_helm1, itm_leather_vest, itm_leather_jerkin, itm_light_leather_boots, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(12), regular_crossbow(12), knows_athletics_1|knows_shield_2, mercenary_face_1, mercenary_face_2],

  ["conquistador_seasoned_crossbowman", "Conquistador_Seasoned_Crossbowman", "Conquistador_Seasoned_Crossbowmen", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield|tf_guarantee_ranged, no_scene, reserved, fac_sod_merc_guild2,
   [itm_heavy_crossbow, itm_sniper_crossbow, itm_steel_bolts, itm_sword_medieval_b_small, itm_buckler_1, itm_buckler_2,
    itm_conquistador_helm2, itm_heraldic_studded_leather_coat, itm_light_leather_boots, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(16), expert_crossbow(16), knows_athletics_2|knows_ironflesh_2|knows_shield_3, mercenary_face_1, mercenary_face_2],


# MERCENARY GUILD - ELEPHANT GUARD
#Melee Infantry
  ["elephant_guard_tribesman", "Elephant_Guard_Tribesman", "Elephant_Guard_Tribesmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild3,
   [itm_elephant_tribe_two_side_spear, itm_sickle, itm_stones, itm_elephant_hide_round_shield_1, 
   itm_elephant_guard_tribesman_body_01, itm_elephant_guard_tribesman_body_02, itm_leather_boots, itm_hide_boots, itm_leather_gloves],
   def_attrib|level(10), regular_melee(10), knows_athletics_6|knows_shield_4|knows_power_strike_3|knows_power_throw_3|knows_ironflesh_3, elephant_guard_face_young_1, elephant_guard_face_young_2],

  ["elephant_guard_fighter", "Elephant_Guard_Fighter", "Elephant_Guard_Fighter", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild3,
   [itm_elephant_tribe_two_side_spear, itm_sickle, itm_stones, itm_elephant_hide_round_shield_2, 
   itm_elephant_guard_tribesman_body_03, itm_elephant_guard_tribesman_body_04, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(14), regular_melee(14), knows_athletics_6|knows_shield_5|knows_power_strike_4|knows_power_throw_4|knows_ironflesh_4, elephant_guard_face_young_3, elephant_guard_face_young_4],

  ["elephant_guard_warrior", "Elephant_Guard_Warrior", "Elephant_Guard_Warriors", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild3,
   [itm_elephant_tribe_two_side_spear, itm_elephant_guard_sickle_1, itm_throwing_knives, itm_elephant_kite_hide_1, 
   itm_elephant_guard_helm_2, itm_elephant_guard_tribesman_body_05, itm_elephant_guard_tribesman_body_06, itm_nobleman_greaves, itm_leather_gloves],
   def_attrib|level(18), regular_melee(18), knows_athletics_7|knows_shield_6|knows_power_strike_5|knows_power_throw_4|knows_ironflesh_5, elephant_guard_face_middle_1, elephant_guard_face_middle_2],

  ["elephant_guard_champion", "Elephant_Guard_Champion", "Elephant_Guard_Champions", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild3,
   [itm_elephant_tribe_two_side_spear, itm_elephant_guard_sickle_2, itm_throwing_daggers, itm_elephant_kite_hide_2, 
   itm_elephant_guard_helm_1, itm_elephant_guard_tribesman_body_07, itm_elephant_guard_tribesman_body_08, itm_elephant_guard_gloves, itm_nobleman_greaves],
   def_attrib|level(22), expert_melee(22), knows_athletics_7|knows_shield_7|knows_power_strike_6|knows_power_throw_6|knows_ironflesh_6, elephant_guard_face_old_1, elephant_guard_face_old_2],

#Ranged Infantry
  ["elephant_guard_spearman", "Elephant_Guard_Spearman", "Elephant_Guard_Spearmen", tf_guarantee_ranged|tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves, no_scene, reserved, fac_sod_merc_guild3,
   [itm_throwing_spear, itm_throwing_spear, itm_elephant_heater_1, itm_sickle, 
    itm_elephant_guard_tribesman_body_09, itm_elephant_guard_tribesman_body_10, itm_leather_gloves, itm_leather_boots, itm_hide_boots],
   def_attrib|level(14), regular_javelinmen(14), knows_athletics_5|knows_shield_3|knows_power_throw_4|knows_ironflesh_3, elephant_guard_face_young_5, elephant_guard_face_young_6],
  
  ["elephant_guard_penetrator", "Elephant_Guard_Penetrator", "Elephant_Guard_Penetrators", tf_guarantee_ranged|tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves, no_scene, reserved, fac_sod_merc_guild3,
   [itm_throwing_spear, itm_throwing_spear, itm_elephant_heater_2, itm_elephant_guard_sickle_1, 
    itm_elephant_guard_helm_1, itm_elephant_guard_tribesman_body_11, itm_elephant_guard_tribesman_body_12, itm_elephant_guard_gloves, itm_nobleman_greaves],
   def_attrib|level(20), expert_javelinmen(20), knows_athletics_5|knows_shield_4|knows_power_throw_6|knows_ironflesh_5, elephant_guard_face_middle_3, elephant_guard_face_middle_4],


# MERCENARY GUILD - JOTNAR CLAN
#Melee Infantry
  ["jotnar_clan_armsman", "Jotnar_Clan_Armsman", "Jotnar_Clan_Armsmen", tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_sod_merc_guild4,
   [itm_battle_axe, itm_two_handed_axe, itm_two_handed_battle_axe_2, itm_realbastarda, itm_hand_axe, itm_one_handed_war_axe_a, itm_one_handed_war_axe_b, itm_jotnar_clan_shield_2, 
   itm_jotnar_clan_helm_1, itm_steppe_cap, itm_helmet_fur_a, itm_khergit_armor, itm_rawhide_coat, itm_jotnar_clan_boots_1, itm_hunter_boots, itm_leather_gloves],
   def_attrib|level(12), regular_melee(12), knows_athletics_3|knows_shield_1|knows_power_strike_2|knows_power_throw_1|knows_ironflesh_1, villianese_black_young_1, villianese_blue_young_2],

  ["jotnar_clan_jarl", "Jotnar_Clan_Jarl", "Jotnar_Clan_Jarls", tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves, no_scene, reserved, fac_sod_merc_guild4,
   [itm_battle_axe, itm_two_handed_axe, itm_two_handed_battle_axe_2, itm_realbastarde, 
   itm_jotnar_clan_helm_2, itm_nordic_helmet, itm_jotnar_clan_armor_1, itm_mail_shirt, itm_mail_hauberk, itm_mail_boots, itm_mail_mittens],
   def_attrib|level(16), regular_melee(16), knows_athletics_3|knows_shield_2|knows_power_strike_3|knows_power_throw_2|knows_ironflesh_2, villianese_black_young_1, villianese_blue_middle_2],

  ["jotnar_clan_einherjar", "Jotnar_Clan_Einherjar", "Jotnar_Clan_Einherjars", tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves, no_scene, reserved, fac_sod_merc_guild4,
   [itm_dblhead_axe_2, itm_nord_battle_axe, itm_great_axe, itm_mountainlordsword, 
   itm_jotnar_clan_helm_3, itm_jotnar_clan_helm_2, itm_jotnar_clan_armor_3, itm_jotnar_clan_armor_4, itm_mail_boots, itm_mail_mittens],
   def_attrib|level(20), regular_melee(20), knows_athletics_4|knows_shield_3|knows_power_strike_4|knows_power_throw_3|knows_ironflesh_3, villianese_black_young_1, villianese_blue_old_2],

#Ranged Infantry
  ["jotnar_clan_axe_thrower", "Jotnar_Clan_Axe_Thrower", "Jotnar_Clan_Axe_Throwers", tf_guarantee_ranged|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild4,
   [itm_throwing_axes, itm_throwing_axes, itm_one_handed_battle_axe_b, itm_one_handed_battle_axe_c, itm_jotnar_clan_shield_3, itm_jotnar_clan_shield_2, 
   itm_jotnar_clan_helm_4, itm_jotnar_clan_helm_5, itm_jotnar_clan_armor_2, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(17), regular_javelinmen(17), knows_athletics_3|knows_shield_3|knows_power_strike_2|knows_power_throw_4|knows_ironflesh_1, villianese_black_young_1, villianese_blue_middle_2],

#Melee Cavalry
   ["jotnar_clan_volva", "Jotnar_Clan_Volva", "Jotnar_Clan_Volvas", tf_female|tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild4,
    [itm_war_spear, itm_sword_viking_1, itm_strong_bow, itm_arrows, itm_javelin, itm_throwing_axes, itm_jotnar_clan_shield_1,
     itm_jotnar_clan_helm_1, itm_steppe_cap, itm_rawhide_coat, itm_khergit_armor, itm_jotnar_clan_boots_1, itm_hunter_boots, itm_leather_gloves,
     itm_sumpter_horse, itm_saddle_horse],
    def_attrib|level(14), regular_melee(14), knows_riding_1|knows_ironflesh_2|knows_horse_archery_2|knows_power_draw_3|knows_power_throw_3|knows_power_strike_2, jotnar_clan_female_young_1, jotnar_clan_female_young_2],

   ["jotnar_clan_shield_maiden", "Jotnar_Clan_Shield_Maiden", "Jotnar_Clan__Shield_Maidens", tf_female|tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild4,
    [itm_war_spear, itm_sword_viking_2, itm_sword_viking_2_small, itm_strong_bow, itm_barbed_arrows, itm_javelin, itm_throwing_axes, itm_jotnar_clan_shield_3, itm_jotnar_clan_shield_4, itm_jotnar_clan_shield_5, 
     itm_nasal_helmet, itm_nordic_helmet, itm_nasal_helmet, itm_jotnar_clan_armor_2, itm_leather_boots, itm_leather_gloves,
     itm_hunter, itm_brown_hunter],
    def_attrib|level(17), regular_melee(17), knows_riding_3|knows_ironflesh_3|knows_horse_archery_3|knows_power_draw_3|knows_power_throw_3|knows_power_strike_3, jotnar_clan_female_young_1, jotnar_clan_female_middle_2],

   ["jotnar_clan_valkyrie", "Jotnar_Clan_Valkyrie", "Jotnar_Clan_Valkyries", tf_female|tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild4,
    [itm_war_spear, itm_sword_viking_2, itm_sword_viking_2_small, itm_dblhead_axe_1, itm_strong_bow, itm_barbed_arrows, itm_jarid, itm_throwing_axes, itm_jotnar_clan_shield_3, itm_jotnar_clan_shield_4, itm_jotnar_clan_shield_5, 
     itm_nordic_helmet, itm_jotnar_clan_armor_5, itm_leather_boots, itm_leather_gloves,
     itm_hunter_c, itm_jotnar_clan_horse_1],
    def_attrib|level(20), regular_melee(20), knows_riding_4|knows_ironflesh_4|knows_horse_archery_4|knows_power_draw_3|knows_power_throw_3|knows_power_strike_3, jotnar_clan_female_middle_1, jotnar_clan_female_middle_2],

   ["jotnar_clan_disir", "Jotnar_Clan_Disir", "Jotnar_Clan_Disirs", tf_female|tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild4,
    [itm_war_spear, itm_sword_viking_3, itm_nordic_axe, itm_dblhead_axe_1, itm_strong_bow, itm_bodkin_arrows, itm_jarid, itm_throwing_axes, itm_jotnar_clan_shield_3, itm_jotnar_clan_shield_4, itm_jotnar_clan_shield_5, 
     itm_jotnar_clan_helm_6, itm_jotnar_clan_helm_7, itm_jotnar_clan_armor_6, itm_villgloves1, itm_mail_boots,
     itm_jotnar_clan_horse_2, itm_jotnar_clan_horse_3],
    def_attrib|level(23), expert_melee(23), knows_riding_5|knows_ironflesh_4|knows_horse_archery_5|knows_power_draw_5|knows_power_throw_5|knows_power_strike_5, jotnar_clan_female_middle_1, jotnar_clan_female_old_1],


# MERCENARY GUILD - SERPENT HOST
#Melee Infantry
  ["serpent_host_kapikulu", "Kapikulu", "Kapikulus", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots, no_scene, reserved, fac_sod_merc_guild5,
   [itm_pickaxe, itm_hammer, itm_hatchet, itm_hand_axe, itm_stones,
    itm_headcloth, itm_serpent_host_turban_1, itm_linen_tunic, itm_shirt, itm_coarse_tunic, itm_short_tunic, itm_hide_boots, itm_wrapping_boots, itm_ankle_boots],
   def_attrib|level(9), regular_melee(9), 0, khergit_face_young_1, khergit_face_young_2],

  ["serpent_host_cemaat", "Cemaat", "Cemaats", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild5,
   [itm_shortened_spear, itm_shortened_spear, itm_war_spear, itm_spear, itm_short_bow, itm_nomad_bow, itm_arrows, itm_barbed_arrows, itm_serpent_host_shield_round_1,
    itm_serpent_host_rabati_1, itm_steppe_armor, itm_leather_gloves, itm_hide_boots, itm_leather_boots, itm_wrapping_boots],
   def_attrib|level(12), regular_melee(12), knows_athletics_1|knows_shield_2|knows_power_strike_2|knows_power_draw_2|knows_ironflesh_2, khergit_face_young_1, khergit_face_young_2],

  ["serpent_host_athanatoi", "Athanatoi", "Athanatois", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild5,
   [itm_sword_khergit_4, itm_sword_khergit_1, itm_one_handed_war_axe_b, itm_one_handed_battle_axe_c, itm_khergit_bow, itm_strong_bow, itm_barbed_arrows, itm_serpent_host_shield_round_2,
    itm_serpent_host_helm_3, itm_serpent_host_armor_1, itm_leather_gloves, itm_leather_boots, itm_leather_boots, itm_serpent_host_boots_1],
   def_attrib|level(18), regular_all(18), knows_athletics_2|knows_shield_3|knows_power_strike_3|knows_power_draw_4|knows_ironflesh_4, khergit_face_middle_1, khergit_face_middle_2],

#Melee Cavalry (also weak in ranged)
   ["serpent_host_akinci", "Akinci", "Akincis", tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild5,
    [itm_war_spear, itm_spear, itm_short_bow, itm_nomad_bow, itm_barbed_arrows, itm_serpent_host_shield_heater_1, 
     itm_serpent_host_rabati_1, itm_steppe_armor, itm_leather_gloves, itm_leather_boots,
     itm_steppe_horse_b, itm_steppe_horse_lv],
    def_attrib|level(15), regular_melee(15), knows_riding_3|knows_ironflesh_2|knows_horse_archery_3|knows_power_draw_3|knows_power_throw_1|knows_power_strike_3, khergit_face_young_1, khergit_face_young_2],

   ["serpent_host_sipahi", "Sipahi", "Sipahi", tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild5,
    [itm_war_spear, itm_spear, itm_light_lance, itm_sword_khergit_1, itm_sword_khergit_2, itm_serpent_host_shield_heater_1, 
     itm_khergit_war_helmet, itm_khergit_helmet, itm_mail_shirt, itm_serpent_host_armor_2, itm_leather_gloves, itm_leather_boots, itm_serpent_host_boots_1, 
     itm_hunter_white, itm_hunter_white_brown],
    def_attrib|level(18), regular_melee(18), knows_riding_4|knows_ironflesh_3|knows_horse_archery_3|knows_power_draw_3|knows_power_throw_2|knows_power_strike_4, khergit_face_middle_1, khergit_face_middle_2],

   ["serpent_host_cataphract", "Cataphract", "Cataphracts", tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild5,
    [itm_war_spear, itm_spear, itm_light_lance, itm_lance, itm_sword_khergit_3, itm_sword_khergit_4, itm_serpent_host_shield_heater_1, itm_serpent_host_shield_round_2,
     itm_serpent_host_helm_2, itm_serpent_host_armor_3, itm_serpent_host_armor_4, itm_scale_gauntlets, itm_serpent_host_boots_1,
     itm_serpent_horse_5, itm_serpent_horse_6],
    def_attrib|level(23), expert_melee(23), knows_riding_5|knows_ironflesh_4|knows_horse_archery_4|knows_power_draw_4|knows_power_throw_3|knows_power_strike_5, khergit_face_middle_2, khergit_face_older_1],

#Ranged Cavalry
  ["serpent_host_timariot", "Timariot", "Timariots", tf_mounted|tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild5,
   [itm_sword_khergit_2, itm_sword_khergit_3, itm_khergit_bow, itm_khergit_arrows, itm_serpent_host_shield_round_2,
    itm_serpent_host_helm_3, itm_serpent_host_armor_1, itm_leather_gloves, itm_scale_gauntlets, itm_serpent_host_boots_1,
    itm_courser_black, itm_courser_gray],
   def_attrib|level(20), expert_archer(20), knows_riding_6|knows_ironflesh_4|knows_horse_archery_6|knows_power_draw_5, khergit_face_middle_1, khergit_face_older_2],


#BOAR CLAN MINI-GUILD (acts like honorable "bandits" on map)
  ["boar_clan_clansman", "Boar Clansman", "Boar Clansmen", tf_guarantee_armor|tf_guarantee_boots, no_scene, reserved, fac_sod_merc_guild7,
   [itm_gladiator_helmet, itm_nomad_armor, itm_coarse_tunic, itm_shirt, itm_leather_gloves, itm_black_army_leather_gloves, itm_leather_boots, itm_black_army_boot_1, 
    itm_boar_spear, itm_two_handed_battle_axe_3, itm_boar_scythe, itm_javelin, itm_tab_shield_pavise_a],
   def_attrib|level(14), regular_melee(14), knows_ironflesh_1|knows_power_strike_1|knows_power_throw_1|knows_shield_1|knows_athletics_1, boar_clan_1, boar_clan_2],

  ["boar_clan_warrior", "Boar Clan Warrior", "Boar Clan Warriors", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots, no_scene, reserved, fac_sod_merc_guild7,
   [itm_gladiator_helmet, itm_padded_mail_4, itm_leather_gloves, itm_black_army_leather_gloves, itm_mail_mittens, itm_leather_boots, itm_black_army_boot_1, itm_splinted_leather_greaves, 
    itm_maul, itm_sledgehammer, itm_warhammer, itm_mace_5, itm_spikepolehammer1, itm_two_handed_battle_axe_3, itm_great_bardiche, itm_boar_scythe, itm_shield_heater_boar],
   def_attrib|level(17), regular_melee(17), knows_ironflesh_3|knows_power_strike_3|knows_shield_3|knows_athletics_3, boar_clan_1, boar_clan_2],

  ["boar_clan_vet_warrior", "Boar Clan Veteran Warrior", "Boar Clan Veteran Warriors", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild7,
   [itm_gladiator_mask, itm_heraldic_banded_armor, itm_heraldic_cuir_bouilli, itm_leather_gloves, itm_black_army_leather_gloves, itm_mail_mittens, itm_leather_boots, itm_black_army_boot_1, itm_splinted_leather_greaves, 
    itm_maul, itm_sledgehammer, itm_warhammer, itm_mace_5, itm_spikepolehammer1, itm_two_handed_battle_axe_3, itm_great_bardiche, itm_boar_scythe, itm_shield_heater_boar, itm_tab_shield_pavise_b, itm_tab_shield_pavise_c, itm_tab_shield_pavise_d],
   def_attrib|level(23), regular_melee(23), knows_ironflesh_4|knows_power_strike_5|knows_shield_4|knows_athletics_4, boar_clan_1, boar_clan_2],

  ["boar_clan_rider", "Boar Clan Rider", "Boar Clan Riders", tf_mounted|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild7,
   [itm_gladiator_helmet, itm_padded_mail_4, itm_leather_gloves, itm_black_army_leather_gloves, itm_mail_mittens, itm_leather_boots, itm_black_army_boot_1, itm_splinted_leather_greaves, itm_shield_heater_boar, 
    itm_military_fork_1, itm_battle_fork_1, itm_trident_1, itm_camel_1, itm_camel_2],
   def_attrib|level(18), regular_melee(18), knows_riding_3|knows_ironflesh_2|knows_power_strike_3, boar_clan_1, boar_clan_2],

  ["boar_clan_vet_rider", "Boar Clan Veteran Rider", "Boar Clan Veteran Riders", tf_mounted|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild7,
   [itm_gladiator_mask, itm_heraldic_mail_with_tabard, itm_heraldic_mail_with_surcoat, itm_leather_gloves, itm_black_army_leather_gloves, itm_mail_mittens, itm_leather_boots, itm_black_army_boot_1, itm_splinted_leather_greaves, itm_shield_heater_boar, itm_tab_shield_round_c, itm_tab_shield_round_d, 
    itm_military_fork_1, itm_battle_fork_1, itm_trident_1, itm_war_camel_1, itm_war_camel_2],
   def_attrib|level(24), regular_melee(24), knows_riding_5|knows_ironflesh_3|knows_power_strike_4, boar_clan_1, boar_clan_2],

   
# MERCENARY GUILD - SLAVERS
#Melee Infantry / Cavalry
  ["henchman", "Henchman", "Henchmen", tf_guarantee_armor, no_scene, reserved, fac_sod_merc_guild6,
   [itm_spiked_mace, itm_wooden_stick, itm_cudgel, itm_hammer, itm_practice_sword, itm_heavy_practice_sword, itm_club, itm_staff, itm_stones, itm_slaver_shield_round_hide, itm_slaver_shield_kite_hide,
    itm_woolen_cap, itm_fur_hat_scarf, itm_rawhide_coat, itm_coarse_tunic, itm_nomad_armor, itm_nomad_boots, itm_wrapping_boots,
    itm_sumpter_horse],
   def_attrib|level(9), regular_melee(9), 0, bandit_face1, bandit_face2],

  ["slave_driver", "Slave Driver", "Slave Drivers", tf_guarantee_armor|tf_guarantee_boots, no_scene, reserved, fac_sod_merc_guild6,
   [itm_spiked_mace, itm_mace_1, itm_mace_2, itm_staff, itm_polehammer2, itm_quarter_staff, itm_throwing_hammers1, itm_throwing_hammers2, itm_slaver_shield_round_hide, itm_slaver_shield_kite_hide,
    itm_fur_hat_scarf, itm_felt_hat, itm_woolen_cap, itm_rawhide_coat, itm_coarse_tunic, itm_nomad_armor, itm_nomad_boots, itm_wrapping_boots, itm_leather_gloves,
    itm_saddle_horse, itm_sumpter_horse],
   def_attrib|level(14), regular_melee(14), 0, bandit_face1, bandit_face2],

  ["slave_hunter", "Slave Hunter", "Slave Hunters", tf_mounted|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_horse, no_scene, reserved, fac_sod_merc_guild6,
   [itm_winged_mace, itm_mace_6, itm_spiked_mace, itm_quarter_staff, itm_iron_staff, itm_throwing_hammers1, itm_throwing_hammers2, itm_slaver_shield_round_hide, itm_slaver_shield_kite_hide,
    itm_leather_warrior_cap, itm_skullcap, itm_padded_leather2, itm_padded_leather3, itm_leather_armor, itm_leather_boots, itm_leather_gloves,
    itm_saddle_horse, itm_rok_saddle_horse2],
   def_attrib|level(18), regular_melee(18), knows_riding_1|knows_power_throw_1|knows_power_strike_1, bandit_face1, bandit_face2],

  ["slave_crusher", "Slave Crusher", "Slave Crushers", tf_mounted|tf_guarantee_armor|tf_guarantee_boots|tf_guarantee_helmet|tf_guarantee_horse, no_scene, reserved, fac_sod_merc_guild6,
   [itm_mace_7, itm_mace_6, itm_mace_4, itm_iron_staff, itm_arena_lance, itm_throwing_military_hammers, itm_slaver_shield_kite,
    itm_iron_skull_mask, itm_skull_helm1, itm_skull_helm2, itm_padded_mail_3, itm_padded_mail_2, itm_nomad_boots, itm_leather_boots, itm_leather_gloves,
    itm_hunter, itm_brown_hunter, itm_hunting_horse_seven],
   def_attrib|level(22), regular_melee(22), knows_riding_3|knows_horse_archery_1|knows_power_throw_2|knows_power_strike_2, bandit_face1, bandit_face2],

  ["slave_master", "Slave Master", "Slave Masters", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse, no_scene, reserved, fac_sod_merc_guild6,
   [itm_twohandedmace, itm_warhammer, itm_arena_lance, itm_jousting_lance, itm_throwing_military_hammers, itm_dragonshield, itm_steel_shield,
    itm_horned_helm1, itm_horned_helm2, itm_horned_helm3, itm_dark_plate2, itm_breast_plate_mail5, itm_mail_boots, itm_mail_mittens,
    itm_charger, itm_warhorse_black, itm_charger_black],
   def_attrib|level(26), regular_melee(26), knows_riding_4|knows_horse_archery_2|knows_power_throw_3|knows_power_strike_3|knows_shield_2|knows_athletics_2, bandit_face1, bandit_face2],


#RANDOM MERCENARIES
  ["ronin", "Ronin", "Ronin", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_boots, no_scene, reserved, fac_commoners,
   [itm_strange_sword, itm_strange_great_sword, itm_strange_short_sword, itm_kanobou_iron_stud_ring, itm_kanobou_wood_stud_ring, itm_strange_helmet, itm_strange_armor, itm_leather_gloves, itm_strange_boots],
   def_attrib|level(28), expert_melee(28), knows_athletics_6|knows_power_strike_7|knows_weapon_master_7|knows_ironflesh_7, khergit_face_younger_1, khergit_face_old_2],

  ["ashkolon_knight", "Knight of Ashkolon", "Knights of Ashkolon", tf_mounted|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_commoners,
   [itm_brasshelm, itm_brassarmor, itm_brassgauntlets, itm_brassboots, itm_jomsviking_shield, itm_jomsviking_axe, itm_throwing_axes, itm_scorpioncharger, itm_goldbaseblackorament],
   def_attrib|level(18), regular_melee(18), knows_riding_3|knows_ironflesh_2|knows_power_strike_2|knows_power_throw_2|knows_athletics_1|knows_tactics_2, nord_face_middle_1, nord_face_middle_2],

  ["rus_champion", "Rus Champion", "Rus Champions", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots, no_scene, reserved, fac_commoners,
   [itm_rus_helmet_a, itm_mail_and_plate, itm_mail_boots, itm_mail_mittens, 
    itm_sword_viking_3, itm_nordic_sword, itm_realpiked, itm_realhalberdb, itm_realhalberdd, itm_norman_shield_3, itm_norman_shield_8, itm_norman_shield_6, itm_norman_shield_7, itm_norman_shield_1],
   def_attrib|level(23), regular_melee(23), knows_ironflesh_4|knows_power_strike_3|knows_athletics_3, nord_face_middle_1, nord_face_middle_2],

   ["shining_eagles", "Shining Eagle", "Shining Eagles", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots, no_scene, reserved, fac_commoners,
   [itm_eaglehelm, itm_eagleplate, itm_eaglegauntlets, itm_eagleboots, itm_realhalberdf, itm_small_pole_axe],
   def_attrib|level(20), weak_melee(18), knows_ironflesh_2|knows_power_strike_3|knows_athletics_3|knows_tactics_2, swadian_face_younger_1, swadian_face_middle_2], 
   #This unit has great armor so level is set intentionally higher than proficiency to cost more and not be over powered for price

   ["heraldic_knight", "Heraldic Knight", "Heraldic Knights", tf_mounted|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_commoners,
   [itm_plain_great_helm, itm_great_helmet_master, itm_pigface, itm_talak_great_helm, itm_great_helmet, itm_dullhelm, itm_heraldic_mail_with_tabard, itm_heraldic_mail_with_surcoat, itm_mail_mittens, itm_splinted_leather_greaves, itm_mail_boots, itm_tab_shield_heater_c, itm_tab_shield_heater_cav_a, itm_tab_shield_kite_cav_b, itm_heavy_lance, itm_lance, itm_light_lance, itm_bastard_sword_b, itm_morningstar, itm_sword_medieval_c, itm_warhorse_sc2_rtw3, itm_warhorse_sc2_rtw2, itm_warhorse_po1_rtw3, itm_warhorse_po2_rtw3, itm_warhorse_maw_b08, itm_warhorse_maw_b05, itm_warhorse_hre_rtw3, itm_warhorse_den_rtw2, itm_warhorse_b],
   def_attrib|level(20), regular_melee(20), knows_riding_5|knows_ironflesh_2|knows_power_strike_3|knows_athletics_2, mercenary_face_1, mercenary_face_2],

  ["black_khergit_horseman", "Black Khergit Horseman", "Black Khergit Horsemen", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse, 0, 0, fac_black_khergits,
   [itm_khergit_bow, itm_nomad_bow, itm_arrows, itm_khergit_arrows, itm_sword_khergit_2, itm_scimitar, itm_winged_mace, itm_spear, itm_lance, itm_plate_covered_round_shield,
    itm_steppe_cap, itm_helmet_fur_a, itm_khergit_war_helmet, itm_khergit_war_helmet, itm_lamellar_armor, itm_mail_hauberk, itm_hide_boots, 
    itm_saddle_horse, itm_steppe_horse],
   def_attrib|level(21), regular_melee(21), knows_riding_3|knows_ironflesh_3|knows_horse_archery_3|knows_power_draw_3|knows_power_strike_2, khergit_face_young_1, khergit_face_old_2],

  ["black_khergit_guard", "Black Khergit Guard", "Black Khergit Guards", tf_mounted|tf_guarantee_ranged|tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_horse, 0, 0, fac_black_khergits,
   [itm_khergit_bow, itm_arrows, itm_khergit_arrows, itm_sword_khergit_1, itm_scimitar, itm_winged_mace, itm_lance, itm_tab_shield_round_e, itm_tab_shield_round_d, itm_tab_shield_round_c, 
    itm_khergit_guard_helmet, itm_khergit_cavalry_helmet, itm_khergit_guard_armor, itm_khergit_guard_boots, 
    itm_steppe_horse_lv, itm_steppe_horse_b, itm_hunter],
   def_attrib|level(25), regular_melee(25), knows_riding_6|knows_ironflesh_4|knows_horse_archery_6|knows_power_draw_6, khergit_face_middle_1, khergit_face_old_2],

  ["ief_sons_of_deer", "Sons of Deer", "Sons of Deer", tf_mounted|tf_guarantee_ranged|tf_guarantee_horse|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots, 0, 0, fac_kingdom_6,
   [itm_strong_bow, itm_khergit_bow, itm_khergit_arrows, itm_barbed_arrows, itm_sword_khergit_2, itm_sword_khergit_3, itm_sword_khergit_4, itm_one_handed_war_axe_a, itm_one_handed_war_axe_b, itm_tab_shield_round_b, itm_tab_shield_round_c, 
    itm_legion_helm_06, itm_legion_helm_07, itm_dvor_lamellar1, itm_dvor_lamellar2, itm_black_army_leather_gloves, itm_black_army_boot_1, itm_hide_boots,
    itm_legion_horse_2, itm_legion_horse_1],
   def_attrib|level(23), expert_archer(23)|weak_melee(23), knows_riding_4|knows_horse_archery_6|knows_power_draw_4|knows_shield_1|knows_ironflesh_1, khergit_face_middle_1, khergit_face_older_2],
   #This unit is a mercenary for the Imperial Expeditionary Force but located here so it will also randomly show up in taverns

  ["ief_bastard_brothers", "Bastard Brothers", "Bastard Brothers", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_boots, 0, 0, fac_kingdom_6,
   [itm_iron_helm, itm_mail_mittens, itm_mail_boots, itm_mail_chausses, 
    itm_heraldic_haubergeon, itm_heraldic_mail_shirt, itm_heraldic_mail_hauberk, itm_heraldic_brigandine_a, itm_heraldic_mail_with_tabard, itm_heraldic_mail_with_surcoat, itm_heraldic_banded_armor, itm_heraldic_cuir_bouilli, itm_heraldic_plate_armor, 
    itm_bastard_sword_a, itm_bastard_sword_b, itm_talak_bastard_sword, itm_raider_battle_axe, itm_nordic_axe, itm_club_with_spike_head, itm_tab_shield_pavise_c, itm_tab_shield_round_c, itm_tab_shield_kite_c, itm_tab_shield_heater_c],
   def_attrib|level(25), expert_melee(25), knows_ironflesh_4|knows_power_strike_5|knows_athletics_4, rhodok_face_young_1, rhodok_face_middle_2],
   #This unit is a mercenary for the Imperial Expeditionary Force but located here so it will also randomly show up in taverns

  ["hand_cannonier", "Hand Cannonier", "Hand Cannoniers", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_ranged, no_scene, reserved, fac_commoners,
   [itm_musket_1, itm_cartridges, itm_cartridges, itm_sword_khergit_1, itm_sword_khergit_2, itm_sword_khergit_3, 
    itm_zerrikanian_noble_helmet, itm_nobleman_outfit6, itm_leather_boots],
   def_attrib|level(17), weak_melee(17)|wp_firearm(170), knows_ironflesh_2|knows_power_strike_1|knows_athletics_2, mercenary_face_1, mercenary_face_2],


#MERCENARY TROOPS END    MERCENARY TROOPS END     MERCENARY TROOPS END     MERCENARY TROOPS END     MERCENARY TROOPS END     MERCENARY TROOPS END     MERCENARY TROOPS END     
#Troops placed between "MERCENARY TROOPS BEGIN" and "MERCENARY TROOPS END" will randomly spawn in taverns

  ["mercenaries_end", "mercenaries_end", "mercenaries_end", 0, no_scene, reserved, fac_commoners,
   [],
   def_attrib|level(4), regular_melee(4), 0, mercenary_face_1, mercenary_face_2],

#Black Army Special Unit (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["black_army_raven_captain", "Black Army Raven Captain", "Black Army Raven Captains", tf_mounted|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield|tf_guarantee_horse, no_scene, reserved, fac_sod_merc_guild1,
   [itm_great_lanceb, itm_great_lancec, itm_arena_lance, itm_iron_staff, itm_katzbalger, itm_realbastarde, itm_talak_warhammer, itm_talak_mace, itm_morningstar, itm_one_handed_battle_axe_c, itm_fighting_axe, itm_light_crossbow, itm_light_crossbow, itm_steel_bolts, itm_steel_bolts, itm_flintlock_pistol, itm_cartridges, itm_black_army_shield_2,
    itm_black_helmet, itm_black_general_helm, itm_black_armor, itm_black_greaves, itm_darkboots, itm_darkgauntlets,
    itm_warhorse_black, itm_charger_black],
   def_attrib|level(25), expert_melee(25)|wp_firearm(200), knows_riding_5|knows_horse_archery_6|knows_power_strike_5|knows_shield_4|knows_athletics_3, mercenary_face_1, mercenary_face_2],

#Black Army Scene Units
  ["black_army_walker_1", "Black Army Prospect", "Black Army Prospects", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild1,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_hand_axe, itm_one_handed_war_axe_a, itm_winged_mace, itm_spiked_mace, itm_hunting_crossbow, itm_bolts, itm_black_army_shield_1,
    itm_black_army_armor_1, itm_leather_boots, itm_black_army_boot_1, itm_black_army_leather_gloves],
   def_attrib|level(5), regular_melee(5), knows_shield_1, mercenary_face_1, mercenary_face_2],

  ["black_army_castle_guard_1", "Castle Guard", "Castle Guards", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild1,
   [itm_great_lanceb, itm_great_lancec, itm_arena_lance, itm_iron_staff, itm_jarid, itm_throwing_axes, itm_katzbalger, itm_realbastarde, itm_talak_warhammer, itm_morningstar, itm_one_handed_battle_axe_c, itm_fighting_axe, itm_light_crossbow, itm_steel_bolts, itm_strong_bow, itm_bodkin_arrows, itm_flintlock_pistol, itm_cartridges, itm_black_army_shield_2,
    itm_black_helmet, itm_black_armor, itm_black_greaves, itm_darkboots, itm_darkgauntlets],
   def_attrib|level(25), expert_melee(25)|wp_firearm(200), knows_riding_5|knows_horse_archery_6|knows_power_strike_5|knows_shield_4|knows_athletics_3, mercenary_face_1, mercenary_face_2],

#Black Army Others
  ["black_army_rep_1", "Black Army Emissary", "Black Army Emissary", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, 0, reserved, fac_sod_merc_guild1, 
    [itm_katzbalger, itm_tab_shield_pavise_d,
    itm_black_army_helm_4, itm_heraldic_mail_with_surcoat, itm_mail_boots, itm_mail_mittens,
    itm_warhorse_black],
   def_attrib|level(15), expert_melee(15), knows_riding_4|knows_power_strike_4|knows_shield_3|knows_athletics_2|knows_tactics_1|knows_leadership_1, 0x000000093f043194653ab2ab1b92b09300000000001e425b0000000000000000],

   ["black_army_deserter_1", "Black Army Line Crusher Deserter", "Black Army Line Crusher Deserters", tf_guarantee_horse|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_deserters,
    [itm_falchion, itm_bastard_sword_a, itm_talak_bastard_sword, itm_black_army_shield_1, itm_black_army_shield_2, 
     itm_black_army_helm_3, itm_black_army_armor_1, itm_black_army_armor_2, itm_black_army_boot_1, itm_black_army_leather_gloves,
     itm_hunter, itm_brown_hunter, itm_hunting_horse_seven],
    def_attrib|level(12), regular_melee(12), knows_riding_3|knows_ironflesh_2|knows_horse_archery_3|knows_power_strike_3, mercenary_face_1, mercenary_face_2],


#Boar Clan Special Unit (have to move outside "mercenaries_end" so they will not spawn in taverns)
   ["boar_clan_tusk_rider", "Boar Clan Tusk Rider", "Boar Clan Tusk Riders", tf_mounted|tf_guarantee_ranged|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_horse, no_scene, reserved, fac_sod_merc_guild7,
   [itm_gladiator_mask, itm_heraldic_banded_armor, itm_heraldic_cuir_bouilli, itm_mail_mittens, itm_mail_boots, itm_shield_heater_boar, itm_tab_shield_round_c, itm_tab_shield_round_d, 
    itm_strong_bow, itm_khergit_bow, itm_khergit_arrows, itm_khergit_arrows, itm_battle_fork_1, itm_maul, itm_sledgehammer, itm_saddleless_hunter_1, itm_saddleless_hunter_2],
   def_attrib|level(26), expert_archer(26), knows_riding_6|knows_ironflesh_3|knows_athletics_2|knows_horse_archery_8|knows_power_draw_7|knows_power_strike_3, boar_clan_1, boar_clan_2],

#Boar Clan Others
   ["boar_clan_representative", "Boar Clan Messenger", "Boar Clan Messenger", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, 0, reserved, fac_sod_merc_guild7,
   [itm_gladiator_helmet, itm_heraldic_mail_with_surcoat, itm_black_army_leather_gloves, itm_black_army_boot_1, itm_shield_heater_boar, 
    itm_battle_fork_1, itm_mace_5, itm_war_camel_2],
   def_attrib|level(15), expert_melee(15), knows_riding_4|knows_power_strike_4|knows_shield_3|knows_athletics_2|knows_tactics_1|knows_leadership_1, boar_clan_1, boar_clan_2],


#Conquistador Special Unit (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["conquistador_lancer", "Conquistador Lancer", "Conquistador Lancers", tf_mounted|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield|tf_guarantee_horse, no_scene, reserved, fac_sod_merc_guild2,
   [itm_great_lanceb, itm_great_lancec, itm_sword_medieval_b_small, itm_tab_shield_kite_cav_b, itm_tab_shield_heater_cav_b, 
    itm_conquistador_helm3, itm_conquistador_plate_1, itm_conquistador_plate_2, itm_iron_greaves, itm_gauntlets,
    itm_conquistador_horse_1, itm_conquistador_horse_2],
   def_attrib|level(25), expert_melee(25), knows_riding_5|knows_power_strike_5|knows_shield_4|knows_athletics_3, mercenary_face_1, mercenary_face_2],

#Conquistador Scene Units
  ["conquistador_walker_1", "Conquistador Immigrant", "Conquistador Immigrants", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild2,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_buckler_1,
    itm_light_leather, itm_light_leather_boots, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(10), regular_melee(10), knows_athletics_1, mercenary_face_1, mercenary_face_2],

  ["conquistador_walker_2", "Conquistador Immigrant", "Conquistador Immigrants", tf_female|tf_guarantee_armor, 0, 0, fac_sod_merc_guild2,
   [itm_bolts, itm_light_crossbow, itm_short_bow, itm_crossbow, itm_buckler_1, itm_hatchet, itm_hand_axe, itm_voulge, itm_fighting_pick, itm_club, itm_dress, itm_woolen_dress, itm_wrapping_boots],
   def_attrib|level(5), regular_melee(5), 0, refugee_face1, refugee_face2],

  ["conquistador_castle_guard_1", "Castle Guard", "Castle Guards", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild2,
   [itm_great_lanceb, itm_great_lancec, itm_sword_medieval_b_small, itm_tab_shield_kite_cav_b, itm_tab_shield_heater_cav_b, 
    itm_conquistador_helm3, itm_conquistador_plate_1, itm_conquistador_plate_2, itm_iron_greaves, itm_gauntlets],
   def_attrib|level(25), expert_melee(25), knows_riding_5|knows_power_strike_5|knows_shield_4|knows_athletics_3, mercenary_face_1, mercenary_face_2],

#Conquistador Others
  ["conquistador_rep_1", "Conquistador Ambassador", "Conquistador Ambassador", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, 0, reserved, fac_sod_merc_guild2, 
    [itm_sword_medieval_b_small, itm_tab_shield_heater_d,
    itm_conquistador_helm3, itm_heraldic_mail_with_surcoat, itm_mail_boots, itm_mail_mittens,
    itm_conquistador_horse_2],
   def_attrib|level(15), expert_melee(15), knows_riding_4|knows_power_strike_4|knows_shield_3|knows_athletics_2|knows_tactics_1|knows_leadership_1, 0x00000009340c250846d18a56e551d75100000000001e6b630000000000000000],

   ["conquistador_deserter_1", "Conquistador Swordsman Deserter", "Conquistador Swordsman Deserters", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_shield, 0, 0, fac_deserters,
   [itm_sword_medieval_b_small, itm_sword_medieval_c_small, itm_buckler_1, itm_buckler_2,
    itm_conquistador_helm1, itm_mail_shirt, itm_mail_hauberk, itm_splinted_leather_greaves, itm_mail_chausses, itm_leather_gloves],
   def_attrib|level(18), regular_melee(18), knows_athletics_3|knows_power_strike_2|knows_ironflesh_2|knows_shield_3, mercenary_face_1, mercenary_face_2],


#Elephant Guard Special Unit (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["elephant_guard_battle_shaman", "Battle Shaman", "Battle Shammans", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_sod_merc_guild3,
   [itm_elephant_guard_sickle_2, itm_elephant_heater_3, itm_throwing_daggers, itm_throwing_daggers,
    itm_elephant_guard_shaman_helm, itm_elephant_guard_shaman_body_1, itm_elephant_guard_shaman_body_2, itm_elephant_guard_gloves, itm_elephant_guard_shaman_boots],
   def_attrib|level(25), expert_all(27), knows_athletics_8|knows_shield_10|knows_power_strike_7|knows_power_throw_7|knows_ironflesh_7|knows_surgery_2|knows_first_aid_2|knows_wound_treatment_2, elephant_guard_shaman_1, elephant_guard_shaman_2],

#Elephant Guard Scene Units
  ["elephant_guard_walker_1", "Elephant Guard Villager", "Elephant Guard Villagers", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild3,
   [itm_elephant_tribe_two_side_spear, itm_sickle, itm_stones, itm_elephant_hide_round_shield_1, itm_elephant_guard_tribesman_body_01, itm_elephant_guard_tribesman_body_02, itm_leather_boots, itm_hide_boots, itm_leather_gloves],
   def_attrib|level(8), regular_melee(8), knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_power_throw_3|knows_ironflesh_3, elephant_guard_face_young_1, elephant_guard_face_young_2],

  ["elephant_guard_walker_2", "Elephant Guard Villager", "Elephant Guard Villagers", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild3,
   [itm_elephant_tribe_two_side_spear, itm_sickle, itm_stones, itm_elephant_kite_hide_2, itm_elephant_guard_tribesman_body_09, itm_elephant_guard_tribesman_body_10, itm_leather_boots, itm_hide_boots, itm_leather_gloves],
   def_attrib|level(8), regular_melee(8), knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_power_throw_3|knows_ironflesh_3, elephant_guard_face_young_5, elephant_guard_face_young_6],

  ["elephant_guard_castle_guard_1", "Town Guard", "Town Guards", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_sod_merc_guild3,
   [itm_elephant_guard_sickle_2, itm_elephant_heater_3, itm_throwing_daggers, itm_throwing_daggers,
    itm_elephant_guard_shaman_helm, itm_elephant_guard_shaman_body_1, itm_elephant_guard_shaman_body_2, itm_elephant_guard_gloves, itm_elephant_guard_shaman_boots],
   def_attrib|level(25), expert_all(27), knows_athletics_7|knows_shield_7|knows_power_strike_7|knows_power_throw_7|knows_ironflesh_7, elephant_guard_shaman_1, elephant_guard_shaman_2],

#Elephant Guard Others
  ["elephant_guard_rep_1", "Elephant Guard Delegate", "Elephant Guard Delegate", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, 0, reserved, fac_sod_merc_guild3, 
    [itm_throwing_spear, itm_elephant_guard_sickle_2, itm_tab_shield_round_d,
    itm_elephant_guard_helm_1, itm_elephant_guard_tribesman_body_12, itm_elephant_guard_gloves, itm_nobleman_greaves],
   def_attrib|level(15), expert_all(15), knows_power_strike_3|knows_power_throw_3|knows_shield_3|knows_athletics_3|knows_tactics_1|knows_leadership_1, elephant_guard_face_young_1, elephant_guard_face_middle_4],

   ["elephant_guard_deserter_1", "Elephant Guard Warrior Deserter", "Elephant Guard Warrior Deserters", tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_shield, 0, 0, fac_deserters,
   [itm_elephant_tribe_two_side_spear, itm_elephant_guard_sickle_1, itm_throwing_knives, itm_elephant_hide_round_shield_2, itm_elephant_guard_helm_2, itm_elephant_guard_tribesman_body_05, itm_elephant_guard_tribesman_body_06, itm_nobleman_greaves, itm_leather_gloves],
   def_attrib|level(18), regular_melee(18), knows_athletics_5|knows_shield_5|knows_power_strike_5|knows_power_throw_4|knows_ironflesh_5, elephant_guard_face_middle_1, elephant_guard_face_middle_2],


#Jotnar Clan Special Unit (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["jotnar_clan_norn_mistress", "Jotnar_Clan_Norn_Mistress", "Jotnar_Clan_Norn_Mistresses", tf_female|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild4,
   [itm_espadona, itm_dblhead_axe_2, itm_mountainlordsword, itm_long_bow, itm_bodkin_arrows, itm_jarid, itm_throwing_axes, itm_throwing_daggers, 
    itm_jotnar_clan_helm_8, itm_jotnar_clan_armor_7, itm_jotnar_clan_armor_8, itm_mail_boots, itm_mail_mittens],
   def_attrib|level(25), expert_melee(25), knows_athletics_5|knows_power_strike_5|knows_power_draw_5|knows_power_throw_5|knows_ironflesh_3, jotnar_clan_female_middle_1, jotnar_clan_female_middle_2],

#Jotnar Clan Scene Units
  ["jotnar_clan_walker_1", "Jotnar Clan Recruit", "Jotnar Clan Recruits", tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_sod_merc_guild4,
   [itm_battle_axe, itm_two_handed_axe, itm_two_handed_battle_axe_2, itm_realbastarda, itm_hand_axe, itm_one_handed_war_axe_a, itm_one_handed_war_axe_b, itm_jotnar_clan_shield_2, 
   itm_khergit_armor, itm_rawhide_coat, itm_jotnar_clan_boots_1, itm_hunter_boots, itm_leather_gloves],
   def_attrib|level(9), regular_melee(9), knows_athletics_1|knows_shield_1|knows_power_strike_1|knows_power_throw_1|knows_ironflesh_1, nord_face_young_1, nord_face_young_2],

  ["jotnar_clan_walker_2", "Jotnar Clan Recruit", "Jotnar Clan Recruits", tf_female|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild4,
    [itm_war_spear, itm_sword_viking_1, itm_strong_bow, itm_arrows, itm_javelin, itm_throwing_axes, itm_jotnar_clan_shield_1,
     itm_rawhide_coat, itm_khergit_armor, itm_jotnar_clan_boots_1, itm_hunter_boots, itm_leather_gloves],
    def_attrib|level(10), regular_melee(10), knows_riding_1|knows_ironflesh_2|knows_horse_archery_1|knows_power_draw_1|knows_power_throw_2|knows_power_strike_2, jotnar_clan_female_young_1, jotnar_clan_female_young_2],

  ["jotnar_clan_castle_guard_1", "Castle Guard", "Castle Guards", tf_female|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild4,
   [itm_espadona, itm_dblhead_axe_2, itm_mountainlordsword, itm_long_bow, itm_bodkin_arrows, itm_jarid, itm_throwing_axes, itm_throwing_daggers, 
    itm_jotnar_clan_helm_8, itm_jotnar_clan_armor_7, itm_jotnar_clan_armor_8, itm_mail_boots, itm_mail_mittens],
   def_attrib|level(25), expert_melee(25), knows_athletics_5|knows_power_strike_5|knows_power_draw_5|knows_power_throw_5|knows_ironflesh_3, jotnar_clan_female_middle_1, jotnar_clan_female_middle_2],

#Jotnar Clan Others
  ["jotnar_clan_rep_1", "Jotnar Clan Envoy", "Jotnar Clan Envoy", tf_female|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, 0, reserved, fac_sod_merc_guild4, 
   [itm_dblhead_axe_1, itm_tab_shield_kite_d, itm_long_bow, itm_bodkin_arrows, 
    itm_jotnar_clan_helm_9, itm_heraldic_mail_with_surcoat, itm_mail_boots, itm_mail_mittens,
    itm_jotnar_clan_horse_2],
   def_attrib|level(15), expert_melee(15), knows_riding_4|knows_power_strike_4|knows_shield_4|knows_athletics_2|knows_tactics_1|knows_leadership_1, 0x0000000bed00c00136db6db6db6db6db00000000001db6db0000000000000000],

   ["jotnar_clan_deserter_1", "Jotnar Clan Jarl Deserter", "Jotnar Clan Jarl Deserters", tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves, 0, 0, fac_deserters,
   [itm_battle_axe, itm_two_handed_axe, itm_two_handed_battle_axe_2, itm_realbastarde, 
   itm_jotnar_clan_helm_2, itm_nordic_helmet, itm_jotnar_clan_armor_1, itm_mail_shirt, itm_mail_hauberk, itm_mail_boots, itm_mail_mittens],
   def_attrib|level(16), regular_melee(16), knows_athletics_3|knows_shield_2|knows_power_strike_3|knows_power_throw_2|knows_ironflesh_2, nord_face_young_1, nord_face_young_2],



#Serpent Host Special Unit (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["serpent_host_basilisk_knight", "Basilisk_Knight", "Basilisk_Knights", tf_mounted|tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild5,
   [itm_cimitar, itm_khergit_bow, itm_strong_bow, itm_khergit_arrows, itm_khergit_arrows, 
    itm_serpent_host_helm_1, itm_serpent_host_armor_5, itm_serpent_host_armor_6, itm_scale_gauntlets, itm_serpent_host_boots_1,
    itm_serpent_horse_7, itm_serpent_horse_8],
   def_attrib|level(25), expert_archer(25), knows_riding_6|knows_ironflesh_5|knows_athletics_3|knows_horse_archery_7|knows_power_draw_7, khergit_face_middle_1, khergit_face_older_2],

#Serpent Host Scene Units
  ["serpent_host_walker_1", "Serpent Host Refugee", "Serpent Host Refugees", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots, no_scene, reserved, fac_sod_merc_guild5,
   [itm_pickaxe, itm_hammer, itm_hatchet, itm_hand_axe, itm_stones,
    itm_headcloth, itm_serpent_host_turban_1, itm_linen_tunic, itm_shirt, itm_coarse_tunic, itm_short_tunic, itm_hide_boots, itm_wrapping_boots, itm_ankle_boots],
   def_attrib|level(8), regular_melee(8), 0, khergit_face_young_1, khergit_face_young_2],

  ["serpent_host_castle_guard_1", "Castle Guard", "Castle Guards", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_sod_merc_guild5,
   [itm_cimitar, itm_khergit_bow, itm_strong_bow, itm_khergit_arrows, itm_khergit_arrows, 
    itm_serpent_host_helm_1, itm_serpent_host_armor_5, itm_serpent_host_armor_6, itm_scale_gauntlets, itm_serpent_host_boots_1],
   def_attrib|level(25), expert_archer(25), knows_riding_6|knows_ironflesh_5|knows_athletics_3|knows_horse_archery_7|knows_power_draw_7, khergit_face_middle_1, khergit_face_older_2],

#Serpent Host Others
  ["serpent_host_rep_1", "Serpent Host Diplomat", "Serpent Host Diplomat", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, 0, reserved, fac_sod_merc_guild5, 
    [itm_khergit_bow, itm_khergit_arrows, itm_sword_khergit_1, itm_tab_shield_small_round_a,
    itm_khergit_war_helmet, itm_heraldic_mail_with_surcoat, itm_mail_boots, itm_mail_mittens,
    itm_serpent_horse_7],
   def_attrib|level(15), expert_archer(15), knows_riding_4|knows_horse_archery_4|knows_power_draw_6|knows_shield_2|knows_tactics_1|knows_leadership_1, 0x00000005bf0c438a12178d9714bb224b00000000001da4bb0000000000000000],

   ["serpent_host_deserter_1", "Serpent Host Timariot Deserter", "Serpent Host Timariot Deserters", tf_mounted|tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_deserters,
   [itm_sword_khergit_2, itm_sword_khergit_3, itm_khergit_bow, itm_khergit_arrows, itm_serpent_host_shield_round_2,
    itm_serpent_host_helm_3, itm_serpent_host_armor_1, itm_leather_gloves, itm_scale_gauntlets, itm_serpent_host_boots_1,
    itm_courser_black, itm_courser_gray],
   def_attrib|level(20), expert_archer(20), knows_riding_6|knows_ironflesh_4|knows_horse_archery_6|knows_power_draw_5, khergit_face_middle_1, khergit_face_older_2],


#Slaver Special Units (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["slave", "Slave", "Slaves", tf_guarantee_helmet, 0, 0, fac_commoners,
   [itm_cudgel, itm_wooden_stick, itm_club, itm_stones, itm_slave_neck_chain],
   def_attrib|level(2), weak_melee(2), 0, slave_1,slave_2],

  ["slave_female", "Slave", "Slaves", tf_female|tf_guarantee_helmet, 0, 0, fac_commoners,
   [itm_cudgel, itm_wooden_stick, itm_club, itm_stones, itm_slave_neck_chain],
   def_attrib|level(2), weak_melee(2), 0, slave_female_1,slave_female_2],

  ["tormenter", "Tormenter", "Tormenters", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_sod_merc_guild6,
   [itm_kanobou_iron_spike_ring, itm_kanobou_wood_spike_ring, itm_kanobou_iron_stud_ring, itm_kanobou_wood_stud_ring,
    itm_slaver_helm_5, itm_slaver_helm_6, itm_slaver_helm_7, itm_slaver_armor_6, itm_slaver_armor_7, itm_iron_greaves, itm_gauntlets],
   def_attrib|level(26), expert_melee(26), knows_trade_3|knows_ironflesh_3|knows_weapon_master_3|knows_power_strike_5|knows_athletics_5, bandit_face1, bandit_face2],

#Slaver Scene Units
  ["slaver_walker_1", "Slaver Henchman", "Slaver Henchmen", tf_guarantee_armor, no_scene, reserved, fac_sod_merc_guild6,
   [itm_spiked_mace, itm_wooden_stick, itm_cudgel, itm_hammer, itm_practice_sword, itm_heavy_practice_sword, itm_club, itm_staff, itm_stones, itm_slaver_shield_round_hide, itm_slaver_shield_kite_hide,
    itm_woolen_cap, itm_fur_hat_scarf, itm_rawhide_coat, itm_coarse_tunic, itm_nomad_armor, itm_nomad_boots, itm_wrapping_boots,
    itm_sumpter_horse],
   def_attrib|level(8), regular_melee(8), 0, bandit_face1, bandit_face2],

  ["slave_prisoner_1", "Slave", "Slaves", tf_guarantee_helmet, 0, 0, fac_commoners,
   [itm_slave_neck_chain],
   def_attrib|level(2), weak_melee(2), 0, man_face_middle_1, man_face_old_2],

#Slaver Others
  ["slaver_rep_1", "Slaver Representative", "Slaver Representative", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_shield, 0, reserved, fac_sod_merc_guild6, 
    [itm_mace_6, itm_arena_lance, itm_throwing_military_hammers, itm_tab_shield_heater_cav_b,
    itm_skull_helm1, itm_heraldic_mail_with_surcoat, itm_mail_boots, itm_mail_mittens,
    itm_charger_black],
   def_attrib|level(15), expert_melee(15), knows_riding_4|knows_power_strike_4|knows_shield_4|knows_athletics_2|knows_tactics_1|knows_leadership_1, 0x00000005bf0410d231586d3b4431d88c00000000001ec2e30000000000000000],

   ["slaver_deserter_1", "Slaver Hunter Deserter", "Slaver Hunter Deserters", tf_mounted|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots|tf_guarantee_horse, 0, 0, fac_deserters,
   [itm_winged_mace, itm_mace_6, itm_spiked_mace, itm_quarter_staff, itm_iron_staff, itm_throwing_hammers1, itm_throwing_hammers2, itm_slaver_shield_round_hide, itm_slaver_shield_kite_hide,
    itm_leather_warrior_cap, itm_skullcap, itm_padded_leather2, itm_padded_leather3, itm_leather_armor, itm_leather_boots, itm_leather_gloves,
    itm_saddle_horse],
   def_attrib|level(18), regular_melee(18), knows_riding_1|knows_power_throw_1|knows_power_strike_1, bandit_face1, bandit_face2],


####################################################################################
# KHERGIT KINGDOM
####################################################################################

  ["khergit_tribesman", "Khergit Tribesman", "Khergit Tribesmen", tf_mounted|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_kingdom_3,
   [itm_arrows, itm_club, itm_spear, itm_hunting_bow,
    itm_steppe_cap, itm_helmet_fur_a, itm_leather_vest, itm_steppe_armor, itm_nomad_boots,
    itm_steppe_horse, itm_sumpter_horse],
   def_attrib|level(5), regular_all(5), knows_riding_3|knows_power_draw_2|knows_horse_archery_2, khergit_face_younger_1, khergit_face_old_2],

  ["khergit_skirmisher", "Khergit Skirmisher", "Khergit Skirmishers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_kingdom_3,
   [itm_arrows, itm_sword_khergit_1, itm_winged_mace, itm_spear, itm_nomad_bow, itm_javelin, itm_tab_shield_small_round_a,
    itm_steppe_cap, itm_helmet_fur_a, itm_nomad_cap_a, itm_khergit_armor, itm_steppe_armor, itm_leather_vest, itm_nomad_boots,
    itm_steppe_horse, itm_saddle_horse],
   def_attrib|level(10), regular_all(10), knows_riding_4|knows_power_draw_3|knows_power_throw_1|knows_horse_archery_3, khergit_face_younger_1, khergit_face_old_2],

  ["khergit_horseman", "Khergit Horseman", "Khergit Horsemen", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged|tf_guarantee_horse, 0, 0, fac_kingdom_3,
   [itm_arrows, itm_light_lance, itm_nomad_bow, itm_sword_khergit_2, itm_tab_shield_small_round_a, itm_tab_shield_small_round_b, itm_spear,
    itm_nomad_cap_a, itm_leather_steppe_cap_a, itm_nomad_robe, itm_nomad_vest, itm_nomad_boots, itm_hide_boots, itm_spiked_helmet, itm_helmet_fur_a,
    itm_steppe_horse, itm_hunter],
   def_attrib|level(16), regular_all(16), knows_riding_5|knows_power_draw_4|knows_ironflesh_2|knows_power_throw_1, khergit_face_young_1, khergit_face_older_2],

  ["khergit_horse_archer", "Khergit Horse Archer", "Khergit Horse Archers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged|tf_guarantee_horse, 0, 0, fac_kingdom_3,
   [itm_arrows, itm_sword_khergit_2, itm_winged_mace, itm_spear, itm_khergit_bow, itm_tab_shield_small_round_a, itm_tab_shield_small_round_a, itm_tab_shield_small_round_b, itm_bodkin_arrows, itm_arrows, itm_javelin, itm_tab_shield_small_round_a, itm_tab_shield_small_round_b,
    itm_leather_steppe_cap_a, itm_leather_steppe_cap_b, itm_tribal_warrior_outfit, itm_nomad_robe, itm_hide_boots,
    itm_steppe_horse],
   def_attrib|level(22), regular_all(22), knows_riding_5|knows_power_draw_3|knows_ironflesh_2|knows_horse_archery_5|knows_power_throw_1, khergit_face_young_1, khergit_face_older_2],

  ["khergit_veteran_horse_archer", "Khergit Veteran Horse Archer", "Khergit Veteran Horse Archers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_kingdom_3,
   [itm_sword_khergit_3, itm_winged_mace, itm_spear, itm_khergit_bow, itm_nomad_bow, itm_nomad_bow, itm_arrows, itm_khergit_arrows, itm_khergit_arrows, itm_javelin, itm_tab_shield_small_round_b, itm_tab_shield_small_round_c,
    itm_leather_steppe_cap_b, itm_leather_warrior_cap, itm_lamellar_vest, itm_tribal_warrior_outfit, itm_hide_boots,
    itm_courser],
   def_attrib|level(25), expert_all(25), knows_riding_6|knows_power_draw_4|knows_ironflesh_4|knows_horse_archery_7|knows_power_throw_3, khergit_face_middle_1, khergit_face_older_2],

  ["khergit_lancer", "Khergit Lancer", "Khergit Lancers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_kingdom_3,
   [itm_arrows, itm_sword_khergit_4, itm_winged_mace, itm_spear, itm_lance, itm_lance, itm_khergit_bow, itm_strong_bow, itm_short_bow, itm_khergit_arrows, itm_arrows, itm_tab_shield_small_round_b, itm_tab_shield_small_round_c,
    itm_khergit_guard_helmet, itm_khergit_cavalry_helmet, itm_lamellar_armor, itm_hide_boots, itm_leather_gloves,
    itm_courser],
   def_attrib|level(23), regular_all(23), knows_riding_6|knows_power_strike_4|knows_power_draw_3|knows_power_throw_2|knows_ironflesh_4|knows_horse_archery_1, khergit_face_middle_1, khergit_face_older_2],

  ["khergit_messenger", "Khergit Messenger", "Khergit Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
   [itm_sword_khergit_2,
    itm_leather_jerkin, itm_leather_boots, itm_leather_gloves, itm_short_bow, itm_arrows,
    itm_courser],
   def_attrib|agi_21|level(25), regular_all(25), knows_riding_7|knows_horse_archery_5|knows_power_draw_5, khergit_face_young_1, khergit_face_older_2],

  ["khergit_deserter", "Khergit Deserter", "Khergit Deserters", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_deserters,
   [itm_arrows, itm_spiked_mace, itm_axe, itm_sword_khergit_1, itm_short_bow, itm_short_bow, itm_hunting_bow, itm_javelin, itm_javelin,
    itm_steppe_cap, itm_helmet_fur_a, itm_leather_vest, itm_leather_vest, itm_nomad_armor, itm_nomad_boots],
   def_attrib|str_10|level(14), regular_all(14), knows_ironflesh_1|knows_power_draw_1, khergit_face_young_1, khergit_face_older_2],

  ["khergit_prison_guard", "Prison Guard", "Prison Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_sword_khergit_3, itm_tab_shield_small_round_b, itm_tab_shield_small_round_a,
    itm_lamellar_vest, itm_lamellar_armor, itm_hide_boots, itm_iron_greaves, itm_khergit_guard_helmet, itm_khergit_cavalry_helmet, itm_leather_warrior_cap],
   def_attrib|level(24), regular_all(24), knows_athletics_3|knows_shield_2|knows_ironflesh_3, khergit_face_middle_1, khergit_face_older_2],

  ["khergit_castle_guard", "Castle Guard", "Castle Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_sword_khergit_4, itm_tab_shield_small_round_b, itm_tab_shield_small_round_a,
    itm_lamellar_vest, itm_lamellar_armor, itm_hide_boots, itm_iron_greaves, itm_khergit_guard_helmet, itm_khergit_cavalry_helmet, itm_leather_warrior_cap],
   def_attrib|level(24), regular_all(24), knows_athletics_3|knows_shield_2|knows_ironflesh_3, khergit_face_middle_1, khergit_face_older_2],


####################################################################################
# NORD KINGDOM
####################################################################################

  ["nord_recruit", "Nord Recruit", "Nord Recruits", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_kingdom_4,
   [itm_axe, itm_hatchet, itm_spear, itm_tab_shield_round_a, itm_tab_shield_round_a, itm_javelin, 
    itm_shirt, itm_coarse_tunic, itm_hide_boots, itm_nomad_boots],
   def_attrib|level(6), regular_all(6), knows_power_strike_1|knows_power_throw_1|knows_athletics_1, nord_face_younger_1, nord_face_old_2],

  ["nord_footman", "Nord Footman", "Nord Footmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_kingdom_4,
   [itm_fighting_axe, itm_one_handed_war_axe_a, itm_spear, itm_tab_shield_round_a, itm_tab_shield_round_b, itm_javelin, itm_throwing_axes,
    itm_leather_cap, itm_skullcap, itm_nomad_vest, itm_shirt, itm_leather_boots, itm_nomad_boots],
   def_attrib|level(10), regular_all(10), knows_ironflesh_3|knows_power_strike_2|knows_power_throw_2|knows_athletics_2|knows_shield_1, nord_face_young_1, nord_face_old_2],

  ["nord_trained_footman", "Nord Trained Footman", "Nord Trained Footmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield|tf_guarantee_helmet, 0, 0, fac_kingdom_4,
   [itm_one_handed_war_axe_a, itm_one_handed_war_axe_b, itm_one_handed_battle_axe_a, itm_tab_shield_round_b, itm_javelin, itm_throwing_axes, 
    itm_skullcap, itm_nasal_helmet, itm_byrnie, itm_studded_leather_coat, itm_leather_jerkin, itm_leather_boots],
   def_attrib|level(14), regular_all(14), knows_ironflesh_4|knows_power_strike_3|knows_power_throw_2|knows_athletics_3|knows_shield_2, nord_face_young_1, nord_face_old_2],

  ["nord_warrior", "Nord Warrior", "Nord Warriors", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield|tf_guarantee_helmet, 0, 0, fac_kingdom_4,
   [itm_arrows, itm_sword_viking_1, itm_one_handed_war_axe_b, itm_one_handed_battle_axe_a, itm_tab_shield_round_c, itm_javelin, itm_throwing_axes,
    itm_nasal_helmet, itm_byrnie, itm_mail_shirt, itm_mail_hauberk, itm_studded_leather_coat, itm_hunter_boots, itm_leather_boots],
   def_attrib|level(19), regular_all(19), knows_ironflesh_5|knows_power_strike_4|knows_power_throw_3|knows_athletics_4|knows_shield_3, nord_face_young_1, nord_face_older_2],

  ["nord_veteran", "Nord Veteran", "Nord Veterans", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield|tf_guarantee_helmet, 0, 0, fac_kingdom_4,
   [itm_arrows, itm_sword_viking_2, itm_sword_viking_2_small, itm_one_handed_battle_axe_b, itm_spiked_mace, itm_tab_shield_round_d, itm_javelin, itm_throwing_axes,
    itm_nordic_helmet, itm_nasal_helmet, itm_byrnie, itm_mail_hauberk, itm_splinted_leather_greaves, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(24), regular_all(24), knows_ironflesh_6|knows_power_strike_5|knows_power_throw_4|knows_athletics_5|knows_shield_4, nord_face_young_1, nord_face_older_2],

  ["nord_champion", "Nord Huscarl", "Nord Huscarls", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield|tf_guarantee_helmet, 0, 0, fac_kingdom_4,
   [itm_sword_viking_3, itm_sword_viking_3_small, itm_great_axe, itm_one_handed_battle_axe_c, itm_tab_shield_round_e, itm_jarid, itm_throwing_axes, itm_throwing_axes,
    itm_great_helmet, itm_nordic_helmet, itm_banded_armor, itm_iron_greaves, itm_mail_boots, itm_leather_boots, itm_mail_mittens],
   def_attrib|level(28), regular_all(28), knows_ironflesh_7|knows_power_strike_7|knows_power_throw_5|knows_athletics_6|knows_shield_5, nord_face_middle_1, nord_face_older_2],

  ["nord_huntsman", "Nord Huntsman", "Nord Huntsmen", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_neutral,
   [itm_arrows, itm_hatchet, itm_hunting_bow,
    itm_shirt, itm_shirt, itm_hide_boots],
   def_attrib|str_10|level(11), regular_archer(11), knows_ironflesh_2|knows_power_draw_2|knows_athletics_2, nord_face_young_1, nord_face_old_2],

  ["nord_archer", "Nord Archer", "Nord Archers", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_neutral,
   [itm_arrows, itm_axe, itm_short_bow,
    itm_leather_jerkin, itm_shirt, itm_leather_boots, itm_nasal_helmet, itm_leather_cap],
   def_attrib|str_11|level(15), regular_archer(15), knows_ironflesh_2|knows_power_draw_3|knows_athletics_3, nord_face_young_1, nord_face_old_2],

  ["nord_veteran_archer", "Nord Veteran Archer", "Nord Veteran Archers", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_neutral,
   [itm_barbed_arrows, itm_one_handed_war_axe_a, itm_sword_viking_1, itm_long_bow,
    itm_leather_jerkin, itm_padded_leather, itm_leather_boots, itm_nasal_helmet, itm_leather_cap],
   def_attrib|str_12|level(20), regular_archer(20), knows_power_strike_1|knows_ironflesh_4|knows_power_draw_6|knows_athletics_4, nord_face_middle_1, nord_face_older_2],

  ["nord_messenger", "Nord Messenger", "Nord Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
   [itm_sword_viking_2, itm_short_bow, itm_arrows,
    itm_leather_jerkin, itm_leather_boots, itm_leather_gloves,
    itm_courser],
   def_attrib|agi_21|level(25), regular_all(25), knows_riding_7|knows_horse_archery_5|knows_power_draw_5, nord_face_young_1, nord_face_older_2],

  ["nord_deserter", "Nord Deserter", "Nord Deserters", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_deserters,
   [itm_arrows, itm_spiked_mace, itm_axe, itm_falchion, itm_short_bow, itm_short_bow, itm_hunting_bow, itm_javelin, itm_javelin,
    itm_steppe_cap, itm_helmet_fur_a, itm_leather_vest, itm_leather_vest, itm_nomad_armor, itm_nomad_boots],
   def_attrib|str_10|level(14), regular_all(14), knows_ironflesh_1|knows_power_draw_1, nord_face_young_1, nord_face_older_2],

  ["nord_prison_guard", "Prison Guard", "Prison Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_ashwood_pike, itm_battle_fork_1, itm_battle_axe, itm_fighting_axe, itm_tab_shield_round_d,
    itm_mail_hauberk, itm_mail_chausses, itm_iron_greaves, itm_nordic_helmet, itm_nordic_helmet, itm_nordic_helmet, itm_spiked_helmet, itm_leather_gloves],
   def_attrib|level(24), regular_all(24), knows_athletics_3|knows_shield_2|knows_ironflesh_3, nord_face_middle_1, nord_face_older_2],

  ["nord_castle_guard", "Castle Guard", "Castle Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_ashwood_pike, itm_battle_fork_1, itm_battle_axe, itm_fighting_axe, itm_tab_shield_round_d, itm_tab_shield_round_e,
    itm_mail_hauberk, itm_heraldic_mail_with_tabard, itm_mail_chausses, itm_iron_greaves, itm_nordic_helmet, itm_nordic_helmet, itm_nordic_helmet, itm_spiked_helmet, itm_leather_gloves],
   def_attrib|level(24), regular_all(24), knows_athletics_3|knows_shield_2|knows_ironflesh_3, nord_face_middle_1, nord_face_older_2],


####################################################################################
# RHODOK KINGDOM
####################################################################################

  ["rhodok_tribesman", "Rhodok Tribesman", "Rhodok Tribesmen", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_kingdom_5,
   [itm_pitch_fork, itm_tab_shield_pavise_a,
    itm_shirt, itm_coarse_tunic, itm_wrapping_boots, itm_nomad_boots, itm_head_wrappings],
   def_attrib|level(4), regular_melee(4), knows_power_draw_2|knows_ironflesh_1, rhodok_face_younger_1, rhodok_face_old_2],

  ["rhodok_spearman", "Rhodok Spearman", "Rhodok Spearmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_kingdom_5,
   [itm_spear, itm_tab_shield_pavise_a, itm_tab_shield_pavise_a,
    itm_leather_cap, itm_common_hood, itm_leather_vest, itm_leather_vest, itm_wrapping_boots, itm_nomad_boots],
   def_attrib|level(10), regular_melee(10), knows_ironflesh_2|knows_shield_1|knows_power_strike_2|knows_athletics_1, rhodok_face_young_1, rhodok_face_old_2],

  ["rhodok_trained_spearman", "Rhodok Trained Spearman", "Rhodok Trained Spearmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_kingdom_5,
   [itm_pike, itm_spear, itm_tab_shield_pavise_b,
    itm_leather_cap, itm_leather_vest, itm_ragged_outfit, itm_padded_cloth, itm_gambeson, itm_nomad_boots],
   def_attrib|level(15), regular_melee(15), knows_ironflesh_4|knows_shield_2|knows_power_strike_3|knows_athletics_2, rhodok_face_young_1, rhodok_face_older_2],

  ["rhodok_veteran_spearman", "Rhodok Veteran Spearman", "Rhodok Veteran Spearmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_5,
   [itm_ashwood_pike, itm_war_spear, itm_pike, itm_club_with_spike_head, itm_tab_shield_pavise_c, itm_sword_medieval_a,
    itm_kettle_hat, itm_leather_cap, itm_byrnie, itm_ragged_outfit, itm_nomad_boots],
   def_attrib|level(20), regular_melee(20), knows_ironflesh_6|knows_shield_3|knows_power_strike_5|knows_athletics_3, rhodok_face_young_1, rhodok_face_older_2],

  ["rhodok_sergeant", "Rhodok Sergeant", "Rhodok Sergeants", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_5,
   [itm_glaive, itm_war_spear, itm_sword_medieval_b, itm_tab_shield_pavise_d,
    itm_kettle_hat, itm_guard_helmet, itm_spiked_helmet, itm_byrnie, itm_surcoat_over_mail, itm_banded_armor, itm_nomad_boots],
   def_attrib|level(25), expert_melee(25), knows_ironflesh_9|knows_shield_5|knows_power_strike_7|knows_athletics_5, rhodok_face_middle_1, rhodok_face_older_2],

  ["rhodok_crossbowman", "Rhodok Crossbowman", "Rhodok Crossbowmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_ranged, 0, 0, fac_kingdom_5,
   [itm_sword_medieval_a, itm_falchion, itm_club_with_spike_head, itm_tab_shield_pavise_a, itm_crossbow, itm_bolts,
    itm_leather_jerkin, itm_ragged_outfit, itm_nomad_boots],
   def_attrib|level(11), regular_crossbow(11), knows_ironflesh_2|knows_shield_1|knows_power_strike_2|knows_athletics_2, rhodok_face_young_1, rhodok_face_older_2],

  ["rhodok_trained_crossbowman", "Rhodok Trained Crossbowman", "Rhodok Trained Crossbowmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_ranged|tf_guarantee_shield, 0, 0, fac_kingdom_5,
   [itm_sword_medieval_a, itm_sword_medieval_b_small, itm_club_with_spike_head, itm_tab_shield_pavise_a, itm_tab_shield_pavise_a, itm_crossbow, itm_bolts,
    itm_leather_cap, itm_leather_jerkin, itm_ragged_outfit, itm_nomad_boots],
   def_attrib|level(16), regular_crossbow(16), knows_ironflesh_3|knows_shield_2|knows_power_strike_3|knows_athletics_3, rhodok_face_young_1, rhodok_face_older_2],

  ["rhodok_veteran_crossbowman", "Rhodok Veteran Crossbowman", "Rhodok Veteran Crossbowmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_ranged|tf_guarantee_shield, 0, 0, fac_kingdom_5,
   [itm_sword_medieval_a, itm_sword_medieval_b_small, itm_fighting_pick, itm_club_with_spike_head, itm_tab_shield_pavise_a, itm_tab_shield_pavise_b, itm_tab_shield_pavise_c, itm_heavy_crossbow, itm_bolts,
    itm_leather_cap, itm_leather_jerkin, itm_padded_leather, itm_nomad_boots],
   def_attrib|level(21), regular_crossbow(21), knows_ironflesh_4|knows_shield_3|knows_power_strike_4|knows_athletics_4, rhodok_face_middle_1, rhodok_face_older_2],

  ["rhodok_sharpshooter", "Rhodok Sharpshooter", "Rhodok Sharpshooters", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_ranged|tf_guarantee_shield, 0, 0, fac_kingdom_5,
   [itm_sword_medieval_b, itm_military_pick, itm_tab_shield_pavise_c, itm_sniper_crossbow, itm_steel_bolts,
    itm_kettle_hat, itm_leather_cap, itm_byrnie, itm_padded_leather, itm_leather_boots],
   def_attrib|level(26), expert_crossbow(26), knows_ironflesh_5|knows_shield_4|knows_power_strike_4|knows_athletics_6, rhodok_face_middle_1, rhodok_face_older_2],

  ["rhodok_messenger", "Rhodok Messenger", "Rhodok Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
   [itm_sword_medieval_b, itm_short_bow, itm_arrows,
    itm_leather_jerkin, itm_leather_boots, itm_leather_gloves,
    itm_courser],
   def_attrib|agi_21|level(25), regular_melee(25), knows_riding_7|knows_horse_archery_5|knows_power_draw_5, rhodok_face_middle_1, rhodok_face_older_2],

  ["rhodok_deserter", "Rhodok Deserter", "Rhodok Deserters", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_deserters,
   [itm_arrows, itm_spiked_mace, itm_axe, itm_falchion, itm_short_bow, itm_short_bow, itm_hunting_bow, itm_javelin, itm_javelin,
    itm_steppe_cap, itm_helmet_fur_a, itm_leather_vest, itm_leather_vest, itm_nomad_armor, itm_nomad_boots],
   def_attrib|str_10|level(14), regular_melee(14), knows_ironflesh_1|knows_power_draw_1, rhodok_face_middle_1, rhodok_face_older_2],

  ["rhodok_prison_guard", "Prison Guard", "Prison Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_ashwood_pike, itm_battle_fork_1, itm_battle_axe, itm_fighting_axe, itm_tab_shield_pavise_b,
    itm_mail_hauberk, itm_byrnie, itm_mail_chausses, itm_iron_greaves, itm_guard_helmet, itm_leather_gloves],
   def_attrib|level(24), regular_melee(24), knows_athletics_3|knows_shield_2|knows_ironflesh_3, rhodok_face_middle_1, rhodok_face_older_2],

  ["rhodok_castle_guard", "Castle Guard", "Castle Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_ashwood_pike, itm_battle_fork_1, itm_battle_axe, itm_fighting_axe, itm_tab_shield_pavise_c,
    itm_mail_hauberk, itm_byrnie, itm_mail_chausses, itm_iron_greaves, itm_guard_helmet, itm_leather_gloves],
   def_attrib|level(24), regular_melee(24), knows_athletics_3|knows_shield_2|knows_ironflesh_3, rhodok_face_middle_1, rhodok_face_older_2],


####################################################################################
# SWADIAN KINGDOM
####################################################################################

  ["swadian_recruit", "Swadian Recruit", "Swadian Recruits", tf_guarantee_armor, 0, 0, fac_kingdom_1,
   [itm_scythe, itm_hatchet, itm_pickaxe, itm_club, itm_stones, itm_tab_shield_heater_a, itm_leather_cap, itm_felt_hat, itm_felt_hat,
    itm_shirt, itm_coarse_tunic, itm_leather_apron, itm_nomad_boots, itm_wrapping_boots],
   def_attrib|level(4), regular_melee(4), 0, swadian_face_younger_1, swadian_face_middle_2],

  ["swadian_militia", "Swadian Militia", "Swadian Militia", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_kingdom_1,
   [itm_bolts, itm_spiked_club, itm_fighting_pick, itm_boar_spear, itm_hunting_crossbow, itm_tab_shield_heater_a,
    itm_padded_cloth, itm_leather_armor, itm_leather_cap, itm_arming_cap, itm_padded_coif, itm_ankle_boots, itm_wrapping_boots],
   def_attrib|level(10), regular_melee(10), 0, swadian_face_young_1, swadian_face_old_2],

  ["swadian_footman", "Swadian Footman", "Swadian Footmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_kingdom_1,
   [itm_spear, itm_fighting_pick, itm_sword_medieval_b_small, itm_sword_medieval_a, itm_tab_shield_heater_b,
    itm_leather_jerkin, itm_padded_leather, itm_leather_armor, itm_ankle_boots, itm_padded_coif, itm_footman_helmet],
   def_attrib|level(15), regular_melee(15), knows_ironflesh_1|knows_power_strike_1|knows_shield_2, swadian_face_young_1, swadian_face_old_2],

  ["swadian_infantry", "Swadian Infantry", "Swadian Infantry", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_kingdom_1,
   [itm_pike, itm_fighting_pick, itm_bastard_sword_a, itm_sword_medieval_a, itm_sword_medieval_b_small, itm_tab_shield_heater_c,
    itm_mail_with_surcoat, itm_haubergeon, itm_hide_boots, itm_ankle_boots, itm_kettle_hat, itm_mail_coif, itm_flat_topped_helmet, itm_helmet_with_neckguard],
   def_attrib|level(20), regular_melee(20), knows_ironflesh_3|knows_power_strike_2|knows_shield_3, swadian_face_middle_1, swadian_face_old_2],

  ["swadian_sergeant", "Swadian Sergeant", "Swadian Sergeants", tf_mounted|tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_kingdom_1,
   [itm_awlpike, itm_bastard_sword_b, itm_morningstar, itm_sword_medieval_c, itm_tab_shield_heater_d,
    itm_surcoat_over_mail, itm_mail_with_surcoat, itm_mail_chausses, itm_iron_greaves, itm_guard_helmet, itm_helmet_with_neckguard, itm_bascinet, itm_guard_helmet, itm_leather_gloves,
    itm_hunter],
   def_attrib|level(25), expert_melee(25), knows_shield_3|knows_ironflesh_7|knows_power_strike_6, swadian_face_middle_1, swadian_face_older_2],

  ["swadian_skirmisher", "Swadian Skirmisher", "Swadian Skirmishers", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_kingdom_1,
   [itm_bolts, itm_light_crossbow, itm_hunting_crossbow, itm_dagger, itm_club, itm_voulge, itm_tab_shield_heater_a,
    itm_leather_armor, itm_padded_cloth, itm_ankle_boots, itm_padded_coif, itm_arming_cap, itm_footman_helmet],
   def_attrib|level(14), regular_crossbow(14), knows_ironflesh_1, swadian_face_young_1, swadian_face_middle_2],

  ["swadian_crossbowman", "Swadian Crossbowman", "Swadian Crossbowmen", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_kingdom_1,
   [itm_bolts, itm_crossbow, itm_light_crossbow, itm_fighting_pick, itm_dagger, itm_sword_medieval_a, itm_voulge, itm_tab_shield_heater_b,
    itm_leather_jerkin, itm_leather_armor, itm_hide_boots, itm_ankle_boots, itm_padded_coif, itm_nasal_helmet, itm_footman_helmet],
   def_attrib|level(19), regular_crossbow(19), knows_ironflesh_1, swadian_face_young_1, swadian_face_old_2],

  ["swadian_sharpshooter", "Swadian Sharpshooter", "Swadian Sharpshooters", tf_guarantee_ranged|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_kingdom_1,
   [itm_bolts, itm_steel_bolts, itm_arrows, itm_crossbow, itm_heavy_crossbow, itm_heavy_crossbow, itm_sword_medieval_b_small, itm_sword_medieval_a, itm_voulge, itm_tab_shield_heater_c,
    itm_haubergeon, itm_padded_leather, itm_mail_boots, itm_norman_helmet, itm_nasal_helmet, itm_kettle_hat, itm_kettle_hat, itm_leather_gloves,
    itm_hunter],
   def_attrib|str_18|level(24), regular_crossbow(24), knows_power_draw_3|knows_ironflesh_2, swadian_face_middle_1, swadian_face_older_2],

  ["swadian_man_at_arms", "Swadian Man at Arms", "Swadian Men at Arms", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield|tf_guarantee_gloves, 0, 0, fac_kingdom_1,
   [itm_lance, itm_bastard_sword_a, itm_sword_medieval_b, itm_sword_medieval_c_small, itm_tab_shield_heater_cav_a,
    itm_mail_with_surcoat, itm_light_mail_and_plate, itm_hide_boots, itm_norman_helmet, itm_mail_coif, itm_flat_topped_helmet, itm_helmet_with_neckguard, itm_mail_mittens,
    itm_warhorse],
   def_attrib|level(20), regular_melee(20), knows_riding_4|knows_ironflesh_2|knows_shield_2|knows_power_strike_4, swadian_face_young_1, swadian_face_old_2],

  ["swadian_knight", "Swadian Knight", "Swadian Knights", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_kingdom_1,
   [itm_heavy_lance, itm_bastard_sword_b, itm_sword_medieval_c, itm_tab_shield_heater_cav_b,
    itm_plate_armor, itm_plate_armor2, itm_mail_chausses, itm_iron_greaves, itm_guard_helmet, itm_great_helmet, itm_bascinet, itm_mail_mittens,
    itm_charger],
   def_attrib|level(25), expert_melee(25), knows_riding_5|knows_shield_2|knows_ironflesh_3|knows_power_strike_5, swadian_face_middle_1, swadian_face_older_2],

  ["swadian_messenger", "Swadian Messenger", "Swadian Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
   [itm_sword_medieval_a, itm_light_crossbow, itm_bolts,
    itm_leather_jerkin, itm_leather_boots, itm_leather_gloves,
    itm_courser],
   def_attrib|agi_21|level(25), regular_melee(25), knows_riding_7|knows_horse_archery_5, swadian_face_young_1, swadian_face_old_2],

  ["swadian_deserter", "Swadian Deserter", "Swadian Deserters", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_deserters,
   [itm_bolts, itm_light_crossbow, itm_hunting_crossbow, itm_dagger, itm_club, itm_voulge, itm_wooden_shield,
    itm_leather_jerkin, itm_padded_cloth, itm_hide_boots, itm_padded_coif, itm_nasal_helmet, itm_footman_helmet],
   def_attrib|level(14), regular_melee(14), knows_ironflesh_1, swadian_face_young_1, swadian_face_old_2],

  ["swadian_prison_guard", "Prison Guard", "Prison Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_awlpike, itm_pike, itm_sword_of_war, itm_morningstar, itm_sword_medieval_b, itm_tab_shield_heater_c,
    itm_coat_of_plates, itm_plate_armor, itm_mail_chausses, itm_iron_greaves, itm_guard_helmet, itm_helmet_with_neckguard, itm_bascinet, itm_guard_helmet, itm_leather_gloves],
   def_attrib|level(25), regular_melee(25), knows_shield_3|knows_ironflesh_3|knows_power_strike_3, swadian_face_young_1, swadian_face_old_2],

  ["swadian_castle_guard", "Castle Guard", "Castle Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_awlpike, itm_pike, itm_sword_of_war, itm_morningstar, itm_sword_medieval_b, itm_tab_shield_heater_c, itm_tab_shield_heater_d,
    itm_coat_of_plates, itm_plate_armor, itm_mail_chausses, itm_iron_greaves, itm_guard_helmet, itm_helmet_with_neckguard, itm_bascinet, itm_guard_helmet, itm_leather_gloves],
   def_attrib|level(25), regular_melee(25), knows_shield_3|knows_ironflesh_3|knows_power_strike_3, swadian_face_young_1, swadian_face_old_2],

####################################################################################
# VAEGIR KINGDOM
####################################################################################

  ["vaegir_recruit", "Vaegir Recruit", "Vaegir Recruits", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_kingdom_2,
   [itm_scythe, itm_hatchet, itm_cudgel, itm_axe, itm_stones, itm_tab_shield_kite_a, itm_tab_shield_kite_a,
    itm_rawhide_coat, itm_nomad_armor, itm_nomad_boots],
   def_attrib|level(4), regular_melee(4), 0, vaegir_face_younger_1, vaegir_face_middle_2],

  ["vaegir_footman", "Vaegir Footman", "Vaegir Footmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_kingdom_2,
   [itm_spiked_club, itm_hand_axe, itm_sword_viking_1, itm_two_handed_axe, itm_tab_shield_kite_a, itm_tab_shield_kite_b, itm_spear,
    itm_helmet_fur_a, itm_skullcap, itm_rawhide_coat, itm_nomad_armor, itm_nomad_boots],
   def_attrib|level(10), regular_melee(10), 0, vaegir_face_young_1, vaegir_face_middle_2],

  ["vaegir_skirmisher", "Vaegir Skirmisher", "Vaegir Skirmishers", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_kingdom_2,
   [itm_arrows, itm_spiked_mace, itm_axe, itm_sword_khergit_1, itm_short_bow, itm_short_bow, itm_hunting_bow, itm_javelin, itm_javelin,
    itm_steppe_cap, itm_helmet_fur_a, itm_leather_vest, itm_leather_vest, itm_nomad_armor, itm_nomad_boots],
   def_attrib|str_10|level(15), regular_archer(15), knows_ironflesh_1|knows_power_draw_1|knows_power_throw_1, vaegir_face_young_1, vaegir_face_old_2],

  ["vaegir_archer", "Vaegir Archer", "Vaegir Archers", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_kingdom_2,
   [itm_arrows, itm_axe, itm_sword_khergit_1, itm_nomad_bow, itm_nomad_bow, itm_short_bow,
    itm_leather_jerkin, itm_leather_vest, itm_nomad_boots, itm_spiked_helmet, itm_nordic_helmet, itm_nasal_helmet, itm_helmet_fur_a],
   def_attrib|str_12|level(20), regular_archer(20), knows_ironflesh_1|knows_power_draw_2|knows_athletics_2|knows_power_throw_1, vaegir_face_young_1, vaegir_face_older_2],

  ["vaegir_marksman", "Vaegir Marksman", "Vaegir Marksmen", tf_guarantee_ranged|tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves, 0, 0, fac_kingdom_2,
   [itm_arrows, itm_bodkin_arrows, itm_axe, itm_voulge, itm_sword_khergit_2, itm_strong_bow, itm_strong_bow, itm_nomad_bow, itm_tab_shield_kite_b,
    itm_leather_vest, itm_studded_leather_coat, itm_lamellar_vest, itm_lamellar_armor, itm_mail_boots, itm_leather_gloves, itm_spiked_helmet, itm_nordic_helmet, itm_nasal_helmet, itm_helmet_fur_a],
   def_attrib|str_18|level(27), expert_archer(27), knows_ironflesh_4|knows_power_draw_5|knows_athletics_3|knows_power_throw_1, vaegir_face_young_1, vaegir_face_older_2],

  ["vaegir_veteran", "Vaegir Veteran", "Vaegir Veterans", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield|tf_guarantee_gloves, 0, 0, fac_kingdom_2,
   [itm_spiked_mace, itm_two_handed_axe, itm_sword_viking_1, itm_tab_shield_kite_b, itm_tab_shield_kite_c, itm_spear,
    itm_steppe_cap, itm_helmet_fur_a, itm_leather_jerkin, itm_studded_leather_coat, itm_nomad_boots,
    itm_saddle_horse],
   def_attrib|level(15), regular_melee(14), knows_athletics_1|knows_ironflesh_1|knows_shield_2, vaegir_face_young_1, vaegir_face_old_2],

  ["vaegir_infantry", "Vaegir Infantry", "Vaegir Infantries", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves, 0, 0, fac_kingdom_2,
   [itm_pike, itm_battle_axe, itm_sword_viking_2, itm_sword_khergit_2, itm_tab_shield_kite_c, itm_spear,
    itm_mail_hauberk, itm_lamellar_vest, itm_nomad_boots, itm_spiked_helmet, itm_nordic_helmet, itm_nasal_helmet, itm_helmet_fur_a],
   def_attrib|level(20), regular_melee(20), knows_athletics_2|knows_ironflesh_3|knows_power_strike_3|knows_shield_2, vaegir_face_young_1, vaegir_face_older_2],

  ["vaegir_guard", "Vaegir Guard", "Vaegir Guards", tf_mounted|tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves, 0, 0, fac_kingdom_2,
   [itm_ashwood_pike, itm_battle_fork_1, itm_bardiche, itm_battle_axe, itm_fighting_axe, itm_tab_shield_kite_d,
    itm_banded_armor, itm_lamellar_vest, itm_lamellar_armor, itm_mail_chausses, itm_iron_greaves, itm_nordic_helmet, itm_nordic_helmet, itm_nordic_helmet, itm_spiked_helmet, itm_leather_gloves,
    itm_hunter],
   def_attrib|level(25), expert_melee(25), knows_athletics_3|knows_shield_2|knows_ironflesh_5|knows_power_strike_4, vaegir_face_middle_1, vaegir_face_older_2],

  ["vaegir_horseman", "Vaegir Horseman", "Vaegir Horsemen", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield|tf_guarantee_gloves, 0, 0, fac_kingdom_2,
   [itm_battle_axe, itm_sword_khergit_2, itm_lance, itm_tab_shield_kite_cav_a, itm_spear,
    itm_lamellar_vest, itm_red_surcoat_over_mail, itm_banded_armor, itm_nomad_boots, itm_spiked_helmet, itm_nordic_helmet, itm_nasal_helmet, itm_helmet_fur_a, itm_mail_mittens,
    itm_steppe_horse, itm_hunter],
   def_attrib|level(19), regular_melee(19), knows_riding_3|knows_ironflesh_2|knows_power_strike_2, vaegir_face_young_1, vaegir_face_older_2],

  ["vaegir_knight", "Vaegir Knight", "Vaegir Knights", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_kingdom_2,
   [itm_cimitar, itm_fighting_axe, itm_lance, itm_lance, itm_tab_shield_kite_cav_b,
    itm_plate_armor, itm_mail_chausses, itm_iron_greaves, itm_nordic_helmet, itm_nordic_helmet, itm_nordic_helmet, itm_spiked_helmet, itm_mail_mittens,
    itm_warhorse, itm_leather_gloves],
   def_attrib|level(24), regular_melee(24), knows_riding_4|knows_shield_2|knows_ironflesh_4|knows_power_strike_4, vaegir_face_middle_1, vaegir_face_older_2],

  ["vaegir_messenger", "Vaegir Messenger", "Vaegir Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
   [itm_sword_medieval_b, itm_short_bow, itm_arrows,
    itm_leather_jerkin, itm_leather_boots, itm_leather_gloves,
    itm_courser],
   def_attrib|agi_21|level(25), regular_melee(25), knows_riding_7|knows_horse_archery_5|knows_power_draw_5, vaegir_face_young_1, vaegir_face_older_2],

  ["vaegir_deserter", "Vaegir Deserter", "Vaegir Deserters", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_deserters,
   [itm_arrows, itm_spiked_mace, itm_axe, itm_falchion, itm_short_bow, itm_short_bow, itm_hunting_bow, itm_javelin, itm_javelin,
    itm_steppe_cap, itm_helmet_fur_a, itm_leather_vest, itm_leather_vest, itm_nomad_armor, itm_nomad_boots],
   def_attrib|str_10|level(14), regular_melee(14), knows_ironflesh_1|knows_power_draw_1, vaegir_face_young_1, vaegir_face_older_2],

  ["vaegir_prison_guard", "Prison Guard", "Prison Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_ashwood_pike, itm_battle_fork_1, itm_bardiche, itm_battle_axe, itm_fighting_axe, itm_tab_shield_kite_b,
    itm_studded_leather_coat, itm_lamellar_armor, itm_mail_chausses, itm_iron_greaves, itm_nordic_helmet, itm_nordic_helmet, itm_nordic_helmet, itm_spiked_helmet, itm_leather_gloves],
   def_attrib|level(24), regular_melee(24), knows_athletics_3|knows_shield_2|knows_ironflesh_3, vaegir_face_middle_1, vaegir_face_older_2],

  ["vaegir_castle_guard", "Castle Guard", "Castle Guards", tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_neutral,
   [itm_ashwood_pike, itm_battle_fork_1, itm_bardiche, itm_battle_axe, itm_fighting_axe, itm_tab_shield_kite_d,
    itm_studded_leather_coat, itm_lamellar_armor, itm_mail_chausses, itm_iron_greaves, itm_nordic_helmet, itm_nordic_helmet, itm_nordic_helmet, itm_spiked_helmet, itm_leather_gloves],
   def_attrib|level(24), regular_melee(24), knows_athletics_3|knows_shield_2|knows_ironflesh_3, vaegir_face_middle_1, vaegir_face_older_2],


###########################################################################################################
# IMPERIAL EXPEDITIONARY FORCE
###########################################################################################################

#Ranged Infantry
  ["ief_velites", "Imperial Velites", "Imperial Velites", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_6,
   [itm_javelin, itm_javelin, itm_legion_sword_hoplite, itm_tab_shield_round_a, itm_tab_shield_round_b, 
    itm_legion_helm_01, itm_legion_armor_1, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(10), regular_all(10), knows_ironflesh_1|knows_shield_3|knows_power_strike_1|knows_athletics_3|knows_power_throw_1, rhodok_face_young_1, rhodok_face_young_2],

  ["ief_arcus", "Imperial Arcus", "Imperial Arcus", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_kingdom_6,
   [itm_crossbow, itm_bolts, itm_bolts, itm_legion_dagger, 
    itm_legion_helm_04, itm_legion_armor_1, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(15), regular_crossbow(15), knows_ironflesh_1|knows_shield_1|knows_power_strike_1|knows_athletics_2|knows_power_throw_1, rhodok_face_young_1, rhodok_face_young_2],

  ["ief_akritoi", "Imperial Akritoi", "Imperial Akritois", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_kingdom_6,
   [itm_heavy_crossbow, itm_bolts, itm_bolts, itm_legion_dagger, 
    itm_legion_helm_04, itm_legion_armor_2, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(20), regular_crossbow(20), knows_ironflesh_2|knows_shield_2|knows_power_strike_2|knows_athletics_3|knows_power_throw_1, rhodok_face_young_1, rhodok_face_young_2],

  ["ief_vexillatio", "Imperial Vexillatio", "Imperial Vexillatios", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_6,
   [itm_sniper_crossbow, itm_steel_bolts, itm_legion_dagger, itm_tab_shield_round_e, 
    itm_legion_helm_05, itm_legion_armor_3, itm_black_army_boot_1, itm_black_army_leather_gloves],
   def_attrib|level(25), expert_crossbow(25), knows_ironflesh_3|knows_shield_3|knows_power_strike_3|knows_athletics_4|knows_power_throw_1, rhodok_face_young_1, rhodok_face_young_2],

#Melee Infantry
   #"ief_bastard_brothers":
   # This unit belong to the Imperial Expeditionary Force but they are also random tavern mercenaries.  They are located in the Random Mercenary Troop Section so they will show up in taverns
   
   ["ief_hestati", "Imperial Hestati", "Imperial Hestati", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_6,
    [itm_legion_sword_kopis, itm_tab_shield_pavise_a, itm_tab_shield_pavise_b, itm_javelin, 
     itm_legion_helm_01, itm_legion_armor_1, itm_black_army_boot_1, itm_black_army_leather_gloves],
    def_attrib|level(15), regular_melee(15), knows_ironflesh_2|knows_shield_3|knows_power_strike_2|knows_athletics_3|knows_power_throw_2, rhodok_face_young_1, rhodok_face_young_2],

   ["ief_principes", "Imperial Principes", "Imperial Principes", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_6,
    [itm_legion_sword_kopis, itm_legion_spear_palton, itm_legion_shield_2,
     itm_legion_helm_01, itm_legion_armor_2, itm_legion_greaves, itm_darkgauntlets],
    def_attrib|level(20), regular_melee(20), knows_ironflesh_3|knows_shield_5|knows_power_strike_3|knows_athletics_4|knows_power_throw_2, rhodok_face_middle_1, rhodok_face_middle_2],

   ["ief_triarii", "Imperial Triarii", "Imperial Triarii", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_6,
    [itm_legion_sword_kopis, itm_legion_spear_palton, itm_legion_axe, itm_legion_shield_2,
     itm_legion_helm_03, itm_legion_armor_3, itm_darkgauntlets, itm_darkboots],
    def_attrib|level(30), expert_melee(30), knows_ironflesh_4|knows_shield_6|knows_power_strike_4|knows_athletics_5, rhodok_face_older_1, rhodok_face_older_2],

#Ranged Cavalry
   # "ief_sons_of_deer":  
   # This unit belong to the Imperial Expeditionary Force but they are also random tavern mercenaries.  They are located in the Random Mercenary Troop Section so they will show up in taverns

# Messenger cavalry used by tax couriers and other non-combat dispatch parties.
   ["ief_messenger", "Imperial Messenger", "Imperial Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
    [itm_legion_sword_sica, itm_short_bow, itm_arrows,
     itm_legion_helm_11, itm_legion_armor_1, itm_black_army_boot_1, itm_black_army_leather_gloves,
     itm_courser],
    def_attrib|agi_21|level(25), regular_all(25), knows_riding_7|knows_horse_archery_5|knows_power_draw_5, rhodok_face_middle_1, rhodok_face_middle_2],

   ["sod_ant_messenger", "Antarian Messenger", "Antarian Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
    [itm_sword_medieval_b_small, itm_short_bow, itm_arrows,
     itm_leather_warrior_cap, itm_padded_leather, itm_hide_boots, itm_leather_gloves,
     itm_courser],
    def_attrib|agi_21|level(25), regular_all(25), knows_riding_7|knows_horse_archery_5|knows_power_draw_5, nord_face_younger_1, nord_face_old_2],

   ["sod_mar_messenger", "Marinian Messenger", "Marinian Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
    [itm_sword_medieval_a, itm_light_crossbow, itm_bolts,
     itm_leather_cap, itm_padded_leather, itm_leather_boots, itm_leather_gloves,
     itm_courser],
    def_attrib|agi_21|level(25), regular_melee(25), knows_riding_7|knows_horse_archery_5, rhodok_face_young_1, rhodok_face_young_2],

   ["sod_ade_messenger", "Adenian Messenger", "Adenian Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
    [itm_sword_medieval_a, itm_light_crossbow, itm_bolts,
     itm_skullcap, itm_mail_shirt, itm_mail_chausses, itm_mail_mittens,
     itm_courser],
    def_attrib|agi_21|level(25), regular_melee(25), knows_riding_7|knows_horse_archery_5, swadian_face_young_1, swadian_face_old_2],

   ["sod_vil_messenger", "Villianese Messenger", "Villianese Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
    [itm_sword_khergit_2, itm_short_bow, itm_arrows,
     itm_pilgrim_hood, itm_pilgrim_disguise, itm_black_army_boot_1, itm_black_army_leather_gloves,
     itm_courser],
    def_attrib|agi_21|level(25), regular_all(25), knows_riding_7|knows_horse_archery_5|knows_power_draw_5, villianese_green_young_1, villianese_black_middle_2],

   ["sod_zer_messenger", "Zerrikanian Messenger", "Zerrikanian Messengers", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_ranged, 0, 0, fac_neutral,
    [itm_sword_khergit_2, itm_short_bow, itm_arrows,
     itm_cossack_helm, itm_rabati, itm_khergit_guard_boots, itm_leather_gloves,
     itm_courser],
    def_attrib|agi_21|level(25), regular_all(25), knows_riding_7|knows_horse_archery_5|knows_power_draw_5, khergit_face_young_1, khergit_face_older_2],

#Melee Cavalry
   ["ief_speculatores", "Imperial Speculatore", "Imperial Speculatores", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_kingdom_6,
    [itm_legion_spear_palton, itm_legion_sword_sica, itm_tab_shield_round_b, 
     itm_legion_helm_11, itm_legion_armor_1, itm_black_army_boot_1, itm_black_army_leather_gloves, 
     itm_legion_horse_3],
    def_attrib|level(14), regular_melee(14), knows_riding_3|knows_ironflesh_2|knows_shield_4|knows_power_strike_2, rhodok_face_middle_1, rhodok_face_middle_2],

   ["ief_clibanarii", "Imperial Clibanarii", "Imperial Clibanariis", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_kingdom_6,
    [itm_legion_spear_kamax, itm_legion_sword_sica, itm_tab_shield_round_d, 
     itm_legion_helm_08, itm_legion_armor_2, itm_black_army_boot_1, itm_black_army_leather_gloves, 
     itm_legion_horse_4],
    def_attrib|level(23), regular_melee(23), knows_riding_4|knows_ironflesh_3|knows_shield_5|knows_power_strike_3, rhodok_face_middle_1, rhodok_face_middle_2],

   ["ief_pronoiar", "Imperial Pronoiar", "Imperial Pronoiars", tf_mounted|tf_guarantee_boots|tf_guarantee_gloves|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_kingdom_6,
    [itm_legion_spear_kamax, itm_legion_sword_sica, itm_tab_shield_kite_cav_a, itm_tab_shield_kite_cav_b, 
     itm_legion_helm_09, itm_legion_armor_3, itm_darkgauntlets, itm_darkboots, 
     itm_legion_horse_5],
    def_attrib|level(30), expert_melee(30), knows_riding_5|knows_ironflesh_4|knows_shield_6|knows_power_strike_4, rhodok_face_middle_1, rhodok_face_middle_2],

#Nobility - Cavalry
  ["ief_hospitalier", "Imperial Hospitalier", "Imperial Hospitaliers", tf_mounted|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_horse|tf_guarantee_shield, 0, 0, fac_kingdom_6,
   [itm_legion_sword_sica, itm_legion_spear_kamax, itm_legion_shield_1, 
    itm_legion_helm_10, itm_legion_armor_4, itm_darkgauntlets, itm_legion_greaves, 
    itm_legion_horse_7],
   def_attrib|level(32), expert_melee(32), knows_riding_5|knows_ironflesh_5|knows_power_strike_7|knows_power_throw_2|knows_athletics_3|knows_tactics_2, rhodok_face_older_1, rhodok_face_older_2],

#Nobility - Melee Infantry
   ["ief_akolouthos", "Imperial Akolouthos", "Imperial Akolouthos", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_6,
    [itm_legion_axe, itm_legion_sword_kopis, itm_legion_sword_hoplite, itm_legion_spear_palton, itm_legion_shield_2, 
     itm_legion_helm_03, itm_legion_armor_4, itm_darkgauntlets, itm_legion_greaves],
    def_attrib|level(32), expert_melee(32), knows_ironflesh_5|knows_shield_7|knows_power_strike_5|knows_athletics_6, rhodok_face_older_1, rhodok_face_older_2],

#Nobility - Ranged Infantry
  ["ief_praetorian", "Imperial Praetorian", "Imperial Praetorian", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_kingdom_6,
   [itm_sniper_crossbow, itm_steel_bolts, itm_legion_dagger, itm_legion_shield_1, 
    itm_legion_helm_05, itm_legion_armor_4, itm_legion_greaves, itm_black_army_leather_gloves],
   def_attrib|level(32), expert_crossbow(32), knows_ironflesh_5|knows_shield_5|knows_power_strike_5|knows_athletics_4|knows_power_throw_1, rhodok_face_older_1, rhodok_face_older_2],

#Others
   ["ief_deserter", "Imperial Deserter", "Imperial Deserter", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_deserters,
    [itm_javelin, itm_javelin, itm_legion_sword_hoplite, itm_tab_shield_round_a, itm_tab_shield_round_b, 
     itm_legion_helm_01, itm_legion_armor_1, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(10), regular_all(10), knows_ironflesh_2|knows_shield_3|knows_power_strike_3|knows_athletics_3|knows_power_throw_2, rhodok_face_young_1, rhodok_face_young_2],


############################################################################################################################################################################################
# ANTARIAN KINGDOM
# The Experience troop* (troop1) is located below
############################################################################################################################################################################################

   ["sod_peasant1", "Antarian Recruit", "Antarian Recruits", tf_guarantee_armor, 0, 0, fac_player_supporters_faction,
    [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones,
     itm_leather_cap, itm_felt_hat, itm_felt_hat, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
    def_attrib|level(4), weak_melee(4), 0, nord_face_younger_1, nord_face_old_2],

#Infantry - Melee
   ["sod_ant_regular", "Antarian Regular Infantry", "Antarian Regular Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 1, fac_player_supporters_faction,
    [itm_realbastarda, itm_tab_shield_round_b, itm_tab_shield_round_c, 
     itm_bascinet, itm_haubergeon, itm_mail_boots, itm_leather_gloves],
    def_attrib|level(11), regular_melee(11), knows_ironflesh_1|knows_power_strike_3|knows_shield_1, nord_face_younger_1, nord_face_old_2],

   ["sod_ant_veteran", "Antarian Veteran Infantry", "Antarian Veteran Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 1, fac_player_supporters_faction,
    [itm_shortened_military_scythe,
     itm_saladed, itm_antplate6, itm_mail_boots, itm_mail_mittens],
    def_attrib|level(17), regular_melee(17), knows_ironflesh_2|knows_power_strike_4|knows_shield_1, nord_face_younger_1, nord_face_old_2],

   ["sod_ant_elite", "Antarian Elite Infantry", "Antarian Elite Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 1, fac_player_supporters_faction,
    [itm_flamberge, itm_shortened_military_scythe,
     itm_saladed, itm_plate_armor2, itm_iron_greaves, itm_gauntlets],
    def_attrib|level(25), expert_melee(25), knows_ironflesh_3|knows_power_strike_6|knows_shield_1, nord_face_middle_1, nord_face_older_2],

#Infantry - Ranged
   ["sod_ant_javelinman", "Antarian Javelinman", "Antarian Javelinmen", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
   [itm_jarid, itm_jarid, itm_jarid, itm_sword_medieval_b, itm_sword_medieval_b_small, itm_sword_medieval_a, itm_tab_shield_kite_cav_a, 
     itm_leather_warrior_cap, itm_skullcap, itm_studded_leather_coat, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(12), regular_javelinmen(12), knows_ironflesh_1|knows_power_throw_3|knows_shield_3|knows_power_strike_1|knows_athletics_3, nord_face_younger_1, nord_face_old_2],

   ["sod_ant_trained_javelinman", "Antarian Trained Javelinman", "Antarian Trained Javelinmen", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
   [itm_ant_angon, itm_ant_angon, itm_ant_angon, itm_sword_medieval_c, itm_sword_medieval_c_small, itm_antshield2, 
     itm_spiked_helmet, itm_ant_lthr_coat, itm_mail_boots, itm_mail_mittens],
    def_attrib|level(18), expert_javelinmen(18), knows_ironflesh_2|knows_power_throw_5|knows_shield_4|knows_power_strike_2|knows_athletics_4, nord_face_middle_1, nord_face_older_2],

#Cavalry - Melee
   ["sod_ant_scout", "Antarian Scout", "Antarian Scouts", tf_mounted|tf_guarantee_horse|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_spear, itm_sword_medieval_b_small, itm_tab_shield_round_b,
     itm_leather_warrior_cap, itm_skullcap, itm_padded_leather, itm_leather_gloves, itm_hide_boots, 
     itm_sumpter_horse, itm_saddle_horse],
    def_attrib|level(15), regular_melee(15), knows_ironflesh_1|knows_power_strike_1|knows_riding_2, nord_face_younger_1, nord_face_old_2],

   ["sod_ant_cavalry", "Antarian Cavalry", "Antarian Cavalry", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_sword_of_war, itm_war_spear, itm_nordic_sword, itm_antshield2, 
     itm_segmented_helmet, itm_mail_shirt, itm_mail_mittens, itm_mail_boots,
     itm_courser, itm_hunter],
    def_attrib|level(20), regular_melee(20), knows_ironflesh_2|knows_power_strike_3|knows_riding_3, nord_face_younger_1, nord_face_old_2],

#Noble (Melee Infantry)
   ["sod_ant_noble", "Antarian Noble", "Antarian Nobles", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_bastard_sword_a, itm_antshield2,
     itm_anthelm1, itm_antplate1, itm_darkboots, itm_antgaunt2],
    def_attrib|level(15), regular_melee(15), knows_ironflesh_1|knows_power_strike_1|knows_shield_1, nord_face_younger_1, nord_face_old_2],

   ["sod_ant_guard", "Antarian Guard", "Antarian Guards", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_swadianespadon, itm_bastard_sword_b, itm_antshield,
     itm_anthelm1, itm_antplate4, itm_darkboots, itm_antgaunt2],
    def_attrib|level(20), regular_melee(20), knows_ironflesh_3|knows_power_strike_3|knows_shield_3, nord_face_middle_1, nord_face_older_2],

   ["sod_ant_honor_guard", "Antarian Honor Guard", "Antarian Honor Guards", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_swadianespadon, itm_realbastarde, itm_antshield,
     itm_anthelm1, itm_antplate2, itm_antplate3, itm_antboots2, itm_antgaunt2],
    def_attrib|level(28), regular_melee(28), knows_ironflesh_4|knows_power_strike_4|knows_shield_4, nord_face_middle_1, nord_face_older_2],



############################################################################################################################################################################################
# MARINIAN KINGDOM
# The Experience troop* (troop1) is located below
############################################################################################################################################################################################

   ["sod_peasant2", "Marinian Recruit", "Marinian Recruits", tf_guarantee_armor, 0, 0, fac_player_supporters_faction,
    [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones,
     itm_leather_cap, itm_felt_hat, itm_felt_hat, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
    def_attrib|level(4), weak_melee(4), 0, rhodok_face_young_1, rhodok_face_young_2],

#Infantry - Melee
   ["sod_mar_conscript", "Marinian Conscript Infantry", "Marinian Conscript Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_small_pole_axe, itm_sword_medieval_a, itm_tab_shield_pavise_a,
     itm_kettle_hat_b, itm_padded_leather, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(10), regular_melee(10), knows_ironflesh_2|knows_power_strike_2, rhodok_face_young_1, rhodok_face_young_2],

   ["sod_mar_regular", "Marinian Regular Infantry", "Marinian Regular Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_realhalberda, itm_sword_medieval_b_small, itm_tab_shield_pavise_b,
     itm_kettle_hat_b, itm_studded_leather_coat, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(15), regular_melee(15), knows_ironflesh_3|knows_power_strike_3|knows_shield_1, rhodok_face_young_1, rhodok_face_young_2],

   ["sod_mar_veteran", "Marinian Veteran Infantry", "Marinian Veteran Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_realglaive, itm_sword_medieval_b, itm_tab_shield_pavise_c,
     itm_marhelm2, itm_marchain2, itm_marboots1, itm_margloves2],
    def_attrib|level(20), regular_melee(20), knows_ironflesh_4|knows_power_strike_4|knows_shield_2, rhodok_face_young_1, rhodok_face_older_2],

   ["sod_mar_elite", "Marinian Elite Infantry", "Marinian Elite Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_small_pole_axe, itm_sword_medieval_c, itm_tab_shield_pavise_d,
     itm_marhelm3, itm_marchain3, itm_marboots3, itm_margloves2],
    def_attrib|level(25), expert_melee(25), knows_ironflesh_5|knows_power_strike_5|knows_shield_3, rhodok_face_young_1, rhodok_face_older_2],

#Infantry - Ranged
   ["sod_mar_crossbowman", "Marinian Crossbowman", "Marinian Crossbowmen", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
    [itm_crossbow, itm_bolts, itm_bolts, itm_sword_medieval_a, itm_falchion, itm_club_with_spike_head, itm_tab_shield_pavise_a, 
     itm_kettle_hat_b, itm_leather_jerkin, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(10), regular_crossbow(10), knows_ironflesh_2|knows_power_draw_1|knows_shield_1|knows_athletics_2, rhodok_face_young_1, rhodok_face_young_2],

   ["sod_mar_trained_crossbowman", "Marinian Trained Crossbowman", "Marinian Trained Crossbowmen", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
    [itm_crossbow, itm_bolts, itm_bolts, itm_sword_medieval_a, itm_sword_medieval_b_small, itm_club_with_spike_head, itm_tab_shield_pavise_a, 
     itm_kettle_hat_b, itm_padded_leather, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(15), regular_crossbow(15), knows_ironflesh_3|knows_power_draw_2|knows_shield_2|knows_athletics_3, rhodok_face_young_1, rhodok_face_young_2],

   ["sod_mar_elite_crossbowman", "Marinian Elite Crossbowman", "Marinian Elite Crossbowmen", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
    [itm_heavy_crossbow, itm_bolts, itm_bolts, itm_sword_medieval_a, itm_sword_medieval_b_small, itm_fighting_pick, itm_club_with_spike_head, itm_tab_shield_pavise_a, itm_tab_shield_pavise_b, itm_tab_shield_pavise_c, 
     itm_kettle_hat_b, itm_heraldic_studded_leather_coat, itm_mail_boots, itm_leather_gloves],
    def_attrib|level(20), regular_crossbow(20), knows_ironflesh_4|knows_power_draw_3|knows_shield_3|knows_athletics_4, rhodok_face_middle_1, rhodok_face_older_2],

   ["sod_mar_sharpshooter", "Marinian Sharpshooter", "Marinian Sharpshooters", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
    [itm_sniper_crossbow, itm_steel_bolts, itm_bolts, itm_sword_medieval_b, itm_military_pick, itm_tab_shield_pavise_c, 
     itm_byzantion_helmet_a, itm_heraldic_mail_shirt, itm_mail_boots, itm_leather_gloves],
    def_attrib|level(25), expert_crossbow(25), knows_ironflesh_5|knows_power_draw_4|knows_shield_4|knows_athletics_6, rhodok_face_middle_1, rhodok_face_older_2],

#Cavalry - Melee
   ["sod_mar_scout", "Marinian Scout", "Marinian Scouts", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_spear, itm_sword_medieval_a, itm_sword_medieval_b_small, itm_tab_shield_round_b,
     itm_leather_cap, itm_padded_leather, itm_leather_boots, itm_leather_gloves,
     itm_sumpter_horse, itm_saddle_horse],
    def_attrib|level(14), regular_melee(14), knows_ironflesh_1|knows_power_strike_1|knows_riding_3, rhodok_face_young_1, rhodok_face_young_2],

#Noble - Ranged Infantry
   ["sod_mar_mercenary", "Marinian Mercenary", "Marinian Mercenaries", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 4, fac_player_supporters_faction,
    [itm_crossbow, itm_steel_bolts, itm_steel_bolts, itm_realpike, itm_realhalberdc, itm_realhalberda,
     itm_marhelm1, itm_marchain1, itm_marboots1, itm_darkgauntlets],
    def_attrib|level(15), regular_crossbow(15), knows_ironflesh_3|knows_power_strike_2|knows_shield_1|knows_athletics_1, rhodok_face_young_1, rhodok_face_young_2],

   ["sod_mar_landsknecht", "Marinian Landsknecht", "Marinian Landsknechts", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_heavy_crossbow, itm_steel_bolts, itm_steel_bolts, itm_sword_medieval_b, itm_tab_shield_pavise_c, 
     itm_marhelm2, itm_marchain2, itm_darkboots, itm_darkgauntlets],
    def_attrib|level(20), regular_crossbow(20), knows_ironflesh_4|knows_power_strike_3|knows_shield_2|knows_athletics_2, rhodok_face_middle_1, rhodok_face_older_2],

   ["sod_mar_condottieri", "Marinian Condottieri", "Marinian Condottieri", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_sniper_crossbow, itm_steel_bolts, itm_steel_bolts, itm_sword_medieval_c, itm_tab_shield_pavise_d, 
     itm_marhelm3, itm_marchain3, itm_marboots3, itm_margloves2],
    def_attrib|level(27), expert_crossbow(27), knows_ironflesh_5|knows_power_strike_4|knows_shield_3|knows_athletics_4, rhodok_face_middle_1, rhodok_face_older_2],



############################################################################################################################################################################################
# ADENIAN KINGDOM
# The Experience troop* (troop1) is located below
############################################################################################################################################################################################

   ["sod_peasant3", "Adenian Recruit", "Adenian Recruits", tf_guarantee_armor, 0, 0, fac_player_supporters_faction,
    [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones,
     itm_leather_cap, itm_felt_hat, itm_felt_hat, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
    def_attrib|level(4), weak_melee(4), 0, swadian_face_younger_1, swadian_face_middle_2],

#Infatry - Melee
   ["sod_ade_regular", "Adenian Regular Infantry", "Adenian Regular Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_sword_medieval_b_small, itm_tab_shield_round_b,
     itm_skullcap, itm_red_gambeson, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(10), regular_melee(10), knows_ironflesh_1|knows_power_strike_1, swadian_face_younger_1, swadian_face_middle_2],

   ["sod_ade_veteran", "Adenian Veteran Infantry", "Adenian Veteran Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_sword_medieval_b_small, itm_tab_shield_round_b,
     itm_footman_helmet, itm_padded_leather, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(15), regular_melee(15), knows_ironflesh_2|knows_power_strike_2|knows_shield_1, swadian_face_young_1, swadian_face_old_2],

   ["sod_ade_elite", "Adenian Elite Infantry", "Adenian Elite Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_sword_medieval_c, itm_sword_medieval_c_small, itm_tab_shield_kite_c, itm_mace_3,
     itm_guard_helmet, itm_segmented_helmet, itm_heraldic_mail_with_surcoat, itm_mail_boots, itm_leather_boots, itm_mail_mittens, itm_leather_gloves],
    def_attrib|level(20), regular_melee(20), knows_ironflesh_3|knows_power_strike_3|knows_shield_2, swadian_face_middle_1, swadian_face_old_2],

#Infantry - Ranged
   ["sod_ade_archer", "Adenian Archer", "Adenian Archers", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
    [itm_arrows, itm_short_bow, itm_short_bow, itm_hunting_bow, itm_one_handed_war_axe_a,
     itm_leather_cap, itm_red_gambeson, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(9), regular_archer(9), knows_power_draw_1|knows_athletics_1, swadian_face_younger_1, swadian_face_middle_2],

   ["sod_ade_veteran_archer", "Adenian Veteran Archer", "Adenian Veteran Archers", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
    [itm_arrows, itm_short_bow, itm_nomad_bow, itm_nomad_bow, itm_one_handed_war_axe_b,
     itm_skullcap, itm_leather_vest, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(14), regular_archer(14), knows_ironflesh_1|knows_power_draw_2|knows_athletics_1, swadian_face_young_1, swadian_face_old_2],

   ["sod_ade_elite_archer", "Adenian Elite Archer", "Adenian Elite Archers", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 2, fac_player_supporters_faction,
    [itm_arrows, itm_strong_bow, itm_nomad_bow, itm_one_handed_battle_axe_a, itm_tab_shield_kite_c,
     itm_mail_coif, itm_leather_vest, itm_leather_boots, itm_leather_gloves],
    def_attrib|level(19), regular_archer(19), knows_ironflesh_2|knows_power_draw_3|knows_athletics_2, swadian_face_middle_1, swadian_face_old_2],

#Cavalry - Melee
   ["sod_ade_light", "Adenian Light Cavalry", "Adenian Light Cavalry", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_sword_medieval_a, itm_steel_shield, itm_spear,
     itm_war_helm, itm_mail_shirt, itm_mail_chausses, itm_mail_mittens,
     itm_hunter, itm_brown_hunter, itm_hunter_c, itm_hunting_horse_seven],
    def_attrib|level(15), regular_melee(15), knows_riding_3|knows_ironflesh_1|knows_power_strike_1|knows_shield_2, swadian_face_young_1, swadian_face_old_2],

   ["sod_ade_medium", "Adenian Medium Cavalry", "Adenian Medium Cavalry", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_lance, itm_lance, itm_tab_shield_kite_cav_b,
     itm_old_great_helm, itm_mail_hauberk, itm_mail_chausses, itm_mail_mittens,
     itm_warhorse],
    def_attrib|level(22), regular_melee(22), knows_riding_4|knows_ironflesh_2|knows_power_strike_2|knows_shield_2, swadian_face_young_1, swadian_face_old_2],

   ["sod_ade_heavy", "Adenian Heavy Cavalry", "Adenian Heavy Cavalry", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_heavy_lance, itm_bastard_sword_b, itm_morningstar, itm_sword_medieval_c, itm_tab_shield_heater_cav_b,
     itm_coat_of_plates, itm_cuir_bouilli, itm_mail_with_surcoat, itm_mail_chausses, itm_iron_greaves, itm_gauntlets, itm_iron_greaves, itm_war_helm,
     itm_charger],
    def_attrib|level(26), regular_melee(26), knows_riding_5|knows_ironflesh_3|knows_power_strike_4|knows_shield_3, swadian_face_middle_1, swadian_face_older_2],

#Noble - Melee Cavalry
   ["sod_ade_sqire", "Adenian Squire", "Adenian Squires", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_spiked_mace, itm_two_handed_axe, itm_sword_viking_1, itm_shield_heater_generic_a,
     itm_shield_heater_generic_c, itm_shield_heater_generic_d, itm_shield_heater_generic_g, itm_shield_heater_generic_j, itm_shield_heater_lionel, itm_shield_heater_normandy, itm_shield_kite_bors, itm_shield_heater_anklin,
     itm_bascinetnasal, itm_mail_hauberk, itm_mail_boots, itm_mail_mittens,
     itm_warhorse],
    def_attrib|level(16), regular_melee(16), knows_riding_4|knows_ironflesh_2|knows_power_strike_2|knows_shield_1, swadian_face_younger_1, swadian_face_middle_2],

   ["sod_ade_knight", "Adenian Knight", "Adenian Knights", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_nord_battle_axe, itm_fighting_axe, itm_lance, 
     itm_shield_heater_generic_a, itm_shield_heater_generic_c, itm_shield_heater_generic_d, itm_shield_heater_generic_g, itm_shield_heater_generic_j, itm_shield_heater_lionel, itm_shield_heater_normandy, itm_shield_kite_bors, itm_shield_heater_anklin,
     itm_coat_of_plates, itm_mail_boots, itm_gauntlets, itm_pigface, itm_pigfacec,
     itm_warhorse_sc2_rtw3, itm_warhorse_sc2_rtw2, itm_warhorse_po1_rtw3, itm_warhorse_po2_rtw3, itm_warhorse_maw_b08, itm_warhorse_maw_b05, itm_warhorse_hre_rtw3, itm_warhorse_den_rtw2, itm_warhorse_b],
    def_attrib|level(23), regular_melee(23), knows_riding_5|knows_ironflesh_3|knows_power_strike_3|knows_shield_2, swadian_face_middle_1, swadian_face_old_2],

   ["sod_ade_magnate", "Adenian Magnate", "Adenian Magnates", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_talak_lance, itm_bastard_sword_b, itm_morningstar, itm_sword_medieval_c,
     itm_shield_heater_generic_a, itm_shield_heater_generic_c, itm_shield_heater_generic_d, itm_shield_heater_generic_g, itm_shield_heater_generic_j, itm_shield_heater_lionel, itm_shield_heater_normandy, itm_shield_kite_bors, itm_shield_heater_anklin,
     itm_plate_armor2, itm_mail_boots, itm_gauntlets, itm_toadhelmet, itm_pigfaceb,
     itm_scorpioncharger, itm_whitebirdongreencharger, itm_whitedeercharger, itm_redandyellowbgnorthbow, itm_darktealthreecircle, itm_blueflamemoon, itm_blackdotwhitered, itm_tribowred, itm_goldbaseblackorament, itm_ravisaris, itm_whisparia, itm_goldturqoisehorsebanner, itm_lazarith, itm_nishra],
    def_attrib|level(27), regular_melee(27), knows_riding_6|knows_ironflesh_4|knows_power_strike_5|knows_shield_3, swadian_face_middle_1, swadian_face_old_2],



############################################################################################################################################################################################
# VILLIANESE KINGDOM
# The Experience troop* (troop1) is located below
############################################################################################################################################################################################

   ["sod_peasant4", "Villianese Recruit", "Villianese Recruits", tf_guarantee_armor, 0, 0, fac_player_supporters_faction,
    [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones, itm_hunting_bow, itm_arrows, 
     itm_common_hood, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
    def_attrib|level(4), weak_melee(4), 0, villianese_green_young_1, villianese_black_old_2],

#Infantry - Melee
   ["sod_vil_regular", "Villianese Regular Infantry", "Villianese Regular Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_sword_khergit_1, itm_sword_khergit_2, itm_tab_shield_pavise_b,
     itm_black_hood, itm_vilarmor_5, itm_vilarmor_6, itm_black_army_boot_1, itm_black_army_leather_gloves],
    def_attrib|level(10), regular_melee(10), knows_ironflesh_2|knows_power_strike_3|knows_shield_1|knows_athletics_4, villianese_black_young_1, villianese_black_young_2],

   ["sod_vil_veteran", "Villianese Veteran Infantry", "Villianese Veteran Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_sword_khergit_2, itm_sword_khergit_3, itm_tab_shield_pavise_c,
     itm_villhelm1, itm_helmet_with_neckguard, itm_vilarmor_9, itm_vilarmor_7, itm_mail_boots, itm_black_army_boot_1, itm_black_army_leather_gloves],
    def_attrib|level(15), regular_melee(15), knows_ironflesh_4|knows_power_strike_5|knows_shield_2|knows_athletics_6, villianese_black_middle_1, villianese_black_middle_2],

   ["sod_vil_elite", "Villianese Elite Infantry", "Villianese Elite Infantry", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_sword_khergit_3, itm_tab_shield_pavise_d,
     itm_guard_helmet, itm_spiked_helmet, itm_mail_coif, itm_vilarmor_8, itm_mail_mittens, itm_mail_boots],
    def_attrib|level(25), regular_melee(25), knows_ironflesh_6|knows_power_strike_6|knows_shield_4|knows_athletics_8, villianese_black_middle_1, villianese_black_old_2],

#Infantry - Ranged
   ["sod_vil_longbowman", "Villianese Longbowman", "Villianese Longbowmen", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor, 0, 2, fac_player_supporters_faction,
    [itm_long_bow, itm_arrows, itm_arrows, itm_sword_khergit_1, 
     itm_vilarmor_1, itm_ragged_outfit, itm_leather_gloves, itm_hide_boots],
    def_attrib|level(10), regular_archer(10), knows_power_draw_2|knows_ironflesh_1|knows_athletics_3, villianese_green_young_1, villianese_black_young_2],

   ["sod_vil_veteran_longbowman", "Villianese Veteran Longbowman", "Villianese Veteran Longbowmen", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 2, fac_player_supporters_faction,
    [itm_long_bow, itm_barbed_arrows, itm_barbed_arrows, itm_sword_khergit_2, 
     itm_vilhelm5, itm_vilarmor_2, itm_leather_gloves, itm_hide_boots],
    def_attrib|level(16), regular_archer(16), knows_power_draw_3|knows_ironflesh_2|knows_athletics_4, villianese_green_young_1, villianese_black_middle_2],

   ["sod_vil_elite_longbowman", "Villianese Elite Longowman", "Villianese Elite Longbowmen", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 2, fac_player_supporters_faction,
    [itm_long_bow, itm_war_bow, itm_bodkin_arrows, itm_bodkin_arrows, itm_sword_khergit_3,
     itm_villhelm1, itm_vilhelm5, itm_vilarmor_9, itm_vilarmor_3, itm_leather_gloves, itm_mail_boots, itm_leather_boots],
    def_attrib|level(21), regular_archer(21), knows_power_draw_4|knows_ironflesh_3|knows_athletics_5, villianese_green_middle_1, villianese_black_middle_2],

   ["sod_vil_sharpshooter", "Villianese Sharpshooter", "Villianese Sharpshooters", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 2, fac_player_supporters_faction,
    [itm_war_bow, itm_bodkin_arrows, itm_bodkin_arrows, itm_sword_khergit_3,
     itm_villhelm2, itm_guard_helmet, itm_spiked_helmet, itm_vilarmor_10, itm_vilarmor_4, itm_mail_mittens, itm_leather_gloves, itm_mail_boots],
    def_attrib|level(27), expert_archer(27), knows_power_draw_5|knows_ironflesh_4|knows_athletics_7, villianese_green_middle_1, villianese_black_old_2],

#Cavalry - Melee
   ["sod_vil_scout", "Villianese Scout", "Villianese Scouts", tf_mounted|tf_guarantee_horse|tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_nomad_bow, itm_short_bow, itm_barbed_arrows, itm_spear, itm_sword_khergit_1, itm_sword_khergit_2, itm_tab_shield_small_round_a, 
     itm_pilgrim_hood, itm_pilgrim_disguise, itm_black_army_leather_gloves, itm_black_army_boot_1, itm_hide_boots, 
     itm_courser],
    def_attrib|level(14), regular_all(14), knows_riding_3|knows_ironflesh_1|knows_horse_archery_3|knows_power_draw_2|knows_power_strike_1, villianese_green_young_1, villianese_black_middle_2],

#Noble - Ranged Infantry
   ["sod_vil_noble", "Villianese Noble", "Villianese Nobles", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_long_bow, itm_bodkin_arrows, itm_sword_khergit_4, itm_sword_khergit_3, itm_villshield,
     itm_vilarmor_9, itm_villboots1, itm_villhelm1, itm_villgloves1],
    def_attrib|level(15), regular_archer(15), knows_ironflesh_1|knows_power_draw_3|knows_power_strike_1|knows_athletics_3|knows_shield_2, villianese_black_young_1, villianese_blue_middle_2],

   ["sod_vil_chief", "Villianese Chief", "Villianese Chiefs", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_war_bow, itm_bodkin_arrows, itm_bodkin_arrows, itm_bastard_sword_a, itm_executionner_axe_, itm_villshield,
     itm_vilarmor_10, itm_villboots2, itm_villhelm2, itm_villgloves2],
    def_attrib|level(20), regular_archer(20), knows_ironflesh_3|knows_athletics_6|knows_power_draw_5|knows_power_strike_2|knows_shield_4, villianese_black_middle_1, villianese_blue_middle_2],

   ["sod_vil_high_chief", "Villianese High Chief", "Villianese High Chiefs", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_war_bow, itm_bodkin_arrows, itm_bodkin_arrows, itm_raider_battle_axe, itm_onehandedwarhammer, itm_noble_greatsword, itm_villshield,
     itm_vilarmor_11, itm_vilarmor_12, itm_villboots2, itm_villhelm4, itm_villgloves2],
    def_attrib|level(28), expert_archer(28), knows_ironflesh_5|knows_athletics_8|knows_power_draw_7|knows_power_strike_3|knows_shield_6, villianese_black_middle_1, villianese_blue_old_2],



############################################################################################################################################################################################
# ZERRIKANIAN KINGDOM
# The Experience troop* (troop1) is located below
# Zerrikanian faces of troops are intentionally different to show background of slavery recruitment
############################################################################################################################################################################################

   ["sod_peasant5", "Zerrikanian Recruit", "Zerrikanian Recruits", tf_guarantee_armor, 0, 0, fac_player_supporters_faction,
    [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones,
     itm_serpent_host_turban_1, itm_leather_cap, itm_slave_neck_chain, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
    def_attrib|level(4), weak_melee(4), 0, man_face_middle_1, man_face_old_2],

#Infantry - Melee
   ["sod_zer_1_infantry", "Zerrikanian Militia", "Zerrikanian Militia", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_one_handed_war_axe_b, itm_club_with_spike_head, itm_mace_6, itm_tab_shield_round_b,
     itm_shahi, itm_magyar_helmet_a, itm_leather_jerkin, itm_light_leather, itm_leather_boots, itm_nomad_boots, itm_leather_gloves],
    def_attrib|level(9), regular_melee(9), knows_ironflesh_1|knows_athletics_1, rhodok_face_younger_1, rhodok_face_old_2],

   ["sod_zer_2_infantry", "Zerrikanian Axeman", "Zerrikanian Axemen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_one_handed_battle_axe_a, itm_one_handed_battle_axe_c, itm_straw_shield,
     itm_helm_rajput_c, itm_rabati, itm_rabati, itm_cossack_armor, itm_khergit_guard_boots, itm_leather_gloves, itm_black_army_leather_gloves],
    def_attrib|level(14), regular_melee(14), knows_ironflesh_2|knows_power_strike_2|knows_athletics_2, khergit_face_middle_1, khergit_face_older_2],

   ["sod_zer_3_infantry", "Zerrikanian Hardened Axeman", "Zerrikanian Hardened Axemen", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 1, fac_player_supporters_faction,
    [itm_berdiche_axe, itm_decor_red2_shield,
     itm_zerk_redmask, itm_zerk_red_helm, itm_zerk_red_helm, itm_zerk_red_armor, itm_zerk_red_boot, itm_mail_mittens],
    def_attrib|level(20), regular_melee(20), knows_ironflesh_3|knows_power_strike_3|knows_athletics_5, khergit_face_middle_1, khergit_face_older_2],

#Infantry - Ranged
   ["sod_zer_1_archer", "Zerrikanian Short Bowman", "Zerrikanian Short Bowman", tf_guarantee_ranged|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 2, fac_player_supporters_faction,
    [itm_short_bow, itm_arrows, itm_dagger, itm_tab_shield_small_round_a,
     itm_fur_hat, itm_sipahi_helmet_b, itm_leather_steppe_cap_a, itm_leather_steppe_cap_c, itm_leather_warrior_cap, itm_nomad_vest, itm_ragged_outfit, itm_nomad_boots, itm_hide_boots, itm_leather_gloves],
    def_attrib|level(10), regular_archer(10), knows_power_draw_2|knows_ironflesh_1|knows_athletics_2, vaegir_face_young_1, vaegir_face_middle_2],

   ["sod_zer_2_archer", "Zerrikanian Dvor Archer", "Zerrikanian Dvor Archers", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 2, fac_player_supporters_faction,
    [itm_khergit_bow, itm_strong_bow, itm_bodkin_arrows, itm_bodkin_arrows, itm_sword_khergit_4,
     itm_dvor_archer_mask1, itm_dvor_archer_helm_2, itm_dvor_archer_helm_1, itm_dvor_archer_helm_1, itm_dvor_archer_armor, itm_dvor_archer_boot, itm_leather_gloves],
    def_attrib|level(19), regular_archer(19), knows_power_draw_3|knows_ironflesh_2|knows_athletics_4, vaegir_face_middle_1, vaegir_face_older_2],

#Cavalry
   ["sod_zer_1_cavalry", "Zerrikanian Scout", "Zerrikanian Scouts", tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_mace_3, itm_light_lance, itm_short_bow, itm_arrows, itm_straw_shield,
     itm_cossack_helm, itm_rabati, itm_cossack_armor, itm_khergit_guard_boots, itm_leather_gloves,
     itm_rok_saddle_horse1, itm_rok_saddle_horse2],
    def_attrib|level(14), regular_all(14), knows_riding_4|knows_ironflesh_2|knows_horse_archery_2|knows_power_draw_1|knows_power_strike_1, khergit_face_young_1, khergit_face_older_2],

   ["sod_zer_1_cavalry_archer", "Zerrikanian Mounted Archer", "Zerrikanian Mounted Archers", tf_guarantee_ranged|tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_khergit_bow, itm_strong_bow, itm_khergit_arrows, itm_sword_khergit_4, itm_bashkir_shield,
     itm_bashkir_helm1, itm_bashkir_helm2, itm_bashkir_helm3, itm_bashkir_armor, itm_bashkir_boots, itm_black_army_leather_gloves,
     itm_rok_bashkir_hunter, itm_rok_bashkir_courser],
    def_attrib|level(21), expert_archer(21), knows_riding_7|knows_ironflesh_2|knows_horse_archery_6|knows_power_draw_5|knows_shield_2|knows_power_strike_1, khergit_face_middle_1, khergit_face_older_2],

   ["sod_zer_2_cavalry", "Zerrikanian Harvester", "Zerrikanian Harvesters", tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_talak_mace, itm_mace_7, itm_morningstar, itm_one_handed_battle_axe_c, itm_jousting_lance, itm_throwing_decor_hammer, itm_decor_colors1_shield, itm_decor_colors2_shield, itm_decor_bluegreen_shield, 
     itm_white_helm, itm_white_mask, itm_white_armor, itm_white_boots, itm_black_army_leather_gloves,
     itm_rok_kalmuck_horse],
    def_attrib|level(19), regular_all(19), knows_riding_6|knows_ironflesh_2|knows_horse_archery_4|knows_power_throw_2|knows_power_strike_2, khergit_face_young_1, khergit_face_older_2],

   ["sod_zer_3_cavalry", "Zerrikanian Reaper", "Zerrikanian Reapers", tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 3, fac_player_supporters_faction,
    [itm_talak_warhammer, itm_mace_pear, itm_morningstar, itm_one_handed_battle_axe_c, itm_jousting_lance, itm_throwing_decor_hammer, itm_decor_red1_shield, itm_decor_red2_shield,
     itm_oprichnik_mask1, itm_oprichnik_mask2, itm_oprichnik_helm, itm_oprichnik_armor, itm_oprichnik_boots, itm_mail_mittens, 
     itm_rok_oprichnik_charger],
    def_attrib|level(27), expert_melee(27), knows_riding_8|knows_shield_3|knows_horse_archery_8|knows_power_throw_8|knows_ironflesh_4|knows_power_strike_5, khergit_face_middle_1, khergit_face_older_2],

#Nobles
   ["sod_zer_1_noble", "Zerrikanian Boyar Son", "Zerrikanian Boyar Son's", tf_guarantee_ranged|tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_nomad_bow, itm_khergit_arrows, itm_bastard_sword_a, itm_gold_jarid, itm_light_lance, 
     itm_decor_aqua_shield, itm_decor_bluegreen_shield, itm_decor_redblue_shield, itm_decor_red1_shield, itm_decor_red2_shield, itm_decor_colors1_shield, itm_decor_colors2_shield, itm_decor_colors3_shield, 
     itm_zerrikanian_noble_helmet, itm_boyar_son_armor1, itm_noble_padded_leather, itm_dynasty_tabard, itm_white_boots, itm_mail_mittens,
     itm_rok_boyar_son_warhorse],
    def_attrib|level(15), regular_all(15), knows_riding_5|knows_ironflesh_4|knows_horse_archery_4|knows_power_throw_2|knows_power_draw_4|knows_power_strike_1, vaegir_face_young_1, vaegir_face_old_2],

   ["sod_zer_2_noble", "Zerrikanian Boyar", "Zerrikanian Boyars", tf_guarantee_ranged|tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 4, fac_player_supporters_faction,
    [itm_khergit_bow, itm_khergit_arrows, itm_realbastarde, itm_gold_jarid, itm_heavy_lance, itm_boyar_shield,
     itm_boyar_helm, itm_boyar_armor2, itm_boyar_armor1, itm_mail_boots, itm_scale_gauntlets,
     itm_rok_boyar_warhorse, itm_rok_boyar_charger],
    def_attrib|level(20), regular_all(20), knows_riding_7|knows_ironflesh_5|knows_horse_archery_5|knows_shield_2|knows_power_throw_3|knows_power_draw_5|knows_power_strike_2, swadian_face_young_1, swadian_face_old_2],

   ["sod_zer_3_noble", "Zerrikanian Dvor", "Zerrikanian Dvors", tf_guarantee_ranged|tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 4, fac_player_supporters_faction,
    [itm_strong_bow, itm_khergit_arrows, itm_cimitar, itm_great_lancec, itm_gold_jarid, 
     itm_decor_colors1_shield, itm_decor_colors2_shield, itm_decor_colors3_shield, 
     itm_dvor1_mask, itm_dvor2_mask, itm_dvor_lamellar1, itm_dvor_lamellar2, itm_black_greaves, itm_darkgauntlets,
     itm_rok_dvor1_charger, itm_rok_dvor2_charger, itm_rok_dvor3_charger],
    def_attrib|level(28), expert_all(28), knows_riding_8|knows_ironflesh_5|knows_horse_archery_6|knows_shield_3|knows_power_throw_5|knows_power_draw_6|knows_power_strike_3, swadian_face_middle_1, swadian_face_older_2],
	
###########################################################################################################
# ############################################# ZEALOTS ###########################################
###########################################################################################################

   ["sod_ant_honor_guard1", "Antarian Zealous Honor Guard*", "Antarian Zealous Honor Guards*", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
    [itm_swadianespadon, itm_realbastarde, itm_antshield,
     itm_anthelm1, itm_antplate2, itm_antplate3, itm_antboots2, itm_antgaunt2],
    def_attrib|level(30), expert_melee(30), knows_ironflesh_4|knows_power_strike_4|knows_shield_4, nord_face_middle_1, nord_face_older_2],

   ["sod_mar_condottieri1", "Marinian Zealous Condottieri*", "Marinian Zealous Condottieri*", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_player_supporters_faction,
    [itm_sniper_crossbow, itm_steel_bolts, itm_steel_bolts, itm_sword_medieval_c, itm_tab_shield_pavise_d, 
     itm_marhelm3, itm_marchain3, itm_marboots3, itm_margloves2],
    def_attrib|level(30), expert_crossbow(30), knows_ironflesh_5|knows_power_strike_4|knows_shield_3|knows_athletics_4, rhodok_face_middle_1, rhodok_face_older_2],

   ["sod_ade_magnate1", "Adenian Zealous Magnate*", "Adenian Zealous Magnates*", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_player_supporters_faction,
    [itm_talak_lance, itm_bastard_sword_b, itm_morningstar, itm_sword_medieval_c,
     itm_plate_armor2, itm_mail_boots, itm_gauntlets, itm_toadhelmet, itm_pigfaceb, itm_shield_heater_generic_a, itm_shield_heater_generic_c, itm_shield_heater_generic_d, itm_shield_heater_generic_g, itm_shield_heater_generic_j, itm_shield_heater_lionel, itm_shield_heater_normandy, itm_shield_kite_bors, itm_shield_heater_anklin,
     itm_scorpioncharger, itm_whitebirdongreencharger, itm_whitedeercharger, itm_redandyellowbgnorthbow, itm_darktealthreecircle, itm_blueflamemoon, itm_blackdotwhitered, itm_tribowred, itm_goldbaseblackorament, itm_ravisaris, itm_whisparia, itm_goldturqoisehorsebanner, itm_lazarith, itm_nishra],
   def_attrib|level(30), expert_melee(30), knows_riding_5|knows_shield_3|knows_ironflesh_3|knows_power_strike_3, swadian_face_middle_1, swadian_face_old_2],

   ["sod_vil_high_chief1", "Villianese Zealous High Chief*", "Villianese Zealous High Chiefs*", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_player_supporters_faction,
    [itm_war_bow, itm_bodkin_arrows, itm_bodkin_arrows, itm_raider_battle_axe, itm_onehandedwarhammer, itm_noble_greatsword, itm_villshield, 
     itm_vilarmor_11, itm_vilarmor_12, itm_villboots2, itm_villhelm4, itm_villgloves2],
    def_attrib|level(30), expert_archer(30), knows_ironflesh_5|knows_athletics_8|knows_power_draw_7|knows_power_strike_3|knows_shield_6, villianese_black_middle_1, villianese_blue_old_2],

   ["sod_zer_3_noble1", "Zerrikanian Zealous Dvor*", "Zerrikanian Zealous Dvors*", tf_guarantee_ranged|tf_guarantee_horse|tf_mounted|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_player_supporters_faction,
    [itm_strong_bow, itm_khergit_arrows, itm_cimitar, itm_great_lancec, itm_gold_jarid, 
     itm_decor_colors1_shield, itm_decor_colors2_shield, itm_decor_colors3_shield, 
     itm_dvor1_mask, itm_dvor2_mask, itm_dvor_lamellar1, itm_dvor_lamellar2, itm_black_greaves, itm_darkgauntlets,
     itm_rok_dvor1_charger, itm_rok_dvor2_charger, itm_rok_dvor3_charger],
    def_attrib|level(30), expert_all(30), knows_riding_8|knows_ironflesh_5|knows_horse_archery_6|knows_shield_3|knows_power_throw_5|knows_power_draw_6|knows_power_strike_3, swadian_face_middle_1, swadian_face_older_2],
	
###########################################################################################################
# ############################################# FAITH:  THE ONE ###########################################
###########################################################################################################

#Adenian
  ["sod_faith1_mount", "Paladin of The One", "Paladins of The One", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_talak_lance, itm_bastard_sword_b, itm_morningstar, itm_sword_medieval_c, itm_tab_shield_heater_cav_b, itm_tab_shield_kite_cav_b, 
    itm_faith_the_one_helm_1, itm_faith_the_one_armor_1, itm_faith_the_one_armor_2, itm_dullplate, itm_dullboots, itm_dullgauntlets, 
    itm_scorpioncharger, itm_whitebirdongreencharger, itm_whitedeercharger, itm_redandyellowbgnorthbow, itm_darktealthreecircle, itm_blueflamemoon, itm_blackdotwhitered, itm_tribowred, itm_goldbaseblackorament, itm_ravisaris, itm_whisparia, itm_goldturqoisehorsebanner, itm_lazarith, itm_nishra],
   def_attrib|level(30), expert_melee(30), knows_riding_10|knows_ironflesh_5|knows_power_strike_10|knows_shield_10, swadian_face_middle_1, swadian_face_old_2],

#Antarian
   ["sod_faith1_foot", "Guardian of The One", "Guardians of The One", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 5, fac_player_supporters_faction,
    [itm_realcrusadersword, itm_swadianespadon, itm_bastard_sword_b, itm_realbastarda, itm_tab_shield_round_e, itm_tab_shield_round_d, 
     itm_faith_the_one_helm_1, itm_faith_the_one_armor_1, itm_faith_the_one_armor_2, itm_dullplate, itm_dullboots, itm_dullgauntlets],
    def_attrib|level(30), expert_melee(30), knows_ironflesh_10|knows_power_strike_10|knows_shield_10|knows_athletics_5, nord_face_middle_1, nord_face_older_2],

#Marinian
   ["sod_faith1_range_1", "Keeper of The One", "Keepers of The One", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
    [itm_sniper_crossbow, itm_steel_bolts, itm_sword_medieval_c, itm_military_pick, itm_tab_shield_pavise_c, itm_tab_shield_pavise_d, 
     itm_faith_the_one_helm_1, itm_faith_the_one_armor_1, itm_faith_the_one_armor_2, itm_dullplate, itm_dullboots, itm_dullgauntlets],
    def_attrib|level(30), expert_crossbow(30), knows_ironflesh_10|knows_power_strike_5|knows_shield_10|knows_athletics_5, rhodok_face_middle_1, rhodok_face_older_2],

#Villianese
   ["sod_faith1_range_2", "Sentinel of The One", "Sentinels of The One", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 5, fac_player_supporters_faction,
    [itm_war_bow, itm_khergit_arrows, itm_khergit_arrows, itm_great_axe, itm_noble_greatsword, 
     itm_faith_the_one_helm_1, itm_faith_enlightenment_armor_1, itm_faith_enlightenment_armor_2, itm_dullboots, itm_dullgauntlets],
    def_attrib|level(30), expert_archer(30), knows_ironflesh_10|knows_power_draw_10|knows_power_strike_5|knows_athletics_10, vaegir_face_middle_1, vaegir_face_older_2],

#Zerrikanian
  ["sod_faith1_mount_range", "Messenger of The One", "Messengers of The One", tf_guarantee_ranged|tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_khergit_bow, itm_khergit_arrows, itm_khergit_arrows, itm_gold_jarid, itm_goldscimitar, itm_lance, itm_tab_shield_heater_cav_b, itm_tab_shield_kite_cav_b, 
    itm_faith_the_one_helm_1, itm_faith_the_one_helm_1, itm_white_mask, itm_faith_the_one_armor_1, itm_faith_the_one_armor_2, itm_dullplate, itm_dullboots, itm_dullgauntlets, 
    itm_rok_bashkir_courser, itm_rok_bashkir_hunter, itm_warhorse_black, itm_charger_black, itm_anthorse1],
   def_attrib|level(30), expert_archer(30), knows_riding_10|knows_horse_archery_10|knows_power_draw_10|knows_power_throw_10|knows_shield_5, khergit_face_middle_1, khergit_face_older_2],


############################################################################################################
# ############################################# FAITH:  OLD GODS ###########################################
############################################################################################################

#Adenian
  ["sod_faith2_mount", "Champion of Ancestors", "Champions of Ancestors", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_nord_battle_axe, itm_jomsviking_axe, itm_onehandedwarhammer, itm_jomsviking_shield, itm_talak_lance,
    itm_faith_old_gods_helm_1, itm_faith_old_gods_helm_2, itm_faith_old_gods_helm_3, itm_faith_old_gods_helm_4, itm_faith_old_gods_helm_5, itm_faith_old_gods_helm_6, itm_faith_old_gods_armor_1, itm_faith_old_gods_armor_2, itm_faith_old_gods_armor_3, itm_faith_old_gods_armor_4, itm_gauntlets, itm_iron_greaves, 
    itm_warhorse_sc2_rtw3, itm_warhorse_sc2_rtw2, itm_warhorse_po1_rtw3, itm_warhorse_po2_rtw3, itm_warhorse_maw_b08, itm_warhorse_maw_b05, itm_warhorse_hre_rtw3, itm_warhorse_den_rtw2, itm_warhorse_b],
   def_attrib|level(30), expert_melee(30), knows_riding_10|knows_ironflesh_5|knows_power_strike_10|knows_shield_10, swadian_face_middle_1, swadian_face_old_2],

#Antarian
  ["sod_faith2_foot", "Chosen One", "Chosen by Gods", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_jomsviking_axe, itm_nord_battle_axe, itm_onehandedwarhammer, itm_jomsviking_shield,
    itm_faith_old_gods_helm_1, itm_faith_old_gods_helm_2, itm_faith_old_gods_helm_3, itm_faith_old_gods_helm_4, itm_faith_old_gods_helm_5, itm_faith_old_gods_helm_6, itm_faith_old_gods_armor_1, itm_faith_old_gods_armor_2, itm_faith_old_gods_armor_3, itm_faith_old_gods_armor_4, itm_gauntlets, itm_iron_greaves],
   def_attrib|level(30), expert_melee(30), knows_ironflesh_10|knows_power_strike_10|knows_shield_10|knows_athletics_5, nord_face_middle_1, nord_face_older_2],

#Marinian
  ["sod_faith2_ranged_1", "Focused One", "Focused Ones", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 5, fac_player_supporters_faction,
   [itm_sniper_crossbow, itm_steel_bolts, itm_steel_bolts, itm_bastard_sword_b, itm_talak_bastard_sword, 
    itm_faith_old_gods_helm_1, itm_faith_old_gods_helm_2, itm_faith_old_gods_helm_3, itm_faith_old_gods_helm_4, itm_faith_old_gods_helm_5, itm_faith_old_gods_helm_6, itm_faith_old_gods_armor_1, itm_faith_old_gods_armor_2, itm_faith_old_gods_armor_3, itm_faith_old_gods_armor_4, itm_gauntlets, itm_iron_greaves],
   def_attrib|level(30), expert_crossbow(30), knows_ironflesh_10|knows_power_strike_10|knows_shield_5|knows_athletics_10, rhodok_face_middle_1, rhodok_face_older_2],

#Villianese
  ["sod_faith2_ranged_2", "Guided One", "Guided Ones", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_war_bow, itm_khergit_arrows, itm_sword_khergit_4, itm_sword_khergit_3, itm_jomsviking_shield, 
    itm_faith_old_gods_helm_1, itm_faith_old_gods_helm_2, itm_faith_old_gods_helm_3, itm_faith_old_gods_helm_4, itm_faith_old_gods_helm_5, itm_faith_old_gods_helm_6, itm_faith_enlightenment_armor_1, itm_faith_enlightenment_armor_2, itm_black_army_leather_gloves, itm_iron_greaves],
   def_attrib|level(30), expert_archer(30), knows_ironflesh_10|knows_power_draw_10|knows_shield_5|knows_power_strike_5|knows_athletics_5, vaegir_face_middle_1, vaegir_face_older_2],

#Zerrikanian
  ["sod_faith2_mount_ranged", "Herald of the Gods", "Heralds of the Gods", tf_guarantee_ranged|tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_khergit_bow, itm_bodkin_arrows, itm_bodkin_arrows, itm_throwing_axes, itm_gold_jarid, itm_jomsviking_axe, itm_war_spear, itm_double_sided_lance, itm_jomsviking_shield,
    itm_faith_old_gods_helm_1, itm_bashkir_helm1, itm_faith_old_gods_helm_2, itm_faith_old_gods_helm_3, itm_faith_old_gods_helm_4, itm_faith_old_gods_helm_5, itm_faith_old_gods_helm_6, itm_faith_enlightenment_armor_1, itm_faith_enlightenment_armor_2, itm_black_army_leather_gloves, itm_iron_greaves,
    itm_rok_bashkir_courser, itm_rok_bashkir_hunter, itm_warhorse_black, itm_charger_black, itm_anthorse1],
   def_attrib|level(30), expert_archer(30), knows_riding_10|knows_horse_archery_10|knows_power_draw_10|knows_power_throw_10|knows_shield_5, khergit_face_middle_1, khergit_face_older_2],


############################################################################################################
# ############################################# FAITH:  THE VOID ###########################################
############################################################################################################

#Adenian
  ["sod_faith3_mount", "Harbinger of The Void", "Harbingers of The Void", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_talak_lance, itm_talak_bastard_sword, itm_talak_mace, itm_tab_shield_heater_cav_b, itm_tab_shield_kite_cav_b, 
    itm_faith_void_helm_1, itm_faith_void_armor_1, itm_darkboots, itm_darkgauntlets, 
    itm_warhorse, itm_charger, itm_warhorse_black, itm_charger_black, itm_anthorse1],
   def_attrib|level(30), expert_melee(30), knows_riding_10|knows_ironflesh_5|knows_power_strike_10|knows_shield_10, swadian_face_middle_1, swadian_face_old_2],

#Antarian
  ["sod_faith3_foot", "Devourer", "Devourers", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_darkespadon, itm_talak_morningstar, itm_small_pole_hammer, itm_realhalberda, 
    itm_tab_shield_heater_d, itm_faith_void_helm_1, itm_faith_void_armor_1, itm_darkboots, itm_darkgauntlets],
    def_attrib|level(30), expert_melee(30), knows_ironflesh_10|knows_power_strike_10|knows_shield_5|knows_athletics_10, nord_face_middle_1, nord_face_older_2],

#Marinian
  ["sod_faith3_ranged_1", "Dark Convict", "Dark Convicts", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 5, fac_player_supporters_faction,
   [itm_sniper_crossbow, itm_steel_bolts, itm_steel_bolts, itm_realpikec, itm_realhalberdf, itm_realhalberde, 
    itm_faith_void_helm_1, itm_black_army_armor_5, itm_black_army_armor_6, itm_darkboots, itm_darkgauntlets],
   def_attrib|level(30), expert_crossbow(35), knows_ironflesh_10|knows_power_strike_10|knows_shield_5|knows_athletics_10, rhodok_face_middle_1, rhodok_face_older_2],

#Villianese
  ["sod_faith3_ranged_2", "Dark Rogue", "Dark Rogues", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 5, fac_player_supporters_faction,
   [itm_war_bow, itm_khergit_arrows, itm_khergit_arrows, itm_cimitar, 
    itm_faith_void_helm_1, itm_faith_void_armor_2, itm_faith_void_armor_3, itm_darkboots, itm_black_army_leather_gloves],
   def_attrib|level(30), expert_archer(35), knows_ironflesh_10|knows_power_draw_10|knows_shield_5|knows_power_strike_5|knows_athletics_5, vaegir_face_middle_1, vaegir_face_older_2],

#Zerrikanian
  ["sod_faith3_mount_ranged", "Night Stalker", "Night Stalkers", tf_guarantee_ranged|tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_gold_jarid, itm_throwing_decor_hammer, itm_jarid, itm_throwing_axes, itm_talak_mace, itm_tab_shield_round_d, itm_tab_shield_round_e, 
    itm_dvor1_mask, itm_dvor2_mask, itm_faith_void_helm_1, itm_faith_void_armor_2, itm_faith_void_armor_3, itm_darkboots, itm_black_army_leather_gloves, 
    itm_rok_bashkir_courser, itm_rok_bashkir_hunter, itm_warhorse_black, itm_charger_black, itm_anthorse1],
   def_attrib|level(30), expert_javelinmen(30), knows_riding_10|knows_horse_archery_10|knows_power_draw_10|knows_power_throw_10|knows_shield_5, khergit_face_middle_1, khergit_face_older_2],


#################################################################################################################
# ############################################# FAITH:  ENLIGHTENMENT ###########################################
#################################################################################################################

#Adenian
  ["sod_faith4_mount", "Boundless Knight", "Boundless Knights", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_realbastarde, itm_steel_shield, itm_talak_lance,
    itm_faith_the_one_helm_1, itm_winged_great_helmet, itm_faith_enlightenment_armor_1, itm_faith_enlightenment_armor_2, itm_dullboots, itm_dullgauntlets,
    itm_warhorse_sc2_rtw3, itm_warhorse_sc2_rtw2, itm_warhorse_po1_rtw3, itm_warhorse_po2_rtw3, itm_warhorse_maw_b08, itm_warhorse_maw_b05, itm_warhorse_hre_rtw3, itm_warhorse_den_rtw2, itm_warhorse_b],
   def_attrib|level(30), expert_melee(35), knows_riding_10|knows_ironflesh_5|knows_power_strike_10|knows_shield_10, swadian_face_middle_1, swadian_face_old_2],

#Antarian
  ["sod_faith4_foot", "Boundless Champion", "Boundless Champions", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_realbastarde, itm_swadianespadon, itm_seax, itm_steel_shield, 
    itm_faith_the_one_helm_1, itm_winged_great_helmet, itm_faith_enlightenment_armor_1, itm_faith_enlightenment_armor_2, itm_dullboots, itm_dullgauntlets],
   def_attrib|level(30), expert_melee(35), knows_ironflesh_10|knows_power_strike_10|knows_shield_10|knows_athletics_5, nord_face_middle_1, nord_face_older_2],

#Marinian
  ["sod_faith4_ranged_1", "Boundless Marksman", "Boundless Marksmen", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_sniper_crossbow, itm_steel_bolts, itm_steel_bolts, itm_sword_medieval_c, itm_tab_shield_round_d, itm_tab_shield_round_e, 
    itm_faith_the_one_helm_1, itm_winged_great_helmet, itm_faith_enlightenment_armor_1, itm_faith_enlightenment_armor_2, itm_dullboots, itm_dullgauntlets],
   def_attrib|level(30), expert_crossbow(35), knows_ironflesh_10|knows_power_strike_5|knows_shield_5|knows_athletics_10|knows_weapon_master_1, rhodok_face_middle_1, rhodok_face_older_2],

#Villianese
  ["sod_faith4_ranged_2", "Boundless Ranger", "Boundless Rangers", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_war_bow, itm_khergit_arrows, itm_foil, itm_steel_shield, 
    itm_faith_the_one_helm_1, itm_winged_great_helmet, itm_faith_enlightenment_armor_1, itm_faith_enlightenment_armor_2, itm_dullboots, itm_dullgauntlets],
   def_attrib|level(30), expert_archer(35), knows_ironflesh_10|knows_power_draw_10|knows_shield_5|knows_power_strike_5|knows_athletics_5, vaegir_face_middle_1, vaegir_face_older_2],

#Zerrikanian
  ["sod_faith4_mount_ranged", "Boundless Wanderer", "Boundless Wanderers", tf_guarantee_ranged|tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_khergit_bow, itm_khergit_arrows, itm_khergit_arrows, itm_goldscimitar, 
    itm_oprichnik_mask1, itm_zerk_redmask, itm_dvor2_mask, itm_faith_enlightenment_armor_1, itm_faith_enlightenment_armor_2, itm_dullboots, itm_black_army_leather_gloves,
    itm_rok_bashkir_courser, itm_rok_bashkir_hunter, itm_rok_boyar_son_warhorse, itm_rok_oprichnik_charger],
   def_attrib|level(30), expert_archer(35), knows_riding_10|knows_horse_archery_10|knows_power_draw_10|knows_power_throw_10|knows_shield_5, khergit_face_middle_1, khergit_face_older_2],


############################################################################################################################
# ############################################# FAITH:  NATURAL PHILOSOPHY #################################################
############################################################################################################################

#Adenian
  ["sod_faith5_mount", "Assault Cavalry", "Assault Cavalry", tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_talak_lance, itm_lance, itm_steel_shield, itm_tab_shield_heater_cav_b, itm_tab_shield_kite_cav_b, itm_tab_shield_round_d, itm_tab_shield_round_e, 
    itm_black_helmet, itm_bascinet, itm_black_armor, itm_faith_void_armor_1, itm_darkgauntlets, itm_darkboots, 
    itm_rok_black_general_horse],
   def_attrib|level(30), expert_melee(30), knows_riding_10|knows_ironflesh_5|knows_power_strike_10|knows_shield_10, swadian_face_middle_1, swadian_face_old_2],

#Antarian
   ["sod_faith5_foot", "Combat Engineer", "Combat Engineers", tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 5, fac_player_supporters_faction,
   [itm_polehammer, itm_greathammer, itm_tab_shield_pavise_d, 
    itm_guard_helmet, itm_helmet_with_neckguard, itm_bascinet, itm_faith_void_armor_1, itm_gauntlets, itm_darkgauntlets, itm_iron_greaves, itm_darkboots],
   def_attrib|level(30), expert_melee(30), knows_ironflesh_10|knows_power_strike_10|knows_shield_10|knows_athletics_5, nord_face_middle_1, nord_face_older_2],

#Marinian
  ["sod_faith5_ranged_1", "Weapon Specialist", "Weapon Specialists", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_musket_2, itm_cartridges, itm_cartridges, itm_military_pick, itm_military_hammer, itm_hand_axe, itm_tab_shield_kite_d, itm_tab_shield_pavise_c, 
    itm_guard_helmet, itm_helmet_with_neckguard, itm_bascinet, itm_faith_void_armor_2, itm_faith_void_armor_3, itm_mail_chausses, itm_iron_greaves, itm_black_army_leather_gloves],
   def_attrib|level(30), regular_melee(30)|wp_firearm(300), knows_ironflesh_10|knows_power_strike_10|knows_shield_5|knows_athletics_10, rhodok_face_middle_1, rhodok_face_older_2],

#Villianese
  ["sod_faith5_ranged_2", "Combat Specialist", "Combat Specialists", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_musket_1, itm_cartridges, itm_cartridges, itm_military_pick, itm_military_hammer, itm_hand_axe, itm_tab_shield_kite_d, itm_tab_shield_pavise_c, 
    itm_guard_helmet, itm_helmet_with_neckguard, itm_bascinet, itm_black_hood, itm_faith_void_armor_2, itm_faith_void_armor_3, itm_mail_chausses, itm_iron_greaves, itm_black_army_leather_gloves],
   def_attrib|level(30), regular_melee(30)|wp_firearm(300), knows_ironflesh_10|knows_power_draw_10|knows_shield_5|knows_power_strike_5|knows_athletics_5, vaegir_face_middle_1, vaegir_face_older_2],

#Zerrikanian
  ["sod_faith5_mount_ranged", "Dragoon", "Dragoons", tf_guarantee_ranged|tf_mounted|tf_guarantee_horse|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 5, fac_player_supporters_faction,
   [itm_flintlock_pistol, itm_cartridges, itm_cartridges, itm_sword_khergit_4, itm_tab_shield_round_d, itm_tab_shield_round_e, 
    itm_dvor2_mask, itm_dvor1_mask, itm_faith_void_armor_2, itm_faith_void_armor_3, itm_black_army_leather_gloves, itm_mail_chausses, itm_iron_greaves, 
    itm_rok_bashkir_courser, itm_rok_bashkir_hunter, itm_rok_boyar_son_warhorse, itm_rok_boyar_warhorse],
   def_attrib|level(30), regular_melee(30)|wp_firearm(300), knows_riding_10|knows_horse_archery_10|knows_power_draw_10|knows_power_strike_10|knows_shield_5, khergit_face_middle_1, khergit_face_older_2],

###########################################################################################################
# OTHER UNITS
###########################################################################################################

  ["looter", "Looter", "Looters", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_outlaws,
   [itm_hatchet, itm_club, itm_butchering_knife, itm_falchion, itm_rawhide_coat, itm_stones,
    itm_nomad_armor, itm_nomad_armor, itm_woolen_cap, itm_woolen_cap, itm_nomad_boots, itm_wrapping_boots],
   def_attrib|level(6), regular_melee(6), 0, bandit_face1, bandit_face2],

  ["bandit", "Bandit", "Bandits", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_outlaws,
   [itm_fighting_axe, itm_one_handed_war_axe_a, itm_spear, itm_tab_shield_round_a, itm_tab_shield_round_b, itm_javelin, itm_throwing_axes,
    itm_leather_cap, itm_skullcap, itm_nomad_vest, itm_shirt, itm_leather_boots, itm_nomad_boots],
   def_attrib|level(9), regular_melee(9), knows_power_draw_1, bandit_face1, bandit_face2],

  ["cutthroat", "Cutthroat", "Cutthroats", tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_boots, 0, 0, fac_outlaws,
   [itm_one_handed_war_axe_a, itm_one_handed_war_axe_b, itm_one_handed_battle_axe_a, itm_tab_shield_round_b, itm_javelin, itm_throwing_axes, 
    itm_skullcap, itm_nasal_helmet, itm_byrnie, itm_studded_leather_coat, itm_leather_jerkin, itm_leather_boots],
   def_attrib|level(14), regular_melee(12), knows_power_draw_2|knows_power_strike_1, rhodok_face_young_1, rhodok_face_old_2],

  ["brigand", "Brigand", "Brigands", tf_guarantee_armor|tf_guarantee_ranged|tf_guarantee_boots, 0, 0, fac_outlaws,
   [itm_arrows, itm_axe, itm_short_bow, itm_leather_jerkin, itm_shirt, itm_leather_boots, 
   itm_nasal_helmet, itm_leather_cap, itm_arrows, itm_axe, itm_hatchet, itm_axe, itm_short_bow, itm_hunting_bow, itm_nomad_bow,
    itm_common_hood, itm_black_hood, itm_shirt, itm_padded_leather, itm_leather_jerkin, itm_ragged_outfit, itm_hide_boots, itm_leather_boots],
   def_attrib|level(14), regular_archer(12), knows_power_draw_3, swadian_face_young_1, swadian_face_old_2],

  ["reaver", "Reaver", "Reavers", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, 0, 0, fac_outlaws,
   [itm_arrows, itm_axe, itm_voulge, itm_sword_khergit_2, itm_strong_bow, itm_nomad_bow, itm_nomad_bow,
    itm_leather_vest, itm_studded_leather_coat, itm_nomad_boots, itm_spiked_helmet, itm_nordic_helmet, itm_nasal_helmet, itm_helmet_fur_a],
   def_attrib|level(19), expert_archer(19), knows_power_draw_3, bandit_face1, bandit_face2],

  ["thug", "Thug", "Thugs", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_outlaws,
   [itm_glaive, itm_sword_medieval_b, itm_sword_viking_2, itm_fighting_axe, itm_battle_axe, itm_spear, itm_nordic_shield, itm_nordic_shield, itm_nordic_shield, itm_wooden_shield, itm_long_bow, itm_javelin, itm_throwing_axes,
    itm_nordic_helmet, itm_byrnie, itm_nasal_helmet, itm_banded_armor, itm_byrnie, itm_surcoat_over_mail, itm_leather_boots, itm_nomad_boots],
   def_attrib|level(19), expert_melee(19), knows_ironflesh_2|knows_power_strike_2|knows_power_draw_3|knows_power_throw_2|knows_riding_1|knows_athletics_2, nord_face_young_1, nord_face_old_2],

  ["mountain_bandit", "Mountain Bandit", "Mountain Bandits", tf_guarantee_armor|tf_guarantee_boots, 0, 0, fac_outlaws,
   [itm_sword_viking_1, itm_spear, itm_winged_mace, itm_falchion, itm_short_bow, itm_arrows, itm_javelin, itm_fur_covered_shield, itm_hide_covered_round_shield, itm_wooden_shield, itm_nordic_shield, 
    itm_felt_hat, itm_head_wrappings, itm_skullcap, itm_khergit_armor, itm_nomad_armor, itm_rawhide_coat, itm_nomad_vest, itm_hide_boots, itm_nomad_boots, 
    itm_saddle_horse],
   def_attrib|level(12), regular_melee(12), knows_power_draw_2|knows_power_strike_1, rhodok_face_young_1, rhodok_face_old_2],

  ["forest_bandit", "Forest Bandit", "Forest Bandits", tf_guarantee_armor|tf_guarantee_ranged|tf_guarantee_boots, 0, 0, fac_outlaws,
   [itm_arrows, itm_axe, itm_hatchet, itm_quarter_staff, itm_short_bow, itm_hunting_bow,
    itm_common_hood, itm_black_hood, itm_shirt, itm_padded_leather, itm_leather_jerkin, itm_ragged_outfit, itm_hide_boots, itm_leather_boots],
   def_attrib|level(12), regular_archer(12), knows_power_draw_3, swadian_face_young_1, swadian_face_old_2],

  ["sea_raider", "Sea Raider", "Sea Raiders", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, 0, 0, fac_outlaws,
   [itm_arrows, itm_sword_viking_1, itm_sword_viking_2, itm_fighting_axe, itm_battle_axe, itm_spear, itm_nordic_shield, itm_nordic_shield, itm_nordic_shield, itm_wooden_shield, itm_long_bow, itm_javelin, itm_throwing_axes,
    itm_nordic_helmet, itm_nordic_helmet, itm_nasal_helmet, itm_leather_jerkin, itm_byrnie, itm_leather_jerkin, itm_leather_boots, itm_nomad_boots],
   def_attrib|level(16), regular_melee(16), knows_ironflesh_2|knows_power_strike_2|knows_power_draw_3|knows_power_throw_2|knows_riding_1|knows_athletics_2, nord_face_young_1, nord_face_old_2],

  ["steppe_bandit", "Steppe Bandit", "Steppe Bandits", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse|tf_guarantee_ranged|tf_mounted, 0, 0, fac_outlaws,
   [itm_arrows, itm_sword_khergit_1, itm_winged_mace, itm_spear, itm_light_lance, itm_nomad_bow, itm_nomad_bow, itm_short_bow, itm_jarid, itm_leather_covered_round_shield, itm_leather_covered_round_shield,
    itm_nomad_cap_a, itm_leather_steppe_cap_a, itm_leather_steppe_cap_b, itm_khergit_armor, itm_nomad_armor, itm_steppe_armor, itm_leather_vest, itm_hide_boots, itm_nomad_boots,
    itm_saddle_horse, itm_steppe_horse, itm_steppe_horse],
   def_attrib|level(13), regular_archer(13), knows_riding_4|knows_horse_archery_3|knows_power_draw_3|knows_power_strike_1, khergit_face_young_1, khergit_face_old_2],

  ["manhunter", "Manhunter", "Manhunters", tf_guarantee_armor, 0, 0, fac_manhunters,
   [itm_spiked_mace, itm_wooden_stick, itm_cudgel, itm_hammer, itm_club, itm_staff, itm_throwing_hammers1, itm_throwing_hammers2, itm_fur_covered_shield, itm_hide_covered_round_shield,
    itm_woolen_cap, itm_rawhide_coat, itm_coarse_tunic, itm_nomad_armor, itm_nomad_boots, itm_wrapping_boots,
    itm_sumpter_horse],
   def_attrib|level(15), regular_melee(15), 0, bandit_face1, bandit_face2],

  ["caravan_master", "Caravan Master", "Caravan Masters", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse, 0, 0, fac_commoners,
   [itm_sword_medieval_c, itm_fur_coat, itm_hide_boots, itm_saddle_horse,
    itm_saddle_horse, itm_saddle_horse, itm_saddle_horse,
    itm_leather_jacket, itm_leather_cap],
   def_attrib|level(9), regular_melee(9), knows_riding_4|knows_ironflesh_3, mercenary_face_1, mercenary_face_2],

  ["kidnapped_girl", "Kidnapped Girl", "Kidnapped Girls", tf_hero|tf_female|tf_randomize_face|tf_unmoveable_in_party_window, 0, reserved, fac_commoners,
   [itm_dress, itm_leather_boots],
   def_attrib|level(2), regular_melee(2), knows_riding_2, woman_face_1, woman_face_2],

#MERC PEASANT (UNUSED)
  ["sod_peasant_merc", "Peasant", "Peasants", tf_guarantee_ranged|tf_guarantee_gloves|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, 0, 0, fac_player_supporters_faction,
   [itm_sword_medieval_b_small, itm_tab_shield_round_b, itm_javelin,
    itm_leather_cap, itm_padded_leather, itm_leather_boots, itm_leather_gloves],
   def_attrib|level(4), weak_melee(4), 0, rhodok_face_young_1, rhodok_face_young_2],


###########################################################################################################
# PEASANT WOMEN
###########################################################################################################

  ["refugee", "Refugee", "Refugees", tf_female|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_headcloth, itm_woolen_hood, itm_robe, itm_woolen_dress, itm_wrapping_boots, 
    itm_knife, itm_pitch_fork, itm_sickle, itm_hatchet, itm_club, itm_throwing_knives],
   def_attrib|level(1), regular_melee(1), 0, refugee_face1, refugee_face2],

  ["peasant_woman", "Peasant Woman", "Peasant Women", tf_female|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_headcloth, itm_woolen_hood, itm_dress, itm_woolen_dress, itm_wrapping_boots, 
    itm_knife, itm_pitch_fork, itm_sickle, itm_hatchet, itm_club, itm_throwing_knives],
   def_attrib|level(1), regular_melee(1), 0, refugee_face1, refugee_face2],

   ["follower_woman", "Camp Follower", "Camp Follower", tf_female|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_skullcap, itm_dress, itm_woolen_dress, itm_wrapping_boots, itm_nordic_shield, itm_hide_covered_round_shield, 
    itm_hatchet, itm_hand_axe, itm_voulge, itm_fighting_pick, itm_club, itm_light_crossbow, itm_short_bow, itm_crossbow, itm_bolts, itm_arrows],
   def_attrib|level(5), regular_melee(5), 0, refugee_face1, refugee_face2],

  ["hunter_woman", "Huntress", "Huntresses", tf_female|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_skullcap, itm_dress, itm_woolen_dress, itm_wrapping_boots, itm_nordic_shield, itm_hide_covered_round_shield, 
    itm_hatchet, itm_hand_axe, itm_voulge, itm_fighting_pick, itm_club, itm_light_crossbow, itm_short_bow, itm_crossbow, itm_bolts, itm_arrows],
   def_attrib|level(10), regular_melee(10), 0, refugee_face1, refugee_face2],

  ["fighter_woman", "Camp Defender", "Camp Defenders", tf_female|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_skullcap, itm_leather_jerkin, itm_leather_vest, itm_wrapping_boots, itm_fur_covered_shield, itm_hide_covered_round_shield, 
    itm_hatchet, itm_voulge, itm_light_crossbow, itm_short_bow, itm_crossbow, itm_bolts, itm_arrows],
   def_attrib|level(16), regular_melee(16), knows_riding_3|knows_athletics_2|knows_ironflesh_1, refugee_face1, refugee_face2],

  ["sword_sister", "Sword Sister", "Sword Sisters", tf_female|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_shield|tf_guarantee_horse, 0, 0, fac_commoners,
   [itm_guard_helmet, itm_helmet_with_neckguard, itm_plate_armor, itm_coat_of_plates, itm_mail_chausses, itm_iron_greaves, itm_leather_gloves, 
    itm_sword_medieval_b, itm_sword_khergit_3, itm_light_crossbow, itm_bolts, itm_plate_covered_round_shield, itm_tab_shield_small_round_c, 
    itm_courser],
   def_attrib|level(22), regular_melee(22), knows_riding_5|knows_athletics_3|knows_ironflesh_2|knows_shield_2, refugee_face1, refugee_face2],


#This troop is the troop marked as soldiers_end
 ["town_walker_1", "Townsman", "Townsmen", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_short_tunic, itm_linen_tunic, itm_fur_coat, itm_coarse_tunic, itm_tabard, itm_leather_vest, itm_arena_tunic_white, itm_leather_apron, itm_shirt, itm_arena_tunic_green, itm_arena_tunic_blue, itm_woolen_hose, itm_nomad_boots, itm_blue_hose, itm_hide_boots, itm_ankle_boots, itm_leather_boots, itm_fur_hat, itm_leather_cap, itm_straw_hat, itm_felt_hat],
   def_attrib|level(4), regular_melee(4), 0, man_face_young_1, man_face_old_2],

 ["town_walker_2", "Townswoman", "Townswomen", tf_female|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_blue_dress, itm_dress, itm_woolen_dress, itm_peasant_dress, itm_woolen_hose, itm_blue_hose, itm_wimple_a, itm_female_hood],
   def_attrib|level(2), regular_melee(2), 0, woman_face_1, woman_face_2],

 ["village_walker_1", "Villager", "Villagers", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_short_tunic, itm_linen_tunic, itm_coarse_tunic, itm_leather_vest, itm_leather_apron, itm_shirt, itm_woolen_hose, itm_nomad_boots, itm_blue_hose, itm_hide_boots, itm_ankle_boots, itm_leather_boots, itm_fur_hat, itm_leather_cap, itm_straw_hat, itm_felt_hat],
   def_attrib|level(4), regular_melee(4), 0, man_face_younger_1, man_face_older_2],

 ["village_walker_2", "Villager", "Villagers", tf_female|tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_blue_dress, itm_dress, itm_woolen_dress, itm_peasant_dress, itm_woolen_hose, itm_blue_hose, itm_wimple_a, itm_female_hood],
   def_attrib|level(2), regular_melee(2), 0, woman_face_1, woman_face_2],

 ["spy_walker_1", "Townsman", "Townsmen", tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_commoners,
   [itm_short_tunic, itm_linen_tunic, itm_coarse_tunic, itm_tabard, itm_leather_vest, itm_robe, itm_leather_apron, itm_shirt, itm_woolen_hose, itm_nomad_boots, itm_blue_hose, itm_hide_boots, itm_ankle_boots, itm_leather_boots, itm_fur_hat, itm_leather_cap, itm_straw_hat, itm_felt_hat],
   def_attrib|level(4), regular_melee(4), 0, man_face_middle_1, man_face_old_2],

 ["spy_walker_2", "Townswoman", "Townswomen", tf_female|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet, 0, 0, fac_commoners,
   [itm_blue_dress, itm_dress, itm_woolen_dress, itm_peasant_dress, itm_woolen_hose, itm_blue_hose, itm_wimple_a, itm_female_hood],
   def_attrib|level(2), regular_melee(2), 0, woman_face_1, woman_face_2],

# Zendar
  ["tournament_master", "Tournament Master", "Tournament Master", tf_hero, scn_zendar_center|entry(1), reserved,  fac_commoners, [itm_nomad_armor, itm_nomad_boots], def_attrib|level(2), regular_melee(2), 0, 0x000000000008414401e28f534c8a2d09],
  ["trainer", "Trainer", "Trainer", tf_hero, scn_zendar_center|entry(2), reserved,  fac_commoners, [itm_leather_jerkin, itm_hide_boots], def_attrib|level(2), regular_melee(2), 0, 0x00000000000430c701ea98836781647f],
  ["Constable_Hareck", "Constable Hareck", "Constable Hareck", tf_hero, scn_zendar_center|entry(5), reserved,  fac_commoners, [itm_leather_jacket, itm_hide_boots], def_attrib|level(5), regular_melee(5), 0, 0x00000000000c41c001fb15234eb6dd3f],

# Ryan BEGIN
  ["Ramun_the_slave_trader", "Ramun, the slave trader", "Ramun, the slave trader", tf_hero, no_scene, reserved, fac_commoners, [itm_leather_jacket, itm_hide_boots], def_attrib|level(5), regular_melee(5), 0, 0x0000000fd5105592385281c55b8e44eb00000000001d9b220000000000000000],

  ["guide", "Quick Jimmy", "Quick Jimmy", tf_hero, no_scene, 0,  fac_commoners, [itm_coarse_tunic, itm_hide_boots], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, 0x00000000000c318301f24e38a36e38e3],
# Ryan END

  ["Xerina", "Xerina", "Xerina",    tf_hero|tf_female, scn_the_happy_boar|entry(5), reserved,  fac_commoners, [itm_leather_jerkin, itm_hide_boots], def_attrib|str_12|agi_20|level(39), expert_all(39),   knows_power_strike_5|knows_ironflesh_5|knows_riding_6|knows_power_draw_6|knows_athletics_8|knows_horse_archery_5|knows_shield_3,   0x00000001ac0820074920561d0b51e6ed00000000001d40ed0000000000000000],
  ["Dranton", "Dranton", "Dranton", tf_hero,           scn_the_happy_boar|entry(2), reserved,  fac_commoners, [itm_leather_vest, itm_hide_boots],   def_attrib|str_21|agi_12|level(42), expert_melee(42), knows_power_strike_6|knows_ironflesh_9|knows_riding_4|knows_power_draw_4|knows_athletics_4|knows_horse_archery_3|knows_shield_5, 0x0000000a460c3002470c50f3502879f800000000001ce0a00000000000000000],
  ["Kradus", "Kradus", "Kradus",    tf_hero,           scn_the_happy_boar|entry(3), reserved,  fac_commoners, [itm_padded_leather, itm_hide_boots], def_attrib|str_15|agi_15|level(43), expert_melee(43), knows_power_strike_7|knows_ironflesh_7|knows_riding_8|knows_power_draw_4|knows_athletics_5|knows_horse_archery_2|knows_shield_3, 0x0000000f5b1052c61ce1a9521db1375200000000001ed31b0000000000000000],

#Tutorial
  ["tutorial_trainer", "Training Ground Master", "Training Ground Master", tf_hero, scn_training_ground|entry(2), reserved, fac_commoners, [itm_robe, itm_nomad_boots], def_attrib|level(2), regular_melee(2), 0, 0x000000000008414401e28f534c8a2d09],

#Salt mine
  ["Galeas", "Galeas", "Galeas", tf_hero, 0, reserved, fac_commoners, [itm_leather_jacket, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, 0x000000000004718201c073191a9bb10c],

#Dhorak keep

  ["farmer_from_bandit_village", "Farmer", "Farmers", tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_linen_tunic, itm_coarse_tunic, itm_shirt, itm_nomad_boots, itm_wrapping_boots],
   def_attrib|level(4), regular_melee(4), knows_common, man_face_middle_1, man_face_older_2],

  ["trainer_1", "Trainer", "Trainer", tf_hero, scn_training_ground_ranged_melee_1|entry(6), reserved,  fac_commoners, [itm_leather_jerkin, itm_hide_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x0000000d0d1030c74ae8d661b651c6840000000000000e220000000000000000],
  ["trainer_2", "Trainer", "Trainer", tf_hero, scn_training_ground_ranged_melee_2|entry(6), reserved,  fac_commoners, [itm_nomad_vest, itm_hide_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x0000000e5a04360428ec253846640b5d0000000000000ee80000000000000000],
  ["trainer_3", "Trainer", "Trainer", tf_hero, scn_training_ground_ranged_melee_3|entry(6), reserved,  fac_commoners, [itm_padded_leather, itm_hide_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x0000000e4a0445822ca1a11ab1e9eaea0000000000000f510000000000000000],
  ["trainer_4", "Trainer", "Trainer", tf_hero, scn_training_ground_ranged_melee_4|entry(6), reserved,  fac_commoners, [itm_leather_jerkin, itm_hide_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x0000000e600452c32ef8e5bb92cf1c970000000000000fc20000000000000000],
  ["trainer_5", "Trainer", "Trainer", tf_hero, scn_training_ground_ranged_melee_5|entry(6), reserved,  fac_commoners, [itm_leather_vest, itm_hide_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x0000000e77082000150049a34c42ec960000000000000e080000000000000000],

# Ransom brokers
  ["ransom_broker_1", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_leather_vest, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_2", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_tabard, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_3", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_leather_vest, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_4", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_short_tunic, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_5", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_gambeson, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_6", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_blue_gambeson, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_7", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_red_gambeson, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_8", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_fur_coat, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_9", "Ransom_Broker", "Ransom_Broker",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_leather_vest, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["ransom_broker_10", "Ransom_Broker", "Ransom_Broker", tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_leather_jacket, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],

# Tavern traveler
  ["tavern_traveler_1", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_fur_coat, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_2", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_tabard, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_3", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_leather_vest, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_4", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_blue_gambeson, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_5", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_short_tunic, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_6", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_fur_coat, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_7", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_leather_jacket, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_8", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_tabard, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_9", "Traveller", "Traveller",  tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_fur_coat, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_traveler_10", "Traveller", "Traveller", tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_leather_jacket, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],

# Tavern traveler
  ["tavern_bookseller_1", "Book_Merchant", "Book_Merchant", tf_hero|tf_is_merchant|tf_randomize_face, 0, reserved, fac_commoners, [itm_fur_coat, itm_hide_boots,
               itm_book_pathfinding_reference, itm_book_administration, itm_book_tactics, itm_book_persuasion, itm_book_wound_treatment_reference, itm_book_leadership,
               itm_book_intelligence, itm_book_training_reference, itm_book_surgery_reference, itm_book_chirurgeons_ledger, itm_book_anatomy_of_mercy,
               itm_book_drill_camp_company], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],
  ["tavern_bookseller_2", "Book_Merchant", "Book_Merchant", tf_hero|tf_is_merchant|tf_randomize_face, 0, reserved, fac_commoners, [itm_fur_coat, itm_hide_boots,
               itm_book_pathfinding_reference, itm_book_administration, itm_book_wound_treatment_reference, itm_book_leadership, itm_book_intelligence, itm_book_trade,
               itm_book_engineering, itm_book_weapon_mastery, itm_book_roads_before_armies, itm_book_quartermasters_burden, itm_book_embassies_in_wartime],
   def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],

# Tavern minstrel.
  ["tavern_minstrel_1", "Minstrel", "Minstrel", tf_hero|tf_randomize_face, 0, reserved, fac_commoners, [itm_leather_jacket, itm_hide_boots], def_attrib|level(5), regular_melee(5), knows_common, merchant_face_1, merchant_face_2],


##################################################################################################################################
#COMPANIONS
##################################################################################################################################
   #Note that some reactions (such as those to not being paid, heavy casualties or going hungry), may be universal, but a random member of the group comes forward to complain.  
   #Since these affect general morale anyway, it is probably best to just avoid either one.
   
   #VILLIANESE MELEE INFANTRY (Tracker & Pathfinder):  Likes npc2, Dislikes npc7, npc16, and heavy losses in battle 
   #Had 10 skills at lvl 3 (+3 IQ for total +15 at lvl 15 = 25 skills).  Originally costs 300 denars.  Should be double that for level and equipment.
   ["npc1", "Borcha", "Borcha", tf_hero|tf_unmoveable_in_party_window, 0, reserved, fac_commoners, 
   [itm_sword_khergit_2, itm_tab_shield_pavise_c, itm_helmet_with_neckguard, itm_vilarmor_7, itm_black_army_boot_1, itm_black_army_leather_gloves],
   str_12|agi_12|int_15|cha_7|level(15), regular_melee(15), 
   knows_ironflesh_1|knows_power_strike_4|knows_weapon_master_1|knows_shield_1|knows_athletics_3|knows_tracking_5|knows_pathfinding_5|knows_spotting_5,
   0x00000008bd0232c756f451979c69236600000000001cc8dc0000000000000000],
   #ZERRIKANIAN MELEE CAVALRY (Slave Trader):  Likes npc1, Dislikes npc5, npc9, failing quests, and taking from villagers
   ##Had 9 skills at lvl 1 (+14 at lvl 15 = 23 skills)
   ["npc2", "Marnid", "Marnid", tf_hero|tf_unmoveable_in_party_window, 0, reserved, fac_commoners, 
   [itm_arena_lance, itm_mace_3, itm_throwing_military_hammers, itm_straw_shield, itm_rabati, itm_cossack_armor, itm_khergit_guard_boots, itm_leather_gloves, itm_rok_saddle_horse1],
   str_12|agi_12|int_11|cha_10|level(15), regular_melee(15)|wp_throwing(120), 
   knows_ironflesh_1|knows_power_strike_4|knows_power_throw_4|knows_weapon_master_1|knows_shield_4|knows_riding_4|knows_wound_treatment_1|knows_first_aid_1|knows_trade_3,
   0x000000019d00400a370b89b712c8d39f00000000001d48190000000000000000],
   #ANTARIAN SCOUT (Melee Cavalry / Healer):  Likes npc9 and leaving troops to cover retreat, Dislikes npc8, npc14, and taking from villagers
   ##Had 8 skills at lvl 1 (+5 IQ for total +19 at lvl 15 = 27 skills)
   ["npc3", "Ymira", "Ymira", tf_female|tf_hero|tf_unmoveable_in_party_window, 0, reserved, fac_commoners, 
   [itm_spear, itm_sword_medieval_b_small, itm_tab_shield_round_b, itm_skullcap, itm_padded_leather, itm_leather_gloves, itm_hide_boots, itm_saddle_horse],
   str_12|agi_12|int_16|cha_6|level(15), regular_melee(15), 
   knows_power_strike_4|knows_weapon_master_1|knows_shield_2|knows_athletics_1|knows_riding_4|knows_wound_treatment_5|knows_surgery_5|knows_first_aid_5,
   0x000000000004000158226538ce81c30200000000001d00000000000000000000],
   #VILLIANESE VETERAN LONGBOWMAN (Some Tactics & Some Healing):  Likes npc5 and failing quests, Dislikes npc7 and npc10
   ##Had 21 skills at lvl 10 (-3 IQ, +3 at lvl 16 = 25 skills)
   ["npc4", "Rolf", "Rolf", tf_hero|tf_unmoveable_in_party_window, 0, reserved, fac_commoners, 
   [itm_long_bow, itm_barbed_arrows, itm_sword_khergit_2, itm_vilhelm5, itm_vilarmor_2, itm_leather_gloves, itm_hide_boots],
   str_15|agi_13|int_10|cha_10|level(16), regular_archer(16), 
   knows_ironflesh_1|knows_power_strike_4|knows_power_draw_5|knows_weapon_master_4|knows_athletics_4|knows_riding_1|knows_horse_archery_1|knows_tactics_2|knows_surgery_1|knows_first_aid_1,
   0x000000003f0e431022b34a399389bcec00000000001c9b540000000000000000],
   #VILLIANESE SCOUT (Cavalry Archer / Some Trainer): Likes npc4 and failing quests, Dislikes npc2, npc11, and heavy casualties
   ##Had 20 skills at lvl 5 (+9 at lvl 14 = 29 skills)
   ["npc5", "Baheshtur", "Baheshtur", tf_hero|tf_unmoveable_in_party_window, 0, reserved, fac_commoners, 
   [itm_pilgrim_hood, itm_pilgrim_disguise, itm_black_army_leather_gloves, itm_black_army_boot_1, itm_nomad_bow, itm_barbed_arrows, itm_sword_khergit_2, itm_tab_shield_small_round_a, itm_courser],
   str_15|agi_12|int_12|cha_7|level(14), regular_archer(14), 
   knows_ironflesh_1|knows_power_strike_4|knows_power_draw_5|knows_weapon_master_4|knows_shield_1|knows_athletics_2|knows_riding_4|knows_horse_archery_4|knows_trainer_2|knows_leadership_2,
   0x00000008bf11a248672c972328324ba200000000001cd3210000000000000000],
   #ADENIAN VETERAN INFANTRY (Some Trainer):  Likes npc12, Dislikes npc11, npc13, taking from villagers, too much fighting, and failing quests 
   ##Had 15 skills at lvl 6 (+9 at lvl 15 = 24 skills)
   ["npc6", "Firentis", "Firentis", tf_hero|tf_unmoveable_in_party_window, 0, reserved, fac_commoners, 
   [itm_sword_medieval_b_small, itm_tab_shield_round_b, itm_footman_helmet, itm_padded_leather, itm_leather_boots, itm_leather_gloves],
   str_16|agi_15|int_10|cha_5|level(15), regular_melee(15), 
   knows_ironflesh_1|knows_power_strike_5|knows_weapon_master_3|knows_shield_5|knows_athletics_5|knows_riding_2|knows_trainer_3,
   0x00000006850052835c1895d074773ca300000000001c0ecb0000000000000000],
   #ZERRIKANIAN DVOR ARCHER (Tracker, Spotting, and Pathfinding):  Likes npc16, Dislikes npc1, npc4, being hungry, and heavy casualties
   ##Had 16 skills at lvl 2 (+5 IQ for total +22 at lvl 19 = 38 skills)
   ["npc7", "Deshavi", "Deshavi", tf_female|tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_khergit_bow, itm_bodkin_arrows, itm_sword_khergit_4, itm_dvor_archer_helm_2, itm_dvor_archer_armor, itm_dvor_archer_boot, itm_leather_gloves],
   str_15|agi_14|int_15|cha_6|level(19), regular_archer(19), 
   knows_ironflesh_2|knows_power_draw_5|knows_weapon_master_4|knows_athletics_4|knows_riding_4|knows_horse_archery_4|knows_tracking_5|knows_pathfinding_5|knows_spotting_5,
   0x000000067c0840033fe35117634d45cc00000000001e12760000000000000000],
   #ADENIAN LIGHT CAVALRY (Some Tactics):  Likes npc13, Dislikes npc3, npc12, and fleeing battle 
   ##Had 18 skills at lvl 7 (+8 at lvl 15 = 26 skills)
   ["npc8", "Matheld", "Matheld", tf_female|tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_sword_medieval_a, itm_steel_shield, itm_spear, itm_war_helm, itm_mail_shirt, itm_mail_chausses, itm_mail_mittens, itm_hunter],
   str_15|agi_12|int_9|cha_10|level(15), regular_melee(15), 
   knows_ironflesh_1|knows_power_strike_5|knows_weapon_master_4|knows_shield_4|knows_athletics_4|knows_riding_4|knows_tactics_2|knows_leadership_2,
   0x00000005800c000637db8314e331e76e00000000001c46db0000000000000000],
   #ANTARIAN NOBLE (Some Tactics):  Likes npc3, Dislikes npc2, npc13, and failing quests
   ##Had 16 skills at lvl 2 (+13 at lvl 15 = 29 skills)
   ["npc9", "Alayen", "Alayen", tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_bastard_sword_a, itm_antshield2, itm_anthelm1, itm_antplate1, itm_darkboots, itm_antgaunt2],
   str_18|agi_14|int_7|cha_8|level(15), regular_melee(15), 
   knows_ironflesh_6|knows_power_strike_6|knows_weapon_master_4|knows_shield_3|knows_athletics_3|knows_riding_4|knows_tactics_2|knows_leadership_1,
   0x000000030100300f499d5b391b6db8d300000000001dc2e10000000000000000],
   #MARINIAN TRAINED CROSSBOWMAN (Trainer, Tactics, Some heal):  Likes npc11, Dislikes npc14, npc4, taking from villagers, and heavy casualties
   ##Had 20 skills at lvl 9 (+6 at lvl 15 = 26 skills)
   ["npc10", "Bunduk", "Bunduk", tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_crossbow, itm_bolts, itm_club_with_spike_head, itm_tab_shield_pavise_a, itm_kettle_hat_b, itm_padded_leather, itm_leather_boots, itm_leather_gloves],
   str_12|agi_15|int_9|cha_10|level(15), regular_crossbow(15),
   knows_ironflesh_3|knows_power_strike_4|knows_weapon_master_2|knows_shield_5|knows_athletics_5|knows_riding_1|knows_trainer_3|knows_tactics_1|knows_first_aid_2,
   0x0000000bbf081006572c91c71c8d46cb00000000001e468a0000000000000000],
   #MARINIAN REGULAR (Trade, Some heal):  Likes npc10, Dislikes npc5, npc6, being hungry, and not being paid 
   ##Had 19 skills at lvl 8 (+7 at lvl 15 = 26 skills)
   ["npc11", "Katrin", "Katrin", tf_female|tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_realhalberda, itm_kettle_hat_b, itm_studded_leather_coat, itm_leather_boots, itm_leather_gloves],
   str_12|agi_12|int_9|cha_13|level(15), regular_melee(15), 
   knows_ironflesh_4|knows_power_strike_4|knows_weapon_master_4|knows_shield_2|knows_athletics_4|knows_riding_2|knows_first_aid_2|knows_trade_4,
   0x0000000d7f0400035915aa226b4d975200000000001ea49e0000000000000000],
   #MARINIAN LANDSKNECHT (Healer / Trade):  Likes npc6, Dislikes npc8, npc15, taking from villagers, and too much fighting
   ##Had 20 skills at lvl 4 (+5 IQ for total +21 at lvl 20 = 41 skills)
   ["npc12", "Jeremus", "Jeremus", tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_heavy_crossbow, itm_steel_bolts, itm_sword_medieval_b, itm_tab_shield_pavise_c, itm_marhelm2, itm_marchain2, itm_darkboots, itm_darkgauntlets],
   str_14|agi_12|int_18|cha_7|level(20), regular_crossbow(20),
   knows_ironflesh_2|knows_power_strike_4|knows_weapon_master_2|knows_shield_4|knows_athletics_4|knows_riding_4|knows_wound_treatment_6|knows_surgery_6|knows_first_aid_6|knows_trade_3,
   0x0000000f0000300e4f8ba62a9cd5d36d00000000001e36250000000000000000],
   #ZERRIKANIAN BOYAR SON (Training):  Likes npc8 and winning against tough odds, Dislikes npc6, and npc9
   ##Had 19 skills at lvl 3 (+12 at lvl 15 = 31 skills)
   ["npc13", "Nizar", "Nizar", tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_bastard_sword_a, itm_gold_jarid, itm_light_lance, itm_decor_aqua_shield, itm_zerrikanian_noble_helmet, itm_boyar_son_armor1, itm_white_boots, itm_mail_mittens, itm_rok_boyar_son_warhorse],
   str_13|agi_13|int_12|cha_8|level(15), regular_melee(15)|wp_throwing(120),
   knows_ironflesh_3|knows_power_strike_4|knows_power_throw_4|knows_weapon_master_4|knows_shield_4|knows_athletics_4|knows_riding_4|knows_trainer_4,
   0x00000004bf0471082f4d9592de4e57cc00000000001e389c0000000000000000],
   #IMPERIAL PRINCIPES (Trainer):  Likes npc15 and cruel acts, Dislikes npc3, and npc10 
   ##Had 19 skills at lvl 5 (+2 IQ for total +17 at lvl 20 = 36 skills)
   ["npc14", "Lezalit", "Lezalit", tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_legion_sword_kopis, itm_legion_spear_palton, itm_tab_shield_pavise_d, itm_legion_helm_01, itm_legion_armor_2, itm_black_army_boot_1, itm_black_army_leather_gloves],
   str_15|agi_15|int_13|cha_8|level(20), regular_melee(20),
   knows_ironflesh_4|knows_power_strike_5|knows_weapon_master_5|knows_shield_5|knows_athletics_5|knows_riding_5|knows_trainer_5|knows_leadership_2,
   0x00000004bf1025911415d1d6e335f96c00000000001db0f80000000000000000],
   #ADENIAN SQUIRE (Engineer, Trade, Tactics):  Likes npc14, Dislikes npc12, npc16, failing quests, being hungry, and heavy casualties
   ##Had 22 skills at lvl 7 (+3 IQ for total +12 at lvl 16 = 34 skills)
   ["npc15", "Artimenner", "Artimenner", tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_sword_viking_1, itm_two_handed_axe, itm_shield_heater_anklin, itm_bascinetnasal, itm_mail_hauberk, itm_mail_boots, itm_mail_mittens, itm_warhorse],
   str_12|agi_12|int_15|cha_8|level(16), regular_melee(16),
   knows_ironflesh_1|knows_power_strike_4|knows_weapon_master_4|knows_shield_4|knows_athletics_4|knows_riding_4|knows_tactics_5|knows_engineer_5|knows_trade_3,
   0x0000000f2e1021862b4b9123594eab5300000000001d55360000000000000000],
   #ANTARIAN JAVELIN THROWER (Tracker, Spotter, Pathfinder):  Likes npc7, Dislikes npc1, npc15, failing quests, being hungry, and heavy casualties
   ##Had 16 skills at lvl 2 (+16 at lvl 18 = 32 skills) 
   ["npc16", "Klethi", "Klethi", tf_female|tf_hero|tf_unmoveable_in_party_window, 0, reserved,  fac_commoners, 
   [itm_ant_angon, itm_sword_medieval_c_small, itm_antshield2, itm_spiked_helmet, itm_ant_lthr_coat, itm_mail_boots, itm_mail_mittens],
   str_18|agi_16|int_8|cha_7|level(18), expert_javelinmen(18),
   knows_ironflesh_1|knows_power_strike_6|knows_power_throw_6|knows_weapon_master_3|knows_shield_5|knows_athletics_5|knows_tracking_2|knows_pathfinding_2|knows_spotting_2,
   0x00000006c10c100739ce9c805d6f3e1300000000001cc7ad0000000000000000],

   #Special post-quest companion. Diego is recruited through the Slaver prison-break quest, not taverns.
   ["diego_companion", "Diego", "Diego", tf_hero|tf_unmoveable_in_party_window, 0, reserved, fac_commoners,
   [itm_slave_neck_chain, itm_twohandedmace, itm_stones],
   def_attrib|level(40), expert_melee(40), knows_power_throw_10|knows_shield_4|knows_ironflesh_10|knows_power_strike_10|knows_athletics_10, 0x0000000e260571403adfd5f2d10f466c00000000001dc71e0000000000000000],
#NPC system changes end

  ["kingdom_heroes_including_player_begin",  "kingdom_heroes_including_player_begin",  "kingdom_heroes_including_player_begin",  tf_hero, 0, reserved,  fac_kingdom_1, [], lord_attrib, wp_all(220), knows_lord_1, 0x000000000010918a01f248377289467d],

########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#FACTION KINGS                                                                                          Horse               Civilian Clothes       Civilian Footwear   Footwear_out        Armor_out                                      Weapon                                                              Shield                        Headwear
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  ["kingdom_1_lord",  "Harlaus",              "Kingdom 1 Lord",  tf_hero, 0, reserved,  fac_kingdom_1, [itm_kali,           itm_rich_outfit,       itm_blue_hose,      itm_iron_greaves,   itm_faith_old_gods_armor_3, itm_gauntlets,     itm_talak_mace, itm_great_lancec, itm_jarid,                        itm_tab_shield_heater_cav_b,  itm_crown3],         lord_attrib2, wp_all(500), knows_lord_2|knows_shield_10|knows_ironflesh_10|knows_athletics_10|knows_power_strike_10|knows_power_throw_10|knows_horse_archery_10|knows_trainer_5|knows_pathfinding_5,   0x0000000f45041105241acd2b5a66a86900000000001e98310000000000000000, swadian_face_older_2],
  ["kingdom_2_lord",  "Yaroglek",             "Kingdom 2 Lord",  tf_hero, 0, reserved,  fac_kingdom_2, [itm_leeko,          itm_courtly_outfit,    itm_leather_boots,  itm_iron_greaves,   itm_faith_old_gods_armor_2, itm_gauntlets,     itm_talak_bastard_sword, itm_strong_bow, itm_bodkin_arrows,         itm_tab_shield_kite_cav_b,    itm_crown],          lord_attrib2, wp_all(500), knows_lord_2|knows_shield_10|knows_ironflesh_10|knows_athletics_10|knows_power_strike_10|knows_power_draw_10|knows_horse_archery_10|knows_trainer_5|knows_pathfinding_5,    0x0000000ec50001400a2269f919dee11700000000001cc57d0000000000000000, vaegir_face_old_2],
  ["kingdom_3_lord",  "Sanjar",               "Kingdom 3 Lord",  tf_hero, 0, reserved,  fac_kingdom_3, [itm_garail,         itm_nomad_robe,        itm_leather_boots,  itm_iron_greaves,   itm_faith_old_gods_armor_1, itm_gauntlets,     itm_cimitar, itm_double_sided_lance, itm_gold_jarid,                itm_tab_shield_small_round_c, itm_crown_ornate],   lord_attrib2, wp_all(500), knows_lord_2|knows_shield_10|knows_ironflesh_10|knows_athletics_10|knows_power_strike_10|knows_power_throw_10|knows_horse_archery_10|knows_trainer_5|knows_pathfinding_5,   0x0000000cee0051cc44be2d14d370c65c00000000001ed6df0000000000000000, khergit_face_old_2],
  ["kingdom_4_lord",  "Ragnar",               "Kingdom 4 Lord",  tf_hero, 0, reserved,  fac_kingdom_4, [itm_makar,          itm_nobleman_outfit,   itm_leather_boots,  itm_iron_greaves,   itm_heraldic_black_armor,   itm_gauntlets,     itm_nordic_axe, itm_war_spear, itm_throwing_axes,                   itm_tab_shield_heater_cav_b,  itm_crown2],         lord_attrib2, wp_all(500), knows_lord_2|knows_shield_10|knows_ironflesh_10|knows_athletics_10|knows_power_strike_10|knows_power_throw_10|knows_horse_archery_10|knows_trainer_5|knows_pathfinding_5,   0x0000000e2c0c028a068e8c18557b12a500000000001c0fe80000000000000000, nord_face_older_2],
  ["kingdom_5_lord",  "Graveth",              "Kingdom 5 Lord",  tf_hero, 0, reserved,  fac_kingdom_5, [itm_asizar,         itm_courtly_outfit,    itm_leather_boots,  itm_iron_greaves,   itm_faith_the_one_armor_1,  itm_gauntlets,     itm_talak_mace, itm_light_crossbow, itm_steel_bolts,                itm_tab_shield_heater_cav_b,  itm_crown_ornate],   lord_attrib2, wp_all(500), knows_lord_2|knows_shield_10|knows_ironflesh_10|knows_athletics_10|knows_power_strike_10|knows_power_draw_10|knows_horse_archery_10|knows_trainer_6|knows_pathfinding_5,    0x0000000efc04119225848dac5d50d62400000000001d48b80000000000000000, rhodok_face_old_2],
  ["kingdom_6_lord",  "Gaius Marius",         "Kingdom 6 Lord",  tf_hero, 0, reserved,  fac_kingdom_6, [itm_legion_horse_6, itm_legion_chiton_red, itm_woolen_hose,    itm_legion_greaves, itm_legion_armor_4,         itm_darkgauntlets, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1,          itm_legion_helm_02], lord_attrib2, wp_all(500), knows_lord_2|knows_shield_10|knows_ironflesh_10|knows_athletics_10|knows_power_strike_10|knows_power_throw_10|knows_horse_archery_10|knows_trainer_10|knows_pathfinding_10, 0x0000000fff0060051294a3734f1bffff00000000001d4cf80000000000000000],


########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#SWADIAN LORDS                                                                       Horse                        Civilian Clothes     Armor                            Civilian Footwear           Footwear_out                         Headwear                                       Weapon                                           Shield
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  ["knight_1_1", "Klargus", "knight_1_1",     tf_hero, 0, reserved,  fac_kingdom_1, [itm_khergitnoblehorse,       itm_courtly_outfit,  itm_heraldic_mail_with_surcoat,  itm_nomad_boots,            itm_splinted_greaves,                itm_great_helmet,        itm_scale_gauntlets,  itm_sword_medieval_c,                            itm_tab_shield_heater_cav_a],  knight_attrib_1, wp_all(130), knight_skills_1|knows_trainer_3, 0x0000000c3e08601414ab4dc6e39296b200000000001e231b0000000000000000, swadian_face_middle_2],
  ["knight_1_2", "Plais", "knight_1_2",       tf_hero, 0, reserved,  fac_kingdom_1, [itm_heraldicchargerone,      itm_gambeson,        itm_heraldic_mail_with_surcoat,  itm_blue_hose,              itm_mail_boots,                      itm_nasal_helmet,        itm_scale_gauntlets,  itm_fighting_pick,                               itm_tab_shield_heater_c],      knight_attrib_2, wp_all(160), knight_skills_2,                 0x0000000c0f08000458739a9a1476199800000000001fb6f10000000000000000, swadian_face_old_2],
  ["knight_1_3", "Mirchaud", "knight_1_3",    tf_hero, 0, reserved,  fac_kingdom_1, [itm_scorpioncharger,         itm_blue_gambeson,   itm_mail_hauberk,                itm_woolen_hose,            itm_mail_chausses,                   itm_guard_helmet,        itm_gauntlets,        itm_sword_two_handed_b,                          itm_tab_shield_heater_cav_b],  knight_attrib_3, wp_all(190), knight_skills_3,                 0x0000000c0610351048e325361d7236cd00000000001d532a0000000000000000, swadian_face_older_2],
  ["knight_1_4", "Stamar", "knight_1_4",      tf_hero, 0, reserved,  fac_kingdom_1, [itm_whitebirdongreencharger, itm_red_gambeson,    itm_heraldic_mail_with_surcoat,  itm_nomad_boots,            itm_iron_greaves,                    itm_guard_helmet,        itm_gauntlets,        itm_bastard_sword_a,                             itm_tab_shield_heater_cav_b],  knight_attrib_4, wp_all(220), knight_skills_4,                 0x0000000c03104490280a8cb2a24196ab00000000001eb4dc0000000000000000, swadian_face_older_2],
  ["knight_1_5", "Ryis", "knight_1_5",        tf_hero, 0, reserved,  fac_kingdom_1, [itm_whitedeercharger,        itm_nobleman_outfit, itm_coat_of_plates,              itm_leather_boots,          itm_splinted_leather_greaves,        itm_winged_great_helmet, itm_gauntlets,        itm_bastard_sword_b,    itm_sword_two_handed_a,  itm_tab_shield_heater_d],      knight_attrib_5, wp_all(250), knight_skills_5,                 0x0000000c330855054aa9aa431a48d74600000000001ed5240000000000000000, swadian_face_older_2],
  ["knight_1_6", "Meltor", "knight_1_6",      tf_hero, 0, reserved,  fac_kingdom_1, [itm_redandyellowbgnorthbow,  itm_rich_outfit,     itm_heraldic_mail_with_surcoat,  itm_nomad_boots,            itm_mail_boots,                      itm_guard_helmet,        itm_gauntlets,        itm_fighting_pick,                               itm_tab_shield_heater_c],      knight_attrib_1, wp_all(130), knight_skills_1,                 0x0000000c2a0805442b2c6cc98c8dbaac00000000001d389b0000000000000000, swadian_face_middle_2],
  ["knight_1_7", "Beranz", "knight_1_7",      tf_hero, 0, reserved,  fac_kingdom_1, [itm_darktealthreecircle,     itm_ragged_outfit,   itm_heraldic_mail_with_surcoat,  itm_nomad_boots,            itm_splinted_greaves,                itm_guard_helmet,        itm_gauntlets,        itm_sword_medieval_c,   itm_sword_two_handed_a,  itm_tab_shield_heater_c],      knight_attrib_2, wp_all(160), knight_skills_2,                 0x0000000c380c30c2392a8e5322a5392c00000000001e5c620000000000000000, swadian_face_old_2],
  ["knight_1_8", "Rafard", "knight_1_8",      tf_hero, 0, reserved,  fac_kingdom_1, [itm_blueflamemoon,           itm_short_tunic,     itm_heraldic_mail_with_tabard,   itm_leather_boots,          itm_mail_chausses,                   itm_nasal_helmet,        itm_scale_gauntlets,  itm_bastard_sword_a,                             itm_tab_shield_heater_cav_a],  knight_attrib_3, wp_all(190), knight_skills_3|knows_trainer_6, 0x0000000c3f10000532d45203954e192200000000001e47630000000000000000, swadian_face_older_2],
  ["knight_1_9", "Regas", "knight_1_9",       tf_hero, 0, reserved,  fac_kingdom_1, [itm_blackdotwhitered,        itm_rich_outfit,     itm_mail_hauberk,                itm_woolen_hose,            itm_mail_chausses,                   itm_great_helmet,        itm_gauntlets,        itm_sword_viking_3,     itm_sword_two_handed_a,  itm_tab_shield_heater_d],      knight_attrib_4, wp_all(210), knight_skills_4,                 0x0000000c5c0840034895654c9b660c5d00000000001e34530000000000000000, swadian_face_older_2],
  ["knight_1_10", "Grainwad", "knight_1_0",   tf_hero, 0, reserved,  fac_kingdom_1, [itm_tribowred,               itm_tabard,          itm_heraldic_mail_with_surcoat,  itm_leather_boots,          itm_mail_boots,                      itm_flat_topped_helmet,  itm_gauntlets,        itm_bastard_sword_b,    itm_sword_two_handed_b,  itm_tab_shield_heater_cav_b],  knight_attrib_5, wp_all(290), knight_skills_5|knows_trainer_5, 0x0000000c1e001500589dae4094aa291c00000000001e37a80000000000000000, swadian_face_older_2],
  ["knight_1_11", "Devlian", "knight_1_1",    tf_hero, 0, reserved,  fac_kingdom_1, [itm_goldbaseblackorament,    itm_courtly_outfit,  itm_heraldic_mail_with_surcoat,  itm_nomad_boots,            itm_splinted_greaves,                itm_great_helmet,        itm_gauntlets,        itm_sword_medieval_c,                            itm_tab_shield_heater_c],      knight_attrib_1, wp_all(130), knight_skills_1,                 0x000000095108144657a1ba3ad456e8cb00000000001e325a0000000000000000, swadian_face_middle_2],
  ["knight_1_12", "Rafarch", "knight_1_2",    tf_hero, 0, reserved,  fac_kingdom_1, [itm_ravisaris,               itm_gambeson,        itm_heraldic_mail_with_surcoat,  itm_blue_hose,              itm_mail_boots,                      itm_nasal_helmet,        itm_scale_gauntlets,  itm_fighting_pick,                               itm_tab_shield_heater_cav_b],  knight_attrib_2, wp_all(190), knight_skills_2|knows_trainer_4, 0x0000000c010c42c14d9d6918bdb336e200000000001dd6a30000000000000000, swadian_face_old_2],
  ["knight_1_13", "Rochabarth", "knight_1_3", tf_hero, 0, reserved,  fac_kingdom_1, [itm_whisparia,               itm_blue_gambeson,   itm_mail_hauberk,                itm_woolen_hose,            itm_mail_chausses,                   itm_winged_great_helmet, itm_gauntlets,        itm_sword_two_handed_a,                          itm_tab_shield_heater_cav_a],  knight_attrib_3, wp_all(210), knight_skills_3,                 0x0000000c150045c6365d8565932a8d6400000000001ec6940000000000000000, swadian_face_older_2],
  ["knight_1_14", "Delinard", "knight_1_4",   tf_hero, 0, reserved,  fac_kingdom_1, [itm_goldturqoisehorsebanner, itm_red_gambeson,    itm_heraldic_mail_with_surcoat,  itm_nomad_boots,            itm_iron_greaves,                    itm_guard_helmet,        itm_gauntlets,        itm_bastard_sword_a,                             itm_tab_shield_heater_cav_b],  knight_attrib_4, wp_all(240), knight_skills_4,                 0x0000000c0f0c320627627238dcd6599400000000001c573d0000000000000000, swadian_face_older_2],
  ["knight_1_15", "Haringoth", "knight_1_5",  tf_hero, 0, reserved,  fac_kingdom_1, [itm_lazarith,                itm_nobleman_outfit, itm_coat_of_plates,              itm_leather_boots,          itm_splinted_leather_greaves,        itm_flat_topped_helmet,  itm_gauntlets,        itm_bastard_sword_b,                             itm_tab_shield_heater_d],      knight_attrib_5, wp_all(260), knight_skills_5|knows_trainer_3, 0x0000000cb700210214ce89db276aa2f400000000001d36730000000000000000, swadian_face_older_2],
  ["knight_1_16", "Despin", "knight_1_6",     tf_hero, 0, reserved,  fac_kingdom_1, [itm_nishra,                  itm_rich_outfit,     itm_heraldic_mail_with_surcoat,  itm_nomad_boots,            itm_mail_boots,                      itm_great_helmet,        itm_gauntlets,        itm_fighting_pick,      itm_sword_two_handed_a,  itm_tab_shield_heater_cav_a],  knight_attrib_1, wp_all(120), knight_skills_1,                 0x00000008200012033d9b6d4a92ada53500000000001cc1180000000000000000, swadian_face_middle_2],
  ["knight_1_17", "Montewar", "knight_1_7",   tf_hero, 0, reserved,  fac_kingdom_1, [itm_yixis,                   itm_ragged_outfit,   itm_heraldic_mail_with_surcoat,  itm_nomad_boots,            itm_splinted_greaves,                itm_great_helmet,        itm_gauntlets,        itm_sword_medieval_c,   itm_sword_two_handed_a,  itm_tab_shield_heater_cav_a],  knight_attrib_2, wp_all(150), knight_skills_2,                 0x0000000c4d0840d24a9b2ab4ac2a332400000000001d34db0000000000000000, swadian_face_old_2],
  ["knight_1_18", "Clais", "knight_1_8",      tf_hero, 0, reserved,  fac_kingdom_1, [itm_asizar,                  itm_short_tunic,     itm_heraldic_mail_with_surcoat,  itm_leather_boots,          itm_mail_chausses,                   itm_winged_great_helmet, itm_gauntlets,        itm_bastard_sword_a,    itm_sword_two_handed_a,  itm_tab_shield_heater_d],      knight_attrib_3, wp_all(180), knight_skills_3|knows_trainer_4, 0x0000000c370c1194546469ca6c4e450e00000000001ebac40000000000000000, swadian_face_older_2],
  ["knight_1_19", "Deglan", "knight_1_9",     tf_hero, 0, reserved,  fac_kingdom_1, [itm_makar,                   itm_rich_outfit,     itm_mail_hauberk,                itm_woolen_hose,            itm_mail_chausses,                   itm_guard_helmet,        itm_gauntlets,        itm_sword_medieval_c,                            itm_tab_shield_heater_d],      knight_attrib_4, wp_all(200), knight_skills_4|knows_trainer_6, 0x0000000c0c1064864ba34e2ae291992b00000000001da8720000000000000000, swadian_face_older_2],
  ["knight_1_20", "Tredian", "knight_1_0",    tf_hero, 0, reserved,  fac_kingdom_1, [itm_garail,                  itm_tabard,          itm_heraldic_mail_with_surcoat,  itm_leather_boots,          itm_mail_boots,                      itm_winged_great_helmet, itm_gauntlets,        itm_bastard_sword_b,    itm_sword_two_handed_b,  itm_tab_shield_heater_cav_b],  knight_attrib_5, wp_all(240), knight_skills_5|knows_trainer_5, 0x0000000c0a08038736db74c6a396a8e500000000001db8eb0000000000000000, swadian_face_older_2],


########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#VAEGIR LORDS                                                                       Horse                         Civilian Clothes     Armor                            Civilian Footwear           Footwear_out                         Headwear                                       Weapon                                               Shield
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  ["knight_2_1", "Vuldrat", "knight_2_1",     tf_hero, 0, reserved,  fac_kingdom_2, [itm_kali,                    itm_fur_coat,        itm_padded_cloth,                itm_nomad_boots,            itm_splinted_leather_greaves,        itm_skullcap,             itm_mail_mittens,    itm_sword_viking_3,                                  itm_tab_shield_kite_c],        knight_attrib_1, wp_all(130), knight_skills_1|knows_trainer_3, 0x00000005590011c33d9b6d4a92ada53500000000001cc1180000000000000000, vaegir_face_middle_2],
  ["knight_2_2", "Naldera", "knight_2_2",     tf_hero, 0, reserved,  fac_kingdom_2, [itm_leeko,                   itm_rich_outfit,     itm_lamellar_armor,              itm_woolen_hose,            itm_mail_chausses,                   itm_nasal_helmet,         itm_mail_mittens,    itm_shortened_military_scythe,                       itm_tab_shield_kite_cav_a],    knight_attrib_2, wp_all(160), knight_skills_2,                 0x0000000c2a0015d249b68b46a98e176400000000001d95a40000000000000000, vaegir_face_old_2],
  ["knight_2_3", "Meriga", "knight_2_3",      tf_hero, 0, reserved,  fac_kingdom_2, [itm_garail,                  itm_short_tunic,     itm_mail_hauberk,                itm_woolen_hose,            itm_mail_chausses,                   itm_nordic_helmet,        itm_scale_gauntlets, itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_cav_b],    knight_attrib_3, wp_all(190), knight_skills_3,                 0x0000000c131031c546a38a2765b4c86000000000001e58d30000000000000000, vaegir_face_older_2],
  ["knight_2_4", "Khavel", "knight_2_4",      tf_hero, 0, reserved,  fac_kingdom_2, [itm_makar,                   itm_courtly_outfit,  itm_lamellar_armor,              itm_leather_boots,          itm_mail_boots,                      itm_khergit_guard_helmet, itm_scale_gauntlets, itm_bastard_sword_b,                                 itm_tab_shield_kite_cav_b],    knight_attrib_4, wp_all(220), knight_skills_4,                 0x0000000c2f0832c748f272540d8ab65900000000001d34e60000000000000000, vaegir_face_older_2],
  ["knight_2_5", "Doru", "knight_2_5",        tf_hero, 0, reserved,  fac_kingdom_2, [itm_asizar,                  itm_rich_outfit,     itm_haubergeon,                  itm_leather_boots,          itm_mail_chausses,                   itm_segmented_helmet,     itm_scale_gauntlets, itm_bastard_sword_b,                                 itm_tab_shield_kite_d],        knight_attrib_5, wp_all(250), knight_skills_5,                 0x0000000e310061435d76bb5f55bad9ad00000000001ed8ec0000000000000000, vaegir_face_older_2],
  ["knight_2_6", "Belgaru", "knight_2_6",     tf_hero, 0, reserved,  fac_kingdom_2, [itm_yixis,                   itm_nomad_vest,      itm_padded_cloth,                itm_woolen_hose,            itm_mail_chausses,                   itm_khergit_guard_helmet, itm_mail_mittens,    itm_sword_viking_3,                                  itm_tab_shield_kite_c],        knight_attrib_1, wp_all(130), knight_skills_1|knows_trainer_3, 0x0000000a0100421038da7157aa4e430a00000000001da8bc0000000000000000, vaegir_face_middle_2],
  ["knight_2_7", "Ralcha", "Ralcha",          tf_hero, 0, reserved,  fac_kingdom_2, [itm_nishra,                  itm_leather_jacket,  itm_mail_hauberk,                itm_leather_boots,          itm_mail_boots,                      itm_nordic_helmet,        itm_scale_gauntlets, itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_cav_a],    knight_attrib_2, wp_all(160), knight_skills_2|knows_trainer_4, 0x0000000c04100153335ba9390b2d277500000000001d89120000000000000000, vaegir_face_old_2],
  ["knight_2_8", "Vlan", "knight_2_8",        tf_hero, 0, reserved,  fac_kingdom_2, [itm_lazarith,                itm_nomad_robe,      itm_nomad_vest,                  itm_woolen_hose,            itm_mail_chausses,                   itm_nasal_helmet,         itm_scale_gauntlets, itm_shortened_military_scythe,                       itm_tab_shield_kite_d],        knight_attrib_3, wp_all(200), knight_skills_3|knows_trainer_5, 0x0000000c00046581234e8da2cdd248db00000000001f569c0000000000000000, vaegir_face_older_2],
  ["knight_2_9", "Mleza", "knight_2_9",       tf_hero, 0, reserved,  fac_kingdom_2, [itm_goldturqoisehorsebanner, itm_rich_outfit,     itm_haubergeon,                  itm_leather_boots,          itm_mail_chausses,                   itm_kettle_hat,           itm_scale_gauntlets, itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_d],        knight_attrib_4, wp_all(230), knight_skills_4,                 0x0000000c160451d2136469c4d9b159ad00000000001e28f10000000000000000, vaegir_face_older_2],
  ["knight_2_10", "Nelag", "knight_2_0",      tf_hero, 0, reserved,  fac_kingdom_2, [itm_whisparia,               itm_fur_coat,        itm_lamellar_armor,              itm_woolen_hose,            itm_mail_boots,                      itm_great_helmet,         itm_scale_gauntlets, itm_military_pick,                                   itm_tab_shield_kite_cav_b],    knight_attrib_5, wp_all(260), knight_skills_5|knows_trainer_6, 0x0000000f7c00520e66b76edd5cd5eb6e00000000001f691e0000000000000000, vaegir_face_older_2],
  ["knight_2_11", "Crahask", "knight_2_1",    tf_hero, 0, reserved,  fac_kingdom_2, [itm_ravisaris,               itm_leather_jacket,  itm_padded_cloth,                itm_nomad_boots,            itm_splinted_leather_greaves,        itm_khergit_guard_helmet, itm_scale_gauntlets, itm_sword_viking_3,                                  itm_tab_shield_kite_cav_a],    knight_attrib_1, wp_all(130), knight_skills_1,                 0x0000000c1d0821d236acd6991b74d69d00000000001e476c0000000000000000, vaegir_face_middle_2],
  ["knight_2_12", "Bracha", "knight_2_2",     tf_hero, 0, reserved,  fac_kingdom_2, [itm_goldbaseblackorament,    itm_rich_outfit,     itm_lamellar_armor,              itm_woolen_hose,            itm_mail_chausses,                   itm_nasal_helmet,         itm_mail_mittens,    itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_cav_a],    knight_attrib_2, wp_all(170), knight_skills_2,                 0x0000000c0f04024b2509d5d53944c6a300000000001d5b320000000000000000, vaegir_face_old_2],
  ["knight_2_13", "Druli", "knight_2_3",      tf_hero, 0, reserved,  fac_kingdom_2, [itm_tribowred,               itm_short_tunic,     itm_mail_hauberk,                itm_woolen_hose,            itm_mail_chausses,                   itm_nordic_helmet,        itm_scale_gauntlets, itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_cav_b],    knight_attrib_3, wp_all(190), knight_skills_3,                 0x0000000c680432d3392230cb926d56ca00000000001da69b0000000000000000, vaegir_face_older_2],
  ["knight_2_14", "Marmun", "knight_2_4",     tf_hero, 0, reserved,  fac_kingdom_2, [itm_blackdotwhitered,        itm_courtly_outfit,  itm_lamellar_armor,              itm_leather_boots,          itm_mail_boots,                      itm_guard_helmet,         itm_scale_gauntlets, itm_shortened_military_scythe,                       itm_tab_shield_kite_cav_b],    knight_attrib_4, wp_all(220), knight_skills_4|knows_trainer_6, 0x0000000c27046000471bd2e93375b52c00000000001dd5220000000000000000, vaegir_face_older_2],
  ["knight_2_15", "Gastya", "knight_2_5",     tf_hero, 0, reserved,  fac_kingdom_2, [itm_blueflamemoon,           itm_rich_outfit,     itm_haubergeon,                  itm_leather_boots,          itm_mail_chausses,                   itm_segmented_helmet,     itm_scale_gauntlets, itm_bastard_sword_b,  itm_shortened_military_scythe, itm_tab_shield_kite_cav_b],    knight_attrib_5, wp_all(250), knight_skills_5,                 0x0000000de50052123b6bb36de5d6eb7400000000001dd72c0000000000000000, vaegir_face_older_2],
  ["knight_2_16", "Harish", "knight_2_6",     tf_hero, 0, reserved,  fac_kingdom_2, [itm_darktealthreecircle,     itm_nomad_vest,      itm_padded_cloth,                itm_woolen_hose,            itm_mail_chausses,                   itm_nordic_helmet,        itm_mail_mittens,    itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_c],        knight_attrib_1, wp_all(120), knight_skills_1,                 0x000000085f00000539233512e287391d00000000001db7200000000000000000, vaegir_face_middle_2],
  ["knight_2_17", "Taisa", "Ralcha",          tf_hero, 0, reserved,  fac_kingdom_2, [itm_redandyellowbgnorthbow,  itm_leather_jacket,  itm_mail_hauberk,                itm_leather_boots,          itm_mail_boots,                      itm_guard_helmet,         itm_scale_gauntlets, itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_cav_a],    knight_attrib_2, wp_all(150), knight_skills_2,                 0x0000000a070c4387374bd19addd2a4ab00000000001e32cc0000000000000000, vaegir_face_old_2],
  ["knight_2_18", "Valishin", "knight_2_8",   tf_hero, 0, reserved,  fac_kingdom_2, [itm_whitedeercharger,        itm_nomad_robe,      itm_nomad_vest,                  itm_woolen_hose,            itm_mail_chausses,                   itm_nasal_helmet,         itm_scale_gauntlets, itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_cav_a],    knight_attrib_3, wp_all(180), knight_skills_3,                 0x0000000b670012c23d9b6d4a92ada53500000000001cc1180000000000000000, vaegir_face_older_2],
  ["knight_2_19", "Rudin", "knight_2_9",      tf_hero, 0, reserved,  fac_kingdom_2, [itm_whitebirdongreencharger, itm_rich_outfit,     itm_haubergeon,                  itm_leather_boots,          itm_mail_chausses,                   itm_guard_helmet,         itm_scale_gauntlets, itm_fighting_pick,  itm_shortened_military_scythe,   itm_tab_shield_kite_d],        knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_4, 0x0000000e070050853b0a6e4994ae272a00000000001db4e10000000000000000, vaegir_face_older_2],
  ["knight_2_20", "Kumipa", "knight_2_0",     tf_hero, 0, reserved,  fac_kingdom_2, [itm_scorpioncharger,         itm_fur_coat,        itm_lamellar_armor,              itm_woolen_hose,            itm_mail_boots,                      itm_great_helmet,         itm_scale_gauntlets, itm_two_handed_battle_axe_2,                         itm_tab_shield_kite_cav_b],    knight_attrib_5, wp_all(240), knight_skills_5|knows_trainer_5, 0x0000000f800021c63b0a6e4994ae272a00000000001db4e10000000000000000, vaegir_face_older_2],


########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#KHERGIT LORDS                                                                       Horse                        Civilian Clothes            Armor                   Civilian Footwear          Footwear_out                               Headwear                                           Weapon                                                                 Shield
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  ["knight_3_1", "Alagur", "knight_3_1",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_leather_vest,           itm_lamellar_armor,     itm_nomad_boots,           itm_mail_boots,                            itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_sword_khergit_3,           itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_c],  knight_attrib_1, wp_all(130), knight_skills_1|knows_horse_archery_5|knows_trainer_3|knows_power_draw_4, 0x000000043000318b54b246b7094dc39c00000000001d31270000000000000000, khergit_face_middle_2],
  ["knight_3_2", "Tonju",  "knight_3_2",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_nomad_vest,             itm_lamellar_armor,     itm_hide_boots,            itm_mail_boots,                            itm_khergit_cavalry_helmet, itm_scale_gauntlets,   itm_shortened_military_scythe, itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_b],  knight_attrib_2, wp_all(160), knight_skills_2|knows_horse_archery_5|knows_power_draw_4,                 0x0000000c280461004929b334ad632aa200000000001e05120000000000000000, khergit_face_old_2],
  ["knight_3_3", "Belir",  "knight_3_3",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_nomad_robe,             itm_lamellar_armor,     itm_nomad_boots,           itm_splinted_leather_greaves,              itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_fighting_pick,             itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_c],  knight_attrib_3, wp_all(190), knight_skills_3|knows_horse_archery_5|knows_trainer_5|knows_power_draw_4, 0x0000000e880062c53b0a6e4994ae272a00000000001db4e10000000000000000, khergit_face_older_2],
  ["knight_3_4", "Asugan", "knight_3_4",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_lamellar_vest,          itm_lamellar_armor,     itm_hide_boots,            itm_splinted_greaves,                      itm_khergit_cavalry_helmet, itm_scale_gauntlets,   itm_shortened_military_scythe,                                         itm_tab_shield_small_round_c],  knight_attrib_4, wp_all(220), knight_skills_4|knows_horse_archery_5|knows_power_draw_4,                 0x0000000c23085386391b5ac72a96d95c00000000001e37230000000000000000, khergit_face_older_2],
  ["knight_3_5", "Brula",  "knight_3_5",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_ragged_outfit,          itm_lamellar_armor,     itm_hide_boots,            itm_mail_boots,                            itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_sword_khergit_3,                                                   itm_tab_shield_small_round_c],  knight_attrib_5, wp_all(250), knight_skills_5|knows_horse_archery_6|knows_power_draw_5,                 0x0000000efe0051ca4b377b4964b6eb6500000000001f696c0000000000000000, khergit_face_older_2],
  ["knight_3_6", "Imirza", "knight_3_6",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_lamellar_vest,          itm_lamellar_armor,     itm_hide_boots,            itm_splinted_leather_greaves,              itm_khergit_cavalry_helmet, itm_scale_gauntlets,   itm_sword_khergit_4,                                                   itm_tab_shield_small_round_b],  knight_attrib_1, wp_all(130), knight_skills_1|knows_horse_archery_5|knows_power_draw_4,                 0x00000006f600418b54b246b7094dc31a00000000001d37270000000000000000, khergit_face_middle_2],
  ["knight_3_7", "Urumuda", "knight_3_7",     tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_tribal_warrior_outfit,  itm_lamellar_armor,     itm_leather_boots,         itm_hide_boots,                            itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_sword_khergit_3,                                                   itm_tab_shield_small_round_b],  knight_attrib_2, wp_all(160), knight_skills_2|knows_horse_archery_5|knows_power_draw_4,                 0x0000000bdd00510a44be2d14d370c65c00000000001ed6df0000000000000000, khergit_face_old_2],
  ["knight_3_8", "Kramuk", "knight_3_8",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_nomad_vest,             itm_lamellar_armor,     itm_woolen_hose,           itm_splinted_greaves,                      itm_khergit_cavalry_helmet, itm_scale_gauntlets,   itm_two_handed_battle_axe_2,                                           itm_tab_shield_small_round_c],  knight_attrib_3, wp_all(190), knight_skills_3|knows_horse_archery_5|knows_power_draw_4,                 0x0000000abc00518b5af4ab4b9c8e596400000000001dc76d0000000000000000, khergit_face_older_2],
  ["knight_3_9", "Chaurka", "knight_3_9",     tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_nomad_robe,             itm_lamellar_armor,     itm_leather_boots,         itm_splinted_leather_greaves,              itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_military_pick,                                                     itm_tab_shield_small_round_c],  knight_attrib_4, wp_all(220), knight_skills_4|knows_horse_archery_5|knows_power_draw_4,                 0x0000000a180441c921a30ea68b54971500000000001e54db0000000000000000, khergit_face_older_2],
  ["knight_3_10", "Sebula", "knight_3_0",     tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_lamellar_vest,          itm_lamellar_armor,     itm_hide_boots,            itm_mail_chausses,                         itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_sword_khergit_4,           itm_shortened_military_scythe,          itm_tab_shield_small_round_c],  knight_attrib_5, wp_all(250), knight_skills_5|knows_horse_archery_6|knows_trainer_6|knows_power_draw_5, 0x0000000a3b00418c5b36c686d920a76100000000001c436f0000000000000000, khergit_face_older_2],
  ["knight_3_11", "Tulug", "knight_3_1",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_leather_vest,           itm_lamellar_armor,     itm_nomad_boots,           itm_mail_boots,                            itm_khergit_cavalry_helmet, itm_leather_gloves,    itm_sword_khergit_4,           itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_b],  knight_attrib_1, wp_all(150), knight_skills_1|knows_horse_archery_5|knows_power_draw_4,                 0x00000007d100534b44962d14d370c65c00000000001ed6df0000000000000000, khergit_face_middle_2],
  ["knight_3_12", "Nasugei", "knight_3_2",    tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_nomad_vest,             itm_lamellar_armor,     itm_hide_boots,            itm_mail_boots,                            itm_khergit_guard_helmet,   itm_leather_gloves,    itm_sword_khergit_3,                                                   itm_tab_shield_small_round_b],  knight_attrib_2, wp_all(190), knight_skills_2|knows_horse_archery_5|knows_power_draw_4,                 0x0000000bf400610c5b33d3c9258edb6c00000000001eb96d0000000000000000, khergit_face_old_2],
  ["knight_3_13", "Urubay", "knight_3_3",     tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_nomad_robe,             itm_lamellar_armor,     itm_nomad_boots,           itm_splinted_leather_greaves,              itm_khergit_cavalry_helmet, itm_scale_gauntlets,   itm_fighting_pick,             itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_c],  knight_attrib_3, wp_all(200), knight_skills_3|knows_horse_archery_5|knows_trainer_3|knows_power_draw_4, 0x0000000bfd0061c65b6eb33b25d2591d00000000001f58eb0000000000000000, khergit_face_older_2],
  ["knight_3_14", "Hugu",  "knight_3_4",      tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_lamellar_vest,          itm_lamellar_armor,     itm_hide_boots,            itm_splinted_greaves,                      itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_shortened_military_scythe, itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_c],  knight_attrib_4, wp_all(300), knight_skills_4|knows_horse_archery_5|knows_trainer_6|knows_power_draw_4, 0x0000000b6900514144be2d14d370c65c00000000001ed6df0000000000000000, khergit_face_older_2],
  ["knight_3_15", "Tansugai", "knight_3_5",   tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_ragged_outfit,          itm_lamellar_armor,     itm_hide_boots,            itm_mail_boots,                            itm_khergit_cavalry_helmet, itm_sword_khergit_4,   itm_shortened_military_scythe,                                         itm_tab_shield_small_round_c],  knight_attrib_5, wp_all(240), knight_skills_5|knows_horse_archery_6|knows_trainer_4|knows_power_draw_5, 0x0000000c360c524b6454465b59b9d93500000000001ea4860000000000000000, khergit_face_older_2],
  ["knight_3_16", "Tirida", "knight_3_6",     tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_tribal_warrior_outfit,  itm_lamellar_armor,     itm_hide_boots,            itm_splinted_leather_greaves,              itm_khergit_guard_helmet,   itm_leather_gloves,    itm_sword_khergit_4,           itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_b],  knight_attrib_1, wp_all(120), knight_skills_1|knows_horse_archery_5|knows_power_draw_4,                 0x0000000c350c418438ab85b75c61b8d300000000001d21530000000000000000, khergit_face_middle_2],
  ["knight_3_17", "Ulusamai", "knight_3_7",   tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_leather_vest,           itm_lamellar_armor,     itm_leather_boots,         itm_mail_boots,                            itm_khergit_guard_helmet,   itm_leather_gloves,    itm_two_handed_battle_axe_2,   itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_c],  knight_attrib_2, wp_all(150), knight_skills_2|knows_horse_archery_5|knows_power_draw_4,                 0x0000000c3c0821c647264ab6e68dc4d500000000001e42590000000000000000, khergit_face_old_2],
  ["knight_3_18", "Karaban", "knight_3_8",    tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_nomad_vest,             itm_lamellar_armor,     itm_hide_boots,            itm_splinted_greaves,                      itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_war_axe,                   itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_c],  knight_attrib_3, wp_all(180), knight_skills_3|knows_horse_archery_5|knows_trainer_4|knows_power_draw_4, 0x0000000c0810500347ae7acd0d3ad74a00000000001e289a0000000000000000, khergit_face_older_2],
  ["knight_3_19", "Akadan", "knight_3_9",     tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_nomad_robe,             itm_lamellar_armor,     itm_leather_boots,         itm_splinted_leather_greaves,              itm_khergit_cavalry_helmet, itm_scale_gauntlets,   itm_sword_khergit_4,           itm_shortened_military_scythe,          itm_tab_shield_small_round_c],  knight_attrib_4, wp_all(210), knight_skills_4|knows_horse_archery_5|knows_trainer_5|knows_power_draw_4, 0x0000000c1500510528f50d52d20b152300000000001d66db0000000000000000, khergit_face_older_2],
  ["knight_3_20", "Dundush", "knight_3_0",    tf_hero, 0, reserved,  fac_kingdom_3, [itm_khergitnoblehorse,       itm_dynasty_outfit,         itm_lamellar_armor,     itm_dynasty_oufit_greaves, itm_mail_chausses,                         itm_khergit_guard_helmet,   itm_scale_gauntlets,   itm_sword_khergit_4,           itm_khergit_bow, itm_khergit_arrows,    itm_tab_shield_small_round_c],  knight_attrib_5, wp_all(240), knight_skills_5|knows_horse_archery_6|knows_power_draw_5,                 0x0000000f7800620d66b76edd5cd5eb6e00000000001f691e0000000000000000, khergit_face_older_2],


########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#NORD LORDS                                                                          Horse                        Civilian Clothes  Armor               Civilian Footwear Footwear_out    Headwear                                   Weapon                                 Shield
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  ["knight_4_1", "Aedin", "knight_4_1",       tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_3|knows_power_throw_6, 0x0000000c13002254340eb1d91159392d00000000001eb75a0000000000000000, nord_face_middle_2],
  ["knight_4_2", "Irya", "knight_4_2",        tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_3|knows_trainer_3|knows_power_throw_5, 0x0000000c1610218368e29744e9a5985b00000000001db2a10000000000000000, nord_face_old_2],
  ["knight_4_3", "Olaf", "knight_4_3",        tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_3|knows_power_throw_6, 0x0000000c03040289245a314b744b30a400000000001eb2a90000000000000000, nord_face_older_2],
  ["knight_4_4", "Reamald", "knight_4_4",     tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_3|knows_trainer_3|knows_power_throw_5, 0x0000000c3f1001ca3d6955b26a8939a300000000001e39b60000000000000000, nord_face_older_2],
  ["knight_4_5", "Turya", "knight_4_5",       tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_5|knows_trainer_6|knows_power_throw_7, 0x0000000ff508330546dc4a59422d450c00000000001e51340000000000000000, nord_face_older_2],
  ["knight_4_6", "Gundur", "knight_4_6",      tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_3|knows_power_throw_6, 0x00000005b00011813d9b6d4a92ada53500000000001cc1180000000000000000, nord_face_middle_2],
  ["knight_4_7", "Harald", "knight_4_7",      tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_3|knows_trainer_3|knows_power_throw_5, 0x00000006690002873d9b6d4a92ada53500000000001cc1180000000000000000, nord_face_old_2],
  ["knight_4_8", "Knudarr", "knight_4_8",     tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_3|knows_power_throw_6, 0x0000000f830051c53b026e4994ae272a00000000001db4e10000000000000000, nord_face_older_2],
  ["knight_4_9", "Haeda", "knight_4_9",       tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_5|knows_trainer_6|knows_power_throw_7, 0x0000000c230401c6349c2e9b2168eb1a00000000001eb0630000000000000000, nord_face_older_2],
  ["knight_4_10", "Turegor", "knight_4_0",    tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_5|knows_trainer_6|knows_power_throw_7, 0x000000084b0002063d9b6d4a92ada53500000000001cc1180000000000000000, nord_face_older_2],
  ["knight_4_11", "Logarson", "knight_4_1",   tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_3|knows_trainer_3|knows_power_throw_5, 0x0000000ca100224d56a5d5c65c70c40a00000000001d54de0000000000000000, nord_face_middle_2],
  ["knight_4_12", "Aeric", "knight_4_2",      tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_5|knows_trainer_6|knows_power_throw_7, 0x0000000b9500020824936cc51cb5bb2500000000001dd4d80000000000000000, nord_face_old_2],
  ["knight_4_13", "Faarn", "knight_4_3",      tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_3|knows_power_throw_6, 0x0000000a300012c439233512e287391d00000000001db7200000000000000000, nord_face_older_2],
  ["knight_4_14", "Bulba", "knight_4_4",      tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_3|knows_trainer_3|knows_power_throw_5, 0x0000000c0700414f2cb6aa36ea50a69d00000000001dc55c0000000000000000, nord_face_older_2],
  ["knight_4_15", "Rayeck", "knight_4_5",     tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_3|knows_power_throw_6, 0x0000000d920801831715d1aa9221372300000000001ec6630000000000000000, nord_face_older_2],
  ["knight_4_16", "Dirigun", "knight_4_6",    tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_5|knows_trainer_6|knows_power_throw_7, 0x000000099700124239233512e287391d00000000001db7200000000000000000, nord_face_middle_2],
  ["knight_4_17", "Marayirr", "knight_4_7",   tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_3|knows_power_throw_6, 0x0000000c2f0442036d232a2324b5b81400000000001e55630000000000000000, nord_face_old_2],
  ["knight_4_18", "Gearth", "knight_4_8",     tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_3|knows_trainer_3|knows_power_throw_5, 0x0000000c0d00118866e22e3d9735a72600000000001eacad0000000000000000, nord_face_older_2],
  ["knight_4_19", "Surdun", "knight_4_9",     tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_3|knows_power_throw_6, 0x0000000c0308225124e26d4a6295965a00000000001d23e40000000000000000, nord_face_older_2],
  ["knight_4_20", "Gerlad", "knight_4_0",     tf_hero, 0, reserved,  fac_kingdom_4, [                             itm_rich_outfit,  itm_cuir_bouilli,   itm_woolen_hose,  itm_gauntlets,  itm_winged_great_helmet, itm_iron_greaves, itm_jomsviking_axe, itm_throwing_axes, itm_tab_shield_round_d], knight_attrib_4, wp_all(210), knight_skills_5|knows_trainer_6|knows_power_throw_7, 0x0000000f630052813b6bb36de5d6eb7400000000001dd72c0000000000000000, nord_face_older_2],


########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#RHODOK LORDS                                                                       Horse                   Civilian Clothes    Armor                             Civilian Footwear     Footwear_out                   Headwear                                       Weapon                                        Shield
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  ["knight_5_1", "Matheas", "knight_5_1",     tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_tabard,         itm_heraldic_mail_with_surcoat,   itm_leather_boots,    itm_mail_boots,                itm_guard_helmet,        itm_leather_gloves,   itm_fighting_pick,                            itm_tab_shield_heater_c], knight_attrib_1, wp_all(130), knight_skills_1|knows_trainer_3, 0x0000000a1b0c00483adcbaa5ac9a34a200000000001ca2d40000000000000000, rhodok_face_middle_2],
  ["knight_5_2", "Gutlans", "knight_5_2",     tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_red_gambeson,   itm_heraldic_mail_with_tabard,    itm_leather_boots,    itm_mail_boots,                itm_nasal_helmet,        itm_leather_gloves,   itm_military_pick,  itm_sword_two_handed_a,   itm_tab_shield_heater_c], knight_attrib_2, wp_all(160), knight_skills_2|knows_trainer_4, 0x0000000c390c659229136db45a75251300000000001f16930000000000000000, rhodok_face_old_2],
  ["knight_5_3", "Laruqen", "knight_5_3",     tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_short_tunic,    itm_mail_and_plate,               itm_nomad_boots,      itm_splinted_leather_greaves,  itm_kettle_hat,          itm_gauntlets,        itm_shortened_military_scythe,                itm_tab_shield_heater_d], knight_attrib_3, wp_all(190), knight_skills_3,                 0x0000000c2f10415108b1aacba27558d300000000001d329c0000000000000000, rhodok_face_older_2],
  ["knight_5_4", "Raichs", "knight_5_4",      tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_leather_jacket, itm_brigandine_a,                 itm_woolen_hose,      itm_splinted_greaves,          itm_flat_topped_helmet,  itm_gauntlets,        itm_bastard_sword_a,                          itm_tab_shield_heater_d], knight_attrib_4, wp_all(220), knight_skills_4,                 0x0000000c3c005110345c59d56975ba1200000000001e24e40000000000000000, rhodok_face_older_2],
  ["knight_5_5", "Reland", "knight_5_5",      tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_rich_outfit,    itm_heraldic_mail_with_tabard,    itm_leather_boots,    itm_mail_boots,                itm_great_helmet,        itm_gauntlets,        itm_shortened_military_scythe,                itm_tab_shield_heater_d], knight_attrib_5, wp_all(250), knight_skills_5,                 0x0000000c060400c454826e471092299a00000000001d952d0000000000000000, rhodok_face_older_2],
  ["knight_5_6", "Tarchias", "knight_5_6",    tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_ragged_outfit,  itm_heraldic_mail_with_tabard,    itm_woolen_hose,      itm_splinted_greaves,          itm_skullcap,            itm_gauntlets,        itm_sword_two_handed_b,                       itm_tab_shield_heater_c], knight_attrib_1, wp_all(130), knight_skills_1,                 0x0000000c040804d2293c46a6a5669ce400000000001db7120000000000000000, rhodok_face_middle_2],
  ["knight_5_7", "Gharmall", "knight_5_7",    tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_coarse_tunic,   itm_heraldic_mail_with_surcoat,   itm_leather_boots,    itm_mail_chausses,             itm_nasal_helmet,        itm_gauntlets,        itm_bastard_sword_a,                          itm_tab_shield_heater_c], knight_attrib_2, wp_all(160), knight_skills_2,                 0x0000000c3a0455c443d46e4c8b91291a00000000001ca51b0000000000000000, rhodok_face_old_2],
  ["knight_5_8", "Talbar", "knight_5_8",      tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_courtly_outfit, itm_heraldic_mail_with_tabard,    itm_woolen_hose,      itm_mail_boots,                itm_nasal_helmet,        itm_gauntlets,        itm_military_pick, itm_sword_two_handed_b,    itm_tab_shield_heater_c], knight_attrib_3, wp_all(190), knight_skills_3|knows_trainer_3, 0x0000000c2c0844d42914d19b2369b4ea00000000001e331b0000000000000000, rhodok_face_older_2],
  ["knight_5_9", "Rimusk", "knight_5_9",      tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_leather_jacket, itm_heraldic_mail_with_tabard,    itm_leather_boots,    itm_splinted_leather_greaves,  itm_kettle_hat,          itm_gauntlets,        itm_two_handed_battle_axe_2,                  itm_tab_shield_heater_d], knight_attrib_4, wp_all(220), knight_skills_4|knows_trainer_6, 0x0000000c130461054af448eb19cd40e400000000001d488a0000000000000000, rhodok_face_older_2],
  ["knight_5_10", "Falsevor", "knight_5_0",   tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_rich_outfit,    itm_heraldic_mail_with_tabard,    itm_blue_hose,        itm_mail_chausses,             itm_great_helmet,        itm_gauntlets,        itm_bastard_sword_a,                          itm_tab_shield_heater_d], knight_attrib_5, wp_all(250), knight_skills_5|knows_trainer_4, 0x00000008e20011063d9b6d4a92ada53500000000001cc1180000000000000000, rhodok_face_older_2],
  ["knight_5_11", "Etrosq", "knight_5_1",     tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_tabard,         itm_heraldic_mail_with_surcoat,   itm_leather_boots,    itm_mail_boots,                itm_skullcap,            itm_leather_gloves,   itm_fighting_pick,                            itm_tab_shield_heater_c], knight_attrib_1, wp_all(130), knight_skills_1,                 0x0000000c170c14874752adb6eb3228d500000000001c955c0000000000000000, rhodok_face_middle_2],
  ["knight_5_12", "Kurnias", "knight_5_2",    tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_red_gambeson,   itm_heraldic_mail_with_tabard,    itm_leather_boots,    itm_mail_boots,                itm_nasal_helmet,        itm_leather_gloves,   itm_military_pick,                            itm_tab_shield_heater_c], knight_attrib_2, wp_all(160), knight_skills_2|knows_trainer_5, 0x0000000c080c13d056ec8da85e3126ed00000000001d4ce60000000000000000, rhodok_face_old_2],
  ["knight_5_13", "Tellrog", "knight_5_3",    tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_short_tunic,    itm_mail_and_plate,               itm_nomad_boots,      itm_splinted_leather_greaves,  itm_winged_great_helmet, itm_gauntlets,        itm_sword_two_handed_a,                       itm_tab_shield_heater_d], knight_attrib_3, wp_all(190), knight_skills_3,                 0x0000000cbf10100562a4954ae731588a00000000001d6b530000000000000000, rhodok_face_older_2],
  ["knight_5_14", "Tribidan", "knight_5_4",   tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_leather_jacket, itm_brigandine_a,                 itm_woolen_hose,      itm_splinted_greaves,          itm_flat_topped_helmet,  itm_gauntlets,        itm_bastard_sword_a,                          itm_tab_shield_heater_d], knight_attrib_4, wp_all(220), knight_skills_4,                 0x0000000c330805823baa77556c4e331a00000000001cb9110000000000000000, rhodok_face_older_2],
  ["knight_5_15", "Gerluchs", "knight_5_5",   tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_rich_outfit,    itm_heraldic_mail_with_tabard,    itm_leather_boots,    itm_mail_boots,                itm_great_helmet,        itm_gauntlets,        itm_sword_two_handed_a,                       itm_tab_shield_heater_d], knight_attrib_5, wp_all(250), knight_skills_5,                 0x0000000d51000106370c4d4732b536de00000000001db9280000000000000000, rhodok_face_older_2],
  ["knight_5_16", "Fudreim", "knight_5_6",    tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_ragged_outfit,  itm_heraldic_mail_with_tabard,    itm_woolen_hose,      itm_splinted_greaves,          itm_guard_helmet,        itm_leather_gloves,   itm_fighting_pick,                            itm_tab_shield_heater_c], knight_attrib_1, wp_all(120), knight_skills_1,                 0x0000000c06046151435b5122a37756a400000000001c46e50000000000000000, rhodok_face_middle_2],
  ["knight_5_17", "Nealcha", "knight_5_7",    tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_coarse_tunic,   itm_heraldic_mail_with_surcoat,   itm_leather_boots,    itm_mail_chausses,             itm_nasal_helmet,        itm_leather_gloves,   itm_bastard_sword_a,                          itm_tab_shield_heater_c], knight_attrib_2, wp_all(150), knight_skills_2,                 0x0000000c081001d3465c89a6a452356300000000001cda550000000000000000, rhodok_face_old_2],
  ["knight_5_18", "Fraichin", "knight_5_8",   tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_courtly_outfit, itm_heraldic_mail_with_tabard,    itm_woolen_hose,      itm_mail_boots,                itm_nasal_helmet,        itm_gauntlets,        itm_military_pick,                            itm_tab_shield_heater_d], knight_attrib_3, wp_all(180), knight_skills_3,                 0x0000000a3d0c13c3452aa967276dc95c00000000001dad350000000000000000, rhodok_face_older_2],
  ["knight_5_19", "Trimbau", "knight_5_9",    tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_leather_jacket, itm_heraldic_mail_with_tabard,    itm_leather_boots,    itm_splinted_leather_greaves,  itm_kettle_hat,          itm_gauntlets,        itm_fighting_pick,  itm_sword_two_handed_a,   itm_tab_shield_heater_d], knight_attrib_4, wp_all(210), knight_skills_4|knows_trainer_5, 0x0000000c3f08038245545e3b236a68de00000000001e37230000000000000000, rhodok_face_older_2],
  ["knight_5_20", "Reichsin", "knight_5_0",   tf_hero, 0, reserved,  fac_kingdom_5, [                       itm_rich_outfit,    itm_heraldic_mail_with_tabard,    itm_blue_hose,        itm_mail_chausses,             itm_great_helmet,        itm_gauntlets,        itm_bastard_sword_b,                          itm_tab_shield_heater_d], knight_attrib_5, wp_all(240), knight_skills_5|knows_trainer_6, 0x0000000d8a00514544be2d14d370c65c00000000001ed6df0000000000000000, rhodok_face_older_2],


########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#PLAYER KINGDOM LORDS                                                                   Horse              Civilian Clothes    Armor                            Civilian Footwear          Footwear_out                    Headwear                 Weapon                                        Shield
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  ["reserved_knight_1", "Pechnak", "knight_5_1",   tf_hero, 0, reserved,  fac_neutral, [itm_saddle_horse,  itm_tabard,         itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_mail_boots,                 itm_skullcap,            itm_fighting_pick,                            itm_tab_shield_heater_c], knight_attrib_1, wp_all(100), knight_skills_1|knows_trainer_1|knows_horse_archery_3|knows_power_throw_3|knows_power_draw_3, 0x0000000a1b0c00483adcbaa5ac9a34a200000000001ca2d40000000000000000, rhodok_face_middle_2],
  ["reserved_knight_2", "Daynad", "knight_5_2",    tf_hero, 0, reserved,  fac_neutral, [itm_saddle_horse,  itm_ragged_outfit,  itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_mail_boots,                 itm_nasal_helmet,        itm_military_pick,  itm_sword_two_handed_a,   itm_tab_shield_heater_c], knight_attrib_1, wp_all(100), knight_skills_1|knows_trainer_1|knows_horse_archery_3|knows_power_throw_3|knows_power_draw_3, 0x0000000c390c659229136db45a75251300000000001f16930000000000000000, rhodok_face_old_2],
  ["reserved_knight_3", "Joayah", "knight_5_3",    tf_hero, 0, reserved,  fac_neutral, [itm_saddle_horse,  itm_short_tunic,    itm_heraldic_mail_with_surcoat,  itm_nomad_boots,           itm_splinted_leather_greaves,   itm_kettle_hat,          itm_shortened_military_scythe,                itm_tab_shield_heater_d], knight_attrib_1, wp_all(100), knight_skills_1|knows_trainer_1|knows_horse_archery_3|knows_power_throw_3|knows_power_draw_3, 0x0000000c2f10415108b1aacba27558d300000000001d329c0000000000000000, rhodok_face_older_2],
  ["reserved_knight_4", "Marlund", "knight_5_4",   tf_hero, 0, reserved,  fac_neutral, [itm_saddle_horse,  itm_leather_jacket, itm_heraldic_mail_with_surcoat,  itm_woolen_hose,           itm_splinted_greaves,           itm_flat_topped_helmet,  itm_bastard_sword_a,                          itm_tab_shield_heater_d], knight_attrib_1, wp_all(100), knight_skills_1|knows_trainer_1|knows_horse_archery_3|knows_power_throw_3|knows_power_draw_3, 0x0000000c3c005110345c59d56975ba1200000000001e24e40000000000000000, rhodok_face_older_2],
  ["reserved_knight_5", "Taarl", "knight_5_5",     tf_hero, 0, reserved,  fac_neutral, [itm_saddle_horse,  itm_ragged_outfit,  itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_mail_boots,                 itm_great_helmet,        itm_shortened_military_scythe,                itm_tab_shield_heater_d], knight_attrib_1, wp_all(100), knight_skills_1|knows_trainer_1|knows_horse_archery_4|knows_power_throw_4|knows_power_draw_4, 0x0000000c060400c454826e471092299a00000000001d952d0000000000000000, rhodok_face_older_2],
  ["reserved_knight_6", "Euscarl", "knight_5_6",   tf_hero, 0, reserved,  fac_neutral, [itm_courser,       itm_ragged_outfit,  itm_heraldic_mail_with_surcoat,  itm_woolen_hose,           itm_splinted_greaves,           itm_skullcap,            itm_military_pick, itm_sword_medieval_c,                       itm_tab_shield_heater_c], knight_attrib_2, wp_all(130), knight_skills_2|knows_trainer_2|knows_horse_archery_4|knows_power_throw_4|knows_power_draw_4, 0x0000000c040804d2293c46a6a5669ce400000000001db7120000000000000000, rhodok_face_middle_2],
  ["reserved_knight_7", "Sigmar", "knight_5_7",    tf_hero, 0, reserved,  fac_neutral, [itm_courser,       itm_coarse_tunic,   itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_mail_chausses,              itm_nasal_helmet,        itm_bastard_sword_a,                          itm_tab_shield_heater_c], knight_attrib_2, wp_all(130), knight_skills_2|knows_trainer_2|knows_horse_archery_4|knows_power_throw_4|knows_power_draw_4, 0x0000000c3a0455c443d46e4c8b91291a00000000001ca51b0000000000000000, rhodok_face_old_2],
  ["reserved_knight_8", "Talesqe", "knight_5_8",   tf_hero, 0, reserved,  fac_neutral, [itm_courser,       itm_courtly_outfit, itm_heraldic_mail_with_surcoat,  itm_woolen_hose,           itm_mail_boots,                 itm_nasal_helmet,        itm_military_pick,  itm_sword_two_handed_b,   itm_tab_shield_heater_c], knight_attrib_2, wp_all(130), knight_skills_2|knows_trainer_2|knows_horse_archery_4|knows_power_throw_4|knows_power_draw_4, 0x0000000c2c0844d42914d19b2369b4ea00000000001e331b0000000000000000, rhodok_face_older_2],
  ["reserved_knight_9", "Aels", "knight_5_9",      tf_hero, 0, reserved,  fac_neutral, [itm_courser,       itm_leather_jacket, itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_splinted_leather_greaves,   itm_kettle_hat,          itm_military_pick, itm_two_handed_battle_axe_2,                  itm_tab_shield_heater_d], knight_attrib_2, wp_all(130), knight_skills_2|knows_trainer_2|knows_horse_archery_4|knows_power_throw_4|knows_power_draw_4, 0x0000000c130461054af448eb19cd40e400000000001d488a0000000000000000, rhodok_face_older_2],
  ["reserved_knight_10", "Raurqe", "knight_5_0",   tf_hero, 0, reserved,  fac_neutral, [itm_courser,       itm_rich_outfit,    itm_heraldic_mail_with_surcoat,  itm_blue_hose,             itm_mail_chausses,              itm_great_helmet,        itm_bastard_sword_a,                          itm_tab_shield_heater_d], knight_attrib_2, wp_all(130), knight_skills_2|knows_trainer_2|knows_horse_archery_4|knows_power_throw_4|knows_power_draw_4, 0x00000008e20011063d9b6d4a92ada53500000000001cc1180000000000000000, rhodok_face_older_2],
  ["reserved_knight_11", "Bragamus", "knight_5_1", tf_hero, 0, reserved,  fac_neutral, [itm_hunter,        itm_tabard,         itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_mail_boots,                 itm_skullcap,            itm_fighting_pick,                            itm_tab_shield_heater_c], knight_attrib_3, wp_all(180), knight_skills_3|knows_trainer_3|knows_horse_archery_5|knows_power_throw_5|knows_power_draw_5, 0x0000000c170c14874752adb6eb3228d500000000001c955c0000000000000000, rhodok_face_middle_2],
  ["reserved_knight_12", "Ramin", "knight_5_2",    tf_hero, 0, reserved,  fac_neutral, [itm_hunter,        itm_red_gambeson,   itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_mail_boots,                 itm_nasal_helmet,        itm_military_pick,                            itm_tab_shield_heater_c], knight_attrib_3, wp_all(180), knight_skills_3|knows_trainer_3|knows_horse_archery_5|knows_power_throw_5|knows_power_draw_5, 0x0000000c080c13d056ec8da85e3126ed00000000001d4ce60000000000000000, rhodok_face_old_2],
  ["reserved_knight_13", "Shulk", "knight_5_3",    tf_hero, 0, reserved,  fac_neutral, [itm_hunter,        itm_short_tunic,    itm_heraldic_mail_with_surcoat,  itm_nomad_boots,           itm_splinted_leather_greaves,   itm_kettle_hat,          itm_military_pick, itm_sword_two_handed_a,                       itm_tab_shield_heater_d], knight_attrib_3, wp_all(180), knight_skills_3|knows_trainer_3|knows_horse_archery_5|knows_power_throw_5|knows_power_draw_5, 0x0000000cbf10100562a4954ae731588a00000000001d6b530000000000000000, rhodok_face_older_2],
  ["reserved_knight_14", "Putar", "knight_5_4",    tf_hero, 0, reserved,  fac_neutral, [itm_hunter,        itm_leather_jacket, itm_heraldic_mail_with_surcoat,  itm_woolen_hose,           itm_splinted_greaves,           itm_flat_topped_helmet,  itm_bastard_sword_a,                          itm_tab_shield_heater_d], knight_attrib_3, wp_all(180), knight_skills_3|knows_trainer_3|knows_horse_archery_5|knows_power_throw_5|knows_power_draw_5, 0x0000000c330805823baa77556c4e331a00000000001cb9110000000000000000, rhodok_face_older_2],
  ["reserved_knight_15", "Reichad", "knight_5_5",  tf_hero, 0, reserved,  fac_neutral, [itm_warhorse,      itm_rich_outfit,    itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_mail_boots,                 itm_great_helmet,        itm_military_pick, itm_sword_two_handed_a,                       itm_tab_shield_heater_d], knight_attrib_4, wp_all(220), knight_skills_4|knows_trainer_4|knows_horse_archery_6|knows_power_throw_6|knows_power_draw_6, 0x0000000d51000106370c4d4732b536de00000000001db9280000000000000000, rhodok_face_older_2],
  ["reserved_knight_16", "Walcheas", "knight_5_6", tf_hero, 0, reserved,  fac_neutral, [itm_warhorse,      itm_ragged_outfit,  itm_heraldic_mail_with_surcoat,  itm_woolen_hose,           itm_splinted_greaves,           itm_skullcap,            itm_fighting_pick,                            itm_tab_shield_heater_c], knight_attrib_4, wp_all(220), knight_skills_4|knows_trainer_4|knows_horse_archery_6|knows_power_throw_6|knows_power_draw_6, 0x0000000c06046151435b5122a37756a400000000001c46e50000000000000000, rhodok_face_middle_2],
  ["reserved_knight_17", "Rulkh", "knight_5_7",    tf_hero, 0, reserved,  fac_neutral, [itm_warhorse,      itm_coarse_tunic,   itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_mail_chausses,              itm_nasal_helmet,        itm_bastard_sword_a,                          itm_tab_shield_heater_c], knight_attrib_4, wp_all(220), knight_skills_4|knows_trainer_4|knows_horse_archery_6|knows_power_throw_6|knows_power_draw_6, 0x0000000c081001d3465c89a6a452356300000000001cda550000000000000000, rhodok_face_old_2],
  ["reserved_knight_18", "Ramar", "knight_5_8",    tf_hero, 0, reserved,  fac_neutral, [itm_charger,       itm_courtly_outfit, itm_heraldic_mail_with_surcoat,  itm_woolen_hose,           itm_mail_boots,                 itm_nasal_helmet,        itm_military_pick,                            itm_tab_shield_heater_d], knight_attrib_5, wp_all(280), knight_skills_5|knows_trainer_6|knows_horse_archery_7|knows_power_throw_7|knows_power_draw_7, 0x0000000a3d0c13c3452aa967276dc95c00000000001dad350000000000000000, rhodok_face_older_2],
  ["reserved_knight_19", "Caldaran", "knight_5_9", tf_hero, 0, reserved,  fac_neutral, [itm_charger,       itm_rich_outfit,    itm_heraldic_mail_with_surcoat,  itm_leather_boots,         itm_splinted_leather_greaves,   itm_kettle_hat,          itm_fighting_pick,  itm_sword_two_handed_a,   itm_tab_shield_heater_d], knight_attrib_5, wp_all(280), knight_skills_5|knows_trainer_6|knows_horse_archery_7|knows_power_throw_7|knows_power_draw_7, 0x0000000c3f08038245545e3b236a68de00000000001e37230000000000000000, rhodok_face_older_2],
  ["reserved_knight_20", "Brabas", "knight_5_0",   tf_hero, 0, reserved,  fac_neutral, [itm_charger,       itm_dynasty_outfit, itm_heraldic_mail_with_surcoat,  itm_dynasty_oufit_greaves, itm_mail_chausses,              itm_great_helmet,        itm_bastard_sword_b,                          itm_tab_shield_heater_d], knight_attrib_5, wp_all(280), knight_skills_5|knows_trainer_6|knows_horse_archery_7|knows_power_throw_7|knows_power_draw_7, 0x0000000d8a00514544be2d14d370c65c00000000001ed6df0000000000000000, rhodok_face_older_2],

#Gave horse archery, power throw, and power draw to all units because some civilizations will spawn with these weapons.  It will not matter to civs that do not (lord skills not accessible)
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#LEGION LORDS                                                                                                     Horse               Bodywear_in                 Armor               Footwear_in       Footwear_out                           Headwear            Weapons                                                             Shield
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
  ["knight_6_01", "Marcus", "knight_4_0",      tf_hero,                   0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000],
  ["knight_6_02", "Oraelius", "knight_4_0",    tf_hero,                   0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x000000003f0410060923ac28a470f2e100000000001d7a1a0000000000000000],
  ["knight_6_03", "Agustus", "knight_4_0",     tf_hero,                   0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x00000007ff0430050923ac28a470f2e100000000001d7a1a0000000000000000],
  ["knight_6_04", "Helios", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2], #all faces below this point are randomly generated
  ["knight_6_05", "Keplos", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_06", "Velious", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_07", "Corelius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_08", "Varinius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_09", "Otho", "knight_4_0",        tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_10", "Hilarious", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_11", "Mercury", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_12", "Faunus", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_13", "Romulus", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_14", "Quirinus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_15", "Tertius", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_16", "Adeodatus", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_17", "Liber", "knight_4_0",       tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_18", "Victorius", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_19", "Laurentius", "knight_4_0",  tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_20", "Fidelis", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_21", "Sidonius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_22", "Pomponius", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_23", "Silvanus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_24", "Publius", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_25", "Valerius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_26", "Camillus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_27", "Aquila", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_28", "Thracius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_29", "Gallus", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_30", "Crescentius", "knight_4_0", tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_31", "Spurius", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_32", "Summanus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_33", "Quintus", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_34", "Cornelius", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_35", "Decimus", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_36", "Seneca", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_37", "Octavius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_38", "Cato", "knight_4_0",        tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_39", "Cicero", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_40", "Faustus", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_41", "Rufus", "knight_4_0",       tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_42", "Longinus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_43", "Pontius", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_44", "Narcissus", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_45", "Marianus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_46", "Vulcan", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_47", "Jove", "knight_4_0",        tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_48", "Secundus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_49", "Sergius", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_50", "Honoratus", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_51", "Evander", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_52", "Aeneas", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_53", "Hadrianus", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_54", "Cassian", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_55", "Livius", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_56", "Cnaeus", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_57", "Agrippa", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_58", "Aurelius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_59", "Cyriacus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_60", "Titus", "knight_4_0",       tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_61", "Herminius", "knight_4_0",   tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_62", "Avitus", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_63", "Lucius", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_64", "Terminus", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_65", "Claudius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_66", "Maurus", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_67", "Saturninus", "knight_4_0",  tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_68", "Leonius", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_69", "Horatius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_70", "Remus", "knight_4_0",       tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_71", "Marinus", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_72", "Victor", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_73", "Appius", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_74", "Brutus", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_75", "Consus", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_76", "Tiberius", "knight_4_0",    tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_77", "Felix", "knight_4_0",       tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  ["knight_6_78", "Maximus", "knight_4_0",     tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, swadian_face_older_2],
  ["knight_6_79", "Julius", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_red,      itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_5, wp_all(410), knight_skills_5|knows_power_throw_5|knows_trainer_2|knows_pathfinding_5, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, nord_face_older_2],
  ["knight_6_80", "Pollux", "knight_4_0",      tf_hero|tf_randomize_face, 0, reserved, fac_kingdom_6,  [itm_legion_horse_6, itm_legion_chiton_half_red, itm_legion_armor_4, itm_woolen_hose,  itm_legion_greaves, itm_darkgauntlets, itm_legion_helm_12, itm_legion_spear_kamax, itm_legion_sword_centurion, itm_gold_jarid, itm_legion_shield_1],  knight_attrib_4, wp_all(350), knight_skills_4|knows_power_throw_4|knows_trainer_2|knows_pathfinding_4, 0x0000000ef50020052694af19cfb969d600000000001d4ced0000000000000000, rhodok_face_older_2],
  
##################################################################################################################################
# MERCENARY GUILD LEADERS
##################################################################################################################################
  ["black_army_leader_1", "Captain_Mogar_Blasius", "Captain_Mogar_Blasius", tf_hero, 0, reserved, fac_sod_merc_guild1, 
   [itm_bastard_sword_b, itm_black_army_shield_2, itm_flintlock_pistol, itm_cartridges, 
    itm_black_general_helm, itm_black_armor, itm_black_greaves, itm_darkgauntlets,
    itm_charger_black],
   def_attrib|level(27), expert_melee(27)|wp_firearm(270), knows_riding_5|knows_horse_archery_7|knows_power_strike_4|knows_shield_4|knows_athletics_4|knows_tactics_2|knows_leadership_3, 0x00000007230962850aaab016ad2b385200000000001dcaf50000000000000000],

  ["conquistador_leader_1", "Lieutenant_Agnessa", "Lieutenant_Agnessa", tf_female|tf_hero, 0, reserved, fac_sod_merc_guild2, 
   [itm_light_crossbow, itm_steel_bolts, itm_foil, itm_buckler_2,
    itm_conquistador_helm3, itm_conquistador_plate_2, itm_iron_greaves, itm_gauntlets,
    itm_conquistador_horse_1],
   def_attrib|level(27), expert_all(27), knows_riding_5|knows_horse_archery_6|knows_power_strike_5|knows_shield_4|knows_athletics_4|knows_tactics_2|knows_leadership_3, 0x000000053f04000238626616db9648f200000000001ee0a30000000000000000],

  ["elephant_guard_leader_1", "Warchief_Bongani", "Warchief_Bongani", tf_hero, 0, reserved, fac_sod_merc_guild3, 
   [itm_elephant_guard_sickle_2, itm_elephant_heater_3, itm_elephant_tribe_two_side_spear, itm_throwing_daggers, 
    itm_elephant_guard_shaman_helm, itm_elephant_guard_tribesman_body_11, itm_elephant_guard_gloves, itm_elephant_guard_shaman_boots], 
   def_attrib|level(27), wp_melee(270)|wp_thrown(270), knows_shield_7|knows_ironflesh_10|knows_power_strike_5|knows_power_throw_5|knows_athletics_7|knows_tactics_2|knows_leadership_3, 0x00000006bf01200058b481ab2b4d699c00000000001f36f60000000000000000], #wp_throwing proficiency brings value to 270 (like expert)

  ["jotnar_clan_leader_1", "Gunnard_Bearmasher", "Gunnard_Bearmasher", tf_hero, 0, reserved, fac_sod_merc_guild4, 
   [itm_dblhead_axe_1, itm_mountainlordsword, itm_war_spear, itm_jotnar_clan_shield_5, 
    itm_jotnar_clan_helm_9, itm_jotnar_clan_armor_3, itm_iron_greaves, itm_gauntlets, 
    itm_jotnar_clan_horse_1],
   def_attrib|level(27), expert_melee(27), knows_riding_3|knows_power_strike_7|knows_athletics_4|knows_tactics_2|knows_leadership_3, 0x0000000f630c5347395b28e6eb862b3200000000001eb9610000000000000000],

  ["serpent_host_leader_1", "Young_Chief_Pinar", "Young_Chief_Pinar", tf_hero, 0, reserved, fac_sod_merc_guild5, 
   [itm_war_spear, itm_khergit_bow, itm_khergit_arrows, itm_serpent_host_shield_round_2,
    itm_serpent_host_helm_3, itm_serpent_host_armor_3, itm_scale_gauntlets, itm_serpent_host_boots_1, 
    itm_serpent_horse_5],
   def_attrib|level(27), expert_all(27), knows_riding_5|knows_power_strike_5|knows_horse_archery_5|knows_power_draw_5|knows_shield_5|knows_athletics_4|knows_tactics_2|knows_leadership_3, 0x00000004a810338b30f575b51d6db45e00000000001f54fb0000000000000000],

  ["slaver_leader_1", "Slaver_Lieutenant", "Slaver_Lieutenant", tf_hero, 0, reserved, fac_sod_merc_guild6, 
   [itm_talak_mace, itm_arena_lance, itm_throwing_military_hammers, itm_dragonshield,
    itm_horned_helm3, itm_breast_plate_mail5, itm_iron_greaves, itm_gauntlets, 
    itm_warhorse], 
   def_attrib|level(27), expert_melee(27), knows_trade_2|knows_riding_4|knows_horse_archery_2|knows_power_throw_3|knows_shield_4|knows_ironflesh_2|knows_power_strike_4|knows_athletics_5|knows_tactics_2|knows_leadership_3, 0x000000049e1010450cb62d3efa8dd31c00000000001cc91a0000000000000000],


##################################################################################################################################
# PRETENDERS
##################################################################################################################################
  ["kingdom_1_pretender", "Isolla", "Kingdom 1 Lord",      tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved,  fac_kingdom_1,  [itm_charger,   itm_rich_outfit,      itm_blue_hose,        itm_iron_greaves,               itm_mail_shirt,           itm_sword_medieval_c_small,   itm_tab_shield_small_round_c,   itm_bascinet],              lord_attrib, wp_all(220), knows_lord_1, 0x00000000ef00000237dc71b90c31631200000000001e371b0000000000000000],
  #Claims pre-salic descent
  ["kingdom_2_pretender", "Valdym", "Kingdom 2 Lord",  tf_hero|tf_unmoveable_in_party_window,           0, reserved,  fac_kingdom_2,  [itm_hunter,    itm_courtly_outfit,   itm_leather_boots,    itm_mail_chausses,              itm_lamellar_armor,       itm_military_pick,            itm_tab_shield_heater_b,        itm_flat_topped_helmet],    lord_attrib, wp_all(220), knows_lord_1, 0x00000000200412142452ed631b30365c00000000001c94e80000000000000000, vaegir_face_middle_2],
  #Had his patrimony falsified
  ["kingdom_3_pretender", "Dustum", "Kingdom 3 Lord",         tf_hero|tf_unmoveable_in_party_window,           0, reserved,  fac_kingdom_3,  [itm_courser,   itm_nomad_robe,       itm_leather_boots,    itm_splinted_greaves,           itm_khergit_guard_armor,  itm_sword_khergit_2,          itm_tab_shield_small_round_c,   itm_segmented_helmet],      lord_attrib, wp_all(220), knows_lord_1, 0x000000065504310b30d556b51238f66100000000001c256d0000000000000000, khergit_face_middle_2],
  #Of the family
  ["kingdom_4_pretender", "Lethwin", "Kingdom 4 Lord",  tf_hero|tf_unmoveable_in_party_window,           0, reserved,  fac_kingdom_4,  [itm_hunter,    itm_tabard,           itm_leather_boots,    itm_mail_boots,                 itm_brigandine_a,         itm_sword_medieval_c,         itm_tab_shield_heater_cav_a,    itm_kettle_hat],            lord_attrib, wp_all(220), knows_lord_1, 0x00000004340c01841d89949529a6776a00000000001c910a0000000000000000, nord_face_young_2],
  #Dispossessed and wronged
  ["kingdom_5_pretender", "Kastor", "Kingdom 5 Lord",    tf_hero|tf_unmoveable_in_party_window,           0, reserved,  fac_kingdom_5,  [itm_warhorse,  itm_nobleman_outfit,  itm_leather_boots,    itm_splinted_leather_greaves,   itm_mail_hauberk,         itm_sword_medieval_c,         itm_tab_shield_heater_d,        itm_spiked_helmet],         lord_attrib, wp_all(220), knows_lord_1, 0x0000000bed1031051da9abc49ecce25e00000000001e98680000000000000000, rhodok_face_old_2],
  #Republican

##################################################################################################################################
# MERCENARY GUILD MASTERS
##################################################################################################################################

#Black Army Guild Master (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["black_army_guild_master", "General_Matias_Corves", "General_Matias_Corves", tf_hero, scn_sod_merc_guild_1|entry(10), reserved, fac_sod_merc_guild1, 
    [itm_flintlock_pistol, itm_cartridges, itm_talak_mace, itm_black_army_shield_2,
    itm_black_general_helm, itm_black_general_armor, itm_black_greaves, itm_darkgauntlets,
    itm_charger_black],
   def_attrib|level(30), expert_melee(30)|wp_firearm(300), knows_riding_7|knows_horse_archery_7|knows_power_strike_3|knows_shield_5|knows_athletics_4|knows_tactics_5|knows_leadership_5, 0x0000000ffc0972933f5dc5175bcb471100000000001d272c0000000000000000],
   

#Conquistador Guild Master (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["conquistador_guild_master", "Saint_Malo", "Saint_Malo", tf_hero, scn_sod_merc_guild_2|entry(10), reserved, fac_sod_merc_guild2, 
    [itm_great_lancec, itm_sword_medieval_b_small, itm_tab_shield_heater_cav_b,
    itm_conquistador_helm3, itm_conquistador_plate_1, itm_iron_greaves, itm_gauntlets,
    itm_conquistador_horse_2],
   def_attrib|level(30), expert_melee(30), knows_riding_5|knows_power_strike_6|knows_shield_5|knows_athletics_4|knows_tactics_5|knows_leadership_5, 0x0000000dbf00251436db6db6db6db6db00000000001db6db0000000000000000],


#Elephant Guard Guild Master (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["elephant_guard_guild_master", "Khepri", "Khepri", tf_female|tf_hero, scn_sod_merc_guild_3|entry(10), reserved, fac_sod_merc_guild3, 
  [itm_elephant_tribe_two_side_spear, itm_throwing_daggers, itm_throwing_daggers, itm_throwing_daggers, 
   itm_elephant_guard_priestess_wig, itm_elephant_guard_priestess_body, itm_elephant_guard_gloves, itm_nobleman_greaves], 
  def_attrib|level(30), wp_melee(300)|wp_thrown(300), knows_shield_8|knows_ironflesh_10|knows_power_strike_7|knows_power_throw_10|knows_athletics_8|knows_tactics_6|knows_leadership_7, 0x000000002510400235a46055048341dc00000000001ea84d0000000000000000],


#Jotnar Clan Guild Master (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["jotnar_clan_guild_master", "Mistress_Velandir", "Mistress_Velandir", tf_female|tf_hero, scn_sod_merc_guild_4|entry(10), reserved, fac_sod_merc_guild4, 
    [itm_dblhead_axe_1, itm_war_bow, itm_bodkin_arrows, itm_jotnar_clan_shield_4, 
    itm_jotnar_clan_helm_9, itm_jotnar_clan_armor_7, itm_iron_greaves, itm_gauntlets], 
   def_attrib|level(30), expert_all(30), knows_riding_3|knows_power_strike_6|knows_power_draw_5|knows_athletics_6|knows_tactics_5|knows_leadership_5, 0x000000068400e002575d6db6db8de7fd00000000001db6da0000000000000000],


#Serpent Host Guild Master (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["serpent_host_guild_master", "Bhey_Sukbathar", "Bhey_Sukbathar", tf_hero, scn_sod_merc_guild_5|entry(10), reserved, fac_sod_merc_guild5, 
    [itm_cimitar, itm_strong_bow, itm_khergit_arrows, itm_serpent_host_shield_round_2,
    itm_serpent_host_helm_3, itm_serpent_host_armor_7, itm_scale_gauntlets, itm_serpent_host_boots_1, 
    itm_serpent_horse_6],
   def_attrib|level(40), expert_all(40), knows_riding_5|knows_power_strike_6|knows_horse_archery_6|knows_power_draw_8|knows_shield_5|knows_ironflesh_10|knows_athletics_8|knows_tactics_5|knows_leadership_5, 0x0000000fc20043081217af091a8a889300000000001d48780000000000000000],


#Slaver Guild Master (have to move outside "mercenaries_end" so they will not spawn in taverns)
  ["slaver_guild_master", "Slaver_Chief", "Slaver_Chief", tf_hero, 0, reserved, fac_sod_merc_guild6, 
  [itm_twohandedmace, itm_iron_staff, itm_throwing_military_hammers, itm_dragonshield,
   itm_horned_helm1, itm_dark_plate2, itm_darkboots, itm_darkgauntlets, 
   itm_charger], 
   def_attrib|level(30), expert_melee(30), knows_trade_5|knows_riding_4|knows_horse_archery_2|knows_power_throw_3|knows_shield_4|knows_ironflesh_2|knows_power_strike_5|knows_athletics_5|knows_tactics_5|knows_leadership_5, 0x0000000fd5105592385281c55b8e44eb00000000001d9b220000000000000000],


#Boar Clan Guild Master (have to move outside "mercenaries_end" so they will not spawn in taverns)
   ["boar_clan_guild_master", "Warlord Akeem Olaju", "Warlord Akeem Olaju", tf_hero, scn_boar_clan_base|entry(10), reserved, fac_sod_merc_guild7,
   [itm_gladiator_helmet, itm_heraldic_banded_armor, itm_mail_mittens, itm_mail_boots, itm_shield_heater_boar, 
    itm_battle_fork_1, itm_maul, itm_war_camel_1],
   def_attrib|level(30), expert_melee(30), knows_riding_7|knows_power_strike_7|knows_shield_7|knows_athletics_5|knows_tactics_5|knows_leadership_5, 0x0000000eff111294426b8db96132d89e00000000001e14ea0000000000000000],

   
  ["slave_hero", "One-Eyed Slave", "One-Eyed Slave", tf_hero|tf_inactive, 0, reserved, fac_commoners,
   [itm_slave_neck_chain, itm_twohandedmace, itm_stones],
   def_attrib|level(40), expert_melee(40), knows_power_throw_10|knows_shield_4|knows_ironflesh_10|knows_power_strike_10|knows_athletics_10, 0x0000000e260571403adfd5f2d10f466c00000000001dc71e0000000000000000],

##################################################################################################################################
# KINGS
##################################################################################################################################
#  ["kingdom_1_lord_a", "Kingdom 1 Lord A", "Kingdom 1 Lord A", tf_hero, 0, reserved,  fac_kingdom_1, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_b", "Kingdom 1 Lord B", "Kingdom 1 Lord B", tf_hero, 0, reserved,  fac_kingdom_2, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_c", "Kingdom 1 Lord C", "Kingdom 1 Lord C", tf_hero, 0, reserved,  fac_kingdom_3, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_d", "Kingdom 1 Lord D", "Kingdom 1 Lord D", tf_hero, 0, reserved,  fac_kingdom_1, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_e", "Kingdom 1 Lord E", "Kingdom 1 Lord E", tf_hero, 0, reserved,  fac_kingdom_1, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_f", "Kingdom 1 Lord F", "Kingdom 1 Lord F", tf_hero, 0, reserved,  fac_kingdom_1, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_g", "Kingdom 1 Lord G", "Kingdom 1 Lord G", tf_hero, 0, reserved,  fac_kingdom_1, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_h", "Kingdom 1 Lord H", "Kingdom 1 Lord H", tf_hero, 0, reserved,  fac_kingdom_2, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_i", "Kingdom 1 Lord I", "Kingdom 1 Lord I", tf_hero, 0, reserved,  fac_kingdom_2, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_j", "Kingdom 1 Lord J", "Kingdom 1 Lord J", tf_hero, 0, reserved,  fac_kingdom_2, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_k", "Kingdom 1 Lord K", "Kingdom 1 Lord K", tf_hero, 0, reserved,  fac_kingdom_2, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_l", "Kingdom 1 Lord L", "Kingdom 1 Lord L", tf_hero, 0, reserved,  fac_kingdom_3, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_m", "Kingdom 1 Lord M", "Kingdom 1 Lord M", tf_hero, 0, reserved,  fac_kingdom_3, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],
#  ["kingdom_1_lord_n", "Kingdom 1 Lord N", "Kingdom 1 Lord N", tf_hero, 0, reserved,  fac_kingdom_3, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x00000000000c710201fa51b7286db721],

#  ["town_1_ruler_a", "King Harlaus",  "King Harlaus",  tf_hero, scn_town_1_castle|entry(9), reserved,  fac_swadians, [itm_saddle_horse, itm_courtly_outfit, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000010908101e36db44b75b6dd],
#  ["town_2_ruler_a", "Duke Taugard",  "Duke Taugard",  tf_hero, scn_town_2_castle|entry(9), reserved,  fac_swadians, [itm_saddle_horse, itm_courtly_outfit, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000000310401e06db86375f6da],
#  ["town_3_ruler_a", "Count Grimar",  "Count Grimar",  tf_hero, scn_town_3_castle|entry(9), reserved, fac_swadians, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004430301e46136eb75bc0a],
#  ["town_4_ruler_a", "Count Haxalye", "Count Haxalye", tf_hero, scn_town_4_castle|entry(9), reserved,  fac_swadians, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000010918701e77136e905bc0e
#  ["town_5_ruler_a", "Count Belicha", "Count Belicha", tf_hero, scn_town_5_castle|entry(9), reserved, fac_swadians, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000421c801e7713729c5b8ce],
#  ["town_6_ruler_a", "Count Nourbis", "Count Nourbis", tf_hero, scn_town_6_castle|entry(9), reserved,  fac_swadians, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c640501e371b72bcdb724],
#  ["town_7_ruler_a", "Count Rhudolg", "Count Rhudolg", tf_hero, scn_town_7_castle|entry(9), reserved,  fac_swadians, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c710201fa51b7286db721],

#  ["town_8_ruler_b", "King Yaroglek", "King_yaroglek", tf_hero, scn_town_8_castle|entry(9), reserved,  fac_vaegirs, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000000128801f294ca6d66d555],
#  ["town_9_ruler_b", "Count Aolbrug", "Count_Aolbrug", tf_hero, scn_town_9_castle|entry(9), reserved,  fac_vaegirs, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004234401f26a271c8d38ea],
#  ["town_10_ruler_b", "Count Rasevas", "Count_Rasevas", tf_hero, scn_town_10_castle|entry(9), reserved, fac_vaegirs, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000001032c201f38e269372471c],
#  ["town_11_ruler_b", "Count Leomir",  "Count_Leomir",  tf_hero, scn_town_11_castle|entry(9), reserved,  fac_vaegirs, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c538001f55148936d3895],
#  ["town_12_ruler_b", "Count Haelbrad", "Count_Haelbrad", tf_hero, scn_town_12_castle|entry(9), reserved,  fac_vaegirs, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000410c701f38598ac8aaaab],
#  ["town_13_ruler_b", "Count Mira",    "Count_Mira",    tf_hero, scn_town_13_castle|entry(9), reserved, fac_vaegirs, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004204401f390c515555594],
#  ["town_14_ruler_b", "Count Camechaw", "Count_Camechaw", tf_hero, scn_town_14_castle|entry(9), reserved,  fac_vaegirs, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008318101f390c515555594],

#  ["kingdom_2_lord_a", "Kingdom 2 Lord A", "Kingdom 2 Lord A", tf_hero, 0, reserved,  fac_kingdom_10, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_b", "Kingdom 2 Lord B", "Kingdom 2 Lord B", tf_hero, 0, reserved,  fac_kingdom_11, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_c", "Kingdom 2 Lord C", "Kingdom 2 Lord C", tf_hero, 0, reserved,  fac_kingdom_12, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_d", "Kingdom 2 Lord D", "Kingdom 2 Lord D", tf_hero, 0, reserved,  fac_kingdom_10, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_e", "Kingdom 2 Lord E", "Kingdom 2 Lord E", tf_hero, 0, reserved,  fac_kingdom_10, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_f", "Kingdom 2 Lord F", "Kingdom 2 Lord F", tf_hero, 0, reserved,  fac_kingdom_10, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_g", "Kingdom 2 Lord G", "Kingdom 2 Lord G", tf_hero, 0, reserved,  fac_kingdom_10, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_h", "Kingdom 2 Lord H", "Kingdom 2 Lord H", tf_hero, 0, reserved,  fac_kingdom_11, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_i", "Kingdom 2 Lord I", "Kingdom 2 Lord I", tf_hero, 0, reserved,  fac_kingdom_11, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_j", "Kingdom 2 Lord J", "Kingdom 2 Lord J", tf_hero, 0, reserved,  fac_kingdom_11, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_k", "Kingdom 2 Lord K", "Kingdom 2 Lord K", tf_hero, 0, reserved,  fac_kingdom_10, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_l", "Kingdom 2 Lord L", "Kingdom 2 Lord L", tf_hero, 0, reserved,  fac_kingdom_12, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_m", "Kingdom 2 Lord M", "Kingdom 2 Lord M", tf_hero, 0, reserved,  fac_kingdom_12, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],
#  ["kingdom_2_lord_n", "Kingdom 2 Lord N", "Kingdom 2 Lord N", tf_hero, 0, reserved,  fac_kingdom_12, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots, itm_coat_of_plates], lord_attrib|level(38), regular_melee(38), knows_common, 0x000000000008318101f390c515555594],


##################################################################################################################################
#ROYAL FAMILY MEMBERS
##################################################################################################################################
  ["knight_1_1_wife", "Lady Anna", "knight_1_1_wife",            tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_1, [itm_lady_dress_ruby ,   itm_turret_hat_ruby,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000055910200107632d675a92b92d00000000001e45620000000000000000],
  ["knight_2_1_wife", "Lady Junitha", "knight_2_1_wife",         tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_2, [itm_lady_dress_green,   itm_turret_hat_green,  itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x00000007c0101002588caf17142ab93d00000000001ddfa40000000000000000],
  ["knight_3_1_wife", "Lady Borge", "knight_3_1_wife",           tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_3, [itm_nomad_vest,                                itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000056e082002471c91c8aa2a130b00000000001d48a40000000000000000],
  ["knight_4_1_wife", "Lady Jadeth", "knight_4_1_wife",          tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_4, [itm_court_dress ,       itm_court_hat,         itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000054b100003274d65d2d239eb1300000000001d49080000000000000000],
  ["knight_5_1_wife", "Lady Brina", "knight_5_1_wife",           tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_5, [itm_lady_dress_green,   itm_turret_hat_green,  itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x00000007e900200416ed96e88b8d595a00000000001cb8ac0000000000000000],

  ["knight_1_2_wife", "Lady Nelda", "knight_1_1_wife",           tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_1, [itm_lady_dress_ruby ,   itm_turret_hat_ruby,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000054f08100232636aa90d6e194b00000000001e43130000000000000000],
  ["knight_2_2_wife", "Lady Katia", "knight_2_1_wife",           tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_2, [itm_lady_dress_green,   itm_turret_hat_green,  itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x00000008c00c20032aa5ae36b4259b9300000000001da6a50000000000000000],
  ["knight_3_2_wife", "Lady Tuan", "knight_3_1_wife",            tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_3, [itm_nomad_vest,                                itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x00000008ec0820062ce4d246b38e632e00000000001d52910000000000000000],
  ["knight_4_2_wife", "Lady Miar", "knight_4_1_wife",            tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_4, [itm_court_dress ,       itm_court_hat,         itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000058610000664d3693664f0c54b00000000001d332d0000000000000000],
  ["knight_5_2_wife", "Lady Aliena", "knight_5_1_wife",          tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_5, [itm_lady_dress_green,   itm_turret_hat_green,  itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000057008200222d432cf6d4a2ae300000000001d37a10000000000000000],

  ["knight_1_1_daughter", "Lady Bela", "knight_1_1_daughter",    tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_1, [itm_lady_dress_blue,    itm_turret_hat_blue,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000018f0410064854c742db74b52200000000001d448b0000000000000000],
  ["knight_2_1_daughter", "Lady Seomis", "knight_2_1_daughter",  tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_2, [itm_peasant_dress ,     itm_wimple_a,          itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x0000000007080004782a6cc4ecae4d1e00000000001eb6e30000000000000000],
  ["knight_3_1_daughter", "Lady Chedina", "knight_3_1_daughter", tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_3, [itm_nomad_robe ,                               itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x00000000320c30023ce23a145a8f27a300000000001ea6dc0000000000000000],
  ["knight_4_1_daughter", "Lady Dria", "knight_4_1_daughter",    tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_4, [itm_peasant_dress,                             itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x00000000000c000469a4d5cda4b1349c00000000001cd6600000000000000000],
  ["knight_5_1_daughter", "Lady Aneth", "knight_5_1_daughter",   tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_5, [itm_lady_dress_ruby ,   itm_turret_hat_ruby,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x00000001b9002002364dd8aa5475d76400000000001db8d30000000000000000],

  ["knight_1_2_daughter", "Lady Elina", "knight_1_1_daughter",   tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_1, [itm_lady_dress_blue,    itm_turret_hat_blue,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000204200629b131e90d6a8ae400000000001e28dd0000000000000000],
  ["knight_2_2_daughter", "Lady Drina", "knight_2_1_daughter",   tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_2, [itm_peasant_dress ,     itm_wimple_a,          itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000054008200638db99d89eccbd3500000000001ec91d0000000000000000],
  ["knight_3_2_daughter", "Lady Ayasu", "knight_3_1_daughter",   tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_3, [itm_nomad_robe ,                               itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000002a0c200348a28f2a54aa391c00000000001e46d10000000000000000],
  ["knight_4_2_daughter", "Lady Glunde", "knight_4_1_daughter",  tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_4, [itm_peasant_dress,                             itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x00000000000000021564d196e2aa279400000000001dc4ed0000000000000000],
  ["knight_5_2_daughter", "Lady Reada", "knight_5_1_daughter",   tf_hero|tf_female|tf_unmoveable_in_party_window, 0, reserved, fac_kingdom_5, [itm_lady_dress_ruby ,   itm_turret_hat_ruby,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000057a0000014123dae69e8e48e200000000001e08db0000000000000000],

#  ["kingdom_11_lord_daughter", "kingdom_11_lord_daughter", "kingdom_11_lord_daughter", tf_hero|tf_female, 0, reserved, fac_kingdom_10, [itm_lady_dress_blue ,   itm_turret_hat_blue,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000008300701c08d34a450ce43],
#  ["kingdom_13_lord_daughter", "kingdom_13_lord_daughter", "kingdom_13_lord_daughter", tf_hero|tf_female, 0, reserved, fac_kingdom_10, [itm_lady_dress_green,   itm_turret_hat_green,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000008000401db10a45b41d6d8],
#  ["kingdom_1_lady_a", "kingdom_1_lady_a", "kingdom_1_lady_a",                         tf_hero|tf_female, 0, reserved, fac_kingdom_1,  [itm_lady_dress_blue ,   itm_turret_hat_blue,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000008500201d8ad93708e4694],
#  ["kingdom_1_lady_b", "kingdom_1_lady_b", "kingdom_1_lady_b",                         tf_hero|tf_female, 0, reserved, fac_kingdom_1,  [itm_lady_dress_ruby ,   itm_turret_hat_ruby,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000004000101c3ae68e0e944ac],
#  ["kingdom_2_lady_a", "Kingdom 2 Lady a", "Kingdom 2 Lady a",                         tf_hero|tf_female, 0, reserved, fac_kingdom_2,  [itm_lady_dress_green,   itm_turret_hat_green,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000008100501d8ad93708e4694],
#  ["kingdom_2_lady_b", "Kingdom 2 Lady b", "Kingdom 2 Lady b",                         tf_hero|tf_female, 0, reserved, fac_kingdom_2,  [itm_lady_dress_blue ,   itm_turret_hat_blue,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000004000401d8ad93708e4694],
#  ["kingdom_3_lady_a", "Kingdom 3 Lady a", "Kingdom 3 Lady a",                         tf_hero|tf_female, 0, reserved, fac_kingdom_3,  [itm_lady_dress_ruby ,   itm_turret_hat_ruby,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000010500301d8ad93708e4694],
                        
#  ["kingdom_3_lady_b", "Kingdom 3 Lady b", "Kingdom 3 Lady b",                         tf_hero|tf_female, 0, reserved, fac_kingdom_3,  [itm_lady_dress_ruby ,   itm_turret_hat_ruby,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000000100601d8b08d76d14a24],
#  ["kingdom_4_lady_a", "Kingdom 4 Lady a", "Kingdom 4 Lady a",                         tf_hero|tf_female, 0, reserved, fac_kingdom_4,  [itm_lady_dress_green,   itm_turret_hat_green,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000010500601d8ad93708e4694],
#  ["kingdom_4_lady_b", "Kingdom 4 Lady b", "Kingdom 4 Lady b",                         tf_hero|tf_female, 0, reserved, fac_kingdom_4,  [itm_lady_dress_blue ,   itm_turret_hat_blue,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common|knows_riding_2, 0x000000000008500201d8ad93708e4694],

  ["heroes_end", "heroes end", "heroes end", tf_hero, 0, reserved,  fac_neutral, [itm_saddle_horse, itm_leather_jacket, itm_nomad_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008318101f390c515555594],

#Merchants
#  ["merchant_1", "merchant_1_F", "merchant_1_F",    tf_hero|tf_female, 0, 0, fac_kingdom_1, [itm_courser,            itm_fighting_axe,       itm_leather_jerkin,         itm_leather_boots,   itm_straw_hat],   def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000008200201e54c137a940c91],
#  ["merchant_2", "merchant_2", "merchant_2",        tf_hero,           0, 0, fac_kingdom_2, [itm_saddle_horse,       itm_arming_sword,       itm_light_leather,          itm_woolen_hose,                    ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000000000601db6db6db6db6db],
#  ["merchant_3", "merchant_3", "merchant_3",        tf_hero,           0, 0, fac_kingdom_3, [itm_courser,            itm_nordic_sword,       itm_leather_jerkin,         itm_woolen_hose,                    ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000008100701db6db6db6db6db],
#  ["merchant_4", "merchant_4_F", "merchant_4_F",    tf_hero|tf_female, 0, 0, fac_kingdom_4, [itm_saddle_horse,       itm_falchion,           itm_light_leather,          itm_blue_hose,                      ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000010500401e54c137a945c91],
#  ["merchant_5", "merchant_5", "merchant_5",        tf_hero,           0, 0, fac_kingdom_5, [itm_saddle_horse,       itm_sword,              itm_ragged_outfit,          itm_hide_boots,                     ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000008038001e54c135a945c91],
#  ["merchant_6", "merchant_6", "merchant_6",        tf_hero,           0, 0, fac_kingdom_1, [itm_saddle_horse,       itm_scimitar,           itm_leather_jerkin,         itm_leather_boots,                  ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000000248e01e54c1b5a945c91],
#  ["merchant_7", "merchant_7_F", "merchant_7_F",    tf_hero|tf_female, 0, 0, fac_kingdom_2, [itm_hunter,             itm_arming_sword,       itm_padded_leather,         itm_blue_hose,                      ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000004200601c98ad39c97557a],
#  ["merchant_8", "merchant_8", "merchant_8",        tf_hero,           0, 0, fac_kingdom_3, [itm_saddle_horse,       itm_nordic_sword,       itm_light_leather,          itm_leather_boots,   itm_woolen_hood], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x00000000001095ce01d6aad3a497557a],
#  ["merchant_9", "merchant_9", "merchant_9",        tf_hero,           0, 0, fac_kingdom_4, [itm_saddle_horse,       itm_sword,              itm_padded_leather,         itm_hide_boots,                     ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000010519601ec26ae99898697],
#  ["merchant_10", "merchant_10", "merchant_10",     tf_hero,           0, 0, fac_merchants, [itm_hunter,             itm_bastard_sword,      itm_light_leather,          itm_woolen_hose,                    ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x00000000000884c401f6837d3294e28a],
#  ["merchant_11", "merchant_11", "merchant_11",     tf_hero,           0, 0, fac_merchants, [itm_saddle_horse,       itm_sword,              itm_leather_jacket,         itm_woolen_hose,                    ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x00000000000c450501e289dd2c692694],
#  ["merchant_12", "merchant_12", "merchant_12",     tf_hero,           0, 0, fac_merchants, [itm_hunter,             itm_falchion,           itm_leather_jerkin,         itm_hide_boots,                     ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x00000000000c660a01e5af3cb2763401],
#  ["merchant_13", "merchant_13", "merchant_13",     tf_hero,           0, 0, fac_merchants, [itm_sumpter_horse,      itm_nordic_sword,       itm_padded_leather,         itm_leather_boots,                  ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x00000000001001d601ec912a89e4d534],
#  ["merchant_14", "merchant_14", "merchant_14",     tf_hero,           0, 0, fac_merchants, [itm_courser,            itm_bastard_sword,      itm_light_leather,          itm_hide_boots,                     ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000004335601ea2c04a8b6a394],
#  ["merchant_15", "merchant_15", "merchant_15",     tf_hero,           0, 0, fac_merchants, [itm_saddle_horse,       itm_sword,              itm_padded_leather,         itm_woolen_hose,     itm_fur_hat],     def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000008358e01dbf27b6436089d],
#  ["merchant_16", "merchant_16_F", "merchant_16_F", tf_hero|tf_female, 0, 0, fac_merchants, [itm_hunter,             itm_bastard_sword,      itm_light_leather,          itm_hide_boots,                     ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x00000000000c300101db0b9921494add],
#  ["merchant_17", "merchant_17", "merchant_17",     tf_hero,           0, 0, fac_merchants, [itm_saddle_horse,       itm_sword,              itm_leather_jacket,         itm_blue_hose,                      ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000008740f01e945c360976a0a],
#  ["merchant_18", "merchant_18", "merchant_18",     tf_hero,           0, 0, fac_merchants, [itm_saddle_horse,       itm_nordic_sword,       itm_padded_leather,         itm_leather_boots,                  ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000008020c01fc2db3b4c97685],
#  ["merchant_19", "merchant_19", "merchant_19",     tf_hero,           0, 0, fac_merchants, [itm_saddle_horse,       itm_falchion,           itm_leather_jerkin,         itm_woolen_hose,                    ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000008118301f02af91892725b],
#  ["merchant_20", "merchant_20_F", "merchant_20_F", tf_hero|tf_female, 0, 0, fac_merchants, [itm_courser,            itm_arming_sword,       itm_padded_leather,         itm_leather_boots,                  ], def_attrib|level(15), regular_melee(15), knows_inventory_management_10, 0x000000000010500401f6837d27688212],


##################################################################################################################################
#SOD COURT
##################################################################################################################################
  ["sod_chancellor", "Chancellor", "Chancellor",                   tf_hero|tf_is_merchant, 0, reserved, fac_neutral, [itm_courtly_outfit,  itm_blue_hose],                                            def_attrib|level(2), regular_melee(2), knows_common, 0x0000000e3f002593205b75b6d36d800700000000001db8f30000000000000000],
  ["sod_treasurer", "Treasurer", "Treasurer",                      tf_hero|tf_is_merchant, 0, reserved, fac_neutral, [itm_nobleman_outfit, itm_blue_hose],                                            def_attrib|level(2), regular_melee(2), knows_common, 0x0000000fbf0005ce205b75b6d36db6db00000000001db8f30000000000000000],
  ["sod_marshal", "Marshall", "Marshall",                          tf_hero|tf_is_merchant, 0, reserved, fac_neutral, [itm_court_outfit,    itm_blue_hose],                                            def_attrib|level(2), regular_melee(2), knows_common, 0x0000000e3f002550201a9ff7ab95ffff00000000001db93b0000000000000000],
  ["sod_jester", "Jester", "Jester",                               tf_hero|tf_is_merchant, 0, reserved, fac_neutral, [itm_jester_tunic,    itm_jester_hat_small, itm_jester_gloves, itm_jester_boot, itm_talak_mace], lord_attrib2|level(99), regular_all(99), knows_lord_2, 0x000000057701800f36db6db6db6db6db00000000001db6db0000000000000000],
  ["sod_strategy_advisor", "Cassian Varro", "Cassian Varro", tf_hero, 0, reserved, fac_neutral, [itm_dynasty_outfit,  itm_elephant_guard_gloves, itm_dynasty_oufit_greaves],     def_attrib|level(25), regular_all(25), knows_riding_4|knows_ironflesh_1|knows_power_strike_4|knows_power_draw_4|knows_horse_archery_5|knows_athletics_1|knows_tactics_2|knows_leadership_5, 0x0000000fc0019305269e6a36d26a152400000000001d366a0000000000000000],
   # Cassian Varro keeps the legacy troop id sod_strategy_advisor for script compatibility.


##################################################################################################################################
#SENESCHALS
##################################################################################################################################
  ["town_1_seneschal", "Town 1 Seneschal", "Town 1 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,       itm_leather_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c218501ef4f5d2ccb0026],
  ["town_2_seneschal", "Town 2 Seneschal", "Town 2 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,     itm_woolen_hose],      def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c03cc01cc34a9a467fdfd],
  ["town_3_seneschal", "Town 3 Seneschal", "Town 3 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,       itm_leather_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c500e01dbb2115a55f3cd],
  ["town_4_seneschal", "Town 4 Seneschal", "Town 4 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,      itm_blue_hose],        def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008035201e6eebaf3f3eb2b],
  ["town_5_seneschal", "Town 5 Seneschal", "Town 5 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jerkin,     itm_woolen_hose],      def_attrib|level(2), regular_melee(2), knows_common, 0x000000000000249101e7898999ac54c6],
  ["town_6_seneschal", "Town 6 Seneschal", "Town 6 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_red_gambeson,       itm_nomad_boots],      def_attrib|level(2), regular_melee(2), knows_common, 0x000000000010360b01cef8b57553d34e],
  ["town_7_seneschal", "Town 7 Seneschal", "Town 7 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jerkin,     itm_woolen_hose],      def_attrib|level(2), regular_melee(2), knows_common, 0x000000000000018101f9487aa831dce4],
  ["town_8_seneschal", "Town 8 Seneschal", "Town 8 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_red_gambeson,       itm_nomad_boots],      def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004715201ea236c60a2bcae],
  ["town_9_seneschal", "Town 9 Seneschal", "Town 9 Seneschal",          tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,       itm_leather_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000440c601e1cd45cfb38550],
  ["town_10_seneschal", "Town 10 Seneschal", "Town 10 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jerkin,     itm_blue_hose],        def_attrib|level(2), regular_melee(2), knows_common, 0x000000000010230c01ef41badb50465e],
  ["town_11_seneschal", "Town 11 Seneschal", "Town 11 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jacket,     itm_nomad_boots],      def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008061301fb89acfb95332f],
  ["town_12_seneschal", "Town 12 Seneschal", "Town 12 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,       itm_leather_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c13ce01dc4723ab936c82],
  ["town_13_seneschal", "Town 13 Seneschal", "Town 13 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jerkin,     itm_woolen_hose],      def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008548e01d952a9b25d6d5a],
  ["town_14_seneschal", "Town 14 Seneschal", "Town 14 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,      itm_blue_hose],        def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004728b01c293c694944b05],
  ["town_15_seneschal", "Town 15 Seneschal", "Town 14 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,      itm_blue_hose],        def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004728b01c293c694944b05],
  ["town_16_seneschal", "Town 16 Seneschal", "Town 14 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,      itm_blue_hose],        def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004728b01c293c694944b05],
  ["town_17_seneschal", "Town 17 Seneschal", "Town 14 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,      itm_blue_hose],        def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004728b01c293c694944b05],
  ["town_18_seneschal", "Town 18 Seneschal", "Town 14 Seneschal",       tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,      itm_blue_hose],        def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004728b01c293c694944b05],

  ["castle_1_seneschal", "Castle 1 Seneschal", "Castle 1 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,          itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x000000000010360b01cef8b57553d34e],
  ["castle_2_seneschal", "Castle 2 Seneschal", "Castle 2 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_nomad_armor,           itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008061301fb89acfb95332f],
  ["castle_3_seneschal", "Castle 3 Seneschal", "Castle 3 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008548e01d952a9b25d6d5a],
  ["castle_4_seneschal", "Castle 4 Seneschal", "Castle 4 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_linen_tunic,           itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004715201ea236c60a2bcae],
  ["castle_5_seneschal", "Castle 5 Seneschal", "Castle 5 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jerkin,        itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c500e01dbb2115a55f3cd],
  ["castle_6_seneschal", "Castle 6 Seneschal", "Castle 6 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,          itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c03cc01cc34a9a467fdfd],
  ["castle_7_seneschal", "Castle 7 Seneschal", "Castle 7 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,         itm_blue_hose],     def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c13ce01dc4723ab936c82],
  ["castle_8_seneschal", "Castle 8 Seneschal", "Castle 8 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c218501ef4f5d2ccb0026],
  ["castle_9_seneschal", "Castle 9 Seneschal", "Castle 9 Seneschal",    tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jacket,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008035201e6eebaf3f3eb2b],
  ["castle_10_seneschal", "Castle 10 Seneschal", "Castle 10 Seneschal", tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000440c601e1cd45cfb38550],
  ["castle_11_seneschal", "Castle 11 Seneschal", "Castle 11 Seneschal", tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000440c601e1cd45cfb38550],
  ["castle_12_seneschal", "Castle 2 Seneschal", "Castle 2 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_nomad_armor,           itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008061301fb89acfb95332f],
  ["castle_13_seneschal", "Castle 3 Seneschal", "Castle 3 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008548e01d952a9b25d6d5a],
  ["castle_14_seneschal", "Castle 4 Seneschal", "Castle 4 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_linen_tunic,           itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004715201ea236c60a2bcae],
  ["castle_15_seneschal", "Castle 5 Seneschal", "Castle 5 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jerkin,        itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c500e01dbb2115a55f3cd],
  ["castle_16_seneschal", "Castle 6 Seneschal", "Castle 6 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,          itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c03cc01cc34a9a467fdfd],
  ["castle_17_seneschal", "Castle 7 Seneschal", "Castle 7 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,         itm_blue_hose],     def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c13ce01dc4723ab936c82],
  ["castle_18_seneschal", "Castle 8 Seneschal", "Castle 8 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c218501ef4f5d2ccb0026],
  ["castle_19_seneschal", "Castle 9 Seneschal", "Castle 9 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jacket,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008035201e6eebaf3f3eb2b],
  ["castle_20_seneschal", "Castle 20 Seneschal", "Castle 20 Seneschal", tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000440c601e1cd45cfb38550],
  ["castle_21_seneschal", "Castle 11 Seneschal", "Castle 11 Seneschal", tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000440c601e1cd45cfb38550],
  ["castle_22_seneschal", "Castle 2 Seneschal", "Castle 2 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_nomad_armor,           itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008061301fb89acfb95332f],
  ["castle_23_seneschal", "Castle 3 Seneschal", "Castle 3 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008548e01d952a9b25d6d5a],
  ["castle_24_seneschal", "Castle 4 Seneschal", "Castle 4 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_linen_tunic,           itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004715201ea236c60a2bcae],
  ["castle_25_seneschal", "Castle 5 Seneschal", "Castle 5 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jerkin,        itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c500e01dbb2115a55f3cd],
  ["castle_26_seneschal", "Castle 6 Seneschal", "Castle 6 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,          itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c03cc01cc34a9a467fdfd],
  ["castle_27_seneschal", "Castle 7 Seneschal", "Castle 7 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,         itm_blue_hose],     def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c13ce01dc4723ab936c82],
  ["castle_28_seneschal", "Castle 8 Seneschal", "Castle 8 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c218501ef4f5d2ccb0026],
  ["castle_29_seneschal", "Castle 9 Seneschal", "Castle 9 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jacket,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008035201e6eebaf3f3eb2b],
  ["castle_30_seneschal", "Castle 20 Seneschal", "Castle 20 Seneschal", tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000440c601e1cd45cfb38550],
  ["castle_31_seneschal", "Castle 11 Seneschal", "Castle 11 Seneschal", tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000440c601e1cd45cfb38550],
  ["castle_32_seneschal", "Castle 2 Seneschal", "Castle 2 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_nomad_armor,           itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008061301fb89acfb95332f],
  ["castle_33_seneschal", "Castle 3 Seneschal", "Castle 3 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008548e01d952a9b25d6d5a],
  ["castle_34_seneschal", "Castle 4 Seneschal", "Castle 4 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_linen_tunic,           itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x000000000004715201ea236c60a2bcae],
  ["castle_35_seneschal", "Castle 5 Seneschal", "Castle 5 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jerkin,        itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c500e01dbb2115a55f3cd],
  ["castle_36_seneschal", "Castle 6 Seneschal", "Castle 6 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_coarse_tunic,          itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c03cc01cc34a9a467fdfd],
  ["castle_37_seneschal", "Castle 7 Seneschal", "Castle 7 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_blue_gambeson,         itm_blue_hose],     def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c13ce01dc4723ab936c82],
  ["castle_38_seneschal", "Castle 8 Seneschal", "Castle 8 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000c218501ef4f5d2ccb0026],
  ["castle_39_seneschal", "Castle 9 Seneschal", "Castle 9 Seneschal",   tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_leather_jacket,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, 0x000000000008035201e6eebaf3f3eb2b],
  ["castle_40_seneschal", "Castle 20 Seneschal", "Castle 20 Seneschal", tf_hero|tf_is_merchant, 0, reserved,  fac_neutral, [itm_padded_leather,        itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common, 0x00000000000440c601e1cd45cfb38550],


##################################################################################################################################
#ARENA MASTERS
##################################################################################################################################
  ["town_1_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_1_arena|entry(52), reserved,   fac_commoners, [itm_coarse_tunic,      itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_2_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_2_arena|entry(52), reserved,   fac_commoners, [itm_linen_tunic,       itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_3_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_3_arena|entry(52), reserved,   fac_commoners, [itm_nomad_armor,       itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_4_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_4_arena|entry(52), reserved,   fac_commoners, [itm_coarse_tunic,      itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_5_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_5_arena|entry(52), reserved,   fac_commoners, [itm_linen_tunic,       itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_6_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_6_arena|entry(52), reserved,   fac_commoners, [itm_leather_jerkin,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_7_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_7_arena|entry(52), reserved,   fac_commoners, [itm_padded_leather,    itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_8_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_8_arena|entry(52), reserved,   fac_commoners, [itm_linen_tunic,       itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_9_arena_master", "Tournament Master", "Tournament Master",  tf_hero|tf_randomize_face, scn_town_9_arena|entry(52), reserved,   fac_commoners, [itm_padded_leather,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_10_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_10_arena|entry(52), reserved,  fac_commoners, [itm_nomad_armor,       itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_11_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_11_arena|entry(52), reserved,  fac_commoners, [itm_coarse_tunic,      itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_12_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_12_arena|entry(52), reserved,  fac_commoners, [itm_leather_jerkin,    itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_13_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_13_arena|entry(52), reserved,  fac_commoners, [itm_coarse_tunic,      itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_14_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_14_arena|entry(52), reserved,  fac_commoners, [itm_padded_leather,    itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_15_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_15_arena|entry(52), reserved,  fac_commoners, [itm_padded_leather,    itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_16_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_16_arena|entry(52), reserved,  fac_commoners, [itm_fur_coat,          itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_17_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_17_arena|entry(52), reserved,  fac_commoners, [itm_padded_leather,    itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],
  ["town_18_arena_master", "Tournament Master", "Tournament Master", tf_hero|tf_randomize_face, scn_town_18_arena|entry(52), reserved,  fac_commoners, [itm_padded_leather,    itm_hide_boots],    def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, man_face_older_2],


##################################################################################################################################
# UNDERGROUND
##################################################################################################################################
#  ["town_1_crook", "Town 1 Crook", "Town 1 Crook", tf_hero,                0, 0, fac_neutral, [itm_linen_tunic,        itm_leather_boots  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, 0x000000000004428401f46e44a27144e3],
#  ["town_2_crook", "Town 2 Crook", "Town 2 Crook", tf_hero|tf_female,      0, 0, fac_neutral, [itm_lady_dress_ruby,    itm_turret_hat_ruby], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, 0x000000000004300101c36db6db6db6db],
#  ["town_3_crook", "Town 3 Crook", "Town 3 Crook", tf_hero,                0, 0, fac_neutral, [itm_leather_apron,      itm_hide_boots     ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, 0x00000000000c530701f17944a25164e1],
#  ["town_4_crook", "Town 4 Crook", "Town 4 Crook", tf_hero,                0, 0, fac_neutral, [itm_coarse_tunic,       itm_hide_boots     ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x00000000000c840501f36db6db7134db],
#  ["town_5_crook", "Town 5 Crook", "Town 5 Crook", tf_hero,                0, 0, fac_neutral, [itm_red_gambeson,       itm_blue_hose      ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x00000000000c000601f36db6db7134db],
#  ["town_6_crook", "Town 6 Crook", "Town 6 Crook", tf_hero,                0, 0, fac_neutral, [itm_coarse_tunic,       itm_hide_boots     ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x00000000000c10c801db6db6dd7598aa],
#  ["town_7_crook", "Town 7 Crook", "Town 7 Crook", tf_hero|tf_female,      0, 0, fac_neutral, [itm_woolen_dress,       itm_woolen_hood    ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x000000000010214101de2f64db6db58d],

#  ["town_8_crook", "Town 8 Crook", "Town 8 Crook", tf_hero,                0, 0, fac_neutral, [itm_leather_jacket,     itm_leather_boots  ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x000000000010318401c96db4db6db58d],
#  ["town_9_crook", "Town 9 Crook", "Town 9 Crook", tf_hero,                0, 0, fac_neutral, [itm_linen_tunic,        itm_hide_boots     ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x000000000008520501f16db4db6db58d],
#  ["town_10_crook", "Town 10 Crook", "Town 10 Crook", tf_hero,             0, 0, fac_neutral, [itm_coarse_tunic,      itm_nomad_boots     ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x000000000008600701f35144db6db8a2],
#  ["town_11_crook", "Town 11 Crook", "Town 11 Crook", tf_hero|tf_female,   0, 0, fac_neutral, [itm_blue_dress,        itm_wimple_a        ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x000000000008408101f386c4db4dd514],
#  ["town_12_crook", "Town 12 Crook", "Town 12 Crook", tf_hero,             0, 0, fac_neutral, [itm_coarse_tunic,      itm_hide_boots      ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x00000000000870c501f386c4f34dbaa1],
#  ["town_13_crook", "Town 13 Crook", "Town 13 Crook", tf_hero,             0, 0, fac_neutral, [itm_blue_gambeson,     itm_nomad_boots     ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x00000000000c114901f245caf34dbaa1],
#  ["town_14_crook", "Town 14 Crook", "Town 14 Crook", tf_hero|tf_female,   0, 0, fac_neutral, [itm_woolen_dress,      itm_turret_hat_ruby ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, 0x00000000001021c001f545a49b6eb2bc],


##################################################################################################################################
# ARMOR MERCHANTS
#arena_masters_end = zendar_armorer
##################################################################################################################################
  ["town_1_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_linen_tunic,     itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_2_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|tf_female|tf_is_merchant, 0, 0, fac_commoners, [itm_woolen_dress,    itm_straw_hat    ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_3_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_arena_tunic_red, itm_hide_boots   ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_4_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_red_gambeson,    itm_leather_boots], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_5_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_linen_tunic,     itm_nomad_boots  ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_6_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,        itm_nomad_boots  ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_7_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_leather_jerkin,  itm_blue_hose    ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_8_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_padded_leather,  itm_leather_boots], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_9_armorer", "Armorer",  "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_blue_gambeson,   itm_nomad_boots  ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_10_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_leather_jerkin,  itm_hide_boots   ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_11_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,        itm_leather_boots], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_12_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_red_gambeson,    itm_nomad_boots  ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_13_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_leather_jacket,  itm_hide_boots   ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_14_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|tf_female|tf_is_merchant, 0, 0, fac_commoners, [itm_woolen_dress,    itm_headcloth    ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_15_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_blue_gambeson,   itm_leather_boots], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_16_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,        itm_nomad_boots  ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_17_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,        itm_hide_boots   ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_18_armorer", "Armorer", "Armorer",  tf_hero|tf_randomize_face|tf_female|tf_is_merchant, 0, 0, fac_commoners, [itm_woolen_dress,    itm_headcloth    ], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, woman_face_1, woman_face_2],


##################################################################################################################################
#WEAPON MERCHANTS
##################################################################################################################################
  ["town_1_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|tf_female|tf_is_merchant, 0, 0, fac_commoners, [itm_linen_tunic,       itm_hide_boots, itm_straw_hat],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_2_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_shirt,             itm_nomad_boots],                   def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_3_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,          itm_hide_boots],                    def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_4_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_shirt,             itm_hide_boots],                    def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_5_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_leather_jerkin,    itm_wrapping_boots],                def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_6_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_linen_tunic,       itm_hide_boots],                    def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_7_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_shirt,             itm_hide_boots],                    def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_8_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|tf_female|tf_is_merchant, 0, 0, fac_commoners, [itm_woolen_dress,      itm_wrapping_boots, itm_straw_hat], def_attrib|level(5), regular_melee(5), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_9_weaponsmith", "Weaponsmith", "Weaponsmith",  tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_leather_jerkin,    itm_leather_boots],                 def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_10_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_linen_tunic,       itm_hide_boots],                    def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_11_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_leather_jacket,    itm_woolen_hose],                   def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_12_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_shirt,             itm_hide_boots],                    def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_13_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_arena_tunic_red,   itm_wrapping_boots],                def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_14_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_arena_tunic_blue,  itm_wrapping_boots],                def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_15_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_leather_jacket,    itm_woolen_hose],                   def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_16_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_shirt,             itm_hide_boots],                    def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_17_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_arena_tunic_green, itm_wrapping_boots],                def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],
  ["town_18_weaponsmith", "Weaponsmith", "Weaponsmith", tf_hero|tf_randomize_face|          tf_is_merchant, 0, 0, fac_commoners, [itm_linen_tunic,       itm_wrapping_boots],                def_attrib|level(5), regular_melee(5), knows_inventory_management_10, mercenary_face_1, mercenary_face_2],


##################################################################################################################################
#TAVERN KEEPERS
##################################################################################################################################
  ["town_1_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face,           scn_town_1_tavern|entry(9), 0,   fac_commoners, [itm_leather_apron,    itm_wrapping_boots],                def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["town_2_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face,           scn_town_2_tavern|entry(9), 0,   fac_commoners, [itm_leather_apron,    itm_leather_boots],                 def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["town_3_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face|tf_female, scn_town_3_tavern|entry(9), 0,   fac_commoners, [itm_woolen_dress,     itm_hide_boots],                    def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],
  ["town_4_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face,           scn_town_4_tavern|entry(9), 0,   fac_commoners, [itm_leather_apron,    itm_leather_boots],                 def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["town_5_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face,           scn_town_5_tavern|entry(9), 0,   fac_commoners, [itm_leather_apron,    itm_hide_boots],                    def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["town_6_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face|tf_female, scn_town_6_tavern|entry(9), 0,   fac_commoners, [itm_woolen_dress,     itm_hide_boots],                    def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],
  ["town_7_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face|tf_female, scn_town_7_tavern|entry(9), 0,   fac_commoners, [itm_woolen_dress,     itm_leather_boots,  itm_headcloth], def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],

  ["town_8_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face,           scn_town_8_tavern|entry(9), 0,   fac_commoners, [itm_leather_apron,    itm_leather_boots],                 def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["town_9_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper",  tf_hero|tf_randomize_face|tf_female, scn_town_9_tavern|entry(9), 0,   fac_commoners, [itm_woolen_dress,     itm_nomad_boots],                   def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],
  ["town_10_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face|tf_female, scn_town_10_tavern|entry(9), 0,  fac_commoners, [itm_woolen_dress,     itm_hide_boots],                    def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],
  ["town_11_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face|tf_female, scn_town_11_tavern|entry(9), 0,  fac_commoners, [itm_woolen_dress,     itm_nomad_boots],                   def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],
  ["town_12_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face,           scn_town_12_tavern|entry(9), 0,  fac_commoners, [itm_leather_apron,    itm_hide_boots],                    def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["town_13_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face|tf_female, scn_town_13_tavern|entry(9), 0,  fac_commoners, [itm_woolen_dress,     itm_hide_boots,     itm_headcloth], def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],
  ["town_14_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face,           scn_town_14_tavern|entry(9), 0,  fac_commoners, [itm_shirt,            itm_leather_boots],                 def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["town_15_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face|tf_female, scn_town_15_tavern|entry(9), 0,  fac_commoners, [itm_woolen_dress,     itm_nomad_boots],                   def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],
  ["town_16_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face,           scn_town_16_tavern|entry(9), 0,  fac_commoners, [itm_leather_apron,    itm_hide_boots],                    def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],
  ["town_17_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face|tf_female, scn_town_17_tavern|entry(9), 0,  fac_commoners, [itm_woolen_dress,     itm_hide_boots,     itm_headcloth], def_attrib|level(2), regular_melee(2), knows_common, woman_face_1, woman_face_2],
  ["town_18_tavernkeeper", "Tavern_Keeper", "Tavern_Keeper", tf_hero|tf_randomize_face,           scn_town_18_tavern|entry(9), 0,  fac_commoners, [itm_shirt,            itm_leather_boots],                 def_attrib|level(2), regular_melee(2), knows_common, mercenary_face_1, mercenary_face_2],


##################################################################################################################################
#GOODS MERCHANTS
##################################################################################################################################
  ["town_1_merchant", "Merchant", "Merchant",  tf_hero|tf_randomize_face|tf_is_merchant, scn_town_1_store|entry(9), 0, fac_commoners,            [itm_coarse_tunic,   itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_2_merchant", "Merchant", "Merchant",  tf_hero|tf_randomize_face|tf_is_merchant, scn_town_2_store|entry(9), 0, fac_commoners,            [itm_leather_apron,  itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_3_merchant", "Merchant", "Merchant",  tf_female|tf_hero|tf_randomize_face|tf_is_merchant, scn_town_3_store|entry(9), 0, fac_commoners,  [itm_dress,          itm_leather_boots,  itm_straw_hat  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_4_merchant", "Merchant", "Merchant",  tf_hero|tf_randomize_face|tf_is_merchant, scn_town_4_store|entry(9), 0, fac_commoners,            [itm_leather_apron,  itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_5_merchant", "Merchant", "Merchant",  tf_hero|tf_randomize_face|tf_is_merchant, scn_town_5_store|entry(9), 0, fac_commoners,            [itm_nomad_armor,    itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_6_merchant", "Merchant", "Merchant",  tf_female|tf_hero|tf_randomize_face|tf_is_merchant, scn_town_6_store|entry(9), 0, fac_commoners,  [itm_woolen_dress,   itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_7_merchant", "Merchant", "Merchant",  tf_hero|tf_randomize_face|tf_is_merchant, scn_town_7_store|entry(9), 0, fac_commoners,            [itm_leather_jerkin, itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],

  ["town_8_merchant", "Merchant", "Merchant",  tf_hero|tf_randomize_face|tf_is_merchant, scn_town_8_store|entry(9), 0, fac_commoners,            [itm_leather_apron,  itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_9_merchant", "Merchant", "Merchant",  tf_hero|tf_randomize_face|tf_is_merchant, scn_town_9_store|entry(9), 0, fac_commoners,            [itm_leather_apron,  itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_10_merchant", "Merchant", "Merchant", tf_hero|tf_randomize_face|tf_is_merchant, scn_town_10_store|entry(9), 0, fac_commoners,           [itm_leather_jerkin, itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_11_merchant", "Merchant", "Merchant", tf_hero|tf_randomize_face|tf_is_merchant, scn_town_11_store|entry(9), 0, fac_commoners,           [itm_leather_apron,  itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_12_merchant", "Merchant", "Merchant", tf_female|tf_hero|tf_randomize_face|tf_is_merchant, scn_town_12_store|entry(9), 0, fac_commoners, [itm_woolen_dress,   itm_leather_boots,  itm_female_hood], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_13_merchant", "Merchant", "Merchant", tf_female|tf_hero|tf_randomize_face|tf_is_merchant, scn_town_13_store|entry(9), 0, fac_commoners, [itm_dress,          itm_leather_boots,  itm_straw_hat  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_14_merchant", "Merchant", "Merchant", tf_hero|tf_randomize_face|tf_is_merchant, scn_town_14_store|entry(9), 0, fac_commoners,           [itm_leather_apron,  itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_15_merchant", "Merchant", "Merchant", tf_hero|tf_randomize_face|tf_is_merchant, scn_town_15_store|entry(9), 0, fac_commoners,           [itm_leather_apron,  itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_16_merchant", "Merchant", "Merchant", tf_female|tf_hero|tf_randomize_face|tf_is_merchant, scn_town_16_store|entry(9), 0, fac_commoners, [itm_woolen_dress,   itm_leather_boots,  itm_female_hood], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_17_merchant", "Merchant", "Merchant", tf_female|tf_hero|tf_randomize_face|tf_is_merchant, scn_town_17_store|entry(9), 0, fac_commoners, [itm_dress,          itm_leather_boots,  itm_straw_hat  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_18_merchant", "Merchant", "Merchant", tf_hero|tf_randomize_face|tf_is_merchant, scn_town_18_store|entry(9), 0, fac_commoners,           [itm_leather_apron,  itm_leather_boots                  ], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_young_1, man_face_older_2],

  ["salt_mine_merchant", "Barezan", "Barezan", tf_hero|tf_is_merchant, scn_salt_mine|entry(1), 0, fac_commoners,                                 [itm_leather_apron, itm_leather_boots],                    def_attrib|level(2), regular_melee(2), knows_inventory_management_10, 0x00000000000c528601ea69b6e46dbdb6],


##################################################################################################################################
#HORSE MERCHANTS
##################################################################################################################################
  ["town_1_horse_merchant", "Horse Merchant", "Town 1 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant|tf_female,  0, 0, fac_commoners, [itm_blue_dress,          itm_blue_hose,      itm_female_hood],   def_attrib|level(2), regular_melee(2), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_2_horse_merchant", "Horse Merchant", "Town 2 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_linen_tunic,         itm_nomad_boots],                       def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_3_horse_merchant", "Horse Merchant", "Town 3 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_nomad_armor,         itm_hide_boots],                        def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_4_horse_merchant", "Horse Merchant", "Town 4 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_leather_jerkin,      itm_nomad_boots],                       def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_5_horse_merchant", "Horse Merchant", "Town 5 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant|tf_female,  0, 0, fac_commoners, [itm_dress,               itm_woolen_hose,    itm_woolen_hood],   def_attrib|level(5), regular_melee(5), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_6_horse_merchant", "Horse Merchant", "Town 6 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_coarse_tunic,        itm_hide_boots],                        def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_7_horse_merchant", "Horse Merchant", "Town 7 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_coarse_tunic,        itm_leather_boots],                     def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_8_horse_merchant", "Horse Merchant", "Town 8 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_coarse_tunic,        itm_hide_boots],                        def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_9_horse_merchant", "Horse Merchant", "Town 9 Horse Merchant",   tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_leather_jerkin,      itm_woolen_hose],                       def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_10_horse_merchant", "Horse Merchant", "Town 10 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant|tf_female,  0, 0, fac_commoners, [itm_blue_dress,          itm_blue_hose,      itm_straw_hat],     def_attrib|level(5), regular_melee(5), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_11_horse_merchant", "Horse Merchant", "Town 11 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_nomad_armor,         itm_leather_boots],                     def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_12_horse_merchant", "Horse Merchant", "Town 12 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_leather_jacket,      itm_hide_boots],                        def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_13_horse_merchant", "Horse Merchant", "Town 13 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_coarse_tunic,        itm_nomad_boots],                       def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_14_horse_merchant", "Horse Merchant", "Town 14 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant|tf_female,  0, 0, fac_commoners, [itm_peasant_dress,       itm_blue_hose,      itm_headcloth],     def_attrib|level(5), regular_melee(5), knows_inventory_management_10, woman_face_1, woman_face_2],
  ["town_15_horse_merchant", "Horse Merchant", "Town 15 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_nomad_armor,         itm_leather_boots],                     def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_16_horse_merchant", "Horse Merchant", "Town 16 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_leather_jacket,      itm_hide_boots],                        def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_17_horse_merchant", "Horse Merchant", "Town 17 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant,            0, 0, fac_commoners, [itm_coarse_tunic,        itm_nomad_boots],                       def_attrib|level(5), regular_melee(5), knows_inventory_management_10, man_face_young_1, man_face_older_2],
  ["town_18_horse_merchant", "Horse Merchant", "Town 18 Horse Merchant", tf_hero|tf_randomize_face|tf_is_merchant|tf_female,  0, 0, fac_commoners, [itm_peasant_dress,       itm_blue_hose,      itm_headcloth],     def_attrib|level(5), regular_melee(5), knows_inventory_management_10, woman_face_1, woman_face_2],


##################################################################################################################################
#TOWN MAYORS
##################################################################################################################################
  ["town_1_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_courtly_outfit,  itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common, man_face_middle_1, mercenary_face_2],
  ["town_2_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_gambeson,        itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_3_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_blue_gambeson,   itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_4_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_fur_coat,        itm_blue_hose],     def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_5_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_nobleman_outfit, itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_6_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_red_gambeson,    itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_7_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_rich_outfit,     itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_8_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_red_gambeson,    itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_9_mayor", "Guild_Master", "Guild_Master",  tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_courtly_outfit,  itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_10_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_leather_jerkin,  itm_blue_hose],     def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_11_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_leather_jacket,  itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_12_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_red_gambeson,    itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_13_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_nobleman_outfit, itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_14_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_blue_gambeson,   itm_blue_hose],     def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_15_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_leather_jacket,  itm_nomad_boots],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_16_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_fur_coat,        itm_leather_boots], def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_17_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_nobleman_outfit, itm_woolen_hose],   def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],
  ["town_18_mayor", "Guild_Master", "Guild_Master", tf_hero|tf_randomize_face, 0, reserved,  fac_neutral, [itm_blue_gambeson,   itm_blue_hose],     def_attrib|level(2), regular_melee(2), knows_common,  man_face_middle_1, mercenary_face_2],


##################################################################################################################################
#VILLIAGE STORES
##################################################################################################################################
  ["village_1_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots,      itm_felt_hat],       def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_2_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_3_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_4_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots,      itm_leather_cap],   def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_5_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_6_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_7_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_8_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_wrapping_boots, itm_felt_hat],        def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_9_elder", "Village_Elder", "village_1_elder",  tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_leather_cap],         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_10_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_11_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_12_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_13_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_14_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_15_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_felt_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_16_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_leather_warrior_cap], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_17_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_18_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_leather_warrior_cap], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_19_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_20_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_leather_warrior_cap], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_21_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_22_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_23_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_felt_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_24_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_25_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_26_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_27_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_wrapping_boots, itm_felt_hat],        def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_28_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_29_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_30_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_31_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_32_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_33_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_34_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_35_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_36_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_37_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_38_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_39_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_40_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_41_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_42_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_43_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_44_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_45_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_46_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_47_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_48_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_49_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_50_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_51_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_52_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_53_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_felt_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_54_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_55_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_56_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_57_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_wrapping_boots, itm_felt_hat],        def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_58_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_59_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_60_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_61_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_62_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_63_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_felt_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_64_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_65_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_66_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_67_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_wrapping_boots, itm_felt_hat],        def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_68_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_69_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_70_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_71_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_72_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_73_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots, itm_felt_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_74_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_75_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_76_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_77_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_wrapping_boots, itm_felt_hat],        def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_78_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_79_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_80_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_81_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_82_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_83_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_wrapping_boots, itm_leather_cap],     def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_84_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots, itm_fur_hat],            def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_85_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_86_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_87_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_88_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_fur_coat,     itm_hide_boots],                          def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_89_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_coarse_tunic, itm_nomad_boots],                         def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
  ["village_90_elder", "Village_Elder", "village_1_elder", tf_hero|tf_randomize_face|tf_is_merchant, 0, 0, fac_commoners, [itm_robe,         itm_wrapping_boots],                      def_attrib|level(2), regular_melee(2), knows_inventory_management_10, man_face_old_1, man_face_older_2],
# Place extra merchants before this point
  ["rtc_garran_ashwake", "Sir Garran Ashwake", "Sir Garran Ashwake", tf_hero|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_commoners, [itm_tabard, itm_hide_boots, itm_leather_gloves, itm_sword_medieval_b, itm_tab_shield_round_a], def_attrib|str_13|agi_11|int_10|cha_12|level(18), regular_melee(18), knows_ironflesh_2|knows_power_strike_3|knows_shield_2|knows_tactics_2|knows_leadership_3, 0x0000000d810021c736db6db6db6db6db00000000001db6db0000000000000000],
  ["rtc_lysara_veyne", "Lysara Veyne", "Lysara Veyne", tf_hero|tf_female|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_blue_dress, itm_hide_boots], def_attrib|str_7|agi_10|int_15|cha_13|level(15), regular_melee(6), knows_trade_3|knows_inventory_management_4|knows_spotting_2|knows_pathfinding_1, 0x00000001801402861236db6db6db6db600000000001db6db0000000000000000],
  ["rtc_imperial_courier", "Imperial Courier", "Imperial Couriers", tf_hero|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse, no_scene, reserved, fac_kingdom_6, [itm_leather_jerkin, itm_hide_boots, itm_saddle_horse, itm_sword_medieval_a], def_attrib|str_10|agi_12|int_9|cha_8|level(14), regular_melee(14), knows_riding_3|knows_pathfinding_2|knows_spotting_1|knows_athletics_1, 0x0000000a810021c436db6db6db6db6db00000000001db6db0000000000000000],
  ["rtc_tamsin_reedhand", "Tamsin Reedhand", "Tamsin Reedhand", tf_hero|tf_female|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_woolen_dress, itm_wrapping_boots], def_attrib|str_8|agi_8|int_11|cha_12|level(12), regular_melee(8), knows_trade_2|knows_inventory_management_3|knows_leadership_2, 0x000000018004018312b6db6d96b6d6db00000000001db6db0000000000000000],
  ["rtc_celeste_di_marina", "Celeste di Marina", "Celeste di Marina", tf_hero|tf_female|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_courtly_outfit, itm_hide_boots], def_attrib|str_7|agi_9|int_14|cha_15|level(16), regular_melee(7), knows_trade_5|knows_inventory_management_4|knows_leadership_1, 0x0000000180101247133a6d76db6db6db00000000001db6db0000000000000000],
  ["rtc_brother_odran", "Brother Odran", "Brother Odran", tf_hero|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_robe, itm_wrapping_boots, itm_pilgrim_hood], def_attrib|str_8|agi_7|int_15|cha_13|level(14), regular_melee(6), knows_first_aid_4|knows_surgery_2|knows_wound_treatment_4|knows_leadership_3, 0x0000000c700411c41236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_wulfred_carr", "Wulfred Carr", "Wulfred Carr", tf_hero|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet, no_scene, reserved, fac_outlaws, [itm_mail_hauberk, itm_mail_boots, itm_mail_mittens, itm_flat_topped_helmet, itm_sword_two_handed_b, itm_military_pick], def_attrib|str_18|agi_11|int_10|cha_13|level(26), expert_melee(26), knows_ironflesh_5|knows_power_strike_5|knows_athletics_3|knows_tactics_3|knows_leadership_4, 0x0000000d4b00110459245b6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_rafe_carrick", "Rafe Carrick", "Rafe Carrick", tf_hero|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_horse, no_scene, reserved, fac_outlaws, [itm_leather_armor, itm_hide_boots, itm_saddle_horse, itm_lance, itm_sword_medieval_b], def_attrib|str_12|agi_12|int_9|cha_10|level(17), regular_all(17), knows_riding_3|knows_power_strike_2|knows_athletics_2|knows_pathfinding_1, 0x0000000c4700310449245b6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_mother_hilda", "Mother Hilda", "Mother Hilda", tf_hero|tf_female|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_robe, itm_wrapping_boots, itm_staff], def_attrib|str_8|agi_7|int_15|cha_15|level(16), regular_melee(6), knows_first_aid_4|knows_surgery_2|knows_wound_treatment_4|knows_leadership_3, 0x00000001801021041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_reeve_martin", "Reeve Martin", "Reeve Martin", tf_hero|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_tabard, itm_hide_boots, itm_dagger], def_attrib|str_9|agi_8|int_13|cha_12|level(13), regular_melee(7), knows_trade_2|knows_inventory_management_3|knows_engineer_1|knows_leadership_2, 0x0000000c410421041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_piers_wainwright", "Piers Wainwright", "Piers Wainwright", tf_hero|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_leather_apron, itm_hide_boots, itm_hatchet, itm_tools], def_attrib|str_12|agi_9|int_10|cha_8|level(12), regular_melee(10), knows_engineer_2|knows_athletics_1|knows_power_strike_1|knows_inventory_management_1, 0x0000000c310421041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_nell_harrow", "Nell Harrow", "Nell Harrow", tf_hero|tf_female|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_peasant_dress, itm_wrapping_boots, itm_knife], def_attrib|str_7|agi_12|int_12|cha_11|level(12), regular_melee(7), knows_spotting_2|knows_tracking_1|knows_pathfinding_1|knows_trade_1, 0x00000001800011041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_garric_ashbow", "Garric Ashbow", "Garric Ashbow", tf_hero|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, no_scene, reserved, fac_commoners, [itm_leather_jerkin, itm_hide_boots, itm_long_bow, itm_arrows, itm_sword_two_handed_a, itm_dagger], def_attrib|str_12|agi_15|int_10|cha_9|level(19), wp_archery(180)|regular_melee(14), knows_power_draw_5|knows_athletics_4|knows_tracking_2|knows_spotting_2|knows_weapon_master_2, 0x0000000c200021041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_oswin_ditchwright", "Oswin Ditchwright", "Oswin Ditchwright", tf_hero|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_shield, no_scene, reserved, fac_commoners, [itm_leather_apron, itm_hide_boots, itm_tab_shield_round_b, itm_hatchet, itm_tools, itm_sword_two_handed_a], def_attrib|str_14|agi_9|int_13|cha_8|level(18), regular_melee(15), knows_engineer_4|knows_shield_3|knows_ironflesh_2|knows_power_strike_2|knows_athletics_1, 0x0000000c430021041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_sir_aldrik_vane", "Sir Aldrik Vane", "Sir Aldrik Vane", tf_hero|tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield, no_scene, reserved, fac_commoners, [itm_mail_with_surcoat, itm_mail_boots, itm_mail_mittens, itm_flat_topped_helmet, itm_hunter, itm_lance, itm_tab_shield_heater_c, itm_sword_two_handed_b], def_attrib|str_16|agi_12|int_10|cha_13|level(24), expert_melee(22), knows_riding_4|knows_ironflesh_4|knows_power_strike_4|knows_shield_4|knows_leadership_3|knows_trainer_2, 0x0000000d310421041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_mirelle_voss", "Mirelle Voss", "Mirelle Voss", tf_hero|tf_female|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_leather_armor, itm_hide_boots, itm_knife, itm_dagger, itm_sword_medieval_a, itm_sword_two_handed_a], def_attrib|str_10|agi_16|int_12|cha_10|level(19), regular_all(18), knows_athletics_5|knows_weapon_master_3|knows_power_strike_3|knows_spotting_2|knows_pathfinding_2, 0x00000001800811041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_tomas_reed", "Tomas Reed", "Tomas Reed", tf_hero|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_commoners, [itm_padded_leather, itm_hide_boots, itm_kettle_hat, itm_spear, itm_tab_shield_round_c, itm_sword_two_handed_a], def_attrib|str_13|agi_11|int_9|cha_9|level(16), regular_melee(16), knows_ironflesh_2|knows_power_strike_2|knows_shield_3|knows_athletics_2|knows_trainer_1, 0x0000000c250421041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_beren_hardhand", "Beren Hardhand", "Beren Hardhand", tf_hero|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet, no_scene, reserved, fac_commoners, [itm_studded_leather_coat, itm_leather_boots, itm_leather_gloves, itm_nasal_helmet, itm_battle_axe, itm_sword_two_handed_b], def_attrib|str_17|agi_10|int_8|cha_8|level(21), expert_melee(21), knows_ironflesh_4|knows_power_strike_5|knows_athletics_3|knows_weapon_master_2, 0x0000000d670021041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_sister_elianor", "Sister Elianor", "Sister Elianor", tf_hero|tf_female|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners, [itm_robe, itm_wrapping_boots, itm_staff, itm_sword_two_handed_a], def_attrib|str_9|agi_9|int_16|cha_14|level(17), regular_melee(8), knows_first_aid_5|knows_surgery_3|knows_wound_treatment_5|knows_trainer_2|knows_leadership_2, 0x00000001801412041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_halvorn_pike", "Halvorn Pike", "Halvorn Pike", tf_hero|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_shield, no_scene, reserved, fac_outlaws, [itm_mail_shirt, itm_hide_boots, itm_kettle_hat, itm_pike, itm_tab_shield_round_d, itm_sword_medieval_b], def_attrib|str_15|agi_10|int_9|cha_9|level(20), regular_melee(20), knows_ironflesh_3|knows_power_strike_3|knows_shield_3|knows_tactics_1, 0x0000000c6b0021041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_maud_ledger", "Maud Ledger", "Maud Ledger", tf_hero|tf_female|tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_outlaws, [itm_court_dress, itm_hide_boots, itm_dagger, itm_light_crossbow, itm_bolts], def_attrib|str_8|agi_10|int_15|cha_12|level(18), regular_crossbow(14)|regular_melee(8), knows_trade_4|knows_inventory_management_4|knows_tactics_2|knows_spotting_2, 0x00000001801802041236db6db6db6db600000000001db6db0000000000000000],
  ["seven_ash_sibert_crow_eye", "Sibert Crow-Eye", "Sibert Crow-Eye", tf_hero|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_ranged, no_scene, reserved, fac_outlaws, [itm_leather_jerkin, itm_hide_boots, itm_short_bow, itm_arrows, itm_sword_medieval_a], def_attrib|str_11|agi_14|int_10|cha_8|level(18), wp_archery(150)|regular_melee(12), knows_power_draw_4|knows_athletics_3|knows_tracking_2|knows_spotting_3, 0x0000000c2f0021041236db6db6db6db600000000001db6db0000000000000000],
  ["merchants_end", "merchants_end", "merchants_end",      tf_hero, 0, 0, fac_commoners, [], def_attrib|level(2), regular_melee(2), knows_inventory_management_10, 0],


##################################################################################################################################
#CHESTS
##################################################################################################################################
  ["zendar_chest", "Zendar Chest", "Zendar Chest", tf_hero|tf_inactive, 0, reserved,  fac_neutral,                     [],                                                                                                                      def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["tutorial_chest_1", "Melee Weapons Chest", "Melee Weapons Chest", tf_hero|tf_inactive, 0, reserved,  fac_neutral,   [itm_tutorial_sword, itm_tutorial_axe, itm_tutorial_spear, itm_tutorial_club, itm_tutorial_battle_axe],                  def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["tutorial_chest_2", "Ranged Weapons Chest", "Ranged Weapons Chest", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [itm_tutorial_short_bow, itm_tutorial_arrows, itm_tutorial_crossbow, itm_tutorial_bolts, itm_tutorial_throwing_daggers], def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["bonus_chest_1", "Bonus Chest", "Bonus Chest", tf_hero|tf_inactive, 0, reserved,  fac_neutral,                      [itm_strange_armor, itm_strange_short_sword],                                                                            def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["bonus_chest_2", "Bonus Chest", "Bonus Chest", tf_hero|tf_inactive, 0, reserved,  fac_neutral,                      [itm_strange_boots, itm_strange_sword],                                                                                  def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["bonus_chest_3", "Bonus Chest", "Bonus Chest", tf_hero|tf_inactive, 0, reserved,  fac_neutral,                      [itm_strange_helmet, itm_strange_great_sword],                                                                           def_attrib|level(18), regular_melee(18), knows_common, 0],

# These are used as arrays in the scripts.
  ["temp_array_a", "temp_array_a", "temp_array_a", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["temp_array_b", "temp_array_b", "temp_array_b", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["temp_array_c", "temp_array_c", "temp_array_c", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],

  ["stack_selection_amounts", "stack_selection_amounts", "stack_selection_amounts", tf_hero|tf_inactive, 0, reserved, fac_neutral, [], def_attrib, 0, knows_common, 0],
  ["stack_selection_ids", "stack_selection_ids", "stack_selection_ids", tf_hero|tf_inactive, 0, reserved, fac_neutral, [], def_attrib, 0, knows_common, 0],

  ["notification_menu_types", "notification_menu_types", "notification_menu_types", tf_hero|tf_inactive, 0, reserved, fac_neutral, [], def_attrib, 0, knows_common, 0],
  ["notification_menu_var1", "notification_menu_var1", "notification_menu_var1", tf_hero|tf_inactive, 0, reserved, fac_neutral, [], def_attrib, 0, knows_common, 0],
  ["notification_menu_var2", "notification_menu_var2", "notification_menu_var2", tf_hero|tf_inactive, 0, reserved, fac_neutral, [], def_attrib, 0, knows_common, 0],

  ["banner_background_color_array", "banner_background_color_array", "banner_background_color_array", tf_hero|tf_inactive, 0, reserved, fac_neutral, [], def_attrib, 0, knows_common, 0],


# Add Extra Quest NPCs below this point

  ["local_merchant", "Local Merchant", "Local Merchants", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["tax_rebel", "Peasant Rebel", "Peasant Rebels", tf_guarantee_armor, 0, reserved, fac_commoners,
   [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones, itm_leather_cap, itm_felt_hat, itm_felt_hat, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
   def_attrib|level(4), regular_melee(4), knows_common, vaegir_face1, vaegir_face2],
  ["trainee_peasant", "Peasant", "Peasants", tf_guarantee_armor, 0, reserved, fac_commoners,
   [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones, itm_leather_cap, itm_felt_hat, itm_felt_hat, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
   def_attrib|level(4), regular_melee(4), knows_common, vaegir_face1, vaegir_face2],
  ["fugitive", "Nervous Man", "Nervous Men", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners,
   [itm_short_tunic, itm_linen_tunic, itm_coarse_tunic, itm_tabard, itm_leather_vest, itm_woolen_hose, itm_nomad_boots, itm_blue_hose, itm_wrapping_boots, itm_fur_hat, itm_leather_cap, itm_sword_medieval_b, itm_throwing_daggers],
   def_attrib|str_24|agi_25|level(26), regular_melee(26), knows_common|knows_power_throw_6|knows_power_strike_6|knows_ironflesh_9, man_face_middle_1, man_face_old_2],
  ["spy", "Ordinary Townsman", "Ordinary Townsmen", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse, 0, 0, fac_neutral,
   [itm_sword_viking_1, itm_leather_jerkin, itm_leather_boots, itm_courser, itm_leather_gloves],
   def_attrib|agi_11|level(20), regular_melee(20), knows_common, man_face_middle_1, man_face_older_2],
  ["spy_partner", "Unremarkable Townsman", "Unremarkable Townsmen", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse, 0, 0, fac_neutral,
   [itm_sword_medieval_b, itm_leather_jerkin, itm_leather_boots, itm_courser, itm_leather_gloves],
   def_attrib|agi_11|level(10), regular_melee(10), knows_common, vaegir_face1, vaegir_face2],
#  ["conspirator", "Conspirator", "Conspirators", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse, 0, 0, fac_neutral,
#   [itm_sword, itm_leather_jerkin, itm_leather_boots, itm_hunter, itm_leather_gloves],
#   def_attrib|agi_11|level(10), regular_melee(10), knows_common, vaegir_face1, vaegir_face2],
#  ["conspirator_leader", "Conspirator", "Conspirators", tf_mounted|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_horse, 0, 0, fac_neutral,
#   [itm_sword, itm_leather_jerkin, itm_leather_boots, itm_hunter, itm_leather_gloves],
#   def_attrib|agi_11|level(10), regular_melee(10), knows_common, vaegir_face1, vaegir_face2],
#  ["peasant_rebel", "Peasant Rebel", "Peasant Rebels", tf_guarantee_armor, 0, reserved, fac_peasant_rebels,
#   [itm_cleaver, itm_knife, itm_pitch_fork, itm_sickle, itm_club, itm_stones, itm_leather_cap, itm_felt_hat, itm_felt_hat, itm_linen_tunic, itm_coarse_tunic, itm_nomad_boots, itm_wrapping_boots],
#   def_attrib|level(4), regular_melee(4), knows_common, vaegir_face1, vaegir_face2],
#  ["noble_refugee", "Noble Refugee", "Noble Refugees", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_noble_refugees,
#   [itm_sword, itm_leather_jacket, itm_hide_boots, itm_saddle_horse, itm_leather_jacket, itm_leather_cap],
#   def_attrib|level(9), regular_melee(9), knows_common, swadian_face1, swadian_face2],
#  ["noble_refugee_woman", "Noble Refugee Woman", "Noble Refugee Women", tf_female|tf_guarantee_armor|tf_guarantee_boots, 0, 0, fac_noble_refugees,
#   [itm_knife, itm_dagger, itm_hunting_crossbow, itm_dress, itm_robe, itm_woolen_dress, itm_headcloth, itm_woolen_hood, itm_wrapping_boots],
#   def_attrib|level(3), regular_melee(3), knows_common, refugee_face1, refugee_face2],


  ["quick_battle_6_player", "quick_battle_6_player", "quick_battle_6_player", tf_hero, 0, reserved,  fac_player_faction, [itm_padded_cloth, itm_nomad_boots, itm_splinted_leather_greaves, itm_skullcap, itm_sword_medieval_b,  itm_crossbow, itm_bolts, itm_plate_covered_round_shield],    knight_attrib_1, regular_melee(22), knight_skills_1, 0x000000000008010b01f041a9249f65fd],

#SoD - Kuba: buildings:
  ["village", "village", "village", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["town", "town", "town", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["castle", "town", "town", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
	
#SoD - Kuba: laws & strategic map:
  ["law", "law", "law", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["fief", "fief", "fief", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["sm_lords", "sm_troops", "sm_troops", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
  ["sm_centers", "sm_centers", "sm_centers", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],

	
#Player history array
  ["log_array_entry_type",            "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["log_array_entry_time",            "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["log_array_actor",                 "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["log_array_center_object",         "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["log_array_center_object_lord",    "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["log_array_center_object_faction", "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["log_array_troop_object",          "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["log_array_troop_object_faction",  "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],
  ["log_array_faction_object",        "Local Merchant", "Local Merchant", tf_guarantee_boots|tf_guarantee_armor, 0, 0, fac_commoners, [itm_leather_apron, itm_leather_boots, itm_butchering_knife], def_attrib|level(5), regular_melee(5), knows_power_strike_1, merchant_face_1, merchant_face_2],

############################################################################################################################################################################################
# EXPERIENCE TROOP* - THIS MUST BE THE LAST TROOP
# The Experience troop* (troop1) is the same level as the next highest ranking troop on the troop tree.  This makes them more useful and take longer to train (no shortcuts on train time)
############################################################################################################################################################################################
	["experience_troop", "experience_troop", "experience_troop", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0],
]

##################################################################################################################################
# TROOP UPGRADE DECLARATIONS
##################################################################################################################################

#VILLAGERS
upgrade(troops, "farmer", "watchman")
upgrade(troops, "townsman", "watchman")
upgrade2(troops, "watchman", "caravan_guard", "sod_mercenary_footman")
upgrade(troops, "caravan_guard", "mercenary_horseman")
upgrade(troops, "mercenary_swordsman", "hired_blade")
upgrade(troops, "mercenary_horseman", "mercenary_cavalry")
upgrade2(troops, "sod_mercenary_footman", "mercenary_crossbowman", "mercenary_swordsman")
upgrade(troops, "mercenary_crossbowman", "sod_mercenary_sharpshooter")

upgrade(troops, "looter", "bandit")
upgrade2(troops, "bandit", "cutthroat", "brigand")
upgrade(troops, "cutthroat", "thug")
upgrade(troops, "brigand", "reaver")

upgrade2(troops, "manhunter", "caravan_guard", "sod_mercenary_footman")

upgrade(troops, "refugee", "follower_woman")
upgrade(troops, "peasant_woman", "follower_woman")
upgrade(troops, "follower_woman", "hunter_woman")
upgrade(troops, "hunter_woman", "fighter_woman")
upgrade(troops, "fighter_woman", "sword_sister")


#KHERGIT
upgrade(troops, "khergit_tribesman", "khergit_skirmisher")
upgrade(troops, "khergit_skirmisher", "khergit_horseman")
upgrade2(troops, "khergit_horseman", "khergit_lancer", "khergit_horse_archer")
upgrade(troops, "khergit_horse_archer", "khergit_veteran_horse_archer")


#NORD
upgrade2(troops, "nord_recruit", "nord_footman", "nord_huntsman")
upgrade(troops, "nord_footman", "nord_trained_footman")
upgrade(troops, "nord_trained_footman", "nord_warrior")
upgrade(troops, "nord_warrior", "nord_veteran")
upgrade(troops, "nord_veteran", "nord_champion")
upgrade(troops, "nord_huntsman", "nord_archer")
upgrade(troops, "nord_archer", "nord_veteran_archer")


#RHODOK
upgrade2(troops, "rhodok_tribesman", "rhodok_spearman", "rhodok_crossbowman")
upgrade(troops, "rhodok_spearman", "rhodok_trained_spearman")
upgrade(troops, "rhodok_trained_spearman", "rhodok_veteran_spearman")
upgrade(troops, "rhodok_veteran_spearman", "rhodok_sergeant")
upgrade(troops, "rhodok_crossbowman", "rhodok_trained_crossbowman")
upgrade(troops, "rhodok_trained_crossbowman", "rhodok_veteran_crossbowman")
upgrade(troops, "rhodok_veteran_crossbowman", "rhodok_sharpshooter")


#SWADIA
upgrade(troops, "swadian_recruit", "swadian_militia")
upgrade2(troops, "swadian_militia", "swadian_footman", "swadian_skirmisher")
upgrade2(troops, "swadian_footman", "swadian_man_at_arms", "swadian_infantry")
upgrade(troops, "swadian_infantry", "swadian_sergeant")
upgrade(troops, "swadian_skirmisher", "swadian_crossbowman")
upgrade(troops, "swadian_crossbowman", "swadian_sharpshooter")
upgrade(troops, "swadian_man_at_arms", "swadian_knight")


#VAEGIR
upgrade(troops, "vaegir_recruit", "vaegir_footman")
upgrade2(troops, "vaegir_footman", "vaegir_veteran", "vaegir_skirmisher")
upgrade(troops, "vaegir_skirmisher", "vaegir_archer")
upgrade(troops, "vaegir_archer", "vaegir_marksman")
upgrade2(troops, "vaegir_veteran", "vaegir_horseman", "vaegir_infantry")
upgrade(troops, "vaegir_infantry", "vaegir_guard")
upgrade(troops, "vaegir_horseman", "vaegir_knight")


# IMPERIAL EXPEDITIONAY FORCE (LEGION)
upgrade2(troops, "ief_velites", "ief_hestati", "ief_arcus")
upgrade(troops, "ief_hestati", "ief_principes")
upgrade(troops, "ief_principes", "ief_triarii")
upgrade(troops, "ief_arcus", "ief_akritoi")
upgrade(troops, "ief_akritoi", "ief_vexillatio")
upgrade(troops, "ief_speculatores", "ief_clibanarii")
upgrade(troops, "ief_clibanarii", "ief_pronoiar")


# BLACK ARMY MERCENARY GUILD
upgrade(troops, "black_army_fresh_blade", "black_army_line_keeper")
upgrade2(troops, "black_army_line_keeper", "black_army_iron_guard", "black_army_ravager")
upgrade(troops, "black_army_line_supporter", "black_army_assaulter")
upgrade(troops, "black_army_line_crusher", "black_army_ironside")


# CONQUISTADOR MERCENARY GUILD
upgrade2(troops, "conquistador_footman", "conquistador_pikeman", "conquistador_swordsman")
upgrade(troops, "conquistador_pikeman", "conquistador_tercio_pikeman")
upgrade(troops, "conquistador_swordsman", "conquistador_rodelero")
upgrade(troops, "conquistador_crossbowman", "conquistador_seasoned_crossbowman")


# ELEPHANT GUARD MERCENARY GUILD
upgrade2(troops, "elephant_guard_tribesman", "elephant_guard_fighter", "elephant_guard_spearman")
upgrade(troops, "elephant_guard_fighter", "elephant_guard_warrior")
upgrade(troops, "elephant_guard_warrior", "elephant_guard_champion")
upgrade(troops, "elephant_guard_spearman", "elephant_guard_penetrator")


# JOTNAR CLAN MERCENARY GUILD
upgrade2(troops, "jotnar_clan_armsman", "jotnar_clan_jarl", "jotnar_clan_axe_thrower")
upgrade(troops, "jotnar_clan_jarl", "jotnar_clan_einherjar")
upgrade(troops, "jotnar_clan_volva", "jotnar_clan_shield_maiden")
upgrade(troops, "jotnar_clan_shield_maiden", "jotnar_clan_valkyrie")
upgrade(troops, "jotnar_clan_valkyrie", "jotnar_clan_disir")


# SERPENT HOST MERCENARY GUILD
upgrade(troops, "serpent_host_kapikulu", "serpent_host_cemaat")
upgrade(troops, "serpent_host_cemaat", "serpent_host_athanatoi")
upgrade2(troops, "serpent_host_akinci", "serpent_host_sipahi", "serpent_host_timariot")
upgrade(troops, "serpent_host_sipahi", "serpent_host_cataphract")


# SLAVER MERCENARY GUILD
upgrade(troops, "slave", "henchman")
upgrade(troops, "henchman", "slave_driver")
upgrade(troops, "slave_driver", "slave_hunter")
upgrade(troops, "slave_hunter", "slave_crusher")
upgrade(troops, "slave_crusher", "slave_master")
upgrade(troops, "slave_female", "follower_woman")

# BOAR CLAN MINI-GUILD
upgrade2(troops, "boar_clan_clansman", "boar_clan_warrior", "boar_clan_rider")
upgrade(troops, "boar_clan_warrior", "boar_clan_vet_warrior")
upgrade(troops, "boar_clan_rider", "boar_clan_vet_rider")

#SoD UPGRADES BEGIN ########################################
upgrade2(troops, "sod_peasant1", "sod_ant_regular", "sod_ant_javelinman")
upgrade2(troops, "sod_ant_regular", "sod_ant_veteran", "sod_ant_scout")
upgrade(troops, "sod_ant_veteran", "sod_ant_elite")
upgrade(troops, "sod_ant_scout", "sod_ant_cavalry")
upgrade(troops, "sod_ant_javelinman", "sod_ant_trained_javelinman")
upgrade(troops, "sod_ant_noble", "sod_ant_guard")
upgrade(troops, "sod_ant_guard", "sod_ant_honor_guard")

upgrade2(troops, "sod_peasant2", "sod_mar_conscript", "sod_mar_crossbowman")
upgrade2(troops, "sod_mar_conscript", "sod_mar_regular", "sod_mar_scout")
upgrade(troops, "sod_mar_regular", "sod_mar_veteran")
upgrade(troops, "sod_mar_veteran", "sod_mar_elite")
upgrade(troops, "sod_mar_crossbowman", "sod_mar_trained_crossbowman")
upgrade(troops, "sod_mar_trained_crossbowman", "sod_mar_elite_crossbowman")
upgrade(troops, "sod_mar_elite_crossbowman", "sod_mar_sharpshooter")
upgrade(troops, "sod_mar_mercenary", "sod_mar_landsknecht")
upgrade(troops, "sod_mar_landsknecht", "sod_mar_condottieri")

upgrade2(troops, "sod_peasant3", "sod_ade_regular", "sod_ade_archer")
upgrade2(troops, "sod_ade_regular", "sod_ade_veteran", "sod_ade_light")
upgrade(troops, "sod_ade_veteran", "sod_ade_elite")
upgrade(troops, "sod_ade_archer", "sod_ade_veteran_archer")
upgrade(troops, "sod_ade_veteran_archer", "sod_ade_elite_archer")
upgrade(troops, "sod_ade_light", "sod_ade_medium")
upgrade(troops, "sod_ade_medium", "sod_ade_heavy")
upgrade(troops, "sod_ade_sqire", "sod_ade_knight")
upgrade(troops, "sod_ade_knight", "sod_ade_magnate")


upgrade2(troops, "sod_peasant4", "sod_vil_regular", "sod_vil_longbowman")
upgrade2(troops, "sod_vil_regular", "sod_vil_veteran", "sod_vil_scout")
upgrade(troops, "sod_vil_veteran", "sod_vil_elite")
upgrade(troops, "sod_vil_longbowman", "sod_vil_veteran_longbowman")
upgrade(troops, "sod_vil_veteran_longbowman", "sod_vil_elite_longbowman")
upgrade(troops, "sod_vil_elite_longbowman", "sod_vil_sharpshooter")
upgrade(troops, "sod_vil_noble", "sod_vil_chief")
upgrade(troops, "sod_vil_chief", "sod_vil_high_chief")


upgrade2(troops, "sod_peasant5", "sod_zer_1_infantry", "sod_zer_1_archer")
upgrade2(troops, "sod_zer_1_infantry", "sod_zer_1_cavalry", "sod_zer_2_infantry")
upgrade2(troops, "sod_zer_1_cavalry", "sod_zer_2_cavalry", "sod_zer_1_cavalry_archer")
upgrade(troops, "sod_zer_2_infantry", "sod_zer_3_infantry")
upgrade(troops, "sod_zer_1_archer", "sod_zer_2_archer")
upgrade(troops, "sod_zer_2_cavalry", "sod_zer_3_cavalry")
upgrade(troops, "sod_zer_1_noble", "sod_zer_2_noble")
upgrade(troops, "sod_zer_2_noble", "sod_zer_3_noble")
#SoD UPGRADES END ########################################

sod_noble_troops = [trp_sod_ant_guard, trp_sod_ant_honor_guard,
trp_sod_mar_landsknecht, trp_sod_mar_condottieri, trp_sod_ade_knight, trp_sod_ade_magnate,
trp_sod_vil_chief, trp_sod_vil_high_chief, trp_sod_zer_2_noble, trp_sod_zer_3_noble,
trp_ief_hospitalier, trp_ief_akolouthos, trp_ief_praetorian]

sod_faith_troops = [trp_sod_faith2_mount, trp_sod_faith2_foot, trp_sod_faith2_ranged_1,
trp_sod_faith2_ranged_2, trp_sod_faith2_mount_ranged, trp_sod_faith1_mount, trp_sod_faith1_foot,
trp_sod_faith1_range_1, trp_sod_faith1_range_2, trp_sod_faith1_mount_range, trp_sod_faith3_mount,
trp_sod_faith3_foot, trp_sod_faith3_ranged_1, trp_sod_faith3_ranged_2, trp_sod_faith3_mount_ranged,
trp_sod_faith4_mount, trp_sod_faith4_foot, trp_sod_faith4_ranged_1, trp_sod_faith4_ranged_2,
trp_sod_faith4_mount_ranged, trp_sod_faith5_mount, trp_sod_faith5_foot, trp_sod_faith5_ranged_1,
trp_sod_faith5_ranged_2, trp_sod_faith5_mount_ranged]

for trp in sod_noble_troops:
	sod_upgrade_command_list.append((troop_set_slot, trp, slot_troop_sod_soldier, 4))
for trp in sod_faith_troops:
	sod_upgrade_command_list.append((troop_set_slot, trp, slot_troop_sod_soldier, 5))


# Black Khergit moving horde leader. Kept near the tail to avoid shifting legacy troop ids.
troops.append(["black_khergit_khan", "Temujin Black Sky", "Temujin Black Sky", tf_hero|tf_mounted|tf_guarantee_ranged|tf_guarantee_shield|tf_guarantee_boots|tf_guarantee_helmet|tf_guarantee_armor|tf_guarantee_horse, 0, 0, fac_black_khergits,
   [itm_khergit_bow, itm_khergit_arrows, itm_sword_khergit_4, itm_scimitar, itm_lance, itm_tab_shield_round_e,
    itm_khergit_war_helmet, itm_khergit_guard_armor, itm_khergit_guard_boots, itm_steppe_horse_lv, itm_steppe_horse_b],
   def_attrib|level(36), expert_archer(36)|expert_melee(36), knows_riding_7|knows_horse_archery_7|knows_power_draw_7|knows_power_strike_6|knows_ironflesh_6|knows_weapon_master_6|knows_shield_4|knows_tactics_4, khergit_face_older_1, khergit_face_old_2])

# Player banking vault. Kept near the tail to avoid shifting legacy troop ids.
troops.append(["sod_bankvault_possessions", "{!}sod_bankvault_possessions", "{!}sod_bankvault_possessions", tf_hero|tf_inactive|tf_is_merchant, no_scene, reserved, fac_neutral, [], def_attrib|level(18), wp_all(60), knows_inventory_management_10, 0])

# Public health relief civilian. Kept near the tail to avoid shifting legacy troop ids.
troops.append(["sod_public_health_clergy", "Relief Cleric", "Relief Clergy", tf_guarantee_boots|tf_guarantee_armor, no_scene, reserved, fac_commoners,
   [itm_staff, itm_quarter_staff, itm_wooden_stick, itm_club,
    itm_robe, itm_pilgrim_hood, itm_wrapping_boots],
   def_attrib|int_12|cha_10|level(8), weak_melee(8), knows_first_aid_2|knows_surgery_1|knows_wound_treatment_2, man_face_middle_1, man_face_old_2])

# for iterating thru experienced troops
troops.append(["last_troop", "last_troop", "last_troop", tf_hero|tf_inactive, 0, reserved,  fac_neutral, [], def_attrib|level(18), regular_melee(18), knows_common, 0])
