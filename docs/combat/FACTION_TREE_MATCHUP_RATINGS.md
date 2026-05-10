# Faction Tree Matchup Ratings

This audit rates the five player-selectable SoD homeland troop trees against the vanilla Calradian kingdoms they are expected to fight during normal play.

Player homeland trees:

- Antarian
- Marinian
- Adenian
- Villianese
- Zerrikanian

Vanilla opponent trees:

- Swadia
- Vaegirs
- Khergits
- Nords
- Rhodoks

Kingdom 6 / IEF is intentionally excluded from this audit. The Imperial Expeditionary Force is an endgame special case and should be rated in its own invasion-readiness audit.

This is a design-facing rating pass, not a battle simulator. Ratings are based on the current SoD troop definitions in `compile/module_troops.py`, Strategy Advisor doctrine descriptions, and practical Warband battlefield behavior.

## Rating Scale

| Rating | Meaning |
| --- | --- |
| `+2` | Strong advantage for the player homeland tree |
| `+1` | Slight advantage for the player homeland tree |
| `0` | Even or highly terrain-dependent |
| `-1` | Slight disadvantage for the player homeland tree |
| `-2` | Severe disadvantage for the player homeland tree |

The main matrix assumes mixed open-field lord battles. Siege and defensive context is handled separately because some trees flip hard depending on terrain.

## Homeland Identity Summary

| Homeland | Core Identity | Best Fight | Worst Fight |
| --- | --- | --- | --- |
| Antarian | Heavy shock infantry with javelin support and modest cavalry | Closing into melee, rough ground, infantry grind | Long missile exposure, horse-archer kiting |
| Marinian | Shielded crossbows, spears, and disciplined infantry | Defensive line, siege defense, anti-cavalry stand | Fast pursuit, scattered open-field chase |
| Adenian | Cavalry-first army with adequate infantry and archers | Open-field charge, pursuit, breaking missile lines | Sieges, dense spear/crossbow defenses |
| Villianese | Elite longbow army with fast light-medium infantry | Open shooting ground, castle defense, attrition | Heavy cavalry contact, shielded crossbow advance |
| Zerrikanian | Mobile combined-arms cavalry, horse archery, blunt/capture pressure | Harassment, pursuit, flexible field fights | Dense shielded infantry or spear/crossbow anchors |

## Vanilla Opponent Summary

| Vanilla Faction | Core Threat | How They Test The Player Tree |
| --- | --- | --- |
| Swadia | Balanced army with strong knights and serviceable infantry/crossbows | Tests whether the player tree can handle heavy cavalry without losing to combined arms |
| Vaegirs | Strong archers, flexible infantry, acceptable cavalry | Tests missile resistance and ability to disrupt ranged lines |
| Khergits | Mounted mobility, horse archers, skirmish cavalry | Tests pursuit, discipline, shields, and anti-cavalry control |
| Nords | Heavy infantry, axes, shields, and brutal close combat | Tests melee staying power and ability to thin infantry before contact |
| Rhodoks | Spear infantry, pavises, crossbows, and castle defense | Tests cavalry restraint, shield pressure, and siege patience |

## Open-Field Matchup Matrix

Rows are the player's homeland tree. Columns are the vanilla opponent. Positive ratings mean the player's homeland tree is favored in normal open-field battles.

| Player Homeland vs Vanilla | Swadia | Vaegirs | Khergits | Nords | Rhodoks |
| --- | ---: | ---: | ---: | ---: | ---: |
| Antarian | `0` | `+1` | `-1` | `0` | `+1` |
| Marinian | `+1` | `0` | `0` | `+1` | `0` |
| Adenian | `0` | `+1` | `+1` | `+1` | `-1` |
| Villianese | `0` | `+1` | `-1` | `+1` | `0` |
| Zerrikanian | `0` | `0` | `+1` | `0` | `-1` |

## Siege And Defensive Context

Positive ratings mean the player homeland improves substantially in sieges, village defense, bridge-like terrain, or other tight defensive fights. Negative ratings mean the homeland loses an important part of its field identity.

| Player Homeland | Defensive Context Rating | Why |
| --- | ---: | --- |
| Antarian | `+1` | Heavy infantry becomes scarier when enemies are funneled, but limited sustained missile fire can hurt long defenses. |
| Marinian | `+2` | Pavises, crossbows, spears, and disciplined infantry make Marinians one of the best defensive trees. |
| Adenian | `-1` | Cavalry dominance is suppressed. Their infantry and archers are serviceable, not defining. |
| Villianese | `+2` | Longbows and noble archers become terrifying on walls or high ground if protected from immediate melee. |
| Zerrikanian | `0` | Elite individual troops help, but much of the tree's value is mobile cavalry and horse archery. |

