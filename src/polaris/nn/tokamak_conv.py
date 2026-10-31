# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris TokamakConv Layer
基于纯整数拓扑与相变机制的防过平滑图神经网络层。
"""

from typing import List, Tuple

class TokamakConv:
    """
    TokamakConv 图卷积层。
    包含：过平滑检测、确定性相变（降维/激发）与位置偏置。
    """
    def __init__(self, over_smooth_threshold: float = 0.5):
        self.threshold = over_smooth_threshold

    def forward(
        self, 
        H: List[List[int]], 
        A: List[List[int]], 
        layer_idx: int
    ) -> Tuple[List[List[int]], float, bool]:
        """
        前向传播。
        
        Args:
            H: 节点特征矩阵 (N x C)
            A: 邻接矩阵 (N x N)
            layer_idx: 当前层数（用于交替相变算子）
            
        Returns:
            H_out: 更新后的特征矩阵
            variance: 聚合后的方差（特征熵）
            is_quenched: 是否触发了退火相变
        """
        N = len(H)
        C = len(H[0])
        
        # 1. 传统图网络邻居聚合 (Message Passing)
        H_agg = [[0] * C for _ in range(N)]
        for i in range(N):
            degree = sum(A[i]) or 1
            for j in range(N):
                if A[i][j] == 1:
                    for c in range(C):
                        H_agg[i][c] += H[j][c]
            for c in range(C):
                H_agg[i][c] = H_agg[i][c] // degree  # 纯整数平均
                
        # 2. 过平滑监测（计算第 0 通道特征的方差，模拟特征发散度）
        base_vals = [H_agg[i][0] % 10 for i in range(N)]
        mean_val = sum(base_vals) // N
        variance = sum((x - mean_val) ** 2 for x in base_vals) / N
        
        # 3. 确定性相变（过平滑抑制）
        is_quenched = False
        if variance < self.threshold:
            is_quenched = True
            # 根据层数奇偶，交替选择激发算子(乘3)或退火算子(乘2)
            k = 3 if layer_idx % 2 != 0 else 2
            for i in range(N):
                for c in range(C):
                    # 节点索引作为位置偏置（Positional Bias）
                    H_agg[i][c] = (H_agg[i][c] * k + i) % 10
                    
        # 4. 强制双墙约束（残差流锚点）
        H_out = []
        for i in range(N):
            row_out = []
            for c in range(C):
                val = H_agg[i][c] % 10
                if c == 0:
                    row_out.append(val)             # 通道 0：生数墙
                elif c == 1:
                    row_out.append((val + 5) % 10)  # 通道 1：成数墙 (强制差值=5)
                else:
                    row_out.append(val)
            H_out.append(row_out)
            
        return H_out, variance, is_quenched
