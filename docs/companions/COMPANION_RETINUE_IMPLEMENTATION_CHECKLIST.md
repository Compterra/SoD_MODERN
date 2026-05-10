# Companion Retinue Implementation Checklist

This document specifies a center-style companion retinue system: companions can hold troops internally, much like a town or castle holds a garrison, while still traveling with the player as members of the company. The design goal is to make companions feel mechanically distinct and worth maintaining without turning them into visible external follower parties.

The retinue is not a free army. It is a companion-owned subdivision inside the player's force. Retinue troops should not count against the player's personal party-size limit, but they should still be real troops with wages, food pressure, battle participation, wounds, deaths, morale consequences, and relationship-driven risk.

## Core Fantasy

- [x] Companions can command their own internal troop groups.
- [x] Retinues feel like garrisons inside a moving center: stored under a container, inspected through menus/dialogue, and moved in/out intentionally.
- [x] The player remains the army commander, but each companion becomes a captain with their own command capacity.
- [x] A companion's retinue capacity comes from that companion's stats, not the player's stats.
- [x] Retinue troops do not count against the player's party-size limit.
- [x] Retinue troops still exist as actual troop stacks, not abstract numbers.
- [x] Retinue troops can fight, be wounded, die, receive wages, consume supplies, and influence morale.
- [x] The player can fund a companion's command purse so the companion can self-manage routine recruitment, upgrades, and post-battle hiring.
- [x] The player can set each companion's desired retinue posture: no troops, half strength, or full strength.
- [x] The player sees each companion's retinue as one command cost instead of micromanaging every wage line.
- [x] Poor companion relationship, unresolved warnings, or personal quest rupture can reduce capacity or threaten retinue loyalty.
- [x] Companion departure, capture, death, or exile handles their retinue explicitly instead of leaking troops or duplicating them.

## Storage Model

Preferred implementation: hidden companion-owned retinue parties.

This mirrors center garrisons better than a pure ledger. Centers hold troop stacks inside the center party. Companion retinues should hold troop stacks inside a hidden party associated with the companion. The party is a storage container first and a world-map object only if a later feature intentionally exposes it.

- [x] Add a dedicated party template such as `pt_sod_companion_retinue`.
- [x] Add a dedicated special party type such as `spt_companion_retinue`.
- [x] Ensure retinue parties are not treated as external follower parties.
- [x] Ensure retinue parties are not commandable through mercenary/patrol dialogue.
- [x] Ensure retinue parties are not visible as normal map followers in ordinary play.
- [x] Ensure retinue parties use `fac_player_faction` only if that does not accidentally expose command dialogue, battle joining, or wage systems incorrectly.
- [x] Store the owning companion troop id on the retinue party.
- [x] Store the retinue party id on the companion troop.
- [x] Store whether the retinue is active, suspended, detached, or pending cleanup.
- [x] Store the last known player party/center context for old-save repair.
- [x] Provide a repair script that recreates or relinks missing retinue parties for companions in the main party.
- [x] Provide a cleanup script that safely empties, transfers, or removes orphaned retinue parties.

Recommended slots:

- [x] `slot_troop_sod_retinue_party`
- [x] `slot_troop_sod_retinue_capacity`
- [x] `slot_troop_sod_retinue_state`
- [x] `slot_troop_sod_retinue_policy`
- [x] `slot_troop_sod_retinue_last_size`
- [x] `slot_troop_sod_retinue_last_wage`
- [x] `slot_troop_sod_retinue_last_morale`
- [x] `slot_troop_sod_retinue_warning_state`
- [x] `slot_troop_sod_retinue_treasury`
- [x] `slot_troop_sod_retinue_wage_reserve`
- [x] `slot_troop_sod_retinue_strength_order`
- [x] `slot_troop_sod_retinue_recruit_policy`
- [x] `slot_troop_sod_retinue_last_recruit_hour`
- [x] `slot_troop_sod_retinue_last_upgrade_hour`
- [x] `slot_troop_sod_retinue_last_invoice`
- [x] `slot_party_sod_retinue_owner_troop`
- [x] `slot_party_sod_retinue_anchor_party`
- [x] `slot_party_sod_retinue_last_sync_hour`
- [x] `slot_party_sod_retinue_state`

State constants:

- [x] `sod_retinue_state_inactive`
- [x] `sod_retinue_state_active`
- [x] `sod_retinue_state_suspended`
- [x] `sod_retinue_state_detached`
- [x] `sod_retinue_state_pending_cleanup`

Policy constants:

- [x] `sod_retinue_policy_balanced`
- [x] `sod_retinue_policy_defensive`
- [x] `sod_retinue_policy_aggressive`
- [x] `sod_retinue_policy_training`
- [x] `sod_retinue_policy_guard_companion`

Strength order constants:

- [x] `sod_retinue_strength_none`
- [x] `sod_retinue_strength_half`
- [x] `sod_retinue_strength_full`

Recruit policy constants:

- [x] `sod_retinue_recruit_policy_none`
- [x] `sod_retinue_recruit_policy_cautious`
- [x] `sod_retinue_recruit_policy_balanced`
- [x] `sod_retinue_recruit_policy_eager`

## Capacity Rules

Companion retinue size should be based on the companion's ability to command soldiers.

- [x] Add `script_sod_companion_retinue_get_capacity(companion)`.
- [x] Base capacity on companion `Leadership`.
- [x] Add a modest `Charisma` contribution.
- [x] Add a small level or renown-equivalent contribution.
- [x] Add an approval/cohesion modifier.
- [x] Add a penalty for active grievance/warning states.
- [x] Add a penalty for unresolved personal quest rupture.
- [x] Cap very low-trust retinues so the system cannot be used to bypass bad relationships.
- [x] Let excellent trust or resolved-good personal quests grant a small capacity bonus.
- [x] Do not use the player's Leadership, Charisma, or renown for companion retinue capacity.
- [x] Do not let retinue capacity become negative.
- [x] Do not silently delete excess troops when capacity falls.
- [x] Put over-capacity retinues into a warning state that blocks adding more troops and asks the player to reclaim or discharge extras.

Suggested first-pass formula:

- [x] Base 4 troops.
- [x] `Leadership * 5`.
- [x] `Charisma / 2`.
- [x] `Level / 3`.
- [x] Trust bonus: +0 to +8 depending on companion cohesion/approval.
- [x] Warning penalty: -5 to -15 depending on severity.
- [x] Good personal quest result bonus: +3 to +8.
- [x] Hard personal quest result bonus: +1 to +4, if the result strengthened command but damaged trust.

## Player Party Size Interaction

The player should gain usable capacity through trusted companions without retinue troops counting as player-commanded bodies.

- [x] Audit every use of `party_get_num_companions("p_main_party")`.
- [x] Audit every use of `party_get_free_companions_capacity("p_main_party")`.
- [x] Audit recruitment, freed-captive, prisoner-recruitment, tavern-hire, village-recruit, and quest-reward troop flows.
- [x] Add `script_sod_get_player_effective_party_size` if needed.
- [x] Add `script_sod_get_player_effective_party_capacity` if needed.
- [x] Keep normal player party-size reporting honest: player-commanded troops and companion-commanded retinues should be distinguished.
- [x] Prevent recruitment flows from bypassing the retinue transfer screen by accidentally adding over-capacity troops to the main party.
- [x] Make it clear when the player cannot personally hold more troops but a companion can take some into retinue.
- [x] Never increase the native player party-size cap by simply adding all retinue capacity to it.
- [x] Avoid duplicate counting if retinue parties are temporarily merged for battle.

## Transfer Flow

Retinue management should feel like assigning troops to a captain, not like a dry exploit menu.

- [x] Add a camp/company menu entry: `Review companion retinues.`
- [x] Add direct companion dialogue: `I want to discuss the troops under your command.`
- [x] Show current retinue size and capacity.
- [x] Show companion-specific command flavor.
- [x] Let the player assign troops from main party to the companion retinue.
- [x] Let the player reclaim troops from the retinue to the main party if there is personal capacity.
- [x] Let the player swap troops between companion retinues only through explicit transfer steps.
- [x] Prevent assigning a companion to command themself.
- [x] Prevent assigning heroes, prisoners, cattle, invalid troops, or nonstandard pseudo-troops.
- [x] Prevent assigning troops when the companion is not in the party.
- [x] Prevent assigning troops to companions who are unconscious, imprisoned, departed, or in a quest absence state.
- [x] Block transfer when the retinue party is missing until repair succeeds.
- [x] Confirm disbanding troops from an over-capacity retinue.
- [x] Give feedback when a companion refuses additional command due to low relationship.
- [x] Give feedback when a companion is over capacity and morale is degrading.
- [x] Let the player move gold into or out of the companion's command purse.
- [x] Let the player set the companion's desired strength: no troops, half strength, or full strength.
- [x] Let the player set whether the companion may recruit and upgrade on their own.
- [x] Let the player inspect the companion's current command purse and wage reserve.
- [x] Let the player order a companion to dismiss, return, or stop replacing troops when set to no troops.
- [x] Let the player order a companion to maintain roughly half of their current capacity.
- [x] Let the player order a companion to build toward full capacity if funds and recruitment opportunities exist.

