# Company Troop Dialogue Incidents Checklist

## Goal

Turn the company accounts and morale systems into visible human pressure. Troops should speak before they desert, mutiny, or silently drag battle cohesion down. The player should hear different voices from mercenaries, enlisted soldiers, noble retainers, faith troops, and companions, then answer with pay, food, rest, rites, discipline, persuasion, or companion mediation.

This is a dialogue-forward layer on top of `docs/COMPANY_ACCOUNTS_AND_MORALE_DESIGN.md`, not a replacement for the existing morale math.

## Design Rules

- [x] Incidents should fire rarely enough to feel meaningful.
- [x] Incidents should explain pressure that already exists in company-account state.
- [x] Incidents should give the player at least two credible responses.
- [x] Warnings should precede desertion and mutiny whenever possible.
- [x] Troop classes should sound distinct.
- [x] Companion mediation should matter when the right companion is present, trusted, and role-suited.
- [x] Incidents should not force a new scene.
- [x] Menus/dialogue should reuse camp, reports, and existing company-account helpers.
- [x] Outcomes should feed existing variables: pay confidence, camp strain, ration confidence, petition severity, desertion risk, mutiny risk, casualty pressure, noble restlessness, and companion approval.

## Core Incident State

- [x] Add `$g_sod_company_last_spokesperson_incident_day`.
- [x] Add `$g_sod_company_spokesperson_type`.
- [x] Add `$g_sod_company_spokesperson_class`.
- [x] Add `$g_sod_company_spokesperson_severity`.
- [x] Add `$g_sod_company_spokesperson_mediator`.
- [x] Add `$g_sod_company_spokesperson_last_response`.
- [x] Add constants for incident type:
  - [x] Pay arrears.
  - [x] Thin rations.
  - [x] Wounded care.
  - [x] Hazard pay.
  - [x] Noble honor/restlessness.
  - [x] Faith rites/mercy.
  - [x] Battle promise due.
  - [x] Defeat shock.
  - [x] Victory spoils.
  - [x] Discipline threat.
- [x] Add constants for response type:
  - [x] Pay now.
  - [x] Promise.
  - [x] Battle promise.
  - [x] Ration change.
  - [x] Recreation/rest.
  - [x] Rites/wounded care.
  - [x] Public honors.
  - [x] Persuade.
  - [x] Companion mediation.
  - [x] Threaten discipline.
  - [x] Dismiss complaint.

## Helper Scripts

- [x] Add `script_sod_company_dialogue_try_spokesperson_incident`.
- [x] Add `script_sod_company_dialogue_select_spokesperson_to_regs`.
- [x] Add `script_sod_company_dialogue_describe_spokesperson_to_sXX`.
- [x] Add `script_sod_company_dialogue_apply_response`.
- [x] Add `script_sod_company_dialogue_find_mediator_to_regs`.
- [x] Add `script_sod_company_dialogue_describe_mediator_to_sXX`.
- [x] Add `script_sod_company_dialogue_process_post_battle_prompt`.
- [x] Add `script_sod_company_dialogue_describe_battle_start_morale_to_sXX`.
- [x] Keep helper outputs register-safe for the current Module System register limit.

## Troop Spokesperson Incidents

### Mercenary Captain

- [x] Trigger when mercenary morale is low or mercenary wage weight dominates arrears.
- [x] Trigger after hazard pressure if many mercenaries fought in a costly battle or siege.
- [x] Dialogue should sound contractual: terms, hazard silver, risk, and reputation.
- [x] Responses:
  - [x] Pay contract arrears or hazard pay.
  - [x] Promise pay by date.
  - [x] Promise pay after next battle.
  - [x] Persuade with Leadership/Persuasion.
  - [x] Threaten discipline.
  - [x] Dismiss.
- [x] Outcomes:
  - [x] Pay strongly improves mercenary morale and pay confidence.
  - [x] Promise reduces immediate risk but creates tracked obligation.
  - [x] Threat lowers petition temporarily but increases future mutiny risk if arrears remain.

### Enlisted Spokesman

- [x] Trigger when enlisted morale is low, rations are poor, or camp strain is high.
- [x] Dialogue should sound practical: bread, boots, wounds, families, fear, and exhaustion.
- [x] Responses:
  - [x] Pay wages.
  - [x] Switch to generous/standard rations.
  - [x] Arrange campfire/tavern/village relief.
  - [x] Care for wounded/dependents.
  - [x] Let a small group leave peacefully.
  - [x] Threaten discipline.
