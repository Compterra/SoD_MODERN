# Companion Interactive Quest Checklist And Design

This document turns the Klethi interactive campaign pass into a reusable roadmap for the rest of the companion roster. Use it alongside `docs/Interactive_Quest_Bible.md`, `docs/COMPANION_DEPTH_BIBLE.md`, and `docs/COMPANION_OVERHAUL_CHECKLIST.md`.

Klethi is the baseline. Future companion quests should not resolve as camp menus with flavor text. They should ask the player to travel, investigate, speak to someone outside the party, make a pressured decision in the world, and return to the companion for aftermath.

## Klethi Baseline Standard

Every remaining companion pass should copy the structure, not the exact content:

- A companion-specific trigger that is guarded by party availability.
- A concrete focus center, party, troop, scene, or route.
- Quest-slot mirrors for target/progress/result data where save compatibility needs it.
- A witness or contact who is not the companion.
- A world action before final resolution.
- An authored confrontation, hearing, rescue, defense, chase, inspection, or fight.
- Result grades that distinguish best, good, hard, failure, and recoverable setback states.
- Cleanup that clears all companion-specific globals when the companion leaves.
- Static tests for companion presence, target gating, result gating, cleanup, and correct troop ids.

## Definition Of Done

A companion campaign slice is complete only when all of these are true:

- [x] The quest cannot start, advance, or resolve unless the companion is in the party or the code path is an explicit cleanup/failure path.
- [x] The quest has a real destination or encounter target, not just a camp/courtship-style dialogue loop.
- [x] The journal tells the player where to go and why the companion cares.
- [x] At least one non-companion NPC, party, or scene prop can change the quest state.
- [x] At least one interactive climax exists in a menu, scene, mission template, or encounter.
- [x] The final moral choice happens after the world action, not at quest start.
- [x] The companion speaks after the outcome and reacts to the player's method.
- [x] Result grade is stored and can be used by approval, reports, or future companion hooks.
- [x] Defeat, retreat, refusal, companion departure, invalid target, and old-save repair are handled.
- [x] Static tests cover the new state variables, guards, target restrictions, and cleanup.
- [x] `py build\test_companion_depth_system.py` passes.
- [x] `py build\test_dialogue_immersion_static.py` passes when dialogue or menus change.
- [x] `py build\doctor.py --doctor-new-only` passes.
- [x] Generated module output is rebuilt if order files, dialogs, menus, scripts, or mission templates changed.

Manual QA remains tracked per companion below and scripted in `docs/COMPANION_INTERACTIVE_QUEST_PLAYTEST_MATRIX.md`. The definition above is the automated implementation gate; do not mark a companion's manual route complete until it has been played in-game.

## Companion Pass Template

Use this checklist for each companion audit:

- [ ] Read the existing companion section in `docs/COMPANION_DEPTH_BIBLE.md`.
- [ ] Find current quest triggers, menus, dialogs, reports, and cleanup.
- [ ] Verify the correct troop id before editing.
- [ ] Identify every path that can currently fire without party presence.
- [ ] Pick one campaign verb: investigate, escort, defend, hunt, negotiate, inspect, train, repair, expose, reconcile, or hold.
- [ ] Pick one focus target: town, village, castle, route, battlefield, caravan, prison, camp, or enemy party.
- [ ] Add target selection with fallback repair for old saves.
- [ ] Add a witness/contact step limited to the focus target.
- [ ] Add an interactive climax with at least three meaningful branches.
- [ ] Move old flavor choices into the correct late-stage moment.
- [ ] Add a result grade and aftermath dialogue.
- [ ] Add cleanup for all new globals and quest slots.
- [ ] Add static tests and at least one manual QA route.

## Recommended Implementation Order

1. Ymira - implemented first pass after Klethi
2. Firentis - implemented first pass after Ymira
3. Deshavi - implemented first pass after Firentis
4. Borcha - implemented first pass after Deshavi
5. Marnid - implemented first pass after Borcha
6. Bunduk - implemented first pass after Marnid
7. Jeremus - implemented first pass after Bunduk
8. Lezalit - implemented first pass after Jeremus
9. Artimenner - implemented first pass after Lezalit
10. Alayen - implemented first pass after Artimenner
11. Rolf - implemented first pass after Alayen
12. Baheshtur - implemented first pass after Rolf
13. Matheld - implemented first pass after Baheshtur
14. Katrin - implemented first pass after Matheld
15. Nizar - implemented first pass after Katrin

