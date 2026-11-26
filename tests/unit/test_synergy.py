from modules.M5_composition_scheduler.composition.synergy_analyzer import analyze
from unittest import TestCase


class Synergy(TestCase):
    def test_distinguishes_synergy_order_and_conflict(self):
        report = analyze([{"control": 1, "singles": [2, 3], "forward": 6, "reverse": 2}])
        self.assertEqual(report["interaction"], 2)
        self.assertEqual(report["order_effect"], 4)
        self.assertFalse(report["conflict"])
        loss = analyze([{"control": 1, "singles": [2, 3], "forward": 2, "reverse": None}])
        self.assertTrue(loss["conflict"])
        self.assertIsNone(loss["order_effect"])
