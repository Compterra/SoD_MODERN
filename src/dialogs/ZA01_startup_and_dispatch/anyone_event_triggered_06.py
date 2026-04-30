from header_dialogs import *
from header_operations import *
from module_constants import *

DIALOGS = [
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reconciliation", 1),
        (eq, "$g_companion_event_variant", 0),
    ], "Enough. We made our point. Let's leave it there.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reconciliation", 1),
        (eq, "$g_companion_event_variant", 1),
    ], "The edge is still there, but it'll heal if we stop digging.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reconciliation", 1),
        (eq, "$g_companion_event_variant", 2),
    ], "I can stand down. Just don't mistake that for forgetting.", "close_window", []],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 0),
        (eq, "$g_companion_event_variant", 0),
    ], "Enough. We've said our piece. Let's put the blades away and move.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 0),
        (eq, "$g_companion_event_variant", 1),
    ], "I don't love the argument, but I trust the crew more than the quarrel.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 0),
        (eq, "$g_companion_event_variant", 2),
    ], "This still stings, but I can live with it if we keep moving.", "close_window", []],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 1),
        (eq, "$g_companion_event_variant", 0),
    ], "We've got friction. Better to name it than let it rot in silence.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 1),
        (eq, "$g_companion_event_variant", 1),
    ], "That's a rough edge, not a wound. Let's not make it one.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 1),
        (eq, "$g_companion_event_variant", 2),
    ], "We can disagree without turning the whole camp sour.", "close_window", []],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 2),
        (eq, "$g_companion_event_variant", 0),
    ], "That cut deeper than it needed to. I'll remember it.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 2),
        (eq, "$g_companion_event_variant", 1),
    ], "You can call it honesty if you want. I call it a problem.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 2),
        (eq, "$g_companion_event_variant", 2),
    ], "One more round of this and the camp is going to split down the middle.", "close_window", []],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 3),
        (eq, "$g_companion_event_variant", 0),
    ], "No. I'm done pretending this is harmless.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 3),
        (eq, "$g_companion_event_variant", 1),
    ], "You keep pushing, and you'll find what the rest of us have been swallowing.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 3),
        (eq, "$g_companion_event_variant", 2),
    ], "The next argument might not end with words.", "close_window", []],

    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 4),
        (eq, "$g_companion_event_variant", 0),
    ], "You've turned the whole party into a powder keg.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 4),
        (eq, "$g_companion_event_variant", 1),
    ], "If that's your idea of leadership, it's a poor one.", "close_window", []],
    [anyone, "event_triggered", [
        (eq, "$g_companion_event_reaction_tier", 4),
        (eq, "$g_companion_event_variant", 2),
    ], "I won't forget this. None of us will.", "close_window", []],
]