Recommended transfer scripts:

- [x] `script_sod_companion_retinue_ensure_party(companion)`
- [x] `script_sod_companion_retinue_can_accept_troop(companion, troop, amount)`
- [x] `script_sod_companion_retinue_add_troops(companion, troop, amount)`
- [x] `script_sod_companion_retinue_remove_troops(companion, troop, amount)`
- [x] `script_sod_companion_retinue_add_troops_up_to_capacity(companion, troop, requested)`
- [x] `script_sod_companion_retinue_remove_troops_up_to_capacity(companion, troop, requested)`
- [x] `script_sod_companion_retinue_select_main_party_troop(current_troop, advance)`
- [x] `script_sod_companion_retinue_select_retinue_troop(companion, current_troop, advance)`
- [x] `script_sod_companion_retinue_get_size(companion)`
- [x] `script_sod_companion_retinue_get_free_capacity(companion)`
- [x] `script_sod_companion_retinue_get_target_size(companion)`
- [x] `script_sod_companion_retinue_set_strength_order(companion, order)`
- [x] `script_sod_companion_retinue_add_gold(companion, amount)`
- [x] `script_sod_companion_retinue_remove_gold(companion, amount)`
- [x] `script_sod_companion_retinue_repair_all`
- [x] `script_sod_companion_retinue_cleanup_for_departure(companion, mode)`

## Companion Treasury And Autonomy

The player should be able to delegate routine troop management. A funded companion can recruit, upgrade, and maintain their retinue toward the player's chosen strength order without asking after every battle or town visit.

- [x] Add a companion command purse stored on the companion.
- [x] Let the player give gold directly to a companion's purse.
- [x] Let the player take gold back from a companion's purse, subject to current wage reserve and relationship rules.
- [x] Track a wage reserve so companions do not spend their last denars on recruits and then immediately fail payroll.
- [x] Show the player's weekly cost as one line per companion: companion wage plus retinue wage.
- [x] Keep the detailed troop wage breakdown available in reports for debugging and transparency.
- [x] Let companions pay retinue wages from their purse first.
- [x] If the purse cannot cover wages, charge the player through the normal weekly wage flow if the player has agreed to cover shortages.
- [x] If neither purse nor player can cover wages, trigger retinue morale loss, desertion risk, or refusal to recruit more.
- [x] Add dialogue for companion concerns when the purse is too low for the ordered strength.
- [x] Prevent companions from spending quest-critical, player-reserved, or negative gold.
- [x] Prevent gold duplication when companions depart, are captured, or reconcile.
- [x] Decide whether angry departures let the companion keep part or all of the command purse.
- [x] Return remaining purse gold to the player on peaceful disbanding unless narrative state says otherwise.

Autonomous recruitment:

- [x] Add `script_sod_companion_retinue_try_autorecruit(companion)`.
- [x] Add `script_sod_companion_retinue_try_autoupgrade(companion)`.
- [x] Add `script_sod_companion_retinue_try_post_battle_hire(companion)`.
- [x] Add `script_sod_companion_retinue_calculate_recruit_budget(companion)`.
- [x] Add `script_sod_companion_retinue_calculate_upgrade_budget(companion)`.
- [x] Use the companion's strength order to decide whether to recruit.
- [x] Use available purse gold after wage reserve to decide how many recruits/upgrades are affordable.
- [x] Use companion troop preferences to choose recruit types where possible.
- [x] Use current location, culture, and recruitment opportunity to choose available recruits.
- [x] Use companion skills and role identity to influence training and upgrade priorities.
- [x] Respect the player's order to keep no troops.
- [x] Respect half-strength orders by stopping near half capacity.
- [x] Respect full-strength orders by recruiting toward capacity.
- [x] Do not recruit if the companion is absent, wounded beyond command threshold, captured, or in a suspended state.
- [x] Do not recruit if the companion is in active grievance or refuses command.
- [x] Do not recruit troops that would violate faction, culture, prisoner, or quest restrictions.
- [x] Do not recruit in scenes or missions where party stacks should not change.