This order starts with companions whose arcs naturally create humane world interactions, then moves into discipline, logistics, honor, mounted warfare, and prestige arcs. It also avoids doing too many fight-heavy campaigns in a row.

## Automated Implementation Status

All native companion first-pass interactive campaign slices are implemented and covered by static QA. Each slice now has presence guards, a witness/contact step, a target or encounter surface, a gated world-action climax, result-grade state, cleanup, journal text, and generated module output.

Current automated validation set:

- [x] `py build\test_companion_depth_system.py`
- [x] `py build\test_dialogue_immersion_static.py`
- [x] `py build\doctor.py --doctor-new-only`
- [x] `py build\build_all.py`

Keep the per-companion manual QA lines open until the major in-game routes in `docs/COMPANION_INTERACTIVE_QUEST_PLAYTEST_MATRIX.md` are played. Static success proves the campaign scaffolding is present; manual QA proves the mission flow, encounter feel, and player-facing text land correctly.

## Ymira - Mercy Under Arms

Core theme: Ymira is learning what mercy costs when the world is violent enough to punish softness.

Interactive pattern: Refugee protection, captive triage, and a pressured shelter decision.

Campaign design:

- Trigger from freeing captives, discovering prisoners after battle, or entering a village with recent hardship.
- Pick a focus village or town edge where displaced people can be sheltered.
- Add a witness step with a freed captive, elder, or wounded civilian.
- Let the player bring Ymira to the focus center to inspect the refugees.
- Climax with slavers, bandit riders, or a hostile militia demanding the refugees be surrendered.
- Resolve through Ymira afterward, where she names what the player taught her.

Branches:

- Best: Shelter the vulnerable and spend supplies or money to make it sustainable.
- Good: Protect them but ration aid carefully, gaining smaller approval.
- Hard: Turn them away or use them as leverage, causing a warning state.
- Failure: Lose the defense or leave before the refugees are secured; quest remains recoverable once.

Checklist:

- [x] Add Ymira availability guards to all trigger and resolution paths.
- [x] Store focus center and refugee state.
- [x] Add witness dialog at the target center.
- [x] Add defense or standoff scene using existing village/town assets.
- [x] Track money, Slaver pressure, honor, refugee count, confrontation, and result grade.
- [x] Add aftermath dialogue and result grade.
- [x] Add static tests for presence guards, target gating, standoff, mission template, result state, and cleanup.
- [ ] Manual QA companion absence, wrong-center witness suppression, defeat recovery, and all aftermath choices.

## Firentis - Debt Of The Sword

Core theme: Firentis does not need absolution handed to him. He needs a chance to make restitution without fleeing the truth.

Interactive pattern: Restitution, witness testimony, and a moral confrontation.

Campaign design:

- Trigger from saving a village, entering a village after battle, or hearing of a wrong tied to soldiers.
- Pick a focus village with an elder, survivor, or grieving family witness.
- The player brings Firentis there to hear what was done and what repair would actually mean.
- Climax with bandits or deserters threatening the restitution effort, or a public accusation that can become a duel, apology, or payment.
- Final dialogue asks whether Firentis's guilt becomes service, silence, or self-punishment.

Branches:

- Best: Public confession plus meaningful restitution.
- Good: Quiet protection and supplies without spectacle.
- Hard: Threaten the accuser or bury the story for convenience.
- Failure: Refuse restitution or lose the defense; Firentis withdraws and approval drops.

Checklist:

- [x] Verify Firentis troop id in all hooks.
- [x] Add focus village and witness state.
- [x] Gate accusation/witness dialog to the focus village and party presence.
- [x] Add restitution cost or service action.
- [x] Add encounter or hearing climax.
- [x] Add result grade that can influence future remorse/discipline content.
- [x] Add static tests for presence guards, focus target, hearing, mission template, result grade, and cleanup state.
- [ ] Manual QA refusal, payment/protection, public confession, combat victory, combat defeat, and companion departure cleanup.

