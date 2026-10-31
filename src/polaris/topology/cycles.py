# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
Polaris Topology Cycles
基于模24群作用的循环遍历分析。
"""

import math
from typing import List, Dict, Any

MOUNTAINS = [
    {"name": "子", "palace": 1, "number": 7}, {"name": "癸", "palace": 1, "number": 8},
    {"name": "丑", "palace": 8, "number": 3}, {"name": "艮", "palace": 8, "number": 4},
    {"name": "寅", "palace": 8, "number": 2}, {"name": "甲", "palace": 3, "number": 8},
    {"name": "卯", "palace": 3, "number": 7}, {"name": "乙", "palace": 3, "number": 6},
    {"name": "辰", "palace": 4, "number": 6}, {"name": "巽", "palace": 4, "number": 8},
    {"name": "巳", "palace": 4, "number": 7}, {"name": "丙", "palace": 9, "number": 4},
    {"name": "午", "palace": 9, "number": 3}, {"name": "丁", "palace": 9, "number": 2},
    {"name": "未", "palace": 2, "number": 7}, {"name": "坤", "palace": 2, "number": 6},
    {"name": "申", "palace": 2, "number": 8}, {"name": "庚", "palace": 7, "number": 2},
    {"name": "酉", "palace": 7, "number": 3}, {"name": "辛", "palace": 7, "number": 4},
    {"name": "戌", "palace": 6, "number": 4}, {"name": "乾", "palace": 6, "number": 2},
    {"name": "亥", "palace": 6, "number": 3}, {"name": "壬", "palace": 1, "number": 6},
]

class CycleAnalyzer:
    """二十四山循环分析器"""
    
    @staticmethod
    def analyze_cycle(K: int, start_name: str = "子") -> Dict[str, Any]:
        """
        分析给定步长 K 和起点时的循环状态。
        """
        if K <= 0:
            raise ValueError("步长 K 必须为正整数")
            
        names = [m["name"] for m in MOUNTAINS]
        if start_name not in names:
            raise ValueError(f"起点必须是二十四山之一，如 {names[0]}")
            
        start_idx = names.index(start_name)
        g = math.gcd(24, K)
        segments = 24 // g
        circles = K // g

        segs = []
        for n in range(segments):
            idx = (start_idx + n * K) % 24
            m = MOUNTAINS[idx]
            cumulative = n * K
            segs.append({
                "segment": n,
                "cumulative_steps": cumulative,
                "circle": cumulative // 24,
                "mountain": m["name"],
                "palace": m["palace"],
                "number": m["number"],
            })

        return {
            "K": K,
            "start": start_name,
            "gcd": g,
            "segments": segments,
            "circles": circles,
            "details": segs
        }
