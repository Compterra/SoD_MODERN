# The Seven Oaths of Ash

> Status: **target-state campaign design**.  
> Source inspiration: `EVENT_CHAIN_SEVEN_SAMURAI.md`, adapted into a medieval, non-fantasy campaign suitable for grounded Mount & Blade-style implementation.

## Overview

- **Campaign ID:** `campaign_seven_oaths_of_ash`
- **Type:** long side campaign / settlement defense epic
- **Length:** long
- **Primary player promise:** a threatened settlement cannot buy safety, cannot trust distant lords, and must assemble a small company of hard, flawed defenders before a professional raider host arrives.
- **Primary antagonist pressure:** Wulfred Carr, called the Ash Captain, a former retinue commander who has turned broken soldiers, deserters, and road brigands into a moving war-band.
- **Primary implementation shape:** a timed campaign chain with recruitment chapters, settlement preparation, pressure interludes, a multi-phase siege, survivor aftermath, and durable ending flags.
- **Tone:** desperate, grounded, human, medieval, no supernatural rescue and no clean victory without cost.
- **Campaign promise:** seven sword-trained defenders cannot defeat an army by being legends; they can make a village think, build, drill, scout, endure, and choose where the blood is spent.

The original stub is a high-drama fantasy event about recruiting seven extraordinary figures to defend a settlement against an overwhelming bandit host. This version keeps the emotional engine but removes fantasy species, demons, curses, undeath, magic, and cosmic bargains. Every solution is made of real medieval materials: walls, ditches, grain, horses, law, reputation, paid service, oaths, fieldcraft, siegecraft, and the terrible arithmetic of defending civilians.

The campaign should feel like an authored war story rather than a menu of buffs. The player should travel, meet people, hear testimony, choose bargains, spend resources, return with consequences, and then watch those choices matter during the siege.

## Design Pillars

1. **The village is a character**  
   The threatened settlement must have named spaces, visible needs, frightened factions, and a memory of what the player asked from it.

2. **Every defender is useful and difficult**  
   The seven are not superhuman. Each solves one real military problem while creating one real social, political, or moral problem.

3. **Preparation is gameplay**  
   The campaign is not won only by the final battle. The player wins or loses through scouting, engineering, food storage, training, discipline, evacuation, intelligence, and morale.

4. **The clock should be felt through people**  
   Do not show only "75 days remain." Show abandoned farms, bad bread, missing livestock, knife-marked doors, exhausted ditch crews, and children practicing with spears too long for them.

5. **No perfect seven**  
   Recruiting everyone is possible but expensive. Some combinations create stronger tactics; some create conflict. The best victory is not "all bonuses stacked" but "the village survives with a method the player can live with."

6. **The raiders are organized**  
   Wulfred's host should not behave like random looters. They scout, pressure, threaten, burn outlying farms, bribe gates, seize hostages, probe roads, and punish indecision.

7. **The ending remembers method**  
   A settlement saved by law feels different from one saved by terror. A settlement saved by sacrifice feels different from one saved by clever preparation.

8. **Roleplay lives in dialogue**  
   Menus and quest logs should frame the adventure, mark travel, summarize outcomes, and carry narrative beats. The player's meaningful roleplaying decisions should usually happen through dialogue with named characters inside scenes, so the campaign feels like an immersive journey rather than a choice book.

## Non-Fantasy Adaptation Rules

The campaign should preserve the "seven defenders against an army" structure while converting every fantasy element into grounded medieval equivalents.

| Stub Element | Medieval Non-Fantasy Replacement |
| --- | --- |
| Elven master archer | Disgraced longbow captain or veteran forester |
| Dwarven explosives savant | Siege engineer, miner, ditchwright, or powderless sapper |
| Death knight | Landless knight bound by oath, debt, or shame |
| Circus blade-dancer assassin | Former camp performer, tavern duelist, smuggler, or knife instructor |
| Demon tempter | Spymaster, outlaw lawyer, banker, or ruthless quartermaster |
| Berserker | Shock infantryman, outlaw champion, or battle-scarred axeman |
| Fanatical ghosts | Survivors, refugees, widows' militia, or chapel order |
| Magic wards | Morale, fieldworks, sanctuary, legal oath, church bell, locked granary |
| Curses/bindings | Hostages, debts, contracts, blackmail, public oaths, legal surety |
| Undead survival | Injury, retreat, prisoner exchange, reputation damage |

No route should require supernatural causality. Luck, fear, reputation, and faith can matter, but they must operate socially and materially.

## Campaign Premise

The village of **Ashwick** sits at a crossroads between grain country, a ferry road, and the edge of a neglected lordship. It has walls only in the generous sense: a ditch, a half-rotten palisade, a churchyard with a stone wall, and two old watch platforms that creak in wind.

Wulfred Carr's host has already destroyed three settlements:

- **Briar Ford** paid and was burned after the host took its cattle.
- **Little Harrow** refused and was made an example.
- **Saint Ormond's Grange** tried to run; its refugees now crowd roads and ditches.

Wulfred sends riders to Ashwick with a demand: **5,000 denars, five hundred sacks of grain, and twelve "surety children" within one hundred days**. If the settlement pays, Wulfred promises protection. Everyone knows what that means. If the settlement refuses, he will return with his host.

The player can:

- prepare Ashwick alone
- recruit outside defenders
- bargain with Wulfred
- evacuate
- attempt assassination or sabotage
- combine recruitment and preparation

The heroic path is not a clean good path. It spends time, coin, trust, labor, and political capital. It asks strangers to risk dying for people they do not know.

## Core Campaign State

Recommended state fields for later implementation:

```md
- campaign_id = campaign_seven_oaths_of_ash
- campaign_status = inactive | active | suspended | completed | failed | archived
- active_stage = ultimatum | audit | recruitment | return | siege | aftermath
- active_recruit_id
- act2_recruitment_board_open
- act2_recruitment_resolved_count
- act2_recruitment_complete
- act3_pressure_started
- days_remaining
- player_field_strength_at_ultimatum
- player_field_strength_at_siege
- wulfred_host_strength
- wulfred_elite_core_strength
- wulfred_pressure
- settlement_strain
- ashwick_morale
- ashwick_food
- ashwick_labor
- ashwick_fortification
- ashwick_militia_training
- ashwick_civilian_safety
- ashwick_elder_trust
- ashwick_youth_trust
- ashwick_farmer_trust
- ashwick_refugee_trust
- noble_notice
- church_notice
- merchant_notice
- outlaw_notice
- recruited_defenders_bitmask
- defender_survival_bitmask
- defender_bond_flags
- defender_conflict_flags
- defender_companion_unlock_bitmask
- defender_companion_refusal_bitmask
- final_siege_plan
- final_siege_result
- ending_flag
```

### Major Campaign Flags

- `seven_ash_ultimatum_received`
- `seven_ash_recruitment_chosen`
- `seven_ash_fortify_alone_chosen`
- `seven_ash_bargain_attempted`
- `seven_ash_evacuation_started`
- `seven_ash_wulfred_scouts_identified`
- `seven_ash_outer_farms_burned`
- `seven_ash_hostages_taken`
- `seven_ash_granary_secured`
- `seven_ash_ditch_line_completed`
- `seven_ash_palisade_repaired`
- `seven_ash_refugee_quarter_established`
- `seven_ash_militia_mustered`
- `seven_ash_civilian_evacuation_ready`
- `seven_ash_wulfred_killed`
- `seven_ash_wulfred_escaped`
- `seven_ash_settlement_survived`
- `seven_ash_settlement_fell`

### Defender Recruitment Flags

- `recruited_garric_ashbow`
- `recruited_oswin_ditchwright`
- `recruited_sir_aldrik_vane`
- `recruited_mirelle_voss`
- `recruited_tomas_reed`
- `recruited_beren_hardhand`
- `recruited_sister_elianor`

### Defender Outcome Flags

- `garric_survived`
- `oswin_survived`
- `aldrik_survived`
- `mirelle_survived`
- `tomas_survived`
- `beren_survived`
- `elianor_survived`
- `defender_betrayal_occurred`
- `defender_departed_before_siege`
- `defender_became_permanent`
- `defender_left_in_anger`
- `defender_memorialized`

### Defender Companion Unlock Flags

- `garric_companion_unlocked`
- `oswin_companion_unlocked`
- `aldrik_companion_unlocked`
- `mirelle_companion_unlocked`
- `tomas_companion_unlocked`
- `beren_companion_unlocked`
- `elianor_companion_unlocked`
- `defender_companion_offer_pending`
- `defender_companion_joined_player_party`
- `defender_companion_stayed_in_ashwick`
- `defender_companion_refused_player`

### Moral Method Flags

- `method_public_oaths`
- `method_paid_contracts`
- `method_blackmail`
- `method_hostage_surety`
- `method_common_defense`
- `method_scorched_fields`
- `method_civilian_first`
- `method_enemy_no_quarter`
- `method_prisoners_spared`
- `method_wulfred_bargained`
- `method_wulfred_assassinated`

## Campaign Systems

### Dialogue-First Interaction Model

The campaign should treat menus and quest logs as scaffolding, not the main roleplaying surface.

Use menus for:

- entering or leaving a campaign beat
- choosing a travel destination
- opening the Act II recruitment board
- selecting a broad preparation project after characters have argued over it
- confirming irreversible transitions such as ending recruitment, beginning the siege, or abandoning Ashwick
- summarizing logistical results that would be tedious to stage physically

Use quest logs for:

- reminding the player where to go next
- preserving testimony and promises
- recording who was recruited, refused, alienated, lost, or abandoned
- stating the current strategic pressure in plain language
- summarizing consequences after a scene has already played

Use dialogue and mission scenes for:

- moral choices
- recruitment persuasion
- threats, bargains, and promises
- witness testimony
- defender conflicts
- village arguments
- decisions that affect trust, fear, pride, debt, or method flags
- moments where a named character should remember what the player said

Design rule: if a choice changes a relationship, moral method, defender loyalty, village trust, or future betrayal risk, it should normally be a dialogue choice with a named character. Menus may confirm the outcome afterward, but should not replace the conversation.

Recommended pattern:

1. **Menu/log gives context:** "Travel to the Split Hart to find Garric Ashbow."
2. **Scene establishes pressure:** Garric is insulted by locals; the widow Eda watches from the hearth.
3. **Dialogue carries the choice:** the player believes Eda, pays Garric, shames him, threatens him, or leaves him.
4. **Quest log records result:** "Garric agreed to train Ashwick's bowmen after you publicly accepted Eda Flint's testimony."
5. **Menu returns control:** travel onward, return later, or choose another lead.

Avoid menu-only moral pivots such as:

- "Recruit him honorably."
- "Blackmail him."
- "Leave."

Instead, write the conversation that makes those options feel like actions:

- "Eda says you held the roof after the lord ran. I believe her."
- "Seven hundred now, three hundred when Ashwick still stands."
- "That old charge can die with my help, or live loudly without it."
- "No. Ashwick needs a steadier man."

### Days Remaining

The primary clock begins at `100` and falls as the player travels, recruits, trains, prepares, or hesitates.

Recommended costs:

- local audit: 2 days
- recruit lead found: 3 days
- recruitment travel: 4-8 days
- recruit negotiation: 1-3 days
- return with recruit: 3-6 days
- fieldwork project: 5-15 days
- scouting operation: 3-7 days
- pressure interlude ignored: 0 days but increases `wulfred_pressure`
- pressure interlude answered: 2-6 days but reduces pressure or strain

Design rule: the clock should rarely hard-fail before the siege. Instead, it should change siege starting conditions.

If Act II is open-ended, `days_remaining` should still tick down during travel and recruitment, but the campaign should not interrupt recruitment with full Act III pressure scenes. Use brief road reports, rumors, and Ashwick letters to show that time is passing.

If `days_remaining <= 0` during Act II, do not instantly launch the final siege in the middle of a recruitment scene. Instead, set `seven_ash_wulfred_arrived_while_away`, force the next return to Ashwick, and begin Act III in emergency mode.

If `days_remaining <= 20`, some slow recruitment options should be unavailable or costly.

If `days_remaining <= 10`, pressure interludes become direct attacks.

### Act Pacing Model

Preferred structure:

1. **Act I is fixed and local.** The ultimatum and village audit establish Ashwick's needs.
2. **Act II is open-ended.** The player can pursue the seven defender roads in any order.
3. **Act III begins only after Act II is complete.** The village pressure phase should not fully begin until the recruitment board is resolved and the player returns to Ashwick.
4. **Act IV is the strategic lock-in.** The oath council happens after Act III has made the cost of preparation visible.

This pacing keeps recruitment from feeling like a rigid checklist while preserving the authored escalation of the village campaign.

Act II completion means every defender road has reached one of these terminal states:

- recruited
- refused
- alienated
- unavailable because the player chose a hard time-saving route
- dead or captured through a failed recruitment scene
- intentionally abandoned through a formal "end recruitment and return to Ashwick" choice

The player does not need to recruit all seven to proceed, but the player must resolve all seven recruitment opportunities or deliberately close the remaining ones. If the design goal for a particular implementation is "true seven only," require all seven recruited before Act III. The broader campaign design should support both modes.

Recommended menu behavior:

- Act II opens `mnu_seven_ash_recruitment_map`.
- Completed defender roads are marked with their outcome.
- Unvisited roads remain available while `days_remaining > 20`.
- Slow or honorable recruitment methods become harder as time falls.
- At any time after at least three defender roads are resolved, the player may choose `Return to Ashwick and end the search.`
- Choosing to end the search sets `act2_recruitment_complete = true`, marks unresolved roads as abandoned, and starts Act III on return.

Recommended pacing pressure during Act II:

- Use short courier reports instead of full interludes.
- Letters from Ashwick should mention fear, food, burned farms, or rumors, but should not demand a large local decision until Act III.
- Wulfred pressure can increase invisibly or lightly, then cash out in Act III.
- The longer Act II takes, the harder Act III opens.
- Recruiting a defender can reduce a specific future Act III problem, but should not skip Act III entirely.

### Wulfred Pressure

`wulfred_pressure` ranges from `0` to `100`.

Pressure increases when:

- the player ignores scouts
- recruitment takes too long
- Ashwick appears divided
- the player publicly refuses Wulfred without preparation
- a recruit is acquired through dishonorable means and rumor spreads
- food or morale collapses
- a pressure interlude is failed

Pressure decreases when:

- scouts are intercepted
- roads are watched
- outlying farms are evacuated
- Wulfred's quartermasters are disrupted
- Ashwick's militia visibly drills
- a defender creates credible deterrence

Breakpoints:

- `25`: Wulfred tests roads and steals livestock.
- `50`: informants, threats, and hostage pressure begin.
- `75`: arson attempts, panic, and deserter offers begin.
- `100`: Wulfred attacks early or begins with siege advantages.

### Player Army and Host Scaling

The campaign must account for the player arriving with a real army. In many SoD games, even an early player can field 50-85 troops, so Wulfred cannot be balanced as a small bandit party. He is a former retinue commander who scouts before committing. If the player brings strength, Wulfred answers with numbers, pressure, timing, and divided objectives.

Design goals:

- a large player army should matter and feel powerful
- a large player army should not skip the campaign's village-defense drama
- scaling should be readable in fiction, not invisible punishment
- Wulfred should adapt through scouts, extra hired blades, forced levies, and allied road brigands
- the final battle should be fought in sectors and waves, not as one simple party-vs-party collision

Recommended strength model:

```md
player_field_strength_at_ultimatum = player party combatants + notable companion/elite weighting
player_field_strength_at_siege = current player party combatants + committed allied troops

base_wulfred_fighters = 140
scaled_wulfred_fighters = base_wulfred_fighters + (player_field_strength_at_siege * 2)
wulfred_host_strength = clamp(scaled_wulfred_fighters, 180, 420)
wulfred_elite_core_strength = clamp(35 + player_field_strength_at_siege / 3, 45, 90)
```

This means:

- weak or solo player: Wulfred still brings about 180 fighters
- player with 50 troops: Wulfred brings about 240 fighters
- player with 85 troops: Wulfred brings about 310 fighters
- late or unusually strong player: Wulfred can reach 350-420 fighters, but should not grow forever

Do not present this as raw rubber-banding. The world should explain it:

- scouts report the player's banners and troop count
- Wulfred delays to gather more deserters
- Maud buys grain and hires extra shieldmen
- Rafe pressures nearby outlaws into joining
- Sibert maps routes that split the player's strength

If the player fields an overwhelming army, unlock an acknowledgement route instead of pretending Ashwick is still helpless:

- Wulfred may avoid open battle and attack farms, wells, hostages, and roads
- the player can force an early negotiation or pursuit
- Ashwick may survive militarily but still suffer if civilians, stores, and fires were neglected
- the "easy military win" should become a question of whether the village was saved cleanly, not whether the player can defeat brigands in a field

### Army Commitment and Sector Pressure

The player's troops should be useful, but they cannot all stand everywhere at once.

Before the siege, ask the player to commit forces to sectors:

- outer fields and farm roads
- palisade and ditch
- gate reserve
- inner streets and fire watch
- churchyard and infirmary guard
- civilian evacuation escort

The seven defenders improve sector performance, but player troops provide bodies. A strong army gives better coverage, more recoverable mistakes, and stronger counterattacks. A weak army makes defender expertise and village preparation more decisive.

Suggested commitment rules:

- each sector has a recommended troop allocation
- under-allocated sectors generate more casualties, fires, or breaches
- over-allocated sectors are safer but leave other sectors exposed
- cavalry performs well in outer fields and pursuit, poorly in tight streets
- archers need Garric, sightlines, or prepared platforms to outperform basic militia
- elite infantry can hold breaches, but without Tomas or Aldrik they may be drawn out of position
- companions and named defenders should be assignable as sector leaders

This keeps large armies meaningful while preserving the campaign fantasy: the player is not just winning a battle; they are commanding a threatened settlement through a coordinated defense.

### Settlement Strain

`settlement_strain` measures what preparation costs the people.

It rises when:

- labor is pulled from fields
- food is stockpiled harshly
- refugees are admitted without supplies
- families are separated for evacuation
- recruits demand payment or privileges
- the player imposes martial law
- outlying farms are burned intentionally

It falls when:

- supplies are fairly distributed
- the church or elders endorse the plan
- militia training feels competent
- the player pays wages
- refugees are given work and shelter
- civilians see visible progress

Breakpoints:

- `25`: grumbling, hoarding, reluctance to drill.
- `50`: families hide food, labor slows, rumor spreads.
- `75`: desertion attempts and elder opposition.
- `100`: internal collapse before or during siege.

### Ashwick Readiness Scores

The defense should be computed from several readable categories rather than one abstract "defense value."

- `ashwick_fortification`: ditch, palisade, barricades, gate, churchyard wall.
- `ashwick_militia_training`: spear line, bow practice, night watch, alarm discipline.
- `ashwick_food`: grain, salted meat, water, livestock, fair ration plan.
- `ashwick_morale`: trust in plan, trust in player, fear level, visible leadership.
- `ashwick_intelligence`: scout reports, mapped approaches, Wulfred's lieutenants known.
- `ashwick_civilian_safety`: evacuation routes, cellar shelters, infirmary, fire breaks.

The final siege should read these categories by phase.

### Recruit Bonds

Each defender tracks:

- `trust`: believes the player means what they say
- `debt`: owes the player, or believes payment/contract binds them
- `pride`: wants public recognition or personal proof
- `fear`: fears exposure, failure, legal punishment, or betrayal
- `village_bond`: grows attached to Ashwick's people

Recruitment methods modify these values.

Examples:

- paying a defender raises `debt`, not necessarily `trust`
- public oath raises `trust` and `pride`
- blackmail raises `fear` and betrayal risk
- shared danger raises `trust` and `village_bond`
- giving command responsibility raises `pride`
- using a defender as disposable raises `fear` and lowers `trust`

### Defender Conflicts

Defenders should not be collectible bonuses without friction.

Potential conflicts:

- Garric dislikes needless heroics and distrusts Beren.
- Oswin objects if civilians are housed too near powder, pitch, or unstable works.
- Sir Aldrik resents Mirelle's underworld methods.
- Mirelle mocks public honor and warns against predictable plans.
- Tomas Reed fights with Beren over discipline versus fury.
- Beren despises retreat plans unless framed as protecting civilians.
- Sister Elianor refuses no-quarter orders if prisoners or children are involved.

Conflicts should create interludes, not instant failure.

### Combined Defense Tactics

Pairings unlock siege options if both recruits are present and not alienated.

| Pairing | Tactic | Requirement | Effect |
| --- | --- | --- | --- |
| Garric + Mirelle | Silent Mark | high intelligence | enemy lieutenant can be ambushed before gate phase |
| Garric + Tomas | Killing Lanes | training + palisade | militia archers fire safely during outer field phase |
| Oswin + Tomas | Ditch Discipline | ditch + trained spear line | first cavalry or foot rush loses momentum |
| Oswin + Mirelle | False Gate | underworld tricks + fieldworks | raiders are lured into a dead-end street |
| Aldrik + Elianor | Bell Oath | church endorsement | morale break chance reduced |
| Aldrik + Beren | Shielded Breach | mutual respect | breach phase becomes recoverable instead of catastrophic |
| Tomas + Beren | Hammer and Anvil | drilled militia + shock reserve | counterattack can be controlled rather than reckless |
| Mirelle + Elianor | Hidden Evacuation | refugee trust | civilians can be moved during street fighting |

## Core Cast

### Wulfred Carr, the Ash Captain

- **Role:** antagonist
- **Background:** former company captain in a lord's retinue, dismissed after ransom fraud and unauthorized foraging turned into massacre.
- **Current power:** commands deserters, broken men-at-arms, poachers, dispossessed tenants, highway thieves, and camp followers who know how armies feed.
- **Public image:** warlord, extortionist, breaker of villages.
- **Private truth:** not chaotic. He is a logistician of fear.
- **Method:** offer terms, make examples, take hostages, recruit the desperate, burn selectively, always leave a witness.
- **Weakness:** pride in being seen as inevitable. If forced to react instead of dictate, his host becomes less disciplined.

Wulfred should speak like a man who has watched lawful armies commit the same crimes under banners. He uses that hypocrisy to recruit and justify himself.

Sample voice:

> "Your lord calls it levy, I call it taking. Your church calls it tithe, I call it taking. Your sheriff calls it fine, I call it taking. I am merely honest enough to arrive with fire."

### Mother Hilda of Ashwick

- **Role:** village moral center and civilian witness
- **Surface:** church elder, keeper of births, deaths, and winter stores
- **Function:** interprets morale, refugee pressure, burial costs, civilian fear
- **Conflict:** she wants survival but refuses methods that make survival meaningless

### Reeve Martin Hobb

- **Role:** village civil authority
- **Surface:** practical, frightened, stubborn
- **Function:** tracks labor, food, taxable goods, elder trust
- **Conflict:** will oppose plans that ruin harvest or invite noble retaliation

### Piers Wainwright

- **Role:** wagoner and road witness
- **Surface:** knows every ditch, ford, and farm track around Ashwick
- **Function:** scouting, evacuation, road pressure, Wulfred's supply lines
- **Conflict:** wants to save his own family first, not become a hero

### Nell of Little Harrow

- **Role:** refugee witness
- **Surface:** survivor from a settlement Wulfred destroyed
- **Function:** tells the player how Wulfred actually attacks
- **Conflict:** pushes for evacuation, distrusts heroic defense, knows what happens when promises fail

## Sword Training Standard

All seven defenders should be trained with a sword. This is a shared credibility baseline, not their whole identity.

Each recruit should be able to stand in a melee scene without feeling like a helpless specialist:

- every defender has a two-handed sword or hand-and-a-half sword sidearm
- every defender can plausibly join a street fight, alley ambush, breach defense, or final churchyard stand
- every defender should have sword-related camp dialogue, drill dialogue, or scene blocking at least once
- sword training should not erase role contrast; Garric is still an archer, Oswin is still an engineer, Elianor is still a healer, and so on
- no defender should be balanced as useless without their specialty weapon

Recommended combat hierarchy:

- **Elite sword fighters:** Sir Aldrik Vane, Mirelle Voss
- **Dangerous melee fighters:** Beren Hardhand, Tomas Reed
- **Competent sidearm fighters:** Garric Ashbow, Oswin Ditchwright, Sister Elianor Grey

