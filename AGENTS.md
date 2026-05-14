# AGENTS.md

## Project
This is a Mount & Blade 1.011 / Sword of Damocles Modern module-system project.

## Rules
- Do not assume this is Warband unless explicitly stated.
- Preserve modular folder ordering.
- Do not rename section folders casually.
- Section codes belong in folder names only, not individual fragment filenames.
- Prefer descriptive filenames.
- Never overwrite live module export files without showing a diff first.
- When debugging strings, check both strings.txt and quick_strings.txt.
- Remember: str_store_string takes a string id or quick string; use str_store_string_reg to copy s-registers.

## Build
- Use the repo's existing build script first.
- If unsure, inspect build_module.bat, build_module.py, process_*.py, and WRECK config before editing.

## Available Tools
- `rg` / ripgrep is available for fast text search.
- `fd` is installed for fast file discovery; refresh the shell PATH if a new terminal cannot see it yet.
- `lazygit` is installed for interactive git inspection when useful.
- `7z` / 7-Zip is installed for archive inspection and extraction.
- `git` is installed and registered through WinGet.

## Diagnostics
Before fixing compiler/runtime issues:
1. Search with rg / Test with pytest
2. Identify source module fragment.
3. Identify generated module_*.py output.
4. Identify exported .txt output.
5. Report exact files changed.
