# Presentation Layout Composer

Presentation Layout Composer makes M&B 1.011 presentation operation code
inspectable as a static layout model. It follows direct trigger operations in
order: `create_*_overlay`, `position_set_x/y`, `overlay_set_position`,
`overlay_set_size`, `overlay_set_text`, `overlay_set_color`, and
`overlay_set_alpha`.

The result is intended for Codex/LLM reasoning first, not as a replacement for
engine rendering. Dynamic branches, loops, register-derived coordinates, text
metrics, and resolution behavior are reported as unresolved instead of being
silently guessed.

## MCP workflow

1. `presentation_find` returns presentation keys and stable `overlay:...`
   IDs.
2. `presentation_canvas` returns a bounded static canvas, source bindings,
   estimated overlap/offscreen/control findings, and all dynamic boundaries.
3. `presentation_patch` produces a semantic source-only diff and SHA-256.
4. `presentation_apply(..., dry_run=true)` rehearses through the shared Change
   Router gate; set `dry_run=false` only after reviewing the plan.
5. `presentation_verify` combines static canvas findings with syntax,
   freshness, narrow test, and optional isolated build evidence.

`presentation_preview` is an optional convenience. It writes only a confined
SVG artifact beneath `devkit/output/`; it never writes source, generated
modules, or exports.

Supported edits are `move_overlay`, `resize_overlay`, `align_overlay`,
`set_text`, `set_mesh`, `set_color`, `set_alpha`, `add_overlay`,
`remove_overlay`, `add_trigger`, `remove_trigger`, and
`replace_trigger_operations`. Trigger actions accept structured `new_trigger`
or a validated operation-list expression, so a presentation event is edited as
an engine operation block rather than free-form text.

When one `position_set_*` expression is reused by multiple overlays, the plan
lists every static consumer under `semantic_operation.shared_binding_impact`.
This prevents a seemingly local move from hiding a group layout change.

## Canvas model

The canvas uses the conventional nominal 0..1000 presentation grid with a
bottom-left engine origin. SVG y is inverted. Overlay scale is an approximate
diagnostic rectangle, not an engine-pixel promise; the canvas calls this out
in every result. `overlay_limit` bounds model output, while SVG previews use a
separately bounded full diagnostic pass.

## JSON CLI

```powershell
py -3 devkit\presentation_layout\presentation_layout.py find sliders
py -3 devkit\presentation_layout\presentation_layout.py canvas sliders --overlay-limit 80
py -3 devkit\presentation_layout\presentation_layout.py preview sliders --output-name sliders.svg
py -3 devkit\presentation_layout\presentation_layout.py patch "overlay:src/presentations/...:L5:C8" move_overlay --x 610 --y 210
```

The MCP interface is preferred for structured `new_overlay` objects. CLI
`apply` stays a dry run unless `--apply` and a plan SHA are both supplied.

## Test

```powershell
py -3 -B devkit\presentation_layout\test_presentation_layout.py
```
