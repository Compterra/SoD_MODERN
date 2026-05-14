# Faith System Audit

## Purpose

The faith system is SoD's realm belief, clergy legitimacy, and faith-elite access layer. It ties the player's chosen creed to local settlement support, clergy happiness, religious buildings, global faith pressure, and the ascension of homeland nobles into faith-order troops.

As implemented, faith is not a single score. It is a layered system:

- player creed selection;
- per-center support for all five faiths;
- local faith tension and institution strength;
- clergy happiness and realm legitimacy;
- global faith and holy burden;
- faith troop ascension gates.

The system is functional and more nuanced than some older UI/building descriptions imply. The main current caveat is presentation drift: a few older descriptions still make buildings sound like direct global-faith generators, while newer code mostly routes faith growth through local support, population-weighted support, clergy state, events, and camp actions.

## Primary Files

- `src/scripts/ZY_helper_scripts/sod_faith_system.py`
  - Core center support, weekly drift, population-weighted faith gain, and realm profile logic.
- `src/constants/module_constants.py`
  - Faith ids, faith support slots, tension constants, ascension thresholds, and faith-related center modifiers.
- `src/scripts/ZY_helper_scripts/sod_troop_get_faith_upgrade.py`
  - Maps eligible noble troops to faith-order upgrade troops.
- `src/scripts/ZY_helper_scripts/sod_troop_can_faith_ascend_at_center.py`
  - Checks whether a faith upgrade is currently legal at a center.
- `src/scripts/ZY_helper_scripts/sod_troop_get_effective_faith.py`
  - Converts raw global faith into effective faith by subtracting holy burden.
- `src/scripts/ZY_helper_scripts/sod_troop_apply_faith_ascension_cost.py`
  - Adds holy burden after faith ascension.
- `src/triggers/ST04_weekly/entry_0132_five_faith_drift.py`
  - Weekly center drift, population faith gain, and realm profile refresh.
- `src/triggers/ST04_weekly/entry_0089.py`
  - Temple weekly faith effects.
- `src/triggers/ST04_weekly/entry_0090.py`
  - Shrine and chapel weekly faith effects.
- `src/triggers/ST04_weekly/entry_0091.py`
  - Monastery weekly faith effects.
- `src/triggers/ST04_weekly/entry_0131.py`
  - Global clergy happiness and global faith modifier application.
- `src/triggers/ST03_daily/entry_0109.py`
  - Daily faith ascension event chance.

## Faith Identities

The player chooses one faith during character creation. The chosen faith is stored in `$g_sod_faith`.

Current faith identities:

| Faith | Internal constant | Notes |
| --- | --- | --- |
| The One | `cb_the_one` | Monotheistic/order faith. |
| Old Gods | `cb_old_gods` | Ancestor, tradition, and old cult identity. |
| The Void | `cb_the_void` | Void/abyssal doctrine. |
| Enlightenment | `cb_enlightenment` | Rational or reformist doctrine. |
| Natural Philosophy | `cb_atheism` | Internal legacy name is still `atheism`; player-facing framing is philosophical/skeptical. |

Vanilla factions also have preferred faiths:

| Faction | Preferred faith |
| --- | --- |
| `fac_kingdom_1` | The One |
| `fac_kingdom_2` | Old Gods |
| `fac_kingdom_3` | The Void |
| `fac_kingdom_4` | Enlightenment |
| `fac_kingdom_5` | Natural Philosophy |
| `fac_kingdom_6` | The One |
| `fac_player_supporters_faction` | Player's chosen faith |

## Center Faith Support

Each center can track support for all five faiths. Support values are clamped from `0` to `100`.

Support slots:

| Slot | Meaning |
| --- | --- |
| `slot_center_sod_faith_1_support` | Faith 1 support. |
| `slot_center_sod_faith_2_support` | Faith 2 support. |
| `slot_center_sod_faith_3_support` | Faith 3 support. |
| `slot_center_sod_faith_4_support` | Faith 4 support. |
| `slot_center_sod_faith_5_support` | Faith 5 support. |

Initialization is migration-safe through `slot_center_sod_faith_migrated`.

When a center is initialized:

- the owner's preferred faith receives the strongest support;
- legacy local faith contributes to the initial owner-faith value;
- minority faiths receive baseline support;
- a few secondary faith pockets are seeded for variety;
- the center faith profile is recalculated.

