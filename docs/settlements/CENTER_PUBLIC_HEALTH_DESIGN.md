# Center Public Health Simulation Checklist

## Goal

Turn center health from a useful abstract score into a believable public-health system for towns, castles, and villages. Health should feel tied to food quality, crowding, sanitation, war damage, trade routes, refugees, disease, healer capacity, and player policy. The system should remain readable in-game: the player should understand why a center is sick, what can be done, and what consequences follow if it is ignored.

This should build on the existing `slot_center_sod_local_health` system rather than replacing it. The current health slot remains the final score used by population, prosperity, recruitment, trade, defenders, and reports; the new model adds causes, pressure, outbreak state, and better recovery logic.

## Design Rules

- [ ] Keep `slot_center_sod_local_health` as the primary public health score.
- [ ] Add cause-based health pressure instead of random or opaque health drift.
- [ ] Make food, sanitation, crowding, war, trade, and healer capacity all matter.
- [ ] Keep villages, towns, and castles distinct.
- [ ] Make outbreaks rare but memorable.
- [ ] Use reports, rumors, guild master dialogue, and companion comments to explain health problems.
- [ ] Give the player counterplay before a center collapses.
- [ ] Let neglect create visible consequences: deaths, migration, lower recruitment, unrest, trade avoidance, and disease spread.
- [ ] Do not require new scenes, art, or a full epidemiology model in v1.
- [ ] Preserve M&B 1.011 compatibility and avoid high-frequency expensive scans.

## Current Baseline

- [x] Centers already store local health in `slot_center_sod_local_health`.
- [x] `script_change_center_health` applies bounded health changes.
- [x] Hospitals and ambulatories raise maximum health.
- [x] Canalization and water supply raise maximum health.
- [x] Weekly town and village population drift uses health as a growth factor.
- [x] Food pressure can reduce prosperity and health.
- [x] Trade can improve food stores and occasionally health.
- [x] Sieges damage center health.
- [x] Health affects trade value, restocking, village defenders, recruitment, and mini-faction behavior.
- [ ] Current reports do not clearly explain health causes.
- [ ] No explicit disease or outbreak state exists.
- [ ] No sanitation, crowding, healer capacity, or disease exposure score exists.
- [ ] No spread through caravans, refugees, armies, or prisoners exists.
- [ ] No player-facing public health intervention menu exists.

## Core State

### Center Slots

- [ ] Add `slot_center_health_sanitation`.
- [ ] Add `slot_center_health_crowding`.
- [ ] Add `slot_center_health_food_quality`.
- [ ] Add `slot_center_health_healer_capacity`.
- [ ] Add `slot_center_health_disease_risk`.
- [ ] Add `slot_center_health_outbreak_type`.
- [ ] Add `slot_center_health_outbreak_severity`.
- [ ] Add `slot_center_health_outbreak_days`.
- [ ] Add `slot_center_health_last_report_day`.
- [ ] Add `slot_center_health_last_intervention_day`.
- [ ] Add `slot_center_health_quarantine`.
- [ ] Add `slot_center_health_refugee_pressure`.
- [ ] Add `slot_center_health_war_damage_pressure`.
- [ ] Add `slot_center_health_trade_exposure`.

### Outbreak Types

- [ ] `sod_outbreak_none`.
- [ ] `sod_outbreak_camp_fever`.
- [ ] `sod_outbreak_flux`.
- [ ] `sod_outbreak_pox`.
- [ ] `sod_outbreak_famine_sickness`.
- [ ] `sod_outbreak_siege_rot`.
- [ ] `sod_outbreak_refugee_sickness`.

### Health Bands

- [ ] Flourishing.
- [ ] Sound.
- [ ] Strained.
- [ ] Sickly.
- [ ] Failing.
- [ ] Plague-ridden.

## Cause Model

### Food Quality

- [ ] Compute food quality from food stores, food security, food variety, cattle availability, and recent famine.
- [ ] Low food quality increases disease risk and lowers population growth.
- [ ] High food quality improves health recovery and birth rates.
- [ ] Spoiled or insufficient food should be worse for large towns and besieged castles.

### Sanitation

- [ ] Compute sanitation from water supply, canalization, prosperity, crowding, siege status, and recent looting.
- [ ] Towns are more sensitive to sanitation than villages.
- [ ] Castles are sensitive to sanitation during long sieges.
- [ ] Canalization and water supply should reduce outbreak chance, not only raise max health.

### Crowding

- [ ] Compute crowding from population versus center capacity.
- [ ] Town crowding should increase disease risk if sanitation is low.
- [ ] Castle crowding should spike during sieges or when refugees/garrisons are large.
- [ ] Village crowding is usually mild unless refugee pressure is high.

### Healer Capacity

