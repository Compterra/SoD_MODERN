# Mercenary Guild Economy Overhaul Checklist

## Vision

Mercenary guilds should behave like competing military institutions rather than infinite shops. Guilds compete for contracts, kingdoms compete for guild support, and the player can influence that market through money, reputation, warfare, patronage, and sabotage.

The overhaul should preserve each guild's personality while centralizing the shared economic rules. The Black Army should not feel like the Boar Clan. The Slavers should not feel like the Elephant Guard. But all guilds should participate in a readable contract economy with supply, demand, price, debt, manpower, support capacity, and active obligations.

## Core Design Rules

- [ ] Preserve seven distinct guild identities.
- [ ] Centralize accounting, not personality.
- [ ] Use weekly pulses for major market decisions.
- [ ] Avoid daily auction spam or opaque churn.
- [ ] Make supply scarce enough that contracts matter.
- [ ] Let player and AI kingdoms compete for the same broad support capacity.
- [ ] Keep player-facing reports clear before adding complex consequences.
- [ ] Keep menus/reports for ledger status; use dialogue for negotiation flavor.
- [ ] Prevent the guild economy from creating infinite troops, gold, relation, or safe power.
- [ ] Preserve existing save behavior where practical, but do not let legacy values poison new ledgers.

## Terminology Cleanup

- [ ] Define `Guild pact`: ongoing political/support arrangement with a guild.
- [ ] Define `Hired company`: an external player-commanded mercenary party.
- [ ] Define `Kingdom service`: the player serving a realm as a mercenary.
- [ ] Define `AI contract`: a guild company hired by an AI lord or kingdom.
- [ ] Define `Support party`: mercenary lord, patrol, caravan escort, supply column, or other guild-backed world party.
- [ ] Update report language to avoid using "contract" for every mercenary relationship.
- [ ] Audit all visible strings using "contract", "pact", "service", "company", and "mercenaries".

## Phase 1: Constants, Slots, And Ledger Foundation

### Guild Ledger Slots

- [x] Add `slot_faction_sod_merc_treasury`.
- [x] Add `slot_faction_sod_merc_manpower`.
- [x] Add `slot_faction_sod_merc_veterans`.
- [x] Add `slot_faction_sod_merc_elite_stock`.
- [x] Add `slot_faction_sod_merc_contract_load`.
- [x] Add `slot_faction_sod_merc_support_capacity`.
- [x] Add `slot_faction_sod_merc_active_contracts`.
- [x] Add `slot_faction_sod_merc_recovery_rate`.
- [x] Add `slot_faction_sod_merc_risk_tolerance`.
- [x] Add `slot_faction_sod_merc_market_reputation`.
- [x] Add `slot_faction_sod_merc_price_pressure`.
- [x] Add `slot_faction_sod_merc_last_market_day`.
- [x] Add `slot_faction_sod_merc_last_settlement_day`.
- [x] Add `slot_faction_sod_merc_last_report_flags`.

### Kingdom Demand Slots

- [x] Add `slot_faction_sod_merc_demand_score`.
- [x] Add `slot_faction_sod_merc_budget`.
- [x] Add `slot_faction_sod_merc_max_bid`.
- [x] Add `slot_faction_sod_merc_preferred_guild`.
- [x] Add `slot_faction_sod_merc_contract_need_type`.
- [x] Add `slot_faction_sod_merc_contract_urgency`.
- [x] Add `slot_faction_sod_merc_last_bid_day`.
- [x] Add `slot_faction_sod_merc_last_hired_guild`.

### Contract Slots

- [ ] Decide whether contracts are represented by faction slots, party slots, or a pseudo-array.
- [x] Add `slot_party_sod_merc_contract_employer`.
- [x] Add `slot_party_sod_merc_contract_guild`.
- [x] Add `slot_party_sod_merc_contract_value`.
- [x] Add `slot_party_sod_merc_contract_wage_rate`.
- [x] Add `slot_party_sod_merc_contract_term_end`.
- [x] Add `slot_party_sod_merc_contract_role`.
- [x] Add `slot_party_sod_merc_contract_quality`.
- [x] Add `slot_party_sod_merc_contract_replenishment_level`.
- [x] Add `slot_party_sod_merc_contract_market_id` if a persistent contract id is needed.

