# 108 Heroes Campaign Quest Audit

## Purpose

This audit reviews `References/108` as a candidate model for making companion content feel like an actual campaign. PoP is a strong model for world-reactive quests. `108` is a strong model for hero-centered campaign structure: named character missions, map-travel conversations, in-battle dialogue overlays, custom scenes, replayable mission result handling, and long-term hero progress tracking.

Primary files reviewed:

- `References/108/108_quest_system.md`
- `References/108/108_hero_systems_overview.md`
- `References/108/108_camp_and_building_system.md`
- `References/108/Source/module_quests.py`
- `References/108/Source/module_dialogs.py`
- `References/108/Source/module_game_menus.py`
- `References/108/Source/module_scripts.py`
- `References/108/Source/module_triggers.py`
- `References/108/Source/module_mission_templates.py`
- `References/108/Source/module_presentations.py`
- `References/108/Source/module_scenes.py`

## High-Level Findings

`108` treats hero content as a campaign layer, not just isolated quests. Its most useful patterns for our companion work are:

- A main campaign journal that updates from global hero mission completion.
- A sub-quest journal for hero-specific equipment or personal progression.
- Three concurrent town random quests, generated from town/faction renown level.
- Random quests that can be assigned to a chosen hero, not only the player.
- Quest progress that can update from map party defeat or from in-battle hero actions.
- A large "own mission" framework for named hero scenarios.
- Custom mission templates with scripted dialogue beats during combat.
- Map-travel dialog sequences triggered after campaign conditions or battle wins.
- Result grading, retry, review, and delayed failure consequences.
- Camp/building systems that assign heroes to roles and make their non-party work matter.

The strongest lesson is simple: a companion quest can be a small campaign if it has a world trigger, travel conversation, scene setup, battle or mission objective, result grade, and follow-up journal entry.

## Quest And Campaign Layers

### 1. Main Campaign Journal

Relevant source:

- `module_quests.py`, `qst_main_quest_begin`
- `module_triggers.py`, initial `script_start_quest` for `qst_main_quest_begin`
- `module_scripts.py`, `script_update_main_quest`

`script_update_main_quest` rebuilds the main campaign journal from living troop and faction state. It loops factions and lords, counts completed hero missions, then writes a status block describing available missions and unlocked campaign powers.

Notable state included in the main quest update:

- Completed own mission count.
- Mind-reading cooldown.
- Extra mind-reading uses.
- Body protection unlock.
- Camp extra level.
- Special medicine count.
- Available hero missions by faction.

Design lesson: companion campaigns should have a living quest note that summarizes the arc, available next steps, and unlocked support powers. The journal should not be a dead description written once at quest start.

### 2. Sub-Quest Journal

Relevant source:

- `module_quests.py`, `qst_sub_quest_tips`
- `module_scripts.py`, `script_update_sub_quest`

`script_update_sub_quest` scans hero troops and builds a journal-like list from per-hero mission stages. It uses troop slot state to show which heroes have active personal equipment missions and which step each one is on.

Design lesson: companion content should have one high-level "Companion Campaigns" quest note or equivalent tracker. It can summarize every companion's personal arc without forcing the player to remember who needs what.

### 3. Town Random Quest Board

Relevant source:

- `module_dialogs.py`, tavernkeeper random quest flow
- `module_scripts.py`, `script_random_town_random_quest`
- `module_scripts.py`, `script_start_town_random_quest`
- `module_scripts.py`, `script_finish_town_random_quest`
- `module_scripts.py`, `script_abort_town_random_quest`

`108` gives towns three random quest slots:

- Slot range `431-438` for town random quest 1.
- Slot range `441-448` for town random quest 2.
- Slot range `451-458` for town random quest 3.

Each generated quest stores:

- Availability or status.
- Difficulty level.
- Target type.
- Required progress count.
- Reward type.
- Reward amount or item.
- Bound active quest id.
- Assigned hero.

The town quest level depends on faction renown, stored in faction slot `113`. Thresholds are:

- Level 2 at 6 renown.
- Level 3 at 20 renown.
- Level 4 at 44 renown.
- Level 5 at 80 renown.
- Cap around 130 renown.

Design lesson: companion quest availability can scale by companion trust, player renown, faction relationship, town relationship, or completed companion arcs. This gives the campaign a sense of earned escalation.

### 4. Hero-Assigned Random Quests

Relevant source:

- `module_dialogs.py`, `tavernkeeper_random_quest_choose_npc_*`
- `module_scripts.py`, `script_start_town_random_quest`
- `module_scripts.py`, `script_finish_town_random_quest`

For target types above `100`, the tavernkeeper flow asks which hero will take the quest. The candidate list is filtered to heroes currently in the main party, and further filtered by relevant hero skill, job, leadership value, or build experience.

