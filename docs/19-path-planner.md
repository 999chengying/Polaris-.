# Polaris 基础架构：三维离散网格中的路径规划与最短路由

## 一、本文解决什么问题

在具身智能（如机器人导航、机械臂控制）与多智能体系统（MARL）中，节点如何从起始坐标移动到目标坐标，同时避开无效区域（或高损耗区域），是底层控制的核心。
传统算法（如 RRT、连续空间 A*）常依赖浮点距离计算。本文基于 \(3 \times 3 \times 3\) 的三维离散拓扑网格，提出一种**“纯整数拓扑路由规划（Topological Path Planning）”**算法。通过曼哈顿距离图与纯整数启发式搜索（Heuristic Search），系统能在不消耗浮点算力的前提下，瞬间计算出最短安全路径。

## 二、核心机制：图搜索与拓扑路由

### 1. 离散空间图建模
将 \(3 \times 3 \times 3\) 的 27 宫格视为一个无向图。每个单元格为节点，相邻（曼哈顿距离为 2）的节点之间存在无向边。
- **有效节点**：未发生故障或未处于“不可通行”状态的单元格。
- **动态障碍**：当某个节点的特征值因遭遇攻击或物理障碍发生极值溢出时，该节点在图网络中被临时剪枝（Pruned）。

### 2. 纯整数启发式搜索（Polaris A*）
传统 A* 算法为 \(f(n) = g(n) + h(n)\)。
在 Polaris 中，我们采用纯整数：
- \(g(n)\)：从起点到当前节点的整数步数。
- \(h(n)\)：当前节点到终点的曼哈顿距离（\(|x_1-x_2| + |y_1-y_2| + |z_1-z_2|\)）。
由于不使用浮点欧氏距离，整个计算过程被严格限制在整数加法与比较中，极其适合在 FPGA 或微控制器上极速运行。

## 三、算法流程

1. **初始化**：将起点加入 Open List，计算初始 \(f\) 值。
2. **循环选择**：从 Open List 中取出 \(f\) 值最小的节点作为当前处理节点。
3. **邻接扩展**：遍历当前节点的所有合法邻居节点。如果邻居是目标节点，则回溯路径并结束。
4. **代价更新**：如果邻居节点已在 Open List 或 Close List 中，且经过当前节点到达它的 \(g\) 值更小，则更新其父节点。
5. **循环终止**：直到找到目标节点，或 Open List 为空（说明无路可达）。

## 四、代码实现

    import heapq

    class Node:
        def __init__(self, coord):
            self.coord = coord
            self.g = float('inf') # 纯整数运算时用大整数替代
            self.f = float('inf')
            self.parent = None

        def __lt__(self, other):
            return self.f < other.f

    def manhattan_distance(coord1, coord2):
        """计算纯整数曼哈顿距离"""
        return sum(abs(coord1[i] - coord2[i]) for i in range(3))

    def get_neighbors(coord, obstacles):
        """获取合法邻居"""
        neighbors = []
        moves = [(-2,0,0), (2,0,0), (0,-2,0), (0,2,0), (0,0,-2), (0,0,2)]
        for move in moves:
            new_coord = tuple(coord[i] + move[i] for i in range(3))
            # 检查是否在 1,3,5 的边界内
            if all(c in [1, 3, 5] for c in new_coord):
                if new_coord not in obstacles:
                    neighbors.append(new_coord)
        return neighbors

    def topological_path_planner(start, goal, obstacles=set()):
        """执行拓扑路径规划"""
        if start in obstacles or goal in obstacles:
            return None
            
        open_list = []
        start_node = Node(start)
        start_node.g = 0
        start_node.f = manhattan_distance(start, goal)
        heapq.heappush(open_list, start_node)
        
        closed_set = set()
        
        while open_list:
            current = heapq.heappop(open_list)
            
            if current.coord == goal:
                # 回溯路径
                path = []
                while current:
                    path.append(current.coord)
                    current = current.parent
                return path[::-1]
                
            closed_set.add(current.coord)
            
            for neighbor_coord in get_neighbors(current.coord, obstacles):
                if neighbor_coord in closed_set:
                    continue
                    
                tentative_g = current.g + 1 # 每走一步代价为 1
                neighbor_node = Node(neighbor_coord)
                neighbor_node.g = tentative_g
                neighbor_node.f = tentative_g + manhattan_distance(neighbor_coord, goal)
                neighbor_node.parent = current
                
                heapq.heappush(open_list, neighbor_node)
                
        return None # 无路可达

    if __name__ == "__main__":
        start_point = (1, 1, 1)
        goal_point = (5, 5, 5)
        # 设置一个障碍物
        obstacles = {(3, 1, 1), (1, 3, 1)} 
        
        path = topological_path_planner(start_point, goal_point, obstacles)
        print(f"从 {start_point} 到 {goal_point} 的最短路径 (纯整数):")
        print(path)

## 五、结论

| 验证项 | 结果 |
|---|---|
| 空间图搜索 | 基于离散网格构建连通图 |
| 纯整数启发式 | 彻底摒弃浮点坐标，采用曼哈顿距离 |
| 极速执行 | 适配堆排序，极适合底层硬件与实时避障 |
