# Constants

`src/constants/` is now the source of truth for `compile/module_constants.py`.

## Layout

- `module_constants.py`: current authored constants source
- `_order_constants.txt`: canonical merge order for constants modules
- `INDEX_SLOTS.md`: slot-allocation notes and maintenance guidance

## Duplicate Slot Tracking

The build runs `build/verify_slot_allocations.py` before writing `compile/module_constants.py`.

It reports:

- duplicate slot values within the same owner group such as `slot_troop_`, `slot_party_`, `slot_faction_`
- slot names whose values cannot be statically evaluated
- reserved-band conflicts if we add protected ranges later

Report output:

- `docs/reports/slot_allocation_report.txt`

## Editing Rules

- Edit only files under `src/constants/`
- Do not hand-edit `compile/module_constants.py`
- Keep new constants grouped by system and documented with comments
- When adding new slot ranges, check the slot report after a build
