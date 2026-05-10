# Strategy Advisor Mentor Overhaul

## Summary

Turn the generic `Strategy Advisor` into a named mentor character with a real past, evolving relationship, and stronger court/field presence. He should feel like the player's old family mentor: a wounded veteran, former Imperial infiltrator, and last living keeper of the player's father's grand strategy. His role is not simply to list troop trees. He should help the player understand the war, challenge reckless choices, prepare for the Legion, and carry the emotional memory of the homeland.

## Working Name

- [x] Rename `Strategy Advisor` in-game to **Cassian Varro**.
- [x] Keep his court title visible in dialogue as **Cassian Varro, Strategy Advisor** where useful.
- [x] Use `trp_sod_strategy_advisor` as the internal troop id for compatibility unless a later full refactor is chosen.
- [x] Add a short lore note explaining that many soldiers still call him "the Strategy Advisor" because his real name was hidden during his years as an Imperial spy.

## Character Core

Cassian Varro was once one of the player's father's most trusted agents. He entered the Imperial Expeditionary Force under false loyalty, learned their doctrine from inside, and survived the fall of the homeland at terrible personal cost. He is no longer young enough to be a reliable battlefield companion forever, but he is not merely frail. He is dangerous, proud, damaged, and loyal in a way that can become suffocating.

His core tension:

- He believes the player must become strong enough to defeat the Legion.
- He fears the player may become too much like the Legion to win.
- He reveres the player's father but should eventually admit that the father's strategy also failed people.
- He wants to guide the player, but the player must outgrow him.

## Personality Targets

- [x] Mentor first, court officer second.
- [x] Speaks like a veteran who has seen both glory and bureaucracy rot from inside.
- [x] Uses military clarity, but allows warmth when speaking about the player's family.
- [x] Gives hard counsel without becoming a scolding tutorial voice.
- [x] Shows guilt over the homeland and disgust toward Imperial doctrine.
- [x] Has blind spots: overvalues discipline, underestimates local Calradian loyalties, and can justify ruthless preparation.
- [ ] Softens if the player builds alliances, protects civilians, and prepares intelligently.
- [ ] Hardens if the player relies on terror, slavery, executions, or needless raids.

## Current System Audit

- [x] Exists as `trp_sod_strategy_advisor`.
- [x] Starts in the player's party.
- [x] Is initialized with homeland-specific equipment.
- [x] Can be talked to from camp while in the party.
- [x] Can move to court after the player becomes an independent landholder.
- [x] Appears in court when `$g_sod_sa_in_court = 1`.
- [x] Provides troop/faction overview dialogue.
- [x] Provides Imperial invasion timing dialogue.
- [x] Provides Imperial spy backstory dialogue.
- [x] Can open the troop tree presentation.
- [x] Has random advice strings through `script_get_random_string_for_troop`.
- [x] Is wage-special-cased.
- [x] Has a real personal name in-game.
- [x] Has polished mentor dialogue.
- [x] Has approval/trust/memory state.
- [x] Has a personal quest or mentor arc.
- [x] Reacts to major player choices.
- [ ] Has field scenes or direct incidents beyond report menus.
- [x] Has late-game reflections after the Legion arrives.
- [x] Has a clean, immersive transition from party companion to court advisor.

## Narrative Arc

### Stage 1: The Old Hand

Early game. Cassian travels with the player as a battlefield mentor and practical advisor.

- [x] Replace generic opening lines with named mentor greetings.
- [x] Add "You knew my father. Tell me what he expected of me."
- [x] Add "What should I worry about first in Calradia?"
- [x] Add early advice that points to caravans, allies, companions, villages, and roads without sounding like a help screen.
- [x] Add first signs of injury: coughing, fatigue, old wound pain, or failing eyesight.

### Stage 2: The Burden of Counsel

After the player takes land or becomes a ruler, Cassian should ask to serve from court.

- [x] Replace the old `sa_council` text with polished dialogue.
- [x] Make the transition happen through direct dialogue, not a blunt menu.
- [ ] Let the player accept warmly, accept pragmatically, or ask him to remain in the field for now.
- [x] If accepted, move him to court and give him court clothing.
- [ ] If delayed, he remains in party but fatigue warnings can recur.
- [x] Avoid punishing the player with a flat honor loss for asking him to stay.

