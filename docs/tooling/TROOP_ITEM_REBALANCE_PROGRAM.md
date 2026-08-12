# Troop and Item Rebalance Program

## Status

- [x] Phase 0 source audit completed.
- [x] Theme-preserving roster inventory and progression tools added to the Balance Lab.
- [x] Campaign-cohort and Imperial-invasion evidence tools added to prevent
  mutually exclusive player cultures and the delayed invasion from being
  flattened into a fake faction average.
- [ ] No troop, item, price, wage, proficiency, or inventory record has been changed by this program yet.
- [ ] Do not begin balance edits until the Phase 1 baseline and scenario measurements are captured.

This is a progression-first rebalance. The aim is not to make every faction
numerically symmetrical. It is to make the route from recruit to elite
understandable, economically sustainable, and challenging while preserving the
equipment identity that makes each troop and faction recognizable.

The supplied forum discussion is useful problem context, but it was not
available to the repository tooling at audit time. Conclusions below are
therefore based on checked-in game source and must be checked against a
reproducible playthrough before any values change.

## Source Evidence

The current analysis is grounded in these authoring sources:

- `compile/module_troops.py`: direct troop records, explicit normal/noble
  `upgrade()` routes, `sod_noble_troops`, and `sod_faith_troops`.
- `compile/module_items.py`: direct item records and item economy data.
- `compile/module_party_templates.py`: native, SoD, and Imperial
  reinforcement-template composition.
- `src/scripts/ZD_centers/cf_village_recruit_volunteers_cond.py` and
  `src/scripts/ZD_centers/village_recruit_volunteers_recruit.py`: recruitment,
  relationship, village-state, cost, capacity, and population limits.
- `src/scripts/ZC_parties/cf_party_upgrade_with_xp.py` and
  `src/scripts/ZY_helper_scripts/sod_troop_can_upgrade_at_center.py`: XP,
  cost, center context, faction permission, and facility gates.
- `src/scripts/ZY_helper_scripts/sod_troop_get_faith_upgrade.py` and
  `src/scripts/ZY_helper_scripts/sod_troop_can_faith_ascend_at_center.py`:
  noble-to-faith ascension and its special gates.
- `src/scripts/ZY_helper_scripts/sod_troop_get_upgrade_cost.py`: upgrade cost
  multipliers, mounted cost, doctrine effects, scarcity, and center effects.
- `src/scripts/ZC_parties/sod_party_training_maintenance.py` and
  `src/scripts/ZD_centers/sod_center_training_maintenance.py`: AI party,
  garrison, trainer, and facility-driven XP sources.
- `src/scripts/ZZ_common_array_processing/update_center_population_supply.py`
  and `src/scripts/ZY_helper_scripts/sod_population_based_construction.py`:
  population, health, food, labor, construction, and garrison feedback.
- `src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_demand.py`
  and `src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_budget.py`:
  mercenary demand as a reaction to war, manpower, wealth, population, health,
  food, and outbreaks.
- `src/triggers/ST03_daily/entry_0088.py`,
  `src/scripts/ZY_helper_scripts/sod_imperial_expedition.py`, and
  `src/scripts/ZA_hardcoded_game_scripts/game_start.py`: Imperial
  pre-invasion staging, wave binding, pressure/supply, total-war, and
  coalition-counterplay behavior.

## Actual Progression Loop

### 0. Campaign Cohorts and Comparison Boundaries

1. Antarian, Marinian, Adenian, Villianese, and Zerrikanian are five
   mutually exclusive player-start cultures. One is selected when a campaign
   begins; the other four do not coexist as player, AI, allied, or enemy
   rosters in that run.
2. Their shared runtime `fac_player_supporters_faction` ownership is an
   implementation detail, not a balance cohort. Each culture remains a
   separate theme, economy, access, and progression baseline.
3. Native kingdoms are persistent world realms and should be reviewed as a
   separate group adjacent to the chosen SoD culture, not mixed into a
   player-culture average.
4. The Imperial Expedition is a delayed endgame invasion. Its quality must be
   judged through arrival timing, advance auxiliaries, reinforcement waves,
   total-war posture, supply, pressure, attrition, and coalition counterplay,
   not a one-for-one faction roster average.

### Implemented Balance Slice: Adenian Loadout Reliability

- [x] Give Adenian Archers the plain round shield already used by the culture's
  regular infantry, matching their existing `tf_guarantee_shield` contract.
