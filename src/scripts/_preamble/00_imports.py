# -*- coding: cp1254 -*-

from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *

import string
from process_common import *
from module_troops import *
from module_items import *

	
############## SOD TWAN : KT0 IMPROVED AUTORESOLVE SYSTEM BEGIN #######################################

# pulls the gigantor values out of the skill blob and returns a 3-tuple
# containing power draw, power strike, and power draw skill values.
def kt_get_power_skills( flags ):
   pdraw = 0
   pstrk = 0
   pthrw = 0
   pdraw_top = knows_power_draw_10 + knows_power_draw_5
   pstrk_top = knows_power_strike_10 + knows_power_strike_5
   pthrw_top = knows_power_throw_10 + knows_power_throw_5
   
   if ( flags & pdraw_top ) > 0:
      pdraw = flags & pdraw_top
      pdraw /= knows_power_draw_1
   if ( flags & pstrk_top ) > 0:
      pstrk = flags & pstrk_top
      pstrk /= knows_power_strike_1
   if ( flags & pthrw_top ) > 0:
      pthrw = flags & pthrw_top
      pthrw /= knows_power_throw_1
   
   return (pdraw, pstrk, pthrw)

# pulls the gigantor values out of the skill blob and returns a 3-tuple
# containing shield, athletics, and ironflesh skill values.
def kt_get_melee_skills( flags ):
   shld = 0
   athl = 0
   irfl = 0
   shld_top = knows_shield_10 + knows_shield_5
   athl_top = knows_athletics_10 + knows_athletics_5
   irfl_top = knows_ironflesh_10 + knows_ironflesh_5
   
   if ( flags & shld_top ) > 0:
      shld = flags & shld_top
      shld /= knows_shield_1
   if ( flags & athl_top ) > 0:
      athl = flags & athl_top
      athl /= knows_athletics_1
   if ( flags & irfl_top ) > 0:
      irfl = flags & irfl_top
      irfl /= knows_ironflesh_1
   
   return (shld, athl, irfl)

# parse troop items and return a tuple containing average item values.  
# we make assumptions on the flags and average gear of the same type
# to get aggregate values.  note that the weights given to items in a
# list that aren't guaranteed with a tf_ flag are a guess.  i'm counting
# no flag as a 0 value in the average which might not be correct.
def kt_apply_doctrine_modifiers(troop_id, o_val, d_val, h_val, troop_type):
   troop_name = troops[troop_id][0]

   # Faith elites and the Imperial Expeditionary Force are meant to be exceptional,
   # but the boost is deliberately bounded so autoresolve remains auditable.
   if troop_name.startswith("sod_faith"):
      o_val *= 115
      o_val /= 100
      d_val *= 115
      d_val /= 100
   elif troop_name.startswith("ief_") or troop_name.startswith("imperial_") or troop_name.startswith("legion_"):
      # Core Expedition troops use the legacy ief_ prefix; retain the older
      # imperial_/legion_ aliases for compatible auxiliary content.
      o_val *= 110
      o_val /= 100
      d_val *= 110
      d_val /= 100
   elif (
      troop_name.startswith("black_army_")
      or troop_name.startswith("conquistador_")
      or troop_name.startswith("elephant_guard_")
      or troop_name.startswith("jotnar_")
      or troop_name.startswith("serpent_")
      or troop_name.startswith("boar_")
      or troop_name.startswith("slaver")
      or troop_name.startswith("tormenter")
   ):
      o_val *= 105
      o_val /= 100
      d_val *= 105
      d_val /= 100

   # Blunt-heavy slaver troops should capture well in played battles, but blunt
   # damage should not make them disproportionate autoresolve killers.
   if troop_name.startswith("slaver") or troop_name.startswith("tormenter"):
      o_val *= 95
      o_val /= 100

   return (o_val, d_val, h_val, troop_type)


