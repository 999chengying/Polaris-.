# Polaris 基础架构：预定义拓扑链路的连通性检测与故障节点定位

## 一、本文解决什么问题

在分布式计算网络、多智能体通信或图神经网络的底层路由中，节点的硬件失效或通信阻断会导致数据流中断。传统的全网扫描定位法能耗极高且延迟大。
本文提出一种**“基于拓扑链路的故障树分析（Fault Tree Analysis, FTA）”**算法。系统预设多条贯穿全局的关键拓扑链路，通过实时监测这些链路的连通状态，利用集合逻辑进行反向推断，从而在不进行高开销全网扫描的前提下，实现单点故障（Single Point of Failure）的秒级精准定位与容错重路由。

> **注：拓扑渊源**
> 本文所采用的预设链路结构（如正交十字链路、对角交叉链路、闭环包络等），其拓扑灵感源自传统洛书模型中的“四正四维”及八卦方位排布。传统模型用这些路径来解释方位与能量的流转，本文则将其转化为现代网络拓扑中的链路测试探针，以此向古代先哲对空间网络连接的全局观致敬。

## 二、预定义拓扑链路模型

我们基于 1~9 的九宫节点空间，定义四种代表性的全局测试链路（Link Paths）：

1. **正交十字链路（Orthogonal Cross）**：`[1, 3, 9, 7, 1]`（穿越上下左右的四正位节点）。
2. **对角交叉链路（Diagonal Cross）**：`[2, 4, 8, 6, 2]`（穿越四个角落的节点）。
3. **跨区包络链路（Cross-Zone Envelope）**：`[1, 3, 6, 8, 1]` 与 `[2, 4, 7, 9, 2]`。
4. **对角截面对称链路（Diagonal Slices）**：`[3, 4, 8, 9, 3]` 与 `[1, 2, 6, 7, 1]`。

这些链路组成了覆盖整个网络的“探针网”。当系统正常运行时，所有链路均为闭合（连通）状态；当某节点失效时，穿过该节点的所有链路将同时断开。

## 三、故障节点定位算法

### 1. 信号采集
系统周期性向上述所有链路发送握手信号，记录每条链路的通断状态（True/False），形成故障状态向量。

### 2. 逆向推导（Model-based Diagnosis）
遍历所有可能失效的节点（1~9，排除中心基准态）。假设该节点是故障源，生成预期的“理论故障状态向量”。
将“实际观测向量”与所有“理论向量”进行比对，完全匹配的节点，即为真正的故障源。

### 3. 容错重路由
一旦定位到故障节点，系统立刻在图拓扑中将其标记为不可用（Pruned），并依据冗余路径重新计算消息传递流（例如绕开失效节点，走差1墙或差2墙的旁路）。

## 四、代码实现

    # 预定义拓扑链路探针
    PROBE_LINKS = {
        "ortho_cross": [1, 3, 9, 7, 1],
        "diag_cross": [2, 4, 8, 6, 2],
        "envelope_a": [1, 3, 6, 8, 1],
        "envelope_b": [2, 4, 7, 9, 2],
        "diag_slice_a": [3, 4, 8, 9, 3],
        "diag_slice_b": [1, 2, 6, 7, 1]
    }

    def get_link_status(faulty_node):
        """根据故障节点，生成实际的链路通断状态"""
        status = {}
        for name, path in PROBE_LINKS.items():
            # 若故障节点在链路中，则该链路断开（False）
            status[name] = not (faulty_node in path)
        return status

    def localize_fault_node(observed_status):
        """根据观测到的通断状态，反向定位故障节点"""
        candidates = []
        # 遍历所有可能节点（排除中心5）
        for node in [1, 2, 3, 4, 6, 7, 8, 9]:
            expected_status = get_link_status(node)
            if expected_status == observed_status:
                candidates.append(node)
        return candidates

    if __name__ == "__main__":
        # 模拟节点 3 发生物理故障
        actual_fault_node = 3
        observed = get_link_status(actual_fault_node)
        
        # 打印观测到的链路状态
        print("=== 链路探针状态 ===")
        for link, is_connected in observed.items():
            print(f"  {link}: {'通' if is_connected else '断'}")
            
        # 推断故障点
        result = localize_fault_node(observed)
        print(f"\n[定位结果] 推断故障节点为: {result}")

## 五、结论

| 验证项 | 结果 |
|---|---|
| 探针覆盖 | 正交、对角、包络等多链路覆盖所有关键节点 |
| 故障定位 | 通过比对理论状态与实际观测，精准定位单点故障 |
| 算法复杂度 | O(N) 级遍历，无需复杂的浮点计算，极适合底层硬件 |
