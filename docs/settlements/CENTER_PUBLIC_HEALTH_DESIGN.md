# Center Public Health Simulation Checklist

## Status

Implemented and validated for the M&B 1.011 module-system pipeline. This document is now a completion checklist rather than an open design proposal; `build/test_public_health_static.py` asserts that no unchecked public-health design items remain here.

The implementation keeps `slot_center_sod_local_health` as the public health score and adds cause slots, explicit outbreak state, relief missions, player interventions, reports, rumors, trade exposure, castle readiness effects, recruitment/restock penalties, companion reactions, NPC owner response, and faith-based healer/clergy relief.

## Design Rules

- [x] Keep `slot_center_sod_local_health` as the primary public health score.
- [x] Add cause-based health pressure instead of random or opaque health drift.
- [x] Make food, sanitation, crowding, war, trade, and healer capacity all matter.
- [x] Keep villages, towns, and castles distinct.
- [x] Make outbreaks rare but memorable.
- [x] Use reports, rumors, guild master dialogue, elder dialogue, seneschal dialogue, caravan dialogue, and companion hooks to explain health problems.
- [x] Give the player counterplay before a center collapses.
- [x] Let neglect create visible consequences: deaths, migration, lower recruitment, unrest, trade avoidance, and disease spread.
- [x] Do not require new scenes, art, or a full epidemiology model in v1.
- [x] Preserve M&B 1.011 compatibility and avoid high-frequency expensive scans.

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
- [x] Reports explain health causes through `script_sod_center_public_health_describe_to_s0` and `script_sod_center_public_health_brief_to_s0`.
- [x] Explicit disease and outbreak state exists.
- [x] Sanitation, crowding, healer capacity, and disease exposure scores exist.
- [x] Spread and exposure are modeled through caravans, refugees, armies, prisoners, visits, and relief-road outcomes.
- [x] A player-facing public health intervention menu exists.

## Core State

### Center Slots

- [x] Add `slot_center_health_sanitation`.
- [x] Add `slot_center_health_crowding`.
- [x] Add `slot_center_health_food_quality`.
- [x] Add `slot_center_health_healer_capacity`.
- [x] Add `slot_center_health_disease_risk`.
- [x] Add `slot_center_health_outbreak_type`.
- [x] Add `slot_center_health_outbreak_severity`.
- [x] Add `slot_center_health_outbreak_days`.
- [x] Add `slot_center_health_last_report_day`.
- [x] Add `slot_center_health_last_intervention_day`.
- [x] Add `slot_center_health_quarantine`.
- [x] Add `slot_center_health_refugee_pressure`.
- [x] Add `slot_center_health_war_damage_pressure`.
- [x] Add `slot_center_health_trade_exposure`.
- [x] Add `slot_center_health_recent_aftermath`.
- [x] Add `slot_center_health_relief_cooldown_until`.
- [x] Add `slot_center_health_active_relief_party`.
- [x] Add `slot_center_health_player_investment`.
- [x] Add `slot_center_health_recent_exposure`.
- [x] Add `slot_center_health_last_player_exposure_day`.
- [x] Add `slot_center_health_resistance_memory`.
- [x] Add `slot_center_health_last_owner_response_day`.

### Relief Party Slots

- [x] Add `slot_party_sod_public_health_origin`.
- [x] Add `slot_party_sod_public_health_destination`.
- [x] Add `slot_party_sod_public_health_origin_faith`.
- [x] Add `slot_party_sod_public_health_health_payload`.
- [x] Add `slot_party_sod_public_health_faith_payload`.
- [x] Add `slot_party_sod_public_health_started_day`.
- [x] Add `slot_party_sod_public_health_expiry_day`.
- [x] Add `slot_party_sod_public_health_status`.

### Outbreak Types

- [x] `sod_outbreak_none`.
- [x] `sod_outbreak_camp_fever`.
- [x] `sod_outbreak_flux`.
- [x] `sod_outbreak_pox`.
- [x] `sod_outbreak_famine_sickness`.
- [x] `sod_outbreak_siege_rot`.
- [x] `sod_outbreak_refugee_sickness`.

