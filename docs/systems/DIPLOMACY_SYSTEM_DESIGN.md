# Ponavosa Diplomacy System Checklist

## Goal

Build a diplomacy system for Ponavosa's non-Warband Module System layout. The system should make realms feel politically distinct, give the player meaningful ruler choices, connect mini-factions to world politics, and keep the Imperial Expeditionary Force as a special endgame exception.

## Design Rules

- [x] Diplomacy is more than war and peace.
- [x] Every treaty, decree, or policy has a benefit and a cost.
- [x] Kingdoms have political personality, not only troop identity.
- [x] Mini-factions influence diplomacy without becoming normal kingdoms.
- [x] `fac_kingdom_6` remains outside normal diplomacy.
- [x] Reports and faction notes explain the system in-game.
- [x] Implementation follows the repo's generated Python structure.
- [x] Static tests cover every new slot, script, menu, and trigger hook.

## Phase 1: Core Diplomatic State

### Constants and Slots

- [x] Add faction diplomatic slots.
  - [x] `slot_faction_diplomacy_temperament`
  - [x] `slot_faction_diplomacy_legitimacy`
  - [x] `slot_faction_diplomacy_fear`
  - [x] `slot_faction_diplomacy_grievance`
  - [x] `slot_faction_diplomacy_war_weariness`
  - [x] `slot_faction_diplomacy_trade_interest`
  - [x] `slot_faction_diplomacy_honor_stance`
  - [x] `slot_faction_diplomacy_slavery_stance`
  - [x] `slot_faction_diplomacy_border_stance`
  - [x] `slot_faction_diplomacy_religious_stance`
  - [x] `slot_faction_diplomacy_current_crisis`
  - [x] `slot_faction_diplomacy_last_envoy_day`
  - [x] `slot_faction_diplomacy_last_treaty_day`

- [x] Add diplomacy enum constants.
  - [x] Temperaments: expansionist, defensive, mercantile, honor-bound, predatory, isolationist, opportunist, anti-Imperial.
  - [x] Crisis states: none, Imperial, Black Khergit, Slaver, famine, succession, multi-war.
  - [x] Memory types: border raid, broken truce, released lord, executed lord, caravan attack, captive freeing, Slaver cooperation, anti-Imperial aid, shared enemy, tribute accepted, tribute refused.

### Initialization

- [x] Add `script_sod_diplomacy_initialize`.
- [x] Assign default temperament to each normal kingdom.
- [x] Assign default legitimacy/fear/grievance/war weariness values.
- [x] Assign default slavery, border, honor, trade, and religious stances.
- [x] Exclude `fac_kingdom_6` from normal diplomacy defaults or mark it with an Imperial exception temperament.
- [x] Hook initialization into the current startup/init flow.

### State Update

- [x] Add `script_sod_diplomacy_update_realm_state`.
- [x] Recalculate diplomatic values daily or weekly.
- [x] Clamp all public-facing values to readable ranges.
- [x] Make badboy/infamy feed into diplomacy state.
- [x] Make right-to-rule/legitimacy feed into diplomacy state.

### Acceptance Criteria

- [x] New constants compile.
- [x] New initialization script exists and is referenced.
- [x] Each normal kingdom receives readable defaults.
- [x] `fac_kingdom_6` is visibly treated as an exception.
- [x] Static test verifies slot and script presence.

## Phase 2: Relationship Memory

### Memory API

- [x] Add `script_sod_diplomacy_apply_memory`.
- [x] Add `script_sod_diplomacy_get_memory_score`.
- [x] Add `script_sod_diplomacy_decay_memories`.
- [x] Support player-kingdom memories first.
- [x] Keep storage compact and readable.

### Memory Events

- [x] Apply memory when a truce is broken.
- [x] Apply memory when a lord is released.
- [x] Apply memory when a lord is executed.
- [x] Apply memory when villages are raided.
- [x] Apply memory when caravans are attacked.
- [x] Apply memory when captives are freed.
- [x] Apply memory when player cooperates with Slavers.
- [x] Apply memory when player fights Slavers.
- [x] Apply memory when player aids anti-Imperial defense.
- [x] Apply memory when tribute is accepted or refused.

### Acceptance Criteria

- [x] Memories change treaty acceptance scores.
- [x] Memories appear in diplomatic reports.
- [x] Memory decay prevents permanent lock-in except for major betrayals.
- [x] Static test verifies memory scripts and at least five hook references.

## Phase 3: War Reasons and War Weariness

