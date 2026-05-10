# Companion Overhaul Checklist

This checklist tracks the Dragon Age-style companion overhaul from framework to fully realized companion arcs. Use it alongside `docs/COMPANION_DEPTH_BIBLE.md`.

## Completion Targets

A companion is not considered "done" until all five layers are present:

- [ ] **Identity:** background, wound, want, contradiction, voice, values, rivalries.
- [ ] **Reactivity:** approval shifts from world actions that match their values.
- [ ] **Presence:** campfire mood, direct talk, warning, reconciliation, report entry.
- [ ] **Utility:** advisor role, role flavor, trust-scaled bonus, failure/degraded state.
- [ ] **Arc:** personal quest opening, test choice, good outcome, hard outcome, aftermath.

## Production Quality Gates

- [x] No companion has only generic approval text.
- [x] No companion quest resolves only as a number change.
- [x] Every warning names the player's behavior, not just "low approval."
- [x] Every good resolution changes how the companion talks about the player.
- [x] Every hard resolution is tempting or useful, not just a fake bad option.
- [x] Every companion has at least one disagreement with a specific other companion.
- [x] Every companion has one reason to respect the player that is not identical to another companion's reason.
- [x] Every companion has one "line the player can cross."
- [x] Role bonuses are useful but small enough not to force one optimal party.
- [x] Role bonuses degrade when approval is below steady.
- [x] Companion content avoids modern slang and keeps Warband-style brevity.
- [x] Campfire text stays readable in menu form.
- [x] Direct dialogue gives character voice, not exposition dumps.

## Dragon Age Origins Depth Gap

This section tracks what is still missing before the companion system feels close to a full Dragon Age-style party experience instead of a strong Warband-compatible framework. The current companion-depth layer is valid and should remain, but the next gap is moving personal arcs into the existing quest framework so they gain journal memory, staged outcomes, event dispatch, and more persistent aftermath.

- [x] Global approval, role, warning, reconciliation, and report framework exists.
- [x] Every companion has a personal quest premise, role identity, and value profile.
- [x] Every companion has at least one friend, rival, or triangle tension.
- [x] Every companion has a deeper world-integrated implementation pass.
- [x] Every companion has multi-stage direct-talk responses keyed to warning, trust-opened, active quest, good resolution, and hard resolution.
- [x] Every companion has at least one personal quest incident triggered by world play, not only campfire choices.
- [x] Every companion has a personal quest with 2-3 meaningful branches and a distinct aftermath state.
- [x] Every companion has a role payoff that changes after their good quest resolution.
- [x] Every companion has a hard/compromise payoff that is useful but emotionally costly.
- [x] Every companion has a late-game reflection after the player repeatedly proves or violates their core value.
- [x] Every companion has at least one unique follow-up line after a major faction system intersects their values.
- [x] Companion reactions can interrupt or immediately comment on major player choices where technically practical.
- [x] Companion banter progresses by approval/quest stage instead of staying mostly static.
- [x] Cross-companion triangle disputes have at least one gameplay-triggered incident each.
- [x] Company report distinguishes completed arcs, unresolved warnings, and future leads for each companion.
- [x] Every companion personal arc has quest-framework metadata rather than only a camp menu and troop-slot stage.
- [x] Every companion personal arc can use quest runtime accept, update, complete, fail, and abort lifecycle hooks where appropriate.
- [x] Every companion personal arc writes journal entries for opening, stage update, good outcome, hard outcome, and failure or rupture.
- [x] Every companion personal arc records at least one memory event through the quest dialogue memory layer.
- [x] Every companion personal arc applies at least one quest outcome consequence beyond approval.
- [x] Companion personal arcs can be advanced by quest event dispatch from world systems.
- [x] Companion reports show visible aftermath from quest-framework state, not only companion-depth slot state.
- [ ] Manual QA confirms each companion's quest opening, middle choice, good outcome, hard outcome, warning, and reconciliation.

### Companion Quest Framework Migration

- [x] Prototype: Ymira and Lezalit have quest-framework IDs and display names.
- [x] Prototype: Ymira and Lezalit keep `slot_troop_companion_personal_quest_stage` as the compatibility layer.
- [x] Prototype: Ymira and Lezalit call quest runtime accept/update/complete/fail hooks from companion-depth stage changes.
- [x] Prototype: Ymira and Lezalit call journal, memory, outcome, and event-dispatch helpers from companion-depth stage changes.
- [x] Prototype: Ymira and Lezalit show quest-framework aftermath in the companion depth report.
- [x] Milestone slice: Bunduk, Jeremus, and Firentis have quest-framework IDs, runtime bridge support, and report aftermath.
- [x] Milestone slice: all remaining companion arcs have quest-framework IDs, runtime bridge support, and report aftermath.
- [x] Milestone slice: gameplay-triggered triangle incidents dispatch quest events, record memory, and refresh the journal.
- [x] Add a quest-framework ID and display name for each companion personal arc.
- [x] Keep `slot_troop_companion_personal_quest_stage` as the compatibility layer for campfire, direct talk, and role payoff checks.
- [x] Use `sod_quest_runtime_accept` when a trust-opened companion arc becomes an active personal quest.
- [x] Use `sod_quest_runtime_update` when a companion arc advances from world play or a menu choice.
- [x] Use `sod_quest_runtime_complete` for good/trust resolutions.
- [x] Use `sod_quest_runtime_fail` or `sod_quest_runtime_abort` for rupture, refusal, or abandoned personal arcs.
- [x] Use `sod_quest_dialogue_record_event` for companion memory beats that future dialogue can reference.
- [x] Use `sod_quest_journal_update` so personal arcs appear in the quest journal with current stage text.
- [x] Use `sod_quest_outcome_apply_consequences` for rewards, penalties, role payoff flags, or world-state changes.
- [x] Use `sod_quest_event_dispatch` or existing world hooks to advance companion arcs from battles, captives, diplomacy, construction, and faction systems.
- [x] Add static coverage that companion quest-framework integration is registered and does not bypass the existing companion-depth framework.

### DAO-Style Gap Milestones

- [x] Milestone 1: migrate Ymira and Lezalit personal arcs into the quest framework as prototypes.
- [x] Milestone 2: migrate Bunduk, Jeremus, and Firentis with stronger battlefield, casualty, mercy, and discipline hooks.
- [x] Milestone 3: migrate all remaining companion arcs into quest-framework identity, journal, memory, and outcome handling.
- [x] Milestone 4: add triangle incidents that are quest events, not only report text.
- [x] Milestone 5: add late-game reflections triggered by repeated value-aligned or value-breaking behavior.

## DAO-Style Personal Quest Requirements

Use these rows to judge whether an individual companion quest has moved beyond "campfire prototype" into a real companion arc.