### Contract Role Constants

- [x] Add `sod_merc_contract_role_field_company`.
- [x] Add `sod_merc_contract_role_patrol`.
- [x] Add `sod_merc_contract_role_escort`.
- [x] Add `sod_merc_contract_role_supply_column`.
- [x] Add `sod_merc_contract_role_mercenary_lord`.
- [x] Add `sod_merc_contract_role_garrison_support`.
- [x] Add `sod_merc_contract_role_special_world_activity`.

### Market Mode Constants

- [x] Add `sod_merc_buyer_player`.
- [x] Add `sod_merc_buyer_ai_lord`.
- [x] Add `sod_merc_buyer_ai_kingdom`.
- [x] Add `sod_merc_buyer_guild_internal`.
- [x] Add `sod_merc_contract_term_monthly`.
- [x] Add `sod_merc_contract_term_quarterly`.
- [x] Add `sod_merc_contract_term_campaign`.

## Phase 2: Guild Profile And Access Helpers

- [x] Add `script_sod_merc_guild_get_profile(guild)`.
- [x] Return base, master, representative, tier unit 1, tier unit 2, noble, proportion, price factor, elite requirement.
- [x] Add `script_sod_merc_guild_get_roster(guild)`.
- [x] Add `script_sod_merc_guild_get_access_level(guild, buyer_faction)`.
- [x] Add `script_cf_sod_faction_is_merc_guild(faction)`.
- [x] Add `script_cf_sod_merc_guild_uses_classic_employer_rotation(guild)`.
- [x] Add `script_cf_sod_merc_guild_uses_world_presence(guild)`.
- [x] Replace magic guild ranges where they encode behavior rather than true range iteration.
- [ ] Preserve existing `guilds_begin` and `guilds_end` for broad iteration.

## Phase 3: Ledger Initialization And Repair

- [x] Add `script_sod_merc_guild_initialize_ledger(guild)`.
- [x] Initialize all seven guild ledgers in `game_start`.
- [x] Seed starting treasury per guild.
- [x] Seed starting manpower per guild.
- [x] Seed starting veteran and elite stock per guild.
- [x] Seed support capacity per guild.
- [x] Seed risk tolerance per guild.
- [x] Seed recovery rate per guild.
- [x] Add `script_sod_merc_guild_repair_ledgers`.
- [x] Run repair before reports and before weekly market pulse.
- [x] Clamp negative treasury to zero unless debt is intentionally represented separately.
- [x] Clamp manpower/veterans/elite stock to valid ranges.
- [x] Clamp active contracts/support load to non-negative values.
- [x] Recount active support parties when ledger counts look desynced.

## Phase 4: Kingdom Demand Model

### Demand Inputs

- [x] Add `script_sod_merc_market_calculate_kingdom_demand(faction)`.
- [x] Include active wars.
- [ ] Include recent defeats.
- [x] Include faction current power compared to enemies.
- [x] Include active marshal campaign needs.
- [x] Include treasury or lord wealth proxies.
- [x] Include number of active lords in the field.
- [x] Include nearby hostile pressure from village looter pressure and recent militia/garrison losses.
- [x] Include village raid pressure and wealthy village patrol demand.
- [x] Include existing guild pact.
- [x] Include kingdom-to-guild relation weighting.
- [x] Reduce demand if already over-supported by mercenaries.
- [x] Let low population plus high lord wealth create gold-for-manpower mercenary demand.
- [x] Make lord wealth materially affect kingdom mercenary budget and bid ceiling.
- [x] Make accepted AI kingdom contracts drain actual ruler/lord wealth after a successful payment preflight.
- [x] Make contract success and losses adjust kingdom-to-guild relation and guild price pressure.
- [x] Exclude inactive, defeated, eliminated, or invalid factions.
- [x] Exclude `fac_kingdom_6` if the design still wants IEF out of this market.

