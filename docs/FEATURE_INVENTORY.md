# Feature Inventory

This document catalogs the major and minor features present in the current `sod_modern` module system. It is an inventory, not a design pitch: entries are based on the source layout, system audits, static tests, menus, mission templates, presentations, quests, and helper scripts currently in the repository.

The project targets Mount & Blade 1.011 / Sword of Damocles Modern, not Warband.

## Source Organization Features

- Modular source fragments under `src/` for constants, dialogs, menus, mission templates, presentations, quests, scripts, and triggers.
- Generated module-system output under `compile/module_*.py`.
- Modular ordering files such as `_order_game_menus.txt`, `_order_dialogs.txt`, `_order_simple_triggers.txt`, `_order_mission_templates.txt`, `_order_quests.txt`, and `_order_constants.txt`.
- Section-code ordering in folders, with descriptive fragment filenames.
- Preamble fragments for imports and shared setup per source category.
- WRECK-style/generated Python build flow through the repo build scripts.
- Static tests under `build/test_*.py` for gameplay systems, export shapes, regressions, and source hygiene.
- Build doctor tooling for missing references, duplicate ids, stubs, global variables, dialog duplicates, and export contract checks.
- Reports and audits under `docs/reports/`, grouped by campaign strategy, combat equipment, companions, dialogue immersion, economy/settlements, parties/world, quests, references, and tooling.
- Maintenance allowlists under `docs/edit/` for doctor findings and intentional exceptions.
- Generated id files under `compile/ids/`.
- Build cache, temporary generation, and standalone builder scripts for menus, dialogs, scripts, quests, presentations, mission templates, simple triggers, and constants.

## Character Creation And Starts

- Original SoD/M&B start flow preserved and modularized.
- Peasant practice start flow.
- Road to the Crown campaign start sequence.
- Seven Oaths of Ash start sequence.
- Faith choice during character creation, stored as the player's creed.
- Culture, realm, and campaign-state initialization hooks.
- Early narrative menus for identity, contacts, council choices, recruitment, village defense, and entry into Calradia.
- New-game player information flow docs and reports.

## Campaign Framework

- Campaign catalog and campaign-state model.
- Branching campaign examples and content examples.
- Scripted campaign arcs with persistent state.
- Campaign quest specs and migration support.
- Campaign bridge events that connect menus, dialogs, quests, parties, and mission templates.
- Campaign strategy reports generated under `docs/reports/campaign_strategy/`.
- Event-driven campaign quest API.
- Runtime event dispatch for quest and campaign progression.
- World event deck/story progression planning.

## Road To The Crown

- Road to the Crown Act I style campaign chain.
- Campaign menus for borrowed names, first recognition, crown council, last road, last smoke, price of bread, hound sign, hounds' terms, three offers, war of witnesses, final confrontation, and door into Calradia.
- Temporary target preparation and cleanup scripts for Road to the Crown scenes and encounters.
- Campaign-state initialization script.
- Static coverage for Road to the Crown menus, scripts, and quest flow.

## Seven Oaths Of Ash

- Seven Oaths of Ash campaign arc.
- Village defense and oath-council menus.
- Recruitment-map, pressure-board, sector-commitment, siege-warning, outer-fields, chapel, quarry, palisade, infirmary, refugee-camp, evacuation-route, watch-platform, gate, pit, and final recruitment menus.
- Seven Ash mission templates for outer fields, palisade, breach, inner streets, and churchyard.
- Oath aftermath/endings archiving.
- Static coverage for Seven Oaths content and quest behavior.

## Quest System

- Modern `src/quests` framework with domain, schema, specs, DSL, runtime, outcomes, event sources, authoring, diagnostics, lanes, migration, giver runtime, and generation modules.
- Quest terminal sentinel to protect quest ordering.
- Quest lanes for grouping and routing quest families.
- Dynamic quest generation rules.
- Runtime quest event API.
- Quest graph export and diagnostics.
- Quest journal system with active log, archive support, and companion personal arc surfacing.
- Quest giver runtime support for lord, enemy lord, army, lady, mayor, village elder, mercenary guild, story/meta, sample campaign, Road to the Crown, companion, and Seven Oaths quests.
- Quest authoring guide, checklist, framework overview, master plan, architecture docs, migration checklist, and QA phase reports.
- Imported/reference quest audits for 108 Heroes and PoP.
- Static checks for quest authoring, generation, runtime, graph exports, graph diagnostics, journal, lanes, party spawn guards, and hostile/rescue/cattle/caravan spawn guards.