def kt_parse_troop_items( item_list, flags, ohprof, thprof, poleprof, bowprof, xbowprof, throwprof, pstrike, pdraw, pthrow ):
   mw_value = 0 # melee weapon damage of the greater if multiple
   mw_count = 0 # never seen a guy without a weapon O_O
   rw_value = 0 # ranged weapon damage
   rw_count = 1
   ha_value = 0 # head armor
   ha_count = 1
   ba_value = 0 # body armor
   ba_count = 1
   fa_value = 0 # foot armor
   fa_count = 1
   na_value = 0 # hand armor
   na_count = 1
   sh_value = 0 # shield percentage 0-100
   sh_count = 1
   ho_value = 0 # horse aggregate charge and armor value
   ho_count = 1

   guarantee_horse = 0
   guarantee_ranged = 0
   troop_type = kt_troop_type_footsoldier

   # parse guarantee flags
   if ( flags & tf_guarantee_boots ) > 0:
      fa_count = 0
   if ( flags & tf_guarantee_armor ) > 0:
      ba_count = 0
   if ( flags & tf_guarantee_helmet ) > 0:
      ha_count = 0
   if ( flags & tf_guarantee_horse ) > 0:
      ho_count = 0
      guarantee_horse = 1
   if ( flags & tf_guarantee_shield ) > 0:
      sh_count = 0
   if ( flags & tf_guarantee_ranged ) > 0:
      rw_count = 0
      guarantee_ranged = 1

   # Determine troop type dynamically by interrogating the parsed items instead of just flags! (Moved to end of function)
   
   # constants
   pierce_flag = pierce << iwf_damage_type_bits
   blunt_flag = blunt << iwf_damage_type_bits

   # parse each item
   # once we know the type, we pull the values from the appropriate places.
   # if we don't know the type, we ignore the item.  we also ignore ammo
   # and books and a handful of other things intentionally.
   for item in item_list:
      item_type = items[item][3] & 0xFF
      if itp_type_horse == item_type:
         ho_count += 1
         chg = get_thrust_damage( items[item][6] )
         arm = get_body_armor( items[item][6] )
         ho_value += chg
         ho_value += (arm+5)/10
      # we only consider the higher of thrust or swing damage
      elif item_type in (itp_type_one_handed_wpn, itp_type_two_handed_wpn, itp_type_polearm):
         mw_count += 1
         swd = get_swing_damage( items[item][6] )
         thd = get_thrust_damage( items[item][6] )
         speed = get_speed_rating( items[item][6] )
         if (swd & pierce_flag) > 0:
            swd &= 0xFF
            swd *= 3
            swd /= 2
         elif (swd & blunt_flag) > 0:
            swd &= 0xFF
            swd *= 5
            swd /= 4
         if (thd & pierce_flag) > 0:
            thd &= 0xFF
            thd *= 3
            thd /= 2
         elif (thd & blunt_flag) > 0:
            thd &= 0xFF
            thd *= 5
            thd /= 4
         # also modify by speed rating and proficiency
         prof = 100
         if item_type == itp_type_one_handed_wpn:
            prof = ohprof
         elif item_type == itp_type_two_handed_wpn:
            prof = thprof
         elif item_type == itp_type_polearm:
            prof = poleprof            
         swd *= speed
         swd *= prof
         thd *= speed
         thd *= prof
         if pstrike > 0:
            swd *= (100 + pstrike * 8)
            swd /= 100
            thd *= (100 + pstrike * 8)
            thd /= 100
         swd /= 10000
         thd /= 10000
         if swd > thd:
            mw_value += swd
         else:
            mw_value += thd
      elif item_type in (itp_type_bow, itp_type_crossbow, itp_type_thrown):
         rw_count += 1
         rdam = get_thrust_damage( items[item][6] )
         # adjust for type
         if (rdam & pierce_flag) > 0:
            rdam &= 0xFF
            rdam *= 3
            rdam /= 2
         elif (rdam & blunt_flag) > 0:
            rdam &= 0xFF
            rdam *= 5
            rdam /= 4
         # adjust for speed and accuracy
         acc = get_leg_armor( items[item][6] )
         spd = get_speed_rating( items[item][6] )
         if acc == 0:
            acc = 100
         rdam *= acc
         rdam *= spd
         # adjust for proficiency
         if item_type == itp_type_bow:
            rdam *= bowprof
            if pdraw > 0:
               pdraw_amt = get_difficulty( items[item][6] )
               pdraw_amt += 4
               if pdraw < pdraw_amt:
                  pdraw_amt = pdraw
               rdam *= (100 + pdraw_amt*14)
               rdam /= 100
         elif item_type == itp_type_crossbow:
            rdam *= xbowprof
         elif item_type == itp_type_thrown:
            rdam *= throwprof
            if pthrow > 0:
               rdam *= (100 + pthrow*10)
               rdam /= 100
         rdam /= 1000000
         rw_value += rdam
      elif itp_type_shield == item_type:
         sh_count += 1
         sh_value += get_weapon_length( items[item][6] )
      elif item_type in (itp_type_head_armor, itp_type_body_armor, itp_type_foot_armor, itp_type_hand_armor):
         if itp_type_head_armor == item_type:            
            ha_count += 1
         elif itp_type_body_armor == item_type:
            ba_count += 1
         elif itp_type_foot_armor == item_type:
            fa_count += 1
         elif itp_type_hand_armor == item_type:
            na_count += 1
            na_value += get_body_armor( items[item][6] )
         else:
            print("ERROR:  item ", items[item][0], " is unknown armor type!") # shouldn't ever get this
         ba_value += get_body_armor( items[item][6] )
         fa_value += get_leg_armor( items[item][6] )
         ha_value += get_head_armor( items[item][6] )

   # do the averaging; values will be rough
   if ba_count > 0:   # nb:  this doesn't catch no body armor + gloves case
      ba_value -= na_value
      ba_value /= ba_count
      if na_count > 0:
         na_value /= na_count
      ba_value += na_value
   if ha_count > 0:
      ha_value /= ha_count
   if fa_count > 0:
      fa_value /= fa_count
   if mw_count > 0:
      mw_value /= mw_count
   if rw_count > 0:
      rw_value /= rw_count
   if sh_count > 0:
      sh_value /= sh_count
   if ho_count > 0:
      ho_value /= ho_count
   # Determine troop type dynamically by interrogating the parsed items instead of just flags!
   if guarantee_horse and guarantee_ranged:
      troop_type = kt_troop_type_mtdarcher
   elif guarantee_horse and not guarantee_ranged:
      troop_type = kt_troop_type_cavalry
   elif not guarantee_horse and guarantee_ranged:
      troop_type = kt_troop_type_archer
   else:
      troop_type = kt_troop_type_footsoldier

   # Fallback dynamically if flag parsing failed or flags were omitted by Modders
   if troop_type == kt_troop_type_footsoldier:
      if ho_value > 0 and rw_value > 0:
         troop_type = kt_troop_type_mtdarcher
      elif ho_value > 0:
         troop_type = kt_troop_type_cavalry
      elif rw_value > 0:
         troop_type = kt_troop_type_archer

   return (mw_value, rw_value, ha_value, ba_value, fa_value, sh_value, ho_value, troop_type)

