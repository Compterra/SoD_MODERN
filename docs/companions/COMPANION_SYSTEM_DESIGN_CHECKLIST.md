# Companion System Design And Checklist

## Purpose

This document is the master design checklist for the modern companion system. Native Mount & Blade companions are mostly recruitable heroes with personality clashes, payment requests, and a few scripted objections. This module's companions are now a much deeper party layer: they have approval, values, roles, retinues, personal quest arcs, campfire presence, world reactions, journal memory, and post-quest consequences.

Use this document as the production standard when adding, refactoring, or reviewing companion content. Use it alongside:

- `docs/companions/COMPANION_DEPTH_BIBLE.md`
- `docs/companions/COMPANION_OVERHAUL_CHECKLIST.md`
- `docs/companions/COMPANION_INTERACTIVE_QUEST_CHECKLIST.md`
- `docs/companions/COMPANION_QUEST_IMMERSION_AUDIT.md`
- `docs/quests/UNIQUE_QUEST_NPCS_CHECKLIST.md`

## Design Pillars

- [x] Companions are people, not stat packages.
- [x] Companions judge the player's choices through approval, not only pairwise likes and dislikes.
- [x] Companions have specific values that intersect with world systems.
- [x] Companions can warn, reconcile, forgive, harden, or leave only after readable escalation.
- [x] Companions provide utility through advisor roles, but role power depends on trust.
- [x] Companions have personal quests with world targets and consequences.
- [x] Companions speak through campfire, direct dialogue, reports, incidents, and quest aftermath.
- [x] Companions can become witnesses to larger campaign systems: slavery, diplomacy, trade, morale, siege, center health, and invasion pressure.

## Companion Categories

### Native-Style Core Companions

These are the sixteen regular companion heroes from `trp_npc1` through `trp_npc16`. They are eligible for the broad companion framework:

- Borcha
- Marnid
- Ymira
- Rolf
- Baheshtur
- Firentis
- Deshavi
- Matheld
- Alayen
- Bunduk
- Katrin
- Jeremus
- Nizar
- Lezalit
- Artimenner
- Klethi

Checklist:

- [x] Included in `companions_begin` to `companions_end`.
- [x] Eligible for tavern candidate rotation.
- [x] Eligible for personality clash/match systems.
- [x] Eligible for campfire and direct-talk companion depth.
- [x] Eligible for advisor roles.
- [x] Eligible for companion quest framework migration.
- [x] Eligible for companion reports and party mood summaries.

### Special Quest Companions

These are unique NPCs who can become companions only through specific quest outcomes. They should not randomly appear in taverns.

Current special quest companion:

- Diego, added as `trp_diego_companion` after successful survival in the Slaver prison-break quest.

Checklist:

- [x] Uses a separate troop entry from the quest-scene NPC.
- [x] Is recruited only by the successful quest branch.
- [x] Is blocked from normal tavern rotation.
- [x] Has `tf_hero` and `tf_unmoveable_in_party_window`.
- [x] Is added through `script_recruit_troop_as_companion`.
- [x] Has duplicate-add protection before joining.
- [x] Has direct party dialogue after recruitment.
- [x] Has a short post-rescue campfire scene.
- [x] Has companion reactions from anti-slavery and pro-order companions.
- [x] Has a long-term role or unique party utility.
- [x] Has a quest-journal aftermath entry.

## Troop And Range Rules

The normal companion range should remain tight and predictable.

- [x] `companions_begin` starts at `trp_npc1`.
- [x] `companions_end` stops before special quest companions that must not spawn in taverns.
- [x] Tavern companion rotation uses only the normal companion range.
- [x] Special quest companions are placed near the companion block for readability.
- [x] Special quest companions are outside tavern rotation unless deliberately promoted into the normal companion set.
- [x] Add static coverage that every special quest companion is outside tavern random placement.
- [x] Add static coverage that every special quest companion has exactly one recruitment source.
- [x] Add static coverage that quest-scene NPCs and permanent companion versions are separate troops.

## Recruitment Standards

### Regular Companion Recruitment

- [x] May occur through taverns or authored companion introduction dialogue.
- [x] Uses the regular companion talk and recruitment systems.
- [x] Can include payment request, background, objection, and acceptance.
- [x] Sets companion occupation and current center correctly.
- [x] Initializes level-up tracking and companion depth state.

### Special Quest Companion Recruitment

- [x] Must be tied to a completed quest action.
- [x] Must not appear before the quest outcome.
- [x] Must not be discoverable from tavern travelers unless the quest explicitly supports it.
- [x] Must guard against duplicate recruitment.
- [x] Must leave the original quest NPC state resolved.
- [x] Must not reuse a scene prisoner/town walker troop as the permanent party hero.
- [x] Should show an immediate join line or post-mission message that names the new status.
- [x] Should record a quest memory event.
- [x] Should update the journal or report with the companion outcome.