- [ ] Compute healer capacity from hospitals, ambulatories, temples, prosperity, guild support, and player investments.
- [ ] Healer capacity should reduce outbreak severity and improve recovery.
- [ ] Jeremus and Ymira advisor/companion hooks can improve intervention outcomes later.

### War Damage

- [ ] Sieges add war damage pressure.
- [ ] Raids add war damage pressure to villages.
- [ ] Burned or looted centers recover slowly without supplies or investment.
- [ ] Repeated military traffic can increase sickness in poor centers.

### Trade And Travel Exposure

- [ ] Caravans improve food and medicine access.
- [ ] Caravans also increase disease exposure when outbreak rumors are active.
- [ ] High trade hubs should recover faster but face higher exposure.
- [ ] Quarantine should reduce exposure but hurt tariffs, prosperity, and merchant relations.

### Refugees And Prisoners

- [ ] Refugee pressure can raise crowding and disease risk.
- [ ] Jotnar and Elephant Guard support should reduce refugee health pressure.
- [ ] Slaver activity should worsen health pressure around captive routes.
- [ ] Prisoner-heavy centers and armies can increase camp fever risk.

## Weekly Public Health Update

- [ ] Add `script_sod_center_public_health_update`.
- [ ] Call it weekly for towns, castles, and villages.
- [ ] Compute cause scores before changing `slot_center_sod_local_health`.
- [ ] Apply slow recovery when causes are favorable.
- [ ] Apply health loss when multiple pressures stack.
- [ ] Roll for outbreak only when disease risk is high enough.
- [ ] Keep random rolls weighted by cause scores, not pure chance.
- [ ] Avoid message spam by reporting only player centers, severe changes, or new outbreaks.

## Daily Outbreak Processing

- [ ] Add `script_sod_center_public_health_process_outbreak`.
- [ ] Process active outbreaks daily or every 48 hours.
- [ ] Outbreak severity affects deaths, prosperity, recruitment, food consumption, and unrest.
- [ ] Severity declines when healer capacity, sanitation, and food quality are strong.
- [ ] Severity rises under siege, starvation, crowding, or neglect.
- [ ] Outbreaks can end naturally after enough recovery.
- [ ] Severe outbreaks can leave aftermath memory for reports and rumors.

## Player Counterplay

### Center Actions

- [ ] Fund healers.
- [ ] Distribute grain.
- [ ] Clean wells and streets.
- [ ] Repair water systems.
- [ ] Establish quarantine.
- [ ] Lift quarantine.
- [ ] Shelter refugees.
- [ ] Move refugees onward.
- [ ] Request temple or guild aid.
- [ ] Pay for burial and cleanup after siege or outbreak.

### Trade Actions

- [ ] Sponsor medicine shipment.
- [ ] Sponsor grain shipment.
- [ ] Pay caravans to avoid infected roads.
- [ ] Pay caravans to supply quarantined centers.
- [ ] Ask caravan masters about sickness on the road.

### Military Actions

- [ ] Relieve besieged centers to reduce siege rot.
- [ ] Patrol refugee roads.
- [ ] Suppress raiders disrupting food and medicine routes.
- [ ] Keep large armies from lingering near sick settlements.

## Center Type Differences

### Villages

- [ ] Food quality and raids are the largest health drivers.
- [ ] Recovery should depend on cattle, harvest stability, security, and village prosperity.
- [ ] Disease should be less frequent but more devastating when food is low.
- [ ] Village sickness should reduce recruits, output, and population.

### Towns

- [ ] Sanitation, crowding, trade exposure, and food variety are the largest health drivers.
- [ ] Towns should have stronger healer capacity and better recovery options.
- [ ] Town outbreaks should damage tariffs, merchant confidence, recruitment, and prosperity.
- [ ] Major towns can become regional disease sources if ignored.

### Castles

- [ ] Garrison crowding, siege length, stores, and water access are the largest health drivers.
- [ ] Castles should not act like civilian markets.
- [ ] Castle sickness should reduce garrison readiness and siege endurance.
- [ ] Long sieges can trigger `sod_outbreak_siege_rot`.

## Reports And Dialogue

### Reports

- [ ] Add public health section to fief reports.
- [ ] Add cause summary: food, sanitation, crowding, healer capacity, disease risk.
- [ ] Add current outbreak status when active.
- [ ] Add recommended intervention.
- [ ] Add recent aftermath note after major sickness or recovery.

### Dialogue

- [ ] Guild masters can mention local health and trade consequences.
- [ ] Village elders can ask for grain, healers, or protection.
- [ ] Castle stewards can warn about siege sickness or garrison crowding.
- [ ] Caravan masters can report sick roads and quarantined towns.
- [ ] Companions can react to humane or ruthless health policy.

### Companion Hooks