## Deshavi - Tracks Through Ash

Core theme: Deshavi knows what raiders leave behind, and she refuses to let the party treat burned villages as map noise.

Interactive pattern: Tracking, rescue, and choosing between justice and protection.

Campaign design:

- Trigger from village raids, bandit encounters, or freed captives.
- Pick a focus village and generate a nearby trail target or raider party.
- Add a survivor witness who gives Deshavi enough signs to track the attackers.
- The player follows the lead to a hidden camp, ambush site, or captive group.
- Climax can be a rescue fight, ambush reversal, or negotiation with a desperate raider splinter.

Branches:

- Best: Rescue captives and return them safely.
- Good: Defeat the raiders but fail to save every captive.
- Hard: Prioritize revenge or loot over survivors.
- Failure: Lose the trail or retreat from the rescue; quest can be repaired by revisiting the village.

Checklist:

- [x] Add focus village, trail target, and clue state.
- [x] Gate trail discovery to Deshavi in party.
- [x] Add survivor witness dialog.
- [x] Add raider party or scene confrontation.
- [x] Add return-to-village or return-to-Deshavi aftermath.
- [x] Add static tests for presence guards, focus target, trail climax, mission template, result grade, and cleanup state.
- [ ] Manual QA wrong village, defeated rescue mission, hard hunt path, aftermath choices, and companion departure cleanup.

## Borcha - The Road Keeps Its Own

Core theme: Borcha is a survivor of roads, lies, and opportunity. His campaign should test whether cunning serves the company or only himself.

Interactive pattern: Road scouting, hidden route discovery, and counter-ambush.

Campaign design:

- Trigger from caravan travel, Black Khergit contact, bandit ambush, or entering a town after a road fight.
- Pick a dangerous route between two centers.
- Add a caravan hand, scout, or captured raider as witness.
- Borcha identifies a side road or ambush point and asks to prove his read.
- Climax with an ambush that can be avoided, reversed, exploited, or bungled.

Branches:

- Best: Use Borcha's route to save travelers and expose the ambushers.
- Good: Protect the party and keep the road usable.
- Hard: Use the route to profit from someone else's danger.
- Failure: Ignore the signs and walk into the trap.

Checklist:

- [x] Add route endpoints and ambush state.
- [x] Require Borcha in party for scouting options.
- [x] Add witness in town, tavern, caravan, or prisoner dialog.
- [x] Add route menu or encounter branch.
- [x] Add aftermath where Borcha reacts to trust versus exploitation.
- [x] Add static tests for route endpoints, witness gating, counter-ambush, mission template, result grade, and cleanup state.
- [ ] Manual QA route invalidation, Borcha departure, wrong-town witness suppression, combat victory, combat defeat, bypass route, and profit route.

## Marnid - The Honest Price

Core theme: Marnid wants trade to be a craft, not a prettier word for theft.

Interactive pattern: Market investigation, dirty contract exposure, and a trade decision with costs.

Campaign design:

- Trigger from profitable trade, prisoner broker contact, caravan rescue, or town market visit.
- Pick a focus town with a goods merchant, caravan master, or broker contact.
- Add a witness who hints that a bargain is backed by stolen goods, captive labor, or a predatory debt.
- The player investigates with Marnid in the town.
- Climax with a sting, public accusation, repayment run, or guarded warehouse confrontation.

Branches:

- Best: Expose the dirty contract and establish a cleaner trade link.
- Good: Repay or compensate victims while preserving some profit.
- Hard: Take the profit and warn Marnid not to ask too many questions.
- Failure: Botch the accusation or lose the evidence.

Checklist:

- [x] Add focus town and market clue state.
- [x] Gate merchant/broker options to Marnid in party.
- [x] Add evidence or account marker.
- [x] Add warehouse, caravan, or town confrontation.
- [x] Add trade payoff, relation change, or morale consequence.
- [x] Add static tests for focus town, evidence, warehouse confrontation, mission template, result grade, and cleanup state.
- [ ] Manual QA no-Marnid triggers, wrong town, evidence missing, combat victory, combat defeat, public audit, blackmail route, and cleanup.

