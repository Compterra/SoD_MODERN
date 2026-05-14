# Trade Economy Improvement Checklist

## Purpose

Turn the current trade economy from a strong simulation/report layer into a more visible, causal, dialogue-driven world system. Caravans, farmers, routes, towns, villages, mini-factions, and player contracts should all leave understandable traces in the campaign.

The current foundation is good:

- Caravan movement and town trade already exist.
- Farmer parties already connect villages to town markets.
- Center demand, goods market, health, food, prosperity, security, and law pressure already feed trade.
- Caravan dialogue already exposes cargo, roads, risks, and contracts.
- Mini-faction pressure already influences route descriptions.

The weak spots are mostly polish and causality:

- Route risk is more descriptive than behavioral.
- Caravan memory is useful but not personal or persistent enough.
- Local trade identity is computed but not memorable enough.
- Some farmer/caravan code should be guarded more defensively.
- Reports can feel more omniscient than medieval.

## Phase 1: Safety And Baseline Robustness

- [x] Add a guard in the farmer hourly trade trigger before reading `slot_party_home_center`.
- [x] Skip or repair farmer parties whose home center is invalid.
- [x] Add fallback behavior for farmers with missing market towns.
- [x] Add defensive center validation before farmer home trade modifies prosperity, health, population, food, or tariffs.
- [x] Add defensive center validation before caravan route selection stores or names a destination.
- [x] Add fallback strings for caravan dialogue when origin or destination is invalid.
- [x] Add a static test that detects unguarded farmer `slot_party_home_center` use.
- [x] Add a static test that detects caravan route string storage without center validation.
- [x] Add a static test that verifies `test_merchant_town_trade_stays_under_mb1011_local_var_limit` is executed by `build/test_trade_network_static.py`.
- [x] Run `py build\test_trade_network_static.py`.
- [x] Run `py build\doctor.py --doctor-new-only`.

## Phase 2: Route Risk Becomes Causal

- [x] Make `script_sod_trade_network_evaluate_route` produce a compact actionable result for AI use, not only dialogue.
- [x] Feed route risk into caravan departure chance.
- [x] Let very dangerous routes delay caravans unless the destination demand is high.
- [x] Let protected caravans ignore some risk when player-funded guards are active.
- [x] Let high Boar Clan pressure increase toll delays and escort rewards.
- [x] Let high Black Khergit pressure increase raid danger on rich or luxury routes.
- [x] Let Serpent Host route watching reduce uncertainty in caravan dialogue.
- [x] Let Black Army road security reduce risk only where their contract heat is relevant.
- [x] Let Slaver market pressure affect captive/black-market route warnings.
- [x] Let Jotnar or Elephant Guard presence reduce risk on refugee, anti-slaver, or sanctuary-adjacent roads.
- [x] Store a route result marker after each caravan arrival: clean, delayed, taxed, raided, protected, profitable, relief delivered, or exploited.
- [x] Use route result markers in the next caravan master conversation.
- [x] Add static coverage that caravan AI movement references trade-network route risk.
- [x] Add static coverage that mini-faction pressure has both dialogue and behavioral trade effects.

## Phase 3: Named Caravan Memory

- [x] Add caravan memory slots for captain name seed, merchant house style, route reputation, and player trust.
- [x] Generate a stable caravan captain label from faction, origin, or merchant-house style.
- [x] Add memory for "the player escorted us before."
- [x] Add memory for "the player abandoned or exploited us."
- [x] Add memory for "lost guards on this road."
- [x] Add memory for "profited well on this run."
- [x] Add memory for "paid tolls under protest."
- [x] Add memory for "saw raiders near destination."
- [x] Add memory for "relief shipment reached a starving market."
- [x] Let repeated interactions improve caravan trust.
- [x] Let low trust hide some trade opportunities or increase buy-in cost.
- [x] Let high trust give better rumors and slightly better contract terms.
- [x] Add a caravan dialogue line that references previous help.
- [x] Add a caravan dialogue line that references previous losses.
- [x] Add a caravan dialogue line that references a familiar road.
- [x] Add static tests for new caravan memory slots.
- [x] Add static tests for dialogue using caravan memory.

## Phase 4: Local Trade Identity

- [x] Keep computed identity as the default.
- [x] Add a small authored identity override table for highly memorable centers.
- [x] Add at least one famous iron market.
- [x] Add at least one grain-root village cluster.
- [x] Add at least one cattle country cluster.
- [x] Add at least one wool or linen country cluster.
- [x] Add at least one salt road.
- [x] Add at least one luxury sink.
- [x] Add at least one strategic military depot.
- [x] Add at least one starving frontier market condition.
- [x] Add at least one caravan hub.
- [x] Use authored identity in caravan dialogue when known.
- [x] Use authored identity in goods merchant gossip.
- [x] Use authored identity in guild master trade gossip.
- [x] Use authored identity in center reports.
- [x] Add fallback behavior if an authored identity points to an invalid center.
- [x] Add static tests for authored identity constants/table.
- [x] Add static tests that identity dialogue falls back safely.

## Phase 5: Dialogue-First Trade Intelligence

