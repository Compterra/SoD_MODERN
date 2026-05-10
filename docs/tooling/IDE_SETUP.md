# sod_modern IDE Setup Guide

This document explains how to work on `sod_modern` in modern IDEs without
fighting the classic Mount & Blade module system.

It is written for this repo as it exists now:

- modular authoring lives in `src/`
- generated module-system Python lives in `compile/`
- runtime `.txt` exports go to `_export/`
- the root build entrypoint is `build_module.bat`

## 1. Open The Right Folder

Open this folder as the project root:

`D:\Program Files (x86)\Steam\steamapps\common\Mount and Blade\Modules\_WORK-MB\sod_modern`

Do not open `compile/` by itself as the project root. The modular workflow
expects the whole repo layout.

## 2. Know Which Files Are Authoritative

Edit these:

- `src/scripts/`
- `src/triggers/`
- `src/menus/`
- `src/dialogs/`
- `src/presentations/`
- `src/mission_templates/`
- `build/`
- `docs/edit/`

Treat these as generated or compiler-side support:

- `compile/module_scripts.py`
- `compile/module_simple_triggers.py`
- `compile/module_game_menus.py`
- `compile/module_dialogs.py`
- `compile/module_presentations.py`
- `compile/module_mission_templates.py`
- `compile/ids/`
- `_export/*.txt`

In normal work, `src/` is the source of truth for the modularized systems.

## 3. Project Layout

`src/`
- The modular authoring tree. This is where new gameplay edits should go.

`build/`
- The modular builders, Doctor validation, and console helpers.

`compile/`
- The classic Python module system environment.
- Builders regenerate the modularized `compile/module_*.py` files here.
- The original `process_*.py` pipeline reads from here and exports text files.

`_export/`
- The final `.txt` files used by the game/module.

`docs/edit/`
- Doctor allowlists and other human-maintained build metadata.

`docs/reports/`
- Generated reports like `doctor_report.txt` and dialog-head duplicates.

## 4. The Preamble Files

Each modularized domain has a `_preamble/` folder:

- `src/scripts/_preamble/`
- `src/triggers/_preamble/`
- `src/menus/_preamble/`
- `src/dialogs/_preamble/`
- `src/presentations/_preamble/`
- `src/mission_templates/_preamble/`

What the preamble does:

- keeps shared imports at the top of a generated module
- defines helper functions or shared setup that multiple fragments rely on
- preserves old module-system context that should appear before the fragment list

How to think about it:

- normal gameplay content belongs in regular fragment files under `src/...`
- shared boilerplate and import context belongs in `_preamble/`
- builders stitch the `_preamble/` content ahead of the fragment list when they
  regenerate `compile/module_*.py`

Edit preamble files carefully:

- they are real source files, not generated files
- a bad import or helper change in `_preamble/` can affect an entire modular
  system at once

Do not duplicate preamble logic across many fragments unless there is a good
reason. If something is truly shared by a whole modular domain, `_preamble/` is
usually the right place for it.

## 5. Build Flow

The build is intentionally two-stage:

1. `src/` fragments are merged into `compile/module_*.py`
2. the old `compile/process/process_*.py` pipeline exports runtime `.txt` files

Run the full build from the repo root:

```bat
build_module.bat
```

Force a clean modular rebuild:

```bat
build_module.bat --no-cache
```

What happens during the build:

- Doctor validates `src/`
- builders regenerate modularized `compile/module_*.py`
- the classic process pipeline runs
- `.txt` outputs land in `_export/`

## 6. Python And Environment

The build wrapper currently resolves Python like this:

- prefer `py -3` when available
- otherwise fall back to `python`

The batch wrapper also sets this `PYTHONPATH` before running builders and
compiler scripts:

```text
compile
compile\headers
compile\ids
compile\process
```

If you run builder scripts directly inside an IDE terminal, set the working
directory to the repo root so imports behave the same way they do in
`build_module.bat`.

## 7. Sixth Checkpoints For This Repo

Sixth checkpoints are automatic and do not require any compiler-side setup in
this repository.

What this repo does require is a checkpoint-friendly workflow:

- treat each file edit and build step as a restore point
- prefer small, reviewable edits instead of broad blind rewrites
- review diffs after builder, ordering, preamble, or other structural changes
- if a change breaks Doctor output, generated merge output, or `_export/`
  results, restore to the last known-good checkpoint instead of hand-untangling
  unrelated fallout

Recommended restore choices in this repo:

- **Restore Workspace Only**
  - use when generated/code changes are wrong but the task direction is still correct
- **Restore Task and Workspace**
  - use when both the code state and the conversation direction should rewind
- **Restore Task Only**
  - use when you want to keep the current files but retry with a different prompt strategy

Project-local Sixth guidance for this workflow lives in:

- `.sixthrules/01-workflow-and-checkpoints.md`

## 8. VS Code / Cursor Setup

VS Code and Cursor can use the same setup.

Recommended workspace root:

- open the repo root, not `src/` or `compile/` alone

Recommended interpreter:

- use a Python 3 interpreter that can run `py -3` compatible code

Suggested first actions:

1. Open Command Palette
2. Run `Python: Select Interpreter`
3. Choose your Python 3 interpreter
4. Open an integrated terminal at the repo root
5. Run `build_module.bat --no-cache` once

Recommended folders to pin in the explorer:

- `src/`
- `build/`
- `compile/`
- `_export/`
- `docs/`

Useful search habits:

- search in `src/` first
- use `compile/module_*.py` only to inspect generated output
- use `_export/*.txt` only when verifying final compiler output

Good VS Code/Cursor tabs to keep open:

- `build_module.bat`
- `build/build_all.py`
- `build/doctor.py`
- the specific fragment file you are editing
- `docs/reports/doctor_report.txt`

## 9. PyCharm Setup

PyCharm works well for this repo if you treat it as a plain Python project with
custom build steps.

Recommended setup:

1. Open the repo root as the project
2. Configure a Python 3 interpreter
3. Mark nothing under `_export/` as source
4. Keep `src/`, `build/`, and `compile/` visible

Recommended run configurations:

Full build:

- Script or batch file: `build_module.bat`
- Working directory: repo root

Doctor only:

- Script path: `build/doctor.py`
- Working directory: repo root

Builder only:

- Script path: `build/build_all.py`
- Working directory: repo root

If you run Python scripts directly instead of the batch file, make sure the
working directory is the repo root.

## 10. How The Module Is Structured

This project is layered on purpose:

`src/`
- human-authored modular source
- the first place you should look and edit

`build/`
- merge logic, ordering logic, validation, and build utilities

`compile/`
- the classic Mount & Blade compiler environment
- receives generated `module_*.py` output from the builders
- still contains legacy non-modular module-system files for systems that have
  not been modularized

`_export/`
- final game-facing text output

The practical rule is:

- edit `src/` when changing modularized gameplay content
- edit `build/` when changing generation or validation behavior
- inspect `compile/` to debug generated output
- inspect `_export/` to verify final compiler output

## 11. What To Edit For Common Tasks

Add or change a script:

- edit `src/scripts/...`

Add or change a simple trigger:

- edit `src/triggers/...`
- keep `src/triggers/_order_simple_triggers.txt` consistent if needed

Add or change a dialog:

- edit `src/dialogs/...`
- keep `src/dialogs/_order_dialogs.txt` consistent

Add or change a menu:

- edit `src/menus/...`

Change builder behavior or validation:

- edit files under `build/`

Suppress intentional legacy Doctor noise:

- edit allowlists under `docs/edit/`

Do not hand-edit exported runtime text:

- `_export/*.txt`

Do not treat generated modular compiler files as your primary edit target:

- `compile/module_*.py`

## 12. Files You Should Not Edit

These are generated or compiler-output files and should normally be treated as
read-only:

- `compile/module_scripts.py`
- `compile/module_simple_triggers.py`
- `compile/module_game_menus.py`
- `compile/module_dialogs.py`
- `compile/module_presentations.py`
- `compile/module_mission_templates.py`
- `compile/ids/ID_*.py`
- `_export/*.txt`
- `docs/reports/*.txt`

Why not to edit them:

- builders overwrite generated `compile/module_*.py`
- the process pipeline rewrites `compile/ids/` and `_export/*.txt`
- report files are generated diagnostics, not source

If you think you need to edit one of those files directly, stop and trace it
back first:

