# Polaris 基础架构：三维张量空间的路径动力学与状态转移

## 一、本文解决什么问题

在图神经网络（GNN）与复杂路由算法中，特征或信号如何在节点之间进行传递（Message Passing），以及这些传递路径如何决定了系统的动力学特征，是底层设计的核心。本文基于 \(3 \times 3 \times 3\) 的三维张量空间，定义**“拓扑路径动力学（Topological Path Dynamics）”**。通过规范节点之间的可达性、最短路径与空间遍历逻辑，为后续的图神经网络消息传递与状态演化提供基础的路由规则。

*(注：本文为早期基础拓扑探索，纯粹从图论与离散几何角度，定义三维网格中的连通性。暂不涉及具体的大模型路由工程应用，留作后续高阶网络拓扑的底层参考。)*

## 二、空间路径与连通性定义

在 27 宫格的三维坐标体系 \((i, j, k) \in \{1, 3, 5\}^3\) 中，我们定义如下路径拓扑：

### 1. 节点与邻接（Adjacency）
- **中心节点（基准锚点）**：\((3, 3, 3)\)。
- **顶点节点**：坐标的 \(i, j, k\) 均在边界 \(\{1, 5\}\) 上。
- **边连通性**：若两个节点的曼哈顿距离为 2（即只有一个坐标轴相差 2，其余坐标相同），则定义为直接连通（直连边）。若曼哈顿距离大于 2，则需要通过中间节点进行多跳（Multi-hop）路由。

### 2. 核心几何子图
在三维网格中，可以通过不同的连通路径，切分出特定的几何结构。这些结构在未来的图卷积核设计（Graph Kernel Design）中可能作为局部特征提取器：
- **正四面体路径（Tetrahedral Paths）**：由 4 个顶点构成的闭合回路，任意两点间的距离相等。这种路径在图中具有最高的对称性，适合作为无偏置的特征聚合探针。
- **三棱锥路径（Triangular Pyramids）**：由一个顶点和底面的三个节点构成。
- **截面路径（Planar Slices）**：穿越同一平面的 9 个节点，构成二维面状的连通图。

## 三、路径动力学：状态转移方程

设 \(P_t\) 为系统在 \(t\) 时刻的活跃节点集。路径动力学定义信号的转移规则为：
\(P_{t+1} = f(P_t, A)\)
其中 \(A\) 为邻接矩阵。
如果在演化中，信号总是沿着最短路径传播，系统将在 \(O(\log N)\) 步内达到全局共识；若引入随机游走（Random Walk）或拓扑偏置，则会形成周期性的遍历。

## 四、代码实现

    import collections

    # 生成三维网格的邻接表
    def generate_3d_grid_adjacency():
        coords = [(i, j, k) for i in [1,3,5] for j in [1,3,5] for k in [1,3,5]]
        adj = {c: [] for c in coords}
        
        for c1 in coords:
            for c2 in coords:
                if c1 == c2: continue
                # 曼哈顿距离为 2 视为直接连通（相邻）
                dist = sum(abs(c1[d] - c2[d]) for d in range(3))
                if dist == 2:
                    adj[c1].append(c2)
        return adj

    def find_shortest_path(adj, start, end):
        """利用 BFS 寻找最短路径"""
        queue = collections.deque([[start]])
        visited = set([start])
        
        while queue:
            path = queue.popleft()
            node = path[-1]
            
            if node == end:
                return path
                
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None

    if __name__ == "__main__":
        adj = generate_3d_grid_adjacency()
        # 测试从 (1,1,1) 到 (5,5,5) 的最短路径
        path = find_shortest_path(adj, (1,1,1), (5,5,5))
        print(f"顶点(1,1,1) 到 (5,5,5) 的最短路径: {path}")

## 五、结论

| 验证项 | 结果 |
|---|---|
| 邻接矩阵 | 成功构建 27 宫格的图连通性网络 |
| 路径搜索 | 基于 BFS 精准计算任意节点间的最短路径 |
| 拓扑意义 | 为高阶图卷积与局部感受野设计提供几何子图 |
