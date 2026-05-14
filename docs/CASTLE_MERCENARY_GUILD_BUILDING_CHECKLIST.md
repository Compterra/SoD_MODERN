# Castle Mercenary Guild Building Checklist

## Design Goal

Castles should be able to become regional mercenary hiring posts. A castle with a Mercenary Guild Hall gives its owning faction a local way to hire, replenish, and upgrade mercenary troops. Without a faction pact, the hall deals in ordinary vanilla mercenaries. With a faction pact, it acts as a contract office for that pact guild, using the existing guild market, manpower, reputation, and debt rules.

The building should make mercenary pacts visible on the map without becoming an infinite elite troop printer.

## Contract Language

- `Guild Pact`: the faction-level relationship with one mercenary guild.
- `Field Company`: an external mercenary party hired under a term.
- `Local Mercenary Pool`: troops available at a castle Mercenary Guild Hall.
- `Upgrade Service`: paid troop advancement allowed by the building and pact state.
- `Vanilla Mercenaries`: basic non-guild mercenaries available when no pact applies.

## Core Rules

- [x] Add a castle/town improvement slot for `slot_center_has_mercenary_guild_hall`, or reuse a safe existing walled-center improvement only if no slot expansion is desired.
- [x] Building is available only at castles in v1.
- [x] Optionally allow towns later, but keep first implementation castle-only.
- [x] Require `slot_center_has_blacksmith`, `slot_center_has_barracks`, or `slot_center_has_guild` as prerequisite if the current building UI supports prerequisites.
- [x] Do not require scene edits.
- [x] Do not spawn a visible guild master NPC in v1 unless the dialog surface already supports center service NPCs safely.

## Default No-Pact Behavior

- [x] If the owning faction has no `slot_faction_merc_pact`, the castle offers basic vanilla mercenary access.
- [x] Default stock should use low/mid vanilla mercenary troops:
  - Watchman
  - Caravan Guard
  - Mercenary Crossbowman
  - Mercenary Swordsman
  - Mercenary Horseman only at low count or higher prosperity
- [x] Do not offer Hired Blades as default stock unless castle prosperity/security is high.
- [x] Default stock refreshes weekly or through the existing center mercenary pool refresh.
- [x] Default stock should be limited by castle prosperity, security, and recent raids.

## Pact Behavior

- [x] If the owning faction has a guild pact, the building identifies the pact guild.
- [x] Player-owned castles use `fac_player_faction` / `fac_player_supporters_faction` pact sync.
- [x] AI-owned castles use that castle owner's `slot_faction_merc_pact`.
- [x] Pact guild stock should draw from `script_sod_merc_guild_get_roster`.
- [x] Pact guild access should respect `script_sod_merc_market_calculate_guild_supply`.
- [x] If guild supply is poor, local stock should be low or unavailable.
- [x] If the faction has missed pact payments or debt, local stock should be reduced or blocked.
- [x] If the pact ends, the castle falls back to vanilla mercenaries after current local stock is depleted or next refresh.

## Recruitment Flow

- [x] Add `script_sod_center_get_mercenary_guild_for_hall(center)`:
  - Return pact guild in `reg0`, or `0` if no pact.
  - Return `1` in `reg1` if using vanilla fallback.
- [x] Add `script_sod_center_refresh_mercenary_guild_hall_stock(center)`:
  - Validate castle.
  - Validate building exists.
  - Determine pact guild or vanilla fallback.
  - Store troop type and amount in safe center slots.
  - Avoid conflicting with tavern mercenary slots if those are town-only.
- [x] Add `script_cf_sod_center_can_hire_mercenary_hall_troops(center)`:
  - Center has building.
  - Center belongs to a valid faction.
  - Player can access center services.
  - Stock exists.
- [x] Add menu/dialog option at owned or friendly castles:
  - "Visit the mercenary guild hall."
- [x] Hiring from the hall adds troops to `p_main_party`, not an external field company.
- [x] Hiring should charge normal join cost plus a small local office premium.
- [x] Hiring should reduce local stock.
- [x] Pact guild hiring should optionally reduce guild manpower modestly.

## Upgrade Flow

- [x] Let the building provide upgrade permission for valid mercenary troops.
- [x] Default no-pact upgrade path:
  - Vanilla mercenary upgrades only.
  - No faction-guild special troops.
- [x] Pact upgrade path:
  - Allow upgrades into the pact guild's troop tree when the troop belongs to that guild or an accepted precursor.
  - Require enough guild supply/manpower for higher tiers.
  - Use existing upgrade cost logic and center modifier hooks.
- [x] Update `script_sod_troop_can_upgrade_at_center`:
  - Castles with the Mercenary Guild Hall can permit vanilla mercenary upgrades.
  - Castles with a pact can permit matching guild mercenary upgrades.
  - Wrong-pact guild troops should fail with `sod_upgrade_fail_merc_permission`.
- [x] Do not allow this building to bypass faith ascension, doctrine facility rules, or faction-specific elite locks.

## AI Use