- [x] Give Adenian Veteran Archers the kite shield already used by the culture's
  elite archers, retaining a visible equipment progression rather than adding a
  foreign item theme.
- [x] Replace the duplicate medium-cavalry lance inventory entry with a standard
  sword fallback. The troop still carries its lance and shield, but no longer
  risks entering sustained melee with only a lance.
- [x] Guard all five player-start culture cohorts against high-severity missing
  weapon, mount, and guaranteed-shield inventory contracts.

This is a reliability correction, not a wholesale stat increase: no troop
levels, skills, proficiencies, item statistics, recruitment rules, wages, or
upgrade costs were changed in this slice.

### Implemented Balance Slice: Player Reinforcements and Faith Ascension

- [x] Reprofile the five mutually exclusive player-start cultures through the
  actual reinforcement selection weights: center garrisons use A 65% / B 35%
  and kingdom hero parties use A 50% / B 25% / C 25%.
- [x] Correct the Zerrikanian player activation binding so its common garrison
  reinforcement slot favors the infantry/ranged template and its regular
  mounted template no longer injects elite cavalry and nobles at the old rate.
  The bounded static garrison-pressure spread is now 1.329 (target <= 1.35),
  and the lord-pressure spread is 1.346 (target <= 1.35).
- [x] Repair the Boundless Wanderer's declared shield contract using the same
  `itm_steel_shield` already equipped by the other Enlightenment elite roles.
- [x] Add a full scripted faith-ascension audit. Every selected-culture
  Noble-to-Faith route now has a valid tier transition, no hard target
  loadout-contract failure, and at least one measurable elite premium while
  preserving role-specific doctrine trades.
- [x] Audit every direct player-culture recruit, normal, and Noble upgrade.
  Each must raise level, preserve rank, keep a complete target loadout, and
  show a kit or training advantage; themed kit trades remain explicit.

These checks are static guardrails, not a substitute for live siege, economy,
or campaign testing.

### Implemented Balance Slice: Native Campaign Peers

- [x] Add a dedicated Native kingdom profile that reads the live
  `game_start.py` culture bindings, the A/B/C reinforcement templates, and the
  shared center/lord selection cadence. Native kingdoms coexist in a campaign,
  so they are evaluated as world peers rather than as mutually exclusive
  player-start alternatives.
- [x] Keep Native doctrine as a design constraint: Swadian cavalry shock,
  Vaegir bows, Khergit mounted pressure, Nord shield-and-axe infantry, and
  Rhodok pike/crossbow defense are compared without being made interchangeable.
- [x] Reduce Khergit A/B reinforcement rider volume while keeping both packages
  entirely mounted. Their static garrison-pressure spread is now 1.426 and
  lord-pressure spread is 1.322, both within the Native target of <= 1.45.
- [x] Audit all 39 direct Native upgrade routes. Every route raises level,
  preserves rank, reaches a complete target loadout, and has a kit or training
  advantage. Four themed kit-score dips are explicitly recorded as
  training-compensated role trades rather than treated as automatic stat buffs.

These checks are static guardrails, not a substitute for live map-speed,
casualty-replacement, siege, economy, or campaign testing.

### Implemented Balance Slice: Mercenary Contract Niches

- [x] Add one role-fit authority for the seven guilds so kingdom demand,
  preferred-guild selection, and bid scoring agree about the job a company is
  best suited to perform.
- [x] Keep the guilds asymmetric: Black Army security, Conquistador supply and
  siege support, Elephant Guard civic defense, Jotnar hearth defense, Serpent
  route work, Slaver capture work, and Boar frontier pressure each receive
  distinct preferred and deprioritized contract roles.
- [x] Shape AI contract companies around their accepted job by redistributing
  their existing base guild troops. The retained per-noble arithmetic and a
  specialist subtraction keep the final company size unchanged; no new troop,
  item, stat, or elite tier was introduced.
- [x] Resolve the deployable role before forming an AI company and reuse that
  resolver at deployment. Impossible patrol, garrison, and supply work becomes
  explicit field service before it selects a roster; mobile escort,
  mercenary-lord, and special work retain their distinct live role while they
  accompany an employer.
- [x] Preserve player mercenary menus and preview composition. A player hire
  never receives the field-AI fallback role or a hidden roster rewrite.
- [x] Make inquiry dialogue name the live guild specialty as well as the
  current assignment, so a player can tell why that company is on the map.
- [x] Add `mercenary-guilds` to the Balance Lab and MCP catalog. The report
  checks the demand-to-dialogue handoff, all seven themed rosters, and the
  fixed-size AI formation contract before roster data is rebalanced further.