### Demand Types

- [x] Add field-company demand.
- [x] Add patrol/security demand.
- [x] Add escort/trade protection demand.
- [x] Add garrison support demand.
- [x] Add campaign surge demand.
- [x] Add special guild demand hooks for wealthy/threatened village patrol activity.
- [x] Add special guild demand hooks for caravans lost, threat-board activity, and roaming mini-faction pressure.

### Budget

- [x] Add `script_sod_merc_market_calculate_kingdom_budget(faction)`.
- [x] Use faction wealth if available.
- [x] Use ruler wealth as fallback.
- [x] Use prosperity/economic strength as fallback if wealth is weak.
- [x] Set max bid from budget and urgency.
- [x] Prevent AI kingdoms from spending themselves into unrecoverable collapse.
- [x] Let desperate kingdoms overspend cautiously.

## Phase 5: Guild Supply Model

### Supply Inputs

- [x] Add `script_sod_merc_market_calculate_guild_supply(guild)`.
- [x] Include manpower.
- [x] Include veterans.
- [x] Include elite stock.
- [x] Include treasury.
- [x] Include current contract load.
- [x] Include support capacity.
- [x] Include recent losses.
- [x] Include world activity pressure.
- [x] Include player relation and kingdom relations.
- [x] Include guild-specific risk tolerance.

### Supply Outputs

- [x] Return available company count.
- [x] Return max company size.
- [x] Return available quality tier.
- [x] Return price pressure.
- [x] Return willingness to accept long contracts.
- [x] Return willingness to accept dangerous contracts.
- [x] Return refusal reason if supply is too low.

### Recovery

- [x] Add weekly manpower recovery.
- [x] Add veteran recovery from successful contracts.
- [x] Add elite recovery slowly and sparingly.
- [x] Add treasury income from active contracts.
- [x] Add treasury drain from losses and overextension.
- [x] Add treasury drain from special world activity.
- [x] Let guild world systems feed ledger values without being rewritten.

## Phase 6: Contract Matching Pulse

### Weekly Market Pulse

- [x] Add `script_sod_merc_market_weekly_pulse`.
- [x] Run after kingdom war/diplomacy updates but before new mercenary support spawns.
- [x] Repair ledgers before matching.
- [x] Calculate kingdom demand for each eligible kingdom.
- [x] Calculate guild supply for each guild.
- [x] Generate bids.
- [x] Rank bids by value, relation, urgency, risk, and guild preference.
- [x] Let guilds accept best suitable bids.
- [x] Update kingdom demand slots.
- [x] Update guild contract load and treasury commitments.
- [x] Spawn or reassign parties after contract acceptance.
- [x] Update reports/notes.

### Bid Rules

- [x] Add `script_sod_merc_market_generate_bid(kingdom, guild, demand_type)`.
- [x] Use kingdom max bid.
- [x] Apply guild price pressure.
- [x] Apply existing pact discount or priority.
- [x] Apply hostility surcharge.
- [x] Apply overextension surcharge.
- [x] Apply long-contract surcharge.
- [x] Apply danger surcharge.
- [x] Reject if kingdom cannot afford minimum bid.
- [x] Reject if guild refuses the work.

### Acceptance Rules

- [x] Add `script_sod_merc_market_try_accept_bid(guild, kingdom, bid_value, demand_type)`.
- [x] Require guild supply.
- [x] Require support capacity.
- [x] Require contract value above guild minimum.
- [x] Prefer existing employer if relationship is strong.
- [x] Prefer player if player relation and payment history are excellent.
- [x] Allow rich rivals to outbid the player if player standing is weak.
- [x] Prevent one kingdom from monopolizing every guild unless it can truly afford it and supply exists.

