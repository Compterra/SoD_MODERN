# Mercenary Faction Balance Audit

## Purpose

This audit reviews the major mercenary factions as battlefield forces and world-economy actors. The goal is not to make every guild equally shaped. The healthier target is asymmetric balance: each mercenary faction should have a clear reason to hire it, a clear reason not to rely on it for everything, and a visible world cost when its power is abused.

Sources reviewed:

- `compile/module_troops.py`
- `compile/module_party_templates.py`
- `compile/module_factions.py`
- `src/scripts/ZA_hardcoded_game_scripts/game_start.py`
- Existing mercenary economy and world-presence docs/reports

## Executive Findings

- The mercenary factions already have strong identities. The safest balance direction is to sharpen those identities instead of flattening them.
- Player-facing hire pools are narrower than world-map party templates. This is mostly good, but it means castle guild halls and pact stock may not fully express some factions.
- Elephant Guard and Boar Clan previously duplicated their two base roster slots. That made them less expressive in systems that draw only from `slot_guild_tier_1_unit_1` and `slot_guild_tier_1_unit_2`; the first balance pass now gives Elephant Guard Spearmen and Boar Clan Riders a controlled base-stock presence.
- Slavers and Boar Clan should not be balanced as ordinary honorable contract companies. Their strength should come with relation, honor, security, or economic consequences.
- Serpent Host and Conquistadors have the highest `slot_guild_troop_proportion` value at 18, Black Army has 16, and the remaining guilds have 12. If that slot represents stock weight or availability in hire systems, Serpent/Conquistador access should be watched closely because both have strong tactical niches.
- The current design wants role balance, not stat parity:
  - Black Army: reliable security company.
  - Conquistadors: disciplined expedition logistics and combined arms.
  - Elephant Guard: anti-slaver sanctuary wardens.
  - Jotnar Clan: hearth defenders and hard infantry.
  - Serpent Host: routes, scouting, mobility, and horse warfare.
  - Slavers: prisoner economy and coercive manpower.
  - Boar Clan: frontier toll bands and intimidation.

## Comparison Matrix

| Guild | Primary Combat Role | Map/Economy Role | Best At | Should Struggle With | Balance Risk |
| --- | --- | --- | --- | --- | --- |
| Black Army | Armored mixed company | Road security and contract heat | Stable field line, patrol work, anti-bandit contracts | Cheap mass recruitment, fast pursuit, elite cavalry wars | Too generically useful if cheap |
| Conquistadors | Pike/crossbow/sword combined arms | Supply contracts and requisition pressure | Sieges, anti-cavalry, disciplined infantry fire support | Low-supply campaigns, fast cavalry pursuit, moral backlash from requisition | Strong if supply costs are too mild |
| Elephant Guard | Shielded infantry and javelin/spear wardens | Sanctuary, devotion, anti-slaver response | Holding villages, protecting civilians, punishing Slavers | Strategic speed, heavy cavalry dominance, ordinary profiteering contracts | Base roster feels too narrow |
| Jotnar Clan | Heavy infantry plus mounted female line | Hearth defense and anti-slaver shelter | Defensive fighting, village protection, brutal melee | Mobility, sustained pursuit, mass missile warfare | Elite infantry can become too efficient if overavailable |
| Serpent Host | Mounted spear/bow cavalry | Route screens, intelligence, safe passage | Scouting, escort, open-field mobility, chasing raiders | Static sieges, dense infantry fights, attrition | Mounted roster can outperform map and battle roles at once |
| Slavers | Blunt-force capture chain | Black market supply/demand/heat | Capturing prisoners, cheap bodies, profit loops | Honor, loyalty, anti-slaver factions, disciplined set-piece battle | Economy can become exploitative if prisoner value is too high |
| Boar Clan | Raider infantry/camel shock force | Frontier tolls, intimidation, tribute | Raiding, rough-country pressure, short violent contracts | Diplomacy, siege discipline, commoner relations, long formal campaigns | World pressure can snowball if rewards are too soft |

