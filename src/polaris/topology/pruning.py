# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
Polaris Topology Pruning
图网络的子图剪枝规则。
"""

from itertools import combinations
from .grid import GridGeometry, COORDS

class SubgraphPruner:
    """子图剪枝器"""
    
    @staticmethod
    def parent_retreat(pole: int, combo: list) -> bool:
        """父母退位规则：生数极点(1-4)不与9同组，成数极点(6-9)不与1同组"""
        if pole in (1, 2, 3, 4) and 9 in combo:
            return False
        if pole in (6, 7, 8, 9) and 1 in combo:
            return False
        return True

    @classmethod
    def prune_candidates(cls, pole: int, opposite_vertices: list, include_empty: bool = False) -> dict:
        """
        基于极点，从对侧顶点中筛选合法组合。
        """
        if pole not in COORDS or pole == 5:
            raise ValueError("极点必须是 1-9 且不含 5")

        candidates = []
        for combo in combinations(opposite_vertices, 3):
            combo = list(combo)
            if 5 in combo or pole in combo or len(set(combo)) != 3:
                continue
            if not cls.parent_retreat(pole, combo):
                continue
                
            four = [pole] + combo
            result = GridGeometry.classify_tetra(four)
            
            if not result["valid"]:
                continue
            if result["form"] == "空" and not include_empty:
                continue
                
            candidates.append(result)

        # 按形态分组
        grouped = {}
        for c in candidates:
            grouped.setdefault(c["form"], []).append(c)
        return grouped