### War Reasons

- [x] Add war reason constants.
  - [x] Border dispute.
  - [x] Retaliation.
  - [x] Conquest.
  - [x] Religious hostility.
  - [x] Slaver outrage.
  - [x] Imperial crisis.
  - [x] Badboy containment.
  - [x] Trade route conflict.
  - [x] Broken treaty.
  - [x] Black Khergit pressure.
  - [x] Mercenary pact obligation.

- [x] Add faction or pair-scoped storage for current war reason.
- [x] Update war-start scripts to assign a reason.
- [x] Update faction notes to display war reasons.

### War Weariness

- [x] Add `script_sod_diplomacy_update_war_weariness`.
- [x] Increase weariness from long wars.
- [x] Increase weariness from lost battles.
- [x] Increase weariness from lost centers.
- [x] Increase weariness from raided villages.
- [x] Increase weariness from captured lords.
- [x] Increase weariness from multiple simultaneous wars.
- [x] Reduce weariness after victories.
- [x] Reduce weariness during peace.
- [x] Reduce weariness through reconstruction policies/decrees.

### Peace Pressure

- [x] Make war weariness improve peace acceptance.
- [x] Make high war weariness reduce campaign aggression.
- [x] Make high war weariness worsen lord discontent.
- [x] Make exhausted realms more vulnerable to mini-faction pressure.

### Acceptance Criteria

- [x] Starting a war records a reason.
- [x] War reason appears in a report or faction note.
- [x] War weariness rises and falls through scripted events.
- [x] Peace scoring references war weariness.
- [x] Static test verifies war reason constants and weariness script.

## Phase 4: Treaty System

### Treaty Records

- [x] Add compact treaty slots.
  - [x] `slot_faction_treaty_partner_1`
  - [x] `slot_faction_treaty_type_1`
  - [x] `slot_faction_treaty_until_day_1`
  - [x] `slot_faction_treaty_strength_1`
  - [x] Repeat for 4 to 6 treaty records.

- [x] Add treaty type constants.
  - [x] Truce.
  - [x] Non-aggression pact.
  - [x] Trade accord.
  - [x] Military access.
  - [x] Defensive pact.
  - [x] Anti-invasion league.
  - [x] Tributary arrangement.
  - [x] Prisoner exchange.
  - [x] Anti-slaver compact.
  - [x] Border security pact.

### Treaty Scripts

- [x] Add `script_sod_diplomacy_score_treaty`.
- [x] Add `script_sod_diplomacy_apply_treaty`.
- [x] Add `script_sod_diplomacy_find_treaty_slot`.
- [x] Add `script_sod_diplomacy_expire_treaties`.
- [x] Add `script_sod_diplomacy_break_treaty`.
- [x] Add `script_sod_diplomacy_describe_treaty_to_sXX`.

### Treaty Effects

- [x] Truce blocks war declaration for duration.
- [x] Non-aggression pact heavily discourages war.
- [x] Trade accord improves prosperity/trade relation.
- [x] Military access reduces border incidents.
- [x] Defensive pact creates limited shared-war pressure.
- [x] Anti-invasion league coordinates against `fac_kingdom_6`.
- [x] Tributary arrangement transfers denars or reduces hostility.
- [x] Prisoner exchange releases nobles or reduces grievance.
- [x] Anti-slaver compact reduces Slaver market tolerance.
- [x] Border security pact increases patrol behavior.

### Acceptance Criteria

- [x] Treaties are stored, described, and expired.
- [x] Treaty acceptance uses scoring.
- [x] Breaking treaties creates memory and badboy.
- [x] `fac_kingdom_6` cannot receive normal treaties.
- [x] Static test verifies treaty slots, scripts, and Imperial exclusion.

## Phase 5: Envoys and Chancellor Actions

### Envoy System

- [x] Add `script_sod_diplomacy_send_envoy`.
- [x] Add `script_sod_diplomacy_resolve_envoy`.
- [x] Track envoy cooldown with `slot_faction_diplomacy_last_envoy_day`.
- [x] Use companion persuasion or Chancellor skill where available.
- [x] Make envoy travel abstract in v1.

### Player Actions

- [x] Propose peace.
- [x] Declare formal war.
- [x] Offer tribute.
- [x] Demand tribute.
- [x] Request non-aggression pact.
- [x] Request trade accord.
- [x] Request military access.
- [x] Request defensive pact.
- [x] Request anti-invasion league membership.
- [x] Propose prisoner exchange.
- [x] Request joint action against Slavers.
- [x] Request joint action against Black Khergits.
- [x] Publicly denounce a faction.

