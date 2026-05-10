from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_quitting_yes", [], "Then I will take you at your word. I will not call this a victory, but I will remember that you chose honesty over dragging the matter into ugliness.", "close_window", [
        (assign, ":nearest_town", "p_town_1"),
        (assign, ":nearest_town_dist", 1000),
        (try_for_range, ":town_no", towns_begin, towns_end),
          (store_faction_of_party, ":town_fac", ":town_no"),
          (store_relation, ":reln", ":town_fac", "fac_player_faction"),
          (ge, ":reln", -10),
          (store_distance_to_party_from_party, ":dist", ":town_no", "p_main_party"),
          (lt, ":dist", ":nearest_town_dist"),
          (assign, ":nearest_town_dist", ":dist"),
          (assign, ":nearest_town", ":town_no"),
        (try_end),
        (troop_set_slot, "$g_talk_troop", slot_troop_cur_center, ":nearest_town"),
        (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_quit),
        (troop_set_slot, "$g_talk_troop", slot_troop_companion_role, sod_companion_role_none),
        (troop_set_slot, "$g_talk_troop", slot_troop_companion_warning_state, sod_companion_warning_broken),
        (call_script, "script_sod_companion_retinue_cleanup_for_departure", "$g_talk_troop", sod_retinue_departure_angry),
        (remove_member_from_party, "$g_talk_troop", "p_main_party"),
        (call_script, "script_sod_companion_cleanup_departed_companion", "$g_talk_troop"),
        (assign, "$npc_is_quitting", 0),
    ]],
]