## Bunduk - The Men Who Hold The Line

Core theme: Bunduk values ordinary soldiers enough to argue with command on their behalf.

Interactive pattern: Rank-and-file grievance, watch reform, and a line-holding test.

Campaign design:

- Trigger from troop losses, low morale, garrison duty, or town/castle guard contact.
- Pick a focus camp, town, or castle where common soldiers are overworked or ignored.
- Add a regular soldier, wounded veteran, or militia witness.
- Bunduk asks the player to hear the complaint instead of dismissing it as whining.
- Climax with a drill, night attack, mutiny scare, or defense where the ignored soldiers prove the issue.

Branches:

- Best: Reform watches, pay, or equipment and let Bunduk speak for the men.
- Good: Solve the immediate tactical problem without broader reform.
- Hard: Crush the complaint and demand obedience.
- Failure: Lose the defense or let the grievance become desertion.

Checklist:

- [x] Add focus center or camp state.
- [x] Gate soldier petition to Bunduk in party.
- [x] Add morale/pay/equipment cost hook where feasible.
- [x] Add defense, drill, or hearing climax.
- [x] Add aftermath keyed to whether soldiers were respected.
- [x] Add static tests for petition, line test, mission template, result grade, and cleanup state.
- [ ] Manual QA garrison/camp edge cases, morale states, combat victory, combat defeat, reassign route, hard-drive route, and cleanup.

## Jeremus - Hands That Will Not Harden

Core theme: Jeremus's mercy is practical, but the campaign should force the player to decide whose pain counts.

Interactive pattern: Triage, medical supplies, and defending the helpless.

Campaign design:

- Trigger from battle casualties, village disease, prisoners, or wounded enemy troops.
- Pick a focus village, town infirmary, or battlefield camp.
- Add wounded ally, civilian, or enemy witness.
- The player brings Jeremus to perform triage and decide how supplies are spent.
- Climax with a raid on the infirmary, a shortage crisis, or a demand to abandon enemy wounded.

Branches:

- Best: Treat all who can be saved and pay the supply cost.
- Good: Prioritize civilians and allies while minimizing cruelty.
- Hard: Deny care to enemies or use treatment as leverage.
- Failure: Leave the wounded exposed or lose the infirmary defense.

Checklist:

- [x] Add focus medical site and supply state.
- [x] Gate triage choices to Jeremus in party.
- [x] Add witness dialog for ally/civilian/enemy perspectives.
- [x] Add supply cost and optional defense encounter.
- [x] Add aftermath with Jeremus's moral assessment.
- [x] Add static tests for witness gating, infirmary crisis, mission template, result grade, and cleanup state.
- [ ] Manual QA low-supply flavor, defeat, no-Jeremus cleanup, witness-to-crisis flow, defend route, reorder route, company-first route, and final aftermath choices.

## Lezalit - Discipline Without Chains

Core theme: Lezalit believes discipline saves lives, but his campaign should test whether he can command without cruelty.

Interactive pattern: Training doctrine, punishment hearing, and controlled combat trial.

Campaign design:

- Trigger from recruit training, troop casualties, low morale, or captured professional soldiers.
- Pick a focus camp, training ground, or town yard.
- Add recruit, veteran, or prisoner witness.
- Lezalit proposes a harsh method; the witness shows the cost.
- Climax with a drill mission, punishment hearing, or attack that tests whether discipline holds under stress.

Branches:

- Best: Teach discipline with purpose and restraint.
- Good: Use strict methods but stop needless humiliation.
- Hard: Back Lezalit's harshest instincts for quick results.
- Failure: Undermine command so badly the unit breaks.

Checklist:

- [x] Add focus training site and recruit state.
- [x] Gate drill/punishment content to Lezalit in party.
- [x] Add witness who challenges or confirms the method.
- [x] Add training or combat trial.
- [x] Add result grade affecting morale/training flavor.
- [x] Add static tests for witness gating, drill trial, mission template, result grade, and cleanup state.
- [ ] Manual QA companion absence, troop shortage flavor, morale edge cases, combat victory, combat defeat, corrected drill route, harsh-mark route, refusal aftermath, and cleanup.