Implementation rule: all seven defender troops should spawn with a two-handed sword sidearm in combat scenes unless a specific disguise, captivity, or cinematic beat intentionally removes weapons. Their primary equipment can still express their role: Garric carries a bow, Oswin carries tools or a shield, Aldrik carries knightly arms, Mirelle carries knife and sword, Tomas carries drill-sergeant infantry gear, Beren carries axe and sword, and Elianor carries a plain serviceable blade suitable for last-line defense.

## The Seven Defenders

The seven defenders should be recruitable in a flexible order after the first lead, but the initial design presents them as a structured chain for implementation simplicity.

### Garric Ashbow

- **Campaign role:** archer captain and scout of killing lanes
- **Troop concept:** veteran longbowman / disgraced forester / sword-trained archer
- **Found at:** The Split Hart tavern near a hunting forest
- **Military value:** ranged discipline, enemy officer targeting, watch posts, scout signs, sidearm discipline when archers are pressed
- **Social cost:** bitter, fatalistic, unnerves young militia
- **Core wound:** he survived a battle where his lord ordered archers to abandon infantry, then blamed Garric for the rout
- **Best recruitment:** give him command over bow training and promise no false charges
- **Hard recruitment:** pay him as a mercenary and accept his contempt
- **Ruthless recruitment:** threaten him with old charges or turn him over to the lord who wants a scapegoat
- **Village bond scene:** he teaches children to cut bowstrings before surrendering them, then shows older militia how to keep a short sword low when an enemy closes under the bow line

### Oswin Ditchwright

- **Campaign role:** engineer, miner, ditch planner, barricade designer
- **Troop concept:** siege carpenter / former castle sapper / sword-trained engineer
- **Found at:** a quarry camp after a bridge collapse dispute
- **Military value:** ditch lines, barricades, gate braces, fire breaks, traps that use stakes, pits, carts, and grease, defensive sword work around fieldworks
- **Social cost:** demands labor, timber, nails, and obedience to unglamorous work
- **Core wound:** his warning about a castle wall was ignored; the wall fell and he was blamed for cowardice
- **Best recruitment:** inspect his old plans and publicly vindicate his competence
- **Hard recruitment:** hire him with coin and give him authority over labor
- **Ruthless recruitment:** use his debt to a quarry master to force service
- **Village bond scene:** he marks door lintels for fire breaks and has to tell families which homes may be sacrificed, his old sword knocking against his carpenter's rule as a reminder that plans fail into hand-to-hand work

### Sir Aldrik Vane

- **Campaign role:** knight, public oath, mounted reserve, discipline symbol
- **Troop concept:** landless sword-and-shield knight with damaged reputation
- **Found at:** a small chapel court where he is acting as unpaid guard
- **Military value:** cavalry discipline, shielded breach response, noble legitimacy, formal sword drill
- **Social cost:** expects deference, angers commoners if given too much authority
- **Core wound:** he yielded a bridge to save hostages and was branded a coward by men who were not there
- **Best recruitment:** hear the hostage witness and let him swear a new oath publicly
- **Hard recruitment:** hire him through legal contract
- **Ruthless recruitment:** promise to erase or exploit the cowardice charge
- **Village bond scene:** he kneels to receive a spear from Ashwick's oldest widow, then lays his sword across both palms and swears it will answer to Ashwick before any lord

### Mirelle Voss

- **Campaign role:** knife instructor, infiltrator, counter-spy, street defense planner
- **Troop concept:** sword-and-knife duelist / former camp performer / smuggler contact
- **Found at:** a riverside tavern that serves deserters and boatmen
- **Military value:** hidden routes, informants, night raids, bandit spy detection, close-quarters sword work
- **Social cost:** criminal contacts, mistrust from church and knightly recruits
- **Core wound:** she survived by informing once and hates that it worked
- **Best recruitment:** give her honest terms and authority over evacuation routes
- **Hard recruitment:** buy her network
- **Ruthless recruitment:** threaten exposure to a magistrate
- **Village bond scene:** she teaches washerwomen where to hide knives and when not to use them, then teaches the lane watch how to use a short sword without overcommitting in a doorway

### Tomas Reed

- **Campaign role:** drillmaster, old sergeant, ration-line disciplinarian
- **Troop concept:** sword-trained retired infantry sergeant
- **Found at:** a roadside veterans' almshouse
- **Military value:** militia training, watch rotations, panic control, spear wall, sword-and-buckler recovery drill
- **Social cost:** harsh discipline, public punishment, risk of breaking morale if unchecked
- **Core wound:** he once kept a levy alive by flogging deserters and is not sure whether that made him savior or butcher
- **Best recruitment:** define strict limits and make him answer to village witnesses
- **Hard recruitment:** give him command and accept fear as the price of order
- **Ruthless recruitment:** let him use terror freely for quick training
- **Village bond scene:** he returns a boy's wooden practice spear and tells him courage is standing where he is placed, not dying where he is not needed; afterward he drills the adults on drawing swords only after the spear line breaks

### Beren Hardhand

- **Campaign role:** shock fighter, breach holder, morale challenge
- **Troop concept:** sword-trained outlaw champion / miller's son turned axeman
- **Found at:** a fighting pit or outlaw camp
- **Military value:** countercharge, breach defense, champion duel, intimidation, brutal sword work when the axe is fouled
- **Social cost:** violent temper, poor obedience, frightens civilians
- **Core wound:** lawful men hanged his brothers as thieves after a famine dispute; he became what they named him
- **Best recruitment:** beat or withstand him in a controlled contest and offer a lawful enemy
- **Hard recruitment:** offer spoils and a place in the breach
- **Ruthless recruitment:** point him at Wulfred and ignore collateral damage
- **Village bond scene:** a frightened girl asks if he will burn her house; he has no answer until the player gives him one, and later he lets the mill boys lift his heavy sword so they understand weight before glory

### Sister Elianor Grey

- **Campaign role:** healer, refugee organizer, sanctuary keeper, conscience
- **Troop concept:** sword-trained battlefield sister / convent nurse / organizer of survivors
- **Found at:** a burned grange turned refugee camp
- **Military value:** infirmary, civilian evacuation, morale, wounded recovery, post-battle legitimacy, last-line defensive sword work
- **Social cost:** demands food and shelter for refugees, opposes no-quarter cruelty
- **Core wound:** she watched a village pay Wulfred and still burn; she refuses empty mercy
- **Best recruitment:** commit to a real sanctuary and ration plan
- **Hard recruitment:** accept her people but limit her authority
- **Ruthless recruitment:** use her refugees as labor or bait, risking her departure
- **Village bond scene:** she chooses which cellar becomes an infirmary and asks who will carry water when arrows fall, then quietly checks the edge on a plain old sword kept for defending the wounded

## Campaign Structure

The target campaign has six acts:

1. **Act I: The Teeth in the Sack** - ultimatum, audit, first choice
2. **Act II: The Seven Roads** - open-ended recruitment board
3. **Act III: The Village Learns Fear** - pressure interludes and preparation after recruitment closes
4. **Act IV: The Oath Council** - return, defender conflicts, final defense plan
5. **Act V: The Ashwick Siege** - multi-phase battle
6. **Act VI: The Names After** - aftermath, endings, permanent consequences

## Act I: The Teeth in the Sack

### Quest: `qst_seven_ash_ultimatum`

#### Trigger Conditions

- Player owns or protects a village, town district, castle village, or major camp.
- Settlement prosperity or population is high enough to be worth extortion.
- Nearby bandit activity or deserter pressure exists.
- Player is not already in a major siege finale.
- Campaign has not already completed or failed.

#### Opening Scene

Wulfred's riders arrive before full daylight. They do not rush. They let Ashwick watch them count doors, wells, barns, and children. Their leader, **Rafe Carrick**, Wulfred's nephew, throws a sack at the reeve's feet.

Inside are teeth, bent buckles, and three stamped tokens from Briar Ford, Little Harrow, and Saint Ormond's Grange.

Rafe says:

> "My uncle asks polite because he remembers being lawful. Five thousand denars. Five hundred sacks of grain. Twelve children as surety. One hundred days. Refuse him and he comes himself."

Mother Hilda asks whether the children are hostages.

Rafe answers:

> "Surety is a kinder word. Use it while you still have kind words."

#### Player-Facing Dilemma

Ashwick can neither pay nor fight as it is. The nearest lord may not come. The sheriff's men are few. The harvest is not fully in. The player must choose the campaign posture.

#### Choices

These choices should be implemented as a council scene with Rafe, Mother Hilda, Reeve Martin, Piers, and Nell present. A menu can present or confirm the final campaign posture after dialogue has played, but the roleplaying should come from who the player answers, reassures, threatens, or ignores.

**1. Prepare Ashwick without outside help**

- **Action:** spend coin, labor, and food to fortify and train.
- **Cost:** high labor strain, immediate production loss, fortification expense.
- **Outcome:** skips most recruitment but opens strong local-preparation route.
- **Flags:** `seven_ash_fortify_alone_chosen`, `method_common_defense`
- **Next:** Act III preparation interludes, then siege.

**2. Find defenders**

- **Action:** seek skilled defenders who can train, plan, and fight.
- **Cost:** travel time, expenses, village fear while player is away.
- **Outcome:** opens Act II recruitment chain.
- **Flags:** `seven_ash_recruitment_chosen`
- **Next:** `qst_seven_ash_first_road`

**3. Send to the nearest lord**

- **Action:** ask lawful authority for protection.
- **Requirement:** lord relation, legal standing, or noble reputation.
- **Outcome:** can gain troops, but Wulfred pressure rises if the lord delays or demands taxes.
- **Branch:** lawful but risky; may create `noble_notice`.
- **Next:** Act III with possible lordly detachment, not enough by itself.

**4. Bargain with Wulfred**

- **Action:** offer coin, grain, road rights, or service.
- **Outcome:** can delay siege or produce a dark ending if accepted fully.
- **Risk:** morale collapse, permanent tribute, Wulfred spies inside Ashwick.
- **Flags:** `method_wulfred_bargained`
- **Possible ending:** `ending_ashwick_under_the_ash_captain`

**5. Evacuate**

- **Action:** abandon Ashwick.
- **Outcome:** not instant game over; creates refugee route and shame memory.
- **Flags:** `seven_ash_evacuation_started`
- **Possible ending:** `ending_the_long_road_from_ashwick`

**6. Kill the messengers**

- **Action:** execute or ambush Rafe's riders.
- **Outcome:** buys pride, not safety. Pressure spikes. Wulfred attacks harder.
- **Flags:** `method_hardline`, `wulfred_pressure +25`
- **Next:** Act II opens with higher pressure, or Act III emergency preparation if the player abandons recruitment and returns immediately.

### Quest: `qst_seven_ash_village_audit`

This quest should occur immediately after the ultimatum unless the player flees or fully bargains.

#### Purpose

Make Ashwick concrete. The player should inspect what can be defended, what must be abandoned, and who is afraid.

#### Required Stops

- **The Palisade:** rotten posts, shallow ditch, missing gate pins.
- **The Granary:** enough food for normal winter, not enough for siege and refugees.
- **The Churchyard:** stone wall, cemetery, potential fallback position.
- **The Mill Bridge:** crossing point and likely first target.
- **The Outer Farms:** impossible to defend all of them.
- **The Cellars:** shelter potential, but fire and smoke risk.

#### Witnesses

- Mother Hilda: civilian survival.
- Reeve Martin: labor and stores.
- Piers Wainwright: roads and evacuation.
- Nell of Little Harrow: Wulfred's real methods.

#### Audit Outcomes

The audit sets starting values:

- `ashwick_fortification`
- `ashwick_food`
- `ashwick_morale`
- `ashwick_intelligence`
- `ashwick_civilian_safety`
- `settlement_strain`

The player can choose one immediate priority:

1. repair palisade
2. dig ditch and stake approaches
3. secure granary
4. train militia
5. evacuate outer farms
6. scout Wulfred's road

Each priority grants a small bonus and changes early pressure.

## Act II: The Seven Roads

Act II should be open-ended once the first lead is discovered. The player receives a recruitment map and can pursue the seven defender roads in any order. This act should feel like riding out into a dangerous country to gather people, not like clicking seven menu entries in a fixed sequence.