These checks prove source wiring and role boundaries, not battle performance.
They still require campaign testing of costs, map speed, wages, casualties,
prisoner capture, and player counterplay before changing mercenary troop or
item statistics.

### 1. Recruitment and Early Survival

1. Village volunteers require a non-raided, non-looted, non-infested village,
   viable relations, party capacity, and available volunteers.
2. Available volunteers are capped by population above the village minimum.
3. Player country selection installs exactly one of the five SoD peasant roots:
   Antarian, Marinian, Adenian, Villianese, or Zerrikanian. Other recruitment
   paths include native and mercenary choices, but the four unselected SoD
   culture trees are not a simultaneous campaign population.
4. Recruitment costs gold and permanently spends local population. Early army
   growth is therefore constrained by money, map safety, relations, party room,
   and local demographic health rather than by troop level alone.

### 2. Normal Troop Progression

1. Recruits take normal cultural branches through the explicit troop tree.
2. Combat simulation, party training, garrison training, and center trainers
   produce XP. AI lords and garrisons use the same public upgrade resolver.
3. The requested target troop determines the training facility: barracks,
   range, stables, chapter, temple, or chapel as appropriate.
4. Upgrade permissions also account for target faction/original faction,
   guild-hall exceptions, blocked ranges, and special no-center-safe cases.
5. Upgrade cost is not simply level: mounted targets, troop doctrine, faith
   scarcity, and center context modify it.

Normal troops must therefore be balanced as accessible, scalable line troops.
They should carry a culture's core battlefield doctrine, but they do not need
to win every equal-number matchup against an elite access tier.

### 3. Holdings, Infrastructure, and the First-Castle Transition

1. A holding is not only income. Facilities unlock or accelerate specific
   troop paths, while trainers can add stack XP in player-owned centers.
2. Population affects recruitment, tax, labor, recovery, and construction.
3. Health, food security, prosperity, security, threats, unrest, and prisoner
   labor policy feed workforce and recovery outcomes.
4. A castle or town is thus a force-multiplier with maintenance burdens. Its
   garrison, economy, and facilities must all be considered when evaluating
   whether the first holding is a viable progression step.

### 4. Noble Progression

1. Noble routes are separate from ordinary recruit branches. The direct
   `sod_noble_troops` list is the source of truth for confirmed noble ranks.
2. Chapter houses gather noble recruits and form the infrastructure bridge
   between normal military growth and elite doctrine.
3. A noble-route entry is still classified as Noble for progression review,
   even when its final runtime rank marker appears on a later troop.

Nobles are deliberately a rank above normal troops. Their balance target is
greater quality, not universal dominance in every role or a reason to erase
normal line specialization.

### 5. Faith and Zealot Progression

1. Faith troops are defined by the direct `sod_faith_troops` list and are a
   rank above nobles.
2. Ascension is not a standard `upgrade()` edge. A top noble is selected
   through an authored `*` candidate troop template and mapped to a
   faith-specific result.
3. Ascension requires an eligible noble, sufficient effective faith, enough
   local faith support, a chapel or temple, sufficient institution strength,
   manageable faith tension, and adds holy burden.
4. Faith scarcity also affects their gold upgrade cost.

Faith/Zealot troops are intended as the best military access tier. Their
rarity, institutional requirements, holy burden, and noble input must remain
meaningful. They should not be balanced as bulk replacements for normal troops.

### 6. Mercenary and Campaign Economy Loop

1. Taverns, guild halls, player companies, and AI contract systems offer
   alternative manpower and specialist access.
2. AI mercenary demand reacts to war pressure, power gaps, campaign health,
   marshal readiness, unpaid lords, lord wealth, population shortage, food,
   health, outbreaks, active support, and patrol/world activity.
3. Mercenary balance must include availability, contract duration, pay, and
   employer budget, not just combat loadout.

## Balance Contract

- [ ] Preserve troop identity before optimizing raw scores. A troop's gear,
  silhouette, mounted/foot role, and cultural doctrine are constraints.
- [ ] Treat the five SoD player cultures as separate, mutually exclusive
  player-start roster families. Shared runtime faction membership is not
  permission to exchange their whole item pools or average their performance.
- [ ] Treat native kingdoms as a coexisting world group adjacent to the
  selected player culture, and treat the Imperial Expedition as a delayed
  invasion profile rather than a normal faction peer.
- [ ] Items may move or swap only within the same themed roster family unless a
  reviewed exception explicitly proves that cross-family use is intended.