## Phase 7: Player Competition And Negotiation

### Player Hire Quote Integration

- [x] Route player company hire quote through the market pricing helper.
- [x] Show whether the guild is overcommitted.
- [x] Show whether player standing improves priority.
- [x] Show whether another kingdom currently has priority.
- [x] Show up-front retainer.
- [x] Show estimated weekly field wages.
- [x] Show replenishment quality.
- [x] Show contract term.
- [x] Show availability limits.

### Player Bidding

- [x] Add optional "outbid current employer" path only after baseline system works.
- [x] Let player pay premium to jump queue.
- [x] Let high relation reduce or waive queue premium.
- [x] Let low relation block queue jumping.
- [ ] Let breaking another kingdom's contract create diplomatic or relation consequences.

### Player Pact Integration

- [x] Make guild pacts consume support capacity.
- [x] Make guild pacts improve player bid priority.
- [x] Make missed payments reduce player priority.
- [x] Make repeated missed payments increase prices and reduce replenishment.
- [x] Make debt visible in the Mercenary Ledger report.

## Phase 8: AI Hire And Renewal Refactor

- [x] Route `script_ai_hire_mercenaries` through shared market demand and bid helpers.
- [x] Route `script_cf_spawn_ai_mercs` through shared roster/quality helpers.
- [x] Split `script_merc_party_change_state` into renewal, reassignment, and disband helpers.
- [x] Use shared renewal pricing for AI companies.
- [x] Let AI companies renew only if employer budget and guild willingness allow it.
- [x] Let AI companies seek another employer if current employer cannot pay.
- [x] Let companies return to guild base when no contract exists.
- [x] Let overextended guilds refuse renewals.
- [x] Preserve existing anti-player-clone safeguards.

## Phase 9: Player-Hired Company Lifecycle

- [x] Keep player-hired companies as `spt_player_mercenaries`.
- [x] Preserve external follower command behavior.
- [x] Decide final model: retainer plus wages, or all-inclusive contract.
- [x] If retainer plus wages:
  - [x] Rename hire cost text to retainer.
  - [x] Show weekly wage estimate before hire.
  - [x] Keep `spt_player_mercenaries` in weekly wage calculation.
- [ ] If all-inclusive:
  - [ ] Remove or reduce weekly wages for player mercenary companies.
  - [ ] Increase contract quote and renewal cost.
  - [ ] Reduce free replenishment if price becomes too generous.
- [x] Use guild ledger manpower for company replenishment.
- [x] Stop daily free replenishment if guild manpower is exhausted.
- [x] Make higher relation improve replenishment priority.
- [x] Make unpaid debt weaken or pause replenishment.

## Phase 10: Mercenary Lords And Support Parties

- [x] Tie mercenary lord spawn eligibility to guild support capacity.
- [x] Tie mercenary lord spawn quality to guild veteran/elite stock.
- [x] Tie mercenary lord employer to accepted market contracts.
- [x] Count active mercenary lords against guild contract load.
- [x] Let guilds with low treasury avoid sending named leaders.
- [x] Let defeated mercenary lords damage guild reputation/manpower.
- [x] Let successful mercenary lords improve guild market reputation.
- [x] Show active mercenary lords in guild ledger reports.

## Phase 11: World Activity Integration

### Black Army

- [x] Feed security fund into guild treasury or pressure.
- [x] Make contract heat affect demand for patrol/security work.
- [x] Let strong Black Army employment reduce road-threat pressure near employer territory.
- [x] Let overcommitment raise prices.

### Conquistadors

- [x] Feed supplies into contract readiness.
- [x] Make requisition heat increase manpower but anger local economies.
- [x] Let rich kingdoms prefer Conquistador supply contracts.

### Elephant Guard

- [x] Feed devotion/supplies/omens into support quality and refusal rules.
- [x] Let high slaver alarm increase their anti-slaver contract preference.
- [x] Let sanctuary commitments reduce availability for ordinary field contracts.