## Role Ratings

Scale: `0` absent, `1` weak, `3` usable, `5` faction-defining.

| Homeland | Melee Infantry | Ranged Infantry | Melee Cavalry | Ranged Cavalry | Noble Line | Flexibility |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Antarian | `5` | `2` | `2` | `0` | `5` | `2` |
| Marinian | `4` | `5` | `1` | `0` | `5` | `3` |
| Adenian | `3` | `2` | `5` | `0` | `5` | `3` |
| Villianese | `3` | `5` | `1` | `1` | `5` | `3` |
| Zerrikanian | `3` | `3` | `4` | `5` | `5` | `5` |

## Homeland Vs Vanilla Notes

### Antarian

Antarians are strongest when they can force a melee decision. Their heavy infantry and Honor Guards let them meet Nord infantry and Rhodok spear lines without being embarrassed, while javelinmen can soften shielded targets before contact.

| Opponent | Rating | Notes |
| --- | ---: | --- |
| Swadia | `0` | Swadian knights threaten Antarian infantry in open ground, but Antarian heavy infantry can win once cavalry is slowed or dehorsed. |
| Vaegirs | `+1` | Vaegir archers hurt, but Antarian armor and shock infantry should win if they close with reasonable cohesion. |
| Khergits | `-1` | Khergit mobility attacks Antaria's weak point. Antarians need terrain, compact movement, and patience. |
| Nords | `0` | This is a direct infantry contest. Antarians have heavier shock tools; Nords have shields, axes, and density. |
| Rhodoks | `+1` | Antarian infantry can beat Rhodoks if it survives the crossbow approach, but reckless uphill or siege attacks are costly. |

Design concern:

- Antarians should not be helpless against Khergits, but they should clearly feel uncomfortable chasing horse archers.

### Marinian

Marinians are the safest player faction against vanilla because their crossbow/spear doctrine answers many common threats. They should feel especially good against cavalry-heavy Swadian armies and Nord infantry pushes, but less dominant when forced to chase.

| Opponent | Rating | Notes |
| --- | ---: | --- |
| Swadia | `+1` | Spears, shields, and crossbows give Marinians a good answer to knights. Bad positioning still lets Swadia break them. |
| Vaegirs | `0` | Vaegir archers and Marinian crossbows trade differently. Terrain and shield use should decide this. |
| Khergits | `0` | Marinians can punish committed cavalry but may struggle to force contact against mobile horse archers. |
| Nords | `+1` | Crossbows soften Nord infantry before the melee grind. Marinian infantry is disciplined enough to hold. |
| Rhodoks | `0` | Similar defensive doctrines. Marinians have stronger homeland identity; Rhodoks are stubborn and excellent in sieges. |

Design concern:

- If crossbows get stronger under an RCM-style pass, Marinians may become too universally safe unless reload, cost, or availability is watched.

### Adenian

Adenians are the most straightforward answer to many vanilla field armies: hit hard, ride down missile troops, and use pursuit to keep enemies from resetting. Their main problem is any opponent that turns the fight into a spear/crossbow wall or siege slog.

| Opponent | Rating | Notes |
| --- | ---: | --- |
| Swadia | `0` | This is the cavalry mirror. Adenians should compete with Swadian knights but not erase them. |
| Vaegirs | `+1` | Adenian cavalry can reach Vaegir archers before they decide the battle, assuming the player manages the charge well. |
| Khergits | `+1` | Adenians have the cavalry tools to catch and punish Khergits better than most homeland trees. |
| Nords | `+1` | Open ground favors cavalry against Nord infantry. Bad charges into dense shields and axes still hurt. |
| Rhodoks | `-1` | Rhodok spears and crossbows are a natural cavalry check, especially on hills or in sieges. |

Design concern:

- If couched lance damage is reduced, Adenian cavalry needs enough melee durability and horse quality to keep the faction distinct.

### Villianese

Villianese are excellent when they get time and space. Their longbow line can punish Vaegirs and Nords before contact, and they become dangerous defenders. Their problems are cavalry disruption and shielded crossbow attrition.