- [x] Outcomes:
  - [x] Food/rest helps enlisted morale more than noble morale.
  - [x] Wounded care lowers casualty compensation pressure.
  - [x] Peaceful leave lowers mutiny risk but costs manpower and confidence.

### Noble Retainer

- [x] Trigger when noble restlessness is high.
- [x] Trigger when noble morale is weak despite acceptable pay.
- [x] Dialogue should sound formal: honor, oath, recognition, shame, and public standing.
- [x] Responses:
  - [x] Hold public honors.
  - [x] Seek tournament/arena spectacle.
  - [x] Promise worthy battle.
  - [x] Hold victory feast if recently victorious.
  - [x] Allow honorable withdrawal.
  - [x] Dismiss as pride.
- [x] Outcomes:
  - [x] Honors/tournaments reduce noble restlessness strongly.
  - [x] Tavern recreation has limited effect on noble complaints.
  - [x] Dismissal raises noble restlessness and may create formal withdrawal pressure.

### Faith Troop Voice

- [x] Trigger when faith morale is low.
- [x] Trigger when casualty compensation pressure is high.
- [x] Trigger after slavery, mercy, or rites-related choices when faith troops are present.
- [x] Dialogue should sound doctrinal: mercy, vows, purity, burial, wounded, and sacred duty.
- [x] Responses:
  - [x] Pay for rites.
  - [x] Pay wounded/dependent care.
  - [x] Free captives or reject cruel profit.
  - [x] Make company offering.
  - [x] Ask companion mediator.
  - [x] Dismiss doctrine.
- [x] Outcomes:
  - [x] Rites and wounded care strongly improve faith morale.
  - [x] Cruel dismissal raises faith/noble restlessness.
  - [x] Mercy choices can feed companion approval.

## Companion Mediation

- [x] Marnid can mediate pay, contracts, debt honesty, and mercenary complaints.
- [x] Bunduk can mediate enlisted, veteran, casualty, and officer cruelty complaints.
- [x] Ymira can mediate wounded, hunger, mercy, and dependent-care complaints.
- [x] Jeremus can mediate wounded, disease, casualty, and triage complaints.
- [x] Lezalit can mediate discipline, order, threats, and mutiny warnings.
- [x] Katrin can mediate food, debt, and practical shortage complaints.
- [x] Borcha can mediate road hardship, empty promises, and survival complaints.
- [x] Firentis can mediate honor, mercy, and restraint complaints.
- [x] Baheshtur can mediate cavalry, steppe, and raider-road complaints where appropriate.
- [x] Artimenner can mediate engineering, siege hazard, and camp logistics complaints.
- [x] Klethi can mediate dirty-profit or underworld complaints, but may worsen honorable reactions.
- [x] Mediation strength should depend on:
  - [x] Companion in party.
  - [x] Approval band not troubled/near breaking.
  - [x] Relevant advisor role if assigned.
  - [x] Relevant skill where useful.
- [x] Mediation should apply companion approval hooks.
- [x] Failed mediation should still be characterful, not a silent no-op.

## Battle-Start Morale Feedback

- [x] Add one short battle-start message when morale state is notable.
- [x] Confident company message when pay confidence/category morale is high.
- [x] Unpaid company message when arrears or broken promises are serious.
- [x] Hungry company message when ration confidence is poor.
- [x] Divided company message when one troop category is very weak.
- [x] Wounded/exhausted company message when casualty or hazard pressure is high.
- [x] Active battle-promise message when the player has promised pay after the fight.
- [x] Avoid spam: only one message per battle start.
- [x] Use company-account category morale state already calculated for in-battle cohesion.

## Post-Battle Camp Choices

- [x] Add a focused post-battle company prompt or report line when recent battle pressure is high.
- [x] Recent victory actions:
  - [x] Pay from spoils.
  - [x] Public honors.
  - [x] Victory feast.
  - [x] Care for wounded.
  - [x] Refuse celebration and keep marching.