## Legacy And Native Quest Families

- Prison break chain.
- Mercenary guild quests.
- Lord quests.
- Enemy lord quests.
- Army quests.
- Lady quests.
- Mayor quests.
- Village elder quests.
- Story and meta quests.
- Cattle, caravan, fugitive, tax, scout, capture-prisoner, raise-troops, deliver-message, duel, peace, and village-bandit style quest logic.
- Captive prisoner recruitment checks.
- Quest party spawn safety.
- Unique quest NPC support.

## Dialogue System

- Modular dialogs split into startup/dispatch, SoD court/strategy, lords/politics/family, centers/economy, townsfolk/special NPCs, encounters/battles/prisoners, companions/named NPCs, and miscellaneous dialog sections.
- Dialogue export static checks.
- Dialogue state inventory and insertion safety docs.
- Player/NPC dialogue immersion audit.
- Dialog close-window safety checks.
- Dialog follow-up spawn guards.
- Invalid-party dialog guards.
- Order-safety tests for inserted immersion dialog.
- Social-weather dialog lines for mayors, elders, merchants, tavernkeepers, and guild/town NPC surfaces.
- Hostile party greeting, local context, negotiation, and reputation reports.
- Party-template-specific dialog for caravans, hostile parties, mini-factions, patrols, deserters, and world activity parties.

## Companion System

- Companion depth system and design bible.
- Companion personal quest arcs surfaced in the quest journal.
- Companion interactive quest checklist, playtest matrix, and QA commands.
- Companion overhaul checklist and immersion audit.
- Companion retinue implementation, battle QA, and party-size audit.
- Companion retinues and non-combat specialists design.
- Companion depth script for recording and reporting companion state.
- Companion grievances, banter, resentment, persuasion, leaving, joining, collecting, switching, and event-triggered talk.
- Companion post-battle comments.
- Companion company report descriptions.
- Companion party screen dialog and membership messages.
- Companion camp job reveal dialog.
- Companion triangle events connected to mini-faction incidents.
- Companion-specific mission templates for Klethi, Ymira, Firentis, Deshavi, Borcha, Marnid, Bunduk, Jeremus, Lezalit, Artimenner, Alayen, Rolf, Baheshtur, Matheld, Katrin, and Nizar.

## Companion Personal Arcs

- Borcha old horde roads.
- Marnid stable-profit/accounting arc.
- Ymira mercy-under-arms arc.
- Rolf public proof and grand-claim arc.
- Baheshtur rider-oath arc.
- Firentis restitution defense arc.
- Deshavi trail rescue arc.
- Matheld shield-line arc.
- Alayen standard/duty arc.
- Bunduk line-test/soldier-defense arc.
- Katrin supply-watch arc.
- Jeremus infirmary/healing arc.
- Nizar charge-lane arc.
- Lezalit discipline-without-chains arc.
- Artimenner repair-watch/design arc.
- Klethi knife-with-name arc.

## Company And Party-Internal Systems

- Company accounts.
- Company morale and ration design.
- Company troop dialogue incidents.
- Company desertion confrontation.
- Surgery and casualty care design.
- Training cadence design.
- Party size reports and centralization.
- Lord party size centralization.
- Unique hero stack sanitization and source checks.
- Party copy, add, wound, prisoner transfer, companion transfer, strength, ideal size, loot, and fit-for-battle helper scripts.
- Party id safety guards and invalid-party hardening.
- Autoresume party globals static checks.

## Camp Systems

- Camp menu extensions.
- Camp jobs and expedition roles.
- Companion camp roles.
- Camp manpower and companion role design.
- Camp jobs script and menu.
- Camp report entry points for diplomacy, mini-factions, quests, economy, strategy, and other reports.

