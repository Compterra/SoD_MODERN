from header_operations import *
from module_constants import *

SCRIPTS = [
    ("companions_event_triggered", [
        (store_script_param, ":companion_a", 1),
        (store_script_param, ":companion_b", 2),
        (store_script_param, ":clash_severity", 3),

        (try_begin),
            (le, ":clash_severity", 0),
            (assign, ":clash_severity", "$g_companion_last_clash_severity"),
        (try_end),

        (call_script, "script_companions_resent", ":companion_a", ":companion_b", ":clash_severity"),

        (assign, ":reaction_tier", reg0),
        (assign, ":average_cohesion", reg1),

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
        (val_clamp, ":variant", 0, 4),

        (assign, "$g_companion_event_variant", ":variant"),

        (assign, reg0, ":reaction_tier"),
        (assign, reg1, ":average_cohesion"),
        (assign, reg2, ":variant"),
    ]),
]