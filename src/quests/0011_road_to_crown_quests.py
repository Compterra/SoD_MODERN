# -*- coding: utf-8 -*-
# The Road to the Crown campaign quest slice.
# Keep quest definitions in numbered fragments and rebuild with build/build_quests.py.
#
# This first fragment intentionally implements the framework-facing quest records
# before live menu/dialogue wiring. The campaign design and implementation
# checklist track the later gameplay hooks.

QUESTS = [
 *quest_chain_from_specs(
  "campaign_road_to_the_crown",
  "The Road to the Crown",
  entry_quest_id="rtc_last_smoke",
  quests=(
   quest_template_spec(
    "rtc_last_smoke",
    "The Last Smoke",
    qf_random_quest,
    "The road behind you is smoke. Gather survivors, decide what can still be saved, and reach the refugee camp before Imperial scouts overrun the road.",
    stages=(
     quest_stage_spec(
      "rtc_last_smoke_find_survivors",
      "Find the Survivors",
      "Search the burned road for survivors.",
      description="The player finds scattered survivors on the road out of the burned homeland.",
      conditions=(
       "campaign_road_to_the_crown active",
       "act_01_ashes active",
      ),
      actions=(
       "locate survivors",
       "mark survivor group for escort",
      ),
      metadata={
       "act": "act_01_ashes",
       "chapter": "rtc_01_last_smoke",
       "phase": "opening",
      },
     ),
     quest_stage_spec(
      "rtc_last_smoke_choose_salvage",
      "Choose What Can Be Saved",
      "Choose whether to save wounded refugees, baggage, or military papers.",
      description="The player chooses the first remembered Act I outcome.",
      conditions=(
       "survivors found",
      ),
      actions=(
       "set act_01_choice_saved_wounded or act_01_choice_saved_baggage or act_01_choice_saved_papers",
       "record first mercy, supply, or intelligence bias",
      ),
      rewards=(
       "opening route memory",
      ),
      failures=(
       "abandon road fight sets companion_wary_mercy",
      ),
      metadata={
       "act": "act_01_ashes",
       "chapter": "rtc_01_last_smoke",
       "branch_point": "first_salvage_choice",
      },
     ),
     quest_stage_spec(
      "rtc_last_smoke_reach_camp",
      "Reach the Refugee Camp",
      "Escort the survivors to the refugee camp.",
      description="The player reaches the first safe camp and can continue even after a soft failure.",
      conditions=(
       "salvage choice resolved",
      ),
      actions=(
       "advance to rtc_borrowed_names",
      ),
      rewards=(
       "stop_act_01_survived",
      ),
      failures=(
       "stop_act_01_poor_start",
      ),
      metadata={
       "act": "act_01_ashes",
       "chapter": "rtc_01_last_smoke",
       "stop_success": "stop_act_01_survived",
       "stop_failure": "stop_act_01_poor_start",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_01_ashes",
     "chapter": "rtc_01_last_smoke",
     "authoring": "schema",
     "design_doc": "docs/campaigns/the_road_to_the_crown.md",
     "checklist": "docs/campaigns/the_road_to_the_crown_implementation_checklist.md",
    },
   ),
   quest_template_spec(
    "rtc_borrowed_names",
    "The Camp of Borrowed Names",
    qf_random_quest,
    "In the refugee camp, Lysara Veyne asks what name should be written beside yours. Choose the public identity Calradia will hear first.",
    stages=(
     quest_stage_spec(
      "rtc_borrowed_names_stabilize_camp",
      "Stabilize the Camp",
      "Speak with the camp witnesses and steady the refugees.",
      description="The player meets the first campaign witnesses and prepares to choose a public identity.",
      conditions=(
       "rtc_last_smoke resolved",
      ),
      actions=(
       "speak to Garran Ashwake",
       "speak to Lysara Veyne",
       "speak to Brother Odran",
      ),
      metadata={
       "act": "act_01_ashes",
       "chapter": "rtc_02_borrowed_names",
       "phase": "camp",
      },
     ),
     quest_stage_spec(
      "rtc_borrowed_names_choose_identity",
      "Choose a Public Name",
      "Choose whether Calradia first knows you as noble, captain, trader, refugee, or avenger.",
      description="This stage stores the first public reputation flag.",
      conditions=(
       "camp stabilized",
      ),
      actions=(
       "set one reputation flag",
       "record witness reactions",
       "advance to rtc_hound_sign",
      ),
      rewards=(
       "reputation_foreign_noble or reputation_free_captain or reputation_trade_operator or reputation_refugee or reputation_avenger",
      ),
      metadata={
       "act": "act_01_ashes",
       "chapter": "rtc_02_borrowed_names",
       "branch_point": "public_identity_choice",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_01_ashes",
     "chapter": "rtc_02_borrowed_names",
     "authoring": "schema",
    },
   ),
   quest_template_spec(
    "rtc_hound_sign",
    "Hound Sign",
    qf_random_quest,
    "Investigate the first proof that Legate Gaius Marius, the Imperial Hound, is moving toward Calradia.",
    stages=(
     quest_stage_spec(
      "rtc_hound_sign_find_evidence",
      "Find Imperial Evidence",
      "Find a courier seal, burned route map, survivor testimony, ration token, or coded pacification order.",
      description="The player gathers the first evidence of Imperial pressure.",
      conditions=(
       "rtc_borrowed_names resolved",
      ),
      actions=(
       "investigate road evidence",
       "record evidence type",
      ),
      metadata={
       "act": "act_01_ashes",
       "chapter": "rtc_03_hound_sign",
       "phase": "investigation",
      },
     ),
     quest_stage_spec(
      "rtc_hound_sign_interpret_warning",
      "Interpret the Warning",
      "Use honor, intrigue, counsel, or trade knowledge to understand the Imperial threat.",
      description="The player earns a method seed or continues with weak evidence.",
      conditions=(
       "imperial evidence found or missed",
      ),
      actions=(
       "set imperial_pressure_low",
       "set method seed when evidence is strong",
       "advance to Act II",
      ),
      rewards=(
       "imperial_pressure_low",
      ),
      failures=(
       "weak evidence delays later preparation but campaign continues",
      ),
      metadata={
       "act": "act_01_ashes",
       "chapter": "rtc_03_hound_sign",
       "stop_success": "stop_act_01_survived",
       "stop_failure": "stop_act_01_poor_start",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_01_ashes",
     "chapter": "rtc_03_hound_sign",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
   "rtc_door_into_calradia",
   "A Door Into Calradia",
   qf_random_quest,
   "The refugee road reaches Calradia, but arrival is not acceptance. Choose the first door you try to open: court, contract, command, village, or road.",
   stages=(
    quest_stage_spec(
     "rtc_door_into_calradia_choose_contact",
     "Choose a First Contact",
     "Approach a noble patron, guild contact, gate captain, village representative, or road scout.",
     description="The player chooses the first social access route into Calradia.",
     conditions=(
      "act_02_choice active",
      "rtc_hound_sign resolved",
     ),
     actions=(
      "choose first Calradian contact",
      "set noble, merchant, commoner, or route trust",
     ),
     metadata={
      "act": "act_02_choice",
      "chapter": "rtc_04_door_into_calradia",
      "branch_point": "first_calradian_contact",
     },
    ),
    quest_stage_spec(
     "rtc_door_into_calradia_secure_witness",
     "Secure a Witness",
     "Gain a first witness who can explain what you are in Calradia.",
     description="The selected contact becomes the first Act II social witness.",
     conditions=(
      "first contact chosen",
     ),
     actions=(
      "record first social witness",
      "advance to rtc_price_of_bread",
     ),
     rewards=(
      "social access established",
     ),
     failures=(
      "unproven social entry",
     ),
     metadata={
      "act": "act_02_choice",
      "chapter": "rtc_04_door_into_calradia",
      "stop_success": "stop_act_02_social_entry_seeded",
     },
    ),
   ),
   metadata={
    "category": "campaign",
    "campaign": "campaign_road_to_the_crown",
    "act": "act_02_choice",
    "chapter": "rtc_04_door_into_calradia",
    "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_price_of_bread",
    "The Price of Bread",
    qf_random_quest,
    "Refugees need grain, but the local village is hungry too. Resolve the dispute before hunger becomes violence.",
    stages=(
     quest_stage_spec(
      "rtc_price_of_bread_hear_dispute",
      "Hear the Grain Dispute",
      "Speak with Tamsin Reedhand, Celeste di Marina, and Brother Odran about the grain crisis.",
      description="The first Act II pressure test reads the Act I state and presents a resource conflict.",
      conditions=(
       "act_02_choice active",
      ),
      actions=(
       "hear village position",
       "hear merchant position",
       "hear mercy position",
      ),
      metadata={
       "act": "act_02_choice",
       "chapter": "rtc_05_price_of_bread",
       "phase": "pressure_test",
       "world_target": "nearest hungry village or first Act II village witness",
       "world_action": "hear local, merchant, and mercy accounts of the grain crisis",
       "witness": "Tamsin Reedhand, Celeste di Marina, and Brother Odran",
       "failure_mode": "witnesses disagree or crisis advances without enough trust",
       "cleanup": "clear temporary speaker pressure after resolution",
       "result_grade": "unresolved until grain resolution is chosen",
      },
     ),
     quest_stage_spec(
      "rtc_price_of_bread_resolve",
      "Resolve the Price of Bread",
      "Pay fairly, negotiate labor, expose hoarding, requisition by force, or raid bandit stores.",
      description="The resolution sets the first commoner, merchant, noble, or fear pressure flags.",
      conditions=(
       "grain dispute heard",
      ),
      actions=(
       "set commoner_trust_high or commoner_trust_low",
       "set merchant_trust_high or merchant_trust_low",
       "set village_fear if requisitioned by force",
       "record hunger pressure on failure",
      ),
      rewards=(
       "trust profile established",
      ),
      failures=(
       "hunger pressure remains",
      ),
      metadata={
       "act": "act_02_choice",
       "chapter": "rtc_05_price_of_bread",
       "branch_point": "grain_resolution",
       "world_target": "grain village, merchant broker, or bandit stores target",
       "world_action": "pay, bargain, expose hoarding, requisition, raid stores, or move on hungry",
       "witness": "local hunger, merchant logistics, and mercy witness",
       "failure_mode": "hunger pressure remains, village fear rises, or a later physical bandit target escapes",
       "cleanup": "copy trust/pressure flags forward and clear or resolve any grain target party",
       "result_grade": "poor for hunger/force, standard for fair pay or hoarding exposure, ideal for balanced labor or successful bandit-store relief",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_02_choice",
     "chapter": "rtc_05_price_of_bread",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_three_offers",
    "Three Offers",
    qf_random_quest,
    "After the first Calradian tests, three public offers and one hidden road try to shape what your claim will become.",
    stages=(
     quest_stage_spec(
      "rtc_three_offers_hear_terms",
      "Hear the Offers",
      "Hear noble protection, paid steel, the people's road, a hard claim, and the quiet ledger.",
      description="The player sees the first Act III route seeds opened by early reputation and trust.",
      conditions=(
       "rtc_price_of_bread resolved",
      ),
      actions=(
       "evaluate noble, mercenary, coalition, conquest, and hidden offers",
       "gate offers by reputation, trust, social contact, method seed, and fear where implementation supports it",
      ),
      metadata={
       "act": "act_03_standing",
       "chapter": "rtc_07_three_offers",
       "phase": "route_seed",
      },
     ),
     quest_stage_spec(
      "rtc_three_offers_choose_route",
      "Choose the First Route",
      "Choose the first route seed for the claim.",
      description="The selected offer sets exactly one primary branch seed and may set a modifier flag.",
      conditions=(
       "offers heard",
      ),
      actions=(
       "set branch_legitimacy or branch_mercenary or branch_conquest or branch_coalition",
       "optionally set branch_reform, branch_betrayal, or branch_hidden_regime_maker",
       "advance to rtc_companions_take_sides",
      ),
      rewards=(
       "primary route seed",
      ),
      failures=(
       "fractured claim if no offer can hold",
      ),
      metadata={
       "act": "act_03_standing",
       "chapter": "rtc_07_three_offers",
       "branch_point": "act_03_primary_route_seed",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_03_standing",
     "chapter": "rtc_07_three_offers",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_companions_take_sides",
    "Companions Take Sides",
    qf_random_quest,
    "The company reacts to the route you have chosen. Some companions see a future; others see the first crack before a crown.",
    stages=(
     quest_stage_spec(
      "rtc_companions_take_sides_campfire",
      "Hold the Campfire",
      "Let companions answer the chosen route seed.",
      description="Companions approve, warn, or near-fracture based on the selected route and their approval state.",
      conditions=(
       "rtc_three_offers route seeded",
      ),
      actions=(
       "record at least one approval reaction",
       "record at least one warning reaction",
       "record near-fracture condition when trust is low",
      ),
      metadata={
       "act": "act_03_standing",
       "chapter": "rtc_08_companions_take_sides",
       "phase": "company_reaction",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_03_standing",
     "chapter": "rtc_08_companions_take_sides",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_first_recognition",
    "First Recognition",
    qf_random_quest,
    "Calradia gives the claim its first public name: lawful claimant, free captain, trade power, people's defender, dangerous warlord, or shadow operator.",
    stages=(
     quest_stage_spec(
      "rtc_first_recognition_name_claim",
      "Name the Claim",
      "Resolve how the first outside witnesses describe your route.",
      description="The campaign converts the seeded route into a first public recognition label.",
      conditions=(
       "companions_take_sides resolved",
      ),
      actions=(
       "recognize lawful claimant, free captain, trade power, people's defender, dangerous warlord, or shadow operator",
       "prepare route lock for Crown Council",
      ),
      metadata={
       "act": "act_03_standing",
       "chapter": "rtc_09_first_recognition",
       "phase": "public_recognition",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_03_standing",
     "chapter": "rtc_09_first_recognition",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_crown_council",
    "Crown Council",
    qf_random_quest,
    "Gather witnesses and answer the first direct challenge to your authority. The council can lock a crown route or fracture the claim before Act V.",
    stages=(
     quest_stage_spec(
      "rtc_crown_council_gather_witnesses",
      "Gather the Witnesses",
      "Bring or simulate noble, commoner, company, and fourth witnesses before the council.",
      description="The council checks whether the claim has enough support categories to survive public challenge.",
      conditions=(
       "first recognition resolved",
      ),
      actions=(
       "require noble or faction witness",
       "require commoner or village witness",
       "require companion or company witness",
       "require faith, scholar, merchant, or military witness",
      ),
      metadata={
       "act": "act_04_crown",
       "chapter": "rtc_10_crown_council",
       "phase": "witness_check",
      },
     ),
     quest_stage_spec(
      "rtc_crown_council_answer_challenge",
      "Answer Maeron's Challenge",
      "Answer Maeron Vald, Septima Varro, and Vaska without losing the route.",
      description="The council turns the Act III route seed into an Act IV route lock or a fractured-claim failure.",
      conditions=(
       "witnesses gathered",
      ),
      actions=(
       "lock legitimacy, mercenary, conquest, coalition, restoration, imperial, or hidden regime-maker branch",
       "fail into fractured claim when witness support is too weak",
      ),
      rewards=(
       "stop_act_04_branch_locked",
      ),
      failures=(
       "stop_act_04_fractured_claim",
      ),
      metadata={
       "act": "act_04_crown",
       "chapter": "rtc_10_crown_council",
       "branch_point": "act_04_route_lock",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_04_crown",
     "chapter": "rtc_10_crown_council",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_hounds_terms",
    "The Hound's Terms",
    qf_random_quest,
    "The Imperial Hound sends terms after the Crown Council. Accept, reject, delay, or let the talks collapse.",
    stages=(
     quest_stage_spec(
      "rtc_hounds_terms_receive",
      "Receive the Terms",
      "Hear the terms Marius or Septima offers according to the locked branch.",
      description="The first Act V crisis reads the Act IV branch lock and Imperial pressure.",
      conditions=(
       "crown council route locked",
      ),
      actions=(
       "show Marius or Septima terms by branch",
       "carry locked route into Act V",
      ),
      metadata={
       "act": "act_05_shadow",
       "chapter": "rtc_11_hounds_terms",
       "phase": "imperial_terms",
      },
     ),
     quest_stage_spec(
      "rtc_hounds_terms_answer",
      "Answer the Hound",
      "Reject, negotiate delay, accept, or let talks collapse.",
      description="The answer determines whether the campaign moves toward open Imperial conflict, accommodation, delay, or collapse.",
      conditions=(
       "terms received",
      ),
      actions=(
       "set terms rejected, negotiated, accepted, or collapsed",
       "raise imperial pressure",
       "prepare Act V follow-up",
      ),
      rewards=(
       "imperial resolution seed",
      ),
      failures=(
       "talks collapse into fractured claim pressure",
      ),
      metadata={
       "act": "act_05_shadow",
       "chapter": "rtc_11_hounds_terms",
       "branch_point": "imperial_terms_answer",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_05_shadow",
     "chapter": "rtc_11_hounds_terms",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_war_of_witnesses",
    "War of Witnesses",
    qf_random_quest,
    "Marius turns from terms to witnesses. Protect, exploit, sacrifice, or redirect the people whose support made the crown possible.",
    stages=(
     quest_stage_spec(
      "rtc_war_of_witnesses_choose_target",
      "Choose the Witness War",
      "Identify which witness target the Empire threatens according to the locked route.",
      description="The witness war presents route-specific targets: court witnesses, payroll roads, vanguards, allies, homeland survivors, Imperial loyalty tests, or ledger witnesses.",
      conditions=(
       "hounds terms answered",
      ),
      actions=(
       "select witness protection target",
       "frame route-specific target variant",
      ),
      metadata={
       "act": "act_05_shadow",
       "chapter": "rtc_12_war_of_witnesses",
       "phase": "witness_war",
      },
     ),
     quest_stage_spec(
      "rtc_war_of_witnesses_resolve",
      "Resolve the Witness War",
      "Protect witnesses, use the route's strongest answer, hand off to the Last Banner of the East, or sacrifice a witness.",
      description="The result determines whether witness legitimacy survives into the final road.",
      conditions=(
       "witness target selected",
      ),
      actions=(
       "protect witness",
       "sacrifice witness",
       "apply route-specific target variant",
       "record side-crisis handoff",
      ),
      rewards=(
       "witnesses preserved or route strengthened",
      ),
      failures=(
       "witness sacrificed and trust damaged",
      ),
      metadata={
       "act": "act_05_shadow",
       "chapter": "rtc_12_war_of_witnesses",
       "branch_point": "witness_survival",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_05_shadow",
     "chapter": "rtc_12_war_of_witnesses",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_last_road",
    "The Last Road",
    qf_random_quest,
    "Choose the final strategy against the Imperial Hound: hold, strike, starve, expose, submit, or collapse.",
    stages=(
     quest_stage_spec(
      "rtc_last_road_choose_strategy",
      "Choose the Final Strategy",
      "Choose how the locked crown route answers the Imperial army.",
      description="The final strategy converts Act V pressure into a confrontation posture.",
      conditions=(
       "war of witnesses resolved",
      ),
      actions=(
       "choose hold the line, strike the Hound, starve the Empire, break the seal, accept the collar, or catastrophic loss",
      ),
      metadata={
       "act": "act_05_shadow",
       "chapter": "rtc_13_last_road",
       "phase": "final_strategy",
      },
     ),
     quest_stage_spec(
      "rtc_last_road_resolve_strategy",
      "Resolve the Last Road",
      "Record the final strategy that will shape the confrontation with Marius.",
      description="The result sets final confrontation posture or fails into catastrophic loss.",
      conditions=(
       "final strategy chosen",
      ),
      actions=(
       "record final strategy seed",
       "adjust imperial pressure",
       "prepare final confrontation",
      ),
      rewards=(
       "final confrontation seed",
      ),
      failures=(
       "catastrophic loss",
      ),
      metadata={
       "act": "act_05_shadow",
       "chapter": "rtc_13_last_road",
       "branch_point": "final_strategy",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_05_shadow",
     "chapter": "rtc_13_last_road",
     "authoring": "schema",
   },
  ),
  quest_template_spec(
    "rtc_final_confrontation",
    "Final Confrontation",
    qf_random_quest,
    "Resolve Marius, the Empire, and the crown road: defeat, force back, submit, refuse personal rule, or collapse.",
    stages=(
     quest_stage_spec(
      "rtc_final_confrontation_face_marius",
      "Face Marius",
      "Bring the final strategy to its confrontation with the Imperial Hound.",
      description="The final confrontation reads the Last Road strategy and presents the campaign's first ending posture.",
      conditions=(
       "last road strategy resolved",
      ),
      actions=(
       "face Marius or his command",
       "resolve imperial pressure",
      ),
      metadata={
       "act": "act_05_shadow",
       "chapter": "rtc_14_final_confrontation",
       "phase": "final_confrontation",
      },
     ),
     quest_stage_spec(
      "rtc_final_confrontation_resolve",
      "Resolve the Crown",
      "Defeat Marius, force him back, accept him as overlord, reject personal rule, or let the claim collapse.",
      description="This closes the campaign spine, archives one primary ending, and records the follow-up arc opened by the result.",
      conditions=(
       "Marius confronted",
      ),
      actions=(
       "record final outcome",
       "archive final branch seed for endings",
      ),
      rewards=(
       "campaign resolution seed",
      ),
      failures=(
       "claim collapse",
      ),
      metadata={
       "act": "act_05_shadow",
       "chapter": "rtc_14_final_confrontation",
       "branch_point": "final_outcome",
      },
     ),
    ),
    metadata={
     "category": "campaign",
     "campaign": "campaign_road_to_the_crown",
     "act": "act_05_shadow",
     "chapter": "rtc_14_final_confrontation",
     "authoring": "schema",
   },
  ),
  ),
  metadata={
   "category": "campaign",
   "campaign": "campaign_road_to_the_crown",
   "authoring": "schema",
   "implementation_slice": "campaign_spine_to_endings",
   "branch_tree": "docs/campaigns/the_road_to_the_crown.md#branch-tree-and-stop-map",
  },
 ).as_legacy_tuples(),
]