## Court, Ruler, And Kingdom Management

- Chancellor dialog and lord recruitment.
- Marshal/field marshal talk and election logic.
- Strategy advisor dialog and mentor system.
- Jester cheat and skirmish features, gated by cheat mode.
- Council/court entry handling.
- Kingdom reports, ruler menus, and governance menus.
- Player faction activation/deactivation.
- Player join/leave faction logic.
- Player kingdom marshal campaign summon.
- Vassal/lord loyalty static checks.
- No formal standing behavior.
- Lord recruitment support through chancellor.
- Court civilian item flag checks.

## Diplomacy System

- Realm diplomacy as a system beyond war/peace.
- Faction temperament, legitimacy, fear, grievance, war weariness, trade interest, honor stance, slavery stance, border stance, religious stance, crisis, envoy day, and treaty day slots.
- Temperaments: expansionist, defensive, mercantile, honor-bound, predatory, isolationist, opportunist, and anti-Imperial.
- Crisis states for Imperial pressure, Black Khergits, Slavers, famine, succession, and multi-war.
- Diplomatic memory types for border raids, broken truces, lord treatment, caravan attacks, captive freeing, Slaver cooperation, anti-Imperial aid, shared enemies, and tribute.
- War reasons including border dispute, retaliation, conquest, religion, Slaver outrage, Imperial crisis, badboy containment, trade route conflict, broken treaty, Black Khergit pressure, and mercenary pact obligation.
- Treaty records for truces, non-aggression pacts, trade accords, military access, defensive pacts, anti-invasion leagues, tribute, prisoner exchange, anti-slaver compacts, and border security.
- Envoy system with proposal, scoring, cooldown, abstract resolution, companion/chancellor influence, rejections, counteroffers, insults, and detention.
- Realm policies for cultural focus, border control, slavery law, military service, justice, and reconstruction.
- Royal decrees for war taxes, emergency conscription, road patrols, anti-Slaver action, Imperial defense, caravan protection, fortress restoration, grain relief, public executions, and deserter amnesty.
- Realm governance report.
- Diplomatic report.
- Crisis diplomacy report.
- Faction notes with diplomacy state.
- AI diplomacy weekly pulse and personality-driven choices.
- Mini-faction diplomacy hooks for Slavers, Jotnar, Elephant Guard, Black Khergits, Black Army, Serpent Host, and Boar Clan.
- Imperial Expeditionary Force exclusion from normal diplomacy, peace, treaties, and mercenary behavior.

## Faith System

- Five-faith player creed model.
- Faith identities: The One, Old Gods, The Void, Enlightenment, and Natural Philosophy.
- Per-center support for all five faiths.
- Dominant faith, player-faith support, tension, institution strength, stability, recovery, unrest, and ascension readiness profile.
- Weekly center faith drift.
- Population-weighted global faith gain.
- Global faith, holy burden, and effective faith.
- Clergy happiness and clergy legitimacy.
- Faith buildings: shrine, monastery, temple, and chapel.
- Faith institutions affecting support, recovery, unrest, and ascension access.
- Faith troop ascension gates.
- Faith elite troop upgrade mapping.
- Faith ascension holy-burden cost.
- Faith world report and elite doctrine report descriptions.
- Center recon notes with local faith detail.
- Static tests for faith system and ascension gates.

## Laws, Policies, And Governance UI

- SoD law presentation.
- SoD law authoring guide.
- Law generation and diagnostics static checks.
- Policy and decree integration with diplomacy.
- Slider presentation support.
- Fief management presentation.
- Fief management trainer slider static checks.
- Governance report menus.

## Economy And Trade

- Regional economy flow.
- Trade network.
- Trade route setup between centers.
- Trade goods value audit.
- Trade good price pressure.
- Trade good production helpers and feedback.
- Goods consumption.
- Center trade demand profiles.
- Center economy profiles.
- Town market profile.
- Village output profile.
- Village market recovery.
- Food economy profile.
- Food reference audit.
- Edible food counting.
- Merchant town trade and party-center trade scripts.
- Caravan trade liquidity.
- Caravan profitability and scarcity profile.
- Caravan demand dialog.
- Farmer trade tax laws.
- Trade tax laws.
- Tax extraction pressure.
- Tax social pressure.
- Tax couriers and messenger design.
- Wealth/prosperity separation.
- Player gold charging helper.
- Auto-buy food from merchant.
- Auto-sell companion inventory to merchant.
- Item buy/sell price factor game callbacks.