1. find the source fragment in `src/`
2. or find the builder/validation rule in `build/`
3. regenerate instead of hand-patching generated output

The main exception is older non-modular systems that still only live in
`compile/`. For those, the compiler-side file may still be the real source.
When in doubt, check whether the file is one of the modularized `module_*.py`
targets listed above.

## 13. Ordered Modular Files

This repo keeps some modular sets in explicit order.

Important order files:

- `src/menus/_order_game_menus.txt`
- `src/dialogs/_order_dialogs.txt`
- `src/triggers/_order_simple_triggers.txt`
- `src/presentations/_order_presentations.txt`
- `src/mission_templates/_order_mission_templates.txt`
- `src/scripts/ZA_hardcoded_game_scripts/_order_za_scripts.txt`

Why this matters:

- menu order should be kept explicit and stable
- dialog order can affect conversation flow
- trigger order can affect behavior timing
- presentation order should be kept explicit and stable
- mission template order should be kept explicit and stable
- hardcoded-style `game_*` script order is kept stable on purpose

If you add a new file to one of these strict buckets, update the matching order
file in the same change.

## 14. Best Daily Workflow

Use this loop:

1. Edit fragments in `src/`
2. Run `build_module.bat --no-cache`
3. Check `docs/reports/doctor_report.txt`
4. Inspect generated `compile/module_*.py` only if you need to confirm merge order
5. Inspect `_export/*.txt` only if you need final compiler verification

This keeps the modular tree authoritative and avoids drifting back into editing
generated files.

## 15. Check The Report Logs

Always check the report logs after meaningful build or structure changes.

Main reports:

- `docs/reports/doctor_report.txt`
- `docs/reports/dialog_head_duplicates.txt`

What they are for:

- `doctor_report.txt` is the main health report for the modular source tree
- `dialog_head_duplicates.txt` is a reference/debugging report for repeated
  dialog head signatures

When to check them:

- after adding or moving fragment files
- after changing order manifests
- after changing builders or Doctor rules
- after fixing a broken build
- before considering a structural refactor "done"

Treat `docs/reports/` as generated diagnostics:

- read them often
- do not hand-edit them
- let the build regenerate them

## 16. Reading Build Output

You will usually see three kinds of output:

Doctor output:

- validates structure, ordering, duplicates, references, and allowlisted legacy
  cases

Builder output:

- reports which `compile/module_*.py` files were regenerated

Process pipeline output:

- old module-system exporter messages
- these may still include some legacy warnings unrelated to the modular layer

Current expected status:

- Doctor should be clean by default
- the process pipeline may still report a few legacy unused-variable warnings

## 17. Debugging Problems

If Doctor fails:

- open `docs/reports/doctor_report.txt`
- fix missing exports, order issues, or duplicate IDs first

If a builder fails:

- inspect the fragment named in the traceback
- then inspect the generated `compile/module_*.py` only if needed

If the process pipeline fails:

- the problem may be in a modular fragment or in older non-modular compiler data
- confirm whether the failure happened before or after `compile/module_*.py`
  generation finished

If text files are missing:

- check `compile/module_info.py`
- confirm `export_dir` points at `_export/`
- rerun `build_module.bat --no-cache`

## 18. Search And Navigation Tips

When tracking gameplay behavior:

- search `src/` first
- if the behavior is not in a modularized system, then search `compile/`

When tracking an exported artifact:

- start from the fragment in `src/`
- then inspect the generated `compile/module_*.py`
- then inspect the final `_export/*.txt`

When working on dialogs:

- use `docs/reports/dialog_head_duplicates.txt` as a reference, not as a bug list

## 19. Team Rules For This Repo

Follow these rules to keep the project healthy:

- prefer editing `src/`, not generated files
- keep ordered manifests updated
- keep Doctor noise intentional through `docs/edit/`
- do not move final `.txt` files back to the repo root
- use `build_module.bat` as the default build entrypoint

## 20. Quick Start Checklist

For a fresh IDE session:

1. Open the repo root
2. Select a Python 3 interpreter
3. Open `src/`, `build/`, `compile/`, and `_export/`
4. Run `build_module.bat --no-cache`
5. Check `docs/reports/doctor_report.txt`
6. Start editing `src/`

That is the safe modern workflow for this original Mount & Blade project.
