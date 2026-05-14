# Mercenary Troop Cost And Role Audit

## Scope

This is the first-pass numeric audit recommended by `docs/MERCENARY_FACTION_BALANCE_AUDIT.md`. It focuses on the named mercenary guild troop trees, their practical battlefield roles, and their estimated weekly wage before player Leadership and mercenary-pact discounts.

The wage estimate follows the current `script_game_get_troop_wage` shape:

- base wage: `((level + 3) * (level + 3)) / 25`
- mounted troops pay the mounted surcharge
- guild noble troops pay the noble surcharge
- player Leadership and pact discounts reduce the final in-game wage after this

These values are directional audit numbers, not a promise that every edge case will display exactly this value after all campaign modifiers.

## Guild Summary

| Guild | Cheap Floor | Midline | Expensive Identity | Balance Lever |
| --- | --- | --- | --- | --- |
| Black Army | Fresh Blades | Line Keepers, Line Supporters | Raven Captains, Ironsides, Assaulters | contract heat and premium wages |
| Conquistadors | Crossbowmen, Footmen | Pikemen, Swordsmen, Rodeleros | Lancers, Tercios | supply pressure and requisition heat |
| Elephant Guard | Tribesmen | Fighters, Spearmen, Warriors | Battle Shamans, Champions | sanctuary commitments and anti-slaver priorities |
| Jotnar Clan | Armsmen | Volvas, Jarls, Shield Maidens | Norn Mistresses, Disir, Einherjar | hearth pressure and local obligation |
| Serpent Host | Kapikulu | Akinci, Cemaat, Sipahi | Basilisk Knights, Cataphracts, Timariots | route pressure, horse cost, elite scarcity |
| Slavers | Slaves, Henchmen | Drivers, Hunters, Crushers | Tormenters, Slave Masters | black-market heat and honor consequences |
| Boar Clan | Clansmen | Warriors, Riders | Tusk Riders, Veteran Riders/Warriors | tribute, intimidation, commoner hostility |

## Player-Facing Hire Slot Changes

Implemented from the balance audit:

- Elephant Guard second base slot now uses `trp_elephant_guard_spearman` instead of duplicating `trp_elephant_guard_tribesman`.
- Boar Clan second base slot now uses `trp_boar_clan_rider` instead of duplicating `trp_boar_clan_clansman`.
- Boar Clan base and noble slots now use named constants in `module_constants.py` instead of inline strings in `game_start.py`.

This keeps both guilds controlled, but their castle/pact stock now expresses their identity earlier:

- Elephant Guard offers shielded wardens plus javelin/spear defenders.
- Boar Clan offers rough infantry plus raiding riders, while Tusk Riders remain noble stock.

## Black Army

| Troop | Level | Mounted | Est. Wage | Role | Notes |
| --- | ---: | --- | ---: | --- | --- |
| Fresh Blade | 7 | no | 4 | cheap armored shield infantry | reasonable baseline |
| Line Keeper | 14 | no | 11 | shield line infantry | professional midline |
| Iron Guard | 21 | no | 23 | defensive heavy infantry | durable but weak melee proficiency tag matters |
| Ravager | 21 | no | 23 | offensive shock infantry | broad weapon list, strong assault flavor |
| Line Supporter | 13 | no | 10 | ranged support | mixed crossbow/bow support, not a pure archer |
| Assaulter | 23 | no | 27 | elite ranged assault | strong siege/support value |
| Line Crusher | 12 | yes | 15 | entry cavalry | useful but not faction-defining elite |
| Ironside | 22 | yes | 41 | heavy mounted shock | should stay limited |
| Raven Captain | 25 | yes | about 76 | noble commander | mounted, firearm-capable, should remain rare |

### Balance Call

Black Army is fair if it stays premium and heat-limited. Its danger is not one extreme troop; it is broad reliability across too many situations.

## Conquistadors

| Troop | Level | Mounted | Est. Wage | Role | Notes |
| --- | ---: | --- | ---: | --- | --- |
| Footman | 14 | no | 11 | shield infantry base | higher floor than many guild basics |
| Pikeman | 18 | no | 17 | anti-cavalry infantry | clear counter-role |
| Tercio Pikeman | 23 | no | 27 | elite anti-cavalry/siege infantry | high value in defensive fights |
| Swordsman | 18 | no | 17 | melee infantry | bridge to Rodelero |
| Rodelero | 20 | no | 21 | shield assault infantry | strong siege assault flavor |
| Crossbowman | 12 | no | 9 | ranged base | cheap and useful |
| Seasoned Crossbowman | 16 | no | 14 | ranged infantry | efficient defensive fire |
| Lancer | 25 | yes | about 76 | noble cavalry | strong but should not define bulk roster |

### Balance Call

Conquistadors are strong because the roster is disciplined and complete. Balance them through supply and requisition pressure before touching stats.

## Elephant Guard