- [ ] Use current roster-local equipment first. Create new items only when the
  existing faction pool cannot express the needed role without breaking theme.
- [ ] Keep normal, Noble, and Faith/Zealot access tiers distinct.
- [ ] Compare like battlefield roles before comparing numeric values: infantry
  with infantry, field cavalry with cavalry, archers with archers, and so on.
- [ ] Treat randomized inventory lists as pools. A highest-item score does not
  prove that every soldier spawns with the highest possible kit.
- [ ] Never use price, static kit score, or an outlier report as an automatic
  change order. Each is triage evidence that needs economy and playtest review.
- [ ] Do not reorder troop/item records, alter generated IDs, or edit exports.

## Balance Lab Workflow

The Balance Lab is read-only by default and reads the true legacy authoring
inputs. Start each work session with these commands:

```powershell
py -3 -B devkit/troop_item_balance/troop_item_balance.py summary
py -3 -B devkit/troop_item_balance/troop_item_balance.py roster-inventory
py -3 -B devkit/troop_item_balance/troop_item_balance.py progression
py -3 -B devkit/troop_item_balance/troop_item_balance.py campaign-cohorts
py -3 -B devkit/troop_item_balance/troop_item_balance.py imperial-invasion --include-auxiliaries
```

Inspect one culture before proposing a troop or item move:

```powershell
py -3 -B devkit/troop_item_balance/troop_item_balance.py roster-inventory --roster Antarian --troop-limit 180 --item-limit 220
py -3 -B devkit/troop_item_balance/troop_item_balance.py progression --roster Antarian --troop-limit 180 --edge-limit 220
```

`roster-inventory` exposes each troop's current inventory pool and labels every
item as `roster_local` or `shared_outside_roster`. `progression` separates
normal/noble explicit upgrade edges from the scripted faith ascension map and
summarizes level, kit, melee, ranged, armor, shield, and mount distributions by
rank and role.

`campaign-cohorts` records the run-level comparison boundary before a
balance claim is made. `imperial-invasion` reports the three actual
Imperial reinforcement templates, optional advance auxiliaries, and the
source contracts that make its campaign pressure and counterplay distinct.

## Implementation Checklist

### Phase 1: Establish the Baseline

- [ ] Export a read-only inventory and progression snapshot for every player
  culture, every native faction, every mercenary guild, and every faith roster.
- [ ] Record a campaign-cohort snapshot before comparing any two groups. Do
  not create an all-five-SoD-cultures average; select one player culture per
  scenario.
- [ ] Record an Imperial invasion profile before changing Imperial troops:
  core wave composition, advance auxiliary composition, doctrine modifier,
  pressure/supply behavior, total-war posture, centurion recovery, and
  coalition/sabotage counterplay.
- [ ] Measure a live pre-invasion campaign at 90, 60, and 30 days remaining.
  The static staging calculation is an upper bound only; record actual
  successful spawns, party sizes, casualties, despawns, player intervention,
  and whether the resulting pressure is understandable and survivable.
- [ ] For each roster, identify its intended primary, secondary, and weak
  battlefield roles from current troop names, equipment, mounts, and upgrade
  branches. Do not infer doctrine from one scalar score.
- [ ] Record recruit source, population cost, recruit cost, upgrade facilities,
  XP source, upgrade cost, wage, and availability for each line.
- [ ] Measure the first-castle scenario: garrison target, food, wage burn,
  population/recruit recovery, facility state, enemy pressure, and player
  party composition at the point the castle becomes difficult to hold.
- [ ] Measure the same scenario for at least one low-income, one mid-income,
  and one healthy/high-infrastructure holding.
- [ ] Capture AI lord and garrison upgrade results with `$g_sod_debug == 1` in
  representative peaceful, sieged, rich, and poor cases.
- [ ] Separate intentional rare/reward items from merchant economy items before
  comparing price to combat score.

### Phase 2: Define Item Economy Bands

- [ ] Build role-specific bands for melee weapons, polearms, bows, crossbows,
  thrown weapons, firearms, ammunition, shields, armor, horses, and utility
  items. Do not combine unlike item classes into one power curve.
- [ ] For every item class, document the relationship among price, availability,
  difficulty, performance, durability, weight, speed, reach, and damage type.
- [ ] Keep faction-exclusive materials, visual motifs, and weapon styles
  meaningful even where two items occupy equivalent economic bands.
- [ ] Flag items that are cheap and broadly available relative to their role
  peers, then validate them in spawned troop pools and shops before editing.
