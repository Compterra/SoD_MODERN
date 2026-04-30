# -*- coding: utf-8 -*-
# Auto-generated from src/quests/0001_all_quests.py.
# Keep quest definitions in the numbered fragments and rebuild with build/build_quests.py.

QUESTS = [
 ("deliver_grain", "Bring wheat to {s3}", qf_random_quest,
  "The elder of the village of {s3} asked you to bring them {reg5} packs of wheat.."
  ),

 ("deliver_cattle", "Deliver {reg5} Heads of Cattle to {s3}", qf_random_quest,
  "The elder of the village of {s3} asked you to bring {reg5} heads of cattle."
  ),

 ("train_peasants_against_bandits", "Train the Peasants of {s13} Against Bandits.", qf_random_quest,
  "None"
  ), 
# Deliver horses, Deliver food, Escort_Caravan, Hunt bandits, Ransom Merchant.
## ("capture_nobleman", "Capture Nobleman",qf_random_quest,
##  "{s1} wanted you to capture an enemy nobleman on his way from {s3} to {s4}. He said the nobleman would leave {s3} in {reg1} days."
##  ),

# Bandit quests: Capture rich merchant, capture banker, kill manhunters?..

# Note : This is defined as the last village elder quest in module_constants.py:,

 ("eliminate_bandits_infesting_village", "Save the Village of {s7} from Marauding Bandits", qf_random_quest,
  "A villager from {s7} begged you to save their village from the bandits that took refuge there."
  ),
]