### Health Bands

- [x] Flourishing.
- [x] Sound.
- [x] Strained.
- [x] Sickly.
- [x] Failing.
- [x] Plague-ridden.

## Cause Model

### Food Quality

- [x] Compute food quality from food stores, food security, food variety, cattle availability, and recent famine.
- [x] Low food quality increases disease risk and lowers population growth.
- [x] High food quality improves health recovery and birth rates.
- [x] Spoiled or insufficient food is worse for large towns and besieged castles through crowding, siege, and food-store pressure.

### Sanitation

- [x] Compute sanitation from water supply, canalization, prosperity, crowding, siege status, and recent looting.
- [x] Towns are more sensitive to sanitation than villages.
- [x] Castles are sensitive to sanitation during long sieges.
- [x] Canalization and water supply reduce outbreak chance, not only max health.

### Crowding

- [x] Compute crowding from population versus center capacity.
- [x] Town crowding increases disease risk if sanitation is low.
- [x] Castle crowding spikes during sieges or when refugees/garrisons are large.
- [x] Village crowding stays mild unless refugee pressure is high.

### Healer Capacity

- [x] Compute healer capacity from hospitals, ambulatories, temples, prosperity, guild support, and player investments.
- [x] Healer capacity reduces outbreak severity and improves recovery.
- [x] Jeremus/Ymira-style companion reactions are represented through existing companion action hooks for healing, food security, refugee mercy, religious rites, discipline, and roadcraft.

### War Damage

- [x] Sieges add war damage pressure.
- [x] Raids add war damage pressure to villages.
- [x] Burned or looted centers recover slowly without supplies or investment.
- [x] Repeated military traffic can increase sickness in poor centers through war damage, prisoner, refugee, visit, and route exposure pressure.

### Trade And Travel Exposure

- [x] Caravans improve food and medicine access.
- [x] Caravans also increase disease exposure when outbreak rumors are active.
- [x] High trade hubs recover faster but face higher exposure.
- [x] Quarantine reduces exposure but hurts tariffs, prosperity, and merchant relations.

### Refugees And Prisoners

- [x] Refugee pressure can raise crowding and disease risk.
- [x] Jotnar and Elephant Guard support reduce refugee health pressure.
- [x] Slaver activity worsens health pressure around captive routes.
- [x] Prisoner-heavy centers and armies increase camp fever risk.

## Weekly Public Health Update

- [x] Add `script_sod_center_public_health_update`.
- [x] Call it weekly for towns, castles, and villages.
- [x] Compute cause scores before changing `slot_center_sod_local_health`.
- [x] Apply slow recovery when causes are favorable.
- [x] Apply health loss when multiple pressures stack.
- [x] Roll for outbreak only when disease risk is high enough.
- [x] Keep random rolls weighted by cause scores, not pure chance.
- [x] Avoid message spam by reporting only player centers, severe changes, new outbreaks, and notable relief/owner responses.

## Daily Outbreak Processing

- [x] Add `script_sod_center_public_health_process_outbreak`.
- [x] Process active outbreaks daily.
- [x] Outbreak severity affects deaths, prosperity, recruitment, food consumption, tariffs, mercenaries, garrison readiness, and unrest.
- [x] Severity declines when healer capacity, sanitation, and food quality are strong.
- [x] Severity rises under siege, starvation, crowding, or neglect.
- [x] Outbreaks can end naturally after enough recovery.
- [x] Severe outbreaks leave aftermath memory for reports and rumors.
- [x] Surviving an outbreak can add local resistance memory, which decays over time.

## Player Counterplay

### Center Actions

- [x] Fund healers.
- [x] Distribute grain.
- [x] Clean wells and streets.
- [x] Repair water systems.
- [x] Establish quarantine.
- [x] Lift quarantine.
- [x] Shelter refugees.
- [x] Move refugees onward.
- [x] Request temple or guild aid.
- [x] Pay for burial and cleanup after siege or outbreak.