- [x] **Trigger:** A world/menu/script event can start or advance the personal matter.
- [x] **Setup:** The companion explains the personal stake in their own voice.
- [x] **Pressure:** The quest tests the companion's core wound, not just their opinion.
- [x] **Choice:** The player gets at least two values-based paths and one pragmatic or dangerous path where appropriate.
- [x] **Companion Response:** The companion reacts immediately to the chosen path.
- [x] **Aftermath:** The company report and direct talk remember the result.
- [x] **Mechanical Consequence:** The role payoff, approval floor, warning state, or world hook changes after resolution.
- [x] **Triangle Reaction:** At least one related companion can approve, object, or complicate the choice.
- [ ] **Manual QA:** The quest is played through in-game once for each major outcome.

## Companion Quest Immersion Gap

See `docs/COMPANION_QUEST_IMMERSION_AUDIT.md`. These rows track the next layer after mechanical completion: moving companion arcs out of abstract camp-menu decisions and into direct dialogue, witnesses, locations, and short adventure beats.

- [x] Audit current companion quest menu surfaces and identify immersion gaps.
- [x] Every companion has a pending incident that can be discussed directly through companion dialogue.
- [x] Every companion has at least one quest choice delivered through dialogue, not only a camp menu.
- [x] Ymira, Lezalit, Bunduk, Jeremus, and Firentis pending incidents can be discussed directly through companion dialogue.
- [x] Ymira, Lezalit, Bunduk, Jeremus, and Firentis quest branch choices can be resolved through dialogue.
- [x] Katrin, Deshavi, Klethi, Rolf, Alayen, Nizar, Baheshtur, Matheld, and Artimenner pending incidents can be discussed directly through companion dialogue.
- [x] Katrin, Deshavi, Klethi, Rolf, Alayen, Nizar, Baheshtur, Matheld, and Artimenner quest branch choices can be resolved through dialogue.
- [x] Camp menus are fallback, travel-planning, or compatibility surfaces rather than the default climax for every companion quest.
- [x] Ymira's captive/refugee arc has first-pass shelter destination logic and location-gated resolution.
- [x] Ymira's shelter destination uses cause-aware target scoring with village safety, health, prosperity, Slaver heat, Jotnar hearth pressure, and Elephant Guard sanctuary pressure.
- [x] Ymira's captive/refugee arc can involve village elder shelter witness dialogue, not only companion dialogue.
- [x] Ymira's captive/refugee arc can involve direct villager refugee-witness dialogue.
- [x] Ymira's captive/refugee arc can involve direct captive/refugee troop witness dialogue.
- [x] Lezalit's Imperial drill arc can involve captured doctrine, troops, or an Imperial witness in dialogue.
- [x] Bunduk's line grievance can involve a troop spokesperson or company petition dialogue.
- [x] Jeremus' triage arc can involve wounded soldier/refugee/prisoner witness dialogue.
- [x] Firentis' restitution arc can involve a village elder and focus village.
- [x] Firentis' restitution focus village uses the shared cause-aware target selector instead of nearest-village fallback.
- [x] Deshavi's trail arc has a first-pass travel/inspect step before final resolution.
- [x] Deshavi's trail arc uses cause-aware target scoring with village hardship, threat, Slaver pressure, Jotnar/Elephant anti-slaver pressure, and Black Khergit horde pressure.
- [x] Deshavi's trail arc has village elder witness dialogue at the focus location.
- [x] Deshavi's trail arc has direct villager survivor/trail witness dialogue at the focus location.
- [x] Deshavi's trail arc has direct hunter/pursuer or ambush-party witness dialogue through Slaver pursuer encounter talk.
- [x] Klethi's old-job arc has a tavern/contact/underworld witness step before final resolution.
- [x] Baheshtur's saddle arc can involve Black Khergit survivors, prisoners, or defectors.
- [x] Katrin's shortage arc is integrated with company accounts, rations, or troop petitions.
- [x] Matheld's shield-line arc is integrated with post-battle morale or troop witnesses.
- [x] Nizar's impossible charge arc can surface before a battle, pursuit, or tournament moment.
- [x] Artimenner's siege arc is integrated with siege preparation or construction context.
- [x] Rolf and Alayen public-honor arcs can surface in town, tavern, lord hall, tournament, or village contexts.
- [x] Static tests confirm direct-talk pending incident entries for migrated arcs.
- [x] Static tests confirm adventure arcs store or derive focus center, focus party, or focus cause where needed.

## Companion Depth Priority Queue

Current best next passes if we want the fastest movement toward the Dragon Age-style target:

- [x] Borcha: roadcraft and Black Khergit integration pass.
- [x] Marnid: trade, caravan, and honest-profit integration pass.
- [x] Ymira: mercy, captives, and Surgeon payoff initial pass.
- [x] Ymira: add a fuller captive/refugee quest menu with protection, ransom, and expedience paths.
- [ ] Ymira: finish with additional aftermath dialogue and manual QA for each captive/refugee path.
- [x] Lezalit: add multi-stage direct talk and a stronger resolved-good Captain/training payoff.
- [x] Lezalit: add a captured Imperial drill quest menu with reform, fear, and refusal paths.
- [ ] Lezalit: finish manual QA for each Imperial drill path.
- [x] Bunduk: add soldier-welfare quest incident tied to casualties, wages, or officer cruelty.
- [x] Bunduk: add line grievance quest menu with advocate, compromise, and crackdown paths.
- [ ] Bunduk: finish manual QA for each line grievance path.
- [x] Jeremus: add battlefield triage incident beyond campfire.
- [x] Jeremus: add triage menu with mercy, hard triage, and company-first paths.
- [ ] Jeremus: finish manual QA for each triage path.
- [x] Firentis: add restitution or battlefield mercy incident beyond campfire.
- [x] Firentis: add restitution menu with protection, confession, and silence paths.
- [ ] Firentis: finish manual QA for each restitution path.
- [x] Katrin: add food/wage shortage incident beyond campfire.
- [x] Katrin: add shortage menu with stores, rationing, and glory-spend paths.
- [ ] Katrin: finish manual QA for each shortage path.
- [x] Deshavi: add trail warning incident tied to poor villages, Slavers, or raiders.
- [x] Deshavi: add trail warning menu with shelter, ambush, and hunt-only paths.
- [ ] Deshavi: finish manual QA for each trail warning path.
- [x] Klethi: add underworld/stealth incident beyond campfire.
- [x] Klethi: add old-job menu with choose, protect, and sellout paths.
- [ ] Klethi: finish manual QA for each old-job path.
- [x] Rolf, Alayen, and Nizar: add public honor/glory/noble legitimacy incident cluster.
- [x] Rolf: add public legitimacy world incident tied to lordly courts, tournaments, or honors.
- [x] Rolf: add public challenge menu with earn, defend, and expose paths.
- [x] Alayen: add oath/standard world incident tied to diplomacy, lord release, or village protection.
- [x] Alayen: add oath menu with duty, oath, and pride paths.
- [x] Nizar: add hard-victory or tournament-glory world incident.
- [x] Nizar: add heroic action menu with responsible, daring, and blood-legend paths.
- [x] Baheshtur, Matheld, and Artimenner: add battlefield freedom/courage/engineering incident cluster.
- [x] Baheshtur: add Black Khergit rider incident with free, pursuit, and submission paths.
- [x] Baheshtur: add mounted-pursuit or Black Khergit pressure payoff for resolved-good Scout/Captain.
- [x] Matheld: add battlefield courage incident beyond campfire.
- [x] Matheld: add battlefield line menu with temper, stand, and blood-price paths.
- [x] Artimenner: add construction/siege-preparation world incident beyond campfire.
- [x] Artimenner: add construction menu with rebuild, improvise, and blame paths.

