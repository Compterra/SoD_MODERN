from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quests.quest_diagnostics import diagnose_battle_objective


def diagnostic_code(item):
    if hasattr(item, "code"):
        return item.code
    return item["code"]


def diagnostic_metadata(item, name):
    if hasattr(item, name):
        return getattr(item, name)
    if isinstance(item, dict):
        if name in item:
            return item[name]
        for container_name in ("details", "context", "extra", "data"):
            container = item.get(container_name)
            if isinstance(container, dict) and name in container:
                return container[name]
        return None
    for container_name in ("details", "context", "extra", "data"):
        container = getattr(item, container_name, None)
        if isinstance(container, dict) and name in container:
            return container[name]
    return None


class BattleObjectiveDiagnosticsTests(unittest.TestCase):
    def assert_codes(self, diagnostics, *expected_codes):
        codes = [diagnostic_code(item) for item in diagnostics]
        for code in expected_codes:
            self.assertIn(code, codes)
        return codes

    def test_invalid_action_kind_is_rejected(self):
        objective = SimpleNamespace(
            action_kind="not_a_real_action",
            quest_id="quest_alpha",
            stage_id="stage_one",
            source="quests/alpha.txt",
            line=17,
        )

        diagnostics = diagnose_battle_objective(
            objective,
            quest_id="quest_alpha",
            stage_id="stage_one",
            source="quests/alpha.txt",
            line=17,
        )

        self.assert_codes(diagnostics, "invalid_battle_action_kind")
        diagnostic = diagnostics[0]
        self.assertEqual(diagnostic_metadata(diagnostic, "quest_id"), "quest_alpha")
        self.assertEqual(diagnostic_metadata(diagnostic, "stage_id"), "stage_one")
        self.assertEqual(diagnostic_metadata(diagnostic, "source"), "quests/alpha.txt")
        self.assertEqual(diagnostic_metadata(diagnostic, "line"), 17)

    def test_missing_target_is_rejected(self):
        objective = {
            "action_kind": "kill_target",
            "quest_id": "quest_beta",
            "stage_id": "stage_two",
            "source": "quests/beta.txt",
            "line": 29,
        }

        diagnostics = diagnose_battle_objective(objective)
        self.assert_codes(diagnostics, "missing_battle_target")

    def test_impossible_timer_is_rejected(self):
        objective = SimpleNamespace(
            action_kind="survive_timer",
            timer_duration=0,
            quest_id="quest_gamma",
            stage_id="stage_three",
            source="quests/gamma.txt",
            line=8,
        )

        diagnostics = diagnose_battle_objective(objective)
        self.assert_codes(diagnostics, "impossible_battle_timer")

    def test_wave_objective_requires_progress_data(self):
        objective = SimpleNamespace(
            action_kind="defeat_wave",
            target_party=23,
            quest_id="quest_delta",
            stage_id="stage_four",
            source="quests/delta.txt",
            line=42,
        )

        diagnostics = diagnose_battle_objective(objective)
        self.assert_codes(diagnostics, "unsupported_battle_objective")

    def test_stage_wrapper_without_hook_path_is_rejected(self):
        objective = SimpleNamespace(
            action_kind="hold_position",
            target_party=19,
            required=1,
            quest_id="quest_epsilon",
            stage_id="stage_five",
            source="quests/epsilon.txt",
            line=61,
        )
        stage = SimpleNamespace(
            quest_id="quest_epsilon",
            stage_id="stage_five",
            battle=True,
            battle_objective=objective,
        )

        diagnostics = diagnose_battle_objective(
            stage,
            quest_id="quest_epsilon",
            stage_id="stage_five",
            source="quests/epsilon.txt",
            line=61,
            stage=stage,
        )

        self.assert_codes(diagnostics, "missing_battle_hook_path")


if __name__ == "__main__":
    unittest.main()
