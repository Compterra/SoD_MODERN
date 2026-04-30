from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quests.quest_diagnostics import validate_quest_chain_graph, validate_quest_template_graph
from quests.quest_domain import quest_chain, quest_stage, quest_template


def diagnostic_codes(diagnostics):
    return [diagnostic.code for diagnostic in diagnostics]


class QuestGraphDiagnosticsTests(unittest.TestCase):
    def test_template_graph_reports_broken_and_unreachable_stage_edges(self):
        template = quest_template(
            "quest_alpha",
            "Quest Alpha",
            0,
            "Exercise stage graph diagnostics.",
            stages=(
                quest_stage(
                    "stage_start",
                    "Start",
                    "Begin the route.",
                    transitions={"advance": "stage_missing"},
                ),
                quest_stage("stage_orphan", "Orphan", "This stage is not reachable."),
            ),
        )

        diagnostics = validate_quest_template_graph(template)
        codes = diagnostic_codes(diagnostics)

        self.assertIn("unknown_stage_transition", codes)
        self.assertIn("unreachable_stage", codes)

    def test_chain_graph_reports_broken_and_unreachable_quest_edges(self):
        first = quest_template(
            "quest_first",
            "First",
            0,
            "The entry quest.",
            stages=(quest_stage("first_stage", "First", "Start here."),),
            transitions={"next": "quest_missing"},
        )
        second = quest_template(
            "quest_second",
            "Second",
            0,
            "A quest that cannot be reached.",
            stages=(quest_stage("second_stage", "Second", "Never reached."),),
        )
        chain = quest_chain(
            "chain_alpha",
            "Chain Alpha",
            quests=(first, second),
            entry_quest_id="quest_first",
        )

        diagnostics = validate_quest_chain_graph(chain)
        codes = diagnostic_codes(diagnostics)

        self.assertIn("unknown_quest_transition", codes)
        self.assertIn("unreachable_chain_quest", codes)

    def test_chain_graph_accepts_terminal_quests_end_transition(self):
        template = quest_template(
            "quest_done",
            "Done",
            0,
            "A quest that ends the chain.",
            stages=(quest_stage("done_stage", "Done", "Finish.", metadata={"terminal": True}),),
            transitions={"done": "quests_end"},
        )
        chain = quest_chain("chain_done", "Chain Done", quests=(template,), entry_quest_id="quest_done")

        diagnostics = validate_quest_chain_graph(chain)

        self.assertNotIn("unknown_quest_transition", diagnostic_codes(diagnostics))

    def test_template_graph_reports_missing_incoming_terminal_outcome_and_label_mix(self):
        template = quest_template(
            "quest_beta",
            "Quest Beta",
            0,
            "Exercise expanded stage graph diagnostics.",
            stages=(
                quest_stage(
                    "stage_start",
                    "Start",
                    "Begin.",
                    transitions={"advance": "stage_middle", "success": "stage_end"},
                ),
                quest_stage("stage_middle", "Middle", "Continue.", transitions={"done": "stage_end"}),
                quest_stage("stage_end", "End", "Finish."),
                quest_stage("stage_side", "Side", "No incoming edge.", metadata={"terminal": True}),
            ),
        )

        codes = diagnostic_codes(validate_quest_template_graph(template))

        self.assertIn("stage_without_incoming_transition", codes)
        self.assertIn("terminal_stage_without_outcome", codes)
        self.assertIn("inconsistent_transition_labels", codes)

    def test_chain_graph_reports_early_quests_end_bypass(self):
        first = quest_template(
            "quest_first",
            "First",
            0,
            "Can end early or continue.",
            stages=(quest_stage("first_stage", "First", "Start.", metadata={"terminal": True}),),
            transitions={"done": "quests_end", "next": "quest_second"},
        )
        second = quest_template(
            "quest_second",
            "Second",
            0,
            "Still reachable.",
            stages=(quest_stage("second_stage", "Second", "Continue.", metadata={"terminal": True}),),
        )
        chain = quest_chain("chain_beta", "Chain Beta", quests=(first, second), entry_quest_id="quest_first")

        self.assertIn("early_quests_end_transition", diagnostic_codes(validate_quest_chain_graph(chain)))

    def test_chain_branch_sequence_counts_for_reachability(self):
        first = quest_template(
            "quest_first",
            "First",
            0,
            "The entry.",
            stages=(quest_stage("first_stage", "First", "Start.", metadata={"terminal": True}),),
        )
        second = quest_template(
            "quest_second",
            "Second",
            0,
            "Reached by branch.",
            stages=(quest_stage("second_stage", "Second", "Continue.", metadata={"terminal": True}),),
        )
        chain = quest_chain(
            "chain_gamma",
            "Chain Gamma",
            quests=(first, second),
            entry_quest_id="quest_first",
            branches={"main": ("quest_first", "quest_second")},
        )

        self.assertNotIn("unreachable_chain_quest", diagnostic_codes(validate_quest_chain_graph(chain)))


if __name__ == "__main__":
    unittest.main()
