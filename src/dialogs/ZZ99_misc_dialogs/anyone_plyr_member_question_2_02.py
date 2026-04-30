DIALOGS = [
[anyone|plyr, "member_question_2",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
    (troop_get_slot, ":last", "$g_talk_troop", slot_troop_level_up),
    (store_character_level, ":current", "$g_talk_troop"),
    (lt, ":last", ":current"),
  ],
  "You've picked up some new tricks. Let's review your skills.", "member_anything_else",
  [
    (store_character_level, ":current", "$g_talk_troop"),
    (troop_set_slot, "$g_talk_troop", slot_troop_level_up, ":current"),
    (change_screen_view_character),
  ]],

[anyone|plyr, "member_question_2",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
    (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
    (lt, reg0, 8),
  ],
  "Tell me your story again.", "member_background_trust_too_low", []],

[anyone|plyr, "member_question_2",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
    (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
    (is_between, reg0, 8, 16),
  ],
  "Tell me your story again.", "member_background_reveal_1", []],

[anyone|plyr, "member_question_2",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
    (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
    (is_between, reg0, 16, 24),
  ],
  "Tell me your story again.", "member_background_reveal_2", []],

[anyone|plyr, "member_question_2",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
    (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
    (ge, reg0, 24),
  ],
  "Tell me your story again.", "member_background_reveal_3", []],

[anyone|plyr, "member_question_2",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
  ],
  "How do you judge the state of our company these days?", "member_campaign_conditions", []],

[anyone|plyr, "member_question_2",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
  ],
  "What sits worst with you about life in this company?", "member_personal_outlook", []],

[anyone|plyr, "member_question_2",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_player_companion),
  ],
  "Is there anyone in the company you find especially hard to bear?", "member_company_friction", []],

[anyone, "member_background_trust_too_low", [],
  "In time, perhaps. A person can ride beside good company for a while and still keep a few locked doors in the heart. Give trust a little longer to take root between us.", "member_anything_else", []],