### Jotnar Clan

- [x] Feed hearth pressure into willingness to leave home territory.
- [x] Let hearth stores increase recovery.
- [x] Let threatened villages reduce available manpower.

### Serpent Host

- [x] Feed route intelligence into escort and scouting contract value.
- [x] Let safe passage reduce risk surcharge.
- [x] Let overused routes reduce willingness to accept long contracts.

### Slavers

- [x] Feed demand/supply/heat into treasury and risk.
- [x] Let high heat increase danger surcharge.
- [x] Let prisoner economy affect their manpower and cash.
- [x] Keep moral/relation consequences distinct and visible.

### Boar Clan

- [x] Feed tribute and intimidation into treasury/risk tolerance.
- [x] Let frontier pressure increase toll-band activity.
- [x] Let high intimidation improve short-term support but hurt diplomacy.

## Phase 12: Reports And Dialogue

### Mercenary Ledger Report

- [x] Add `script_sod_merc_market_describe_overview_to_sXX`.
- [x] Add `script_sod_merc_guild_describe_ledger_to_sXX(guild)`.
- [x] Add a report menu for the mercenary market.
- [x] Show each guild's availability: plentiful, stretched, overcommitted, depleted.
- [x] Show each guild's price pressure.
- [x] Show active employer or top contract.
- [x] Show player standing.
- [x] Show player debt.
- [x] Show whether the player has priority.
- [x] Show why a guild refuses work.

### Kingdom Reports

- [x] Show which kingdoms are actively bidding for mercenaries.
- [x] Show which kingdoms are over-reliant on mercenaries.
- [x] Show which guilds are currently backing which kingdoms.
- [x] Show when a guild switches employer.

### Dialogue Polish

- [x] Guild masters should mention market state in dialogue.
- [x] Guild masters should react to player debt.
- [x] Guild masters should react to player victories against their rivals.
- [x] Guild masters should react when their companies were destroyed by the player.
- [x] High-standing dialogue should sound preferential.
- [x] Low-standing dialogue should sound transactional or wary.
- [x] Avoid making economic negotiation a menu-only experience.

## Phase 13: Balance Guardrails

- [x] Prevent guild treasury from creating infinite money.
- [x] Prevent manpower recovery from creating infinite free troops.
- [x] Prevent a single guild from supporting every active kingdom at full strength.
- [x] Prevent player pacts from granting unlimited discounts.
- [x] Prevent repeated missed payments from being harmless.
- [x] Prevent active contract count from desyncing after party defeat.
- [x] Prevent spawned mercenary parties from missing guild ownership slots.
- [x] Prevent destroyed parties from failing to apply manpower/treasury losses.
- [x] Prevent AI kingdoms from bankrupting themselves every week.
- [x] Prevent player from cheaply exhausting a guild then hiring it at exploit prices unless that is a deliberate risky bargain.
- [x] Prevent Slaver/Boar special economies from bypassing market limits if they create player-hired companies.

## Phase 14: Failure, Debt, And Consequences

- [x] Add missed payment consequence tiers.
- [x] Add debt threshold warnings.
- [x] Add debt-based price surcharge.
- [x] Add debt-based replenishment penalty.
- [x] Add debt-based refusal state.
- [x] Add relation loss for long unpaid debts.
- [x] Add contract cancellation rules.
- [x] Add guild retaliation or blacklisting only as a later, controlled feature.
- [x] Add player option to settle debt through gold.
- [x] Add player option to settle debt through service or dangerous guild work if desired later.

## Phase 15: Testing

### Static Tests

