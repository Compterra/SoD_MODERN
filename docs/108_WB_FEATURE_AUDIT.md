# 108-WB Source Feature Audit

Source audited: `References/108-WB/Source`

Date: 2026-05-13

This audit looks for reusable feature ideas in the 108-WB module source, with an eye toward systems that could strengthen SoD/Ponavosa without dragging in 108-WB's whole bespoke campaign.

## High-Value Feature Candidates

### Mid-Battle Dialogue Overlay

Primary anchors:
- `References/108-WB/Source/module_presentations.py`: `dialogs_in_the_battle`
- `References/108-WB/Source/module_scripts.py`: `script_troop_say_word_in_battle_for_mission`
- `References/108-WB/Source/module_mission_templates.py`: repeated calls to battle dialogue scripts

What it does:
- Shows short in-battle speech panels with troop portraits.
- Lets mission scripts push spoken lines during combat without leaving the battle.
- Supports top/bottom speaker slots and timed display.

Fit for this project:
- Strong fit.
- This is the cleanest way to turn some current menu-like outcomes into world or battle events.
- Best use would be commander shouts, mercenary grievances, betrayal warnings, rescue calls, morale breaks, and battlefield aftermath beats.

Port priority: High.

### Commander Duel / VS Fight System

Primary anchors:
- `References/108-WB/vs_system_documentation.md`
- `References/108/108_1v1_commander_duel_analysis.md`
- `References/108-WB/Source/module_mission_templates.py`: `$can_vs`, `$vs_fight`, `ally call vs`, duel HP/status logic

What it does:
- Creates a formal commander duel inside a live battle.
- Uses temporary neutrality/ring logic so both armies pause around the duel.
- Tracks win/loss, HP bars, timeouts, morale fallout, and duel loot.

Fit for this project:
- Strong concept fit, but technically complex.
- The spectacle is good, but it should remain rare and contextual: heroic challenge, noble rivalry, trial by combat, champion duel, or a desperate morale gambit.

Port priority: Medium-high. Documented enough to prototype later.

### Post-Defeat Spectator And Hero Switching

Primary anchors:
- `References/108-WB/Source/module_mission_templates.py`: repeated defeat messages mentioning watching, camera controls, switching heroes, and choosing a hero
- `References/108-WB/Source/module_presentations.py`: `choose_fighter_in_battle`

What it does:
- After the player is defeated, battle can continue under watch mode.
- Player can rotate/move camera, switch watched heroes, and in some missions choose another fighter.

Fit for this project:
- Good feature for companion-heavy play.
- Could make companions matter more after player knockout.
- Risk is high because camera/agent control code is scattered through mission templates and may conflict with existing battle handling.

Port priority: Medium.

### In-Battle Tactics And Battle Setting UI

Primary anchors:
- `References/108-WB/Source/module_presentations.py`: `tactics_window`, `battle_setting`
- `References/108-WB/Source/module_game_menus.py`: camp entries for opening tactics/battle setting presentations

What it does:
- Adds presentation-based tactical controls.
- Stores class/order/density/line settings on item slots.
- Gives the player a more explicit pre-battle or camp configuration layer.

Fit for this project:
- Good idea, but should be adapted instead of copied.
- This project should favor clear Warband-compatible controls and avoid a dense debug-looking UI.
- Could become a mercenary command doctrine screen: infantry posture, missile discipline, cavalry reserve, skirmisher behavior, baggage guard policy.

Port priority: Medium.

### Hero Battle Ranking

Primary anchors:
- `References/108-WB/Source/module_game_menus.py`: `get kill rank list`, `show battle rank detail`, `check_battle_rank_per_week`
- `References/108-WB/Source/module_presentations.py`: `main_party_hero_rank`
- `References/108-WB/Source/module_simple_triggers.py`: weekly and battle-result related rank/display hooks

What it does:
- Tracks hero performance and displays rankings.
- Appears to support weekly checks and battle detail views.

Fit for this project:
- Strong fit if tied to companion/company systems.
- Could support contracts, pay disputes, honors, promotion, reputation, jealousy, and morale.
- This is a better home for "public honors" than a generic camp menu option.

Port priority: High.

### Hero Special Skills

Primary anchors:
- `References/108-WB/Source/module_simple_triggers.py`: repeated `script_display_hero_special_skill_out_battle`, `snd_special_skill`
- `References/108-WB/Source/module_game_menus.py`: special skill detail menus
- `References/108-WB/Source/module_mission_templates.py`: `special skill...active`, skill-specific mission effects

What it does:
- Gives named heroes special abilities.
- Displays out-of-battle and in-battle skill messages.
- Uses custom sounds and mission-side effects.

Fit for this project:
- Good inspiration, but needs restraint.
- Better as companion traits, command talents, event expertise, or rare battlefield interventions than as arcade powers.

Port priority: Medium.

## Economy And Company Systems

### Center Building With Workers

Primary anchors:
- `References/108-WB/Source/module_presentations.py`: `center_status`, `center_building`, `center_building_test`
- `References/108-WB/Source/module_scripts.py`: `get_center_building_level`, `get_building_needs_attribute`, `get_town_population_increase`, `get_town_equipment_increase`, `get_town_horse_increase`, `set_worker_in_building`
- `References/108-WB/Source/module_simple_triggers.py`: building and worker update logic around the late trigger blocks

What it does:
- Adds levelled center buildings.
- Assigns workers/leaders to buildings.
- Produces population, equipment, horses, and soldier backup value.

Fit for this project:
- Strong economy inspiration, but not a direct import.
- This project already has its own economy direction. The reusable idea is worker assignment changing production, not the exact 108-WB building tree.

Port priority: Medium-high for design mining, low for direct port.

### Camp Building / Company Base

