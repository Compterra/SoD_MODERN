"""M&B 1.011 world-map party encounter callback.

This hardcoded callback is the engine's entry point for talking to parties and
entering centers. Keep native/SoD routing intact, but guard the party reads so
old invalid/reserved encounter ids do not poison later menus.
"""

from typing import Any

SCRIPTS = [
    ("game_event_party_encounter",
     [
       (store_script_param_1, "$g_encountered_party"),
       (store_script_param_2, "$g_encountered_party_2"),
       (assign, "$g_encountered_party_faction", -1),
       (assign, "$g_encountered_party_relation", 0),
       (assign, "$g_encountered_party_type", -1),
       (assign, "$g_encountered_party_template", -1),

       (try_begin),
         (gt, "$g_encountered_party", 0),
         (party_is_active, "$g_encountered_party"),
         (store_faction_of_party, "$g_encountered_party_faction", "$g_encountered_party"),
         (store_relation, "$g_encountered_party_relation", "$g_encountered_party_faction", "fac_player_faction"),
         (party_get_slot, "$g_encountered_party_type", "$g_encountered_party", slot_party_type),
         (party_get_template_id, "$g_encountered_party_template", "$g_encountered_party"),
       (else_try),
         (assign, "$g_encountered_party", -1),
       (try_end),
       (try_begin),
         (lt, "$g_encountered_party_2", 0),
         (assign, "$g_encountered_party_2", -1),
       (else_try),
         (neg|party_is_active, "$g_encountered_party_2"),
         (assign, "$g_encountered_party_2", -1),
       (try_end),

       (call_script, "script_party_count_fit_regulars", "p_main_party"),
       (assign, "$playerparty_prebattle_regulars", reg0),
       (assign, "$g_last_rest_center", -1),
       (assign, "$talk_context", 0),
       (assign, "$g_player_surrenders", 0),
       (assign, "$g_enemy_surrenders", 0),
       (assign, "$g_leave_encounter", 0),
       (assign, "$g_engaged_enemy", 0),
       (try_begin),
         (this_or_next|le, "$g_encountered_party", 0),
         (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
         (rest_for_hours, 0),
       (try_end),
       (assign, "$new_encounter", 1),

       (try_begin),
         (le, "$g_encountered_party", 0),
         (jump_to_menu, "mnu_camp"),
       (else_try),
         (lt, "$g_encountered_party_2", 0),
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (jump_to_menu, "mnu_castle_outside"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
           (jump_to_menu, "mnu_castle_outside"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_ship),
           (jump_to_menu, "mnu_ship_reembark"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
           (jump_to_menu, "mnu_village"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_merc_base),
           (jump_to_menu, "mnu_sod_merc_guild"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_cattle_herd),
           (jump_to_menu, "mnu_cattle_herd"),
         (else_try),
           (is_between, "$g_encountered_party", training_grounds_begin, training_grounds_end),
           (jump_to_menu, "mnu_training_ground"),
         (else_try),
           (eq, "$g_encountered_party", "p_zendar"),
           (jump_to_menu, "mnu_zendar"),
         (else_try),
           (eq, "$g_encountered_party", "p_salt_mine"),
           (jump_to_menu, "mnu_salt_mine"),
         (else_try),
           (eq, "$g_encountered_party", "p_four_ways_inn"),
           (jump_to_menu, "mnu_four_ways_inn"),
         (else_try),
           (eq, "$g_encountered_party", "p_test_scene"),
           (jump_to_menu, "mnu_test_scene"),
         (else_try),
           (eq, "$g_encountered_party", "p_battlefields"),
           (jump_to_menu, "mnu_battlefields"),
         (else_try),
           (eq, "$g_encountered_party", "p_training_ground"),
           (jump_to_menu, "mnu_tutorial"),
         (else_try),
           (eq, "$g_encountered_party", "p_camp_bandits"),
           (jump_to_menu, "mnu_camp"),
         (else_try),
           (jump_to_menu, "mnu_simple_encounter"),
         (try_end),
       (else_try),
         (try_begin),
           (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
           (try_begin),
             (eq, "$auto_enter_town", "$g_encountered_party"),
             (jump_to_menu, "mnu_town"),
           (else_try),
             (eq, "$auto_besiege_town", "$g_encountered_party"),
             (jump_to_menu, "mnu_besiegers_camp_with_allies"),
           (else_try),
             (jump_to_menu, "mnu_join_siege_outside"),
           (try_end),
         (else_try),
           (jump_to_menu, "mnu_pre_join"),
         (try_end),
       (try_end),
       (assign, "$auto_enter_town", 0),
       (assign, "$auto_besiege_town", 0),
     ]),
]

from src.scripts.ZG_quests.sod_quest_battle_advance_action import _dispatch_battle_event


def _extract_context(args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    runtime = kwargs.get("runtime")
    quest_id = kwargs.get("quest_id")
    stage_id = kwargs.get("stage_id")
    event = kwargs.get("event")
    payload = kwargs.get("payload", {})

    positional = list(args)
    if runtime is None and positional:
        runtime = positional.pop(0)
    if quest_id is None and positional:
        quest_id = positional.pop(0)
    if stage_id is None and positional:
        stage_id = positional.pop(0)
    if event is None and positional:
        event = positional.pop(0)
    if positional and not payload:
        payload = positional.pop(0)

    return {
        "runtime": runtime,
        "quest_id": quest_id,
        "stage_id": stage_id,
        "event": event,
        "payload": payload,
    }


def script_game_event_party_encounter(*args: Any, **kwargs: Any) -> None:
    context = _extract_context(args, kwargs)
    event = context["event"]
    if event is None:
        event = _dispatch_battle_event(
            context["runtime"],
            "battle_started",
            quest_id=context["quest_id"],
            stage_id=context["stage_id"],
            payload=context["payload"] if isinstance(context["payload"], dict) else {},
        )
    else:
        _dispatch_battle_event(
            context["runtime"],
            "battle_started",
            quest_id=context["quest_id"],
            stage_id=context["stage_id"],
            payload=context["payload"] if isinstance(context["payload"], dict) else {},
        )


def game_event_party_encounter(*args: Any, **kwargs: Any) -> None:
    script_game_event_party_encounter(*args, **kwargs)


__all__ = [
    "game_event_party_encounter",
    "script_game_event_party_encounter",
]