Post-battle self-management:

- [x] After battle, let eligible companions request to hire suitable leftover rescued/freed troops.
- [x] Let companions prefer troops matching their retinue identity.
- [x] Let companions take only troops that fit their capacity and purse.
- [x] Let the player opt out globally or per companion.
- [x] Prevent companions from taking troops the player explicitly chose to keep in the main party.
- [x] Prevent companions from hiring prisoners directly unless a later design intentionally supports it.
- [x] Add feedback such as: `Bunduk has taken 3 crossbowmen under his command.`
- [x] Add a report line when a companion wanted recruits but lacked gold, capacity, or trust.

Desired strength behavior:

- [x] No troops: companion returns or dismisses retinue troops over time and stops replacing losses.
- [x] Half troops: companion maintains about 50 percent of current capacity, with a small tolerance band to avoid constant churn.
- [x] Full party: companion recruits and upgrades toward maximum capacity while keeping wage reserve.
- [x] Over-capacity plus no-troops order should prioritize returning troops to the player, then discharge if needed.
- [x] Over-capacity plus half/full order should stop recruitment and ask for player intervention.
- [x] If capacity changes, target size recalculates from the new capacity.
- [x] If relationship drops, the companion may refuse full-strength orders until trust is restored.

## Battle Participation

Retinue troops must be real in combat. If they do not fight, the system becomes invisible storage.

- [x] Audit how nearby allied parties join player battles.
- [x] Decide whether hidden retinue parties join as nearby allied parties or temporarily merge into a battle roster.
- [x] Ensure retinue troops can spawn in battles where the companion is present.
- [x] Ensure retinue casualties are applied back to the correct retinue party.
- [x] Ensure retinue wounded/dead outcomes do not duplicate or erase stacks.
- [x] Ensure retinue troops do not appear twice if the retinue party and player party are both counted.
- [x] Ensure retinue troops are excluded from battles if the owning companion is absent, captured, or detached.
- [x] Ensure the companion can appear with their retinue if battle spawn logic supports captain grouping.
- [x] Add fallback behavior if the engine cannot safely auto-join hidden parties: temporarily merge before battle and restore afterward.
- [x] Add static tests for whichever battle bridge is chosen.
- [x] Add manual QA for ordinary field battle, siege attack, siege defense, village raid defense, and ambush/quest battle.

## Wages, Food, Morale, And Training

Retinues should not be free support. They should shift burden from player command capacity to companion command quality.

- [x] Include retinue troops in weekly wage calculation.
- [x] Show retinue wages as a single companion command cost in the primary weekly wage summary.
- [x] Show retinue wages separately in detailed company/account reports.
- [x] Do not charge retinue wages twice.
- [x] Make the companion's command purse the first payer for retinue wages.
- [x] Decide whether the player automatically covers command-purse shortages or must explicitly replenish them.
- [x] If automatic coverage is enabled, show the companion's shortage as part of the weekly wage bill.
- [x] If automatic coverage is disabled, apply morale/desertion consequences when the purse cannot pay.
- [x] Apply companion Leadership wage reduction only to that companion's retinue if desired.
- [x] Apply player-wide wage modifiers only where existing faction/company logic already applies.
- [x] Include retinue troops in food consumption or a companion-specific supply pressure calculation.
- [x] Include retinue size in morale pressure, but distinguish player overcrowding from retinue cohesion.
- [x] Let high companion Leadership soften morale pressure inside that retinue.
- [x] Let over-capacity retinues create morale loss or desertion risk.
- [x] Let companion role bonuses affect only suitable retinue troops when appropriate.
- [x] Decide whether companion Trainer skill grants XP to their retinue.
- [x] Let companions spend purse gold on upgrades only after keeping a minimum wage reserve.
- [x] Let companions train toward their preferred troop roles before buying raw numbers.
- [x] Prevent retinue training from becoming stronger than intended by stacking all companions.