There is also a legacy slot, `slot_center_sod_local_faith`. The modern system keeps it alive for compatibility by mirroring relevant player-faith support where needed. Future work should treat the five-faith support profile as the real model and the legacy slot as a compatibility bridge.

## Center Faith Profile

`script_sod_get_center_faith_profile` returns the current faith state for a center.

Returned registers:

| Register | Meaning |
| --- | --- |
| `reg0` | Dominant faith. |
| `reg1` | Dominant faith support. |
| `reg2` | Player-faith support. |
| `reg3` | Faith tension. |
| `reg4` | Institution strength. |
| `reg5` | Stability effect. |
| `reg6` | Recovery effect. |
| `reg7` | Unrest pressure. |
| `reg8` | Ascension readiness. |

Faith tension is derived from the gap between the top faith and the second strongest faith:

```text
faith tension = second support - dominant support + 50
```

The value is clamped from `0` to `100`.

Lower tension means one faith is clearly dominant. Higher tension means the center is divided.

Institution strength comes from faith buildings and faith stability modifiers:

| Source | Institution contribution |
| --- | ---: |
| Temple | +35 |
| Chapel | +25 |
| Monastery | +30 |
| Shrine | +15 |
| `sod_center_modifier_faith_stability_flat` | added directly |

Institution strength is clamped from `0` to `100`.

Profile effects:

- strong institutions improve stability and recovery;
- high tension increases unrest pressure;
- clergy happiness can improve or worsen the profile;
- mismatch between dominant faith and player faith adds unrest pressure;
- ascension readiness rises with player-faith support and institution strength, and falls with tension.

## Weekly Faith Drift

Every week, `entry_0132_five_faith_drift.py` applies faith drift to all centers.

The drift generally pushes a center toward the owner's preferred faith.

Drift increases when:

- institution strength is at least `25`;
- institution strength is at least `50`.

Drift decreases when:

- effective security threat is high;
- unrest pressure is high;
- food security is poor.

The final drift is clamped from `-2` to `4`.

If a center's faith tension is above `sod_faith_tension_soft_cap`, a rival faith may also gain support. This keeps divided centers from feeling instantly solved by ownership alone.

## Population-Weighted Global Faith Gain

`script_sod_apply_weekly_population_faith_gain` calculates a hidden weekly global-faith gain from the player's realm.

The script:

- requires a valid `$g_sod_faith`;
- scans player-supporter centers;
- reads each center's population;
- reads player-faith support and total faith support;
- estimates the population that supports the player's faith;
- converts that population into global faith gain.

Large, stable, player-faith centers matter more than small or divided centers.

The weekly gain is clamped from `0` to `25`.

This is one reason older building descriptions can be misleading. A shrine or temple helps by strengthening local support and institutions, which can then improve population-weighted faith gain, but the newer model is not simply "building gives global faith every week."

## Global Faith, Holy Burden, And Effective Faith

Raw global faith is stored in `$g_sod_global_faith`.

It is clamped from `-2000` to `2000`.

Effective faith is calculated as:

```text
holy burden = $g_sod_holy * 10
effective faith = $g_sod_global_faith - holy burden
```

This means the player can have high raw global faith but still lack enough effective faith if too many faith ascensions have recently been used.

Each faith ascension adds holy burden:

```text
holy cost = ascended troop count * sod_faith_ascension_holy_cost
```

Current ascension cost:

```text
sod_faith_ascension_holy_cost = 20
```

The design effect is good: faith elites consume spiritual/political capital, and the realm needs time and support to rebuild that capital.

## Clergy Happiness And Legitimacy

Clergy happiness is stored in `$g_sod_clergy_happines`.

Weekly clergy and global faith modifiers are applied in `entry_0131.py`.

When clergy happiness is negative, global faith suffers additional penalties. When it is positive, global faith receives bonuses.

Realm faith profile calculates:

- dominant realm faith;
- player-faith coverage;
- average realm faith tension;
- clergy legitimacy.

Clergy legitimacy is based mostly on realm tension, with a bonus if the dominant realm faith matches the player's faith and a penalty if it does not.

This gives faith a political dimension: a realm can be militarily controlled but religiously unstable.

## Faith Buildings

Faith buildings currently matter through local support, institution strength, recovery, unrest control, and ascension access.

| Building | Settlement type | Current role |
| --- | --- | --- |
| Shrine | Village | Local faith support, modest institution strength, unrest reduction, retention. |
| Monastery | Village | Stronger local faith institution, recovery, administration, population support. |
| Temple | Town | Major faith institution, strong local support, unrest reduction, law compliance. |
| Chapel | Castle | Castle faith institution, faith ascension access, garrison/recovery support. |

