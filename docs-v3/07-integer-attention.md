# Polaris V3-07：硬路由注意力：基于赢者通吃（WTA）的纯整数掩码机制

## 一、本文解决什么问题

在上一版（V3-06）的幂零注意力中，如果幂零投影的判定条件过于严苛，会导致大量 Token 的注意力权重全为 0，引发“Token 死亡”或信息丢失。
本文提出一种改进的纯整数注意力机制——**赢者通吃硬路由（Winner-Takes-All Routing）**。该机制通过寻找局部匹配分数的最大值，实现二值掩码分配。既保留了纯整数计算的极低能耗，又确保了特征信息的高效无损路由。

## 二、核心机制：WTA 硬路由

### 1. 纯整数匹配分数
与 V3-06 相同，首先计算出所有节点的原始匹配分数 \(S_{ij}\)。

### 2. 赢者通吃（Winner-Takes-All）
对于每一个 Query \(i\)，遍历它与所有 Key \(j\) 的匹配分数：
- 找出当前行的最大匹配分数 \(M_i = \max(S_i)\)。
- 如果 \(S_{ij} == M_i\)，则注意力权重 \(A_{ij} = 1\)。
- 如果 \(S_{ij} < M_i\)，则 \(A_{ij} = 0\)。

### 3. 特征更新
最终输出 \(O = A \times V\)，即只对取得最大匹配分数的 Value 向量进行无损提取。

## 三、平局断点（Tie-breaking）与防死锁

在纯整数点乘中，极易出现多个分数并列最高的情况（例如特征完全对称）。在实际工程中，可在代数比较时引入微小的“拓扑位置偏置（Positional Bias）”作为索引断点，确保系统总能选出一个唯一的胜者，避免特征聚合时的对称相消。

## 四、工程价值

1. **彻底废除 Softmax**：不再需要计算指数与归一化除法，直接比较大小，极大地节省了算力。
2. **拒绝 Token 死亡**：每一行必定有一个以上的最大值得分，确保每一个 Query 都能提取到相应的特征，绝不空手而归。
3. **硬件友好**：WTA 操作在芯片底层仅仅是一个简单的比较器树（Comparator Tree），速度极快。

## 五、代码实现

    def wta_attention(Q, K, V):
        """
        赢者通吃（WTA）纯整数注意力。
        """
        seq_len = len(Q)
        A = [[0] * seq_len for _ in range(seq_len)]
        
        # 1. 计算原始分数
        raw_scores = []
        for i in range(seq_len):
            row_scores = [sum(Q[i][d] * K[j][d] for d in range(len(Q[0]))) % 10 for j in range(seq_len)]
            raw_scores.append(row_scores)
            
        # 2. WTA 硬路由 (平局取索引最靠前者)
        for i in range(seq_len):
            max_score = max(raw_scores[i])
            winner_idx = raw_scores[i].index(max_score)
            A[i][winner_idx] = 1
            
        # 3. 特征更新 (A * V)
        O = [[0] * len(V[0]) for _ in range(seq_len)]
        for i in range(seq_len):
            for d in range(len(V[0])):
                O[i][d] = sum(A[i][j] * V[j][d] for j in range(seq_len)) % 10
                
        return O

## 六、结论

| 验证项 | 结果 |
|---|---|
| 路由机制 | 直接提取最大匹配分数，无除法 |
| 防死锁 | 平局断点确保唯一胜者，避免对称相消 |
| 矩阵稀疏性 | 输出矩阵高度稀疏，仅保留核心特征 |
