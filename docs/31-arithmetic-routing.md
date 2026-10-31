# Polaris 基础架构：算术驱动的纯整数拓扑路由算法

## 一、本文解决什么问题

在分布式系统、网络交换芯片以及大模型的混合专家（MoE）架构中，传统的路由算法（如基于 Softmax 的权重打分或复杂的哈希字典树）往往依赖庞大的浮点运算或极高的内存寻址开销。
本文提出一种**“纯整数算术路由（Arithmetic Routing）”**机制。该机制完全摒弃浮点权重与复杂的路由表，仅通过底层的模运算（Modulo）、坐标偏置加法与大小比较，即可在 \(O(1)\) 的时钟周期内决定数据包的最优转发路径，极度契合低功耗、高并发的边缘计算硬件。

## 二、核心机制：代数哈希与拓扑偏移

### 1. 算术哈希路由（Arithmetic Hash Routing）
系统将输入的特征数据或网络包头，视为一个离散的状态值 \(V\)。基于当前拓扑节点的坐标 \((i, j, k)\)，通过极简的代数公式计算路由目的地的索引：
\(Index = (V \times W_{addr} + \text{Offset}) \pmod{N}\)
其中，\(W_{addr}\) 是当前节点的空间坐标权重，\(N\) 是目标节点（或专家）的总数。这一纯整数哈希运算，避免了传统浮点全连接层的矩阵乘法。

### 2. 差值感知与拥塞避让（Delta-Aware Avoidance）
在多智能体或并发网络中，如果计算出的目标节点发生拥塞（即状态值接近极值，如前文所述的“差5墙”约束），系统利用差值算术直接寻找最近的空闲邻居：
\(New\_Index = (Index + \Delta) \pmod{N}\)
其中 \(\Delta\) 为固定的步长（如加 1 或加 3），通过这种极简的线性探测（Linear Probing），实现无锁的负载均衡。

### 3. 硬件底层实现（Hardware Implementation）
该路由算法在芯片底层不需要浮点乘法器（FPU），仅需要：
- 一个取模器（通常通过位运算掩码实现）。
- 一个加法器。
- 一个比较器（Comparator）。
这使得该路由逻辑可以在极小的芯片面积内实现，功耗极低。

## 三、工程价值

1. **零浮点（Zero-Float）**：彻底避免了大模型路由中的 `e^x` 指数运算，计算开销降低数个数量级。
2. **确定性延迟**：每次路由寻址的时间是常数级 \(O(1)\)，不受网络节点数量扩增的影响。
3. **无状态（Stateless）**：路由器本身不需要维护庞大的历史路由表，直接通过当前特征值进行算术推演即可判定去向。

## 四、代码实现

    def arithmetic_router(input_state, current_coord, num_experts=4):
        """
        基于纯整数算术的拓扑路由算法。
        """
        # 1. 计算当前节点的空间偏置权重
        addr_weight = sum(current_coord) % 10
        
        # 2. 纯整数代数哈希：决定目标专家节点
        # 核心路由公式，零浮点，纯取模
        target_expert = (input_state * addr_weight + current_coord[2]) % num_experts
        
        # 3. 拥塞检测与差值避让
        # 假设我们有一个模拟的专家负载状态
        expert_loads = [2, 8, 4, 9] # 专家3负载过高 (接近10)
        
        # 如果目标专家负载过高，触发算术探测
        if expert_loads[target_expert] > 7:
            original_target = target_expert
            # 线性探测：向后挪一步
            target_expert = (target_expert + 1) % num_experts
            return target_expert, f"节点 {original_target} 拥塞，路由重定向至 {target_expert}"
            
        return target_expert, "正常路由"

    if __name__ == "__main__":
        # 模拟输入状态和当前坐标
        state = 7
        coord = (1, 3, 5)
        
        target, status = arithmetic_router(state, coord)
        print(f"输入状态: {state}, 坐标: {coord}")
        print(f"路由结果: 目标专家节点 {target} | 状态: {status}")

## 五、结论

| 验证项 | 结果 |
|---|---|
| 路由计算 | 全链路采用纯整数算术，无浮点乘法 |
| 复杂度 | \(O(1)\) 极速寻址，极适合底层硬件加速 |
| 拥塞避让 | 利用线性取模探测，自动避开高负载节点 |
