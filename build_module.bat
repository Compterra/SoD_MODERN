@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
pushd "%ROOT%"

set "PY=C:\Users\Computica\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe"
if not exist "%PY%" (
  set "PY=python"
  where py >nul 2>nul && set "PY=py -3"
)

set "PYTHONPATH=%ROOT%;%ROOT%compile\ids;%ROOT%compile;%ROOT%compile\headers;%ROOT%compile\process"
set "ROOT_DISPLAY=%ROOT:~0,-1%"

if not exist "%ROOT%_export" mkdir "%ROOT%_export"

for /f "usebackq delims=" %%T in (`powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss'"`) do set "BUILD_STARTED_AT=%%T"
if not defined BUILD_STARTED_AT set "BUILD_STARTED_AT=%DATE% %TIME%"

%PY% "%ROOT%build\tools\printc.py" dim "Build started: %BUILD_STARTED_AT%"
%PY% "%ROOT%build\tools\printc.py" title "sod_modern - Build & Compile"
for /f "usebackq delims=" %%V in ("%ROOT%build\version.txt") do (
  %PY% "%ROOT%build\tools\printc.py" version "Build tools version: %%V"
  goto :ver_done
)
:ver_done
%PY% "%ROOT%build\tools\printc.py" dim "Working dir: %ROOT_DISPLAY%"

%PY% "%ROOT%build\tools\printc.py" step "1) Build fragments -> compile\\"
%PY% "%ROOT%build\tools\run_color.py" "%ROOT%build\build_all.py" -- %*
if errorlevel 1 goto fail

%PY% "%ROOT%build\tools\printc.py" step "2) Process pipeline (compile\\process\\...)"
pushd "%ROOT%compile\ids"

for %%F in (
  process_init.py
  process_global_variables.py
  process_strings.py
  process_skills.py
  process_music.py
  process_animations.py
  process_meshes.py
  process_sounds.py
  process_skins.py
  process_map_icons.py
  process_factions.py
  process_items.py
  process_scenes.py
  process_troops.py
  process_particle_sys.py
  process_scene_props.py
  process_tableau_materials.py
  process_presentations.py
  process_party_tmps.py
  process_parties.py
  process_quests.py
  process_scripts.py
  process_mission_tmps.py
  process_game_menus.py
  process_simple_triggers.py
  process_dialogs.py
  process_global_variables_unused.py
) do (
  %PY% "%ROOT%build\tools\printc.py" substep "- %%F"
  %PY% "%ROOT%build\tools\run_color.py" "%ROOT%compile\process\%%F"
  if errorlevel 1 goto fail_from_ids
)

popd
%PY% "%ROOT%build\tools\printc.py" step "3) Doctor hardcoded ID contract"
%PY% "%ROOT%build\tools\run_color.py" "%ROOT%build\doctor.py" -- --doctor-hardcoded-postprocess
if errorlevel 1 goto fail

%PY% "%ROOT%build\tools\printc.py" ok "Build finished successfully."
goto end

:fail_from_ids
popd

:fail
%PY% "%ROOT%build\tools\printc.py" error "Build failed."

:end
popd
endlocal
