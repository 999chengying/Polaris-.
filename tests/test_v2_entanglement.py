# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from v2_entanglement import power_iteration, dual_entanglement, triple_entanglement

class TestV2Entanglement(unittest.TestCase):
    def test_power_convergence(self):
        path, status = power_iteration(2, 2, steps=5)
        self.assertEqual(status, "不动点")
        self.assertEqual(path[-1], 6)

    def test_dual_oscillation(self):
        # 2和3以平方和立方互相纠缠
        final_state, steps = dual_entanglement(2, 3, 2, 3, steps=5)
        self.assertEqual(final_state, (8, 2)) # 或者(2,8)

    def test_triple_consensus(self):
        # 三生纠缠瞬间达成共识
        final_state, steps = triple_entanglement(2, 3, 4, 2, 2, 2)
        self.assertEqual(final_state, (6, 6, 6))
        self.assertEqual(steps, 1)

if __name__ == "__main__":
    unittest.main()
