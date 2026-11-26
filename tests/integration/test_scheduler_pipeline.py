from tests.support import WithWorkspace


class SchedulingPipeline(WithWorkspace):
    def test_records_observed_context_and_both_replayed_policies(self):
        self.cli(cycles=3)
        report = self.read_report("scheduling/policy-replay.json")
        self.assertEqual(set(report["replay_action_counts"]), {"UCB", "Thompson"})
        self.assertEqual(sum(item["count"] for item in report["observed"]), 3)
