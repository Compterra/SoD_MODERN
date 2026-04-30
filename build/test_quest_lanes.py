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

from quests.quest_diagnostics import validate_quest_template_graph
from quests.quest_domain import quest_reward, quest_stage, quest_template
from quests.quest_lanes import quest_dialogue_lanes, quest_lane_contract, quest_outcome_triggers


def codes(diagnostics):
    return [diagnostic.code for diagnostic in diagnostics]


class QuestLaneTests(unittest.TestCase):
    def test_lane_contract_snapshot(self):
        contract = quest_lane_contract(
            "lane_alpha",
            dialogue_lanes=quest_dialogue_lanes(accepted="dlg_accept"),
            outcome_triggers=quest_outcome_triggers(success="script_success"),
            journal_lanes={"accepted": "journal_accept"},
            required_lanes=("accepted",),
            required_outcomes=("success",),
        )
        snapshot = contract.to_snapshot()

        self.assertEqual(snapshot["contract_id"], "lane_alpha")
        self.assertEqual(snapshot["dialogue_lanes"]["accepted"], "dlg_accept")
        self.assertEqual(snapshot["outcome_triggers"]["success"], "script_success")

    def test_missing_required_dialogue_lane_is_diagnosed(self):
        contract = quest_lane_contract("lane_beta", required_lanes=("accepted",))
        template = quest_template(
            "quest_lane_beta",
            "Lane Beta",
            0,
            "Missing an accepted dialogue lane.",
            stages=(quest_stage("stage_start", "Start", "Begin.", metadata={"lane_contract": contract.to_snapshot(), "terminal": True}),),
        )

        self.assertIn("missing_dialogue_lane", codes(validate_quest_template_graph(template)))

    def test_reward_stage_requires_success_outcome_when_contract_declared(self):
        contract = quest_lane_contract("lane_gamma", dialogue_lanes={"done": "dlg_done"}, journal_lanes={"done": "journal_done"})
        template = quest_template(
            "quest_lane_gamma",
            "Lane Gamma",
            0,
            "Reward path without outcome trigger.",
            stages=(
                quest_stage(
                    "stage_done",
                    "Done",
                    "Finish.",
                    rewards=(quest_reward("lane_gamma_reward", "paid"),),
                    metadata={"lane_contract": contract.to_snapshot()},
                ),
            ),
        )

        self.assertIn("missing_outcome_trigger", codes(validate_quest_template_graph(template)))

    def test_complete_lane_contract_is_clean(self):
        contract = quest_lane_contract(
            "lane_delta",
            dialogue_lanes={"accepted": "dlg_accept"},
            outcome_triggers={"success": "script_success"},
            journal_lanes={"accepted": "journal_accept"},
            required_lanes=("accepted",),
            required_outcomes=("success",),
        )
        template = quest_template(
            "quest_lane_delta",
            "Lane Delta",
            0,
            "Complete lane coverage.",
            stages=(quest_stage("stage_done", "Done", "Finish.", metadata={"lane_contract": contract.to_snapshot(), "terminal": True}),),
        )

        lane_codes = [code for code in codes(validate_quest_template_graph(template)) if code.startswith("missing_") and "lane" in code]
        self.assertEqual(lane_codes, [])


if __name__ == "__main__":
    unittest.main()