Each recruitment stage should have:

- lead source
- travel target
- witness
- negotiation
- optional test
- recruitment method
- result flags
- return consequence

### Open-Ended Recruitment Board

The recruitment board is the Act II hub. It should show all known defender leads, their travel targets, and their current status.

The board should not resolve recruitment by itself. It sends the player to people and places. The actual persuasion, refusal, coercion, and compromise should happen through dialogue with the recruit, their witness, their enemy, or the local authority around them.

Recommended statuses:

- `unknown`: lead not discovered yet
- `available`: lead known and can be pursued
- `in_progress`: player is inside that recruitment chapter
- `recruited`: defender joined or agreed to meet at Ashwick
- `refused`: player declined or failed peacefully
- `alienated`: defender will not help because of player method
- `lost`: defender died, was captured, or became impossible to recover
- `abandoned`: player ended Act II before resolving this lead

Design rules:

- The player can leave a recruitment chapter and return later unless the local scene logically closes.
- Some recruitment chapters can reveal or discount others, but none should require a fixed previous defender.
- The board should warn the player when a route is becoming time-sensitive.
- Abandoning unresolved leads is allowed, but should be explicit and remembered.
- Returning to Ashwick with fewer than seven defenders is valid, not a soft lock.

### Act II Completion Gate

Act III should not begin until Act II is complete. Completion occurs when all seven defender roads are terminal or when the player formally ends recruitment.

Completion script logic:

```md
act2_recruitment_resolved_count =
  recruited + refused + alienated + lost + abandoned

if act2_recruitment_resolved_count >= 7:
  act2_recruitment_complete = true

if player_selects_end_recruitment:
  mark all non-terminal defender roads as abandoned
  act2_recruitment_complete = true
```

Once `act2_recruitment_complete = true`, the next return to Ashwick starts Act III. The return should be a proper scene, not an instant menu transition: villagers count who came back, who did not, and what the player spent to find them.

### Act II Pacing Beats

Act II should still have momentum even while open-ended.

Use these light-touch beats between recruitment chapters:

- **Day 80-70:** Ashwick sends practical letters: timber shortfalls, grain tallies, frightened families.
- **Day 69-55:** travelers mention Wulfred's scouts asking after Ashwick.
- **Day 54-40:** courier reports show pressure rising: livestock stolen, roads watched, rumors spreading.
- **Day 39-25:** some slow recruitment methods become harder, more expensive, or morally compromised.
- **Day 24-1:** Ashwick begs the player to return; unresolved leads can still be chased, but the cost should be obvious.
- **Day 0 or below:** the next return begins Act III in emergency mode with Wulfred already near.

These beats should be short and atmospheric. They should not interrupt the player with major village choices until Act III.

### Return to Ashwick Scene

When Act II closes, run a visible homecoming scene.

Scene ingredients:

- defenders arrive one by one or are conspicuously absent
- Mother Hilda asks how many beds to prepare
- Reeve Martin asks how much coin, grain, and time remain
- Nell watches the road behind the player instead of the recruits
- villagers react differently to honorable recruits, paid recruits, coerced recruits, and missing recruits

This scene should set:

- `act2_recruitment_complete`
- `act3_pressure_started`
- starting Act III pressure modifiers
- defender bond flags visible to the village
- unresolved recruitment consequences

### Quest: `qst_seven_ash_garric_ashbow`

#### Lead

Nell of Little Harrow names a forester who shot raiders from a church roof while others ran. Piers knows he drinks at the Split Hart and sells rabbits no one saw him trap.

#### Target

The Split Hart tavern, near a disputed hunting wood.

#### Opening Scene

Garric sits with his back to the wall and his bow unstrung across his knees. He counts every door before he lets the player speak. Two young men at another table call him coward. He does not answer because he has already decided where each would fall if the room turned.

He says:

> "Villages do not need heroes. They need orders that do not change when screaming starts. Can you give those?"

#### Witness Step

Speak to **Eda Flint**, a widow whose husband fought under Garric. She says Garric held the line longer than his lord did, but the lord wrote the report.

Options:

- believe Eda publicly
- keep her testimony quiet
- use it to shame Garric
- ignore it and negotiate only coin

#### Recruitment Choices

**1. Pay him as a captain**

- **Cost:** 700 denars now, 300 after siege.
- **Gain:** Garric joins with high `debt`, low `trust`.
- **Effect:** `ashwick_intelligence +5`, archer training unlock.
- **Risk:** may leave if payment fails.

**2. Give him authority over bowmen and no false charges**

- **Requirement:** honor reputation or successful Eda witness.
- **Gain:** high `trust`, moderate `pride`.
- **Effect:** `ashwick_militia_training +8`, `ashwick_morale +3`.
- **Scene:** Garric asks for names of every person expected to hold a bow.

**3. Promise to clear his name after the siege**

- **Requirement:** access to noble court or legal route.
- **Gain:** high `pride`, moderate `debt`.
- **Risk:** if promise is not kept, post-campaign grievance.

**4. Blackmail him with the old rout**

- **Gain:** immediate service.
- **Cost:** `method_blackmail`, `garric_fear +20`, betrayal risk.
- **Effect:** good tactical performance, poor morale aura.

**5. Leave without him**

- **Outcome:** unlocks alternate archer training with lower ceiling.
- **Cost:** time spent, no defender.

#### Return Scene

Garric climbs Ashwick's watch platform and quietly says which roofs must be cleared, which trees must be cut, and which young men should never be given bows because they want to be seen firing.

### Quest: `qst_seven_ash_oswin_ditchwright`

#### Lead

Reeve Martin says walls are useless without a ditch, and there is a man at the quarry who can read earth like a clerk reads a ledger.

#### Target

Harrowcut Quarry, where a bridge collapse has killed two workers and the quarry master blames Oswin.

#### Opening Scene

Oswin is standing knee-deep in mud while men shout at him from dry ground. He has drawn the failed bridge in charcoal on a plank and marked the exact beam that gave way.

He says:

> "Every collapse has witnesses. Wood bends. Stone shifts. Men lie afterward."

#### Witness Step

Inspect the bridge site with Oswin and question three workers.

Findings:

- cheap timber was used
- the quarry master rushed work
- Oswin warned them
- one worker hid the warning because he feared losing wages

#### Recruitment Choices

**1. Vindicate him publicly**

- **Action:** expose the quarry master's negligence.
- **Gain:** Oswin joins with high `trust`.
- **Cost:** quarry master hostility, possible timber price increase.
- **Effect:** stronger fortification projects.

**2. Pay the quarry debt**

- **Cost:** 500 denars.
- **Gain:** Oswin joins through `debt`.
- **Effect:** reliable engineering, no political fight.

**3. Hire him but limit his authority**

- **Gain:** joins.
- **Risk:** slower fieldworks, fewer sacrifices demanded.
- **Effect:** lower strain, lower fortification.

**4. Force service through debt**

- **Gain:** immediate service.
- **Cost:** `method_hostage_surety` style debt pressure, Oswin resentment.
- **Risk:** sabotage? No. Oswin is professional, but may refuse dangerous heroics.

**5. Leave without him**

- **Outcome:** local carpenters can repair palisade but no advanced fieldworks.

#### Return Scene

Oswin walks the palisade with a string line, then asks which homes the village is willing to pull down for timber. The question lands like an accusation.

### Quest: `qst_seven_ash_sir_aldrik_vane`

#### Lead

Mother Hilda knows of a knight guarding a chapel road for food and candle money. He once bore a good name, then lost it.

#### Target

Saint Cuthbert's Wayside Chapel.

#### Opening Scene

Sir Aldrik is polishing a dented helm outside a chapel too poor to repair its bell rope. A boy offers him an apple. Aldrik cuts it in half and returns the larger piece.

He says:

> "If you have come for a knight, you are late. If you have come for a man with armor, speak plainly."

#### Witness Step

Find **Mara of the Bridge**, one of the hostages Aldrik saved when he yielded the bridge. She confirms he chose living prisoners over a lord's pride.

#### Recruitment Choices

**1. Let him swear a new public oath**

- **Action:** bring Mara's testimony and Ashwick's need.
- **Gain:** high `trust`, high `pride`.
- **Effect:** morale bonus, noble notice.
- **Risk:** if Ashwick uses dishonorable methods, Aldrik objects.

**2. Hire him as a mounted captain**

- **Cost:** 600 denars, horse feed, armor repairs.
- **Gain:** `debt`, moderate reliability.
- **Effect:** mounted reserve.

**3. Promise legal restoration**

- **Requirement:** noble route.
- **Gain:** strong pride, possible post-campaign court hook.
- **Risk:** failure damages reputation.

**4. Use his cowardice charge**

- **Action:** threaten exposure or offer false pardon.
- **Gain:** service under fear.
- **Cost:** future betrayal or departure if exposed.

**5. Leave him at chapel**

- **Outcome:** church may still send supplies if treated well.

#### Return Scene

Aldrik asks permission to place his shield on Ashwick's gate. If allowed, the village cheers too loudly, because they are cheering the idea of rescue more than the man.

### Quest: `qst_seven_ash_mirelle_voss`

#### Lead

Piers says Wulfred's host has informants. To catch them, the player needs someone who knows how frightened people sell secrets.

#### Target

The riverside tavern called The Low Lantern.

#### Opening Scene

Mirelle Voss owns the room without appearing to. She pours watered ale for men with knives and remembers who pays in clipped coin. She smiles when the player asks for help.

She says:

> "You want honest folk defended by dishonest work. That is most wars, only smaller."

#### Witness Step

A boy named **Tib** has been carrying messages for Wulfred's scouts. Mirelle can catch him, but what happens to him becomes the moral test.

Options:

- spare Tib and turn him into a double messenger
- pay him and send him away
- hand him to local law
- threaten him and use his fear

#### Recruitment Choices

**1. Give Mirelle evacuation authority**

- **Gain:** high `trust`, high `village_bond`.
- **Effect:** hidden routes, spy detection, civilian safety.
- **Cost:** elders dislike giving authority to a tavern criminal.

**2. Buy her network**

- **Cost:** 500 denars, recurring expense.
- **Gain:** intelligence, low trust.

**3. Promise protection from magistrates**

- **Requirement:** legal or underworld leverage.
- **Gain:** she joins, but expects future favors.

**4. Threaten exposure**

- **Gain:** service through fear.
- **Risk:** she may sell controlled information to test you.

**5. Leave without her**

- **Outcome:** Wulfred spy interludes become harder.

#### Return Scene

Mirelle asks for chalk, thread, and three women who can keep secrets. By dusk, Ashwick has routes through kitchens, pig pens, and loose fence boards that no raider would think to watch.

### Quest: `qst_seven_ash_tomas_reed`

#### Lead

Garric or Mother Hilda names a retired sergeant whose levies survived two campaigns. He now lives in a veterans' almshouse, where half the men hate him and half owe him their lives.

#### Target

The Red Crutch almshouse.

#### Opening Scene

Tomas Reed is mending boots, not weapons. He listens to the threat, then asks how many children Ashwick has and how much grain. When the player gives him fighting numbers first, he interrupts.

> "I asked what breaks if you lose. Men fight better when they know what stands behind them."

#### Witness Step

Speak to two veterans:

- **Old Jory**, who says Tomas saved them with discipline.
- **Matteo**, who says Tomas had deserters flogged until one died.

Both are true.

#### Recruitment Choices

**1. Hire him with written limits**

- **Action:** Tomas may drill, punish, and command watches, but cannot flog without council approval.
- **Gain:** high trust from villagers, moderate respect from Tomas.
- **Effect:** training bonus without major morale loss.

**2. Give him full command over militia**

- **Gain:** fast training.
- **Cost:** morale strain, youth fear.
- **Risk:** desertion interlude if strain rises.

**3. Ask him to train trainers, not soldiers**

- **Gain:** slower but sustainable training.
- **Effect:** lower strain, lower peak combat.

**4. Use him to break panic**

- **Action:** authorize harsh discipline.
- **Cost:** `method_hardline`, `settlement_strain +15`.
- **Effect:** strong anti-rout bonus.

**5. Leave without him**

- **Outcome:** militia training capped.

#### Return Scene

Tomas watches Ashwick's militia hold spears like broom handles and says, "Good. No bad habits yet." Nobody knows whether to laugh.