Important implementation note:

- temples and chapels are hard gates for faith troop ascension;
- shrines and monasteries are more about local support, stability, and recovery;
- building descriptions still mention direct global-faith growth in some places, but the newer implementation leans more on local support and population-weighted global gain.

## Faith Troop Ascension

Faith ascension is the highest troop doctrine layer.

Eligible homeland noble troops can become faith-order troops based on the player's chosen faith.

The mapping is handled by `script_sod_troop_get_faith_upgrade`.

Faith ascension requires:

- an eligible faith-tier upgrade;
- the player faith to be valid;
- enough effective faith;
- a valid player-aligned center when center context is used;
- temple or chapel support at the center;
- enough local player-faith support;
- institution strength of at least `20`;
- faith tension not higher than `sod_faith_tension_soft_cap + 10`.

Key thresholds:

| Constant | Value | Meaning |
| --- | ---: | --- |
| `sod_zealot_min_faith` | 100 | Minimum effective faith for ascension access. |
| `sod_faith_ascension_local_min` | 35 | Minimum local faith support for center-based ascension. |
| `sod_faith_tension_soft_cap` | 60 | Tension benchmark used by drift and ascension checks. |

The daily faith event trigger can also fire if:

- the player is not a prisoner;
- a valid faith candidate exists;
- effective faith meets the minimum;
- the player owns at least one religious seat with a temple or chapel.

More religious seats and recruitment-policy ascension bonuses improve the event chance.

## Reports And Player-Facing Surfaces

Faith data appears in several places:

- normal report strings;
- elite doctrine report;
- faith world report;
- center recon notes;
- upgrade continuation text;
- holy event menus.

The deeper faith world report is cheat/debug gated. It explains:

- chosen faith;
- raw faith;
- holy burden;
- effective faith;
- dominant realm faith;
- player-faith coverage;
- realm tension;
- clergy legitimacy;
- religious seats;
- ascension-ready centers;
- strained centers;
- best ascension seat.

Center recon notes also expose local faith details:

- dominant local faith;
- player-faith support;
- tension;
- institution strength;
- faith unrest.

## Current Strengths

- Faith has both local and realm-wide meaning.
- Conquest does not instantly erase local religious identity.
- Buildings act as institutions, not just flat income generators.
- Faith troop ascension has multiple meaningful gates.
- Holy burden prevents faith elites from being produced endlessly.
- Clergy happiness makes religious politics matter.
- The system already integrates with settlement security, food, unrest, population, recovery, and recruitment policy.

## Current Quirks And Risks

- Some text still implies direct building-to-global-faith income, even though newer code mostly uses local support and population-weighted gain.
- `slot_center_sod_local_faith` still exists beside the modern five-faith support profile. This is useful for compatibility but can confuse future work.
- Natural Philosophy still uses the internal constant `cb_atheism`.
- Some older comments say castles do not track faith, but chapel/castle faith now matters in several places.
- The deepest faith report is cheat gated, so normal players may not understand why ascension is blocked.
- Faith tension and institution strength are mechanically important, but not always surfaced clearly at the moment the player needs the information.

## Recommended Future Polish

- Update building descriptions so they explain local support, institution strength, and population-weighted global faith more accurately.
- Add a normal, non-cheat faith summary report once the system is stable.
- Make faith ascension failure text more specific:
  - low effective faith;
  - no chapel or temple;
  - weak local player-faith support;
  - local faith tension too high;
  - institution strength too low.
- Continue treating the five-faith support profile as canonical.
- Keep the legacy local faith slot only as a compatibility mirror.
- Consider displaying holy burden as "recent holy strain" or similar player-facing language.
- Add a small weekly note when a center's faith tension is dangerously high and affecting unrest or ascension.

## As-Is Summary

The faith system is a settlement, realm, clergy, and elite-troop access system.

The player chooses one creed. Centers develop support for all five creeds. Religious buildings strengthen local institutions. Security, food, unrest, and clergy happiness affect how faith spreads. Population-weighted support produces global faith. Global faith is reduced by holy burden to produce effective faith. Effective faith, local player-faith support, temple or chapel access, institution strength, and low tension are required for faith elite ascension.

The system is already strong mechanically. Its main weakness is clarity: the code has grown into a nuanced faith-and-institution model, while some player-facing text still describes an older, flatter version.
