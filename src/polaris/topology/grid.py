# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Topology Grid
九宫三维坐标映射、距离计算与空间形态（五形）分类。
"""

from typing import List, Dict, Set, Tuple
from itertools import combinations

# 活跃宫的 3D 坐标映射 (1-9)
COORDS: Dict[int, Tuple[int, int, int]] = {
    9: (1, 1, 1), 4: (5, 1, 1), 3: (5, 5, 1), 8: (1, 5, 1),
    7: (1, 1, 5), 2: (5, 1, 5), 6: (1, 5, 5), 1: (5, 5, 5),
    5: (3, 3, 3)
}

# 预定义的面与截面
FACES = [{1, 2, 3, 4}, {6, 7, 8, 9}, {1, 3, 6, 8}, {2, 4, 7, 9}, {1, 2, 6, 7}, {3, 4, 8, 9}]
DIAG_SECTIONS = [{1, 3, 7, 9}, {2, 4, 6, 8}, {1, 2, 8, 9}, {3, 4, 6, 7}, {1, 4, 6, 9}, {2, 3, 7, 8}]

class GridGeometry:
    """九宫几何计算器"""
    
    @staticmethod
    def dist_sq(a: int, b: int) -> int:
        """计算两个状态节点之间的欧氏距离平方"""
        pa, pb = COORDS[a], COORDS[b]
        return sum((x - y) ** 2 for x, y in zip(pa, pb))

    @staticmethod
    def classify_tetra(numbers: List[int]) -> dict:
        """
        对 4 个节点构成的子图进行分类。
        返回形态 (生/化/变/恒/空) 及其几何属性。
        """
        nums = list(numbers)
        result = {"valid": False, "numbers": nums, "form": "未知", "volume": None}
        
        # 基础校验
        if len(nums) != 4 or len(set(nums)) != 4 or 5 in nums:
            result["reason"] = "输入必须为4个不重复且不含5的节点"
            return result
        if any(n not in COORDS for n in nums):
            result["reason"] = "节点必须存在于1-9中"
            return result

        result["valid"] = True
        s = set(nums)

        # 共面判定 (剔除)
        if s in FACES or s in DIAG_SECTIONS:
            result.update({"coplanar": True, "form": "空", "volume": 0.0})
            return result

        # 基于距离分布的模式识别
        ds = sorted(GridGeometry.dist_sq(a, b) for a, b in combinations(nums, 2))
        result["dist_sq"] = ds
        
        if ds == [1, 1, 1, 2, 2, 2]:
            form = "生"
        elif ds == [1, 1, 1, 2, 2, 3]:
            form = "化"
        elif ds == [1, 1, 2, 2, 2, 3]:
            form = "变"
        elif ds == [2, 2, 2, 2, 2, 2]:
            form = "恒"
        else:
            form = "未知"

        result["form"] = form
        result["volume"] = 1.0/6.0 if form in ["生", "化", "变"] else (1.0/3.0 if form == "恒" else None)
        return result
