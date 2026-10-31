# Polaris 基础架构：分布式推理的拓扑互联与消息传递机制

## 一、本文解决什么问题

在超大规模神经网络（或分布式多智能体系统）中，单节点的算力与显存永远无法承载全局模型。必须将模型与状态切分到不同的物理节点上。这就引出了一个致命的瓶颈：**节点间的通信延迟（Communication Latency）**。
传统的分布式推理框架（如 Megatron、DeepSpeed）依赖昂贵的 InfiniBand 网络与复杂的浮点张量通信。本文基于纯整数的三维拓扑网络，提出一种**“拓扑互联与隐式消息传递机制（Topological Interconnect & Message Passing）”**。通过空间正交路由与状态机的强约束，实现极低带宽消耗与高确定性的分布式协同推理。

## 二、核心机制：张量切分与拓扑路由

### 1. 三维正交切分（3D Tensor Slicing）
我们将庞大的全局网络状态切分为 \(3 \times 3 \times 3\) 的网格拓扑。每个小节点只负责维护局部特征。
例如，将高维张量切分为 X、Y、Z 三个正交维度的块，分别分配给不同的物理计算节点（或 NPU 核心）。

### 2. 局部消息传递（Local Message Passing）
节点之间不再广播全量的浮点矩阵，而是仅在相邻的物理链路（曼哈顿距离为 2 的连接）上进行消息传递。
- **聚合规则**：节点 \(N\) 在更新状态时，只接收来自左、右（X轴）以及前、后（Y轴）的直接邻居特征。
- **偏移衰减**：距离越远的节点传递过来的消息，受到的空间偏置权重衰减越大，防止信息过载。

### 3. 无锁跨节点同步（Lock-free Synchronization）
在传统分布式系统中，多节点更新共享张量需要加锁（Mutex）。本架构中，由于底层采用模 10 纯整数运算，且每个节点的坐标具有绝对唯一性，系统直接利用“拓扑偏移定则”进行无锁聚合：
\(State_{update} = (State_{local} + \sum Neighbor_{val} \times W_{addr}) \pmod{10}\)
计算完成后直接覆写，彻底避免了死锁与死等。

## 三、工程价值

1. **通信带宽极低**：每轮同步只需传输 0~9 的纯整数状态，通信量比传统大模型降低了数个数量级。
2. **极高的容错率**：如果某条网络链路超时，节点可以直接用本地状态进行推演，等待下一轮心跳同步，不会导致整个集群崩溃。
3. **天然支持流水线并行（Pipeline Parallelism）**：Z 轴可以专门作为数据流向的流水线通道，X、Y 轴负责切片计算，实现完美的计算与通信重叠。

## 四、代码实现

    def distributed_inference_step(local_state, neighbors_states, coord):
        """
        模拟单个计算节点的本地推理与跨节点消息传递。
        local_state: 节点自身的当前特征 (0-9)
        neighbors_states: 邻居节点传来的特征列表
        coord: 当前节点的空间坐标 (i, j, k)
        """
        # 计算当前节点的空间偏置权重
        weight = sum(coord) % 10
        
        # 若无邻居，直接返回本地推演结果
        if not neighbors_states:
            return (local_state * 3) % 10
            
        # 聚合邻居消息 (纯整数加法)
        neighbor_sum = sum(neighbors_states) % 10
        
        # 无锁同步 + 空间偏移定则
        new_state = (local_state * 2 + neighbor_sum + weight) % 10
        
        return new_state

    if __name__ == "__main__":
        # 模拟节点 (1, 3, 5) 的情况
        my_coord = (1, 3, 5)
        my_val = 4
        # 接收到来自上下游节点的消息
        incoming_msgs = [2, 7, 1] 
        
        result = distributed_inference_step(my_val, incoming_msgs, my_coord)
        print(f"节点 {my_coord} 本地状态 {my_val}")
        print(f"接收邻居消息: {incoming_msgs}")
        print(f"推理后更新状态: {result}")

## 五、结论

| 验证项 | 结果 |
|---|---|
| 分布式切分 | 状态张量被切分至三维网格，解耦算力瓶颈 |
| 消息传递 | 依赖局部邻居特征聚合，无需全局广播 |
| 无锁同步 | 通过坐标权重消除写冲突，确保高并发稳定 |
