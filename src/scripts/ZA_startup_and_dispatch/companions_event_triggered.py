from header_operations import *
from module_constants import *

SCRIPTS = [
    ("companions_event_triggered", [
        (store_script_param, ":companion_a", 1),
        (store_script_param, ":companion_b", 2),
        (store_script_param, ":clash_severity", 3),

        # Companion reaction text is only legal while this dispatch owns a
        # verified pair in the current main party.  Clear first so an engine
        # callback with stale or absent actors cannot leave a reusable global
        # selector behind for an unrelated event_triggered conversation.
        (assign, "$g_companion_event_active", 0),
        (assign, "$g_companion_event_actor_a", -1),
        (assign, "$g_companion_event_actor_b", -1),
        (assign, "$g_companion_event_reaction_tier", -1),
        (assign, "$g_companion_event_average_cohesion", -1),
        (assign, "$g_companion_event_clash_severity", -1),
        (assign, "$g_companion_event_reconciliation", -1),
        (assign, "$g_companion_event_variant", -1),
        (assign, ":reaction_tier", 0),
        (assign, ":average_cohesion", 0),
        (assign, ":variant", 0),

        (try_begin),
            (is_between, ":companion_a", companions_begin, companions_end),
            (is_between, ":companion_b", companions_begin, companions_end),
            (neq, ":companion_a", ":companion_b"),
            (call_script, "script_cf_sod_companion_in_main_party", ":companion_a"),
            (call_script, "script_cf_sod_companion_in_main_party", ":companion_b"),
            (try_begin),
                (le, ":clash_severity", 0),
                (assign, ":clash_severity", "$g_companion_last_clash_severity"),
            (try_end),

            (call_script, "script_companions_resent", ":companion_a", ":companion_b", ":clash_severity"),
            (assign, ":reaction_tier", reg0),
            (assign, ":average_cohesion", reg1),

            (assign, "$g_companion_event_actor_a", ":companion_a"),
            (assign, "$g_companion_event_actor_b", ":companion_b"),
            (assign, "$g_companion_event_reaction_tier", ":reaction_tier"),
            (assign, "$g_companion_event_average_cohesion", ":average_cohesion"),
            (assign, "$g_companion_event_clash_severity", ":clash_severity"),
            (assign, "$g_companion_event_reconciliation", "$g_companion_last_clash_was_reconciliation"),

            (assign, ":variant", ":reaction_tier"),
            (try_begin),
                (eq, "$g_companion_last_clash_was_reconciliation", 1),
                (val_add, ":variant", 1),
            (try_end),
            (try_begin),
                (gt, ":average_cohesion", 75),
                (val_sub, ":variant", 1),
            (try_end),
            (try_begin),
                (gt, "$g_companion_clash_chain", 2),
                (val_add, ":variant", 1),
            (try_end),
            # Dialogues deliberately cover the closed selector domain 0..2.
            # Keeping the runtime value in that domain prevents an otherwise
            # valid event from falling through to an unrelated generic route.
            (val_clamp, ":variant", 0, 3),

            (assign, "$g_companion_event_variant", ":variant"),
            (assign, "$g_companion_event_active", 1),
        (try_end),

        (assign, reg0, ":reaction_tier"),
        (assign, reg1, ":average_cohesion"),
        (assign, reg2, ":variant"),
    ]),
]
