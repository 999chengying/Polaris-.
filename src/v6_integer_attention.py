# -*- coding: utf-8 -*-
"""
Polaris V6: 纯整数拓扑注意力 (Integer Attention)
Winner-Takes-All 硬路由，全程无浮点、无指数、无除法。
依据：docs-v3/07-integer-attention.md
"""

def mod10(x):
    return x % 10

def integer_attention_wta(Q, K, V):
    seq_len = len(Q)
    
    # 1. 计算原始 QK^T 匹配分数 (纯整数)
    raw_scores = [[0] * seq_len for _ in range(seq_len)]
    for i in range(seq_len):
        for j in range(seq_len):
            score = sum(Q[i][d] * K[j][d] for d in range(len(Q[0])))
            raw_scores[i][j] = mod10(score)
        
    # 2. 硬路由归一化 (Winner-Takes-All)
    A = [[0] * seq_len for _ in range(seq_len)]
    for i in range(seq_len):
        max_score = max(raw_scores[i])
        for j in range(seq_len):
            if raw_scores[i][j] == max_score:
                A[i][j] = 1
                
    # 3. 特征输出更新 (A * V)
    O = [[0] * len(V[0]) for _ in range(seq_len)]
    for i in range(seq_len):
        for d in range(len(V[0])):
            val = sum(A[i][j] * V[j][d] for j in range(seq_len))
            O[i][d] = mod10(val)
            
    return O

if __name__ == "__main__":
    print("=" * 55)
    print("☯️ Polaris V6 纯整数拓扑注意力")
    print("=" * 55)
    
    Q = [[2, 7], [5, 5], [8, 3]]
    K = [[8, 3], [3, 8], [1, 6]]
    V = [[4, 9], [2, 1], [7, 6]]
    
    O = integer_attention_wta(Q, K, V)
    
    print("Output O:")
    for row in O:
        print(f"  {row}")