## Approval And Values

Each regular companion should have approval logic that answers what the player proves to them.

- [x] Approval bands exist.
- [x] Approval is shown narratively rather than as raw numbers.
- [x] Approval can rise or fall from major player actions.
- [x] Low approval weakens role bonuses.
- [x] Warnings come before permanent departure pressure.
- [x] Reconciliation content exists.
- [x] Special quest companions need approval compatibility rules.
- [x] Diego needs explicit values: anti-slavery, commoner rescue, distrust of coercive profit, respect for courage.
- [x] Add static coverage for special quest companion approval initialization if they enter the depth framework.

## Advisor Roles

Advisor roles make companions useful without turning them into mandatory builds.

Current role families:

- Quartermaster
- Surgeon
- Scout
- Captain
- Envoy
- Engineer
- Spymaster

Checklist:

- [x] Roles can be assigned from companion-facing surfaces.
- [x] Role descriptions exist.
- [x] Role active and degraded states exist.
- [x] Role effects are small and trust-scaled.
- [x] Personal quest outcomes can improve or alter role payoff.
- [x] Special quest companions need role eligibility rules.
- [x] Diego should probably start with Captain, Spymaster, or anti-slaver rescue utility rather than a generic tavern role.

## Personal Quest Standards

Every regular companion arc should have more than campfire flavor. A strong companion quest has a value, a wound, a destination, a witness, a dilemma, and aftermath.

- [x] Each companion has a personal quest premise.
- [x] Each companion has at least one world-triggered incident.
- [x] Each companion has direct dialogue for active quest states.
- [x] Each companion has good and hard outcomes.
- [x] Each companion has aftermath lines.
- [x] Each companion has quest-framework metadata.
- [x] Each companion can write journal and memory data through the quest framework.
- [x] Each companion has at least one role payoff.
- [ ] Manual QA remains required for every full quest chain.

For special quest companions:

- [x] Diego has a quest chain that recruits him if he survives.
- [x] Diego needs a post-recruitment personal arc or loyalty scene.
- [x] Diego needs an aftermath report entry.
- [x] Diego needs at least one later anti-slaver incident.
- [x] Diego needs failure-state handling if he is rescued, joins, and later leaves or is removed.

## Dialogue Surfaces

Companions should not rely on one menu.

- [x] Campfire exists as a party mood and companion reflection surface.
- [x] Direct talk exists for personal quest, role, warning, and reconciliation beats.
- [x] Companion reports summarize approval, roles, warnings, and quest aftermath.
- [x] World incidents can trigger companion commentary.
- [x] Quest journal distinguishes "talk to companion" from "go to place/actor."
- [x] Diego needs a direct party talk branch after recruitment.
- [x] Diego needs at least one direct line about the Slaver base after the rescue.
- [x] Diego needs at least one line reacting to freeing captives.
- [x] Diego needs at least one line reacting to selling/buying slaves.

## World Reaction Coverage

Companions should feel attached to the world, not sealed inside the party screen.

Major systems that should dispatch companion reactions:

- [x] Slaver actions.
- [x] Captive freeing.
- [x] Buying or selling slaves.
- [x] Village help or abuse.
- [x] Raids and post-battle outcomes.
- [x] Diplomacy decisions.
- [x] Imperial Expeditionary Force actions.
- [x] Black Khergit tribute and bribes.
- [x] Trade contracts and relief shipments.
- [x] Company accounts, wages, rations, and morale.
- [x] Mini-faction support or hostility.
- [x] Diego should be added to Slaver/captive reaction hooks if he joins the party.
- [x] Diego should have special affinity with ransom brokers or commoner rescue outcomes.

## Companion-To-Companion Dynamics

The goal is not only that companions react to the player. They should also react to each other.

- [x] Every regular companion has at least one liked companion.
- [x] Every regular companion has at least one disliked companion.
- [x] Triangle incidents exist.
- [x] Banter can advance by approval or quest stage.
- [x] Diego needs initial relationship mapping if promoted into the broad companion drama layer.
- [x] Diego likely likes Ymira, Bunduk, Jeremus, and Firentis when they oppose cruelty.
- [x] Diego likely clashes with Lezalit over discipline versus coercion.
- [x] Diego likely clashes with Marnid if trade profit turns toward captive markets.

## Reports And UI

The player needs readable information without breaking immersion.