| Opponent | Rating | Notes |
| --- | ---: | --- |
| Swadia | `0` | Villianese can kill knights on approach, but if Swadian cavalry reaches the line the battle can swing quickly. |
| Vaegirs | `+1` | Villianese should win the archer-quality contest if terrain is fair and infantry screens hold. |
| Khergits | `-1` | Khergit mobility disrupts static foot archers and forces awkward target selection. |
| Nords | `+1` | Longbows punish Nord infantry before the axe wall arrives. If Nords reach the line intact, danger spikes. |
| Rhodoks | `0` | Rhodok pavises and crossbows blunt the longbow advantage. Terrain and siege geometry matter enormously. |

Design concern:

- Any RCM-inspired missile pass must keep elite Villianese archers frightening. Their whole identity depends on that pressure.

### Zerrikanian

Zerrikanians are the most flexible homeland tree. They can skirmish, pursue, capture, harass, and fight with mixed cavalry. They are not the cleanest at static line warfare, but they can make vanilla armies fight badly.

| Opponent | Rating | Notes |
| --- | ---: | --- |
| Swadia | `0` | Swadia's balanced cavalry and infantry prevent easy kiting. Zerrikanians can win through disruption, not brute force. |
| Vaegirs | `0` | Zerrikanian mobility pressures Vaegir archers, but Vaegir missile quality and infantry can punish mistakes. |
| Khergits | `+1` | Zerrikanians can meet Khergits in their own language while bringing stronger hybrid cavalry and noble tools. |
| Nords | `0` | Zerrikanians can harass Nord infantry, but a direct melee commitment into Nord axes is dangerous. |
| Rhodoks | `-1` | Rhodok spear/crossbow discipline is a poor matchup for mobile mixed cavalry if the Rhodoks hold formation. |

Design concern:

- Zerrikanian balance depends heavily on horse-archer AI and throwing weapon tuning. Too weak feels chaotic; too strong becomes impossible to pin down.

## Key Player-Facing Matchups

### Best Beginner Homeland

Marinian is probably the most forgiving into vanilla Calradia. Crossbows, shields, spears, and solid infantry give the player answers to Swadian cavalry, Nord infantry, and Rhodok defenses without requiring perfect cavalry micro.

### Best Open-Field Homeland

Adenian is the cleanest open-field power pick. It handles Vaegirs, Khergits, and Nords well, but Rhodok wars and siege-heavy campaigns should feel more awkward.

### Best Siege Homeland

Marinian and Villianese both rate highly, but for different reasons. Marinians are safer and more shielded. Villianese are deadlier if protected and positioned well.

### Most Skill-Dependent Homeland

Zerrikanian. The tree has tools for almost everything, but it needs movement, timing, and restraint. It should reward an active commander more than a static line commander.

### Most Terrain-Dependent Homeland

Antarian. In rough ground, villages, forests, and sieges, Antarian infantry becomes terrifying. In wide open steppe against Khergits, the same army can feel painfully heavy.

## RCM-Inspired Combat Tuning Risks

If we add an RCM-inspired combat profile, preserve these matchup identities:

- Antarians should gain from stronger armor, but not become immune to Rhodok/Marinian bolts or Khergit harassment.
- Marinians should remain the best anti-cavalry defensive homeland, but crossbows must not make them dominant in every fight.
- Adenians should still beat loose missile armies in open terrain even if couch damage is toned down.
- Villianese longbows must still punish infantry before contact, especially Nords and Antarians.
- Zerrikanians must remain disruptive against Khergits and Vaegirs without becoming untouchable.
- Rhodoks should remain the main vanilla check on Adenian and Zerrikanian cavalry.
- Khergits should remain the main vanilla check on Antarian and Villianese static doctrines.

## Needed Follow-Up Audit

- [ ] Generate a numeric troop-stat table for each homeland troop.
- [ ] Generate a compact vanilla troop-role table for Swadia, Vaegirs, Khergits, Nords, and Rhodoks.
- [ ] Add item armor/damage summaries for each homeland branch.
- [ ] Compare noble and faith elites separately from normal homeland trees.
- [ ] Add mini-faction matchup notes for Black Army, Conquistadors, Elephant Guard, Jotnar, Serpent Host, Slavers, and Boar Clan.
- [ ] Create a separate IEF / Kingdom 6 invasion-readiness audit.
- [ ] Re-rate after any RCM-style `module.ini` or item damage pass.
- [ ] Add Strategy Advisor dialogue summaries for homeland-vs-vanilla matchup advice.