## Global Framework

- [x] Add companion approval slots.
- [x] Add trust tier, warning state, role, last reaction day, personal quest stage, and loyalty lock slots.
- [x] Add approval bands: devoted, loyal, steady, wary, troubled, near breaking.
- [x] Add companion action IDs for major world choices.
- [x] Add companion advisor roles: Quartermaster, Surgeon, Scout, Captain, Envoy, Engineer, Spymaster.
- [x] Add daily companion depth processing.
- [x] Add role effect processing.
- [x] Add approval shifting helper with warning state support.
- [x] Add trust threshold that unlocks personal quest stage.
- [x] Add campfire menu.
- [x] Add campfire warning acknowledgement.
- [x] Add company report integration.
- [x] Add static companion-depth test.
- [x] Add companion design bible.
- [x] Add voice guide, approval tiers, quest outcome index, and cross-companion triangle notes.
- [x] Add a dedicated companion report page with one row per companion.
- [x] Add companion-specific warning conversations for every companion.
- [x] Add companion-specific departure/reconciliation logic after warnings.
- [x] Add a clearer display for active advisor role bonuses.
- [x] Add a debug/test menu option to inspect companion approval bands in-game.
- [x] Add common helper for companion-specific campfire mood text to reduce script bloat.
- [x] Add common helper for role bonus report text.
- [x] Add common helper for companion quest stage labels.
- [x] Add common helper for warning/reconciliation availability.
- [x] Add per-companion cooldowns for strong reaction messages.
- [x] Add a safe way to clear/repair hard warning states.
- [x] Add "strongest loyalty" and "sharpest doubt" companion report detail.
- [x] Add "unresolved personal matters" report detail.
- [x] Add "company triangles" report detail when conflicting companions are present.

## Shared Gameplay Hooks

- [x] Slaver prisoner selling affects companion approval.
- [x] Buying slaves affects companion approval.
- [x] Carrying slaves through Slaver market logic affects companion approval.
- [x] Freeing captives affects companion approval.
- [x] Lord execution affects companion approval.
- [x] Village help affects companion approval.
- [x] Village abuse/taking food/looting affects companion approval.
- [x] Training troops affects companion approval.
- [x] Defeating Imperial Expeditionary Force heroes affects companion approval.
- [x] Black Khergit tribute affects companion approval.
- [x] Black Khergit bribe/persuasion affects companion approval.
- [x] Black Khergit defeats affect companion approval.
- [x] Battle clean-victory/heavy-loss/retreat outcomes affect Borcha.
- [x] Jotnar support affects companion approval.
- [x] Elephant Guard support affects companion approval.
- [x] Diplomacy policy hooks affect companion approval.
- [x] Trade profit/caravan protection should affect Marnid directly.
- [x] Hunger/food shortage should affect Borcha, Deshavi, Katrin, and Klethi.
- [x] Unpaid wages should affect Katrin, Marnid, Lezalit, and Bunduk.
- [x] Heavy casualties should affect Borcha, Deshavi, Bunduk, Artimenner, and Baheshtur.
- [x] Tough-odds victory should affect Nizar, Matheld, Alayen, and Lezalit.
- [x] Peace treaties and honorable diplomacy should affect Jeremus, Ymira, Alayen, and Marnid.
- [x] Siege preparation/building/engineering choices should affect Artimenner.
- [x] Scout/ambush/road-warning events should affect Borcha, Deshavi, and Klethi.
- [x] Caravan escort completion should affect Marnid and Borcha.
- [x] Defending villages from raiders should affect Ymira, Firentis, Bunduk, Deshavi, and Alayen.
- [x] Raiding villages should affect Ymira, Firentis, Jeremus, Bunduk, Deshavi, Marnid, and Katrin.
- [x] Breaking Slaver caravans should affect Ymira, Jeremus, Jotnar-aligned companions, and possibly Marnid.
- [x] Supporting Slavers should affect Ymira, Jeremus, Firentis, Deshavi, and Bunduk negatively.
- [x] Supporting Elephant Guard should affect Ymira, Jeremus, Alayen, and Firentis positively.
- [x] Supporting Jotnar hearth work should affect Ymira, Firentis, Deshavi, Katrin, and Bunduk positively.
- [x] Supporting Black Army security should affect Lezalit, Bunduk, Alayen, and Artimenner differently.
- [x] Paying Black Khergit tribute should affect Borcha, Marnid, Matheld, Baheshtur, and Alayen differently.
- [x] Bribing Black Khergits toward another target should create mixed reactions from Borcha, Marnid, Ymira, and Alayen.
- [x] Defeating Black Khergit camp should affect Borcha, Baheshtur, Matheld, and Alayen.
- [x] IEF hero deaths should affect Lezalit, Alayen, Ymira, Jeremus, and Firentis.
- [x] Diplomacy betrayal should affect Alayen, Firentis, Jeremus, Marnid, Rolf, and Nizar.
- [x] Peace after high war weariness should affect Jeremus, Ymira, Katrin, Marnid, and Firentis.
- [x] Tournament/duel glory should affect Nizar, Matheld, Rolf, Alayen, and Baheshtur.
- [x] Building hospitals/ambulatory should affect Jeremus and Ymira.
- [x] Building markets/banks/manufactures should affect Marnid and Artimenner.
- [x] Building walls/security improvements should affect Artimenner, Lezalit, Bunduk, and Katrin.
- [x] Completing construction without wasted workforce should affect Artimenner and Marnid.

## Writing Deliverables

Use this section before touching quest-framework migration. The companion-depth code already provides the baseline writing surface; remaining unchecked rows are DAO-depth prose gaps, not missing plumbing.

### Baseline Writing Coverage

For every companion:

- [x] 6 campfire mood lines, one per approval band.
- [x] 1 generic "ask how you are" direct dialogue response.
- [x] 1 trust-unlock line.
- [x] 1 warning line.
- [x] 1 reconciliation line.
- [x] 1 role assignment line for each valid role.
- [x] 1 role-active report sentence.
- [x] 1 role-disabled/low-approval sentence.
- [x] 1 quest opening line.
- [x] 2 middle-stage choice lines.
- [x] 1 good resolution line.
- [x] 1 hard resolution line.
- [x] 1 aftermath line after good resolution.
- [x] 1 aftermath line after hard resolution.
- [x] 1 triangle dispute seed.
- [x] 2 banter seeds with liked companion.
- [x] 2 banter seeds with disliked companion.
- [x] 1 late-game reflection line.

### Writing Coverage Matrix

| Companion | Mood bands | Direct talk | Warning/repair | Role prose | Quest beats | Aftermath | Triangle seed | Banter seeds | Late reflection |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Borcha | Done | Done | Done | Done | Done | Done | Done | Partial | Done |
| Marnid | Done | Done | Done | Done | Done | Done | Done | Partial | Done |
| Ymira | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Lezalit | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Bunduk | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Jeremus | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Firentis | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Rolf | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Alayen | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Nizar | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Baheshtur | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Matheld | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Artimenner | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Katrin | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Deshavi | Done | Done | Done | Done | Done | Done | Done | Done | Done |
| Klethi | Done | Done | Done | Done | Done | Done | Done | Done | Done |

### Banter Seed Backlog

- [x] Borcha/Marnid: add two practical-friendship banter seeds and two road-vs-status friction seeds.
- [x] Ymira/Lezalit/Bunduk: add two mercy-discipline-soldier welfare banter seeds and two argument seeds.
- [x] Firentis/Jeremus/Matheld: add two penance-healing banter seeds and two courage-vs-restraint argument seeds.
- [x] Rolf/Alayen/Nizar: add two public-honor banter seeds and two legitimacy/glory argument seeds.
- [x] Baheshtur/Katrin/Artimenner: add two road-supplies-planning banter seeds and two freedom-vs-accounts argument seeds.
- [x] Deshavi/Klethi/Katrin: add two survival-practicality banter seeds and two theft-vs-care argument seeds.

### Late Reflection Backlog

- [x] Borcha: late reflection after Black Khergit camp disruption.
- [x] Marnid: late reflection after major trade stability.
- [x] Ymira: late reflection after repeated captive mercy or repeated slave-trade cruelty.
- [x] Lezalit: late reflection after repeated disciplined victories or repeated command weakness.
- [x] Bunduk: late reflection after repeated soldier-welfare choices or repeated needless casualties.
- [x] Jeremus: late reflection after repeated healing/peace choices or repeated cruelty.
- [x] Firentis: late reflection after repeated restraint/penance choices or repeated dishonorable bloodshed.
- [x] Rolf: late reflection after repeated public honors or repeated humiliation/status fraud.
- [x] Alayen: late reflection after repeated honorable diplomacy or repeated oath-breaking.
- [x] Nizar: late reflection after repeated responsible glory or repeated cowardice.
- [x] Baheshtur: late reflection after repeated free-rider respect or repeated coercion.
- [x] Matheld: late reflection after repeated courageous stands or repeated avoidant command.
- [x] Artimenner: late reflection after repeated careful engineering or repeated ignored expertise.
- [x] Katrin: late reflection after repeated practical care or repeated waste.
- [x] Deshavi: late reflection after repeated poor-village protection or repeated neglect.
- [x] Klethi: late reflection after repeated chosen-belonging choices or repeated betrayal.

## Dialogue File Pattern

For each companion, prefer:

- [x] `anyone_plyr_companion_depth_borcha.py`
- [x] `anyone_companion_depth_borcha.py`
- [x] `anyone_plyr_companion_depth_marnid.py`
- [x] `anyone_companion_depth_marnid.py`
- [x] `anyone_plyr_companion_depth_<name>.py` for every remaining companion.
- [x] `anyone_companion_depth_<name>.py` for every remaining companion.
- [ ] Optional warning files only when the generic state is not expressive enough.
- [ ] Optional personal quest files if the campfire menu becomes too crowded.
- [x] Register each file near the existing member-talk companion entries.
- [x] Keep direct dialogue available from `member_talk`.
- [x] Keep campfire quest choices available from `mnu_companion_campfire`.

## Companion Implementation Template

Use this per-companion standard for future expansion passes. The global framework is implemented; unchecked rows should mean a real future content gap, not a reminder to confirm existing plumbing.

### Identity and Values

- [x] Confirm design bible entry is complete.
- [x] Confirm core wound, core value, and command fear are distinct.
- [x] Confirm default advisor role and fallback role fit the companion.
- [x] Confirm approval band language matches the companion's voice.

### Approval and Reactivity Hooks

- [x] Add companion-specific approval deltas in `sod_companion_apply_player_action`.
- [x] Add at least one positive shared-world hook.
- [x] Add at least one negative shared-world hook.
- [x] Add warning and reconciliation text before departure risk.
- [x] Add optional late-game reflection hook when the companion's theme has been proven over time.

### Campfire and Direct Dialogue

- [x] Add campfire mood text by approval band.
- [x] Add personal quest campfire opening.
- [x] Add direct `member_talk` dialogue entry.
- [x] Add companion response dialogue.
- [x] Register dialogue files in `_order_dialogs.txt`.

### Advisor Role and Degraded State

- [x] Add role assignment flavor lines.
- [x] Add role effect payoff.
- [x] Add low-approval/degraded role state text.
- [x] Ensure low approval weakens or blocks the role payoff.

### Personal Quest Stages and Outcomes

- [x] Add quest framework ID/name.
- [x] Add quest journal opening text.
- [x] Add quest journal stage update text.
- [x] Add quest journal good outcome text.
- [x] Add quest journal hard outcome text.
- [x] Add quest journal failure or rupture text.
- [x] Add at least one recorded memory event.
- [x] Add at least one quest outcome consequence beyond approval.
- [x] Add at least one triangle or companion witness reaction where thematically appropriate.
- [x] Add trust opening.
- [x] Add at least two path choices.
- [x] Add good/trust resolution.
- [x] Add hard/compromise or rupture resolution.
- [x] Add at least one beyond-campfire incident where world play tests the companion's values.
- [x] Add one non-fatal warning consequence for the bad path when the theme calls for it.

### Cross-Companion Triangle Coverage

- [x] Add at least one friend, foil, or rival triangle.
- [x] Surface triangle status in the companion depth report.
- [x] Add optional triangle-specific incident when three companions have a strong shared stake.

### World-System Integration

- [x] Connect companion values to at least one existing world system.
- [x] Prefer existing hooks such as captives, prisoners, IEF victories, caravans, villages, diplomacy, construction, and horde pressure.
- [x] Avoid new scenes, art, or large quest infrastructure unless the companion truly needs it.
- [ ] Add manual QA scenario for each new world incident.

### Static Tests and Build Verification