### Envoy Outcomes

- [x] Accepted.
- [x] Rejected politely.
- [x] Rejected with relation loss.
- [x] Counteroffer requested.
- [x] Envoy insulted.
- [x] Envoy detained in extreme cases.

### Acceptance Criteria

- [x] Chancellor or camp menu exposes envoy actions.
- [x] Envoy scoring references relation, ruler relation, legitimacy, fear, honor, badboy, memory, relative strength, war weariness, and faction temperament.
- [x] Result messages are concise.
- [x] Static test verifies envoy scripts and menu entries.

## Phase 6: Realm Policies

### Policy Slots

- [x] Add policy slots or reuse a clean slot range.
  - [x] Cultural focus.
  - [x] Border control.
  - [x] Slavery law.
  - [x] Military service.
  - [x] Justice.
  - [x] Reconstruction.

### Policy Options

- [x] Cultural focus supports trade, balanced, and military.
- [x] Border control supports open, guarded, and sealed.
- [x] Slavery law supports banned, tolerated, regulated, and accepted.
- [x] Military service supports volunteer, levy, conscription, and forced levy.
- [x] Justice supports merciful, balanced, severe, and terror law.
- [x] Reconstruction supports austerity, normal, rebuilding, and relief.

### Policy Effects

- [x] Cultural focus affects tariffs, prosperity recovery, construction speed, campaign tolerance, and army size.
- [x] Border control affects trade, relations, patrols, raider infiltration, Black Khergit pressure, and caravan safety.
- [x] Slavery law affects Slaver market strength, honor, labor discounts, Jotnar reaction, and underworld access.
- [x] Military service affects recruit count, recruit tier, village relation, prosperity, and lord support.
- [x] Justice affects honor, fear, banditry, lord relation, and legitimacy.
- [x] Reconstruction affects village recovery, health, prosperity, treasury cost, and war capacity.

### Scripts

- [x] Add `script_sod_diplomacy_recalculate_policy_effects`.
- [x] Add `script_sod_diplomacy_apply_policy_change`.
- [x] Add `script_sod_diplomacy_describe_policy_to_sXX`.
- [x] Add policy effects to daily or weekly processing.

### Acceptance Criteria

- [x] Policies can be read in a report.
- [x] Policies produce at least one visible gameplay effect each.
- [x] Slavery and border policies connect to existing mini-faction systems.
- [x] Static test verifies policy constants, scripts, and report text.

## Phase 7: Royal Decrees

### Decree Slots

- [x] Add decree active/inactive slots.
- [x] Add decree start day slots if minimum duration is needed.
- [x] Add decree cooldown slots if needed.

### Decrees

- [x] War Taxes.
- [x] Emergency Conscription.
- [x] Road Patrol Mandate.
- [x] Anti-Slaver Edict.
- [x] Imperial Defense Mobilization.
- [x] Caravan Protection Charter.
- [x] Fortress Restoration Order.
- [x] Grain Relief.
- [x] Public Executions.
- [x] Amnesty for Deserters.

### Scripts

- [x] Add `script_sod_diplomacy_apply_decree`.
- [x] Add `script_sod_diplomacy_repeal_decree`.
- [x] Add `script_sod_diplomacy_process_decrees`.
- [x] Add `script_sod_diplomacy_describe_decree_to_sXX`.

### Decree Rules

- [x] Each decree has a cost or upkeep.
- [x] Each decree has a visible benefit.
- [x] Each decree has a visible consequence.
- [x] Each decree has a minimum duration before repeal.
- [x] Each decree appears in reports and faction notes where relevant.

### Acceptance Criteria

- [x] Player can enable and disable v1 decrees.
- [x] War taxes affect income/prosperity.
- [x] Reconstruction affects recovery.
- [x] Anti-Slaver Edict affects Slaver heat/market strength.
- [x] Road Patrol Mandate affects patrol/security pressure.
- [x] Static test verifies decree constants, scripts, and menu entries.

## Phase 8: Reports and Notes

### Realm Governance Report

- [x] Add `mnu_sod_realm_governance_report`.
- [x] Show legitimacy.
- [x] Show fear.
- [x] Show honor.
- [x] Show badboy.
- [x] Show current policies.
- [x] Show active decrees.
- [x] Show treasury pressure.
- [x] Show war weariness.
- [x] Show patrol coverage.
- [x] Show Slaver influence.
- [x] Show border threat.
- [x] Show Imperial crisis status.