Quest completion can reward the assigned hero directly:

- Build experience.
- Leadership experience.
- Job experience.
- Hero title progress.
- NPC battle statistics.

Design lesson: companion quests should not always reward the player. Sometimes the outcome should level a companion's craft, unlock a personal trait, improve their party role, or change how other companions see them.

### 5. Map And Battle Progress Tracking

Relevant source:

- `module_scripts.py`, `script_check_town_random_quest_process`
- `module_scripts.py`, `script_check_town_random_quest_process_in_battle`
- `module_mission_templates.py`, calls to `script_check_town_random_quest_process_in_battle`

`108` splits random quest progress into two channels:

- Map progress for party/faction/template targets.
- Battle progress for hero-specific action types.

Map targets include bandit templates, deserters, dark knights, hostile caravans, hostile patrols, active hostile parties, and similar campaign entities.

Battle targets above `100` listen for specific action codes. The exact labels are decompiled away, but the structure is clear: quest target type `101-112` maps to in-battle event values such as kills, defeats, job actions, leadership actions, or similar hero contributions.

Design lesson: companion quests should advance from the companion's actual behavior. If Bunduk is proving discipline, count shield-wall survival or infantry kills. If Jeremus is proving triage, count wounded saved or post-battle recovery. If Deshavi is scouting, count ambush avoidance or trail discoveries.

## Own Mission Campaign Framework

### 1. Scale And Structure

Relevant source:

- `References/108/README.md`
- `module_game_menus.py`, `mnu_108_heroes_own_mission_result`
- `module_scripts.py`, `script_ini_own_lord_mission`
- `module_scripts.py`, `script_lord_mission_program_effect`
- `module_mission_templates.py`, named `108_heroes_*_mission` templates
- `module_scenes.py`, named `108_heroes_*_mission` scenes

The documentation reports `$108_heroes_own_mission_total_num = 67`. Source confirms a broad framework around `$missioning_lord` and many named mission templates/scenes.

Examples of named mission templates found:

- `mt_108_heroes_han_tao_mission`
- `mt_108_heroes_zhang_qing_mission`
- `mt_108_heroes_daizong_mission`
- `mt_108_heroes_zhu_tong_mission`
- `mt_108_heroes_li_zhong_mission`
- `mt_108_heroes_du_xing_mission`
- `mt_108_heroes_zhang_heng_mission`
- `mt_108_heroes_xiao_rang_mission`
- `mt_108_heroes_yang_xiong_mission`
- `mt_108_heroes_hua_rong_mission`
- `mt_108_heroes_suo_chao_mission`
- `mt_108_heroes_dong_ping_mission`
- `mt_108_heroes_tang_long_mission`
- `mt_108_heroes_li_ying_mission`

Examples of named mission scenes found:

- `scn_108_heroes_zhang_qing_mission`
- `scn_108_heroes_daizong_mission`
- `scn_108_heroes_han_tao_mission`
- `scn_108_heroes_lei_heng_mission`
- `scn_108_heroes_wang_ying_mission`
- `scn_108_heroes_zou_run_mission`
- `scn_108_heroes_zhu_tong_mission`
- `scn_108_heroes_li_zhong_mission`
- `scn_108_heroes_meng_kang_mission`
- `scn_108_heroes_du_xing_mission`
- `scn_108_heroes_zhang_heng_mission`
- `scn_108_heroes_peng_qi_mission`
- `scn_108_heroes_yang_xiong_mission`
- `scn_108_heroes_hua_rong_mission`
- `scn_108_heroes_suo_chao_mission`
- `scn_108_heroes_dong_ping_mission`
- `scn_108_heroes_tang_long_mission`

Design lesson: our companions do not need 67 bespoke missions, but they do need a small number of real scenes. A companion's "campaign" should not be considered complete until at least one stage has custom scene placement, scripted agents, and an objective beyond standard conversation.

### 2. Mission Initialization

Relevant source:

- `module_scripts.py`, `script_ini_own_lord_mission`

`script_ini_own_lord_mission` chooses a scene, resets visitors, clears per-troop mission slot `203`, applies health setup, sets specific visitors, and can temporarily set the player troop to the mission hero.

Common patterns:

- Use current town/castle context if the mission starts from a town.
- Otherwise find the nearest town/castle scene.
- Reset all visitors before placing mission cast.
- Give mission actors controlled health.
- Use troop slot `203` as a temporary mission role/team/state marker.
- Place named heroes and enemies into exact visitor slots.

Design lesson: companion campaign missions should get a reusable initializer:

- Pick scene based on current town, village, or companion origin.
- Reset scene visitors.
- Place player, companion, witnesses, enemies, and civilians deliberately.
- Mark temporary mission roles in slots.
- Restore normal player/companion state afterward.

### 3. Mission Progress And Dialogue Beats

Relevant source:

- `module_mission_templates.py`, named `108_heroes_*_mission` templates
- `module_scripts.py`, `script_troop_say_word_in_battle`
- `module_scripts.py`, `script_troop_say_word_in_battle_for_mission`
- `module_presentations.py`, `prsnt_dialogs_in_the_battle`

Many own missions use `$108_heroes_own_mission_progress` as a staged state machine. Mission triggers advance progress, spawn or move actors, refill ammo, display messages, and fire in-battle dialogue lines.

The dialogue system uses presentation overlays rather than normal Warband conversation screens:

- One side can speak at the top of the battle interface.
- Another side can answer at the bottom.
- Timed mission dialogue can stay visible for several seconds.
- Regular battle events also trigger hero lines for kills and defeats.

Design lesson: companion missions should use short in-scene lines during action. The player should hear the companion react while moving, fighting, escorting, sneaking, or investigating.

### 4. Result Grading, Retry, And Review

Relevant source:

- `module_game_menus.py`, `mnu_108_heroes_own_mission_result`
- `module_scripts.py`, `script_lord_mission_program_effect`

`108` mission results are not just success/failure. The result menu supports:

- Failure.
- Success.
- Higher-grade or perfect success.
- Restart.
- Continue.
- Review mode.
- Cooldown or renown loss on failure.
- Hero title progress on stronger success.
- Global title progress for completing all own missions.

`script_lord_mission_program_effect` evaluates mission performance by checking the missioning hero's remaining hit points, with different thresholds per hero.

Design lesson: companion quest outcomes should have grades:

- Failed but recoverable.
- Completed with cost.
- Clean success.
- Ideal outcome that unlocks an extra companion trait, title, or camp role.

This gives companion campaigns replay value and lets failure be interesting without breaking the arc.

## Map Travel Dialogue

Relevant source:

- `module_triggers.py`, map dialog trigger flow
- `module_scripts.py`, `script_show_troop_dialogs_in_the_map`
- `module_scripts.py`, `script_set_map_dialog_info`
- `module_scripts.py`, `script_set_map_dialog_slots`
- `module_scripts.py`, `script_cf_check_map_dialog_progress_immediately`
- `module_scripts.py`, `script_cf_check_map_dialog_progress`
- `module_scripts.py`, `script_map_dialog_set_result`
- `module_presentations.py`, `prsnt_dialogs_in_the_map`

`108` has a campaign-map conversation system. A trigger searches for immediate or post-battle dialogue opportunities. If one is found, the player receives a prompt to press `Y` to trigger a special dialogue or `N` to ignore it. The system then launches a presentation that sequences multiple speakers.

`script_set_map_dialog_info` contains a large catalog of speaker sequences, often alternating between companions, the player, named NPCs, faction heroes, bandit heroes, or special troops.

Design lesson: this is a very strong companion campaign pattern. Instead of making the player manually ask "anything on your mind?" after every event, companions can initiate travel conversations after:

- Winning a battle.
- Entering a companion's homeland.
- Passing a relevant village.
- Recruiting another companion.
- Defeating a hated enemy type.
- Failing or delaying their quest.
- Reaching a trust threshold.

Important robustness note: unlike `108`, our implementation should guard every companion map-dialog trigger with a strict companion availability check so absent companions cannot speak.

## Camp And Building Integration

Relevant source:

- `108_camp_and_building_system.md`
- `108_hero_systems_overview.md`

`108` uses a camp/building system where heroes can be assigned to buildings, workers, jobs, and long-term upgrades. This matters for companion campaigns because it makes companions useful outside the player's immediate party.

Design lesson: a companion campaign can unlock a non-combat role:

- Artimenner supervises construction.
- Jeremus runs an infirmary.
- Deshavi leads a scout post.
- Katrin manages stores.
- Lezalit trains militia.
- Bunduk drills garrison troops.
- Ymira administers a refuge or school.

This should be explicit and timed, with the companion unavailable or partially unavailable while assigned.

## Lessons For Companion Campaigns

### Build Around Campaign Episodes

A companion campaign should be built from episodes, not just quest stages:

1. Travel trigger or personal confession.
2. World target selection.
3. Arrival at town, village, camp, lair, or battlefield.
4. Scene-based conversation or confrontation.
5. Combat, investigation, escort, or skill challenge.
6. In-action companion dialogue.
7. Result grade.
8. Journal update and new unlocked role or next lead.

### Let The Companion Be The Protagonist Sometimes

`108` can temporarily set the player troop to the mission hero. We probably do not need to go that far for every companion, but the idea is valuable: some missions should center the companion's abilities.

Adaptation options:

- Player fights beside the companion while the companion is the required survivor.
- Companion must duel, scout, heal, persuade, or build while the player protects or supports.
- Companion receives the direct reward: title, trait, job skill, or camp assignment.