- [x] Update companion-depth static test.
- [x] Add static checks for new helper scripts, action IDs, report text, and hook sites.
- [x] Run focused companion static coverage.
- [x] Run broad feature audit.
- [x] Run doctor and full module build.
- [x] Update this checklist after implementation.
- [ ] Update `COMPANION_DEPTH_BIBLE.md` if implementation changes the design.

## Advisor Role Checklist

- [x] Borcha: Scout.
- [x] Marnid: Quartermaster.
- [x] Ymira: Surgeon.
- [x] Lezalit: Captain.
- [x] Rolf: Envoy or Captain.
- [x] Baheshtur: Scout or Captain.
- [x] Firentis: Captain or Envoy.
- [x] Deshavi: Scout or Spymaster.
- [x] Matheld: Captain.
- [x] Alayen: Envoy or Captain.
- [x] Bunduk: Captain or Quartermaster.
- [x] Katrin: Quartermaster or Surgeon.
- [x] Jeremus: Surgeon or Envoy.
- [x] Nizar: Captain or Scout.
- [x] Artimenner: Engineer or Quartermaster.
- [x] Klethi: Spymaster or Scout.
- [x] Each role has an approval gate.
- [x] Each role has a low-approval degraded state.
- [x] Each role has at least one unique companion-specific payoff.
- [x] Each role has report text explaining what it does.

## Companion Rollout Order

- [x] Borcha.
- [x] Marnid.
- [x] Ymira polish.
- [x] Lezalit polish.
- [x] Deshavi.
- [x] Klethi.
- [x] Firentis.
- [x] Jeremus.
- [x] Bunduk.
- [x] Katrin.
- [x] Matheld.
- [x] Alayen.
- [x] Rolf.
- [x] Nizar.
- [x] Baheshtur.
- [x] Artimenner.

Recommended rationale:

- [x] Road and ledger pair first: Borcha and Marnid.
- [x] Mercy and discipline prototypes next: Ymira and Lezalit.
- [x] Scout/underworld layer next: Deshavi and Klethi.
- [x] Company conscience layer next: Firentis, Jeremus, Bunduk, Katrin.
- [x] Glory/rank/warcraft layer last: Matheld, Alayen, Rolf, Nizar, Baheshtur, Artimenner.

## Borcha - The Road Keeps Its Own

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Scout.
- [x] Approval hooks for safe roadcraft.
- [x] Approval hooks for costly battle.
- [x] Approval hooks for village help/abuse.
- [x] Approval hooks for Black Khergit tribute/bribe.
- [x] Approval hooks for Black Khergit defeat/disruption.
- [x] Campfire approval-band mood text.
- [x] Scout role assignment flavor.
- [x] Quartermaster role assignment flavor.
- [x] Scout role effect reduces Black Khergit pressure.
- [x] Good quest resolution improves Scout payoff.
- [x] Campfire quest opening.
- [x] Trust/scout route choice.
- [x] Plunder route choice.
- [x] Dismiss route choice.
- [x] Good resolution.
- [x] Hard/profit resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Static test coverage.
- [x] Build verified.
- [ ] Add richer multi-stage quest beyond campfire resolution.
- [x] Add a real road incident tied to an active Black Khergit raider/camp target.
- [x] Add Borcha-specific warning dialogue when approval is troubled.
- [x] Add reconciliation dialogue after warning.
- [x] Add optional synergy with Marnid for road-and-ledger choices.
- [x] Add Borcha/Borcha-specific report sentence for Scout active.
- [x] Add Borcha low-approval role-disabled sentence.
- [x] Add Borcha late-game reflection after Black Khergit camp disruption.
- [x] Add Borcha/Deshavi rivalry banter over tracks.
- [x] Add Borcha/Rolf clash over rank and road knowledge.
- [x] Add Borcha/Marnid friendship banter over routes and ledgers.
- [x] Add hidden-route outcome to world activity if Black Khergit camp exists.

## Marnid - The Honest Price

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Quartermaster.
- [x] Approval hooks for orderly profit.
- [x] Approval hooks for dirty profit.
- [x] Approval hooks for village help/abuse.
- [x] Approval hooks for prisoner selling.
- [x] Approval hooks for slave-adjacent choices.
- [x] Approval hooks for Black Khergit tribute/bribe.
- [x] Campfire approval-band mood text.
- [x] Quartermaster role assignment flavor.
- [x] Envoy role assignment flavor.
- [x] Quartermaster role payoff.
- [x] Good quest resolution improves Quartermaster payoff.
- [x] Campfire quest opening.
- [x] Clean trade choice.
- [x] Dirty prisoner-profit choice.
- [x] Clean resolution.
- [x] Hard/profit resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add direct trade profit hook.
- [x] Add caravan protection hook.
- [x] Add market-town contact event.
- [x] Add Marnid-specific warning dialogue when approval is troubled.
- [x] Add reconciliation dialogue after warning.
- [x] Add optional synergy with Borcha for safe road commerce.
- [x] Add Marnid-specific report sentence for Quartermaster active.
- [x] Add Marnid low-approval role-disabled sentence.
- [x] Add Marnid late-game reflection after major trade stability.
- [x] Add Marnid/Borcha friendship banter over practical survival.
- [x] Add Marnid/Alayen clash over noble contempt for trade.
- [x] Add Marnid/Baheshtur clash over pride vs accounts.
- [x] Add Honest Price outcome to trade or caravan route logic.

## Ymira - Mercy Under Arms

- [x] Prototype approval hooks for captives, slavery, execution, village help/abuse.
- [x] Default role: Surgeon.
- [x] Campfire quest entry exists.
- [x] Direct member-talk entry exists.
- [x] Direct companion response exists.
- [x] Add approval-band campfire mood text.
- [x] Add Surgeon role flavor and improved quest payoff text.
- [x] Expand Mercy Under Arms into staged choices.
- [x] Add mercy/protection choice.
- [x] Add hard necessity choice.
- [x] Add good resolution.
- [x] Add hard resolution.
- [x] Add captive/refugee incident beyond campfire.
- [x] Add bad-resolution warning instead of only generic warning.
- [x] Add reconciliation dialogue.
- [x] Add cross-companion dispute with Lezalit and Bunduk.
- [x] Add expanded background/core notes in `COMPANION_DEPTH_BIBLE.md`.
- [x] Add multi-stage direct-talk responses by warning and quest stage.
- [x] Add resolved-good Surgeon payoff when freeing captives.
- [x] Add dedicated Mercy Under Arms captive/refugee menu beyond campfire.
- [x] Add protection, ransom/weakest-release, and expedience paths.
- [x] Add quest-stage consequences from the captive/refugee menu.
- [ ] Add manual QA for Ymira's direct-talk stage variants.
- [ ] Add manual QA for Ymira's resolved-good Surgeon captive payoff.
- [ ] Add manual QA for Mercy Under Arms protection, ransom, and expedience paths.