# generates code tuples for setting slots based on values accessible
# during compile.  this gets inserted into the scripts array and parsed
# like any other module code.  
def kt_python_init_troop_slots():
   module_code = []
   
   # figure out our bounds
   underscore_pos = str.find( soldiers_begin, "_" )
   id_str = soldiers_begin[ underscore_pos+1:len(soldiers_begin) ]
   begin_troop = find_troop( troops, id_str )
   underscore_pos = str.find( soldiers_begin, "_" )
   id_str = soldiers_end[ underscore_pos+1 : len(soldiers_end) ]   
   end_troop = find_troop( troops, id_str )
      
   # process for each troop
   for i_troop in range(begin_troop, end_troop+1):
      oneh_prof = (troops[i_troop][9] >> one_handed_bits) & 0x3FF
      twoh_prof = (troops[i_troop][9] >> two_handed_bits) & 0x3FF
      pole_prof = (troops[i_troop][9] >> polearm_bits) & 0x3FF
      arch_prof = (troops[i_troop][9] >> archery_bits) & 0x3FF
      xbow_prof = (troops[i_troop][9] >> crossbow_bits) & 0x3FF
      thrw_prof = (troops[i_troop][9] >> throwing_bits) & 0x3FF
      att_str = (troops[i_troop][8] & 0xFF)
      att_agi = (troops[i_troop][8] & 0xFF00) >> 8
      att_int = (troops[i_troop][8] & 0xFF0000) >> 16
      att_cha = (troops[i_troop][8] & 0xFF000000) >> 24
      # setup special skills (add whatever you care about here as well)
      (skill_pdraw, skill_pstrike, skill_pthrow) = kt_get_power_skills( troops[i_troop][10] )
      (skill_shld, skill_athl, skill_irfl) = kt_get_melee_skills( troops[i_troop][10] )
      mw_value = 0
      rw_value = 0
      ha_value = 0
      ba_value = 0
      fa_value = 0
      sh_value = 0
      ho_value = 0
      troop_type = 0
      (mw_value, rw_value, ha_value, ba_value, fa_value, sh_value, ho_value, troop_type) = kt_parse_troop_items( troops[i_troop][7], troops[i_troop][3], oneh_prof, twoh_prof, pole_prof, arch_prof, xbow_prof, thrw_prof, skill_pstrike, skill_pdraw, skill_pthrow )
      d_val = ha_value + ba_value + fa_value + sh_value
      d_val /= 5
      d_val += skill_irfl*2
      d_val += att_str
      if troop_type in (kt_troop_type_mtdarcher, kt_troop_type_archer):
         o_val = mw_value / 3 + rw_value
      if troop_type in (kt_troop_type_footsoldier, kt_troop_type_cavalry):
         o_val = mw_value + rw_value / 4
      h_val = ho_value
      (o_val, d_val, h_val, troop_type) = kt_apply_doctrine_modifiers(i_troop, o_val, d_val, h_val, troop_type)
      module_code.append( (troop_set_slot, "trp_"+troops[i_troop][0], kt_slot_troop_o_val, o_val) )
      module_code.append( (troop_set_slot, "trp_"+troops[i_troop][0], kt_slot_troop_d_val, d_val) )
      module_code.append( (troop_set_slot, "trp_"+troops[i_troop][0], kt_slot_troop_h_val, h_val) )
      module_code.append( (troop_set_slot, "trp_"+troops[i_troop][0], kt_slot_troop_type, troop_type) )
   
      old_val = troops[i_troop][8]
      old_val >>= level_bits
      old_val &= level_mask
      old_val += 12
      old_val *= old_val
      old_val /= 100
      troop_string = "footsoldier"
      if troop_type == kt_troop_type_cavalry:
         troop_string = "cavalry"
      if troop_type == kt_troop_type_archer:
         troop_string = "archer"
      if troop_type == kt_troop_type_mtdarcher:
         troop_string = "mtdarcher"
         
   return module_code[:]
   
   ############## SOD TWAN : KT0 IMPROVED AUTORESOLVE SYSTEM END #######################################
 

 #### Autoloot improved by rubik begin