### Stage 3: The Shadow of the Legion

Midgame. Cassian becomes the main interface for Imperial intelligence and invasion preparation.

- [x] Expand invasion timing dialogue into a "Legion War Room" conversation.
- [x] Add lines for invasion delay through alliances and counter-intelligence.
- [x] Add advice for preparing border garrisons, supply stores, diplomacy, and mini-faction contacts.
- [x] Add warnings if the player has few allies before the invasion.
- [x] Add praise if the player builds a coalition.
- [x] Add distress if the player copies Imperial terror methods.

### Stage 4: Mentor Challenged

Cassian should not be right about everything. The player should be able to challenge him.

- [x] Add dialogue where the player questions his loyalty after his years in the Legion.
- [x] Add dialogue where he admits to actions he regrets during infiltration.
- [x] Add dialogue where he defends the player's father, then later admits the father made mistakes.
- [ ] Add a mentor dispute if the player pursues mercy over ruthless preparation.
- [ ] Add a mentor dispute if the player pursues ruthless preparation over mercy.
- [ ] Let high-trust outcomes make him more balanced.
- [ ] Let low-trust outcomes make him colder and more utilitarian.

### Stage 5: The Last Lesson

Late game, once the Imperial Expeditionary Force is active.

- [x] Add a direct war-room reflection after the first major victory over the Legion.
- [x] Add a reflection after an Imperial Centurion dies.
- [x] Add a reflection if the player defeats the Legion with strong alliances.
- [x] Add a darker reflection if the player defeats the Legion through executions, slavery, and terror.
- [x] Add an ending-state line where Cassian says the player is no longer a student.

## Gameplay Role

Cassian should become the player's mentor and strategic intelligence hub, not a generic report menu.

- [x] Provide immersive access to invasion status.
- [x] Provide immersive access to diplomacy/coalition guidance.
- [x] Provide immersive access to troop doctrine and troop tree views.
- [ ] Provide hostile reputation and road-memory intelligence.
- [x] Provide contextual advice based on player kingdom status.
- [x] Provide a court "War Room" dialogue branch when in court.
- [x] Provide a field "Old Campaigner" dialogue branch while in party.

## Dialogue Surfaces

### Camp

- [x] Existing camp option appears while he is in the party.
- [x] Rename option to "Speak with Cassian Varro."
- [x] Add direct mentor greeting lines based on early/mid/late campaign.
- [x] Add direct questions about the player's father, the homeland, Calradia, companions, and the Legion.
- [x] Add context-aware advice based on invasion timer, player faction, allies, frontier logistics, and minor powers.
- [x] Add company morale-specific mentor advice.

### Court

- [x] Existing court spawning is controlled by `$g_sod_sa_in_court`.
- [x] Rename council option to "Speak with Cassian Varro, Strategy Advisor."
- [x] Add a War Room dialogue branch.
- [x] Add reports as spoken counsel rather than menu-like lists.
- [x] Add court-only lines about rulers, vassals, diplomacy, and frontier defense.

### Post-Battle

- [x] Existing post-land acquisition/siege continuation can trigger his retirement dialogue.
- [x] Add post-battle comments after major Imperial victories.
- [ ] Add post-battle comments after defeats or costly victories.
- [ ] Add comments when the player's troops break, mutiny, or suffer severe morale collapse.
- [ ] Add comments after commander duels if the player wins or loses.

### Presentations

- [x] He can route into troop tree presentation.
- [x] Polish the troop tree return flow so it feels like he is opening and closing a campaign ledger.
- [ ] Fix typo in `troop_trees_prsenatation` naming only if a later compatibility-safe refactor is done.

## Mentor Trust System

Use a compact trust layer instead of making him a normal romance/friendship companion.

Suggested slots:

- [x] `slot_troop_sod_mentor_trust`
- [x] `slot_troop_sod_mentor_arc_stage`
- [x] `slot_troop_sod_mentor_warning_state`
- [x] `slot_troop_sod_mentor_last_reaction_day`
- [x] `slot_troop_sod_mentor_legion_memory`