## Lezalit - Discipline Without Chains

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Captain.
- [x] Secondary role: Engineer.
- [x] Approval hooks for training.
- [x] Approval hooks for IEF defeat.
- [x] Approval hooks for executions and hard discipline.
- [x] Disapproval hooks for retreat/fail and weak command.
- [x] Disapproval hooks for unpaid troops and chaotic mercy.
- [x] Campfire approval-band mood text.
- [x] Captain role assignment flavor.
- [x] Engineer role assignment flavor.
- [x] Captain role payoff.
- [x] Good quest resolution improves Captain payoff.
- [x] Campfire quest opening.
- [x] Reform choice.
- [x] Harsh punishment choice.
- [x] Dismissal choice.
- [x] Reform resolution.
- [x] Hard/fear resolution.
- [x] IEF discipline incident beyond campfire.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion dispute with Ymira and Bunduk.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add multi-stage direct-talk responses by warning and quest stage.
- [x] Add resolved-good Captain training payoff beyond morale.
- [x] Add dedicated Discipline Without Chains captured Imperial drill menu beyond campfire.
- [x] Add reform, fear, and refusal paths.
- [x] Add pending IEF victory incident state from post-battle logic.
- [ ] Add manual QA for IEF discipline incident.
- [ ] Add manual QA for Lezalit direct-talk stage variants.

## Rolf - A Name Worth Wearing

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Envoy.
- [x] Secondary role: Captain.
- [x] Approval hooks for public honor.
- [x] Approval hooks for noble diplomacy.
- [x] Approval hooks for decisive victories.
- [x] Disapproval hooks for humiliation.
- [x] Disapproval hooks for shabby conduct.
- [x] Disapproval hooks for commoner-first choices.
- [x] Campfire approval-band mood text.
- [x] Envoy role assignment flavor.
- [x] Captain role assignment flavor.
- [x] Envoy/Captain role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Claimant/title challenge event.
- [x] Defend/redefine dignity choice.
- [x] Preserve the lie/status choice.
- [x] Expose/humiliate choice.
- [x] Earned dignity resolution.
- [x] Exposed/rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Alayen and Nizar.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add public legitimacy world incident tied to lordly courts, tournaments, or honors.
- [x] Add dedicated A Name Worth Wearing public challenge menu beyond campfire.
- [x] Add earn, defend, and expose paths.
- [x] Add Rolf-specific report sentence for Envoy active.
- [x] Add Rolf low-approval role-disabled sentence.
- [ ] Add Rolf late-game reflection after repeated public honors.
- [ ] Add manual QA for title challenge paths.

## Baheshtur - The Unbroken Saddle

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Scout.
- [x] Secondary role: Captain.
- [x] Approval hooks for mounted victories.
- [x] Approval hooks for fast campaigns.
- [x] Approval hooks for bold movement.
- [x] Approval hooks for refusing humiliation.
- [x] Disapproval hooks for heavy casualties.
- [x] Disapproval hooks for timidity.
- [x] Disapproval hooks for excessive bargaining.
- [x] Disapproval hooks for hunger and slow defensive wars.
- [x] Campfire approval-band mood text.
- [x] Scout role assignment flavor.
- [x] Captain role assignment flavor.
- [x] Scout/Captain role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Steppe rival or Black Khergit warband event.
- [x] Free loyalty choice.
- [x] Mutual respect compromise choice.
- [x] Submission/refusal choice.
- [x] Free loyalty resolution.
- [x] Submission/rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Katrin and Artimenner.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add mounted-pursuit or Black Khergit pressure payoff for resolved-good Scout/Captain.
- [x] Add dedicated The Unbroken Saddle Black Khergit rider menu beyond campfire.
- [x] Add free, pursuit, and submission paths.
- [x] Add Baheshtur-specific report sentence for Scout active.
- [x] Add Baheshtur low-approval role-disabled sentence.
- [ ] Add manual QA for Black Khergit/steppe rival event.

## Firentis - Debt of the Sword

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Captain.
- [x] Secondary role: Envoy.
- [x] Approval hooks for restraint.
- [x] Approval hooks for village protection.
- [x] Approval hooks for honorable command.
- [x] Approval hooks for sparing the helpless.
- [x] Disapproval hooks for cruelty.
- [x] Disapproval hooks for excessive fighting.
- [x] Disapproval hooks for failed promises.
- [x] Disapproval hooks for executions.
- [x] Campfire approval-band mood text.
- [x] Captain role assignment flavor.
- [x] Envoy role assignment flavor.
- [x] Captain/Envoy role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Past-victim or penance event.
- [x] Confession/restitution choice.
- [x] Concealment choice.
- [x] Violence/erasure choice.
- [x] Restitution resolution.
- [x] Concealment/violence rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Jeremus and Matheld.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add battlefield mercy or village restitution world incident.
- [x] Add dedicated Debt of the Sword restitution menu beyond campfire.
- [x] Add restitution, confession, and silence paths.
- [x] Add Firentis-specific report sentence for Captain active.
- [x] Add Firentis low-approval role-disabled sentence.
- [ ] Add manual QA for penance event paths.

## Deshavi - Tracks Through Ash

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Scout.
- [x] Secondary role: Spymaster.
- [x] Approval hooks for food security.
- [x] Approval hooks for caution and low casualties.
- [x] Approval hooks for poor-village protection.
- [x] Approval hooks for scouting enemy movements.
- [x] Disapproval hooks for hunger.
- [x] Disapproval hooks for heavy losses.
- [x] Disapproval hooks for village abuse.
- [x] Disapproval hooks for ignored trails.
- [x] Campfire approval-band mood text.
- [x] Scout role assignment flavor.
- [x] Spymaster role assignment flavor.
- [x] Scout/Spymaster role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Destroyed settlement or raider/slaver trail event.
- [x] Rescue/shelter choice.
- [x] Ambush-first choice.
- [x] Keep-marching/survival choice.
- [x] Justice/rescue resolution.
- [x] Hard hunt-only resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Borcha and Rolf.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add active trail warning world incident tied to raiders, Slavers, or poor villages.
- [x] Add dedicated Tracks Through Ash trail warning menu beyond campfire.
- [x] Add shelter, ambush, and hunt-only paths.
- [x] Add Deshavi-specific report sentence for Scout/Spymaster active.
- [x] Add Deshavi low-approval role-disabled sentence.
- [ ] Add manual QA for trail event paths.