[anyone, "member_background_reveal_1",
  [
    (troop_get_slot, ":first_met", "$g_talk_troop", slot_troop_first_encountered),
    (str_store_party_name, 20, ":first_met"),
    (troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
    (str_store_party_name, 21, ":home"),
    (troop_get_slot, ":recap", "$g_talk_troop", slot_troop_home_recap),
    (str_store_string, 5, ":recap"),
  ], "{s5}", "member_anything_else", []],

[anyone, "member_background_reveal_2",
  [
    (troop_get_slot, ":first_met", "$g_talk_troop", slot_troop_first_encountered),
    (str_store_party_name, 20, ":first_met"),
    (troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
    (str_store_party_name, 21, ":home"),
    (troop_get_slot, ":recap", "$g_talk_troop", slot_troop_home_recap),
    (str_store_string, 5, ":recap"),
  ], "{s5}", "member_background_reveal_2b", []],

[anyone, "member_background_reveal_2b",
  [
    (str_store_string, 19, "str_here_plus_space"),
    (troop_get_slot, ":first_met", "$g_talk_troop", slot_troop_first_encountered),
    (str_store_party_name, 20, ":first_met"),
    (troop_get_slot, ":backstory_a", "$g_talk_troop", slot_troop_backstory_a),
    (str_store_string, 5, ":backstory_a"),
  ], "{s5}", "member_anything_else", []],

[anyone, "member_background_reveal_3",
  [
    (troop_get_slot, ":first_met", "$g_talk_troop", slot_troop_first_encountered),
    (str_store_party_name, 20, ":first_met"),
    (troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
    (str_store_party_name, 21, ":home"),
    (troop_get_slot, ":recap", "$g_talk_troop", slot_troop_home_recap),
    (str_store_string, 5, ":recap"),
  ], "{s5}", "member_background_reveal_3b", []],

[anyone, "member_background_reveal_3b",
  [
    (str_store_string, 19, "str_here_plus_space"),
    (troop_get_slot, ":first_met", "$g_talk_troop", slot_troop_first_encountered),
    (str_store_party_name, 20, ":first_met"),
    (troop_get_slot, ":backstory_a", "$g_talk_troop", slot_troop_backstory_a),
    (str_store_string, 5, ":backstory_a"),
  ], "{s5}", "member_background_reveal_3c", []],

[anyone, "member_background_reveal_3c",
  [
    (troop_get_slot, ":backstory_b", "$g_talk_troop", slot_troop_backstory_b),
    (str_store_string, 5, ":backstory_b"),
  ], "{s5}", "member_background_reveal_3d", []],

[anyone, "member_background_reveal_3d",
  [
    (troop_get_slot, ":backstory_c", "$g_talk_troop", slot_troop_backstory_c),
    (str_store_string, 5, ":backstory_c"),
  ], "{s5}", "member_anything_else", []],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. {reg11?She:He} watches too much, asks too little, and moves like someone who expects the purse to vanish the moment {reg11?she:he} blinks. I prefer a rogue who smiles when the knife is coming.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}, I am afraid. {reg11?She:He} turns every campfire into an argument and every small inconvenience into a test of pride. Trade is simpler than people; goods rarely take offense on purpose.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}, though I wish it were otherwise. {reg11?She:He} has a way of speaking that makes kindness sound foolish, and after enough days of that a person begins dreading the next conversation before it starts.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}, unquestionably. {reg11?She:He} lacks breeding, measure, and any sense that a company ought to possess standards. One can pardon low birth more easily than low conduct.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. {reg11?She:He} carries camp-sulk like a winter cloak and seems determined to share the cold with everyone nearby. I would rather ride beside a storm than a sour face that never lifts.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. I strive for patience, but {reg11?she:he} seems to treat courtesy as a weakness to be tested. Discipline can steady many faults; contempt, once made habitual, infects everything around it.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. Too loud, too sure, too eager to push into another person's shadow and call it company. I do not mind silence, but some folk hear silence and rush to fill it with themselves.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. {reg11?She:He} mistakes softness for virtue and caution for wisdom often enough to make a warrior grind {reg11?her:his} teeth. I have no quarrel with mercy; I do quarrel with spinelessness dressed in better words.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}, and not by a little. {reg11?She:He} has the gift of reducing every conversation to mud and calling the result plain dealing. There is a difference between honesty and boorishness, though some never learn it.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. Soldiers do not need to love each other, but they do need to be reliable, and {reg11?she:he} has a way of turning every small matter into needless disorder. That is a costly habit in the field.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. {reg11?She:He} can turn a mouthful of bread into a sermon and a shared chore into a slight. Life is ugly enough without someone polishing every annoyance until it shines like a grievance.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}, alas. There are ailments of the body, ailments of the mind, and then there is the chronic condition of being exhausting to live beside. I suspect no physic has yet cured the last of these.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}, my dour star. Some people drain the color out of a camp simply by standing in it. A company needs laughter now and then; {reg11?she:he} seems to regard that as moral collapse.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. I have no objection to eccentricity in the abstract, but in camp it usually arrives with noise, sloppiness, and a stubborn resistance to correction. Those are not charming defects in a soldier.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}. A badly made bridge and a badly made conversation share one defect: both collapse under the slightest strain. {reg11?She:He} has a talent for turning solvable problems into untidy spectacles.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}, easily. {reg11?She:He} makes vice look boring, which is harder to forgive than vice itself. If someone is going to be self-righteous, cruel, or tedious, I would at least ask a little style of the effort.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (store_character_level, reg11, ":clash"),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 12),
  ],
  "{s11}, without much doubt. I try to keep a civil tongue, but too much marching in close company strips the polish off everyone. There are habits a person can ignore for a few days and not for a whole campaign.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash_object),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash2_object),
    (gt, ":clash", 0),
    (main_party_has_troop, ":clash"),
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 18),
  ],
  "If I must name another, then {s11} also knows how to sour a camp. One sharp word may be nothing, but the hundredth sharp word has a way of lodging in the memory.", "member_anything_else",
  [
    (troop_get_slot, ":clash", "$g_talk_troop", slot_troop_personalityclash2_object),
    (call_script, "script_store_troop_name", s11, ":clash"),
  ]],

[anyone, "member_company_friction",
  [
    (troop_get_slot, ":grievance", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":grievance", 8),
  ],
  "There is no single villain in it. Campaign life simply rubs people raw. Small vanities become insults, old habits become provocations, and before long everyone is measuring everyone else too closely.", "member_anything_else", []],