- [ ] Flag expensive but weak merchant items separately from intentionally free,
  quest, blacksmith, or nonmerchant items.
- [ ] Produce a reviewed item change sheet before applying any item patch.

### Phase 3: Rebalance Normal Lines by Culture

- [ ] Work one culture at a time: Antarian, Marinian, Adenian, Villianese, then
  Zerrikanian. Do not balance all five from an aggregate faction average.
- [x] Establish the coexisting Native kingdom static baseline from live A/B/C
  template bindings and direct upgrade routes. The current doctrine-preserving
  pressure bound is <= 1.45 for both garrison and lord reinforcement calls.
- [ ] Run live Native field, siege, and map-speed trials after the template
  correction. The static profile cannot measure the operational advantage of
  all-mounted Khergit parties or actual casualty replacement cadence.
- [ ] Preserve existing named roles and branch purpose. A specialist branch may
  trade one kit dimension for another, but that trade must be deliberate and
  visible in its cost, facility, and battlefield job.
- [ ] Check every explicit branch edge for accidental level, skill,
  proficiency, inventory, wage, or upgrade-cost regressions.
- [ ] Swap existing same-roster items before changing item stats when the issue
  is a misplaced loadout rather than an item-wide problem.
- [ ] Validate recruit, veteran, elite, cavalry, and ranged paths separately.
- [ ] Check AI lords, garrisons, player parties, and battle simulation after
  each culture because XP and center rules affect each differently.

### Phase 4: Rebalance Nobles as a Distinct Access Tier

- [ ] Establish a role-matched noble floor above the normal line without
  demanding that every noble exceed every normal specialist in every metric.
- [ ] Audit chapter-house access, noble assembly availability, wages, upkeep,
  upgrade cost, and replenishment together.
- [ ] Preserve noble visual identity and equipment motifs. Prefer same-roster
  swaps over converting noble troops into generic heavy units.
- [ ] Confirm that top noble routes remain viable inputs to faith ascension.

### Phase 5: Rebalance Faith and Zealot Troops as the Top Tier

- [ ] Compare faith troops against their originating culture's top noble and
  against role-matched faith peers, not against low-tier recruits.
- [ ] Audit all ascension gates together: effective faith, local support,
  chapel/temple, institution strength, tension, holy burden, noble supply, and
  faith scarcity cost.
- [ ] Make faith superiority clear but not mass-producible. Gate pressure and
  economic burden should be more important than arbitrary raw-stat inflation.
- [ ] Test one-faith dominance, mixed-faith tension, and low-faith recovery.

### Phase 6: Mercenaries, Minor Factions, and AI Economy

- [ ] Rebalance mercenary companies by contract cost, availability, quality,
  employer reserve, and deployment role as well as troop equipment.
- [ ] Confirm that AI mercenary demand reacts sensibly to manpower shortage,
  food, health, outbreaks, war, and fiscal stress.
- [ ] Prevent mercenaries from becoming the universally cheapest route to the
  same combat quality as gated nobles or faith elites.
- [ ] Audit prisoner/slaver conversion routes separately so they do not create
  a hidden infinite supply of high-tier troops.

### Phase 7: Scenario and Release Validation

- [ ] Run controlled field battles for every role match-up at recruit, veteran,
  normal elite, noble, and faith tiers.
- [ ] Run siege offense and defense tests with representative garrisons.
- [ ] Run first-castle, established-castle, and multi-holding economy scenarios.
- [ ] Run AI campaign simulations long enough to expose recruitment, wealth,
  mercenary, and upgrade feedback loops.
- [ ] Review player and AI upgrade logs for silent facility, center, wealth, or
  faith gate failures.
- [ ] Run Balance Lab verification, existing static guards, the normal build,
  doctor, generated import checks, and a diff review of all generated output.
- [ ] Require a written rationale, source diff, test evidence, and in-game
  smoke result for every final batch.

## Initial Audit Findings: Review, Not Changes

- [x] The five player-culture roster baselines were captured with the new
  progression tool. Each currently has one scripted top-Noble-to-`*` candidate
  route and five faith ascension outcomes. The direct authored roster counts
  are: Antarian 13 (9 Normal, 4 Noble), Marinian 15 (11 Normal, 4 Noble),
  Adenian 15 (11 Normal, 4 Noble), Villianese 14 (10 Normal, 4 Noble), and
  Zerrikanian 15 (11 Normal, 4 Noble). The Noble count includes the authored
  `*` candidate troop where applicable.