from module_items import *
  #### Autoloot improved by rubik end

  #### Autoloot improved by rubik begin
ibf_item_type_mask = 0x000000ff

def set_item_difficulty():
  item_difficulty = []    # create a empty list: item_difficulty
  for i_item in range(len(items)):  # do a loop in the list items
    item_difficulty.append((item_set_slot, i_item, slot_item_difficulty, get_difficulty(items[i_item][6]))) # append Module System sentences to the list
  return item_difficulty[:]  # return the whole list with all MS sentences above

def get_swing_damage_type(y):
  return (y >> (iwf_damage_type_bits+iwf_swing_damage_bits)) & 0x03

def get_thrust_damage_type(y):
  return (y >> (iwf_damage_type_bits+iwf_thrust_damage_bits)) & 0x03

def set_item_base_score():
  item_base_score = []
  for i_item in range(len(items)):
    # get the base type without its bitflag attributes
    type = items[i_item][3] & ibf_item_type_mask

    if type >= itp_type_head_armor and type <= itp_type_hand_armor:

      # store armor attributes
      item_base_score.append((item_set_slot, i_item, slot_item_head_armor, get_head_armor(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, slot_item_body_armor, get_body_armor(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, slot_item_leg_armor, get_leg_armor(items[i_item][6])))

    elif type >= itp_type_one_handed_wpn and type <= itp_type_thrown and type != itp_type_shield:

      # store weapon attributes
      item_base_score.append((item_set_slot, i_item, slot_item_thrust_damage, get_thrust_damage(items[i_item][6])&0xff))
      item_base_score.append((item_set_slot, i_item, slot_item_swing_damage, get_swing_damage(items[i_item][6])&0xff))
      item_base_score.append((item_set_slot, i_item, slot_item_thrust_damage_type, get_thrust_damage_type(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, slot_item_swing_damage_type, get_swing_damage_type(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, slot_item_weapon_speed, get_speed_rating(items[i_item][6])))
      if items[i_item][3] & itp_cant_use_on_horseback == itp_cant_use_on_horseback:
        item_base_score.append((item_set_slot, i_item, slot_item_cant_use_on_horseback, 1))
      else:
        item_base_score.append((item_set_slot, i_item, slot_item_cant_use_on_horseback, 0))

    elif type == itp_type_shield:

      # store shield attributes
      item_base_score.append((item_set_slot, i_item, slot_item_shield_size, get_weapon_length(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, slot_item_shield_armor, get_body_armor(items[i_item][6])))
      if items[i_item][3] & itp_cant_use_on_horseback == itp_cant_use_on_horseback:
        item_base_score.append((item_set_slot, i_item, slot_item_cant_use_on_horseback, 1))
      else:
        item_base_score.append((item_set_slot, i_item, slot_item_cant_use_on_horseback, 0))

    elif type == itp_type_horse:

      # store horse attributes
      item_base_score.append((item_set_slot, i_item, slot_item_horse_speed, get_missile_speed(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, slot_item_horse_armor, get_body_armor(items[i_item][6])))
      item_base_score.append((item_set_slot, i_item, slot_item_horse_charge, get_thrust_damage(items[i_item][6])&0xff))

  return item_base_score[:]
  #### Autoloot improved by rubik end

def set_imod_effects():
  effects = []
  for i_effect in range(len(imod_effects)):
    imod_id = imod_effects[i_effect][0]
    effects.append((item_set_slot, imod_id, slot_item_imod_cost,    imod_effects[i_effect][1]))
    effects.append((item_set_slot, imod_id, slot_item_imod_require, imod_effects[i_effect][2]))
    effects.append((item_set_slot, imod_id, slot_item_imod_speed,   imod_effects[i_effect][3]))
    effects.append((item_set_slot, imod_id, slot_item_imod_armor,   imod_effects[i_effect][4]))
    effects.append((item_set_slot, imod_id, slot_item_imod_damage,  imod_effects[i_effect][5]))
  return effects[:]

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################