## Artimenner - The Siege That Should Have Worked - implemented first pass after Lezalit

Core theme: Artimenner sees engineering as memory made useful. Failed work should leave evidence the player can inspect.

Interactive pattern: Inspection, repair, and technical decision under pressure.

Campaign design:

- Trigger from sieges, castle visits, construction projects, or engineer reports.
- Pick a focus castle, town wall, or construction site.
- Add worker, engineer, wounded builder, or garrison witness.
- Artimenner identifies a flaw and asks to inspect it in person.
- Climax with a repair under attack, a design choice, or exposure of sabotage.

Branches:

- Best: Fix the flaw properly and credit the workers who warned him.
- Good: Make a fast field repair that holds for now.
- Hard: Blame workers or choose a dangerous shortcut.
- Failure: Let the structure fail or abandon the repair.

Checklist:

- [x] Add focus fortification and flaw state.
- [x] Gate inspection to Artimenner in party.
- [x] Add witness at site.
- [x] Add repair menu, scene, or encounter.
- [x] Add material/time/cost consequence.
- [x] Add static tests for focus center, witness gating, repair watch, mission template, result grade, and cleanup state.
- [ ] Manual QA invalid center, siege state changes, old-save repair, ladder inspection, tower inspection, repair-watch victory, repair-watch defeat, simplify route, blame-workers route, and cleanup.

## Alayen - The Standard And The Self - implemented first pass after Artimenner

Core theme: Alayen's honor should become useful to people who cannot afford noble theater.

Interactive pattern: Public duty, banner witness, and choosing service over vanity.

Campaign design:

- Trigger from lord halls, village defense, insults, or banner/oath references.
- Pick a focus village, town hall, or lord court.
- Add elder, minor noble, or common witness who challenges Alayen's idea of honor.
- The player brings Alayen to answer publicly.
- Climax with a hearing, duel challenge, or defense where the honorable choice is not the glamorous one.

Branches:

- Best: Protect dependents and let honor mean service.
- Good: Maintain public dignity while doing the necessary work.
- Hard: Choose prestige over practical protection.
- Failure: Escalate the dispute into needless bloodshed or humiliation.

Checklist:

- [x] Add focus center and honor dispute state.
- [x] Gate public challenge to Alayen in party.
- [x] Add witness and optional lord/elder reaction.
- [x] Add hearing, duel, or defense climax.
- [x] Add result grade affecting Alayen's later honor language.
- [x] Add static tests for witness gating, public standard test, mission template, result grade, and cleanup state.
- [ ] Manual QA no-Alayen paths, faction/center invalidation, village elder witness, lord witness, standard-test victory, standard-test defeat, public-cost route, prestige route, final aftermath choices, and cleanup.

## Rolf - A Name Worth Wearing - implemented first pass after Alayen

Core theme: Rolf's grand self-image should be tested by a moment where claims matter less than conduct.

Interactive pattern: Public identity challenge, comic pressure, and earned dignity.

Campaign design:

- Trigger from taverns, lord courts, tournaments, or boasts after victory.
- Pick a focus town or hall where someone challenges Rolf's story.
- Add claimant, gossip, minor noble, or old mercenary witness.
- Rolf asks the player to back his name.
- Climax with a public debate, duel, staged proof, or service task that lets Rolf become useful despite the lie.

Branches:

- Best: Redefine the name through service and courage.
- Good: Defend Rolf theatrically without harming bystanders.
- Hard: Threaten or bribe witnesses to preserve the myth.
- Failure: Expose him cruelly or lose the public challenge.

Checklist:

- [x] Add focus town/hall and challenge state.
- [x] Gate boast/challenge to Rolf in party.
- [x] Add witness with a specific claim.
- [x] Add debate, duel, or public service climax.
- [x] Add aftermath that preserves humor without making the quest empty.
- [x] Add static tests for focus town, witness gating, public proof, mission template, result grade, and cleanup state.
- [ ] Manual QA public failure, combat loss, witness absence, wrong-town witness suppression, patron route, theater route, final aftermath choices, and cleanup.

