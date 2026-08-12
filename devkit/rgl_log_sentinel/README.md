# RGL Log Sentinel

`rgl_log_sentinel/` is the runtime half of the SoD Modern diagnostics stack.
It reads a Mount & Blade 1.011 `rgl_log.txt`, groups related engine failures,
maps named scripts and numeric engine opcodes to canonical source/generated/export evidence, and can
compare the workspace `_export/` set with an explicitly supplied live module.
It is deterministic and entirely read-only.

## LLM-first use

Use the MCP tools when available:

- `rgl_log_analyze` for one gameplay log plus an optional live module path.
- `rgl_log_contract` before a build or release to check protected engine
  callback party-handle guards.

The analyzer identifies invalid-party to invalid-faction cascades as one root
failure.  It reports the current callback-contract state separately from the
historical gameplay log, so an old deployed export cannot be mistaken for a
source regression that is already fixed.

## CLI

```powershell
py -3 -B devkit\rgl_log_sentinel\rgl_log_sentinel.py analyze `
  --log "D:\Program Files (x86)\Steam\steamapps\common\Mount and Blade\rgl_log.txt" `
  --live-module "D:\Program Files (x86)\Steam\steamapps\common\Mount and Blade\Modules\Sword of Damocles - V5.0" `
  --format markdown

py -3 -B devkit\rgl_log_sentinel\rgl_log_sentinel.py contract
.\devkit\SoDDev.bat rgl contract
```

`analyze` returns a non-zero exit code whenever the log contains a script
error, the engine callback contract is broken, or the supplied live module is
stale.  That makes it useful in a test-session handoff or CI-style wrapper
without pretending it can replace actual gameplay testing.

## Current protected contract

`game_event_simulate_battle` receives engine-owned dynamic party parameters.
Before any party or faction read, both roots must pass `party_is_active`; a
failed gate must end the stale simulation through `set_trigger_result`.  The
same contract is checked by the strict Release Gate and the normal builder
Doctor.

## Boundaries

- The tool never changes a save, source file, generated module, export, or
  live module directory.
- A missing-material warning can identify an asset problem, but the sentinel
  will not edit a binary `.brf` asset.
- RGL traces show reported engine operations, not a full native-engine replay.