## Black Army

### Current Roster Shape

- Base hire slots:
  - `trp_black_army_fresh_blade`
  - `trp_black_army_line_supporter`
  - Noble: `trp_black_army_raven_captain`
- Reinforcement pool also includes `trp_black_army_line_crusher`.
- Upgrade paths include:
  - Fresh Blade -> Line Keeper -> Iron Guard or Ravager.
  - Line Supporter -> Assaulter.
  - Line Crusher -> Ironside.
- World parties include patrols and contract columns with Iron Guards, Assaulters, Ironsides, Ravagers, and Raven Captains.

### Strengths

- Best "professional security contractor" identity.
- Good combined-arms foundation: shield infantry, ranged support, some mounted pressure.
- Should be the safest default for kingdoms that need roads cleared, patrol reinforcement, and reliable campaign bodies.
- Their report systems already support security fund, road-threat reduction, and contract heat.

### Weaknesses

- Should not be the cheapest way to solve every military problem.
- Should be less explosive than Serpent cavalry and less specialized than Conquistador pike/crossbow formations.
- If contract heat rises, overcommitment should make them expensive or slow to accept work.

### Balance Recommendation

Keep Black Army as the baseline premium guild. They should be broadly useful but priced for reliability. Avoid giving them the best version of every role. Their cavalry and ranged line should support the contract company, not replace dedicated mounted or missile factions.

### Tuning Watchpoints

- If Black Army contract columns are affordable and plentiful, kingdoms may have little reason to hire anyone else.
- Their world security benefit should be real but local, not a global bandit suppression button.
- Castle guild halls should surface their mixed roster without making Raven Captains routine.

## Conquistadors

### Current Roster Shape

- Base hire slots:
  - `trp_conquistador_footman`
  - `trp_conquistador_crossbowman`
  - Noble: `trp_conquistador_lancer`
- Upgrade paths include:
  - Footman -> Pikeman or Swordsman.
  - Pikeman -> Tercio Pikeman.
  - Swordsman -> Rodelero.
  - Crossbowman -> Seasoned Crossbowman.
- World parties include procurement columns and expeditionary camps with Lancers, Rodeleros, Tercios, and Seasoned Crossbowmen.

### Strengths

- Excellent disciplined combined-arms identity.
- Natural answer to cavalry through pikes and dense infantry.
- Strong siege and defensive value through crossbows, shields, and formation flavor.
- Economy systems already make them about supplies, requisition, rich employer demand, and campaign readiness.

### Weaknesses

- Should be vulnerable to supply disruption and political backlash.
- Should not dominate fast pursuit, open-field skirmishing, or low-cost garrison filling.
- Lancers should be useful, but not common enough to turn them into a cavalry guild.

### Balance Recommendation

Conquistadors should be powerful when paid, supplied, and deployed deliberately. Their risk should be economic and political: high wages, supply needs, and requisition heat if kingdoms or the player lean on them too hard.

### Tuning Watchpoints

- Their `slot_guild_troop_proportion` is 18, tied with Serpent Host for the highest value among guilds.
- If requisition heat is too forgiving, Conquistadors become a low-friction elite combined-arms solution.
- If castle guild halls stock too many pikes/crossbows cheaply, Rhodok-style defensive play may become too easy for all factions.

## Elephant Guard

### Current Roster Shape

- Base hire slots:
  - `trp_elephant_guard_tribesman`
  - `trp_elephant_guard_spearman`
  - Noble: `trp_elephant_guard_battle_shaman`
- Upgrade paths include:
  - Tribesman -> Fighter or Spearman.
  - Fighter -> Warrior -> Champion.
  - Spearman -> Penetrator.
- World parties include sanctuary patrols and relic processions with Battle Shamans, Champions, Warriors, Fighters, Spearmen, and Penetrators.

### Strengths

- Strong defensive and protective identity.
- Good shield, athletics, throwing, spear, and anti-slaver flavor.
- Best suited for holding threatened settlements, escorting refugees, and answering Slaver pressure.
- Their economy reports already support devotion, supplies, omens, sanctuary commitments, and slaver alarm.

