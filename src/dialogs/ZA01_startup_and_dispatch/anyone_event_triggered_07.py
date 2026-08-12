from header_dialogs import *
from header_operations import *
from module_constants import *

# This is a single-consumer reaction sink.  The event-triggered preamble
# validates the live participants before dialogue selection; each selected
# route consumes the active flag so stale selector globals cannot hijack the
# next event_triggered conversation.
#
# The conditions below are deliberately a disjoint partition.  Reconciliation
# owns its own selector space, then every ordinary reaction tier owns one
# variant branch (and, where needed, complementary numeric bounds).  Dialogue
# order is therefore presentation order, never hidden routing behavior.
DIALOGS = [
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 1),
        (eq, "$g_companion_event_variant", 0),
        (gt, "$g_companion_event_average_cohesion", 75),
    ], "Fine. Truce, then. We still know how to stand together when the camp needs it.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 1),
        (eq, "$g_companion_event_variant", 0),
        (le, "$g_companion_event_average_cohesion", 75),
    ], "Fine. Truce, then.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 1),
        (eq, "$g_companion_event_variant", 1),
    ], "Call it settled before somebody gets stubborn.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 1),
        (eq, "$g_companion_event_variant", 2),
    ], "I can work beside you, but don't test me on this again.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 0),
        (eq, "$g_companion_event_variant", 0),
        (gt, "$g_companion_event_average_cohesion", 80),
    ], "Enough. We've said our piece. Let's put the blades away and move.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 0),
        (eq, "$g_companion_event_variant", 0),
        (le, "$g_companion_event_average_cohesion", 80),
    ], "Fine. I'll let it lie.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 0),
        (eq, "$g_companion_event_variant", 1),
    ], "I don't want this dragging behind us.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 0),
        (eq, "$g_companion_event_variant", 2),
    ], "This still stings, but I can live with it if we keep moving.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 1),
        (eq, "$g_companion_event_variant", 0),
    ], "We both know the tension is there. At least we're honest about it.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 1),
        (eq, "$g_companion_event_variant", 1),
    ], "No more knives in the dark. Say what you mean, then let it go.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 1),
        (eq, "$g_companion_event_variant", 2),
    ], "This is a crack, not a collapse. Let's keep it from spreading.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 2),
        (eq, "$g_companion_event_variant", 0),
    ], "I'm not eager to forget that exchange.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 2),
        (eq, "$g_companion_event_variant", 1),
    ], "You can hear the room tightening around us, can't you?", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 2),
        (eq, "$g_companion_event_variant", 2),
        (gt, "$g_companion_last_clash_average_cohesion", 45),
    ], "That wasn't just an argument. That was a crack in the hull.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 2),
        (eq, "$g_companion_event_variant", 2),
        (le, "$g_companion_last_clash_average_cohesion", 45),
    ], "That wasn't just an argument. That's what a company sounds like when it's starting to come apart.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 3),
        (eq, "$g_companion_event_variant", 0),
    ], "I'm tired of hearing apologies that don't change anything.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 3),
        (eq, "$g_companion_event_variant", 1),
    ], "You keep pushing, and you'll find what the rest of us have been swallowing.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 3),
        (eq, "$g_companion_event_variant", 2),
    ], "The next argument might not end with words.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 4),
        (eq, "$g_companion_event_variant", 0),
    ], "The next insult is going to cost more than pride.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 4),
        (eq, "$g_companion_event_variant", 1),
    ], "If we're doing this again, then we're all pretending not to see the cracks.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 4),
        (eq, "$g_companion_event_variant", 2),
        (gt, "$g_companion_event_clash_severity", 80),
    ], "Keep provoking the wrong person and the camp will answer for it.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_active", 1),
        (eq, "$g_companion_event_reconciliation", 0),
        (eq, "$g_companion_event_reaction_tier", 4),
        (eq, "$g_companion_event_variant", 2),
        (le, "$g_companion_event_clash_severity", 80),
    ], "I won't forget this. None of us will.", "close_window", [
        (assign, "$g_companion_event_active", 0),
    ]],
]