### Diplomatic Report

- [x] Add `mnu_sod_diplomatic_report`.
- [x] Show relation per realm.
- [x] Show current treaty per realm.
- [x] Show war reason per realm.
- [x] Show war weariness per realm.
- [x] Show strength estimate.
- [x] Show ruler attitude.
- [x] Show shared enemies.
- [x] Show recent memory.
- [x] Show treaty acceptance estimate.

### Crisis Report

- [x] Add `mnu_sod_crisis_diplomacy_report`.
- [x] Show Imperial Expedition status.
- [x] Show Black Khergit horde target.
- [x] Show Slaver market heat.
- [x] Show Jotnar hearth pressure.
- [x] Show major mini-faction activity.

### Faction Notes

- [x] Add diplomacy status to faction notes.
- [x] Add political temperament.
- [x] Add current wars and reasons.
- [x] Add current treaties.
- [x] Add war weariness.
- [x] Add policy identity.
- [x] Add slavery stance.
- [x] Add border stance.
- [x] Add crisis stance.
- [x] Add player reputation summary.

### Acceptance Criteria

- [x] Reports are reachable from camp or ruler menus.
- [x] Faction notes summarize diplomacy without excessive text.
- [x] Crisis report references current mini-faction systems.
- [x] Static test verifies report menus and faction-note text.

## Phase 9: Mini-Faction Diplomacy Hooks

### Slavers

- [x] Slavery policy modifies Slaver market strength.
- [x] Anti-Slaver Edict raises heat and reduces market safety.
- [x] Accepted slavery increases Slaver access and labor discounts.
- [x] Anti-slaver actions improve honor and Jotnar standing.
- [x] Slaver cooperation damages honor and anti-slaver relations.

### Jotnar Clan

- [x] Jotnar approve anti-slaver laws.
- [x] Jotnar approve refugee support.
- [x] Jotnar approve mercy and captive freeing.
- [x] Jotnar disapprove selling captives.
- [x] Jotnar disapprove predatory border policies.
- [x] Jotnar hearth pressure appears in crisis diplomacy.

### Elephant Guard

- [x] Elephant Guard respect legitimacy.
- [x] Elephant Guard respect honor.
- [x] Elephant Guard distrust terror law.
- [x] Elephant Guard distrust reckless conquest.
- [x] Elephant Guard support can improve prestige or center defense.

### Black Khergits

- [x] Border policy changes Black Khergit harassment pressure.
- [x] Patrol mandates reduce local horde pressure.
- [x] Player bribes to redirect horde create diplomatic memory.
- [x] Realms can request aid against the horde camp.
- [x] Trade-focused kingdoms suffer more from horde pressure.

### Other Threat Groups

- [x] Black Army activity can influence road security.
- [x] Serpent Host reports can feed crisis intelligence.
- [x] Boar Clan pressure can affect trade-route conflict.

### Acceptance Criteria

- [x] At least Slavers, Jotnar, and Black Khergits are wired in v1.
- [x] Mini-faction hooks affect diplomacy without creating normal treaties.
- [x] Crisis report displays mini-faction diplomatic pressure.
- [x] Static test verifies hook references.

## Phase 10: Imperial Expeditionary Force Exception

### Rules

- [x] `fac_kingdom_6` is always hostile to settled kingdoms.
- [x] `fac_kingdom_6` cannot receive normal peace.
- [x] `fac_kingdom_6` cannot receive normal treaties.
- [x] `fac_kingdom_6` cannot hire normal mercenaries.
- [x] `fac_kingdom_6` can use only dedicated Imperial auxiliaries.
- [x] Imperial ruler death remains gated behind vassal commander deaths.

### Special Diplomacy

- [x] Add or preserve anti-Imperial league support.
- [x] Add sabotage supply as special crisis action.
- [x] Add rally frontier defense as special crisis action.
- [x] Add emergency truce pressure between native realms.
- [x] Add Imperial intelligence line to reports.

### Acceptance Criteria

- [x] Normal envoy/treaty menus hide invalid Imperial options.
- [x] Reports explain why normal diplomacy does not apply.
- [x] Anti-Imperial league can target only Imperial crisis behavior.
- [x] Static test verifies all Imperial exclusions.

## Phase 11: AI Diplomacy

### Weekly AI Pulse