### Quest: `qst_seven_ash_beren_hardhand`

#### Lead

Wulfred has a champion called **Halvorn Pike**. If the raiders breach the wall, someone must meet him. Mirelle knows a man ugly enough for that work.

#### Target

An outlaw camp, mill yard, or pit-fighting barn.

#### Opening Scene

Beren Hardhand fights three men with a blunted axe and still makes the spectators step back. When he hears Ashwick's name, he spits.

> "Villages remember law when they need hanging done. Now one needs a lawless man to stand in its gate. That is a fine joke."

#### Witness Step

Speak to **Ansel Miller**, who knew Beren's family before famine law turned them into thieves. He says Beren is dangerous, but not empty.

#### Recruitment Choices

**1. Best him or endure him in a controlled duel**

- **Requirement:** combat capability or champion companion substitute.
- **Gain:** high `pride`, moderate `trust`.
- **Effect:** shock reserve without friendly-fire risk.

**2. Offer lawful pardon for service**

- **Requirement:** legal authority or noble witness.
- **Gain:** strong reason to fight, but local resentment.

**3. Offer spoils**

- **Gain:** joins for plunder.
- **Risk:** looting temptation during siege.

**4. Point him at Wulfred and ignore restraint**

- **Gain:** strong combat.
- **Cost:** civilian fear, possible prisoner killing.

**5. Leave without him**

- **Outcome:** breach duel becomes harder.

#### Return Scene

Beren stands in Ashwick's gate and tests the beam with his shoulder. A child hides behind Mother Hilda. Beren notices and steps away from the gate, as if that fixes anything.

### Quest: `qst_seven_ash_sister_elianor`

#### Lead

Refugees from Saint Ormond's say a sister keeps survivors alive in the old sheep barns. She has no soldiers, but fifty people obey her faster than they obey any lord.

#### Target

Saint Ormond's refugee camp.

#### Opening Scene

Sister Elianor is washing blood from a boy's hair with water already used twice. She does not look holy. She looks tired enough to become stone.

> "If you want blessings, go to a bishop. If you want people carried out from under burning roofs, tell me how many carts you brought."

#### Witness Step

The player must inspect the camp:

- wounded who cannot march
- widows who want revenge
- children who need shelter
- two men who want to join the fight but cannot stand in formation

#### Recruitment Choices

**1. Create a sanctuary at Ashwick**

- **Cost:** food, space, labor.
- **Gain:** high `trust`, high refugee trust.
- **Effect:** civilian survival, healing, morale.

**2. Accept only able workers and fighters**

- **Gain:** labor and militia.
- **Cost:** Elianor disapproves; refugee trust split.

**3. Fund her camp but do not bring refugees**

- **Cost:** coin and supplies.
- **Gain:** healer support, lower strain.
- **Effect:** less civilian safety bonus.

**4. Use refugees as labor under guard**

- **Gain:** fast fieldworks.
- **Cost:** high strain, Elianor may refuse or depart.

**5. Leave without her**

- **Outcome:** no organized infirmary; aftermath casualties rise.

#### Return Scene

Elianor asks for the church key, the granary tally, and a list of every cellar that stays dry. Mother Hilda gives her all three without asking the player.

## Act III: The Village Learns Fear

Act III begins only after Act II is complete and the player has returned to Ashwick. This is where the pressure that built quietly during the open-ended recruitment phase becomes local, visible, and interactive.

Trigger requirement:

- `act2_recruitment_complete = true`
- player has returned to Ashwick
- campaign has not shifted into bargain-only, evacuation-only, or failed state

Act III interludes should trigger based on `days_remaining`, `wulfred_pressure`, recruited defenders, abandoned defender roads, and player choices.

### Act III Opening Mood

The first Act III scene should always answer three questions:

1. Who did the player bring back?
2. What did Ashwick lose while the player was away?
3. What must be done before Wulfred arrives?

Opening variations:

- **Strong return:** five to seven defenders recruited, moderate time remaining, villagers gather with fear but visible hope.
- **Thin return:** two to four defenders recruited, several roads abandoned, villagers ask whether this is all.
- **Hard return:** several coerced recruits, high method fear, defenders arrive armed but not trusted.
- **Late return:** `days_remaining <= 20`, work begins at night, and the first interlude fires almost immediately.
- **Emergency return:** `days_remaining <= 0`, Wulfred's vanguard is already near and Act III compresses into rapid preparation choices.

### Act III Pacing

Act III should feel denser than Act II. The player is no longer roaming freely for recruits; they are triaging a community under pressure.

Recommended duration:

- standard return: 20-40 campaign days of preparation and interludes
- late return: 8-20 days
- emergency return: 1-7 days or immediate siege setup

Recommended rhythm:

- one opening consequence scene
- two to four pressure interludes
- one defender conflict or loyalty scene
- one preparation project choice
- one final warning before Act IV

The exact number should scale with remaining time and pressure. Do not force every interlude in one playthrough.

### Interlude: The Burned Cow

#### Trigger

`wulfred_pressure >= 25` or 70 days remaining.

#### Scene

A cow is found burned in an outer pasture with Wulfred's mark cut into the fence. The animal matters because it is meat, milk, traction, and fear in one body.

#### Choices

1. send scouts after the raiders
2. evacuate outer farms
3. publicly ignore the provocation
4. punish suspected informants
5. send a warning back to Wulfred

#### Effects

- scouting can reduce pressure
- evacuation raises strain but protects civilians
- ignoring preserves time but hurts morale
- punishing informants can catch a spy or create injustice
- warning back raises pressure and pride

### Interlude: The Knife-Marked Door

#### Trigger

Mirelle not recruited and `wulfred_pressure >= 50`, or any route with high outlaw notice.

#### Scene

A door is marked at night. By morning the family inside has fled. Someone in Ashwick is telling Wulfred which households have sons fit for hostage taking.

#### Choices

1. investigate quietly
2. hold public accusations
3. move vulnerable families
4. bait the informant with false plans
5. do nothing to avoid panic

#### Effects

Mirelle makes this easier. Aldrik may oppose quiet methods. Elianor demands protection over punishment.

### Interlude: The Grain Riot

#### Trigger

`ashwick_food` low or `settlement_strain >= 50`.

#### Scene

Women gather at the granary because ration measures have changed. Tomas calls it disorder. Elianor calls it hunger. Reeve Martin calls it arithmetic.

#### Choices

1. open the stores fairly
2. enforce ration discipline
3. buy grain at high cost
4. seize hidden private grain
5. promise future compensation

#### Effects

This interlude should strongly affect morale and trust. It also tells the player whether Ashwick is becoming a community or a garrison.

### Interlude: Wulfred's Offer

#### Trigger

`wulfred_pressure >= 60`, at least one defender recruited.

#### Scene

Wulfred sends a letter addressed to one defender. The offer is tailored:

- Garric: name cleared and archers spared
- Oswin: money and materials
- Aldrik: restored knightly standing
- Mirelle: safe passage and legal pardon
- Tomas: command under Wulfred
- Beren: Halvorn's place as champion
- Elianor: refugees left untouched if Ashwick yields

#### Choices

1. let the defender answer privately
2. answer publicly as a village
3. hide the letter
4. forge a reply to mislead Wulfred
5. punish the messenger

#### Effects

Reads defender bond values. High trust creates a strong loyalty scene. High fear or debt may create departure risk.

### Interlude: The First Funeral

#### Trigger

Any interlude casualty or preparation accident.

#### Scene

The village buries someone before the siege has even begun. This is where the campaign asks whether preparation has already become war.

#### Choices

1. speak honestly about the cost
2. promise victory
3. blame Wulfred
4. blame negligence
5. say nothing and return to work

#### Effects

Small but durable morale shift. Defenders react based on personality.

## Act IV: The Oath Council

### Quest: `qst_seven_ash_oath_council`

#### Trigger

Act III has started, at least one major Act III interlude has resolved, and one of the following is true:

- `days_remaining <= 25`
- `wulfred_pressure >= 75`
- the player has completed the chosen preparation project
- the player chooses to call the council early
- emergency return mode is active

#### Purpose

Bring all recruited defenders, village witnesses, and preparation choices into one visible strategic decision.

#### Scene

The council meets in the church because it is the only building with enough stone to make frightened people speak quietly. A rough map of Ashwick lies on a trestle table. Every defender marks the map differently:

- Garric marks sightlines.
- Oswin marks ditches and weak posts.
- Aldrik marks where men should stand.
- Mirelle marks where frightened people will actually run.
- Tomas marks watch rotations.
- Beren marks the gate and asks why anything else matters.
- Elianor marks cellars, wells, and the infirmary.

#### Required Council Questions

1. Where do civilians go?
2. What is defended first?
3. What is abandoned?
4. Who commands the militia?
5. What happens to prisoners?
6. What is the fallback if the gate breaks?
7. Does the village fight to preserve homes, people, or Wulfred's destruction?

#### Defense Plans

**Plan A: Hold the Palisade**

- Strong with Garric, Oswin, Tomas.
- Protects buildings.
- Risks high militia casualties if breach occurs.

**Plan B: Defense in Depth**

- Strong with Oswin, Mirelle, Elianor.
- Abandons outer ring, protects civilians.
- Costs homes and morale before battle.

**Plan C: Counterstroke**

- Strong with Aldrik, Beren, Tomas.
- Attempts to break Wulfred's vanguard.
- High risk, high reward.

**Plan D: Cut the Head**

- Strong with Garric and Mirelle.
- Focuses on Wulfred and lieutenants.
- Can reduce enemy morale, but failure causes chaos.

**Plan E: The Empty Village**

- Strong with Piers, Mirelle, Elianor.
- Evacuates civilians and turns Ashwick into a trap.
- Saves lives but may destroy settlement.

**Plan F: Terms and Trap**

- Uses false negotiation.
- Requires high intelligence or Mirelle/Oswin.
- Can wound Wulfred before siege, but if discovered pressure spikes.

#### Council Conflict Checks

Potential conflicts:

- Beren rejects evacuation as cowardice.
- Aldrik rejects assassination or false surrender.
- Elianor rejects no-quarter orders.
- Tomas rejects militia command by committee.
- Mirelle rejects plans that assume civilians obey orders under fire.
- Oswin rejects heroic defense of indefensible walls.
- Garric rejects any charge not covered by archers.

The player can:

- mediate
- choose one commander's plan
- split responsibilities
- silence dissent
- delay decision

Delaying decision increases pressure but may unlock one more preparation.

## Act V: The Ashwick Siege

The final siege should play in phases. Implementation can begin with short order menus, dialogue check-ins, and mission templates, then later become fuller scenes.

### Siege Overview

Wulfred arrives with a host sized to the player's visible strength. The recommended narrative range is **180-420 fighters**, with about **240-320** being the common range when the player fields a typical 50-85 troop SoD army.

Example host sizes:

| Player field strength | Wulfred host size | Campaign read |
| --- | ---: | --- |
| 0-25 troops | 180 fighters | Ashwick is nearly alone against a war-band. |
| 26-50 troops | 190-240 fighters | Wulfred expects resistance and brings extra blades. |
| 51-85 troops | 240-310 fighters | Wulfred treats the player as a real commander. |
| 86-130 troops | 310-400 fighters | Wulfred gathers allied brigands and deserter companies. |
| 131+ troops | 400-420 fighters | Wulfred avoids fair battle and pressures civilians, roads, and fires. |

Composition:

- deserter men-at-arms
- foot brigands
- poacher archers
- mounted scouts
- wagon followers
- shielded gate-breakers
- two or three named lieutenants

Suggested lieutenants:

- **Rafe Carrick:** envoy and nephew, fast cavalry pressure.
- **Halvorn Pike:** champion, breach leader.
- **Maud the Ledger:** quartermaster, keeps host fed and disciplined.
- **Sibert Crow-Eye:** scout leader and arsonist.

The player does not need to kill all enemies. Victory can come from breaking command, exhausting assault, saving civilians, or forcing retreat. The siege should spawn the host in waves and sectors rather than placing every raider on the field at once.

Recommended wave allocation:

- **Outer Fields:** 12-18% of host strength, mostly scouts, poachers, mounted raiders, arsonists.
- **Palisade and Ditch:** 25-35% of host strength, mostly brigands, archers, shield carriers.
- **Gate or Breach:** 15-25% of host strength, including elite core and Halvorn's men.
- **Inner Streets:** 12-20% of host strength, mixed raiders and looters who slipped through.
- **Churchyard Stand:** 8-15% of host strength, Wulfred's remaining loyalists and named survivors.
- **Reserve/offscreen pressure:** any remainder, used for pursuit, civilian threat, morale checks, or retreat logic.

Preparation can reduce the number that reaches later phases. Poor scouting, high pressure, or weak sector commitment increases the number that arrives fresh.

Large player army rule: if the player has enough troops to win one sector easily, Wulfred should threaten another. The campaign should reward strength with fewer casualties and cleaner options, but still ask the player to protect civilians, supplies, roads, and fire lines.

### Phase 1: Outer Fields

#### Conditions Read

- `ashwick_intelligence`
- scout interludes
- Garric recruited
- Mirelle recruited
- Wulfred pressure
- outer farms evacuated

#### Possible Events

- scouts find Wulfred's vanguard early
- poachers burn hayricks
- civilians trapped at outer farms
- mounted probes test the ditch
- Sibert Crow-Eye attempts arson

#### Player Choices

1. skirmish forward with scouts
2. hold all forces behind ditch
3. rescue outer farm families
4. burn fields to deny cover
5. feign weakness to draw scouts in

#### Outcomes

Good scouting lowers enemy opening strength. Failed scouting lets Wulfred choose attack line.

### Phase 2: Ditch and Palisade

#### Conditions Read

- `ashwick_fortification`
- Oswin recruited
- Tomas recruited
- Garric recruited
- ditch completed
- palisade repaired

#### Possible Events

- enemy rushes ditch
- gate pins fail
- archers panic
- militia overfires too early
- Oswin's planned dead ground works or fails

#### Player Choices

1. hold fire until marked range
2. reinforce gate
3. countercharge a stuck assault
4. abandon palisade as planned
5. spend reserve to save a weak section

#### Outcomes

This phase determines whether the battle enters street fighting cleanly or catastrophically.

### Phase 3: Gate and Breach

#### Conditions Read

- Aldrik recruited
- Beren recruited
- Tomas recruited
- militia training
- morale
- Halvorn Pike alive

#### Possible Events

- Halvorn challenges the gate
- Aldrik can lead a shielded reserve
- Beren can meet the champion
- Tomas can steady spear ranks
- panic may open a side lane

#### Player Choices

1. send Beren to meet Halvorn
2. send Aldrik and shieldmen
3. collapse the gate approach
4. retreat to inner streets
5. rally militia personally

#### Outcomes

If the breach is held, Wulfred loses time and men. If it collapses, civilians are at immediate risk.

### Phase 4: Inner Streets

#### Conditions Read

- Mirelle recruited
- Elianor recruited
- civilian safety
- evacuation routes
- settlement strain
- defense plan

#### Possible Events

- raiders enter homes
- fires start
- civilians trapped in cellars
- false lanes lure enemies
- infirmary threatened
- Maud the Ledger tries to keep raiders disciplined

#### Player Choices

1. save civilians
2. hold barricades
3. lure raiders into false gate
4. protect infirmary
5. abandon street to preserve final reserve

#### Outcomes

This phase determines civilian casualties and settlement damage more than enemy casualties.

### Phase 5: The Churchyard Stand

#### Conditions Read

- morale
- Elianor recruited
- Aldrik recruited
- Mother Hilda alive
- churchyard prepared
- Wulfred wounded or confident

#### Scene

The church bell rings until the rope snaps. The cemetery wall becomes the final line. Wulfred enters either laughing, furious, wounded, or silent depending on prior phases.

#### Player Choices

1. duel or confront Wulfred
2. offer terms for prisoners and retreat
3. order no quarter
4. save remaining civilians over killing Wulfred
5. trigger last trap or last counterattack

#### Outcomes

The siege ends here, but not always with Wulfred dead.

## Act VI: The Names After

### Immediate Aftermath

The aftermath should not jump straight to rewards. It should walk through the cost.

Required checks:

- How many civilians died?
- How many homes burned?
- How many defenders survived?
- Was Wulfred killed, captured, escaped, or bargained with?
- Did the player keep promises?
- Were prisoners spared?
- Did Ashwick remain a village or become a fortress/refugee camp?

### Defender Epilogues

Each recruited defender gets a short outcome.

### Companion Conversion Rule

The seven can become companions, but survival alone is not enough. Each defender should offer to join the player only if they personally believe the player's decisions proved something they value.

Shared requirements:

- the defender was recruited
- the defender survived the siege
- the defender was not alienated, betrayed, or abandoned
- the player speaks to the defender in aftermath dialogue
- the defender's unique unlock condition is met

If a defender qualifies, their aftermath dialogue should offer three outcomes:

1. **Join the player as a companion.**
2. **Remain in Ashwick as a unique trainer/contact.**
3. **Part ways with respect.**

If a defender does not qualify, they should still receive an epilogue, but they should explain why they are not joining. This refusal should be character-specific, not a generic "requirements not met" line.

Recommended implementation:

```md
if defender_survived and defender_recruited and unique_companion_condition_met:
  set defender_companion_unlock_bitmask
  open defender companion offer dialogue
else:
  set defender_companion_refusal_bitmask when refusal is explicit
  play defender-specific closure dialogue
```

#### Garric

- **High trust, survived:** stays to train watch archers or leaves with his name partly restored.
- **Paid only:** collects and disappears before speeches.
- **Blackmailed:** may challenge the player or vanish with evidence.
- **Died:** arrows are planted on the watch platform as memorial.
- **Companion unlock:** the player publicly accepted Eda Flint's testimony, did not blackmail Garric, used covered fire or disciplined defense during the siege, and avoided wasting militia in an uncovered charge.
- **Why he joins:** the player proved they understand command responsibility and will not spend common soldiers for vanity.
- **Why he refuses:** if the player ordered needless charges, hid the truth, or treated him as a hired bow, Garric stays only long enough to settle his account.

#### Oswin

- **Vindicated:** becomes master of works or receives court summons.
- **Debt-bound:** demands payment and apology.
- **Died:** his chalk marks remain on doors that did not burn.
- **Companion unlock:** the player vindicated him or respected his engineering authority, accepted at least one hard fieldwork sacrifice, and did not override his warnings for heroic theater.
- **Why he joins:** the player listened when earth, timber, and measurements mattered more than pride.
- **Why he refuses:** if forced through debt, ignored safety warnings, or protected every house while demanding impossible walls, Oswin remains a builder but not the player's man.

#### Aldrik

- **Oath honored:** regains standing through common witness, not noble pardon.
- **Used dishonorably:** leaves shield behind, refuses praise.
- **Died:** buried at church gate with spear and shield reversed.
- **Companion unlock:** the player let him swear a public oath, spared prisoners or kept lawful terms, did not use assassination/false surrender as the main plan, and protected civilians when honor demanded it.
- **Why he joins:** Ashwick gave him a new oath, and the player proved that oath can ride beyond one village.
- **Why he refuses:** if the player won through dishonor, hostage methods, or no-quarter cruelty, Aldrik may respect the victory but will not carry the player's banner.

#### Mirelle

- **Trusted:** becomes quiet protector of Ashwick's roads.
- **Bought:** takes payment and warns the player to keep better secrets.
- **Threatened:** may leak a final truth or demand favor.
- **Died:** women of Ashwick keep her chalk marks intact.
- **Companion unlock:** the player trusted her with evacuation routes or spy work, handled Tib or another informant without pointless cruelty, used deception to save lives rather than only to humiliate enemies, and did not expose or threaten her past.
- **Why she joins:** the player can use dirty work without pretending their hands are clean.
- **Why she refuses:** if bought, threatened, or treated as disposable criminal labor, Mirelle leaves with a smile and one secret still held back.

#### Tomas

- **Limited discipline worked:** admits villagers can be soldiers without becoming camp beasts.
- **Harsh route:** leaves behind drilled men and bitter families.
- **Died:** his whistle hangs in the militia hall.
- **Companion unlock:** the player set clear discipline limits, kept the militia line from breaking, avoided terror as the default training method, and showed that order can protect civilians without crushing them.
- **Why he joins:** the player gave frightened people discipline without turning them into punished animals.
- **Why he refuses:** if the player encouraged flogging, martial fear, or command by cruelty, Tomas may call the defense effective but will not pretend it was soldiering.

#### Beren

- **Respected:** accepts a place at the mill or gate.
- **Spoils route:** takes loot and unsettles Ashwick.
- **Unrestrained route:** may become a new local threat.
- **Died:** remembered as frightening, necessary, and not fully understood.
- **Companion unlock:** the player beat or withstood him fairly, gave him a lawful enemy, restrained him from harming civilians, and let him prove strength in the breach or against Halvorn without turning him loose on Ashwick.
- **Why he joins:** the player gave his violence a boundary and a purpose.
- **Why he refuses:** if fed only spoils, revenge, or permission to hurt, Beren either stays as a dangerous local shadow or walks away before someone tries to chain him.

#### Elianor

- **Sanctuary honored:** founds an infirmary or refuge house.
- **Limited aid:** continues elsewhere with mixed words for the player.
- **Exploited:** denounces the victory.
- **Died:** refugees maintain the infirmary in her name.
- **Companion unlock:** the player created a real sanctuary, protected refugees or wounded during the siege, avoided using civilians as bait or forced labor, and refused no-quarter orders where prisoners or children were involved.
- **Why she joins:** the player proved that survival and mercy can stand in the same doorway.
- **Why she refuses:** if refugees were exploited, prisoners butchered, or the infirmary sacrificed for convenience, Elianor's farewell should be quiet and devastating.

### Endings

| Ending ID | Name | Conditions | Outcome |
| --- | --- | --- | --- |
| `ending_seven_oaths_kept` | The Seven Oaths Kept | 6-7 defenders recruited, Ashwick survives, promises mostly kept | Ashwick becomes a renowned free defense village; militia quality and morale improve permanently. |
| `ending_ashwick_stands` | Ashwick Stands | settlement survives with moderate losses | The village survives, scarred but functional. |
| `ending_wall_of_names` | The Wall of Names | high casualties, victory | Memorial culture; morale mixed, pilgrimage/renown possible. |
| `ending_empty_houses` | The Empty Houses | civilians saved, settlement heavily damaged | Refugees live, homes burn; rebuild campaign opens. |
| `ending_wulfred_broken` | The Ash Captain Broken | Wulfred killed or captured cleanly | Regional bandit pressure drops; player gains lawful reputation. |
| `ending_wulfred_escaped` | The Ash Captain Rides | Wulfred escapes | Future revenge campaign or recurring raider pressure. |
| `ending_the_bargain_brand` | The Bargain Brand | player makes terms with Wulfred | Ashwick survives under tribute or compromised protection; trust collapses. |
| `ending_blood_for_ash` | Blood for Ash | no-quarter/scorched victory | Wulfred destroyed, but Ashwick fears the player. |
| `ending_the_long_road_from_ashwick` | The Long Road From Ashwick | evacuation route | settlement lost, people survive as refugees. |
| `ending_the_palisade_grave` | The Palisade Grave | defense fails with high casualties | Ashwick falls; survivors carry a ruin memory. |
| `ending_the_new_wolf` | The New Wolf | player uses terror, forced labor, hostage methods | settlement survives by becoming militarized and feared. |
| `ending_the_common_bell` | The Common Bell | few elite recruits, strong village preparation | Ashwick's own militia becomes the legend. |

### Rewards and Consequences

Possible rewards:

- permanent Ashwick militia upgrade
- local relation increase
- regional bandit pressure decrease
- special watch post or militia hall
- access to qualifying surviving defenders as companions
- non-joining survivors can remain as trainers, engineers, militia officers, healers, scouts, or underworld contacts
- trade route safety
- court recognition if lawful methods used
- refugee labor and population recovery if sanctuary honored

Possible costs:

- burned buildings
- lost prosperity
- refugee burden
- noble suspicion
- church condemnation
- underworld debt
- Wulfred revenge
- defender grievance
- internal Ashwick faction split

## Implementation Lowering Plan

### Campaign Flow Graph