## Matheld - No Backward Step

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Captain.
- [x] Approval hooks for courage.
- [x] Approval hooks for hard fights.
- [x] Approval hooks for direct challenges.
- [x] Approval hooks for punishing raiders.
- [x] Disapproval hooks for fleeing.
- [x] Disapproval hooks for repeated compromise.
- [x] Disapproval hooks for unavenged insult.
- [x] Disapproval hooks for mercy that creates danger.
- [x] Campfire approval-band mood text.
- [x] Captain role assignment flavor.
- [x] Captain role payoff.
- [x] Good quest resolution improves Captain payoff.
- [x] Personal quest opening.
- [x] Direct threat/challenge event.
- [x] Stand-firm choice.
- [x] Temper-courage choice.
- [x] Blood-price choice.
- [x] Courage-tempered resolution.
- [x] Needless-bloodshed rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Firentis and Jeremus.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add hard-battle morale payoff for resolved-good Captain.
- [x] Add dedicated No Backward Step battlefield line menu beyond campfire.
- [x] Add temper, stand, and blood-price paths.
- [x] Add Matheld-specific report sentence for Captain active.
- [x] Add Matheld low-approval role-disabled sentence.
- [ ] Add manual QA for threat/challenge paths.

## Alayen - The Standard and the Self

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Envoy.
- [x] Secondary role: Captain.
- [x] Approval hooks for honorable victories.
- [x] Approval hooks for kept oaths.
- [x] Approval hooks for noble responsibility.
- [x] Approval hooks for disciplined tactics.
- [x] Disapproval hooks for dishonor.
- [x] Disapproval hooks for failed obligations.
- [x] Disapproval hooks for crude profiteering.
- [x] Disapproval hooks for dishonorable deals.
- [x] Campfire approval-band mood text.
- [x] Envoy role assignment flavor.
- [x] Captain role assignment flavor.
- [x] Envoy/Captain role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Family pride vs humble honor event.
- [x] Responsibility choice.
- [x] Family pride choice.
- [x] Humble duty choice.
- [x] Responsibility resolution.
- [x] Pride/rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Rolf and Nizar.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add oath/standard world incident tied to diplomacy, lord release, or village protection.
- [x] Add dedicated The Standard and the Self oath menu beyond campfire.
- [x] Add duty, oath, and pride paths.
- [x] Add Alayen-specific report sentence for Envoy active.
- [x] Add Alayen low-approval role-disabled sentence.
- [ ] Add manual QA for family pride event paths.

## Bunduk - The Men Who Hold the Line

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Captain.
- [x] Secondary role: Quartermaster.
- [x] Approval hooks for soldier welfare.
- [x] Approval hooks for pay.
- [x] Approval hooks for low casualties.
- [x] Approval hooks for village defense.
- [x] Disapproval hooks for heavy losses.
- [x] Disapproval hooks for officer cruelty.
- [x] Disapproval hooks for village abuse.
- [x] Disapproval hooks for noble arrogance.
- [x] Campfire approval-band mood text.
- [x] Captain role assignment flavor.
- [x] Quartermaster role assignment flavor.
- [x] Captain/Quartermaster role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Veteran grievance or brutal-officer event.
- [x] Soldiers' advocate choice.
- [x] Chain-of-command compromise choice.
- [x] Officer-cruelty choice.
- [x] Soldiers' advocate resolution.
- [x] Officer-cruelty rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Ymira and Lezalit.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add casualty-shock or wage-stability payoff for resolved-good Captain/Quartermaster.
- [x] Add dedicated Men Who Hold the Line grievance menu beyond campfire.
- [x] Add advocate, compromise, and crackdown paths.
- [x] Add pending incident state from heavy casualties and unpaid wages.
- [x] Add Bunduk-specific report sentence for Captain active.
- [x] Add Bunduk low-approval role-disabled sentence.
- [ ] Add manual QA for veteran grievance paths.

## Katrin - The Last Coin in Camp

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Quartermaster.
- [x] Secondary role: Surgeon.
- [x] Approval hooks for food.
- [x] Approval hooks for wages.
- [x] Approval hooks for practical care.
- [x] Approval hooks for sensible trade.
- [x] Disapproval hooks for hunger.
- [x] Disapproval hooks for unpaid troops.
- [x] Disapproval hooks for reckless spending.
- [x] Disapproval hooks for endless glory campaigns.
- [x] Campfire approval-band mood text.
- [x] Quartermaster role assignment flavor.
- [x] Surgeon role assignment flavor.
- [x] Quartermaster/Surgeon role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Camp shortage event.
- [x] Pay soldiers choice.
- [x] Feed refugees choice.
- [x] Future supplies/bribe choice.
- [x] Practical-care resolution.
- [x] Heroic-waste rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Deshavi and Klethi.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add food/wage world incident tied to hunger or unpaid wages.
- [x] Add dedicated Last Coin in Camp shortage menu beyond campfire.
- [x] Add stores, rationing, and glory-spend paths.
- [x] Add Katrin-specific report sentence for Quartermaster active.
- [x] Add Katrin low-approval role-disabled sentence.
- [ ] Add manual QA for camp shortage paths.

## Jeremus - Hands That Will Not Harden

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Surgeon.
- [x] Secondary role: Envoy.
- [x] Approval hooks for healing.
- [x] Approval hooks for peace.
- [x] Approval hooks for sparing civilians.
- [x] Approval hooks for restraint.
- [x] Disapproval hooks for excessive fighting.
- [x] Disapproval hooks for executions.
- [x] Disapproval hooks for slavery.
- [x] Disapproval hooks for village abuse.
- [x] Campfire approval-band mood text.
- [x] Surgeon role assignment flavor.
- [x] Envoy role assignment flavor.
- [x] Surgeon/Envoy role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Battlefield triage event.
- [x] Treat civilians first choice.
- [x] Treat allies first choice.
- [x] Refuse/limit care choice.
- [x] Compassion-under-pressure resolution.
- [x] Refusal/rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Firentis and Matheld.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add battlefield triage world incident beyond campfire.
- [x] Add dedicated Hands That Will Not Harden triage menu beyond campfire.
- [x] Add mercy, hard triage, and company-first paths.
- [x] Add pending incident state from costly battle casualties.
- [x] Add Jeremus-specific report sentence for Surgeon active.
- [x] Add Jeremus low-approval role-disabled sentence.
- [ ] Add manual QA for triage event paths.

## Nizar - The Impossible Charge

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Captain.
- [x] Secondary role: Scout.
- [x] Approval hooks for tough-odds victories.
- [x] Approval hooks for daring rescues.
- [x] Approval hooks for renown.
- [x] Approval hooks for public glory.
- [x] Disapproval hooks for excessive caution.
- [x] Disapproval hooks for dull retreats.
- [x] Disapproval hooks for procedure over daring.
- [x] Campfire approval-band mood text.
- [x] Captain role assignment flavor.
- [x] Scout role assignment flavor.
- [x] Captain/Scout role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] High-risk heroic action event.
- [x] Heroic charge choice.
- [x] Responsible courage choice.
- [x] Refuse spectacle choice.
- [x] Glory-with-responsibility resolution.
- [x] Reckless rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Alayen and Rolf.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add hard-victory or tournament-glory world incident.
- [x] Add dedicated The Impossible Charge heroic action menu beyond campfire.
- [x] Add responsible, daring, and blood-legend paths.
- [x] Add Nizar-specific report sentence for Captain active.
- [x] Add Nizar low-approval role-disabled sentence.
- [ ] Add manual QA for heroic action paths.

