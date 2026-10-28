# -*- coding: utf-8 -*-
"""
Polaris V9: 极化拓扑注意力网络 (Polarized Topological Attention)
- 基于 7 个 5 的分布式 MoE 架构
- 向量点乘打分 + 平局断点硬路由 + 残差回传
依据：docs-v4/01-polarized-attention-architecture.md
"""

def mod10(x):
    return x % 10

def vec_mod10(vec):
    return [v % 10 for v in vec]

def dot_product(v1, v2):
    """纯整数点乘"""
    return sum(a * b for a, b in zip(v1, v2))

class Node5:
    """分布式 5 节点（微型专家）"""
    def __init__(self, name, weight_vec):
        self.name = name
        self.weight = weight_vec

    def forward(self, input_vec):
        score = dot_product(input_vec, self.weight)
        out_vec = [v * w for v, w in zip(input_vec, self.weight)]
        return mod10(score), vec_mod10(out_vec)

class PolarizedAttentionLayer:
    def __init__(self):
        # 7 个 5 节点，各自具备独立权重
        self.nodes = [
            Node5("中央太极", [5, 5]),
            Node5("一号炉左", [3, 8]),
            Node5("一号炉右", [7, 2]),
            Node5("二号炉前", [1, 6]),
            Node5("二号炉后", [9, 4]),
            Node5("外骨骼下", [2, 7]),
            Node5("外骨骼上", [8, 3])
        ]

    def attention_route(self, input_vec):
        scores = []
        for node in self.nodes:
            score, _ = node.forward(input_vec)
            scores.append(score)
        
        max_score = max(scores)
        
        # 拓扑平局断点：取最高分且索引最靠前的节点
        winner_idx = scores.index(max_score)
        winner_node = self.nodes[winner_idx]
        
        _, out_vec = winner_node.forward(input_vec)
        
        # 拓扑残差回传
        final_output = [mod10(input_vec[d] + out_vec[d]) for d in range(len(input_vec))]
        return final_output, winner_node.name

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris V9 极化拓扑注意力网络")
    print("=" * 60)
    
    attn_layer = PolarizedAttentionLayer()
    test_vectors = [[2, 7], [5, 5], [8, 3], [1, 9]]
    
    for vec in test_vectors:
        out, winner = attn_layer.attention_route(vec)
        print(f"输入: {vec} | 激活胜者: {winner} | 输出: {out}")