- [ ] Ymira approves mercy, healers, shelter, and grain relief.
- [ ] Jeremus approves medical aid, quarantine discipline, and plague response.
- [ ] Marnid approves clean trade relief and stable markets.
- [ ] Lezalit approves disciplined quarantine and military sanitation.
- [ ] Borcha approves practical road safety and avoiding infected routes.
- [ ] Klethi can react to profiteering from shortages.

## Mini-Faction Integration

- [ ] Slavers increase health pressure around captive traffic and unstable towns.
- [ ] Jotnar reduce refugee health pressure near hearth activity.
- [ ] Elephant Guard reduce health pressure near sanctuary/protection routes.
- [ ] Black Khergits increase raid, refugee, and trade disruption pressure.
- [ ] Boar Clan tolls can worsen access to food and medicine.
- [ ] Serpent Host can improve disease-road intelligence.
- [ ] Black Army patrol/security contracts can lower road disruption.

## Gameplay Consequences

- [ ] Low health reduces population growth.
- [ ] Low health increases deaths during food shortages.
- [ ] Low health reduces recruit availability.
- [ ] Low health lowers village output and market restocking.
- [ ] Low health increases unrest and migration pressure.
- [ ] Outbreaks reduce prosperity and tariffs.
- [ ] Outbreaks can push caravans away unless profit or relief contracts justify the risk.
- [ ] Severe neglect can cause companion disapproval.
- [ ] Effective relief can improve relation, honor-style reputation, and companion approval.

## Implementation Milestones

### Milestone 1: Cause Scores And Reports

- [ ] Add slots/constants for sanitation, crowding, food quality, healer capacity, disease risk, and outbreak state.
- [ ] Add `script_sod_center_public_health_compute_causes`.
- [ ] Add `script_sod_center_public_health_describe_to_sXX`.
- [ ] Add fief report health cause text.
- [ ] Add static tests for constants, scripts, and report integration.

### Milestone 2: Weekly Health Update

- [ ] Add `script_sod_center_public_health_update`.
- [ ] Hook weekly update for towns, villages, and castles.
- [ ] Replace scattered weekly health drift where feasible with public-health cause logic.
- [ ] Preserve existing `script_change_center_health` as the final health mutator.
- [ ] Add message gating for severe public-health changes.

### Milestone 3: Outbreaks

- [ ] Add outbreak constants and slots.
- [ ] Add outbreak start, process, and resolve helpers.
- [ ] Add daily or 48-hour outbreak trigger.
- [ ] Add consequences for population, prosperity, recruitment, and trade.
- [ ] Add outbreak report and rumor lines.

### Milestone 4: Player Actions

- [ ] Add center intervention menu/report actions.
- [ ] Add caravan/guild/village dialogue hooks for health information.
- [ ] Add grain and medicine shipment contracts.
- [ ] Add quarantine actions and tradeoff consequences.
- [ ] Add companion approval hooks.

### Milestone 5: Cross-System Polish

- [ ] Integrate mini-faction pressure.
- [ ] Integrate company morale when troops pass through plague-ridden areas.
- [ ] Integrate companion personal quest hooks for Ymira and Jeremus.
- [ ] Add late-game public-health reflections.
- [ ] Add manual QA scenarios.

## Static Test Targets

- [ ] Public health constants exist.
- [ ] Public health helper scripts are registered.
- [ ] Weekly trigger calls public health update.
- [ ] Outbreak processor is called on a daily or 48-hour cadence.
- [ ] `script_change_center_health` remains the only direct final health mutator for most systems.
- [ ] Reports include food, sanitation, crowding, healer capacity, disease risk, and outbreak status.
- [ ] Player interventions call companion reaction hooks where appropriate.
- [ ] Caravan dialogue can mention sick roads or quarantined centers.
- [ ] Mini-faction pressure is referenced by public-health cause logic.

## Build And QA Checklist

- [ ] Run `py build\doctor.py --doctor-new-only`.
- [ ] Run `py build\test_feature_audit_static.py`.
- [ ] Run focused public-health static test.
- [ ] Run `cmd /c build_module.bat --no-cache`.
- [ ] Manual QA: healthy prosperous town recovers slowly.
- [ ] Manual QA: starving village loses health and population.
- [ ] Manual QA: besieged castle develops siege health pressure.
- [ ] Manual QA: outbreak starts only under believable conditions.
- [ ] Manual QA: quarantine reduces spread but hurts trade.
- [ ] Manual QA: relief shipment improves health pressure and companion approval.

## Open Design Questions

- [ ] Should outbreaks be visible immediately, or first appear as rumors?
- [ ] Should centers have local immunity/resistance after surviving an outbreak?
- [ ] Should lords respond to outbreaks in their own fiefs?
- [ ] Should plague spread through armies or only through caravans/refugee pressure in v1?
- [ ] Should quarantined centers block recruitment, trade, or both?
- [ ] Should temples/faith troops have special health-response effects?