```md
campaign_seven_oaths_of_ash
|
+-- qst_seven_ash_ultimatum
|   |
|   +-- prepare alone
|   |   -> qst_seven_ash_village_audit
|   |   -> qst_seven_ash_pressure_interlude
|   |   -> qst_seven_ash_oath_council
|   |
|   +-- recruit defenders
|   |   -> qst_seven_ash_village_audit
|   |   -> mnu_seven_ash_recruitment_map
|   |   -> seven defender roads in any order
|   |   -> all roads recruited/refused/alienated/lost/abandoned
|   |   -> qst_seven_ash_return_to_ashwick
|   |   -> qst_seven_ash_pressure_interlude
|   |   -> qst_seven_ash_oath_council
|   |
|   +-- call for lordly aid
|   |   -> qst_seven_ash_village_audit
|   |   -> noble_notice route modifier
|   |   -> delayed or partial reinforcement
|   |
|   +-- bargain with Wulfred
|   |   -> qst_seven_ash_terms_and_surety
|   |   -> ending_the_bargain_brand or compromised siege
|   |
|   +-- evacuate
|   |   -> qst_seven_ash_empty_houses
|   |   -> ending_the_long_road_from_ashwick or refugee defense branch
|   |
|   +-- kill messengers
|       -> pressure spike
|       -> open Act II with higher pressure or emergency siege if recruitment is abandoned
|
+-- qst_seven_ash_pressure_interlude
|   |
|   +-- scouts answered
|   |   -> lower Wulfred pressure
|   |
|   +-- scouts ignored
|   |   -> outer farms damaged
|   |
|   +-- internal strain answered
|   |   -> morale or food stabilized
|   |
|   +-- internal strain ignored
|       -> desertion, hoarding, or betrayal risk
|
+-- qst_seven_ash_oath_council
|   |
|   +-- hold palisade
|   |   -> qst_seven_ash_outer_fields
|   |   -> qst_seven_ash_palisade
|   |
|   +-- defense in depth
|   |   -> qst_seven_ash_outer_fields
|   |   -> qst_seven_ash_inner_streets
|   |
|   +-- counterstroke
|   |   -> qst_seven_ash_outer_fields
|   |   -> qst_seven_ash_breach
|   |
|   +-- cut the head
|   |   -> Wulfred command test
|   |   -> rout, failed assassination, or churchyard confrontation
|   |
|   +-- empty village
|       -> civilian survival test
|       -> trap route or exile route
|
+-- qst_seven_ash_churchyard_stand
    |
    +-- Wulfred killed or captured
    |   -> qst_seven_ash_aftermath
    |   -> lawful/common/hardline victory ending
    |
    +-- Wulfred routed but alive
    |   -> qst_seven_ash_aftermath
    |   -> revenge hook
    |
    +-- Ashwick survives but burns
    |   -> qst_seven_ash_aftermath
    |   -> rebuild or refugee successor
    |
    +-- Ashwick falls
        -> qst_seven_ash_aftermath
        -> failure, exile, or revenge successor
```

### Stop Points for Implementation

These are clean archive, suspend, or handoff points for incremental implementation.

| Stop ID | Location | Runtime outcome | Campaign meaning | Follow-up |
| --- | --- | --- | --- | --- |
| `stop_seven_ash_ultimatum_answered` | after ultimatum choice | `complete` | player has chosen posture | audit or branch-specific route |
| `stop_seven_ash_audit_complete` | after village audit | `complete` | Ashwick readiness baseline exists | recruitment or preparation |
| `stop_seven_ash_first_defender` | after first recruited defender | `complete` | recruitment systems proven | continue Act II |
| `stop_seven_ash_three_defenders` | after three defender roads resolved | `complete` | viable partial defense exists | player may end recruitment early, but Act III does not begin until Act II is closed |
| `stop_seven_ash_all_roads_resolved` | after seven defender roads are terminal | `complete` | Act II recruitment board is complete | return to Ashwick and start Act III |
| `stop_seven_ash_return_complete` | after Act II homecoming scene | `complete` | Ashwick sees who came back and what was lost | Act III pressure interludes |
| `stop_seven_ash_pressure_failure` | failed pressure interlude | `fail` but recoverable | Wulfred gains advantage | later siege penalty |
| `stop_seven_ash_oath_council_locked` | after defense plan | `complete` | final plan selected | siege phases |
| `stop_seven_ash_outer_fields_done` | after outer fields | `complete` | siege opening resolved | palisade or alternate route |
| `stop_seven_ash_breach_done` | after gate/breach | `complete` or `fail` | battle state determined | inner streets or churchyard |
| `stop_seven_ash_churchyard_done` | after final stand | `complete` or `fail` | military result known | aftermath |
| `stop_seven_ash_archived` | after aftermath | `complete` | ending and survivors stored | optional successor hooks |

### Quest Chain

Recommended quest IDs:

```md
qst_seven_ash_ultimatum
qst_seven_ash_village_audit
qst_seven_ash_garric_ashbow
qst_seven_ash_oswin_ditchwright
qst_seven_ash_sir_aldrik_vane
qst_seven_ash_mirelle_voss
qst_seven_ash_tomas_reed
qst_seven_ash_beren_hardhand
qst_seven_ash_sister_elianor
qst_seven_ash_pressure_interlude
qst_seven_ash_oath_council
qst_seven_ash_outer_fields
qst_seven_ash_palisade
qst_seven_ash_breach
qst_seven_ash_inner_streets
qst_seven_ash_churchyard_stand
qst_seven_ash_aftermath
```

### Suggested Troops

Shared defender equipment rule:

- all seven unique defender troops should include a two-handed sword sidearm
- role-specific weapons remain primary where appropriate
- mission templates should not spawn any recruited defender as an unarmed noncombatant unless the scene is explicitly a captivity, disguise, or medical aftermath scene
- AI reinforcement groups should treat all seven as combat-capable, even when their best contribution is command, scouting, engineering, or healing

Unique NPCs:

- `trp_seven_ash_wulfred_carr`
- `trp_seven_ash_rafe_carrick`
- `trp_seven_ash_mother_hilda`
- `trp_seven_ash_reeve_martin`
- `trp_seven_ash_piers_wainwright`
- `trp_seven_ash_nell_harrow`
- `trp_seven_ash_garric_ashbow`
- `trp_seven_ash_oswin_ditchwright`
- `trp_seven_ash_sir_aldrik_vane`
- `trp_seven_ash_mirelle_voss`
- `trp_seven_ash_tomas_reed`
- `trp_seven_ash_beren_hardhand`
- `trp_seven_ash_sister_elianor`
- `trp_seven_ash_halvorn_pike`
- `trp_seven_ash_maud_ledger`
- `trp_seven_ash_sibert_crow_eye`

Generic troop use:

- village elder
- watchman
- farmer
- refugee
- caravan guard
- man-at-arms
- bandit
- brigand
- deserter
- hunter
- townswoman

### Suggested Menus

Menu role: navigation, confirmation, travel, broad logistics, and aftermath summary. Menus should usually be short narrative frames that move the player into dialogue or a scene.

Avoid using menus as the main place for persuasion, moral judgment, or relationship-changing decisions.

- `mnu_seven_ash_ultimatum`
- `mnu_seven_ash_village_audit`
- `mnu_seven_ash_recruitment_map`
- `mnu_seven_ash_garric_recruitment`
- `mnu_seven_ash_oswin_recruitment`
- `mnu_seven_ash_aldrik_recruitment`
- `mnu_seven_ash_mirelle_recruitment`
- `mnu_seven_ash_tomas_recruitment`
- `mnu_seven_ash_beren_recruitment`
- `mnu_seven_ash_elianor_recruitment`
- `mnu_seven_ash_pressure_interlude`
- `mnu_seven_ash_oath_council`
- `mnu_seven_ash_siege_outer_fields`
- `mnu_seven_ash_siege_palisade`
- `mnu_seven_ash_siege_breach`
- `mnu_seven_ash_siege_inner_streets`
- `mnu_seven_ash_siege_churchyard`
- `mnu_seven_ash_aftermath`

### Suggested Dialogues

Dialogue role: primary roleplaying and decision surface.

Core dialogue families:

- `dlg_seven_ash_rafe_ultimatum`: posture choice after the threat is delivered
- `dlg_seven_ash_mother_hilda_audit`: civilian survival, sanctuary, evacuation, moral objections
- `dlg_seven_ash_reeve_martin_audit`: labor, food, taxes, stores, property sacrifice
- `dlg_seven_ash_piers_roads`: scouting, evacuation routes, road rumors, courier reports
- `dlg_seven_ash_nell_harrow_witness`: Wulfred's methods and refugee pressure
- `dlg_seven_ash_garric_recruit`: Eda's testimony, command terms, pay, blackmail, refusal
- `dlg_seven_ash_oswin_recruit`: bridge evidence, quarry blame, debt, authority over fieldworks
- `dlg_seven_ash_aldrik_recruit`: hostage witness, public oath, contract, reputation pressure
- `dlg_seven_ash_mirelle_recruit`: Tib's messages, informant handling, evacuation secrets, criminal leverage
- `dlg_seven_ash_tomas_recruit`: discipline limits, punishment, drill authority, fear as method
- `dlg_seven_ash_beren_recruit`: contest terms, lawful enemy, spoils, collateral restraint
- `dlg_seven_ash_elianor_recruit`: sanctuary terms, refugee admission, triage, labor ethics
- `dlg_seven_ash_return_home`: who came back, who is missing, how Ashwick reacts
- `dlg_seven_ash_pressure_interludes`: local arguments during burned cow, marked door, grain riot, funeral
- `dlg_seven_ash_oath_council`: final defense plan argued by defenders and village witnesses
- `dlg_seven_ash_aftermath`: survivor memory, blame, gratitude, grief, permanent consequences
- `dlg_seven_ash_companion_offers`: unique survivor offers, refusals, Ashwick-stay choices, and respectful farewells

Implementation rule: each menu that offers a morally meaningful branch should point to a dialogue entry or mission scene before setting final method flags.

### Suggested Mission Templates

First implementation can still use menus for navigation and state control, but the key moments should be dialogue-led and scene-backed. Mission templates are needed when physical presence matters: a tavern insult, quarry inspection, pit contest, street argument, scouting ambush, or siege phase.

- `mt_seven_ash_garric_tavern_test`
- `mt_seven_ash_oswin_quarry_dispute`
- `mt_seven_ash_beren_pit_test`
- `mt_seven_ash_outer_fields_skirmish`
- `mt_seven_ash_palisade_defense`
- `mt_seven_ash_breach_hold`
- `mt_seven_ash_inner_streets`
- `mt_seven_ash_churchyard_stand`

### Campaign Slots

Suggested quest slots:

```md
slot_quest_target_center = Ashwick or current focus site
slot_quest_target_party = Wulfred host or scout party
slot_quest_target_troop = active defender or witness
slot_quest_object_troop = Wulfred / lieutenant / village witness
slot_quest_target_amount = days remaining or pressure bucket
slot_quest_sod_runtime_progress = current stage progress
slot_quest_sod_runtime_metadata = packed readiness or ending grade
slot_quest_sod_chain_choice = primary method
slot_quest_sod_chain_ending = ending flag
```

Suggested globals:

```md
$g_seven_ash_days_remaining
$g_seven_ash_wulfred_pressure
$g_seven_ash_settlement_strain
$g_seven_ash_morale
$g_seven_ash_food
$g_seven_ash_fortification
$g_seven_ash_training
$g_seven_ash_intelligence
$g_seven_ash_civilian_safety
$g_seven_ash_recruited_bitmask
$g_seven_ash_survival_bitmask
$g_seven_ash_companion_unlock_bitmask
$g_seven_ash_companion_refusal_bitmask
$g_seven_ash_final_plan
$g_seven_ash_result_grade
```

### Bitmask Allocation

Defender bits:

- `1`: Garric
- `2`: Oswin
- `4`: Aldrik
- `8`: Mirelle
- `16`: Tomas
- `32`: Beren
- `64`: Elianor

This allows compact checks:

- all seven recruited: bitmask `127`
- at least three recruited: count bits >= 3
- key pair: `(bitmask & 9) == 9` for Garric + Mirelle
- companion unlocks use the same bit values as recruitment and survival
- a defender can be recruited and survived without setting their companion unlock bit
- companion refusal bit marks a survivor who explicitly declines because their personal condition was violated

