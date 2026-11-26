from tests.support import WithWorkspace


class CompositionPipeline(WithWorkspace):
    def test_live_ablation_uses_matched_seeds_and_reversed_order(self):
        self.cli(cycles=10)
        rows = self.read_report("composition/experiments.json")
        self.assertTrue(rows)
        first = rows[0]
        self.assertGreaterEqual(len(first["components"]), 2)
        self.assertEqual({pair["seed"] for pair in first["paired"]}, {11, 29})
        self.assertTrue(all(pair["reverse"] is not None for pair in first["paired"]))
