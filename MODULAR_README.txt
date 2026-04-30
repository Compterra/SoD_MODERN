Modular Project bootstrap for sod_modern

This project now has a modular authoring layer modeled after:
D:\Program Files (x86)\Steam\steamapps\common\MountBlade Warband\_WORK\_Gemini_Kernal

What is modular right now
- module_scripts.py
- module_simple_triggers.py
- module_game_menus.py
- module_dialogs.py
- module_presentations.py
- module_mission_templates.py

Folder layout
- src/
  Modular source fragments you edit.
- build/
  Builders and validation scripts that regenerate compile/module_*.py.
- compile/
  The classic Mount & Blade module system compiler environment.
  - headers/
  - ids/
  - process/
  - module_*.py

Current status
- The six modularized systems are split into ordered source fragments under src/.
- Builders regenerate the matching compile/module_*.py files from those fragments.

Build
- Run build_module.bat from the project root.
- Step 1 regenerates compile/module_*.py from src/.
- Step 2 runs the original process_*.py compiler pipeline from compile/process.
- IDE setup and workflow notes live in docs/IDE_SETUP.md.

Strict order files
- src/menus/_order_game_menus.txt
- src/dialogs/_order_dialogs.txt
- src/triggers/_order_simple_triggers.txt
- src/presentations/_order_presentations.txt
- src/mission_templates/_order_mission_templates.txt
- src/scripts/ZA_hardcoded_game_scripts/_order_za_scripts.txt

Notes
- The active source of truth is src/ for modularized systems and compile/ for the classic compiler environment.
- Final runtime text exports are written to _export/.
