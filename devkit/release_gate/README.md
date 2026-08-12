# Strict Release Gate

`release_gate/` combines the project’s established static checks into one
read-only, deterministic preflight. It is intended for a release candidate
after normal authoring work—not as a replacement for a focused diagnosis.

The default run stages the full route below in a temporary directory and never
writes live `compile/` or `_export/` data:

`src/**` -> staged generated modules -> staged legacy exports -> live export comparison

It blocks on all of the following:

- source/generated/export drift across all 30 generated exports, including
  `strings.txt` and `quick_strings.txt`;
- a staged builder or processor failure, warning, or explicit error diagnostic;
- string-integrity errors or warnings not covered by the exact checked-in
  intentional-blank contract;
- dialogue-model error findings; and
- failed order/ID contracts, generated-order drift, or dialogue-order hazards.

The blank-sink contract is deliberately exact-count rather than a broad
suppression. If an approved warning disappears, increases, moves to a new
source owner, or a new warning appears, the gate blocks and asks for a review.

## CLI

```powershell
py -3 -B devkit\release_gate\release_gate.py run
py -3 -B devkit\release_gate\release_gate.py run --format markdown
.\devkit\SoDDev.bat gate run
```

JSON is the primary output. The command exits `0` only for `state: passed` and
exits `1` when any required preflight is blocked.

For a canonical live build followed by the same isolated preflight, use:

```powershell
cmd /c build_module.bat --release-gate --no-cache
```

`--release-gate` is stripped before fragment assembly, then runs only after the
ordinary build, text audit, and hardcoded-ID doctor have passed. A blocked gate
returns a non-zero build result.

## Verify

```powershell
py -3 -B devkit\release_gate\test_release_gate.py
```