### First Vertical Slice

Recommended first implementation slice:

1. `qst_seven_ash_ultimatum`
2. `qst_seven_ash_village_audit`
3. Garric recruitment
4. Oswin recruitment
5. one pressure interlude
6. Act II return to Ashwick scene
7. oath council
8. simplified palisade defense
9. aftermath with three endings

This slice proves:

- timed pressure works
- village readiness fields work
- defender recruitment state works
- menus route to dialogue instead of resolving moral decisions directly
- at least one social witness matters
- at least one mission changes ending
- aftermath reads method and casualties

### Later Milestones

#### Phase 1: Spine

- Add campaign globals and quest IDs.
- Add ultimatum, audit, and basic clock.
- Add Wulfred pressure interlude.
- Add simplified final defense.

#### Phase 2: First Defenders

- Add Garric, Oswin, and Tomas.
- Add bow training, fieldworks, and militia training readiness.
- Add palisade defense mission.

#### Phase 3: Social and Moral Defenders

- Add Aldrik, Mirelle, and Elianor.
- Add oath, spy, evacuation, and sanctuary mechanics.
- Add defender conflict scenes.

#### Phase 4: Breach and Shock

- Add Beren and Halvorn.
- Add breach mission.
- Add controlled counterattack routes.

#### Phase 5: Full Siege

- Add outer fields, palisade, breach, inner streets, churchyard stand.
- Add Wulfred's lieutenants.
- Add combined defense tactics.

#### Phase 6: Endings and Persistence

- Add all ending flags.
- Add surviving defender aftermath.
- Add permanent Ashwick consequences.
- Add Wulfred escaped revenge hook.

## Dialogue Tone Guide

### Wulfred's Host

- practical threats
- contempt for noble hypocrisy
- logistics-minded cruelty
- never random cackling

Example:

> "I know how much grain a village hides after harvest. I know how many sons a widow can spare before she stops praying for kings. Do not insult me with poor lies."

### Ashwick Villagers

- specific fears
- food, children, doors, wells, livestock
- resentment if treated like pieces on a board

Example:

> "You say abandon the outer farms. My father is buried there. My winter hay is there. My roof beams are there. Tell me what part of my life you mean by outer."

### Defenders

Each defender should sound like their craft:

- Garric: sightlines, range, patience, bitter precision.
- Oswin: wood, earth, measures, failure points.
- Aldrik: oath, shame, public duty, restraint.
- Mirelle: doors, lies, secrets, exits.
- Tomas: watches, ranks, orders, panic.
- Beren: strength, insult, hunger, direct violence.
- Elianor: water, wounds, names, shelter.

## Dialogue Craft Checklist

Use this checklist for every authored dialogue file, recruitment scene, pressure interlude, oath council exchange, and aftermath companion offer.

### Scene Purpose

- The scene has a clear dramatic job: recruit, refuse, reveal, test, argue, reconcile, threaten, mourn, or commit.
- The scene changes at least one state, relationship, promise, clue, pressure value, or player understanding.
- The scene starts from a visible situation, not abstract exposition.
- The player knows who is speaking, where they are, and what is at stake.
- The scene would still make emotional sense if the menu text were removed.

### Character Voice

- Every named speaker has vocabulary tied to their craft, wound, class, and current fear.
- No two defenders could swap the same line without it feeling wrong.
- Villagers talk about concrete things: doors, hay, sons, wells, debts, roofs, bread, animals, cellars, names.
- Wulfred's people sound organized and practical, not randomly evil.
- Emotional lines are grounded in material stakes rather than speeches about themes.
- Characters rarely explain themselves perfectly on the first line; they reveal through objection, deflection, bargaining, or detail.

### Player Choice Writing

- Important choices are written as spoken lines, not labels.
- Each player line implies a tone: honest, lawful, pragmatic, cruel, evasive, generous, proud, fearful, or ruthless.
- At least one option lets the player ask a question before committing.
- At least one option lets the player refuse without sounding like a menu cancel button.
- Hard choices have believable advantages, not fake "bad option" framing.
- Ruthless choices should be tempting because they solve a real problem quickly.
- Merciful choices should cost something concrete.
- Honorable choices should sometimes create tactical risk.
- Pragmatic choices should sometimes disappoint idealists.

### Choice Consequences

- Every major dialogue choice maps to a clear flag, score, or later callback.
- Trust, debt, pride, fear, village bond, method flags, and companion unlock conditions are updated close to the line that earns them.
- A named character should react immediately when a choice violates their values.
- The quest log records the outcome after the conversation, not before.
- Later scenes should reference at least some earlier choices in specific language.
- Companion unlock or refusal logic should be traceable to spoken promises and visible outcomes.

### Recruitment Dialogues

- The recruit is not waiting to be collected; they are busy with a personal problem when found.
- A witness, rival, victim, or local authority complicates the recruit's own version of events.
- The player can learn why the recruit is useful before negotiating.
- The player can learn why the recruit is difficult before committing.
- Best, hard, ruthless, and refusal routes are all expressed through dialogue.
- The recruit's acceptance line should name exactly what convinced them.
- The recruit's refusal line should hurt a little and still sound like that recruit.

### Pressure Interludes

- The interlude begins with a physical problem in Ashwick: fire, hunger, missing people, marked doors, frightened animals, broken tools, blocked roads.
- The player hears at least two local perspectives before deciding.
- A recruited defender can reframe the problem in their own voice.
- The choice is about triage, not abstract morality.
- The result changes Ashwick visibly or changes how the next siege phase starts.

### Oath Council

- Every recruited defender should have a meaningful line if their expertise applies.
- Missing defenders should be felt through silence, weaker options, or villagers asking where they are.
- The council should feel like people arguing over a map, not a strategy menu with portraits.
- The final plan is confirmed after dialogue has exposed costs, objections, and likely casualties.
- Each plan should have at least one defender who supports it and one character who fears its cost.

### Siege Dialogue

- Battle dialogue is short, urgent, and tied to physical conditions.
- Characters call out visible events: smoke, gate strain, ditch failure, lost children, collapsing carts, shield gaps, exhausted archers.
- Defender barks should reflect their role and bond state.
- If a defender dies, flees, or is wounded, the moment should be acknowledged by someone who had reason to care.
- The player should receive tactical information through shouted observations, not detached system prose where possible.

### Aftermath and Companion Offers

- Every surviving defender gets a private or semi-private aftermath conversation.
- The defender names one thing the player did that mattered to them.
- If the defender can join, the offer feels like a personal decision, not a reward unlock.
- If the defender refuses, the refusal names the violated value or unfinished duty.
- Staying in Ashwick should feel honorable, not a consolation prize.
- Joining the player should not erase the defender's bond to Ashwick; it should explain why they can leave.
- Dead defenders receive memorial language specific to their craft and relationships.

### Polish Pass

- Remove generic medieval filler such as "my lord, as you wish, very well" unless the character would actually say it.
- Replace abstract stakes with concrete nouns.
- Cut repeated exposition once a fact has been established.
- Prefer one strong image over three explanatory sentences.
- Avoid modern therapy phrasing, slogan lines, and villain monologues.
- Keep most spoken lines short enough to feel speakable in a Warband dialogue box.
- Use pauses sparingly; do not make every character theatrical.
- Check that player choices are not all the same tone with different rewards.
- Check that the same choice wording is not reused across defenders.
- Read each scene aloud once. If it sounds like a menu pretending to be dialogue, rewrite it.

### Per-Defender Craft Tests

- **Garric:** at least one line notices range, cover, sightline, or wasted lives.
- **Oswin:** at least one line notices material, measurement, failure point, or preventable collapse.
- **Aldrik:** at least one line weighs oath, witness, restraint, or public duty.
- **Mirelle:** at least one line notices exits, secrets, lies, or what frightened people actually do.
- **Tomas:** at least one line distinguishes discipline from cruelty.
- **Beren:** at least one line shows force being given a boundary.
- **Elianor:** at least one line names water, wounds, shelter, refugees, or mercy under pressure.

## Journal Text Samples

### Opening

`@Wulfred Carr, the Ash Captain, has marked Ashwick for tribute: coin, grain, and hostages in one hundred days. The village cannot pay and cannot stand as it is. Inspect Ashwick's stores, walls, roads, and people before choosing how it will answer.`

### Recruitment

`@Ashwick needs more than swords. Seek defenders who can train, build, scout, heal, command, and hold. Each journey spends time Wulfred will use.`

### Pressure

`@Wulfred's scouts are testing Ashwick's outer farms. Answer the pressure or let the village learn fear without you.`

### Oath Council

`@The defenders and village witnesses are gathered in Ashwick's church. Choose what the settlement will defend first: walls, homes, civilians, Wulfred's head, or the road out.`

### Siege

`@Wulfred's host has reached Ashwick. The outer fields, palisade, breach, inner streets, and churchyard will each test different parts of your preparation.`

### Aftermath

`@Ashwick has survived, fallen, or changed beyond its old name. Speak the cost aloud and decide what remains after the ash cools.`

## QA Checklist

- Ultimatum cannot fire twice.
- Campaign can proceed through preparation-only, recruitment, bargain, and evacuation routes.
- Days remaining changes after travel and preparation.
- Wulfred pressure changes visible interlude behavior.
- Wulfred host size scales from player field strength and clamps to a readable range.
- A player army of 50-85 troops produces a host large enough to remain a settlement-defense campaign, not a small bandit fight.
- Siege phases use sector commitment and waves rather than spawning every troop in one field battle.
- Settlement strain can create internal problems without hard-breaking the campaign.
- Each defender can be recruited, refused, alienated, or lost.
- Each defender has at least one witness or test before recruitment.
- Recruitment methods affect trust/debt/fear/pride.
- Recruitment methods are chosen through dialogue with named characters, not menu-only moral pivots.
- Quest logs summarize testimony, promises, and outcomes after scenes rather than replacing scenes.
- Menus mostly handle navigation, broad logistics, confirmations, and transitions.
- Dialogue scenes pass the Dialogue Craft Checklist before implementation is considered complete.
- Each major dialogue has a clear dramatic job, concrete stakes, and at least one later state or memory effect.
- Each defender's dialogue includes craft-specific voice and cannot be swapped cleanly with another defender.
- Companion offer/refusal lines are personally grounded in the defender's unique values and witnessed player choices.
- Oath council reads recruited defenders and village readiness.
- Final siege can start early if pressure reaches maximum.
- Final siege can resolve with Wulfred killed, captured, escaped, bargained, or victorious.
- Civilian survival is tracked separately from settlement structural survival.
- Defender survival is tracked separately from campaign victory.
- Defender companion unlocks require unique personal conditions, not survival alone.
- Each surviving defender has aftermath dialogue that can join, stay in Ashwick, part respectfully, or refuse with a character-specific reason.
- Companion unlock and refusal bitmasks use the same seven defender bit allocation as recruitment/survival.
- Endings store compact flags.
- All seven defenders are described, equipped, and staged as sword-trained combatants.
- All seven defender troop templates include a two-handed sword sidearm unless a special scene intentionally removes weapons.
- Sword training does not erase distinct role checks: archer, engineer, knight, infiltrator, sergeant, shock fighter, healer-organizer.
- No route depends on fantasy elements, magic, monsters, undead, demons, nonhuman races, or supernatural items.

## Summary

`The Seven Oaths of Ash` is a grounded medieval defense campaign about whether a threatened settlement can become more than prey before an organized raider host arrives.

The design should not make seven defenders into mythic superheroes. All seven know a sword, but their value is practical:

- one reads sightlines before steel is drawn
- one reads earth and timber before the gate is hit
- one lends public oath and formal sword discipline
- one knows secrets, exits, and close-quarters blades
- one trains fear into formation and swords into reserve weapons
- one holds the breach when the first weapon fails
- one keeps the wounded and displaced alive, sword ready only when sanctuary is threatened

The player wins by choosing what kind of defense Ashwick becomes. A lawful stand, a common militia, a hidden trap, a hard bargain, a costly evacuation, a bloody revenge, or a remembered village where frightened people learned to hold together.

The central question:

**When an army comes for a village, what is worth saving first: the walls, the homes, the people, the law, the truth, or the name that will be spoken afterward?**