## Artimenner - The Siege That Should Have Worked

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Engineer.
- [x] Secondary role: Quartermaster.
- [x] Approval hooks for siege preparation.
- [x] Approval hooks for building.
- [x] Approval hooks for logistics.
- [x] Approval hooks for expert advice.
- [x] Disapproval hooks for hunger.
- [x] Disapproval hooks for failed quests.
- [x] Disapproval hooks for avoidable losses.
- [x] Disapproval hooks for ignoring siege logic.
- [x] Campfire approval-band mood text.
- [x] Engineer role assignment flavor.
- [x] Quartermaster role assignment flavor.
- [x] Engineer/Quartermaster role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Failed design/siege event.
- [x] Admit error choice.
- [x] Respect expertise choice.
- [x] Blame others choice.
- [x] Expertise-respected resolution.
- [x] Blame/rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Katrin and Baheshtur.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add construction/siege-preparation world incident beyond campfire.
- [x] Add dedicated The Siege That Should Have Worked construction menu beyond campfire.
- [x] Add rebuild, improvise, and blame paths.
- [x] Add Artimenner-specific report sentence for Engineer active.
- [x] Add Artimenner low-approval role-disabled sentence.
- [ ] Add manual QA for failed design paths.

## Klethi - A Knife With a Name

- [x] Deep background documented.
- [x] Voice guide documented.
- [x] Approval tiers documented.
- [x] Quest outcome index documented.
- [x] Default role: Spymaster.
- [x] Secondary role: Scout.
- [x] Approval hooks for ambushes.
- [x] Approval hooks for stealth.
- [x] Approval hooks for autonomy.
- [x] Approval hooks for food security.
- [x] Disapproval hooks for hunger.
- [x] Disapproval hooks for rigid plans.
- [x] Disapproval hooks for betrayal.
- [x] Disapproval hooks for failed quests.
- [x] Campfire approval-band mood text.
- [x] Spymaster role assignment flavor.
- [x] Scout role assignment flavor.
- [x] Spymaster/Scout role payoff.
- [x] Good quest resolution improves role payoff.
- [x] Personal quest opening.
- [x] Old job recognition event.
- [x] Protect Klethi choice.
- [x] Face the damage on her terms choice.
- [x] Betray/use the secret choice.
- [x] Chosen-belonging resolution.
- [x] Betrayal/rupture resolution.
- [x] Direct member-talk entry.
- [x] Direct companion response.
- [x] Warning dialogue.
- [x] Reconciliation dialogue.
- [x] Cross-companion triangle with Deshavi and Katrin.
- [x] Static test coverage.
- [x] Build verified.
- [x] Add richer multi-stage direct-talk responses by warning and quest stage.
- [x] Add underworld/stealth world incident beyond campfire.
- [x] Add dedicated A Knife With a Name old-job menu beyond campfire.
- [x] Add choose, protect, and sellout paths.
- [x] Add Klethi-specific report sentence for Spymaster active.
- [x] Add Klethi low-approval role-disabled sentence.
- [ ] Add manual QA for old job recognition paths.

## Test Checklist

- [x] `py build\test_companion_depth_system.py`
- [x] `py build\test_feature_audit_static.py`
- [x] `py build\doctor.py --doctor-new-only`
- [x] `cmd /c build_module.bat --no-cache`
- [x] Add static checks for every future companion dialogue pair.
- [x] Add static checks for companion warning dialogue coverage.
- [x] Add static checks for companion role effect coverage.
- [x] Add static checks that each companion has at least one approval hook.
- [x] Add static checks that each personal quest has good and hard outcomes.
- [x] Add static checks that checklist and bible contain matching companion headings.
- [x] Add static checks that rollout order contains every companion.
- [x] Add static checks that every implemented companion has two dialogue files.
- [x] Add static checks that every implemented companion has campfire mood text helper.
- [x] Add static checks for no stale script rename references after `cf_` changes.
- [x] Run `py build\test_population_based_construction.py` after construction helper changes.
- [x] Run focused Black Khergit test after Borcha road changes.
- [x] Run full module build after adding dialogue/menu files.
- [x] Confirm `doctor.py --doctor-new-only` stays at 0 warnings.

## Manual QA Scenarios

- [ ] Recruit Borcha and confirm campfire shows his mood line.
- [ ] Assign Borcha as Scout and confirm role message appears.
- [ ] Resolve Borcha's quest cleanly and confirm Scout effect improves.
- [ ] Defeat Black Khergit raiders with Borcha present and confirm reaction.
- [ ] Win a low-loss battle with Borcha present and confirm approval reaction.
- [ ] Suffer a high-loss battle with Borcha present and confirm disapproval reaction.
- [ ] Recruit Marnid and confirm campfire shows his mood line.
- [ ] Assign Marnid as Quartermaster and confirm role message appears.
- [ ] Resolve Marnid's quest cleanly and confirm Quartermaster effect improves.
- [ ] Choose dirty profit in Marnid's quest and confirm hard outcome.
- [ ] Sell prisoners with Marnid and Ymira present and confirm mixed reaction logic.
- [ ] Free at least three slaves with Ymira's quest open and confirm the captive/refugee incident advances.
- [ ] Keep at least three slaves with Ymira's quest open and confirm her bad-path warning appears.
- [ ] Resolve Mercy Under Arms well, assign Ymira as Surgeon, free at least three slaves, and confirm the organized refuge morale payoff.
- [ ] Talk to Ymira across trust-opened, test-started, resolved-good, resolved-hard, and warning states.
- [ ] Defeat an IEF lord with Lezalit's quest open and confirm the discipline incident advances.
- [ ] Defeat an IEF lord with Ymira, Bunduk, and Lezalit present and confirm the triangle report line appears.
- [ ] Abuse a village with Marnid, Ymira, and Borcha present and confirm all relevant approval drops.
- [ ] Trigger generic grievance acknowledgement at campfire and confirm warning state clears.
- [ ] Talk directly to Borcha through member talk.
- [ ] Talk directly to Marnid through member talk.
- [ ] Confirm direct talk can unlock trust stage at high approval.

## Release Notes Checklist

- [ ] Summarize newly deepened companions.
- [ ] Mention new campfire options.
- [ ] Mention new advisor role effects.
- [ ] Mention new world reactions.
- [ ] Mention any new tests.
- [ ] Mention any known limitations, especially companions still waiting for beyond-campfire quest incidents.