## Companion Relationship Effects

This feature should reward maintaining hard relationships.

- [x] High approval increases retinue capacity modestly.
- [x] Low approval reduces capacity.
- [x] Active warning state blocks expansion or increases desertion risk.
- [x] Low approval can make a companion unwilling to accept a full-strength order.
- [x] High approval can make a companion more careful with command-purse spending.
- [x] Personal quest good outcome grants a small command bonus.
- [x] Personal quest hard outcome may grant a tactical bonus but reduce loyalty safety.
- [x] Personal quest failure may suspend retinue command.
- [x] Companion grievance events can cause retinue unrest.
- [x] Reconciliation can restore capacity.
- [x] Companion-specific values should influence troop preferences where practical.
- [x] Companion report should mention retinue health, over-capacity, and loyalty risk.

## Companion Identity And Preferred Troops

Retinues should make companions feel different without hard-locking the player.

- [x] Add optional preferred troop categories per companion.
- [x] Use preferences for flavor, small bonuses, warnings, or training efficiency.
- [x] Do not forbid off-theme troops unless there is a strong narrative reason.
- [x] Let martial companions command larger or more stable retinues.
- [x] Let non-martial companions command smaller but useful specialist retinues.
- [x] Make Ymira, Jeremus, Katrin, and other non-frontline companions viable through support-focused retinues.
- [x] Make Lezalit, Bunduk, Matheld, Baheshtur, Alayen, and Firentis feel like real field captains.
- [x] Make Klethi, Borcha, Deshavi, Marnid, Nizar, Rolf, and Artimenner feel distinct through scouting, irregulars, trade guards, glory troops, or engineers where appropriate.

Example preference map:

- [x] Alayen: disciplined noble infantry/cavalry, low tolerance for rabble.
- [x] Artimenner: engineers, crossbowmen, siege-support troops.
- [x] Baheshtur: mounted troops, scouts, horse archers.
- [x] Borcha: scouts, light cavalry, irregular road fighters.
- [x] Bunduk: infantry, crossbowmen, veterans with soldier-welfare concern.
- [x] Deshavi: archers, trackers, village militia, ambushers.
- [x] Firentis: disciplined infantry and redeemed lowborn troops.
- [x] Jeremus: guards, wounded recovery support, defensive escorts.
- [x] Katrin: caravan guards, household troops, practical militia.
- [x] Klethi: skirmishers, knife-fighters, light irregulars.
- [x] Lezalit: drilled infantry, recruits in training, formations.
- [x] Marnid: caravan guards, mercantile escorts, crossbowmen.
- [x] Matheld: shield troops, axes, hard infantry.
- [x] Nizar: cavalry, shock troops, tournament-glory volunteers.
- [x] Rolf: prestige troops, self-styled noble guard, heavy infantry.
- [x] Ymira: protectors, escorts, mercy-focused defenders.

## UI And Dialogue Surfaces

Menus should manage storage and status; dialogue should carry character.

- [x] Add a clear company-level retinue overview.
- [x] Add companion-specific direct-talk entries for retinue command.
- [x] Use menus for transfer lists and troop counts.
- [x] Use dialogue for trust, refusal, warnings, over-capacity concern, and personal command identity.
- [x] Add report text that distinguishes player party, companion retinues, external parties, and garrisons.
- [x] Add compact status lines:
  - [x] `Under your command: 18 / 27`
  - [x] `Order: half strength`
  - [x] `Command purse: 1,240 denars`
- [x] `Wage reserve: 2 weeks`
  - [x] `Current burden: steady`
  - [x] `Loyalty: strained`
  - [x] `Wages due this week: 312 denars`
- [x] Avoid making the system feel like a generic storage chest.
- [x] Avoid using quest-style moral choices for routine troop transfer.
- [x] Add a warning before assigning expensive troops to a companion with low loyalty.
- [x] Add a warning before reclaiming troops if it would exceed the player's personal capacity.
- [x] Add dialogue for setting strength order: no troops, half strength, full strength.
- [x] Add dialogue for giving the companion command funds.
- [x] Add dialogue for withdrawing unused command funds.
- [x] Add a clear explanation that autonomous recruitment uses only the companion's purse and current orders.