### Weaknesses

- Should be less suitable for ordinary conquest-for-hire.
- Should have limited strategic speed and limited cavalry projection.
- Should refuse or price up contracts that conflict with sanctuary identity.

### Balance Recommendation

Keep the Elephant Guard narrow but meaningful. They should be excellent defensive allies and morally distinct, not just another infantry store. The second base slot now uses `trp_elephant_guard_spearman`, giving their pact/castle stock a clearer defensive identity without making Battle Shamans common.

### Tuning Watchpoints

- Spearmen in base stock should be watched for availability, but they fit the guild's defensive role.
- Battle Shaman access should be rare and tied to strong standing or pact support.
- Their anti-slaver bonuses should not become universal combat buffs.

## Jotnar Clan

### Current Roster Shape

- Base hire slots:
  - `trp_jotnar_clan_volva`
  - `trp_jotnar_clan_armsman`
  - Noble: `trp_jotnar_clan_norn_mistress`
- Upgrade paths include:
  - Armsman -> Jarl or Axe Thrower.
  - Jarl -> Einherjar.
  - Volva -> Shield Maiden -> Valkyrie -> Disir.
- World parties include hearth guards and wintering camps with Jarls, Armsmen, Volvas, and Shield Maidens.

### Strengths

- Strongest hearth-defense fantasy.
- Excellent hard infantry and melee staying power.
- Female mounted line gives them more tactical texture than a pure infantry faction.
- Anti-slaver and village-protection systems make them feel socially grounded.

### Weaknesses

- Should be slower and less flexible than Serpent Host.
- Should not be the best cheap garrison filler if their elite infantry are easy to mass.
- Should be reluctant to leave home if hearth pressure is high.

### Balance Recommendation

Jotnar should be powerful but locally rooted. Let them be excellent for defending villages, breaking Slaver pressure, and anchoring infantry lines, while making long foreign campaigns expensive or harder to negotiate during homeland threats.

### Tuning Watchpoints

- Jarl/Einherjar availability should be controlled tightly.
- If hearth pressure recovery is too generous, their "local obligation" weakness will vanish.
- Their mounted female line should add mobility, not make them a full cavalry substitute.

## Serpent Host

### Current Roster Shape

- Base hire slots:
  - `trp_serpent_host_akinci`
  - `trp_serpent_host_kapikulu`
  - Noble: `trp_serpent_host_basilisk_knight`
- Upgrade paths include:
  - Kapikulu -> Cemaat -> Athanatoi.
  - Akinci -> Sipahi or Timariot.
  - Sipahi -> Cataphract.
- World parties include route screens and courier lances with Akincis, Timariots, Sipahis, Cataphracts, Kapikulu, and occasional Basilisk Knights.

### Strengths

- Best mobility faction.
- Strong scouting, escort, safe-passage, and route-control identity.
- Excellent open-field cavalry roster with both melee cavalry and horse archers.
- Natural foil to Black Khergit movement and Boar Clan toll pressure.

### Weaknesses

- Should be weaker in sieges and static infantry attrition than Black Army, Conquistadors, or Jotnar.
- Should care about route pressure and overused roads.
- Should have high horse-related costs and limited elite cavalry availability.

### Balance Recommendation

Serpent Host should win through movement, pursuit, and battlefield control. Their balancing cost should be availability, route state, and price, not making their troops weak. They are allowed to be scary in the open field.

### Tuning Watchpoints

- Their `slot_guild_troop_proportion` is 18, tied for highest guild availability.
- Mounted troops can overperform both map and battle systems, so contract price and route-pressure refusal matter.
- Basilisk Knights and Cataphracts should be pact/standing rewards, not casual castle stock.

## Slavers

### Current Roster Shape

- Base hire slots:
  - `trp_henchman`
  - `trp_slave`
  - Noble: `trp_tormenter`