## Settlements And Center Simulation

- Building system and building registry.
- Center modifier system and registry.
- Center modifier migration.
- Construction cost modifiers.
- Population-based construction.
- Population capacity limiter.
- Population reactivity.
- Center population normalization.
- Population supply updates.
- Center public health simulation.
- Center health notifications.
- Center food profile and food store limits.
- Castle building development.
- Town building development.
- Village building development.
- Center investments.
- NPC center investment.
- Center profile caching.
- Center goods market profile and reporting.
- Security economic infrastructure.
- Security threat system.
- Center military modifiers.
- Center security profile.
- Center recon notes.
- Center notes.
- Center guard culture.
- Building modifier discipline.
- Settlement attachments and local economy design.

## Villages

- Village economic root.
- Village recruitment and recruitment-garrison modifiers.
- Village garrison unification.
- Village garrison assault.
- Village bandit-result handling.
- Looter village raids.
- Village market root dialog.
- Village market recovery.
- Village foragers/lightweight logistics planning.
- Volunteer troop updates.
- Bandit infestation updates.
- Village state processing.
- Cattle purchase, stealing, herd creation, and herd killing helpers.
- Cattle quest spawn guards and cattle pipeline checks.

## Castles And Patrols

- Castle support profile.
- Castle food resupply.
- Castle patrol creation.
- Castle patrol processing, success, destruction, refuge, return, target selection, and local cost.
- Castle patrol companion role bonuses.
- Player command, commission, redirect, recall, and order reports for castle patrols.
- Castle patrol population effects.
- Castle patrol faction caps and capacity.
- Castle patrol threat, escort, and route endpoint selection.
- Castle mercenary guild hall building.
- Castle mercenary guild hall stock refresh, troop support, troop selection, stock consumption, access, and reporting.
- Castle mercenary guild hall playtest checklist.

## Towns

- Town market profile.
- Town walkers and center ambiance.
- Tavern NPC refresh scripts for travelers, minstrels, ransom brokers, booksellers, and mercenaries.
- Tavern individual mercenary hiring.
- Goods merchant trade rumors, tax courier rumors, social weather, and market reports.
- Arena/tournament menus and training.
- Town passage/castle passage hardening.

## Prisoners, Slavery, And Captivity

- Prisoner economy and logistics.
- Prisoner, Slaver, Ransom, and Captive system audits.
- Prisoner price game callback.
- Prisoner limit game callback.
- Prisoner transfer to/from hostile parties.
- Hostile prisoner trade.
- Prisoner selling checks.
- Slave ownership consequences and release paths.
- Ramun/Slaver market interactions.
- Prison break mission and quest completion hardening.
- Captivity menus and systemic outcome inputs.
- Party prisoner cleanup and transfer helpers.

## Mercenary Economy

- Mercenary economy audit.
- Mercenary guild economy overhaul.
- Mercenary faction balance audit.
- Mercenary troop cost and role audit.
- Guild favor, guild pacts, master service, service pay, standing perks, quest tiers, reward scaling, price factors, relation factors, and elite relation requirements.
- Contract board descriptions, reports, renewal, extension, and party contract cost.
- Mercenary market overview, kingdom demand, kingdom budget, guild supply, bids, preferred guilds, guardrails, world activity pressure, and weekly pulse.
- AI mercenary clone regression checks.
- Mercenary party limits.
- Mercenary lord spawning and battle outcome tracking.
- Castle mercenary guild hall integration.
- Individual tavern mercenary hiring cleanup and pick flow.

## Mini-Faction World Activity