- [x] The first player-culture source batch repairs three Adenian loadout
  contracts: basic and veteran archers now contain the shields their existing
  guarantees require, and medium cavalry now has a sword fallback instead of
  a duplicate lance entry. `build/test_player_start_roster_static.py` keeps
  all five player-start cohorts free of high-severity missing shield, mount,
  and weapon contracts.
- [x] The runtime reinforcement audit now prevents the selected culture's
  garrison and lord templates from drifting into a broad static-pressure
  outlier. It preserves distinct cavalry, crossbow, bow, and foot doctrines
  instead of equalizing the five mutually exclusive cultures.
- [x] The faith-ascension audit models the five `*` Noble candidates and all
  25 scripted Faith outcomes. It catches missing route matrix entries,
  invalid rank transitions, hard loadout failures, and ascensions with no
  measurable elite premium. This is how Faith remains above Nobles without
  treating every weapon or proficiency delta as a mandatory increase.
- [x] The direct player-culture progression audit now covers all 52 authored
  recruit, normal, and Noble upgrade edges. Every edge raises level, preserves
  rank, and has a complete target loadout plus a kit or training advantage.
  Five intentional kit-score dips are explicit training-compensated trades,
  not silent regressions.
- [x] The Native profile now covers the five coexisting kingdoms, all live
  culture-to-template bindings, and all 39 direct Native upgrade routes. The
  Khergit A/B packages retain their all-mounted identity but supply fewer
  riders per reinforcement call, bringing garrison pressure from 1.619x to
  1.426x the lowest Native baseline and lord pressure to 1.322x.
- [x] Initial same-role static kit-score review candidates are deliberately
  narrow: Antarian Noble -> Guard, Antarian Regular -> Veteran, Adenian Light
  -> Medium, Villianese Longbowman -> Veteran Longbowman, and Zerrikanian
  Archer I -> Archer II. These are not approved changes; randomized pools,
  role intent, proficiency, cost, facility, and battle results must be checked
  before any adjustment.
- [ ] The broad existing troop equipment audit is useful as a coarse safety
  net, but it is not enough to prove a satisfying progression curve. It allows
  intentional role differences and does not model recruitment, access, cost,
  random pools, or dynamic faith ascension.
- [ ] Some normal upgrade edges have non-monotonic static kit scores. This may
  be a valid specialization trade, an inventory-pool artifact, or a real
  regression. Each edge needs role and spawn review before it is changed.
- [ ] Faith ascension is invisible to a standard `upgrade()` tree unless it is
  modeled as a separate scripted route. Any total troop rebalance that ignores
  this would undercount the top-tier trajectory.
- [ ] Population, health, food, security, construction, and mercenary demand
  are already connected to manpower and campaign reaction. Troop changes that
  alter costs, wages, or availability must be tested against those systems.
- [ ] Mobile AI lords now resolve safe training-center context before upgrading;
  balance measurement must still account for whether a faction has facilities,
  wealth, and a non-sieged center available.
- [x] The Imperial profile confirms three core reinforcement templates and a
  separate 40-member Legion auxiliary template. The pre-invasion trigger
  visits eight entry villages and applies that auxiliary template two, three,
  and four times per successful spawn at 90, 60, and 30 days respectively.
  Its source-level upper bounds are 640, 960, and 1280 members by stage,
  or 2880 across all stages if every spawn succeeds and survives. These are
  review evidence, not live campaign measurements or an automatic nerf order.
- [x] The generated autoresolve setup now recognizes the actual core
  Expedition `ief_` troop prefix while preserving the existing
  `imperial_` and `legion_` compatibility aliases. This is an
  intent-preserving source fix, not a direct troop or item stat change.

## Definition of Done

- [ ] Every roster has a documented role doctrine, item pool, tier trajectory,
  access path, cost/wage model, and scenario evidence.
- [ ] Normal troops remain culturally distinct and useful throughout the game.
- [ ] Nobles are meaningfully above normal troops and remain supply-limited.
- [ ] Faith/Zealot troops are meaningfully above nobles and remain genuinely
  gated by the faith system.
- [ ] The first-castle transition has at least one viable, understandable path
  that does not require exploiting a single troop line or mercenary loophole.
- [ ] AI factions can recruit, train, afford, and react with comparable
  structural rules rather than relying on free universal upgrades.
- [ ] No rebalance batch changes record order, generated IDs, or export files
  directly, and every batch passes its reviewed build and in-game checks.
