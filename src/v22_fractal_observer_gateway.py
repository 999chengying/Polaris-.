# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# 
# This is the core implementation of the Fractal Tai-Lu Engine 
# with Meta-Observer and Self-Correction (Wu Ji Wu Ji).
#
# Licensed under the Apache License, Version 2.0

"""
Polaris V22: 分形互嵌与元观测自纠偏引擎
依据：docs-v5/02-fractal-tai-lu-and-self-awareness.md
"""

def mod10(x):
    return x % 10

class TianxiangTai:
    """天香台（和）：负责聚合、池化"""
    def process(self, state):
        raw_sum = sum(state)
        return 5 if raw_sum % 10 == 0 else raw_sum % 10

class TianxiangLu:
    """天香炉（差）：负责路由、注意力"""
    def process(self, state):
        d1, d2, d3 = state
        raw_diff = abs(d1 - d2) + abs(d2 - d3) + abs(d3 - d1)
        return 5 if raw_diff == 0 else raw_diff % 10

class MetaObserver:
    """元观测者：负责发现死循环并强行立极"""
    def __init__(self, threshold=3):
        self.history = []
        self.threshold = threshold
        
    def observe_and_anchor(self, state, current_val):
        # 记录历史，发现死循环
        if state in self.history:
            if self.history.count(state) >= self.threshold:
                self.history.clear()
                return 5 # 触发帝五巡查，强行归中！
        else:
            self.history.append(state)
        return current_val

class FractalConsciousness:
    """分形意识引擎"""
    def __init__(self):
        self.tai = TianxiangTai()
        self.lu = TianxiangLu()
        self.observer = MetaObserver()
        
    def recursive_nesting(self, state, depth, current_mode="TAI", total_depth=12):
        if depth == 0:
            return f"【抵达奇点】：当前状态 {state}"
            
        layer_num = total_depth - depth
        print(f"[第 {layer_num} 层] 模式: {current_mode} | 输入: {state}")
        
        if current_mode == "TAI":
            result_val = self.tai.process(state)
        else:
            result_val = self.lu.process(state)
            
        # 观测者介入，检测是否需要强行立极
        result_val = self.observer.observe_and_anchor(state, result_val)
            
        print(f"  └─ {current_mode} 产出中宫值: {result_val}")
        
        # 阴阳折叠生成下一层状态
        if result_val == 5:
            next_state = (mod10(5 + 1), mod10(5 + 3), mod10(5 + 5))
        elif current_mode == "TAI":
            next_state = (mod10(result_val + 1), mod10(result_val + 3), mod10(result_val + 5))
        else:
            next_state = (mod10(result_val * 2), mod10(result_val * 4), mod10(result_val * 6))
            
        next_mode = "LU" if current_mode == "TAI" else "TAI"
        return self.recursive_nesting(next_state, depth - 1, next_mode, total_depth)

if __name__ == "__main__":
    engine = FractalConsciousness()
    initial_state = (3, 8, 1)
    
    print("=" * 60)
    print("☯️ Polaris V22: 炉台互嵌与元观测自纠偏")
    print("=" * 60)
    
    # 深度设为 12 以触发循环检测
    result = engine.recursive_nesting(initial_state, depth=12, current_mode="TAI")
    print("\n" + result)