- [x] Company report includes approval bands and warnings.
- [x] Companion reports include role state and quest leads.
- [x] Campfire gives mood and unresolved tension.
- [x] Quest journal tracks companion arcs.
- [x] Special quest companions need a report category.
- [x] Diego needs a short report entry after rescue.
- [x] Diego should not bloat the normal companion report if he is not in the party.

## Save And Runtime Safety

The companion system touches many long-lived slots and dialogs, so safety matters.

- [x] Recruitment paths should guard against duplicate hero stacks.
- [x] Quest-scene NPCs should not become permanent companions directly.
- [x] Direct-talk incident branches should require party presence unless explicitly resolving cleanup.
- [x] Quest target center/party values should be validated before display.
- [x] Companion quest triggers should store focus center, focus party, or focus cause.
- [x] Add a static duplicate-hero check for special quest companions.
- [x] Add a static check that every special quest companion has no tavern current-center assignment.
- [x] Add a static check that every companion reward branch has `neg|main_party_has_troop`.

## Diego Implementation Checklist

### Diego Core Design

**Core fantasy:** A one-eyed survivor of the Slaver pits who turns captivity into a lifelong war against the people who profit from chains.

**Role in the party:** Diego should feel like a rescued veteran who joins because the player proved action, not pity. He is not a tavern sellsword and not a soft moral lecturer. He is a hard, grateful, suspicious man whose loyalty is built around whether the player uses power to break cages or build them.

**Core wound:** Diego was once useful, respected, and able to protect others. The Slavers reduced him to a spectacle and a warning. He fears becoming only a weapon of revenge, but he fears passivity more.

**Core want:** He wants the Slaver web damaged badly enough that ordinary captives have a chance to run before anyone counts the profit.

**Contradiction:** Diego hates coercion, but he understands violence, intimidation, and fear better than comfort or mercy. He can approve of harsh action against predators while recoiling from cruelty toward the helpless.

**Voice:** Blunt, scarred, unsentimental. He uses images of chains, ledgers, pits, cages, missing names, and unpaid debts. He should not speak like a court knight or a priest. His warmth appears as practical loyalty: warnings, watchfulness, and promises to stand near the player when chains are broken.

### Diego Values

- [x] **Break chains:** Free captives, rescue prisoners, disrupt Slaver caravans, and weaken Slaver markets.
- [x] **Protect the forgotten:** Help commoners, refugees, escaped slaves, ransom victims, and people with no lord willing to spend coin on them.
- [x] **Punish predators:** Strike Slavers, abusive captors, prison wardens, and profiteers who hide behind polite trade.
- [x] **Respect earned courage:** Approves when the player takes real risks for someone who cannot repay them.
- [x] **Distrust clean-handed profit:** Dislikes merchants, lords, or commanders who benefit from suffering while pretending not to see it.
- [x] **Reject ownership of people:** Buying, selling, returning, or exploiting slaves should hit Diego harder than almost any other action.
- [x] **No pity performance:** He dislikes sentimental promises without action. Mercy must do something concrete.

### Diego Approval Direction

Approval rises from:

- [x] Freeing runaway slaves.
- [x] Attacking or disrupting Slaver caravans.
- [x] Refusing to buy slaves.
- [x] Helping captives after battles.
- [x] Paying ransom for poor captives or supporting ransom brokers.
- [x] Supporting Elephant Guard sanctuary work.
- [x] Supporting Jotnar kin rescue when Slaver pressure is involved.
- [x] Sparing helpless prisoners when there is a safe alternative.
- [x] Fighting the Imperial Expeditionary Force when they act like an empire of cages and tribute.

Approval falls from:

- [x] Buying slaves.
- [x] Selling prisoners into slavery.
- [x] Returning runaway slaves.
- [x] Strengthening the Slaver market.
- [x] Taking Slaver escort work.
- [x] Executing helpless prisoners for spectacle.
- [x] Raiding poor villages for easy supplies.
- [x] Using threats against unpaid or frightened troops when pay or food would solve the issue.
- [x] Making alliances with coercive factions for profit without any restraint or sabotage.

### Diego Lines The Player Can Cross

- [x] Repeated slave trading after Diego joins should trigger a direct warning.
- [x] Returning runaway slaves after Diego joins should trigger an immediate confrontation if he is in the party.
- [x] Working repeatedly for Ramun or Slaver guild interests should push Diego toward rupture.
- [x] If the player frees captives repeatedly after Diego's warning, he should reconcile and become deeply loyal.

### Diego Role Direction

Diego should not be a generic companion role clone. He should have one focused identity.

Preferred role concepts:

- [x] **Pit Veteran:** Improves prisoner escape resistance, prison-break odds, or captive rescue outcomes.
- [x] **Anti-Slaver Captain:** Gives small morale or combat bonuses when fighting Slaver parties.
- [x] **Ransom Broker Contact:** Improves ransom-broker prices or lowers costs for freeing poor captives.
- [x] **Chainbreaker:** Adds a small chance to convert freed captives/refugees into grateful volunteers.

Recommended v1 role:

- [x] Chainbreaker: when Diego is in the party and approval is steady or better, freeing captives gives a small morale/commoner relation reward and occasional rescued volunteer support.

### Diego Relationships

Likely respects:

- [x] Ymira, because mercy still matters after violence.
- [x] Bunduk, because soldiers and commoners deserve not to be spent casually.
- [x] Jeremus, because healing gives captives a life after rescue.
- [x] Firentis, because atonement through action makes sense to him.

Likely clashes:

- [x] Lezalit, when discipline begins to sound like ownership.
- [x] Marnid, when trade language hides captive suffering.
- [x] Rolf, if noble pride treats commoners as scenery.
- [x] Klethi, if opportunism becomes predation.

Triangle ideas:

- [x] Diego / Ymira / Lezalit: Mercy, discipline, and whether cruelty can ever build order.
- [x] Diego / Marnid / Borcha: Trade, survival, and where profit becomes complicity.
- [x] Diego / Bunduk / Rolf: Common soldiers, noble reputation, and who gets remembered after battle.

### Diego Dialogue Deliverables

- [x] First party talk after rescue.
- [x] Campfire reflection after the first rest.
- [x] Direct warning after slave trading.
- [x] Direct warning after returning runaway slaves.
- [x] Reconciliation line after anti-Slaver actions.
- [x] Role assignment line.
- [x] Role active report line.
- [x] Role disabled/low-approval report line.
- [x] Slaver caravan reaction.
- [x] Captive-freeing reaction.
- [x] Ransom broker reaction.
- [x] Late-game reflection after repeated anti-slaver play.
- [x] Late-game rupture line after repeated coercive profit.

### Current State

- [x] `trp_slave_hero` remains the prison-scene/quest NPC.
- [x] `trp_diego_companion` is the permanent party version.
- [x] `trp_diego_companion` copies Diego's original gear, face, level, skills, and hero flags.
- [x] Diego joins only if he survives the prison-break mission.
- [x] Diego is protected against duplicate joining.
- [x] Diego is outside the tavern rotation.
- [x] Diego's quest start, return, refusal, and breakout acceptance have idempotent guards.

### Next Diego Work

- [x] Rename or polish visible title if needed: "Diego" versus "One-Eyed Diego." Current visible name remains "Diego".
- [x] Add a post-rescue direct dialogue branch.
- [x] Add a campfire reflection after the first rest following rescue.
- [x] Add a party report line when Diego is present.
- [x] Add one Slaver-market reaction.
- [x] Add one captive-freeing reaction.
- [x] Add one objection to slave trading.
- [x] Add one reconciliation or gratitude line if the player repeatedly fights Slavers.
- [x] Add one unique role payoff, probably anti-slaver rescue intelligence or prisoner escape odds.
- [x] Add static tests for Diego's direct dialogue and report entry.
- [ ] Manual QA: rescue Diego alive and confirm he joins exactly once.
- [ ] Manual QA: Diego dies during prison break and does not join.
- [ ] Manual QA: player refuses the breakout and the chain closes cleanly.

## Future Expansion Checklist

- [x] Create a `special_companions_begin/end` range if more post-quest companions are added.
- [x] Add a helper script for special companion recruitment and duplicate protection.
- [x] Add special companion report integration.
- [x] Add special companion campfire integration.
- [x] Add special companion reaction dispatch.
- [x] Add special companion departure and recovery rules.
- [x] Add special companion role eligibility table.
- [x] Add static coverage for special companion troop placement.
- [ ] Add manual QA routes for every special companion.

## Definition Of Done

A regular companion is done when:

- [x] They have identity, approval, presence, utility, and arc layers.
- [x] They have quest-framework metadata and journal/memory support.
- [x] They have at least one world-triggered incident.
- [x] They have good and hard outcome aftermath.
- [x] They have role payoff and degraded role behavior.
- [ ] Their full route has been manually played and verified.

A special quest companion is done when:

- [x] Their quest NPC and permanent party troop are separate.
- [x] Their recruitment is unique, guarded, and quest-bound.
- [x] They never appear in tavern rotation unless intentionally designed to.
- [x] They have at least one direct talk branch after joining.
- [x] They have at least one world-system reaction.
- [x] They have a report or journal aftermath.
- [x] They have duplicate-add and failure-state static coverage.
- [ ] Their success and failure routes have been manually played.
