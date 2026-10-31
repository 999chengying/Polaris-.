# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
PTPP 防幻觉网关演示脚本。
直接运行此脚本可查看网关对异常特征的诊断与因果干预。
"""

import sys
import os

# 确保能导入 src 下的包
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.polaris.gateway.ptpp import (
    hash_project_float_to_small_model,
    causal_steer,
    MetaObserver
)
from src.polaris.core.operators import TopologicalOperators

def run_gateway_demo():
    print("=" * 50)
    print("☯️ Polaris PTPP 防幻觉网关演示")
    print("=" * 50)

    # 1. 模拟大模型输出的异常特征（128维或更高维度的浮点向量）
    # 这里用部分数据模拟“发散/幻觉”状态
    hallucination_features = [-0.98, 0.92, 0.11, -0.45, 0.88, 0.01, 0.99, -0.76, 0.33, -0.99]
    
    print(f"\n[输入] 原始高维特征: {hallucination_features[:3]} ...")
    
    # 2. 拓扑投影
    state = hash_project_float_to_small_model(hallucination_features)
    print(f"[投影] 降维至离散小模: {state}")
    
    # 3. 网关诊断与因果干预
    status, consensus, offset = causal_steer(state)
    
    if status == "PASS":
        print(f"[结果] 特征安全。共识值: {consensus}")
    else:
        print(f"[警告] 发现幻觉！当前共识: {consensus}")
        print(f"[干预] 注入代数偏置力场: {offset}")
        
        # 4. 执行干预后的状态复原
        new_state = tuple((state[i] + offset[i]) % 10 for i in range(3))
        new_consensus = causal_steer(new_state)[1]
        print(f"[复诊] 干预后状态: {new_state} | 新共识: {new_consensus}")
        
        if new_consensus in [7, 8, 9]:
            print("🎯 [结论] 手术成功！幻觉被物理消灭，拉回安全区。")
            
    # 5. 演示元观测者（防复读机）
    print("\n" + "-" * 50)
    print("☯️ 元观测者（防复读机）演示")
    print("-" * 50)
    
    observer = MetaObserver(threshold=3)
    print(f"[注入] 模拟系统连续输出死循环特征值: [3, 7, 3, 7, 3, 7]")
    sequence = [3, 7, 3, 7, 3, 7]
    
    for i, val in enumerate(sequence):
        out_val, obs_status = observer.observe(val)
        print(f"  步 {i+1}: 输入={val} | 输出={out_val} | 状态: {obs_status}")


if __name__ == "__main__":
    run_gateway_demo()
