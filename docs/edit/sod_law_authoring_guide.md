# SoD Law Authoring Guide

The law system is faction-wide. The player realm uses the same backend as NPC kingdoms, while `trp_law` remains a compatibility mirror for older scripts and the current presentation layout.

## Add A Law

1. Add a stable `sod_law_*` constant in `src/constants/module_constants.py`.
2. Add or reuse the contiguous `sod_law_name_*`, `sod_law_description_*`, and `sod_law_mesh_*` assets.
3. Add category and AI behavior through the law helper scripts in `src/scripts/ZZ_common_array_processing/sod_law_framework.py`.
4. Add persistent effects in `script_sod_law_apply_effect_profile`.
5. Add conflicts or requirements in `script_sod_law_get_conflict_mask_or_pair_checks` and `script_sod_law_get_required_law_checks`.
6. Run doctor and the law tests.

## Design Rules

- Laws should be defined by persistent modifiers, not activate/deactivate inverse edits.
- Enactment and dismissal costs are separate from persistent effects.
- IDs 10, 20, and 30 are legacy category spacers and must remain non-enactable.
- Constitutional laws should be rare, mutually constrained, and strategically loud.
- NPC laws need AI tags so kingdoms can choose them without custom one-off code.

## Compatibility

Use these wrappers only for legacy callers:

- `script_law_is_active`
- `script_activate_law`
- `script_deactivate_law`

New code should call the faction-aware scripts directly.
