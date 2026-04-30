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

from quests.quest_authoring import (
    quest_components_from_mapping,
    quest_component_registry,
    quest_motif_escort_ambush_debrief,
    quest_motif_from_mapping,
    quest_motif_linear_chain,
)


class QuestAuthoringTests(unittest.TestCase):
    def test_registry_registers_and_reads_components(self):
        registry = quest_component_registry("registry_alpha")
        condition = registry.register_condition("ready", "player ready")
        action = registry.register_action("brief", "brief patrol")
        reward = registry.register_reward("paid", "paid")

        self.assertEqual(registry.get_condition("ready"), condition)
        self.assertEqual(registry.get_action("brief"), action)
        self.assertEqual(registry.get_reward("paid"), reward)
        snapshot = registry.snapshot()
        self.assertIsInstance(snapshot, dict)
        self.assertIn("ready", snapshot["conditions"])

    def test_registry_rejects_duplicate_names(self):
        registry = quest_component_registry("registry_beta")
        registry.register_condition("ready", "player ready")

        with self.assertRaises(ValueError):
            registry.register_condition("ready", "player still ready")

    def test_registry_can_be_populated_from_mapping(self):
        registry = quest_components_from_mapping(
            "registry_bulk",
            {
                "conditions": {"ready": "player ready"},
                "actions": {"brief": "brief patrol"},
                "rewards": {"paid": "paid"},
                "failures": {"lost": "lost"},
            },
        )

        self.assertTrue(registry.has_condition("ready"))
        self.assertTrue(registry.has_action("brief"))
        self.assertTrue(registry.has_reward("paid"))
        self.assertTrue(registry.has_failure("lost"))

    def test_linear_motif_builds_chain_and_legacy_tuples(self):
        chain = quest_motif_linear_chain("motif_alpha", "Motif Alpha", ("Start", "Finish"))

        self.assertEqual(chain.entry_quest_id, "motif_alpha_1")
        self.assertEqual(chain.branches["main"], ("motif_alpha_1", "motif_alpha_2"))
        self.assertEqual(chain.normalized_quests()[0].transitions["done"], "motif_alpha_2")
        self.assertEqual(chain.normalized_quests()[1].transitions["done"], "quests_end")
        self.assertEqual(len(chain.as_legacy_tuples()), 2)

    def test_linear_motif_can_apply_registry_defaults(self):
        registry = quest_components_from_mapping(
            "registry_defaults",
            {
                "conditions": {"ready": "player ready"},
                "actions": {"brief": "brief patrol"},
                "rewards": {"paid": "paid"},
            },
        )
        chain = quest_motif_linear_chain(
            "motif_defaults",
            "Motif Defaults",
            ("Start", "Finish"),
            registry=registry,
            condition_names=("ready",),
            action_names=("brief",),
            reward_names=("paid",),
        )
        first = chain.normalized_quests()[0]

        self.assertEqual(first.conditions[0].condition_id, "registry_defaults_ready")
        self.assertEqual(first.actions[0].action_id, "registry_defaults_brief")
        self.assertEqual(first.rewards[0].reward_id, "registry_defaults_paid")
        self.assertEqual(first.metadata["component_registry"], "registry_defaults")

    def test_registry_defaults_fail_on_missing_component(self):
        registry = quest_component_registry("registry_missing")

        with self.assertRaises(KeyError):
            quest_motif_linear_chain(
                "motif_missing",
                "Motif Missing",
                ("Start",),
                registry=registry,
                condition_names=("ready",),
            )

    def test_motif_can_be_authored_from_mapping(self):
        chain = quest_motif_from_mapping(
            {
                "chain_id": "motif_mapping",
                "title": "Motif Mapping",
                "motif": "linear_chain",
                "quest_titles": ("Start", "Finish"),
                "registry": {
                    "conditions": {"ready": "player ready"},
                    "actions": {"brief": "brief patrol"},
                    "rewards": {"paid": "paid"},
                },
                "defaults": {
                    "conditions": ("ready",),
                    "actions": ("brief",),
                    "rewards": ("paid",),
                },
            }
        )
        first = chain.normalized_quests()[0]

        self.assertEqual(chain.chain_id, "motif_mapping")
        self.assertEqual(first.conditions[0].condition_id, "motif_mapping_registry_ready")
        self.assertEqual(first.actions[0].action_id, "motif_mapping_registry_brief")

    def test_named_motif_uses_expected_shape(self):
        chain = quest_motif_escort_ambush_debrief("escort_alpha", "Escort Alpha")

        self.assertEqual(len(chain.normalized_quests()), 3)
        self.assertEqual(chain.metadata["motif"], "escort_ambush_debrief")


if __name__ == "__main__":
    unittest.main()
