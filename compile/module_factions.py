from header_factions import *

####################################################################################################################
#  Each faction record contains the following fields:
#  1) Faction id: used for referencing factions in other files.
#     The prefix fac_ is automatically added before each faction id.
#  2) Faction name.
#  3) Faction flags. See header_factions.py for a list of available flags
#  4) Faction coherence. Relation between members of this faction.
#  5) Relations. This is a list of relation records.
#     Each relation record is a tuple that contains the following fields:
#    5.1) Faction. Which other faction this relation is referring to
#    5.2) Value: Relation value between the two factions.
#         Values range between -1 and 1.
#  6) Ranks
#  7) Faction color (default is gray)
####################################################################################################################

default_kingdom_relations = [("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.05), ("mountain_bandits", -0.02), ("forest_bandits", -0.02), ("sod_merc_guild7", -0.02)]
factions = [
  ("no_faction", "No Faction", 0, 0.9, [], []),
  ("commoners", "Commoners", 0, 0.1, [("player_faction", 0.1)], []),
  ("outlaws", "Outlaws", max_player_rating(-30), 0.5, [("commoners", -0.6), ("player_faction", -0.15)], [], 0x888888),
# Factions before this point are hardwired into the game end their order should not be changed.

  ("neutral", "Neutral", 0, 0.1, [("player_faction", 0.0)], [], 0xFFFFFF),
  ("innocents", "Innocents", ff_always_hide_label, 0.5, [("outlaws", -0.05)], []),
  ("merchants", "Merchants", ff_always_hide_label, 0.5, [("outlaws", -0.5), ], []),

  ("dark_knights", "Dark Knights", 0, 0.5, [("innocents", -0.9), ("player_faction", -0.4)], []),

  ("culture_1",  "culture_1", 0, 0.9, [], []),
  ("culture_2",  "culture_2", 0, 0.9, [], []),
  ("culture_3",  "culture_3", 0, 0.9, [], []),
  ("culture_4",  "culture_4", 0, 0.9, [], []),
  ("culture_5",  "culture_5", 0, 0.9, [], []),
  ("culture_6",  "culture_6", 0, 0.9, [], []),
#SOD BEGIN
  ("sod_culture_1",  "sod_culture_1", 0, 0.9, [], []),
  ("sod_culture_2",  "sod_culture_2", 0, 0.9, [], []),
  ("sod_culture_3",  "sod_culture_3", 0, 0.9, [], []),
  ("sod_culture_4",  "sod_culture_4", 0, 0.9, [], []),
  ("sod_culture_5",  "sod_culture_5", 0, 0.9, [], []),
#SOD END
#SoD mercenary guilds begin
	("sod_merc_guild1","The Black Army", ff_always_hide_label, 0.5,[("outlaws", -1), ("peasant_rebels", -1), ("deserters", -1), ("mountain_bandits", -1), ("forest_bandits", -1)],[],0xFFFFFFFF),
	("sod_merc_guild2","The Conquistadors", ff_always_hide_label, 0.5,[("outlaws", -1), ("peasant_rebels", -1), ("deserters", -1), ("mountain_bandits", -1), ("forest_bandits", -1)],[],0xFFFFFFFF),
	("sod_merc_guild3","The Elephant Guard", ff_always_hide_label, 0.5,[("outlaws", -1), ("peasant_rebels", -1), ("deserters", -1), ("mountain_bandits", -1), ("forest_bandits", -1)],[],0xFFFFFFFF),
	("sod_merc_guild4","The Jotnar Clan", ff_always_hide_label, 0.5,[("outlaws", -1), ("peasant_rebels", -1), ("deserters", -1), ("mountain_bandits", -1), ("forest_bandits", -1)],[],0xFFFFFFFF),
	("sod_merc_guild5","The Serpent Host", ff_always_hide_label, 0.5,[("outlaws", -1), ("peasant_rebels", -1), ("deserters", -1), ("mountain_bandits", -1), ("forest_bandits", -1)],[],0xFFFFFFFF),
	("sod_merc_guild6","The Slavers", ff_always_hide_label, 0.5,[("outlaws", -1), ("peasant_rebels", -1), ("deserters", -1), ("mountain_bandits", -1), ("forest_bandits", -1)],[],0xFFFFFF),
	("sod_merc_guild7","The Boar Clan", ff_always_hide_label, 0.5,[("commoners", -0.6), ("player_faction", -0.05)],[],0xCDBA96),
#SoD mercenary guilds end

	# additional mercenary guild
	("kingdom_6_mercenaries",  "Imperial Mercenaries", max_player_rating(-100), 0.9, [("player_faction", -1), ("player_supporters_faction", -1), ("kingdom_1", -1), ("kingdom_2", -1), ("kingdom_3", -1), ("kingdom_4", -1), ("kingdom_5", -1), ("outlaws", -1), ("peasant_rebels", -1), ("deserters", -1), ("mountain_bandits", -1), ("forest_bandits", -1)], [], 0xFF0000),

#  ("swadian_caravans", "Swadian Caravans", 0, 0.5, [("outlaws", -0.8), ("dark_knights", -0.2)], []),
#  ("vaegir_caravans", "Vaegir Caravans", 0, 0.5, [("outlaws", -0.8), ("dark_knights", -0.2)], []),

  ("player_faction", "Player Faction", 0, 0.9, [], []),
  ("player_supporters_faction", "Player Faction", 0, 0.9, [("sod_merc_guild7", -0.05), ("player_faction", 1.00), ("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.05), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], []),
  ("kingdom_1",  "Kingdom of Swadia", 0, 0.9, [("sod_merc_guild7", -0.05), ("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0xDD8844),
  ("kingdom_2",  "Kingdom of Vaegirs",    0, 0.9, [("sod_merc_guild7", -0.05), ("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0x33DD33),
  ("kingdom_3",  "Khergit Khanate", 0, 0.9, [("sod_merc_guild7", -0.05), ("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0xCC99FF),
  ("kingdom_4",  "Kingdom of Nords",    0, 0.9, [("sod_merc_guild7", -0.05), ("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0xDDDD33),
  ("kingdom_5",  "Rhodok Republic",  0, 0.9, [("sod_merc_guild7", -0.05), ("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0x33DDDD),
  ("kingdom_6",  "Imperial Expeditionary Force", max_player_rating(-100), 0.9, [("player_faction", -1), ("player_supporters_faction", -1), ("kingdom_1", -1), ("kingdom_2", -1), ("kingdom_3", -1), ("kingdom_4", -1), ("kingdom_5", -1)], [], 0xFF0000),
##  ("kingdom_1_rebels",  "Swadian rebels", 0, 0.9, [("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0xCC2211),
##  ("kingdom_2_rebels",  "Vaegir rebels",    0, 0.9, [("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0xCC2211),
##  ("kingdom_3_rebels",  "Khergit rebels", 0, 0.9, [("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0xCC2211),
##  ("kingdom_4_rebels",  "Nord rebels",    0, 0.9, [("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0xCC2211),
##  ("kingdom_5_rebels",  "Rhodok rebels",  0, 0.9, [("outlaws", -0.05), ("peasant_rebels", -0.1), ("deserters", -0.02), ("mountain_bandits", -0.05), ("forest_bandits", -0.05)], [], 0xCC2211),

  ("kingdoms_end", "kingdoms_end", 0, 0, [], []),
	("elephant_guard", "kingdoms_end", 0, 0, [], []),
	("slavers", "kingdoms_end", 0, 0, [], []),
  ("robber_knights",  "robber_knights", 0, 0.1, [], []),

  ("khergits", "Khergits", 0, 0.5, [("player_faction", 0.0)], []),
  ("black_khergits", "Black Khergits", 0, 0.5, [("player_faction", -0.3), ("kingdom_1", -0.02), ("kingdom_2", -0.02)], []),

##  ("rebel_peasants", "Rebel Peasants", 0, 0.5, [("vaegirs", -0.5), ("player_faction", 0.0)], []),

  ("manhunters", "Manhunters", 0, 0.5, [("outlaws", -0.6), ("player_faction", 0.1)], []),
  ("deserters", "Deserters", 0, 0.5, [("commoners", -0.2), ("manhunters", -0.6), ("merchants", -0.5), ("player_faction", -0.1)], [], 0x888888),
  ("mountain_bandits", "Mountain Bandits", 0, 0.5, [("commoners", -0.2), ("merchants", -0.5), ("manhunters", -0.6), ("player_faction", -0.2),], [], 0x888888),
  ("forest_bandits", "Forest Bandits", 0, 0.5, [("commoners", -0.2), ("merchants", -0.5), ("manhunters", -0.6), ("player_faction", -0.15)], [], 0x888888),

  ("undeads", "Undeads", max_player_rating(-30), 0.5, [("commoners", -0.7), ("player_faction", -0.5)], []),
  ("peasant_rebels", "Peasant Rebels", 0, 1.0, [("noble_refugees", -1.0), ("player_faction", -0.4)], []),
  ("noble_refugees", "Noble Refugees", 0, 0.5, [], []),
  
  ("factions_end","factions_end", 0, 0,[], []),
]