## Departure, Capture, And Failure Rules

No retinue should survive as a broken orphan if its companion stops being a valid captain.

- [x] On voluntary companion departure, decide whether retinue troops return, leave with them, or partially desert.
- [x] On angry departure, allow a relationship-based chance that some retinue troops follow the companion.
- [x] On voluntary companion departure, decide whether unused command-purse gold returns to the player.
- [x] On angry departure, allow the companion to keep some or all of their command purse if relationship state justifies it.
- [x] On companion capture, suspend the retinue and move troops to a safe temporary state.
- [x] On companion capture, suspend autonomous recruitment and protect the purse from weekly spending until the capture outcome resolves.
- [x] On companion death or permanent removal, transfer survivors to player party if capacity allows, otherwise force a disband/over-capacity decision.
- [x] On companion quest absence, suspend transfers until the companion returns.
- [x] On companion quest absence, suspend autonomous recruitment and training.
- [x] On player defeat, apply normal loss logic to retinues.
- [x] On player capture, ensure retinue parties do not remain active invisible armies.
- [x] On faction change, rebellion, or mercenary contract change, preserve retinue ownership unless the companion leaves.
- [x] On old-save load, repair missing retinue parties before any transfer menu opens.
- [x] On mod upgrade, ensure existing companions start with empty inactive retinues rather than invalid slots.

## Exploit And Edge Case Controls

- [x] Prevent using retinues to bypass all morale consequences.
- [x] Prevent using retinues to bypass all wages.
- [x] Prevent using companion purses to duplicate or hide player gold.
- [x] Prevent companion purses from spending below zero.
- [x] Prevent autonomous recruitment from ignoring the player's no-troops order.
- [x] Prevent autonomous recruitment from repeatedly buying and disbanding troops because of tight half-strength thresholds.
- [x] Prevent using retinues to bypass prisoner or hero limits.
- [x] Prevent hiding troops from defeat/capture losses.
- [x] Prevent retinue troops from being sold, upgraded, or transferred through unintended menus.
- [x] Prevent retinue troops from joining external follower party commands.
- [x] Prevent retinue parties from being selected as quest targets.
- [x] Prevent retinue parties from being assigned town AI or patrol AI.
- [x] Prevent retinue parties from being counted as independent player-owned companies.
- [x] Prevent retinue troops from disappearing when changing scenes, joining tournaments, entering disguise missions, or using quest-specific party operations.
- [x] Prevent transfer loops that create negative troop counts.
- [x] Prevent capacity calculations from reading uninitialized companion slots.

## Integration Points To Audit

Party size and recruitment:

- [x] `src/scripts/ZA_hardcoded_game_scripts/game_get_party_companion_limit.py`
- [x] Village recruitment flows.
- [x] Tavern mercenary hiring flows.
- [x] Freed captive recruitment flows.
- [x] Prisoner recruitment flows.
- [x] Quest reward troop flows.
- [x] Any direct `party_get_free_companions_capacity` checks.

Economy and morale:

- [x] `src/scripts/ZB_economy_and_trade/calculate_player_faction_wage.py`
- [x] `src/scripts/ZA_hardcoded_game_scripts/game_get_troop_wage.py`
- [x] `src/scripts/ZC_parties/get_player_party_morale_values.py`
- [x] Company accounts/report scripts.
- [x] Food consumption and starvation checks.
- [x] Player gold transfer and treasury scripts.
- [x] Weekly budget, payroll, and arrears scripts.
- [x] Troop upgrade cost scripts.
- [x] Training scripts.

Battle and parties:

- [x] Nearby-party battle join scripts.
- [x] Player defeat/capture scripts.
- [x] Siege attack/defense setup.
- [x] Village raid defense setup.
- [x] Quest mission templates that assume only `p_main_party` matters.
- [x] External follower party scripts, to keep retinues separate from mercenary/patrol command systems.

Companion lifecycle:

- [x] Companion hiring/joining dialogue.
- [x] Companion departure dialogue.
- [x] Companion grievance and reconciliation scripts.
- [x] Companion personal quest absence/cleanup.
- [x] Company report and companion report scripts.
- [x] Companion depth role payoff scripts.

## Implementation Phases

### Phase 1 - Architecture And Static Guardrails

