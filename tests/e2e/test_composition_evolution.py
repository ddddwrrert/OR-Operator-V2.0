from tests.support import WithWorkspace


class CompositionEvolution(WithWorkspace):
    def test_composition_cap_is_enforced(self):
        report = self.cli(cycles=9, overrides={"budget": {"composition_trials": 1}})
        self.assertEqual(report["budget_used"]["composition_trials"], 1)
        self.assertEqual(len(self.read_report("composition/experiments.json")), 1)
