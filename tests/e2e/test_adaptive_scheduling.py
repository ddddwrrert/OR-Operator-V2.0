from tests.support import WithWorkspace


class AdaptiveScheduling(WithWorkspace):
    def test_thompson_can_act_as_live_policy(self):
        self.cli(cycles=5, overrides={"scheduler": {"algorithm": "Thompson"}})
        plans = self.read_report("scheduling/policy-replay.json")["decisions"]
        self.assertTrue(all(item["algorithm"] == "Thompson" for item in plans))
        self.assertGreater(len({item["kind"] for item in plans}), 1)