- [x] Add constants, slots, state names, and party template.
- [x] Add retinue ensure/repair/cleanup scripts.
- [x] Add capacity script.
- [x] Add size/free-capacity scripts.
- [x] Add static tests for constants, slots, template, and helper registration.
- [x] Add old-save repair test coverage.

### Phase 2 - Storage And Transfer

- [x] Create retinue parties for companions in the main party.
- [x] Add camp/company retinue overview.
- [x] Add companion dialogue entry.
- [x] Add assign/reclaim transfer flow.
- [x] Add give/withdraw command-purse gold flow.
- [x] Add no/half/full strength order flow.
- [x] Validate troop stack movement between `p_main_party` and companion retinue party.
- [x] Block invalid troop types and absent companions.
- [x] Add static tests for all transfer restrictions.

### Phase 3 - Capacity And Player Party Limit

- [x] Wire companion capacity to stats and relationship.
- [x] Add player effective-size/capacity helpers if needed.
- [x] Patch recruitment/captive/hire flows so retinue capacity is offered deliberately, not accidentally.
- [x] Update party-size report text to show player-commanded vs companion-commanded troops.
- [x] Add static tests that retinue troops do not count against player personal cap.
- [ ] Add manual QA for recruiting when main party is full but a companion has free retinue space.

### Phase 4 - Wages, Food, Morale, And Reports

- [x] Include retinues in wages.
- [x] Charge retinue wages through companion purses first.
- [x] Add weekly companion command-cost invoice lines.
- [x] Add command-purse shortage consequences.
- [x] Include retinues in food/supply pressure.
- [x] Include retinues in morale pressure.
- [x] Add report breakdown by companion.
- [x] Add purse, wage reserve, and strength order to report breakdown.
- [x] Add over-capacity morale warning.
- [x] Add static tests for no double-charge and no free upkeep.

### Phase 5 - Autonomous Recruitment And Training

- [x] Implement no/half/full target-size calculation.
- [x] Implement autonomous recruiting from companion purse.
- [x] Implement autonomous upgrades from companion purse.
- [x] Implement post-battle leftover troop hiring.
- [x] Respect companion troop preferences.
- [x] Respect location/culture/recruitment availability.
- [x] Respect wage reserve and low-purse constraints.
- [x] Respect no-troops order and suspended command states.
- [x] Add static tests for no autonomous recruitment when blocked.
- [ ] Add manual QA for a companion growing from empty to half and half to full.

### Phase 6 - Battle Integration

- [x] Choose battle bridge: hidden ally join or temporary battle merge/restore.
- [x] Implement one battle bridge only after confirming it works.
- [x] Apply casualties back to the owning retinue.
- [x] Prevent duplicate spawn/counting.
- [x] Add static tests around battle setup calls.
- [ ] Add manual QA battle matrix.

### Phase 7 - Relationship Consequences

- [x] Add approval/cohesion capacity modifiers.
- [x] Add warning/grievance penalties.
- [x] Add personal quest outcome modifiers.
- [x] Add relationship effects on willingness to run full-strength retinues.
- [x] Add relationship effects on command-purse trust, refusal, and departure handling.
- [x] Add departure/capture consequences.
- [x] Add companion-specific flavor lines.
- [x] Add report warnings for strained command.

### Phase 8 - Polish And Regression

- [x] Add all companion preference text.
- [x] Add retinue status to company report.
- [x] Add retinue status to companion report.
- [x] Polish transfer menu text.
- [x] Polish refusal and warning dialogue.
- [x] Run full static and build validation.
- [ ] Run manual QA for at least three companions: one martial, one support, one unstable/low-trust.

## Static Test Plan

Add `build/test_companion_retinue_static.py`.

