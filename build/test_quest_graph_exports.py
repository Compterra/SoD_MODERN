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

from quests.quest_authoring import quest_motif_linear_chain
from quests.quest_diagnostics import quest_graph_dot, quest_graph_mermaid, quest_graph_report_json, quest_graph_snapshot


class QuestGraphExportTests(unittest.TestCase):
    def test_snapshot_and_json_report_shape(self):
        chain = quest_motif_linear_chain("graph_alpha", "Graph Alpha", ("Start", "Finish"))
        snapshot = quest_graph_snapshot(chain)
        report = quest_graph_report_json((chain,))

        self.assertEqual(snapshot["graph_id"], "graph_alpha")
        self.assertEqual(snapshot["kind"], "chain")
        self.assertEqual(len(snapshot["nodes"]), 2)
        self.assertEqual(len(snapshot["templates"]), 2)
        self.assertEqual(snapshot["templates"][0]["kind"], "template")
        self.assertIn("graphs", report)
        self.assertEqual(report["summary"]["graph_count"], 1)
        self.assertEqual(report["summary"]["template_count"], 2)
        self.assertEqual(report["summary"]["stage_count"], 2)
        self.assertEqual(report["graphs"][0]["graph_id"], "graph_alpha")

    def test_mermaid_contains_nodes_and_edges(self):
        chain = quest_motif_linear_chain("graph_beta", "Graph Beta", ("Start", "Finish"))
        mermaid = quest_graph_mermaid(chain)

        self.assertIn("flowchart TD", mermaid)
        self.assertIn("graph_beta_1", mermaid)
        self.assertIn("-->|done|", mermaid)
        self.assertIn("subgraph graph_beta_1_stages", mermaid)

    def test_dot_contains_nodes_and_edges(self):
        chain = quest_motif_linear_chain("graph_gamma", "Graph Gamma", ("Start", "Finish"))
        dot = quest_graph_dot(chain)

        self.assertIn("digraph graph_gamma", dot)
        self.assertIn("graph_gamma_1", dot)
        self.assertIn("->", dot)
        self.assertIn("subgraph cluster_graph_gamma_1", dot)


if __name__ == "__main__":
    unittest.main()