- Upgrade paths include:
  - Slave -> Henchman -> Slave Driver -> Slave Hunter -> Slave Crusher -> Slave Master.
  - Female Slave -> Follower Woman.
- World systems include slave transports, black market demand/supply/heat, prisoner economy effects, and anti-slaver reactions.

### Strengths

- Strong capture economy through blunt weapons and mounted hunter lines.
- Can turn prisoners and coercive markets into manpower and cash.
- Useful as a morally ugly shortcut for players or factions willing to accept the consequences.
- Tormenters and Slave Masters give them dangerous late-chain shock presence.

### Weaknesses

- Should be hated, risky, and politically toxic.
- Should lose badly to organized anti-slaver pressure if exposed.
- Low-tier slaves are extremely weak and should not become efficient combat mass by accident.

### Balance Recommendation

Do not balance Slavers by making them honorable mercenaries. Balance them by making their battlefield/economic utility come with heat, honor loss, anti-slaver retaliation, and diplomacy problems. They should be tempting because they are profitable, not because they are the clean best army.

### Tuning Watchpoints

- Prisoner profit loops need close watching.
- If black-market heat is too easy to ignore, Slavers become pure upside.
- Systems should keep Slaver access distinct from normal castle guild hall stock unless intentionally allowed by pact or black-market mechanics.

## Boar Clan

### Current Roster Shape

- Base hire slots:
  - `trp_boar_clan_clansman`
  - `trp_boar_clan_rider`
  - Noble: `trp_boar_clan_tusk_rider`
- Upgrade paths include:
  - Clansman -> Warrior or Rider.
  - Warrior -> Veteran Warrior.
  - Rider -> Veteran Rider.
- World parties include Boar Clan Fighters with Tusk Riders, Warriors, Riders, Veterans, and Clansmen.
- Faction relations differ from other guilds: Boar Clan is hostile to commoners and mildly hostile to player faction by default.

### Strengths

- Strong frontier raider identity.
- Good shock value through rough melee infantry, hammers, axes, polearms, camels, and intimidation.
- Works well as a pressure system against neglected roads and border settlements.
- Tribute and intimidation already give them a different economic language from formal guilds.

### Weaknesses

- Should be poor at formal diplomacy and long clean contracts.
- Should be bad for commoner relations and frontier prosperity when unchecked.
- Should be less disciplined in sieges or professional campaign service than Black Army or Conquistadors.

### Balance Recommendation

Boar Clan should feel useful but dangerous to normalize. Paying or hiring them should solve short-term frontier problems while creating long-term reputation and intimidation costs. They should remain semi-bandit, not a seventh polite mercenary guild.

### Tuning Watchpoints

- Rider base stock makes the raider identity visible earlier; keep Tusk Riders relation-gated and uncommon.
- World pressure can snowball if toll-band activity drains villages faster than patrol/security systems can respond.
- Tusk Rider access should remain a relationship/standing reward.

## Cross-Guild Balance Principles

### Keep Asymmetry

The goal should not be "each guild has infantry, cavalry, ranged, elite, and support." That would make the system less interesting. Each guild should be balanced by role, price, supply, refusal rules, and world consequences.

### Separate Hire Pool From World Party Identity

Current world templates are often richer than the base hire slots. That is good for flavor, but it creates a balance issue when a pact/castle system draws only from base slots. For each guild, decide whether castle guild halls are meant to sell:

- basic recruits only,
- basic recruits plus one elite identity unit,
- or a wider pact roster unlocked by relation and building investment.

### Watch Base Slot Expression

The first balance pass removed the two most visible duplicate base slots:

- Elephant Guard now uses `trp_elephant_guard_tribesman` / `trp_elephant_guard_spearman`.
- Boar Clan now uses `trp_boar_clan_clansman` / `trp_boar_clan_rider`.

This is not meant to widen elite access. It is meant to make base/pact stock communicate faction identity earlier while keeping nobles and high-tier troops rare.

### Balance With Costs That Fit The Guild

