@echo off
path=%path%;"C:\Python26"

@rem MAKE SURE YOU UPDATE module_info.py to point to the correct target folder!

@echo backing up our previous variables.txt...
if not exist "variables.txt" goto nobackup
if exist "variables backup 9.txt" del "variables backup 9.txt" > nul
if exist "variables backup 8.txt" ren "variables backup 8.txt" "variables backup 9.txt" > nul
if exist "variables backup 7.txt" ren "variables backup 7.txt" "variables backup 8.txt" > nul
if exist "variables backup 6.txt" ren "variables backup 6.txt" "variables backup 7.txt" > nul
if exist "variables backup 5.txt" ren "variables backup 5.txt" "variables backup 6.txt" > nul
if exist "variables backup 4.txt" ren "variables backup 4.txt" "variables backup 5.txt" > nul
if exist "variables backup 3.txt" ren "variables backup 3.txt" "variables backup 4.txt" > nul
if exist "variables backup 2.txt" ren "variables backup 2.txt" "variables backup 3.txt" > nul
if exist "variables backup 1.txt" ren "variables backup 1.txt" "variables backup 2.txt" > nul

@rem I want to ensure that the file time stamp is what it was, not now...
ren "variables.txt" "variables backup 1.txt" > nul
copy "variables backup 1.txt" "variables.txt" > nul

:nobackup
python process_init.py
python process_global_variables.py
python process_strings.py
python process_skills.py
python process_music.py
python process_animations.py
python process_meshes.py
python process_sounds.py
python process_skins.py
python process_map_icons.py
python process_factions.py
python process_items.py
python process_scenes.py
python process_troops.py
python process_particle_sys.py
python process_scene_props.py
python process_tableau_materials.py
python process_presentations.py
python process_party_tmps.py
python process_parties.py
python process_quests.py
python process_scripts.py
python process_mission_tmps.py
python process_game_menus.py
python process_simple_triggers.py
python process_dialogs.py
python process_global_variables_unused.py
pause press enter to continue...
@del *.pyc
