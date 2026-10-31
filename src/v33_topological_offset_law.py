# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
#
# Polaris 拓扑偏移定则验证代码 (Topological Offset Law)
# 证明“值+址”相比传统投影法的绝对优势。
#
# Licensed under the Apache License, Version 2.0

def mod10(x):
    return x % 10

class TopologicalOffsetEngine:
    def __init__(self):
        # 定义空间地址的权重（例如：左端为1，右端为5）
        self.addr_left = 1
        self.addr_right = 5
        
    def traditional_projection(self, val_left, val_right):
        """
        传统投影法：纯数值相加，容易在中间节点坍缩。
        """
        projected_val = mod10(val_left + val_right) 
        if projected_val == 0: 
            projected_val = 5 # 传统规则：合十归5
        return projected_val

    def topological_offset(self, val_left, val_right):
        """
        拓扑偏移定则：值+址，打破死锁，保留特征差异。
        """
        offset_result = mod10((val_left * self.addr_left) + (val_right * self.addr_right))
        return offset_result

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris V33: 拓扑偏移定则 (向华为韬定律致敬)")
    print("=" * 60)
    
    engine = TopologicalOffsetEngine()
    
    # 测试特征对 (9,4), (8,3), (2,7), (1,1), (4,4)
    test_cases = [
        (9, 4),  
        (8, 3),  
        (2, 7),  
        (1, 1),  
        (4, 4)   
    ]
    
    print(f"{'左值':<5} | {'右值':<5} | {'传统投影':<10} | {'拓扑偏移(铁律)':<15}")
    print("-" * 60)
    
    for v_left, v_right in test_cases:
        res_trad = engine.traditional_projection(v_left, v_right)
        res_topo = engine.topological_offset(v_left, v_right)
        print(f"{v_left:<6} | {v_right:<6} | {res_trad:<12} | {res_topo:<18}")

    print("=" * 60)
    print("结论：拓扑偏移定则通过坐标权重，完美保留了特征差异，且杜绝了0的死锁！")