### Use In-Scene Dialogue Instead Of Menu Recaps

Dialogue should happen while the event is unfolding:

- A companion warns the player before an ambush.
- A witness interrupts during an investigation.
- An enemy recognizes the companion mid-fight.
- A companion reacts when the player chooses mercy or vengeance.
- A town elder changes tone after seeing the companion act.

This is where `108` is especially useful: it demonstrates that Warband can carry short dialogue beats inside mission templates and map presentations.

### Track Multiple Companion Arcs Cleanly

Borrow the sub-quest journal idea:

- One summary quest tracks all companion campaigns.
- Each companion has a visible state: dormant, lead found, active, waiting, failed/cooldown, completed, epilogue.
- Notes show the next actionable place or condition.
- Completed arcs remain summarized so the player remembers what changed.

### Reward More Than Gold

`108` rewards hero-specific progression. Companion campaigns should do the same:

- Personal trait.
- Party skill bonus.
- Camp role.
- Unique troop training option.
- Relationship shifts with other companions.
- Custom item or equipment improvement.
- New battle interjection set.
- New map dialogue branch.

## Companion Campaign Applications

### Klethi

Use `108` map dialogue plus PoP's investigation pattern.

- Trigger: after a town theft, battle loot dispute, or entering a specific town.
- Episode: map-travel warning, town scene with witnesses, night confrontation.
- Mechanics: clue bits, stealth/street fight, optional bribe.
- Result grade: wrong mark, messy success, clean exposure, Klethi personal trait.

### Deshavi / Borcha

Use `108` town random quest progress and map dialogue.

- Trigger: after defeating bandits or passing a forest/steppe village.
- Episode: companion reads trail, party follows target, ambush or lair scene.
- Mechanics: map target from real party, battle progress, companion scouting lines.
- Result grade: target escaped, target defeated, captives rescued, route network unlocked.

### Firentis

Use `108` own mission result grading.

- Trigger: confession after enough trust or after witnessing civilian casualties.
- Episode: village scene, accused survivor, rescue or duel, mercy choice.
- Mechanics: protect target, prevent companion from falling, choose judgment.
- Result grade: vengeance, mercy, public redemption, new honor-based trait.

### Artimenner

Use camp/building and delayed campaign update.

- Trigger: arrive at ruined bridge, mine, tower, or village works.
- Episode: inspect scene, gather material, protect workers, timed construction.
- Mechanics: companion temporarily assigned as engineer.
- Result grade: poor repair, standard repair, masterwork project with extra benefit.

### Jeremus / Ymira

Use hero-assigned random quests and non-combat mission goals.

- Trigger: outbreak, refugee camp, wounded prisoners, village shortage.
- Episode: gather supplies, diagnose cause, defend infirmary, confront profiteer.
- Mechanics: companion skill checks, timed pressure, battle or no-battle resolution.
- Result grade: saved few, saved many, exposed cause, unlocked healer/refuge role.

### Lezalit / Matheld / Bunduk

Use own mission and battle action tracking.

- Trigger: training dispute, unruly militia, veteran challenge, shield-wall test.
- Episode: training field scene, command drill, duel or formation battle.
- Mechanics: companion survival, troop losses, specific battle event progress.
- Result grade: humiliation, grudging respect, disciplined victory, training role.

## Design Rules From 108

- Treat companion content as a campaign layer, not a single quest.
- Let travel, battle, town, and camp systems all participate.
- Give companions voiced/present dialogue during action.
- Store companion campaign state in reusable slots with clear stage names.
- Use a summary tracker so multiple companion arcs remain readable.
- Let the companion receive progression, not just the player.
- Give missions result grades and recovery paths.
- Always guard companion-triggered content by party presence and availability.
- Prefer authored scenes for personal moments.
- Use map prompts sparingly so companion dialogue feels special, not noisy.

## Implementation Recommendations

The first `108`-inspired implementation slice should create a reusable "companion campaign episode" framework:

- Companion availability helper.
- Companion campaign tracker quest note.
- Map-travel dialogue trigger with cooldown.
- Scene initializer for companion episodes.
- In-mission companion dialogue helper.
- Result grade helper.
- Companion reward/trait helper.
- Failure and retry cooldown helper.

After that framework exists, rebuild one companion as a vertical slice. Best candidates:

1. **Klethi**, because investigation plus map dialogue will show the full campaign feel quickly.
2. **Firentis**, because result grading and moral choices fit his arc.
3. **Artimenner**, because camp/building integration creates a visible long-term payoff.
4. **Deshavi or Borcha**, because live map targets and battle progress make the campaign reactive.

The acceptance bar should be: the player travels somewhere with the companion, sees a scene or mission built for that companion, hears dialogue during the event, gets a graded result, and sees the companion's campaign tracker update afterward.