- [x] AI factions with pact-backed castles may treat those castles as local mercenary support nodes.
- [x] First pass can be passive: building affects stock and upgrade eligibility only.
- [x] Later pass can let lords refill from nearby castle guild halls when visiting.
- [x] Do not let AI bypass guild support capacity.
- [x] Do not spawn extra external companies directly from every castle hall in v1.

## Market And Economy Integration

- [x] Add a small positive supply/market effect when a faction owns multiple Mercenary Guild Halls.
- [x] The effect should be subtle:
  - slightly faster local stock refresh;
  - slightly better field company replenishment for that faction;
  - small guild reputation benefit if paid on time.
- [x] Add a center modifier only if useful:
  - possible future modifier: `mercenary_stock_flat`;
  - possible future modifier: `mercenary_upgrade_access_flat`;
  - do not add new modifiers if direct scripts are simpler.
- [x] Building upkeep should be meaningful.
- [x] Hiring should never create free troops.
- [x] Upgrades should never become cheaper than normal training without explicit balance reason.

## Reports And Player Feedback

- [x] Castle service menu should say whether the hall is:
  - independent/local vanilla office;
  - backed by a specific guild pact;
  - blocked by debt or market shortage.
- [x] Mercenary Market report should mention castle halls if they materially affect supply.
- [x] Guild ledger should mention player-owned halls supporting that guild.
- [x] Fief report should mention local mercenary stock.
- [x] Keep menu text factual; use dialogue-style flavor only if an NPC interface is added later.

## Edge Cases

- [x] Castle changes faction while stock is present.
- [x] Faction pact changes while stock is present.
- [x] Player captures a castle with a hall from a pact-backed faction.
- [x] Castle becomes besieged.
- [x] Castle is looted/devastated by scripts or aftermath.
- [x] Guild supply hits zero.
- [x] Pact debt blocks new support.
- [x] Old saves lack the building slot.
- [x] Troops in stock belong to a deleted/invalid guild.
- [x] Player tries to upgrade wrong-guild troops at a pact-backed hall.
- [x] AI faction has a pact with a guild whose world presence is temporarily disabled.

## Exploit Controls

- [x] Prevent infinite local stock refresh by entering/leaving the castle.
- [x] Prevent hiring stock that exceeds stored amount.
- [x] Prevent free upgrade loops.
- [x] Prevent using the hall to upgrade hostile guild troops without proper pact.
- [x] Prevent guild manpower from going below zero.
- [x] Prevent local stock from bypassing global guild overextension/refusal state.
- [x] Prevent captured castles from preserving enemy pact stock forever.
- [x] Prevent the building from counting as a tavern mercenary pool.
- [x] Prevent external field companies from being created through the local troop-hire menu.

## Implementation Phases

### Phase 1: Building Definition

- [x] Add building slot/registry entry.
- [x] Add display name: `Mercenary Guild Hall`.
- [x] Add description:
  - "Maintains a contract office for local mercenaries. Without a guild pact it deals in ordinary sellswords; with a pact it can draw limited support from the faction's guild partner."
- [x] Add construction cost, duration, upkeep, and category.
- [x] Add static test for registry entry and castle availability.

### Phase 2: Stock Helpers

- [x] Implement pact/fallback selector.
- [x] Implement stock refresh helper.
- [x] Implement hiring eligibility helper.
- [x] Add default vanilla roster helper.
- [x] Add pact guild roster helper.
- [x] Add static tests for no-pact fallback and pact-guild selection.

### Phase 3: Castle Menu Surface

- [x] Add castle menu option to visit the hall.
- [x] Add stock/status presentation.
- [x] Add hire option for available stack.
- [x] Add blocked-state messages.
- [x] Add tests for menu gating.

### Phase 4: Upgrade Integration

- [x] Update center upgrade permission for Mercenary Guild Hall.
- [x] Add tests for vanilla merc upgrades with no pact.
- [x] Add tests for pact guild upgrades with matching pact.
- [x] Add tests for wrong guild blocked.

### Phase 5: Economy And Reports

- [x] Add subtle stock refresh scaling from prosperity/security.
- [x] Add optional guild supply drain for pact stock.
- [x] Add report lines.
- [x] Add doctor/static coverage for visible terminology.

### Phase 6: AI And Balance Polish

- [x] Let AI benefit from local upgrade permission if already visiting/reinforcing.
- [x] Keep AI use passive until player-facing flow is stable.
- [x] Tune stock numbers and refresh rate.
- [x] Add playtest checklist.

## Recommended V1 Scope

- Add the building.
- Add stock refresh.
- Add player hiring at castles.
- Add upgrade permission for vanilla mercenaries and matching pact guild troops.
- Add reports.
- Do not add new NPC scenes, new external company spawning, or AI lord shopping behavior yet.

## Test Plan

- [x] `py build\test_castle_mercenary_guild_static.py`
- [x] `py build\test_mercenary_market_static.py`
- [x] `py build\test_feature_audit_static.py`
- [x] `py build\doctor.py --doctor-new-only`
- [x] `py build\build_all.py`