Primary anchors:
- `References/108-WB/Source/module_mission_templates.py`: `camp_building`
- `References/108-WB/Source/module_scripts.py`: `set_camp_building_visitors`, `set_camp_building_roles`, `auto_set_camp_building_practice_roles`, `cf_camp_building_can_build`, `cf_camp_building_can_upgrade`, `get_camp_building_leader`, `get_camp_building_upgrade_requirement`
- `References/108-WB/Source/module_simple_triggers.py`: camp building checks, role changes, repairs, refinement, follower searches

What it does:
- Creates a camp/base scene with buildings, leaders, roles, and background jobs.
- Supports training/practice roles, building upgrades, over-limit member handling, and job changes.

Fit for this project:
- Very strong concept fit.
- Could become a real mercenary company camp rather than another menu hub.
- Best use would be quartermaster, infirmary, forge, stables, scout tent, baggage train, and training yard as world/company state.

Port priority: High for concept, medium for code reuse.

### Item Repair, Refinement, And Special Item Leveling

Primary anchors:
- `References/108-WB/Source/module_simple_triggers.py`: `repair_bad_imod_by_camp_building`, auto-use refine stone for special item leveling
- `References/108-WB/Source/module_scripts.py`: `repair_bad_imod_by_camp_building`, `get_troop_all_equipment_point`, `check_troop_all_equipment_point_while_leaving`

What it does:
- Repairs bad item modifiers through camp building logic.
- Uses refinement stones or special item progression.
- Checks troop equipment point totals when leaving.

Fit for this project:
- Useful if reframed as quartermaster work, smithing contracts, salvage, and maintenance costs.
- Direct magical item levelling is probably off-tone unless the mod wants legendary gear progression.

Port priority: Medium.

### Horse HP And Mounted Endurance

Primary anchors:
- `References/108-WB/Source/module_scripts.py`: `change_horse_max_hp_by_riding_skill`, `heal_player_and_horse_hp`, `move_horse_to_two_corners`
- `References/108-WB/Source/module_mission_templates.py`: VS horse damage and HP messages

What it does:
- Adjusts horse max HP by riding skill.
- Heals player and horse HP in some flows.
- Handles horse positioning and horse damage messaging.

Fit for this project:
- Good economy/tactics idea if attached to stables, remounts, horse care, and cavalry fatigue.
- Needs careful balance so it does not become hidden stat churn.

Port priority: Medium.

## Quest And Presentation Systems

### 108 Heroes Arena / Team Fight System

Primary anchors:
- `References/108-WB/Source/module_game_menus.py`: `108_heroes_fight`, `108_heroes_arena_team_fight_main_menu`, old/new fight menus, monthly checks, choose/event/result menus
- `References/108-WB/Source/module_presentations.py`: `108_heroes_fight_choose_troop`, `108_heroes_arena_team_fight_pre`, `108_heroes_arena_team_fight_choose_fighter`, `108_heroes_arena_team_fight_result`
- `References/108-WB/Source/module_mission_templates.py`: `108_heroes_arena_team_fight`, `108_heroes_hill_battle`, `108_heroes_arena_battle_new`, `108_heroes_arena_battle_old`

What it does:
- Large tournament/team fight subsystem.
- Supports troop choice, pre-fight presentation, results, scoring, money, renown, and monthly events.

Fit for this project:
- Mixed.
- The structure is valuable, but the content is very 108-specific.
- Better adapted as mercenary games, musters, judicial combats, company trials, or contract showcases.

Port priority: Medium-low.

### Hero Personal Mission Framework

Primary anchors:
- `References/108-WB/Source/module_mission_templates.py`: many `108_heroes_*_mission` templates
- `References/108-WB/Source/module_presentations.py`: `108_heroes_mission_poem`, mission-specific presentations
- `References/108-WB/Source/module_dialogs.py`: hero mission dialogue branches

What it does:
- Provides many mission-specific scenes and encounter scripts for named heroes.
- Uses staged dialogue, poems, special skills, and combat beats.

Fit for this project:
- Good architecture inspiration for companion arcs.
- Weak direct port because narrative content is specific to Water Margin/108 Heroes.

Port priority: Medium for patterns, low for content.

### World-Map And Utility Presentations

Primary anchors:
- `References/108-WB/Source/module_presentations.py`: `world_map`, `card_view`, `all_items`, `second_round_type_slot_code`

What it does:
- Adds utility/debug/visual presentations for map, cards, item inspection, and slot code views.

Fit for this project:
- Mostly developer or debugging inspiration.
- `all_items` and slot-code views may help audit content, but they should not become player-facing unless redesigned.

Port priority: Low.

## Best Fits For Current Design Goals

The strongest feature direction is not another menu tree. It is eventful company state:

1. Use battle/world dialogue overlays for events that should feel alive.
2. Move "public honors" style actions into battle ranking or post-battle company events.
3. Use camp/base roles to ground economy decisions in people and places.
4. Treat workers, wounded, horses, gear repair, and training as company logistics.
5. Reserve large presentation menus for planning/configuration, not for every narrative outcome.

## Suggested Extraction Order

1. Document exact globals/slots used by battle dialogue and hero ranking.
2. Prototype a small battle/company event overlay using existing SoD event state.
3. Add a battle performance ledger for companions and troop groups.
4. Convert honors/feast/reward concepts into conditional post-battle events.
5. Mine camp building roles into a mercenary company camp design.
6. Revisit duel and spectator systems after the smaller battle-event layer is stable.

## Things To Avoid Directly Porting

- The full 108 Heroes tournament stack without redesign.
- Hero-specific missions as-is.
- Dense debug-style presentations as player UI.
- Magical item progression unless the setting explicitly wants that tone.
- Any menu-only grievance, honor, or warning option that should instead appear as a timed world event, camp encounter, or post-battle consequence.
