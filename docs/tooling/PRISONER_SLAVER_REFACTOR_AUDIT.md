# Prisoner And Slaver Refactor Audit

## Scope

This audit covers the three campaign-performance targets introduced for non-hero captives:

1. Daily prisoner-train processing.
2. Prisoner-train destination pressure scoring.
3. Slaver black-market state refreshes.

The goal is to reduce repeated map-party and center work without allowing cached data to alter campaign outcomes.

## Evidence Reviewed

- Source: `src/scripts/ZY_helper_scripts/sod_prisoner_economy.py`.
- Source: `src/scripts/ZY_helper_scripts/sod_slavers_black_market.py`.
- Shared party lifecycle sources that can create, remove, or convert Slaver activity parties.
- Generated targets: `compile/module_scripts.py` and `compile/ids/ID_scripts.py`.
- Live export target: `_export/scripts.txt`; it is not changed by source-only work or validation builds.

## Findings And Resolution

| Target | Audit finding | Implementation |
| --- | --- | --- |
| Daily prisoner trains | The previous snapshot counted every party, then the processor scanned every party again to process the same trains. | `script_sod_process_prisoner_trains` now uses `pt_prisoner_train_party` as a cheap no-train gate and rebuilds faction train counts during its single active-train scan. |
| Post-processing train caps | Train arrivals and disbands occur inside that scan, so a pre-processing count would make later creation gates overly restrictive. | The existing disband helper decrements the rebuilt faction count, and the snapshot runs after train processing; creation and patrol gates therefore observe the current map state. |
| Faction train caps | A forming train transferred to a new owner could leave active-train counts on the previous faction. | The transfer branch now moves the active-train count with the party before later creation checks. |
| Pressure cache initialization | On campaign day zero, a default `last_update_day` of `0` could be mistaken for a valid profile and produce a zero capacity. | Cached reads now require a positive update day; otherwise they recalculate the profile. |
| Holding-policy changes | Changing a local holding policy did not refresh stored unrest and escape pressure. | The local-policy setter now recalculates pressure immediately. |
| Slaver refresh accuracy | The market refresh counted any party slot, including inactive/removed party records. | The full refresh now requires `party_is_active`. |
| Slaver cache initialization | A day-zero cache timestamp is also the default uninitialized value, which would either return empty market slots or force unnecessary repeated refreshes. | Explicit cache and delta initialization flags distinguish a fresh campaign from a valid day-zero cache entry. |
| Slaver cache invalidation | A Slaver transport removed through battle, noncombat resolution, sanity cleanup, or party conversion could remain in the daily cache. | A party-aware dirty helper is called before shared removal/conversion paths, while Slaver world activity continues to dirty the cache on its own spawn and arrival paths. |
| Slaver market value writers | Prisoner arrivals, incidents, diplomacy, companion effects, and world-presence systems wrote cached supply, demand, or heat directly. A later dirty refresh could discard an otherwise valid same-day effect. | `script_sod_slavers_apply_market_delta` is now the sole mutation path. It records applied daily supply/demand deltas before changing live values; refreshes rebuild the expensive baseline and then reapply those deltas. Heat remains persistent in its faction slot. |

## Compatibility Rules

- `script_sod_count_active_prisoner_trains_to_regs` remains available as the full reconciliation helper.
- Existing train creation, disbanding, policy, destination, and player menu entrypoints retain their names and parameters.
- Weekly prisoner pressure still forces a live recalculation before applying escape or unrest outcomes.
- Cached Slaver reads retain the existing public `script_sod_slavers_update_market_state` entrypoint.

## Regression Coverage

`build/test_prisoner_economy_static.py` now verifies:

- one guarded active-train scan rather than a daily count-then-scan pair;
- post-processing arrival/disband count reconciliation before creation gates;
- train-count transfer between factions;
- safe first-day pressure-cache fallback;
- pressure refresh after a local holding-policy change;
- active-party filtering in Slaver refreshes; and
- centralized cache-aware Slaver market mutations, including a guard against new direct writers; and
- dirty invalidation for generic Slaver party lifecycle changes.

## Remaining Manual QA

- Load a new day-zero campaign and form or reroute a prisoner train.
- Transfer a forming train by changing the origin center owner.
- Destroy a Slaver transport in battle and inspect the black-market report without advancing a day.
- Complete a noncombat Slaver target and confirm the active transport count drops immediately.
- Verify high-volume prisoner campaigns do not show a map-tick slowdown.