- Mini-faction world activity dashboard.
- Shared standing ledger, incident reporting, countermeasure reporting, recommendations, local footprints, targeted counterplay, and aftermath.
- Dispatch countermeasures with cooldown and cost.
- Mini-faction incidents connected to quest events, journal updates, and companion triangle events.
- Dashboard links to Slaver, Jotnar, Elephant Guard, Black Khergit, Boar Clan, Serpent Host, Black Army, and Conquistador reports.
- Recent incident, last countermeasure, last pressure shift, world response, targeted counterplay, and local footprint displays.

## Slavers

- Slaver black market.
- Slaver world presence.
- Slaver market heat, supply, safety, access, and anti-Slaver disruption.
- Player actions to buy slaves, free captives, cooperate, or attack.
- Slaver caravans and world activity dialog.
- Slavery law and Anti-Slaver Edict diplomacy hooks.
- Slaver influence in crisis reports.

## Jotnar

- Jotnar world presence.
- Jotnar hearthbound kin system.
- Jotnar hearth pressure.
- Hearth support actions and reports.
- Jotnar clan arena.
- Jotnar revenge/competition quest handling.
- Jotnar approval/disapproval hooks for slavery, captive freeing, mercy, refugees, and border policy.

## Elephant Guard

- Elephant Guard world presence.
- Sacred warden report.
- Elephant Guard training mission.
- Elephant Guard respect for legitimacy and honor.
- Elephant Guard distrust of terror law and reckless conquest.
- Support hooks for prestige and center defense.

## Black Khergits

- Moving Black Khergit horde.
- Horde camp, raiders, and night guard party templates.
- Horde pressure, camp party, safe passage, disrupted camp, raid reports, and camp activity state.
- Spawn/recover camp, pressure economy, day cycle, raids, safe passage, and active-party refresh scripts.
- Bribe target, persuade enemy, defeat guards, and safe-passage actions.
- Black Khergit horde report.
- Khan field audience, duel, hire, prisoner, guard, and raider dialogs.
- Territorial response, individual hiring, guard dialog, and Boar Clan separation checks.

## Boar Clan

- Boar Clan world presence.
- Boar Clan frontier pressure.
- Boar Clan toll behavior.
- Boar Clan encounter scripts and band hire action.
- Boar Clan frontier report.
- Boar Clan fighters and desert-party dialogs.
- Boar Clan connection to trade-route conflict and mini-faction incidents.

## Black Army

- Black Army world presence.
- Black Army security report.
- Black Army contract heat.
- Road-threat interdiction and hire-patrol actions.
- Black Army caravans, patrols, warband aid, and security pressure.
- Integration with mini-faction dashboard and road security.

## Serpent Host

- Serpent Host world presence.
- Serpent route pressure, intelligence, and safe passage.
- Route report.
- Track horde and buy-intel actions.
- Couriers, route screen, and world route dialog.
- Crisis intelligence hooks.

## Conquistadors

- Conquistador world presence.
- Conquistador supply report.
- Requisition heat and supply stock.
- Fund supplies action.
- Expeditionary camp and procurement column dialogs.

## Imperial Expedition

- Imperial Expedition system.
- Invasion arrival and report surfaces.
- Imperial Expeditionary Force special diplomacy exception.
- Dedicated Imperial auxiliaries and mercenary exclusions.
- Imperial hero death gated behind commander/vassal deaths.
- Imperial hero death popup.
- Imperial ruler/centurion/lore dialog hardening.
- Gaius/Marcus-style lore dialog fixes.
- Anti-Imperial league and crisis support.

## Factions, Lords, And Politics

- Faction campaign director.
- Faction doctrine comparison.
- Faction notes with realm systems.
- Faction strength recalculation and power slots.
- Faction AI, objectives, marshal selection, and campaign planning.
- Kingdom support parties strategy layer.
- Messenger command latency planning.
- Lord family structure audit and validation.
- Lord AI bugfixes.
- Lord morale and battle rout enhancement.
- NPC lord morale.
- Lord reinforcement support.
- Lord faction-change notifications.
- Lord hostile encounter none checks.
- Lord duel safety.
- Vassal loyalty checks.
- House politics.
- Pretender politics, state, audit, and system reports.
- Claimant civil war.
- Chancellor lord recruitment.
- Badboy/threat/zealot handling.

## Strategic Map And Reports