## Baheshtur - The Unbroken Saddle - implemented first pass after Rolf

Core theme: Baheshtur values freedom, pride, and horsemen's bonds; his campaign should let mounted identity become a choice, not just flavor.

Interactive pattern: Rider negotiation, pursuit, and oath under pressure.

Campaign design:

- Trigger from Black Khergit encounters, mounted battles, steppe travel, or captive riders.
- Pick a focus route, town, or rider party.
- Add captive rider, rival scout, or steppe witness.
- Baheshtur recognizes a rider custom and asks the player to handle it properly.
- Climax with mounted pursuit, negotiation, prisoner exchange, or duel of speed.

Branches:

- Best: Win respect through restraint and release an honorable oath.
- Good: Defeat the riders cleanly and spare those who yield.
- Hard: Force submission and break the custom for advantage.
- Failure: Mishandle the exchange or lose the pursuit.

Checklist:

- [x] Add rider target and custom/clue state.
- [x] Gate rider dialog to Baheshtur in party.
- [x] Add mounted or route-based encounter.
- [x] Add prisoner/release/oath consequence.
- [x] Add aftermath tied to pride versus domination.
- [x] Add static tests for party availability helper, witness gating, rider-oath trial, mission template, result grade, and cleanup state.
- [ ] Manual QA Black Khergit raider witness, night guard witness, no-witness camp suppression, rider-oath combat win/loss, free oath route, bind route, final aftermath choices, and departure cleanup.

## Matheld - No Backward Step - implemented first pass after Baheshtur

Core theme: Matheld's courage is real, but her campaign should ask whether courage includes restraint and protecting the line.

Interactive pattern: Hold, retreat, shield others, and choose the cost of valor.

Campaign design:

- Trigger from hard battles, village defense, sea-raider-style threats, or wounded frontliners.
- Pick a focus village, bridge, pass, or battlefield edge.
- Add frightened militia, wounded shieldbearer, or hostile champion witness.
- Matheld wants to stand and prove the line will not break.
- Climax with a hold-the-line fight, controlled retreat, or champion challenge.

Branches:

- Best: Hold long enough to save vulnerable people, then withdraw intelligently.
- Good: Win the stand with acceptable losses.
- Hard: Chase glory and accept avoidable casualties.
- Failure: Break the line or abandon those being shielded.

Checklist:

- [x] Add focus defense point and pressure state.
- [x] Gate shield-line content to Matheld in party.
- [x] Add witness who represents those protected by the stand.
- [x] Add defense mission or timed encounter.
- [x] Add casualty/morale/result grade.
- [x] Add static tests for party availability helper, ranker witness gating, shield-line test, mission template, result grade, and cleanup state.
- [ ] Manual QA ranker witness, no-witness camp suppression, shield-line combat win/loss, breathing-wall route, blood-roar route, final aftermath choices, and departure cleanup.

## Nizar - The Impossible Charge - implemented first pass after Katrin

Core theme: Nizar wants life to become legend. His campaign should let the player decide whether legend is a tool or an appetite.

Interactive pattern: Daring rescue, spectacle, and risk management.

Campaign design:

- Trigger from tournaments, cavalry fights, pursuit opportunities, or travelers in danger.
- Pick a focus route, arena-like scene, or enemy party.
- Add scout, admirer, rival, or endangered traveler witness.
- Nizar sees a chance for a dazzling intervention.
- Climax with a charge, rescue, duel, or pursuit where planning affects casualties.

Branches:

- Best: Achieve the dramatic rescue with a practical escape plan.
- Good: Win the spectacle but pay a smaller cost.
- Hard: Choose glory over safety.
- Failure: Lose the charge, fail the rescue, or let Nizar's pride turn ugly.

Checklist:

- [x] Add focus target and spectacle state.
- [x] Gate charge/rescue hook to Nizar in party.
- [x] Add witness and optional crowd/rival reaction.
- [x] Add combat or pursuit climax.
- [x] Add result grade keyed to glory versus responsibility.
- [x] Add static tests for party availability helper, field setup gating, charge-lane test, mission template, result grade, and cleanup state.
- [ ] Manual QA field setup before battle, no-field-setup camp suppression, charge-lane combat win/loss, exit-first route, applause-first route, final aftermath choices, and departure cleanup.