- [ ] Add `build/test_mercenary_market_static.py`.
- [ ] Assert new ledger slots exist.
- [ ] Assert all seven guilds initialize ledger values.
- [ ] Assert guild profile helper references all seven guilds.
- [x] Assert classic employer rotation uses a helper instead of magic `fac_sod_merc_guild6` end range.
- [x] Modernize legacy guild-employer fallback to score kingdoms by demand, budget, urgency, preferred guild, and kingdom-to-guild relation/history instead of assigning a random active kingdom.
- [x] Assert accepted AI kingdom contracts touch `slot_troop_wealth` and fully collect payment before accepting.
- [x] Assert contract outcome handling updates kingdom-to-guild relation and guild price pressure.
- [ ] Assert player hire quote routes through shared market quote helper.
- [ ] Assert AI hire routes through shared bid/market helper.
- [ ] Assert `spt_player_mercenaries` wage inclusion or exclusion matches chosen model.
- [ ] Assert reports distinguish kingdom service, hired company, and guild pact.
- [ ] Assert guild 6 and 7 special handling is explicit.

### Simulation Tests

- [ ] Add a small script-driven weekly pulse smoke test if practical.
- [ ] Verify a weak kingdom generates demand.
- [ ] Verify a rich kingdom can outbid a weak kingdom.
- [ ] Verify an overcommitted guild raises price or refuses.
- [ ] Verify player pact improves priority.
- [ ] Verify player debt hurts priority.
- [ ] Verify contract load decreases when a party is destroyed or expires.
- [ ] Verify guild manpower decreases when companies spawn.
- [ ] Verify guild manpower recovers slowly.

### Build Validation

- [ ] Run `py build\doctor.py --doctor-new-only`.
- [ ] Run relevant static tests.
- [ ] Run `py build\build_all.py`.
- [ ] Run `cmd /c build_module.bat --no-cache` before considering the overhaul shippable.

## Phase 16: Manual QA

- [ ] Start a new campaign and check initial guild ledger values.
- [ ] Let several weekly pulses pass and confirm kingdoms hire different guilds.
- [ ] Join a kingdom as a mercenary and confirm reports use "kingdom service" language.
- [ ] Hire a player external company and confirm quote/wage/contract text is clear.
- [ ] Maintain a guild pact and confirm fee/debt/report behavior.
- [ ] Miss pact payments and confirm consequences are visible.
- [ ] Destroy an AI mercenary company and confirm guild manpower/load update.
- [ ] Destroy a player-hired company and confirm no orphan contract remains.
- [ ] Watch Slaver and Boar Clan special activity to ensure they remain distinct.
- [ ] Verify reports stay readable and not spammy.

## Preferred Implementation Order

1. Add ledger slots, helpers, and repair scripts with no balance changes.
2. Add report/readout improvements so the market is visible.
3. Add shared quote helpers while preserving current prices.
4. Route player hire and renewal through the shared quote layer.
5. Route AI hiring and renewal through the shared quote layer.
6. Add weekly demand/supply pulse.
7. Connect accepted bids to actual support parties.
8. Connect world activity systems to ledger inputs.
9. Rebalance prices, wages, replenishment, and debt after the system is visible.

## Design Decision Still Needed

- [ ] Decide whether player-hired external companies are retainer plus weekly wages.
- [ ] Decide whether player-hired external companies are all-inclusive contracts.
- [ ] Decide whether guild manpower limits player company replenishment immediately or after a grace period.
- [ ] Decide how aggressively AI kingdoms should compete against the player.
- [ ] Decide whether breaking another kingdom's guild contract is allowed.
- [ ] Decide whether guilds can become hostile economic actors if betrayed or ruined.

## Definition Of Done

- [ ] Guilds have readable ledger state.
- [ ] Kingdoms generate understandable demand.
- [ ] Guilds accept or refuse contracts based on supply, price, risk, and relation.
- [ ] Player and AI compete for mercenary availability.
- [ ] Existing guild identities remain distinct.
- [ ] Hired company pricing is clear to the player.
- [ ] Weekly wages and contract fees no longer feel like hidden double-charging.
- [ ] Reports explain market state without drowning the player.
- [ ] Static tests cover the central rules.
- [ ] Build validation passes.