- [x] Add `script_sod_diplomacy_ai_weekly_pulse`.
- [x] Update war weariness.
- [x] Update grievances.
- [x] Score current enemies.
- [x] Score possible peace.
- [x] Score treaty opportunities.
- [x] React to crisis threats.
- [x] Adjust patrol/reconstruction posture.

### AI Personality Effects

- [x] Expansionist lowers war threshold.
- [x] Defensive raises border security and peace preference.
- [x] Mercantile prefers trade accords and open borders.
- [x] Honor-bound dislikes slavery and broken treaties.
- [x] Predatory tolerates Slavers and tribute demands.
- [x] Isolationist dislikes access treaties and foreign entanglements.
- [x] Opportunist attacks weak/exhausted targets.
- [x] Anti-Imperial prioritizes invasion response.

### Acceptance Criteria

- [x] AI kingdoms can prefer different diplomatic choices.
- [x] AI diplomacy does not spam world messages.
- [x] AI cannot break Imperial exception rules.
- [x] Static test verifies AI pulse hook.

## Phase 12: UI and Player Flow

### Menu Access

- [x] Add diplomacy entry to camp reports.
- [x] Add governance report entry when player is a ruler.
- [x] Add envoy action entry when player has a Chancellor/minister or valid ruler status.
- [x] Add policy management entry when player rules a kingdom.
- [x] Add decree management entry when player rules a kingdom.

### Text Standards

- [x] Keep reports concise.
- [x] Avoid walls of flavor text in menus.
- [x] Use numerical summaries where helpful.
- [x] Explain tradeoffs before confirming a policy or decree.
- [x] Show cooldowns and costs before actions are selected.

### Acceptance Criteria

- [x] Player can understand current diplomacy state from camp menus.
- [x] Player can act without needing external documentation.
- [x] No report option appears when it cannot function.
- [x] Static test verifies menu reachability.

## Phase 13: Testing

### Static Tests

- [x] Add `build/test_diplomacy_system_static.py`.
- [x] Test diplomacy slots/constants exist.
- [x] Test treaty scripts exist.
- [x] Test envoy scripts exist.
- [x] Test policy/decree scripts exist.
- [x] Test daily/weekly triggers call diplomacy processing.
- [x] Test faction notes include diplomacy status.
- [x] Test Imperial Expedition is excluded from normal diplomacy.
- [x] Test Slaver/Jotnar/Black Khergit hooks are referenced.
- [x] Test diplomatic report menu is reachable.
- [x] Test no missing script references.

### Build Checks

- [x] `py build\doctor.py --doctor-new-only`
- [x] `py build\test_feature_audit_static.py`
- [x] `py build\test_diplomacy_system_static.py`
- [x] `cmd /c build_module.bat --no-cache`

### Gameplay Scenarios

- [x] Player sends envoy for peace.
- [x] Player signs trade accord.
- [x] Player pays or demands tribute.
- [x] Player breaks treaty and gains badboy/memory penalty.
- [x] War weariness pushes exhausted realm toward peace.
- [x] Anti-slaver decree affects Slaver market state.
- [x] Border control reduces Black Khergit pressure.
- [x] Anti-Imperial league behavior excludes normal diplomacy.
- [x] Faction notes describe current diplomatic state.

## V1 Implementation Target

Start with the smallest powerful version:

- [x] Core slots and initialization.
- [x] Legitimacy, fear, badboy, and war weariness.
- [x] Diplomatic report menu.
- [x] Treaty records for truce, trade accord, tribute, and anti-Imperial league.
- [x] Envoy menu with peace, tribute, trade accord, and anti-Imperial league actions.
- [x] Realm policies for slavery, border control, and cultural focus.
- [x] Decrees for war taxes, reconstruction, anti-slaver edict, and road patrol mandate.
- [x] Faction note upgrades.
- [x] Static tests.

## Later Expansion

- [x] Military access.
- [x] Defensive pacts.
- [x] Prisoner exchange.
- [x] Anti-slaver compact.
- [x] Border security pact.
- [x] Companion envoy travel parties.
- [x] Counteroffers.
- [x] Envoy detention.
- [x] AI treaty offers.
- [x] More realm personalities.
- [x] Full policy management presentation.

## Final Definition of Done

- [x] Diplomacy is visible in reports and notes.
- [x] Diplomacy changes gameplay outcomes.
- [x] Kingdoms behave differently from each other.
- [x] Player ruler choices involve real tradeoffs.
- [x] Mini-factions create diplomatic pressure.
- [x] Imperial Expedition remains a special endgame threat.
- [x] Static tests and build checks pass.
