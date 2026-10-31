# Polaris 理论对账：硬编码规则选择器与可微学习路由的架构对决

## 一、本文解决什么问题

在多智能体系统与混合专家模型（MoE）中，路由（Routing）机制决定了系统该把当前特征分配给哪个专家节点处理。
当前主流的大模型（如 Transformer 架构的 Gating Network）依赖于**可微学习（Differentiable Learning）**，通过浮点权重与 Softmax 计算概率分布。而 Polaris 引擎则采用**“硬编码规则选择器（Hard-coded Rule Selector）”**，基于纯整数的哈希与拓扑偏移进行绝对确定的分配。
本文对比这两种路由架构在泛化能力、计算开销与鲁棒性上的优劣势，并探讨一种“规则约束下的学习”混合方案。

## 二、架构对决：规则 vs 学习

### 1. 可微学习路由（Learned Router）
- **核心机制**：通过庞大的浮点权重矩阵，计算输入特征与各个专家的匹配概率。在反向传播中，路由器通过梯度下降不断修正权重。
- **优势**：具备极强的数据拟合能力，能自动发现人类难以察觉的隐性特征关联。
- **劣势**：极度依赖海量训练数据；黑盒属性强；在遇到分布外数据（OOD）或对抗攻击时，容易发生“路由坍塌（全部挤向少数专家）”。

### 2. 硬编码规则选择器（Rule Selector）
- **核心机制**：依靠底层的离散代数公式（如模10运算、拓扑偏移定则、预计算查表）进行路由寻址。路由结果在代码写定的那一刻就已经固化。
- **优势**：零浮点开销；延迟极低；路由结果绝对确定；泛化能力强（因为基于纯数学拓扑，不依赖训练数据）。
- **劣势**：无法像神经网络那样从无监督数据中自适应地调整路由偏好。

## 三、工程破局：规则作为学习之锚

实践发现，纯靠学习的软路由存在长尾效应，而纯靠规则的硬路由缺乏灵活性。Polaris 引擎的终极方案是：**用硬规则作为安全护栏，用轻量级学习作为偏好微调。**
例如：利用可微学习计算大致的专家方向，但在最终执行时，强制通过纯整数取模，将其约束在合法的拓扑节点内（如利用 10 进制取余）。这既保留了智能，又锁死了底线。

## 四、代码实现

    import random

    def learned_router(input_vector, expert_weights):
        """
        模拟可微学习路由（软路由）
        """
        # 模拟浮点权重矩阵的点乘计算
        scores = [sum(v * w for v, w in zip(input_vector, weights)) for weights in expert_weights]
        # 简单的 Softmax 模拟
        total = sum(scores)
        probs = [s / total for s in scores] if total != 0 else [0.5, 0.5]
        # 根据概率随机采样（训练时常用）
        chosen_expert = probs.index(max(probs))
        return chosen_expert, probs

    def rule_selector(input_state, topology_rules):
        """
        纯整数规则选择器（硬路由）
        """
        # 利用纯整数的代数哈希直接映射，杜绝浮点概率
        chosen = (input_state * 3 + 7) % len(topology_rules)
        return chosen

    if __name__ == "__main__":
        # 模拟输入
        input_vec = [0.5, 0.2, 0.9]
        expert_wts = [[1, -1, 1], [-1, 1, -1]]
        
        # 1. 学习路由
        expert_idx, probabilities = learned_router(input_vec, expert_wts)
        print(f"[可微学习路由] 命中专家: {expert_idx}, 概率分布: {probabilities}")
        
        # 2. 规则选择
        state_val = 7 # 假设当前状态为 7
        rule_expert = rule_selector(state_val, expert_wts)
        print(f"[规则选择器路由] 命中专家: {rule_expert} (零延迟直接映射)")

## 五、结论

| 维度 | 可微学习路由（Learned） | 规则选择器（Hard-coded） | Polaris 混合策略 |
|---|---|---|---|
| 训练成本 | 极高（依赖海量数据） | 零（基于代数规则） | 低（仅微调权重） |
| 泛化能力 | 强（拟合概率分布） | 强（基于拓扑流形） | 极强（规则锁边界，学习找最优） |
| 运算开销 | 极高（高维矩阵乘法） | 极低（纯整数哈希） | 低（混合计算） |
| 安全性 | 黑盒，易被攻击 | 白盒，绝对可控 | 灰盒，强鲁棒性 |
