# Polaris 实验记录：自指循环动力学的收敛性与极限环检测

## 一、本文解决什么问题

在循环神经网络（RNN）或深层 Transformer 的自注意力机制中，系统状态的“自我迭代（自指运算）”极易引发梯度爆炸或模式坍塌（即死锁在某个无意义的循环中）。本文通过构建纯整数模10空间的动力学实验，系统性观测自指迭代下的状态收敛规律，为后续大模型的防死锁机制提供实验基础。

## 二、实验设计

系统初始化一个基础状态 \(x\)，执行多次迭代：\(x_{t+1} = (x_t^n) \pmod{10}\)。
系统在每一步记录当前状态，并利用“历史轨迹检测器”判断其是否进入以下三种宿命：
1. **不动点（Fixed Point）**：连续多次输出相同值，系统进入绝对稳态。
2. **极限环（Limit Cycle）**：状态在两个或多个值之间反复横跳，无法收敛。
3. **混沌（Chaos）**：状态遍历周期极长，无法在短期内判定收敛。

## 三、实验现象与数学结论

1. **平方迭代（n=2）**：状态快速收敛至幂等元（1, 5, 6）。例如 \(2 \to 4 \to 6 \to 6 \to 6\)。这在代数上因为 \(6^2 \equiv 6 \pmod{10}\)，说明系统能够极速找到锚点并固化。
2. **立方迭代（n=3）**：产生显著的二周期振荡。例如 \(2 \leftrightarrow 8\)，\(3 \leftrightarrow 7\)。因为 \(2^3 = 8, 8^3 = 512 \equiv 2\)。在工程中，这对应了模型在两种极端特征间的反复拉扯（复读机）。
3. **四次迭代（n=4）**：重新快速收敛至（1, 5, 6），高维干涉打破了二周期纠缠。

## 四、代码实现

    def self_reference_experiment(start, power, steps=15):
        path = [start]
        for _ in range(steps):
            next_val = (path[-1] ** power) % 10
            path.append(next_val)
            # 检测不动点
            if len(path) >= 4 and len(set(path[-4:])) == 1:
                return path, "不动点收敛"
            # 检测二周期极限环
            if len(path) >= 4 and path[-1] == path[-3] and path[-2] == path[-4]:
                return path, "极限环死锁"
        return path, "长周期/混沌"

    if __name__ == "__main__":
        print(self_reference_experiment(start=2, power=2)) # 不动点
        print(self_reference_experiment(start=3, power=3)) # 极限环

## 五、结论

| 迭代幂次 | 动力学宿命 | 代数原因 | 大模型对应现象 |
|---|---|---|---|
| 平方 (n=2) | 极速收敛至幂等元 | \(x^2 \equiv x\) | 快速达成推理共识 |
| 立方 (n=3) | 二周期极限环 | 逆元震荡 | 梯度震荡 / 复读机 |
| 四次 (n=4) | 破局归真 | 高阶吸收 | 强行纠偏 |