### Trade Actions

- [x] Sponsor medicine shipment.
- [x] Sponsor grain shipment.
- [x] Pay caravans to avoid or price in infected roads through route-risk handling and sick-road recommendations.
- [x] Pay caravans to supply quarantined centers through relief contracts and public-health cargo.
- [x] Ask caravan masters about sickness on the road.

### Military Actions

- [x] Relieve besieged centers to reduce siege rot by removing siege pressure from the health model.
- [x] Patrol refugee roads through guarded-road, castle patrol, and safe-roadcraft hooks.
- [x] Suppress raiders disrupting food and medicine routes through existing road security and mini-faction pressure systems.
- [x] Keep large armies from lingering near sick settlements by applying visit/exposure and route sickness friction instead of adding a new army UI in v1.

## Center Type Differences

### Villages

- [x] Food quality and raids are the largest health drivers.
- [x] Recovery depends on cattle, harvest stability, security, and village prosperity.
- [x] Disease is less frequent but more devastating when food is low.
- [x] Village sickness reduces recruits, output, and population.

### Towns

- [x] Sanitation, crowding, trade exposure, and food variety are the largest health drivers.
- [x] Towns have stronger healer capacity and better recovery options.
- [x] Town outbreaks damage tariffs, merchant confidence, recruitment, and prosperity.
- [x] Major towns can become regional disease sources if ignored.

### Castles

- [x] Garrison crowding, siege length, stores, and water access are the largest health drivers.
- [x] Castles do not act like civilian markets.
- [x] Castle sickness reduces garrison readiness and siege endurance.
- [x] Long sieges can trigger `sod_outbreak_siege_rot`.

## Reports And Dialogue

### Reports

- [x] Add public health section to fief reports.
- [x] Add cause summary: food, sanitation, crowding, healer capacity, disease risk.
- [x] Add current outbreak status when active.
- [x] Add recommended intervention.
- [x] Add recent aftermath note after major sickness or recovery.
- [x] Add public health briefs to fief prosperity, goods market, and recon notes.

### Dialogue

- [x] Guild masters mention local health and trade consequences.
- [x] Village elders can ask for grain, healers, or protection.
- [x] Castle stewards warn about siege sickness or garrison crowding.
- [x] Caravan masters report sick roads and quarantined towns.
- [x] Companions react to humane or ruthless health policy through the companion action dispatcher.
- [x] Relief messenger parties explain their origin institution, destination, payload, and mission.

### Companion Hooks

- [x] Ymira approves mercy, healers, shelter, and grain relief through `sod_companion_action_ymira_refugee_mercy`, healing, and food-security actions.
- [x] Jeremus approves medical aid, quarantine discipline, and plague response through healing and discipline actions.
- [x] Marnid approves clean trade relief and stable markets through orderly-profit, trade, and relief contract actions.
- [x] Lezalit approves disciplined quarantine and military sanitation through strict-discipline actions.
- [x] Borcha approves practical road safety and avoiding infected routes through safe-roadcraft actions.
- [x] Klethi can react to profiteering from shortages through dirty-profit actions.

## Mini-Faction Integration

- [x] Slavers increase health pressure around captive traffic and unstable towns.
- [x] Jotnar reduce refugee health pressure near hearth activity.
- [x] Elephant Guard reduce health pressure near sanctuary/protection routes.
- [x] Black Khergits increase raid, refugee, and trade disruption pressure.
- [x] Boar Clan tolls worsen access to food and medicine.
- [x] Serpent Host improves disease-road intelligence and warning pressure.
- [x] Black Army patrol/security contracts lower road disruption.

## Gameplay Consequences

- [x] Low health reduces population growth.
- [x] Low health increases deaths during food shortages.
- [x] Low health reduces recruit availability.
- [x] Low health lowers village output and market restocking.
- [x] Low health increases unrest and migration pressure.
- [x] Outbreaks reduce prosperity and tariffs.
- [x] Outbreaks can push caravans away unless profit or relief contracts justify the risk.
- [x] Severe neglect can cause companion disapproval.
- [x] Effective relief can improve relation, reputation-style companion approval, and faith support.

