from tests.support import WithWorkspace


class Pipeline(WithWorkspace):
    def test_archive_connects_profile_diagnosis_candidate_and_trial(self):
        self.cli(cycles=2)
        report = self.read_report("experiment/000001.json")
        for field in ("profile", "diagnosis", "operator", "pairs", "hash"):
            self.assertIn(field, report)
        self.assertEqual(len(report["pairs"]), 3)
