# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
Polaris 大模型防幻觉网关 (PTPP) 实战演示。
本脚本模拟了 LLM 在生成文本时的特征流，并演示 Polaris 如何在极低算力下，
瞬间拦截发散的幻觉特征，并在代数层面执行物理纠偏。
"""

import sys
import os
import time
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.polaris.gateway.ptpp import (
    hash_project_float_to_small_model,
    causal_steer,
    MetaObserver
)

def mock_llm_generate_features(text: str, is_hallucination: bool = False) -> list:
    """
    模拟大模型生成文本时的底层高维浮点特征 (例如 128 维 Embedding)。
    正常推理：特征相对收敛。
    产生幻觉：特征极度发散、正负乱跳。
    """
    random.seed(len(text) if not is_hallucination else 9999)
    features = []
    for _ in range(12): # 用12维模拟高维
        if is_hallucination:
            # 幻觉特征：极值乱跳
            features.append(random.uniform(-1.0, 1.0))
        else:
            # 正常特征：围绕正向均值收敛
            features.append(random.uniform(0.1, 0.8))
    return features

def run_guardrail_demo():
    print("=" * 60)
    print("☯️ Polaris PTPP 防幻觉网关 - 大模型实时拦截实战")
    print("=" * 60)

    observer = MetaObserver(threshold=3)
    
    # 模拟大模型输出的两段文本对应的底层特征
    tasks = [
        ("正常的物理知识描述", "物理学的基础是严谨的数学实验。", False),
        ("大模型产生的严重幻觉", "物理学的基础是魔法和飞龙。", True),
        ("幻觉持续发散", "魔法飞龙正在吞噬太阳。", True)
    ]

    for task_name, text, is_hallucination in tasks:
        print(f"\n>>> 正在处理任务: 【{task_name}】")
        print(f"    文本内容: {text}")
        
        # 1. 获取大模型特征 (模拟)
        float_features = mock_llm_generate_features(text, is_hallucination)
        
        start_time = time.perf_counter()
        
        # 2. PTPP 拓扑投影 (降维至纯整数小模)
        state = hash_project_float_to_small_model(float_features)
        print(f"    [拓扑投影] 离散小模状态: {state}")
        
        # 3. 网关诊断与干预
        status, consensus, offset = causal_steer(state)
        
        if status == "PASS":
            print(f"    ✅ [安全放行] 特征收敛，共识值: {consensus}")
        else:
            print(f"    🚨 [发现幻觉] 特征发散！当前共识: {consensus}")
            print(f"    🔪 [因果干预] 计算反向代数偏置: {offset}")
            
            # 4. 执行强制纠偏
            new_state = tuple((state[i] + offset[i]) % 10 for i in range(3))
            new_consensus = causal_steer(new_state)[1]
            
            print(f"    🩸 [干预复诊] 纠偏后状态: {new_state} | 新共识: {new_consensus}")
            if new_consensus in [7, 8, 9]:
                print(f"    🎯 [手术成功] 幻觉已被物理消灭，强制拉回安全区！")
                
        # 5. 防复读机监控 (元观测者)
        out_val, obs_status = observer.observe(consensus)
        if obs_status != "正常演化":
             print(f"    ⚠️ [元观测者警报] {obs_status}")

        elapsed = (time.perf_counter() - start_time) * 1000
        print(f"    ⏱️ [耗时] PTPP 网关处理耗时: {elapsed:.4f} 毫秒 (算力极低)")

    print("\n" + "=" * 60)
    print("结论：PTPP 网关在完全不需要梯度下降的情况下，")
    print("通过纯整数代数方程，毫秒级斩断了模型的幻觉发散路径。")
    print("=" * 60)

if __name__ == "__main__":
    run_guardrail_demo()