- Black Army: contract heat, overcommitment, premium wages.
- Conquistadors: supply stores, requisition heat, local resentment.
- Elephant Guard: sanctuary commitments, moral refusal rules, anti-slaver priority.
- Jotnar Clan: hearth pressure, reluctance to abandon threatened villages.
- Serpent Host: route pressure, safe-passage state, horse cost, elite scarcity.
- Slavers: black-market heat, honor damage, anti-slaver retaliation.
- Boar Clan: tribute, intimidation, commoner hostility, frontier damage.

## Recommended Balance Pass

### Phase 1: Baseline Data Sheet

- Record recruit cost, weekly wage, level, equipment type, and upgrade cost for every mercenary faction troop.
- Compare each guild's practical cost per role:
  - shield infantry,
  - ranged infantry,
  - spear/anti-cavalry,
  - melee cavalry,
  - horse archer,
  - shock infantry,
  - prisoner-capture specialist.
- Mark any troop whose wage/cost does not match its battlefield role.

### Phase 2: Hire Pool Review

- Playtest Elephant Guard Spearmen and Boar Clan Riders in castle/pact stock.
- Decide whether pact castle halls should unlock second-tier stock through `script_sod_merc_guild_get_roster`.
- Ensure Slavers and Boar Clan have explicit gates if they appear in ordinary castle systems.
- Make sure noble units are rare enough to feel like pact or relationship rewards.

### Phase 3: Counterplay Review

- Black Army should be countered by cost and overcommitment.
- Conquistadors should be countered by supply and requisition heat.
- Elephant Guard should be countered by limited offensive availability.
- Jotnar should be countered by local obligation and slow projection.
- Serpent Host should be countered by siege weakness, route pressure, and price.
- Slavers should be countered by heat, honor loss, and anti-slaver factions.
- Boar Clan should be countered by diplomacy damage and frontier instability.

### Phase 4: Player Choice Review

For each guild, the player should be able to answer:

- Why would I hire them?
- What situation makes them better than vanilla mercenaries?
- What problem do they create if I lean on them too much?
- Which companion, kingdom, or campaign style naturally prefers them?

### Phase 5: AI Kingdom Fit

- Wealthy kingdoms should be drawn to Conquistadors and Black Army.
- Frontier/unstable kingdoms should be tempted by Boar Clan or Slavers, with consequences.
- Kingdoms suffering bandit pressure should value Black Army and Serpent Host.
- Kingdoms facing Slaver pressure should value Elephant Guard and Jotnar.
- Cavalry-poor kingdoms should value Serpent Host, but pay heavily for it.
- Defensive kingdoms should value Conquistadors, Jotnar, and Elephant Guard.

## Immediate Recommendations

1. Do not globally equalize the guilds.
2. Add a troop-cost data sheet before changing stats.
3. Watch the new Elephant Guard and Boar Clan base slot variety in castle guild halls before changing stats.
4. Keep Slavers and Boar Clan consequence-heavy.
5. Use contract price, stock, relation, and world pressure as the first tuning levers before editing troop stats.
6. Audit castle Mercenary Guild Hall stock after several in-game weeks with and without pacts.
7. If one faction dominates, reduce access or increase its world cost before weakening its identity.

## Balance Verdict

The mercenary factions make sense as distinct forces. They do not need to be balanced into sameness. The likely problem areas are access and consequence, not raw concept:

- Black Army and Conquistadors risk becoming default best professional hires.
- Serpent Host risks overperforming because mobility is powerful in both combat and world-map systems.
- Elephant Guard and Boar Clan should now feel more distinct in hire systems; the risk shifts to making sure their new second slots do not become too available.
- Slavers risk becoming an exploit if prisoner profit and black-market heat are not kept visible and painful.
- Jotnar are probably the cleanest current design: strong identity, clear strengths, clear home-pressure lever.

The next practical step should be a numeric troop/wage/cost audit, followed by a pact/castle stock playtest. That will show whether the problem is troop stats, price, availability, or world consequences.