Trust bands:

- [x] Reverent: believes the player honors the father's best hopes.
- [x] Confident: trusts the player's command.
- [x] Watchful: loyal but concerned.
- [x] Strained: fears what the campaign is making of the player.
- [x] Bitter: serves the realm more than the player.

Trust should rise from:

- [x] Building alliances before the invasion.
- [x] Preparing fiefs and supply lines.
- [x] Defeating Imperial forces.
- [x] Showing mercy without losing discipline.
- [x] Protecting civilians and refugees.
- [x] Rejecting slavery and predatory systems.

Trust should fall from:

- [x] Repeated lord executions outside clear necessity.
- [x] Slave trading or alliance with Slaver power.
- [x] Needless village raids.
- [ ] Ignoring invasion preparation.
- [x] Betraying allies.
- [x] Paying tribute to predatory forces too often.
- [x] Letting the company collapse through unpaid wages or repeated preventable defeats.

## Personal Quest: The Last Order

Theme: loyalty, guilt, old orders, and whether strategy can become conscience.

### Opening

- [x] Unlock after the player holds land or after the invasion timer reaches a danger threshold.
- [x] Cassian asks to speak privately about the player's father.
- [x] He reveals he still carries one sealed order from the father, never opened because the homeland fell first.

### Middle Incident

- [x] A Legion courier, old spy cache, or captured Imperial officer reveals that Cassian's old network may still exist.
- [x] Player chooses whether to use the network for sabotage, rescue, diplomacy, or purge.
- [x] The incident should store a focus center, party, or cause.
- [x] Journal hint should name the place or actor.

### Choices

- [x] Use the network for ruthless counter-intelligence against the Legion.
- [x] Use the network to extract refugees, informants, or families left behind.
- [x] Publicly expose the network and risk losing its strategic value.
- [x] Burn the network to protect those who served in secret.

### Outcomes

- [x] Good/balanced outcome: Cassian gains trust, improves invasion-delay/counter-intelligence counsel, and softens.
- [x] Hard outcome: Cassian gains strategic effectiveness but becomes colder.
- [x] Mercy outcome: Cassian accepts that the father's last order was incomplete without conscience.
- [ ] Failure/rupture: Cassian remains in court but speaks more formally and with reduced trust.

### Rewards

- [x] Improved invasion intelligence clarity.
- [ ] Small bonus to invasion-delay operations if allies exist.
- [x] One-time Imperial supply sabotage discount or effectiveness boost.
- [x] Mentor ending reflection.

## Integration With Existing Systems

### Companion Depth

- [x] Decide whether Cassian is part of the normal companion approval framework or a special mentor framework.
- [ ] If normal framework is used, add him to companion report with a special "Mentor" label.
- [x] Add companion reactions to his mentor arc from Lezalit, Ymira, Bunduk, Marnid, and Borcha.
- [x] Add at least one triangle: Cassian / Lezalit / Ymira on discipline versus mercy.
- [x] Add at least one triangle: Cassian / Marnid / Borcha on logistics versus opportunism.

### Diplomacy

- [x] Add advice for making allies to delay the Legion.
- [x] Add commentary when a treaty is signed.
- [x] Add warnings when the player fights too many fronts.
- [x] Add special lines for the Imperial Expeditionary Force being outside normal diplomacy.

### Mini-Factions

- [x] Add counsel for each mini-faction's strategic value.
- [x] Slavers: warns that profit from coercion echoes Imperial logic.
- [x] Jotnar: recognizes kin survival as useful but not easily commanded.
- [x] Elephant Guard: respects sanctuary and anti-slaver pressure.
- [x] Black Khergits: treats them as mobile strategic infection.
- [x] Boar Clan: warns about road moralists becoming toll tyrants.
- [x] Serpent Host: values intelligence and route watching.
- [x] Black Army: values discipline but distrusts mercenary loyalty.

### Company Accounts And Morale

