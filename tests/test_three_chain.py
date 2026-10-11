# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from three_chain_net import ThreeChainNet, CENTER, geo_dist


class TestThreeChainNet(unittest.TestCase):
    def test_shun_and_ni(self):
        net = ThreeChainNet()
        net.shun(9 * 7)
        self.assertGreater(geo_dist(net.pos), 30)
        steps = net.ni()
        self.assertIsNotNone(steps)
        self.assertEqual(net.pos, CENTER)

    def test_repeatable(self):
        results = []
        for _ in range(3):
            net = ThreeChainNet()
            net.shun(9 * 7)
            steps = net.ni()
            results.append((net.pos, steps))
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])


if __name__ == "__main__":
    unittest.main()