- [x] Assert retinue constants and slots exist.
- [x] Assert `pt_sod_companion_retinue` exists.
- [x] Assert `spt_companion_retinue` exists.
- [x] Assert retinue parties are not accepted by external follower command dialogue.
- [x] Assert capacity script does not reference player Leadership/Charisma/renown.
- [x] Assert transfer scripts guard companion presence.
- [x] Assert transfer scripts reject heroes and invalid troops.
- [x] Assert command-purse add/remove scripts cannot create negative or duplicate gold.
- [x] Assert no/half/full strength order constants and setter script exist.
- [x] Assert autonomous recruitment respects no-troops order.
- [x] Assert autonomous recruitment uses companion purse, not direct player gold.
- [x] Assert autonomous recruitment keeps a wage reserve.
- [x] Assert post-battle hiring does not take player-selected troops.
- [x] Assert departure cleanup calls retinue cleanup.
- [x] Assert wage script includes retinue parties.
- [x] Assert wage script supports companion command-cost invoice lines.
- [x] Assert morale/food scripts either include retinues or explicitly call a retinue helper.
- [x] Assert recruitment flows do not blindly treat retinue capacity as main-party capacity.
- [x] Assert battle integration path has no duplicate retinue counting marker.
- [x] Assert old-save repair script exists and is called from a safe startup/daily path.

Focused validation:

- [x] `py build\test_companion_retinue_static.py`
- [x] `py build\test_companion_depth_system.py`
- [x] `py build\test_external_follower_parties_static.py`
- [x] `py build\test_dialogue_immersion_static.py`
- [x] `py build\doctor.py --doctor-new-only`

Build validation:

- [x] `py build\build_constants.py`
- [x] `py build\build_scripts.py`
- [x] `py build\build_dialogs.py`
- [x] `py build\build_game_menus.py`
- [x] Party-template output is regenerated through `py build\build_all.py` in this repo; no standalone `build_party_templates.py` exists.
- [x] `py build\build_all.py`

## Manual QA Matrix

- [ ] Start a new game and recruit a companion.
- [ ] Confirm retinue starts empty and inactive.
- [ ] Assign one troop stack to a companion retinue.
- [ ] Confirm player party size decreases or remains under cap as intended.
- [ ] Reclaim the troop stack.
- [ ] Attempt to reclaim when player party is full.
- [ ] Assign troops up to exact capacity.
- [ ] Attempt to assign over capacity.
- [ ] Give gold to a companion's command purse.
- [ ] Withdraw unused gold from a companion's command purse.
- [ ] Set a companion to no troops and confirm they stop recruiting/replacing losses.
- [ ] Set a companion to half strength and confirm they maintain near half capacity.
- [ ] Set a companion to full strength and confirm they recruit toward capacity when funded.
- [ ] Confirm a companion refuses or warns when ordered to full strength at low relationship.
- [ ] Confirm post-battle leftover troop hiring only happens when enabled, funded, and under target size.
- [ ] Lower companion relationship and confirm reduced capacity/warning behavior.
- [ ] Resolve a companion personal quest positively and confirm capacity/status change.
- [ ] Enter a field battle and confirm retinue troops fight once.
- [ ] Take casualties and confirm retinue troop counts update.
- [ ] Pay weekly wages and confirm retinue wages are included.
- [ ] Pay weekly wages and confirm the companion purse is charged first.
- [ ] Empty the command purse and confirm shortage behavior is clear.
- [ ] Consume food over time and confirm retinue supply pressure is included.
- [ ] Trigger companion departure and confirm retinue resolution.
- [ ] Trigger companion departure and confirm purse resolution.
- [ ] Save/load with active retinue and confirm storage repairs correctly.
- [ ] Verify external follower party dialogue does not appear for retinue parties.

## Definition Of Done

- [x] Retinues use real troop-stack storage, not only variables.
- [x] Retinues feel internal to the player company, not like visible external followers.
- [x] Companion stats and relationship determine capacity.
- [x] The player can fund companion command purses.
- [x] The player can set no, half, or full retinue strength orders.
- [x] Funded companions can recruit, train, and hire eligible leftover troops according to orders.
- [x] Retinue troops do not count against the player's personal party-size limit.
- [x] Retinue troops still count for battle, wages, supply, and morale pressure.
- [x] Companion retinue wages appear as a single command cost in the primary wage summary.
- [x] All transfer paths are guarded against invalid troops, absent companions, and over-capacity errors.
- [x] All treasury paths are guarded against negative gold, duplicate gold, and unintended spending.
- [x] Companion departure/capture/failure cannot orphan or duplicate retinue troops.
- [x] Reports explain the system clearly.
- [x] Static tests cover constants, storage, capacity, transfer, cleanup, wages, and command-dialogue separation.
- [x] Build output regenerates cleanly.
- [ ] Manual QA confirms at least one normal battle, one siege/village edge case, one departure case, and one save/load repair case.
