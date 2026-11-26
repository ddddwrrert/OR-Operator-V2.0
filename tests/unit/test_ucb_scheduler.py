from modules.M5_composition_scheduler.scheduling.ucb_scheduler import choose
from unittest import TestCase


class Ucb(TestCase):
    def test_ucb_explores_then_exploits(self):
        self.assertEqual(choose(["a", "b"], {"a": [0.9]}), "b")
        self.assertEqual(choose(["a", "b"], {"a": [0.9], "b": [0.1]}, 0), "a")