- [x] Review caravan dialogue options and remove choices that feel too report-like or omniscient.
- [x] Split caravan answers into nearby certainty and distant rumor.
- [x] Make low-skill/low-renown answers more general.
- [x] Let Trade skill improve price and shortage clarity.
- [x] Let Path-finding or Spotting improve road danger clarity.
- [x] Let Serpent Host standing improve horde/toll/ambush warnings.
- [x] Let local relation improve town-specific trade gossip.
- [x] Add caravan master lines that admit uncertainty.
- [x] Add caravan master lines for old news or rumor.
- [x] Add caravan master lines for merchant superstition and caution.
- [x] Add goods merchant prompts that point the player toward caravan masters.
- [x] Add guild master prompts that point the player toward recent caravans.
- [x] Keep the Trade Network Report as archive/summary, not the best source of new intelligence.
- [x] Add static tests that caravan dialogue calls trade-network helper scripts.
- [x] Add static tests that trade reports do not expose unsupported exact values.

## Phase 6: Player Trade Counterplay

- [x] Make "fund extra guards" reduce real route risk for the active caravan.
- [x] Make "buy cargo space" depend on route risk, cargo focus, and destination demand.
- [x] Make "insure caravan" pay out based on actual loss/disruption, not only high risk.
- [x] Make "relief shipment" visibly improve the destination only if it arrives.
- [x] Make "profit shipment" risk reputation loss if exploiting scarcity.
- [x] Add "fund road patrols" as a broader route action once the caravan dialogue flow is solid.
- [x] Add "suppress toll pressure" as a Boar Clan counterplay action.
- [x] Add "subsidize caravans to needy center" as a ruler/large-party action.
- [x] Add "invest in repeat route" after named caravan memory exists.
- [x] Connect clean trade to Marnid approval.
- [x] Connect roadcraft/protection to Borcha approval.
- [x] Connect relief shipments to Ymira and Jeremus approval.
- [x] Connect exploitative shortage profit to Klethi reaction.
- [x] Connect disciplined logistics to Lezalit approval.
- [x] Add static tests for companion hooks on trade contracts.
- [x] Add static tests for contract consequences on arrival.

## Phase 7: Farmer And Village Economy Visibility

- [x] Add village elder dialogue about what the village sends to market.
- [x] Add village elder dialogue about blocked roads.
- [x] Add village elder dialogue about cattle, grain, raw materials, or labor shortages.
- [x] Add town guild master dialogue about which villages feed the town.
- [x] Add a farmer-party encounter line explaining where they are bound.
- [x] Let farmer disruptions affect town food pressure more visibly.
- [x] Let successful farmer runs slowly improve village confidence or prosperity.
- [x] Let repeated raids reduce farmer activity or increase guard requests.
- [x] Add report text for village-market dependency.
- [x] Add static tests that farmer trade has center validation.
- [x] Add static tests that village-root dialogue exists.

## Phase 8: Trade And Public Health

- [x] Connect sick towns to caravan caution dialogue.
- [x] Connect sick towns to reduced merchant willingness.
- [x] Add quarantine-style warnings to goods merchant or guild master dialogue.
- [x] Let relief shipments include food or medicine flavor where appropriate.
- [x] Let repeated trade with diseased centers carry a small health-risk marker.
- [x] Let high health centers be described as safer markets.
- [x] Add public health report references to trade disruption only when known to the player.
- [x] Add static tests for trade-health dialogue hooks.
- [x] Add static tests for disease/health trade modifiers.

## Phase 9: Reports And Presentation Polish

- [x] Rename any overly abstract report option text into in-world language.
- [x] Make the Trade Network Report begin with known information only.
- [x] Separate "known by direct caravan talk" from "rumored by merchants."
- [x] Add "no reliable word" fallback when the player has not spoken to caravans recently.
- [x] Avoid repeating exact route labels too often.
- [x] Avoid raw numeric pressure values in player-facing reports.
- [x] Include active player-sponsored caravans.
- [x] Include recent protected or lost caravans.
- [x] Include recent relief shipments.
- [x] Include recent exploitative profit shipments if known.
- [x] Add static tests for invalid center fallback strings in reports.
- [x] Add static tests that report text avoids raw debug labels.

## Phase 10: Playtest Scenarios

- [ ] Talk to a caravan with no prior memory and confirm the answers are useful but general.
- [ ] Talk to the same caravan after escorting it and confirm it remembers help.
- [ ] Fund guards on a dangerous route and confirm route danger or outcome improves.
- [ ] Buy cargo space on a high-demand route and confirm payout depends on arrival.
- [ ] Sponsor relief to a struggling town and confirm prosperity/relation feedback.
- [ ] Exploit a shortage and confirm profit plus reputation/companion consequence.
- [ ] Let Boar pressure rise and confirm toll-road warnings become more common.
- [ ] Let Black Khergit pressure rise and confirm rich road warnings become more common.
- [x] Confirm farmer parties with invalid/missing data do not crash or spam logs.
- [x] Confirm distant trade information remains rumor-like.
- [x] Confirm reports do not reveal more than the player plausibly knows.

## Suggested Implementation Order

1. Safety guards and static tests.
2. Route risk feeding caravan behavior.
3. Named caravan memory.
4. Dialogue-first intelligence polish.
5. Local trade identity overrides.
6. Player contract consequences.
7. Farmer/village visibility.
8. Trade-health integration.
9. Report polish and playtest pass.