[anyone, "member_company_friction", [],
  "No more than is usual for a marching company. Put enough tired souls under one banner and a few tempers will always grate together. Ours is not yet beyond bearing.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (troop_get_slot, ":morality_grievances", "$g_talk_troop", slot_troop_morality_penalties),
    (troop_get_slot, ":personality_grievances", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":morality_grievances", 15),
    (gt, ":morality_grievances", ":personality_grievances"),
  ],
  "What weighs on me most is not the road, but the things done upon it. A hard march can be borne. The company loses its shape when too many small choices begin to feel wrong, and a person must swallow each one in silence.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (troop_get_slot, ":morality_grievances", "$g_talk_troop", slot_troop_morality_penalties),
    (troop_get_slot, ":personality_grievances", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":personality_grievances", 15),
    (gt, ":personality_grievances", ":morality_grievances"),
  ],
  "The company itself is manageable. It is the tongues, tempers, and old grudges that sour the air. One difficult companion can darken a whole fire at night, and we have had more of that than I would like.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (call_script, "script_npc_morale", "$g_talk_troop"),
    (ge, reg0, 70),
  ],
  "At present? Not much. The company has its frictions, but they are the ordinary frictions of people who have marched long together and still mean to go on. That is about as much peace as soldiers are ever granted.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (call_script, "script_npc_morale", "$g_talk_troop"),
    (lt, reg0, 40),
  ],
  "The feeling that the strain is settling into everything. Men answer too quickly, sleep too lightly, and take every inconvenience as a personal slight. When a company reaches that state, even small troubles start drawing blood.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (troop_get_slot, ":morality_grievances", "$g_talk_troop", slot_troop_morality_penalties),
    (troop_get_slot, ":personality_grievances", "$g_talk_troop", slot_troop_personalityclash_penalties),
    (ge, ":morality_grievances", 8),
    (ge, ":personality_grievances", 8),
  ],
  "A little of everything, if I am honest. The road is hard enough on its own, and it is harder still when poor choices and poor company begin feeding each other. No single thing breaks a warband; it is the steady accumulation.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
  ],
  "If you want the truth, it is the constant need to keep one eye open. A camp is full of smiling faces, loose hands, and little lies. March long enough with people and you learn that trust is always the dearest ration.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
  ],
  "Waste, mostly. Men wear themselves thin because no one thinks ahead as carefully as they should. A company lives or dies on small matters well tended, and too many people only notice them after the loss is already paid.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
  ],
  "How quickly hardship teaches people to grow hard themselves. Hunger and fear are one thing; I expect those. What troubles me is how easily folk begin to speak cruelly, laugh cruelly, and think that is simply the way of war.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
  ],
  "The lack of standards. A proper company should carry itself with some dignity even in discomfort, but too many here seem willing to live like ditch-folk so long as they are fed and pointed toward the next fight.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
  ],
  "Stagnation. A warband should move like a live thing, quick to choose and quicker to act. The road feels sour when people keep circling the same worries until even a clear sky starts to feel like a cage.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
  ],
  "The strain between duty and bitterness. Men are asked much in a company, and that is no wrong in itself. What sits ill with me is when hardship stops feeling purposeful and begins to feel merely habitual.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
  ],
  "Too many people, too little silence. On the trail you learn more from what is not said than from what is, and a crowded camp is full of boasting, watching, and needless questions. It wears a person thin.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
  ],
  "Softness where there should be steel. I do not mind hardship, blunt speech, or a bloody road. I mind when people begin excusing weakness in themselves and calling it prudence or good sense.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
  ],
  "Pettiness. A company ought to be shaped by ambition, courage, and some notion of worth. Instead, too often, good men spend their breath on trifles and let their conduct sink beneath the station they might have claimed.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
  ],
  "Slovenly habits. Most troubles in a company are not grand tragedies; they are boots left unrepaired, watches kept poorly, gear stacked carelessly, and tempers raised because simple things were not done when they should have been.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
  ],
  "Pretense. Folk love to dress their failings up in fine excuses, but most of the time the truth is simpler: they are lazy, vain, or waiting for someone else to carry the ugly end of life for them. That gets old fast.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
  ],
  "Avoidable misery. Mud, wounds, and bad sleep are the common furniture of campaign life; I can accept that. What needles me is how much extra suffering people create through stupidity, vanity, and a heroic devotion to poor judgment.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
  ],
  "Monotony, oddly enough. Misery can be borne more easily than dreariness. A company becomes insufferable when every fire sounds the same, every grievance smells the same, and no one remembers that wit is sometimes as necessary as bread.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
  ],
  "Disorder. A body of soldiers should not need to be reminded of every standard, every formation, every duty, every single day. Nothing corrodes confidence faster than seeing the same avoidable faults return because no one has the discipline to stamp them out.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
  ],
  "Muddle. A difficult road can be measured, supplied for, and overcome. What is hard to abide is waste born of poor planning—tools not kept, tasks not thought through, and people charging at problems that would yield faster to patience and design.", "member_anything_else", []],

