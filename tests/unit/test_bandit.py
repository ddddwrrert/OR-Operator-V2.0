from modules.M5_composition_scheduler.scheduling.contextual_bandit import samples
from modules.M5_composition_scheduler.scheduling.thompson_scheduler import choose
from unittest import TestCase


class Bandit(TestCase):
    def test_feedback_remains_in_context_and_cost_affects_reward(self):
        history = [{"plan": {"context": "cold", "kind": "a"}, "accepted": True, "gain": 0.15, "seconds": 1},
                   {"plan": {"context": "hot", "kind": "b"}, "accepted": False}]
        self.assertEqual(samples(history, "cold", 0.2), {"a": [0.15]})
        self.assertEqual(choose(["a", "b"], samples(history, "cold", 0.2), 42), "b")