- Strategic map presentation.
- Strategic map order guards.
- Campaign strategy and mini-faction reports.
- Regional threat board.
- Threat board contracts, rewards, offers, stakes, active contract descriptions, completion, failure, party links, target spawning, and pressure effects.
- Player-facing exact information audits.
- Party, kingdom, diplomacy, economy, mini-faction, quest, faith, and crisis reports.
- Report/presentation safety hardening.

## Combat Systems

- Formations layer and PBOD/FormRanks references.
- Formation commands, wedge/stagger/ranks behavior, and AI dismount fixes.
- Battle tactics initialization and application.
- Battle advantage calculation.
- Commander duel system.
- Ponavosa commander duel presentation and scripts.
- Lord duels and honor duels.
- Arena challenge fight and SoD arena duel fights.
- Jotnar clan arena.
- Lead charge, siege, village raid, village attack, bandits-at-night, prison break, tutorial, custom battle, and custom battle siege mission templates.
- Late-join battle spawn pressure.
- Battle objective diagnostics.
- Battle spam reward checks.
- Post-battle comments.
- Battle aftermath global validation.
- Nearby party join battle logic.
- Friendly kill checks.
- Battle cry.

## Sieges

- Siege processing.
- Belfry assignment, movement, rotation, and AI.
- Siege object removal.
- Inner battle templates for castles and town centers.
- Wall assault templates for sally, belfry, and ladder assaults.
- Forum siege regiment regression checks.
- Neutral town siege entry bugfix.

## Training, Arenas, And Tournaments

- Training ground menus and mission templates.
- Training ground result, selection, and details flows for melee, ranged, and mounted training.
- Arena training presentation.
- Arena melee fight.
- Tournament item setup.
- Training cadence system.
- AI training mission.

## Items, Equipment, And Loot

- Item system audits.
- Item value and availability audit.
- Item price rebalance.
- Item name typo checks.
- Armor, melee weapon, ranged weapon, ammo, shield, mount, special item, and imod compatibility audits.
- Troop loadout, troop role consistency, tier fit, balance layer, upgrade path, and non-hero troop audits.
- Crossbow rebalance.
- Loot equipment system.
- Auto-loot initialization and item protection.
- Auto-loot evaluation descriptions.
- Protected item recovery from loot pools.
- Equipment degradation after battle.
- Repairability checks and repair cost.
- Player party and troop equipment repair.
- Item modifier degradation.
- Shield banner application.
- Item score/difficulty/cost with item modifiers.
- Item extra text game callback.

## Artifacts And Royal Items

- Royal artifacts presentation.
- Artifact registry initialization.
- Artifact kill tracking, progress, milestones, set rewards, tooltips, doctrine discounts, modifier blocks, lord doctrine bias, transfer, capture spoils, reliquary report, and equipped-set checks.
- Royal pending artifact delivery.
- Royal expedition hero return.
- Artifact system static tests.

## Troop Doctrine And Upgrades

- Elite doctrine report.
- Troop doctrine and elite-tier helper scripts.
- Troop noble checks.
- Faith elite checks.
- Facility-gated upgrades.
- Center-based troop upgrade checks.
- Upgrade cost and failure reason helpers.
- SoD upgrade menu text checks.
- Faith ascension candidate search and upgrade mapping.
- Recruitment/garrison modifier checks.
- Kingdom 6 unique equipment checks.

## Banners And Presentation UI

- Banner selection.
- Custom banner.
- Banner charge positioning and selection.
- Banner background, flag type, flag map type, and color selection.
- Banner drawing to regions.
- Game credits and SoD credits.
- Retirement presentation.
- Horse health presentation.
- Troop trees presentation.
- Description presentation.
- Presentation hardening tests.
- Menu-to-presentation flow checks.

## Books, Notes, And Information

- Books system.
- Bookseller refresh.
- Troop notes and location notes.
- Faction notes and traveler notes.
- Center notes and recon notes.
- Relevant comment helpers.
- Rumor generation.
- Nemesis memory report.
- Deserter lord intel.
- Bandit hideout clues.
- Player-facing reports and exact-information audits.

## Hostile Parties, Bandits, Deserters, And Noncombat Resolution