[anyone, "member_personal_outlook",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
  ],
  "Sanctimony. I can tolerate rough living, sharp dealing, and the occasional wicked impulse; I have known all three. What wears on me is listening to people pretend they are saints while doing the same ugly things with duller style.", "member_anything_else", []],

[anyone, "member_personal_outlook", [],
  "Nothing dramatic. It is the usual soldier's life: too much mud, too little rest, and too many people carrying private burdens they do not name. We are enduring, but endurance has a cost.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_aristocratic),
    (party_get_morale, ":party_morale", "p_main_party"),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (ge, ":party_morale", 75),
    (ge, ":food_stacks", 4),
  ],
  "I would call the company sound. The ranks are steady, the camp is supplied, and people still remember their place. Men endure hardship well enough when they see order above them and confidence beside them.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_aristocratic),
    (party_get_morale, ":party_morale", "p_main_party"),
    (lt, ":party_morale", 50),
  ],
  "Less well than I would like. Slack tempers and a worn spirit invite familiarities that soldiers should not mistake for fellowship. A company that stops carrying itself with pride soon forgets how to stand at all.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_egalitarian),
    (party_get_morale, ":party_morale", "p_main_party"),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (ge, ":party_morale", 65),
    (ge, ":food_stacks", 3),
  ],
  "Fairly well, I think. The people eat, the burdens are bearable, and no one feels entirely forgotten. A company can march a long way so long as the strong do not take everything and the weary are not left behind.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_egalitarian),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (le, ":food_stacks", 1),
  ],
  "Poorly enough that the common folk in the ranks will feel it first. Hunger always falls hardest on the ones with the least to spare. If the baggage grows any lighter, grumbling will not stay grumbling for long.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_humanitarian),
    (party_get_morale, ":party_morale", "p_main_party"),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (ge, ":party_morale", 65),
    (ge, ":food_stacks", 3),
  ],
  "Better than many companies I have seen. The men have food, the mood is not cruel, and there is still some warmth left in the campfires. Hard service is easier to bear when people are treated as more than meat for the march.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_humanitarian),
    (party_get_morale, ":party_morale", "p_main_party"),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (try_begin),
      (this_or_next|lt, ":party_morale", 50),
      (le, ":food_stacks", 1),
    (else_try),
      (eq, 1, 0),
    (try_end),
  ],
  "I worry for the company, to be plain. Empty bellies, sore feet, and a hard mood can turn decent folk into brutes. We need food, rest, and a little mercy before the road makes strangers of us all.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_honest),
    (party_get_morale, ":party_morale", "p_main_party"),
    (ge, ":party_morale", 65),
  ],
  "Well enough, because people still believe there is purpose in what we do. Soldiers will forgive cold nights and aching backs if they think the road ahead means something and their captain keeps faith with what is promised.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_honest),
    (party_get_morale, ":party_morale", "p_main_party"),
    (lt, ":party_morale", 55),
  ],
  "I would say the company is strained. When spirits sink, every promise is weighed more carefully and every hardship feels like a lie being tested. Men can endure much, but not long if they think they are being led without purpose.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_pious),
    (party_get_morale, ":party_morale", "p_main_party"),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (ge, ":party_morale", 60),
    (ge, ":food_stacks", 2),
  ],
  "Steadier than most. The company still has bread, resolve, and some sense that we are meant for more than mere survival. That is often enough to keep despair from making a home among the tents.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (troop_slot_eq, "$g_talk_troop", slot_troop_morality_type, tmt_pious),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (le, ":food_stacks", 1),
  ],
  "Want and weariness are settling over us, and such things test more than the body. Hungry men grow desperate, and desperate men begin to think only of themselves. We should mend that before necessity teaches uglier lessons.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (party_get_morale, ":party_morale", "p_main_party"),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (ge, ":party_morale", 80),
    (ge, ":food_stacks", 4),
  ],
  "Better than most warbands I have known. The camp is orderly, the packs are well stocked, and the men still look ahead with some confidence. That counts for more than banners and boasts.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (party_get_morale, ":party_morale", "p_main_party"),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (ge, ":party_morale", 65),
    (ge, ":food_stacks", 2),
  ],
  "We are holding together well enough. There is food in the baggage, discipline in the line, and not too much muttering by the fires. For a company on campaign, that is almost the same thing as comfort.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (party_get_morale, ":party_morale", "p_main_party"),
    (assign, ":food_stacks", 0),
    (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
    (try_for_range, ":slot", 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
      (is_between, ":item", food_begin, food_end),
      (val_add, ":food_stacks", 1),
    (try_end),
    (lt, ":party_morale", 45),
    (le, ":food_stacks", 1),
  ],
  "Poorly, if you want the truth of it. Empty packs and sour tempers make for a dangerous camp. Men forgive wounds more readily than hunger, and hunger is beginning to stalk us.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (party_get_morale, ":party_morale", "p_main_party"),
    (lt, ":party_morale", 55),
  ],
  "The company still follows you, but I would not call the mood easy. Too many hard miles and too little rest leave even good soldiers sharp-tongued. We should mind that before it festers.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc1"),
  ],
  "I've seen camps turn rotten faster than this one. Ours still keeps its feet under it, though I sleep better when the watches are sharp and the purses are tied tight.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc2"),
  ],
  "Reasonably sound, I would say. The company is not flourishing, but the accounts of misery have not yet exceeded the means to mend them, and that already puts us ahead of many ventures.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
  ],
  "We are enduring, and that matters. People are still speaking to one another as human beings more often than not, and while that may seem a small mercy, I do not think it is one.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
  ],
  "The company is serviceable, though not distinguished. Men are still marching, still obeying, still presenting something like a respectable front, and for now that keeps disgrace at a distance.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
  ],
  "Alive and moving, which is more than some can claim. I'd not call the mood merry, but the road is still open before us and nobody has quite forgotten how to ride it.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
  ],
  "Steady enough, if not easy. The company still has purpose in it, and purpose can carry weary people farther than comfort ever could.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
  ],
  "I've seen worse trails and worse camps. Folk still keep their eyes open, and the company still listens when it matters. That is usually enough to stay alive.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
  ],
  "Hard, but not weak. The company still has fight in it, and I would sooner ride with a hard company than a soft, smiling one waiting to break at the first true test.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
  ],
  "Adequate, though I have known companies that carried themselves with more pride. Still, there remains some ambition in the ranks, and that is preferable to mere survival.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
  ],
  "Fit for service. The line has not gone slack, the camp has not gone to complete disorder, and men still know the day has work in it. That counts for a great deal.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
  ],
  "I've known uglier outfits. People still eat, still march, still complain more than they mutiny, so by the standards of ordinary life I'd say we are doing almost grandly.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
  ],
  "Not ideal, but viable. The patient is tired rather than dying, which in campaign terms is practically excellent news.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
  ],
  "Tolerable. No one is singing, but neither are we all composing farewell speeches in the dark, and I have found that to be a useful dividing line.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
  ],
  "Capable, though not as disciplined as I would prefer. The company still functions, orders still carry, and errors remain correctable. That is enough for the moment.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc15"),
  ],
  "Operational. We are not running with elegance, but we are still running, and that separates a functioning enterprise from a heap of armed improvisation.", "member_anything_else", []],

[anyone, "member_campaign_conditions",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
  ],
  "I've lived through worse arrangements with worse company. This one still has teeth, wit, and enough appetite for tomorrow to keep from turning entirely dreary.", "member_anything_else", []],

[anyone, "member_campaign_conditions", [],
  "I have seen worse roads and worse camps. We are not thriving, perhaps, but neither are we on the edge of breaking. Keep the company paid, fed, and moving with purpose, and most will endure.", "member_anything_else", []],
]