- [x] Recent defeat actions:
  - [x] Rally the camp.
  - [x] Pay wounded/dependents first.
  - [x] Issue generous rations.
  - [x] Let shaken troops rest.
  - [x] Promise recovery pay.
- [x] Post-battle choices should remain accessible from company accounts, not forced every battle.
- [x] The company report should point clearly to available post-battle choices.

## Menu And Dialogue Surfaces

- [x] Add `mnu_company_spokesperson_incident`.
- [x] Add option from `mnu_company_accounts`: “Hear the company’s spokesman.”
- [x] Add option from petition/desertion/mutiny menus to use current spokesperson handling when appropriate.
- [x] Add response options based on incident type.
- [x] Add mediator option when a suitable companion exists.
- [x] Add fallback “No one is ready to speak formally” text.
- [x] Keep text short enough for Warband menu readability.

## Report Polish

- [x] Company Accounts report should show current spokesperson risk.
- [x] Company Accounts report should show best mediator if one exists.
- [x] Troop-category morale watch point should mention likely incident type.
- [x] Petition report should point to spokesperson dialogue when pressure is above threshold.
- [x] Post-battle report should mention active battle-promise due dates.

## Integration Hooks

- [x] Daily/hourly company pressure processing can schedule spokesperson incidents.
- [x] Post-battle victory hook can flag victory-spoils or wounded-care incidents.
- [x] Total defeat hook can flag defeat-shock incidents.
- [x] Battle-start mission hook can call battle-start morale description.
- [x] Camp accounts can manually trigger current incident.
- [x] Companion depth hooks receive mediation and harsh-response events.
- [x] Company-account pay/ration/recreation helpers remain the source of actual state changes.

## Static Tests

- [x] Add `build/test_company_troop_dialogue_static.py`.
- [x] Assert incident constants exist.
- [x] Assert helper scripts exist.
- [x] Assert company account initialization includes incident globals.
- [x] Assert camp menu links to spokesperson incident menu.
- [x] Assert battle-start mission hook calls morale feedback script.
- [x] Assert victory and defeat hooks can create post-battle incident pressure.
- [x] Assert mediator companions are named in script/report text.
- [x] Assert company accounts report mentions spokesperson risk and mediator.
- [x] Assert tests are referenced by broad feature audit if desired.

## Build Checks

- [x] `py build\test_company_troop_dialogue_static.py`
- [x] `py build\test_company_accounts_static.py`
- [x] `py build\test_companion_depth_system.py`
- [x] `py build\test_feature_audit_static.py`
- [x] `py build\doctor.py --doctor-new-only`
- [x] `cmd /c build_module.bat --no-cache`

## Milestones

### Milestone 1: Spokesperson Framework

- [x] Add incident state/constants.
- [x] Add incident selection helper.
- [x] Add camp menu for current spokesperson.
- [x] Add generic response application.
- [x] Add static test.

### Milestone 2: Class-Specific Voices

- [x] Implement mercenary captain incident.
- [x] Implement enlisted spokesman incident.
- [x] Implement noble retainer incident.
- [x] Implement faith troop voice incident.
- [x] Add report watch-point text for each.

### Milestone 3: Companion Mediation

- [x] Add mediator finder.
- [x] Add mediator description.
- [x] Add role/approval strength checks.
- [x] Add companion approval hooks for mediation.
- [x] Add companion approval hooks for dismissal, threats, and fair settlements.
- [x] Add unique mediator flavor lines for first pass companions.

### Milestone 4: Battle Feedback

- [x] Add battle-start morale feedback script.
- [x] Hook mission start.
- [x] Add post-victory prompt state.
- [x] Add post-defeat prompt state.
- [x] Improve report lines for recent battle aftermath.

### Milestone 5: Polish And QA

- [ ] Tune thresholds to avoid spam.
- [ ] Review menu text length in-game.
- [ ] Verify each troop class can produce an incident.
- [ ] Verify mediation succeeds/fails based on companion state.
- [ ] Verify incidents affect battle morale indirectly through existing company-account state.
- [ ] Manual QA: unpaid mercenary company.
- [ ] Manual QA: hungry enlisted company.
- [ ] Manual QA: restless noble retinue.
- [ ] Manual QA: faith troops after bloody battle.
- [ ] Manual QA: defeat with active battle promise.
- [ ] Manual QA: costly victory with wounded care pressure.
