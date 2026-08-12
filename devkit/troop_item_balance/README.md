# Troop + Item Balance Lab

`troop_item_balance` is the LLM-first viewer, balance analyzer, and guarded
editor for SoD Modern's Mount & Blade **1.011** troop and item authoring.

The project currently keeps these two domains in legacy compile-layer authoring
lists:

- `compile/module_items.py`
- `compile/module_troops.py`

The normal build pipeline consumes them with `process_items.py` and
`process_troops.py`; it does not rebuild them from modular `src/` fragments.
The Lab calls this out explicitly, evaluates those lists in a short-lived
compatible Python process, and never mislabels a generated/export layer as a
safe authoring target.

## LLM-first workflow

Use the MCP tools where available, or deterministic JSON CLI commands:

```powershell
py -3 -B devkit/troop_item_balance/troop_item_balance.py summary
py -3 -B devkit/troop_item_balance/troop_item_balance.py items --query khergit --limit 20
py -3 -B devkit/troop_item_balance/troop_item_balance.py item itm_khergit_bow
py -3 -B devkit/troop_item_balance/troop_item_balance.py troops --faction kingdom_1 --exclude-heroes
py -3 -B devkit/troop_item_balance/troop_item_balance.py troop trp_swadian_recruit
py -3 -B devkit/troop_item_balance/troop_item_balance.py upgrade-tree trp_swadian_recruit --depth 4
py -3 -B devkit/troop_item_balance/troop_item_balance.py roster-inventory
py -3 -B devkit/troop_item_balance/troop_item_balance.py roster-inventory --roster Antarian --troop-limit 120 --item-limit 180
py -3 -B devkit/troop_item_balance/troop_item_balance.py progression --roster Antarian
py -3 -B devkit/troop_item_balance/troop_item_balance.py campaign-cohorts
py -3 -B devkit/troop_item_balance/troop_item_balance.py imperial-invasion --include-auxiliaries
py -3 -B devkit/troop_item_balance/troop_item_balance.py player-start-factions
py -3 -B devkit/troop_item_balance/troop_item_balance.py player-start-progression
py -3 -B devkit/troop_item_balance/troop_item_balance.py native-kingdoms
py -3 -B devkit/troop_item_balance/troop_item_balance.py mercenary-guilds
py -3 -B devkit/troop_item_balance/troop_item_balance.py faith-ascensions
py -3 -B devkit/troop_item_balance/troop_item_balance.py outliers --domain all
```

The Lab returns evaluated item bit-packed stats, price/score relationships,
troop equipment pools, static kit pressure, direct upgrade declarations,
faction/role distribution, source provenance, and generated-ID parity.
Scores are review aids—not combat DPS, economy simulation, or a claim about a
randomized troop loadout actually spawned in game.

## Theme-safe roster evidence

Use `roster-inventory` without a roster argument to discover the available
roster families. Supplying one exact roster name or ID then returns its direct
troop inventory pools and every equipped item, including whether that item is
local to the roster or also used outside it.

The five SoD player cultures are deliberately reported as separate roster
families even though they share `fac_player_supporters_faction` at runtime.
This makes an Antarian equipment swap visible as an Antarian-only decision
instead of silently treating Marina, Aden, Villian, and Zerrikan gear as a
single generic faction pool. Faith rosters are likewise separate.

`progression` reports a selected roster's explicit normal/noble `upgrade()`
edges, rank-by-role trajectory summaries, and the separate scripted
noble-candidate-to-faith mapping. It distinguishes three access ranks:

- `Normal`: ordinary recruitment and branch progression.
- `Noble`: a separate noble route, above normal troops.
- `Faith/Zealot`: ascended noble elites, above nobles and gated by faith,
  local support, religious institutions, tension, and holy burden.

Neither command edits source data. Their score deltas identify review points;
they never prescribe flattening faction roles, costs, or item themes.

## Campaign-Aware Evidence

`campaign-cohorts` is the companion to roster evidence. It prevents a
technically true runtime faction field from becoming a false balance claim:

- Antarian, Marinian, Adenian, Villianese, and Zerrikanian are separate,
  mutually exclusive player-start cultures. A single campaign contains the
  selected culture, not all five trees at once.
- Native kingdoms are persistent world realms. They are a separate comparison
  group from player-start cultures.
- Faith troops are a gated elite overlay attached to the selected culture's
  noble progression, not five territorial factions.
- The Imperial Expedition is a delayed endgame invasion, not a normal
  steady-state faction. Review it through wave composition, supply, pressure,
  total-war behavior, and counterplay.