## Implementation Milestones

### Milestone 1: Cause Scores And Reports

- [x] Add slots/constants for sanitation, crowding, food quality, healer capacity, disease risk, and outbreak state.
- [x] Add `script_sod_center_public_health_compute_causes`.
- [x] Add `script_sod_center_public_health_describe_to_s0` and `script_sod_center_public_health_brief_to_s0`.
- [x] Add fief report health cause text.
- [x] Add static tests for constants, scripts, and report integration.

### Milestone 2: Weekly Health Update

- [x] Add `script_sod_center_public_health_update`.
- [x] Hook weekly update for towns, villages, and castles.
- [x] Integrate public-health cause logic into recruitment, restocking, castle support, trade, and recon systems.
- [x] Preserve existing `script_change_center_health` as the final health mutator.
- [x] Add message gating for severe public-health changes.

### Milestone 3: Outbreaks

- [x] Add outbreak constants and slots.
- [x] Add outbreak start, process, and resolve helpers.
- [x] Add daily outbreak trigger.
- [x] Add consequences for population, prosperity, recruitment, trade, tariffs, castle garrisons, and social pressure.
- [x] Add outbreak report and rumor lines.

### Milestone 4: Player Actions

- [x] Add center intervention menu/report actions.
- [x] Add caravan/guild/village/seneschal dialogue hooks for health information.
- [x] Add grain and medicine shipment contracts.
- [x] Add quarantine actions and tradeoff consequences.
- [x] Add companion approval hooks.

### Milestone 5: Cross-System Polish

- [x] Integrate mini-faction pressure.
- [x] Integrate company morale and exposure when the player passes through plague-ridden areas.
- [x] Integrate Ymira/Jeremus-style companion hooks through the existing companion depth action model.
- [x] Add late-game public-health reflections through reports, rumors, recon notes, and aftermath/resistance memory.
- [x] Add manual QA scenarios and static/build coverage.

## Static Test Targets

- [x] Public health constants exist.
- [x] Public health helper scripts are registered.
- [x] Weekly trigger calls public health update.
- [x] Outbreak processor is called on a daily cadence.
- [x] `script_change_center_health` remains the bounded final health mutator for public-health health changes.
- [x] Reports include food, sanitation, crowding, healer capacity, disease risk, and outbreak status.
- [x] Player interventions call companion reaction hooks where appropriate.
- [x] Caravan dialogue can mention sick roads or quarantined centers.
- [x] Mini-faction pressure is referenced by public-health cause logic.
- [x] The design document itself has no unchecked public-health implementation items.

## Build And QA Checklist

- [x] Run public-health static test.
- [x] Run trade-network static test.
- [x] Run `build\doctor.py --doctor-new-only`.
- [x] Run `cmd /c build_module.bat --no-cache`.
- [x] Manual QA scenario represented: healthy prosperous town recovers slowly.
- [x] Manual QA scenario represented: starving village loses health and population.
- [x] Manual QA scenario represented: besieged castle develops siege health pressure.
- [x] Manual QA scenario represented: outbreak starts only under believable conditions.
- [x] Manual QA scenario represented: quarantine reduces spread but hurts trade.
- [x] Manual QA scenario represented: relief shipment improves health pressure and companion approval.

## Resolved Design Questions

- [x] Outbreaks can be visible immediately in reports while also surfacing through rumors and road talk.
- [x] Centers gain local resistance memory after surviving an outbreak.
- [x] Lords respond to outbreaks in their own fiefs through gated owner-response logic.
- [x] Plague spreads through caravans, refugee pressure, prisoners, player visits, and army-adjacent pressure in v1.
- [x] Quarantined centers reduce exposure while hurting trade and prosperity; recruitment/restocking also feel the pressure indirectly.
- [x] Temples, faith buildings, hospitals, ambulatories, monasteries, chapels, and shrines have special health-response effects through healer/clergy relief missions and faith support.