- Hostile party economy profiles.
- Hostile encounter profiles.
- Hostile reputation memory and reports.
- Hostile greeting, local context, and negotiation options.
- Noncombat hostile economy effects.
- Bribe/redirect hostile party.
- Resolve hostile party without combat.
- Deserter spawning and active-deserter counts.
- Looter/bandit/deserter economy audit.
- Spawn bandits helper.
- Remove-party safety checklist.
- Party ignore-player helpers.
- Campaign party sanity checks.

## Map, Movement, And Travel

- Party speed multiplier game callback.
- Party sees party game callback.
- Detect/undetect party callbacks.
- Movement order name storage.
- Find travel location helper.
- Closest center/town/village/walled-center helpers.
- Patrol detection.
- External follower party audit.
- Messenger party dialogs.
- Map icon and party template generation through the normal module system.

## Menus

- Hardcoded M&B 1.011 report/menu surfaces.
- Arena/tournament menus.
- Camp menus.
- Captivity menus.
- Center common/town/castle/village menus.
- Duel menus.
- Economy menus.
- Encounter menus.
- Event menus.
- Jotnar menus.
- Kingdom/court menus.
- Prisoner menus.
- Reports menus.
- Start-game menus.
- Training menus.
- Empty menu fragment audit to prevent dead-end fragments.
- Menu export static checks.

## Mission Templates

- Native town, village, castle, alley, siege, battle, training, prison break, tutorial, and custom battle templates.
- SoD-specific mercenary base, slaver base, companion quest, Seven Ash, commander duel, arena duel, Jotnar, and training templates.
- Random battlefield scene size checks.
- Random scene setup helper.
- Mission template builder and static coverage.

## Triggers

- Every-frame triggers.
- Hourly triggers.
- Daily triggers.
- Weekly triggers.
- Other/special trigger groups.
- Faith weekly drift and daily ascension triggers.
- Diplomacy daily/weekly processing.
- Mini-faction incident processing.
- World presence updates.
- Economic, settlement, party, and campaign processing.
- String probe trigger.
- Message suppression leak guard.

## Hardcoded Game Callback Coverage

- `game_start`.
- Party encounter.
- Battle end.
- Simulate battle.
- Buy/sell item.
- Detect/undetect party.
- Context menu buttons.
- Party speed, prisoner limit, companion limit, wages, total wages, prisoner price, join cost, item price factors, item extra text, money/date/statistics text, skill modifiers, and prisoner sale checks.
- M&B 1.011 hardcoded callback contract docs and tests.

## Runtime Hardening And Regression Fixes

- Invalid party guards in encounters, dialogs, scripts, and party helpers.
- Remove-party safety.
- String register usage audits.
- Probable string leak tracing.
- Message feed suppression guard.
- Dialog close-window and terminal family audits.
- Menu empty-fragment audit.
- Script export shape checks.
- Split fragment duplicate-id checks.
- Modernization static checks.
- Forum regression checks.
- Legacy bugfix tests for duels, formations, party encounters, castle passages, court entry, battle debriefs, prison break, and companion/lore dialog.

## Build, Test, And Tooling

- `build_module.bat` and slow build variant.
- `build/build_all.py` orchestrator.
- Standalone builders for core generated files.
- Doctor command and tests.
- Constants merge/build scripts.
- Slot allocation verification.
- Static audit scripts for food, population, construction, buildings, center modifiers, item systems, weapons, armor, shields, mounts, lord families, trade goods, taxes, string registers, and security threat.
- Dialogue immersion report generator.
- Build profile and version files.
- IDE setup documentation.
- Modernization checklist.
- Optimization backlog.
- Runtime regression hardening audit.

## Documentation Set

- Documentation map.
- Campaign framework docs.
- Combat and formation docs.
- Companion docs.
- Company docs.
- Economy docs.
- Quest framework docs.
- Settlement docs.
- System docs for diplomacy, faith, strategy advisor, and center modifiers.
- Tooling docs.
- Generated reports and audits.
- Reference feature adaptation docs.
- Playtest checklists for major systems such as castle mercenary guild halls.