- [x] Add advice if unpaid wages strain the company.
- [x] Add comments if noble troops grow restless.
- [x] Add comments if the player uses threats instead of pay.
- [x] Add praise for disciplined, well-supplied campaigns.

### Center Health

- [x] Add strategic counsel about villages as economic roots.
- [x] Add warnings when castles lack support.
- [x] Add advice when towns are starving, diseased, or overtaxed.

## Text Polish Targets

- [x] Replace "Yor Strategy Advisor" typo.
- [x] Replace "premission" typo.
- [x] Replace "faithfuly" typo.
- [x] Rewrite old "cup and bed... ale or woman" line.
- [x] Standardize capitalization of "my lord" unless title-specific.
- [x] Update old faction descriptions to match current mini-faction designs.
- [x] Replace blunt tutorial phrasing with in-world counsel.
- [x] Reduce walls of text into shorter, branching dialogue beats.
- [x] Preserve a few old lines as flavor where they still fit.

## Implementation Milestones

### Milestone 1: Name And Surface Polish

- [x] Rename display name to Cassian Varro.
- [x] Update camp option text.
- [x] Update council option text.
- [x] Update random advice strings to use his voice.
- [x] Rewrite the court-transition scene.
- [x] Add static test for name, camp option, court option, and transition text.
- [x] Run `py build\doctor.py --doctor-new-only`.
- [x] Run `cmd /c build_module.bat --no-cache`.

### Milestone 2: Mentor Dialogue Expansion

- [x] Add early mentor questions.
- [x] Add father/homeland dialogue.
- [x] Add Calradia survival dialogue.
- [x] Add invasion preparation dialogue.
- [x] Add court War Room branch.
- [x] Add static dialogue graph coverage.
- [x] Run focused dialogue safety tests.

### Milestone 3: Mentor Trust

- [x] Add mentor trust slots/constants.
- [x] Initialize mentor trust.
- [x] Add action hook script.
- [x] Hook diplomacy, slavery, invasion, morale, and fief-health actions.
- [x] Add report/War Room trust-band language.
- [x] Add tests for hooks and trust bands.

### Milestone 4: The Last Order Quest

- [x] Add quest metadata.
- [x] Add runtime accept/update/complete/fail calls.
- [x] Add journal entries.
- [x] Add memory events.
- [x] Add focus center/party/cause storage.
- [x] Add direct dialogue incident.
- [x] Add outcome consequences.
- [x] Add tests for quest framework integration.

### Milestone 5: Late Game Reflections

- [x] Add first Imperial victory reflection.
- [x] Add Centurion death reflection.
- [x] Add alliance victory reflection.
- [x] Add ruthless victory reflection.
- [x] Add final mentor closure line.
- [x] Add tests for trigger gates.

## Static Test Checklist

- [x] Strategy Advisor display name is Cassian Varro.
- [x] Camp option says Cassian Varro.
- [x] Court option says Cassian Varro.
- [x] `$g_sod_sa_in_court` transition remains safe.
- [x] No post-dialogue close-window branch strands the player.
- [x] Troop tree presentation return still works.
- [x] Mentor trust constants exist.
- [x] Mentor action hook exists.
- [x] The Last Order quest exists in quest framework.
- [x] The Last Order journal text exists.
- [x] Legion, diplomacy, slavery, company morale, and fief-health systems call mentor hooks.
- [ ] Manual QA rows remain unchecked until played.

## Manual QA Checklist

- [ ] New game: Cassian starts in party with correct name and gear.
- [ ] Camp: Cassian conversation opens and exits safely.
- [ ] Troop tree: Cassian opens and returns from presentation safely.
- [ ] Player takes first fief: mentor transition triggers at the right time.
- [ ] Accept court role: Cassian leaves party and appears in court.
- [ ] Delay court role: Cassian remains in party and can be asked again later.
- [ ] Court: War Room conversation opens and exits safely.
- [ ] Invasion not started: Cassian gives useful preparation counsel.
- [ ] Invasion active: Cassian changes tone and gives war counsel.
- [ ] Slavery/mercy choices affect mentor trust.
- [ ] Alliance-building affects mentor trust.
- [ ] Last Order quest can complete with multiple outcomes.