## Katrin - The Last Coin In Camp - implemented first pass after Matheld

Core theme: Katrin understands that campaigns are won or lost in small economies: food, debt, pay, and the quiet cost of waste.

Interactive pattern: Camp logistics, market pressure, and a petition hearing.

Campaign design:

- Trigger from low food, unpaid troops, market visits, wounded troops, or post-battle looting.
- Pick a focus market, camp, village, or supply contact.
- Add regular soldier, merchant, wounded camp follower, or creditor witness.
- Katrin asks the player to look at the actual accounts.
- Climax with procurement under pressure, a camp petition, a debt confrontation, or defense of a supply wagon.

Branches:

- Best: Pay the real cost and stabilize the camp.
- Good: Stretch stores without cruelty.
- Hard: Squeeze the weak, delay pay, or hide losses.
- Failure: Let shortages become desertion, sickness, or morale damage.

Checklist:

- [x] Add focus supply target and account state.
- [x] Gate petition/account content to Katrin in party.
- [x] Add witness representing the human cost of logistics.
- [x] Add procurement, hearing, or wagon defense climax.
- [x] Add money/food/morale consequence.
- [x] Add static tests for party availability helper, accounts/camp witness gating, supply watch, mission template, result grade, and cleanup state.
- [ ] Manual QA low-money account witness, low-food regular-member witness, no-witness camp suppression, supply-watch combat win/loss, open-books route, hide-shortage route, final aftermath choices, and departure cleanup.

## Shared QA Matrix

Run these checks after each companion campaign implementation:

- [x] Static QA: start trigger has companion presence or availability guard.
- [x] Static QA: trigger without companion is blocked by party presence or cleanup-only path.
- [x] Static QA: departed companion cleanup clears companion-specific globals.
- [x] Static QA: wrong target suppresses witness/contact options through focus gating.
- [x] Static QA: correct target/action surface exists for the witness or clue step.
- [x] Static QA: final resolution is gated behind clue and confrontation progress.
- [x] Static QA: best, good, hard, and failure/result-grade paths are represented.
- [x] Static QA: journal entries mention actionable targets or world steps.
- [x] Static QA: result grade is reset on start/cleanup and mirrored into quest metadata.
- [x] Static QA: old-save target repair or safe fallback exists where target data can be missing.
- [x] Static QA: troop ids reference the intended companion only.
- [x] Static QA: generated order files include new menus, dialogs, scripts, and mission templates.

Manual QA still required:

- [ ] Start trigger with companion in party.
- [ ] Attempt the same trigger without companion in party.
- [ ] Remove companion after quest start and verify cleanup or recoverable blocking.
- [ ] Visit the wrong town/village/route and verify witness options do not appear.
- [ ] Visit the correct target with the companion and verify the witness/action appears.
- [ ] Try to resolve before the clue or confrontation and verify it is blocked.
- [ ] Complete best, good, hard, and failure paths.
- [ ] Verify journal entries update after target selection, clue acquisition, climax, and aftermath.
- [ ] Verify result grade is not left stale after quest completion or failure.
- [ ] Verify old saves with missing target data can repair or fail gracefully.
- [ ] Verify troop ids reference the intended companion only.
- [ ] Verify generated order files include new menus, dialogs, scripts, and mission templates.

Use `docs/COMPANION_INTERACTIVE_QUEST_PLAYTEST_MATRIX.md` as the live playtest script for these rows.

## Static Test Expectations

Each companion pass should add assertions to `build/test_companion_depth_system.py` or the closest existing static test file for:

- Correct companion troop id.
- Presence guard on triggers, witnesses, climax, and final resolution.
- New helper usage where appropriate.
- Focus target gating.
- Result/progress gating.
- Cleanup of every new global and quest slot.
- Journal text mentioning the actionable target.
- No direct final resolution from the first camp/dialog prompt.

Dialogue-heavy passes should also extend `build/test_dialogue_immersion_static.py` with checks that the quest has world-facing verbs, target-centered text, and aftermath lines that reflect result grade.