`imperial-invasion` reads the three actual Imperial reinforcement templates,
optionally includes the advance auxiliary template, and shows the campaign
source contracts for activation, pressure/supply, coalition counterplay, and
the Imperial autoresolve doctrine prefix. It also calculates the source-level
pre-invasion staging upper bound from the entry-party ID range and each
`spawn_around_party`/`party_add_template` application. Its aggregates are
deliberately template references, never claims about a spawned party, a
surviving force, or a battle outcome.

`player-start-factions` is the first-castle companion report. It follows each
culture's actual runtime binding in
`activate_deactivate_player_faction.py`, then applies the center (A 65% / B
35%) and kingdom-hero (A 50% / B 25% / C 25%) selection rules from
`cf_reinforce_party.py`. Its pressure proxy is only expected stack size times
static kit score, so it deliberately allows distinct cavalry, bow, crossbow,
and foot doctrines while flagging an outsized bulk reinforcement package for
review.

`faith-ascensions` completes the player-tier view. It follows every scripted
`Noble* -> Faith` route and requires a valid rank transition, a complete
loadout, and at least one measurable elite premium in level, equipment,
combat skills, or proficiencies. It deliberately allows role-specific trades
instead of requiring every Faith troop to be a heavier version of its Noble
candidate.

`player-start-progression` checks every direct recruit, normal, and Noble
upgrade in the five player cultures. An edge must raise level, preserve rank,
retain a complete target loadout, and show at least one equipment or training
advance. When a higher tier trades raw equipment score for stronger skills or
proficiencies, the report records that as a visible themed trade for review.

`native-kingdoms` follows the actual `game_start.py` culture bindings for all
five coexisting Native A/B/C reinforcement packages, then applies the shared
center and lord selection weights. It bounds bulk campaign reinforcement
pressure without requiring an all-mounted Khergit force, a Rhodok pike line,
or a Nord shield wall to resemble each other. It also audits every direct
Native upgrade route for level, rank, training, and hard loadout regressions;
intentional role conversions remain visible as training-compensated kit
trades instead of being flattened into a universal gear score.

`mercenary-guilds` treats the seven guilds as contract specialists rather than
territorial factions. It follows the live job from kingdom demand through
guild selection, bid evaluation, accepted-contract spawn, and contract
dialogue. The accepted job is first resolved to a deployable role, so an
impossible local task becomes field service before formation; mobile escort,
mercenary-lord, and special jobs retain their live identity while following an
employer. The report verifies that AI companies express that role by
redistributing existing guild line troops without increasing the company size
or inventing a new elite tier. Player hiring previews intentionally remain
independent: their chosen composition is not rewritten from an AI job.

## Guarded balance edits

The editor is intentionally narrow rather than a generic file writer:

- Items: name, price, and values of stat constructors already present in the
  direct record (for example `weight`, `body_armor`, `spd_rtng`, or
  `swing_damage`).
- Troops: name/plural name, evaluated attributes, per-weapon proficiencies,
  skills, and inventory list.
- Derived upgrade-variant troops are view-only; their runtime records have no
  direct source record to patch.
- It never changes record order, generated IDs, `compile/ids`, `_export`, or
  source ordering manifests.

First create a plan and review its unified diff:

```powershell
py -3 -B devkit/troop_item_balance/troop_item_balance.py patch item itm_khergit_bow --changes '{"price":1234,"stats":{"weight":2.5}}'
```

Then rehearse the exact change with the returned `base_sha256` and
`plan_sha256`. A real apply additionally requires `--apply` and
`--allow-legacy-compile-authoring`; hardwired engine records require the extra
protected-record acknowledgement.

```powershell
py -3 -B devkit/troop_item_balance/troop_item_balance.py apply item itm_khergit_bow --changes '{"price":1234}' --expected-sha256 <base_sha> --expected-plan-sha256 <plan_sha>
```

After a non-dry apply, run the existing reviewed build, inspect generated
module/ID/export diffs, and smoke-test the intended shop, troop spawn,
randomized inventory, and upgrade path in game.

## Evidence boundary

The isolated evaluator uses the same local Python module/header/ID import
graph that the M&B process pipeline uses. It writes nothing, but it does
evaluate local legacy authoring expressions to avoid a fake static parser that
would misread helper functions and upgrade mutations. Treat that input graph
as part of the trusted local project source, just as the normal builder does.

`verify` proves source parse/evaluation, explicit upgrade target existence,
inventory index validity, and generated-ID parity. It deliberately does not
run a build, overwrite an export, simulate the engine, certify save
compatibility, or decide gameplay balance for you.
