# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from v2_small_model import add_one, sub_one, add_k, decimal_division

class TestV2SmallModel(unittest.TestCase):
    def test_add_one_carry(self):
        state, carried = add_one((0, 0, 9))
        self.assertEqual(state, (0, 1, 0))
        self.assertTrue(carried)

    def test_sub_one_borrow(self):
        state, borrowed = sub_one((0, 1, 0))
        self.assertEqual(state, (0, 0, 9))
        self.assertTrue(borrowed)

    def test_add_k_carries(self):
        _, carries = add_k((0, 0, 8), 3)
        self.assertEqual(carries, 1) # 8+3=11, 1次进位

    def test_decimal_division_inf(self):
        digits, exact = decimal_division(1, 3, depth=5)
        self.assertEqual(digits, [3, 3, 3, 3, 3])
        self.assertFalse(exact)

if __name__ == "__main__":
    unittest.main()