| Troop | Level | Mounted | Est. Wage | Role | Notes |
| --- | ---: | --- | ---: | --- | --- |
| Tribesman | 10 | no | 6 | shield/spear militia warden | strong skills for level |
| Fighter | 14 | no | 11 | shield infantry | sturdy midline |
| Warrior | 18 | no | 17 | experienced melee warden | good defensive infantry |
| Champion | 22 | no | 25 | elite infantry | should remain uncommon |
| Spearman | 14 | no | 11 | javelin/spear defender | now appears as second base slot |
| Penetrator | 20 | no | 21 | elite javelin/spear troop | strong anti-armor/anti-cav flavor |
| Battle Shaman | 25 | no | about 46 | noble support/elite defender | medical skills make it more valuable than wage implies |

### Balance Call

The Elephant Guard should be strong in village defense and anti-slaver work. Their new second slot gives them visible identity without increasing noble availability.

## Jotnar Clan

| Troop | Level | Mounted | Est. Wage | Role | Notes |
| --- | ---: | --- | ---: | --- | --- |
| Armsman | 12 | no | 9 | axe infantry base | cheap hard infantry |
| Jarl | 16 | no | 14 | stronger melee infantry | stepping stone to elite |
| Einherjar | 20 | no | 21 | elite heavy infantry | control availability |
| Axe Thrower | 17 | no | 16 | throwing infantry | useful mixed pressure |
| Volva | 14 | yes | 18 | light mounted hybrid | current first base slot |
| Shield Maiden | 17 | yes | 26 | mounted hybrid | flexible but not top-tier cavalry |
| Valkyrie | 20 | yes | 35 | strong mounted hybrid | watch mass availability |
| Disir | 23 | yes | 45 | elite mounted hybrid | should be rare |
| Norn Mistress | 25 | no | about 46 | noble elite | strong support/elite identity |

### Balance Call

Jotnar are in the best shape conceptually. Their power is clean and understandable; keep them tied to hearth pressure so they cannot become unlimited export infantry.

## Serpent Host

| Troop | Level | Mounted | Est. Wage | Role | Notes |
| --- | ---: | --- | ---: | --- | --- |
| Kapikulu | 9 | no | 5 | cheap infantry base | weak floor |
| Cemaat | 12 | no | 9 | spear/bow infantry | flexible militia line |
| Athanatoi | 18 | no | 17 | elite infantry hybrid | good but not main risk |
| Akinci | 15 | yes | 20 | mobile base cavalry | first base slot, strong map value |
| Sipahi | 18 | yes | 28 | melee cavalry | strong open-field value |
| Cataphract | 23 | yes | 45 | elite heavy cavalry | should be scarce |
| Timariot | 20 | yes | 35 | horse archer | very valuable due mobility plus ranged |
| Basilisk Knight | 25 | yes | about 76 | noble horse archer | highest-risk elite access |

### Balance Call

Serpent Host should remain dangerous. Do not weaken the identity first. Keep elite supply tight, raise route-pressure consequences, and make heavy use expensive.

## Slavers

| Troop | Level | Mounted | Est. Wage | Role | Notes |
| --- | ---: | --- | ---: | --- | --- |
| Slave | 2 | no | 1 | coerced body | intentionally weak |
| Henchman | 9 | no/sometimes horse item | 5 | cheap blunt infantry | base guild slot |
| Slave Driver | 14 | no/sometimes horse item | 11 | control troop | still cheap |
| Slave Hunter | 18 | yes | 28 | mounted capture troop | strong prisoner economy value |
| Slave Crusher | 22 | yes | 41 | heavy mounted blunt troop | capture plus durability |
| Slave Master | 26 | yes | 55 | elite mounted slaver | profitable if not punished |
| Tormenter | 26 | no | about 49 | noble shock troop | high melee and trade flavor |

### Balance Call

Slavers should be balanced by heat, honor damage, and anti-slaver retaliation. Their wage alone cannot carry the moral/economic cost of prisoner capture loops.

## Boar Clan

| Troop | Level | Mounted | Est. Wage | Role | Notes |
| --- | ---: | --- | ---: | --- | --- |
| Clansman | 14 | no | 11 | rough infantry base | first base slot |
| Warrior | 17 | no | 16 | shock infantry | hammer/axe identity |
| Veteran Warrior | 23 | no | 27 | elite shock infantry | dangerous in melee |
| Rider | 18 | yes | 28 | raiding cavalry | now second base slot |
| Veteran Rider | 24 | yes | 48 | elite raiding cavalry | should remain mostly party/template stock |
| Tusk Rider | 26 | yes | about 82 | noble horse archer/shock rider | very strong, keep rare |

### Balance Call

Boar Clan’s new second slot makes them feel like a raiding faction immediately. That is good, but it means their access should remain tied to tribute, intimidation, and relationship consequences.

## Tuning Priorities After This Pass

1. Watch Serpent Host and Boar Clan mounted stock in castle guild halls.
2. Confirm Elephant Guard spearmen make pact stock feel better without making them too common.
3. Keep noble stock rare across all guilds.
4. Use guild market supply and price pressure before editing troop stats.
5. Make sure Slaver prisoner profit is always paired with visible black-market heat and anti-slaver reaction.
6. If one guild dominates AI hiring, tune kingdom demand preferences before nerfing troops.

## Current Recommendation

No broad stat rebalance yet. The immediate changes should make under-expressed guilds read better in the new pact/castle systems. The next balance decision should come after playtesting castle guild stock for several weeks of campaign time.
