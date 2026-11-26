from tests.support import WithWorkspace


class VersionTwo(WithWorkspace):
    def test_runs_and_emits_graph_and_budget(self):
        report = self.cli(cycles=6)
        self.assertEqual(report["version"], "2.0")
        self.assertGreater(report["accepted"], 0)
        self.assertTrue(self.read_report("composition/operator-graph.json")["nodes"])
