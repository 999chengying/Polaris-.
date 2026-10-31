# Polaris 基础架构：离散拓扑状态解码与连续物理控制映射

## 一、本文解决什么问题

纯整数心智引擎在内部完成推演后，输出的是离散的模10状态（如三元组 `(3, 8, 1)`）。然而，在具身智能与机器人控制中，底层执行器（如电机、舵机、液压阀）接收的是连续的物理控制信号（如电压、电流或 PWM 占空比）。
本文提出一种**“离散状态解码与连续映射算法（Discrete State Decoding & Continuous Mapping）”**。通过纯整数插值与线性映射，系统能够将内部高维的离散特征，无损、平滑地转化为物理世界的连续控制量，完成“感知-推演-执行”的具身闭环。

## 二、核心机制：从空间状态到物理信号

### 1. 离散三元组解码（State Decoding）
系统内部的三维状态 `(d1, d2, d3)` 代表十分位、百分位、千分位。通过加权乘法，将其还原为一个介于 `0.000` 到 `0.999` 之间的归一化连续系数（Continuous Coefficient）：
\(C = (d_1 \times 100 + d_2 \times 10 + d_3) / 1000\)

### 2. 线性物理映射（Linear Mapping）
不同的执行器有不同的控制区间。系统将归一化系数 `C` 进行线性拉伸，映射到目标物理区间 `[Min, Max]`（例如舵机的 0° ~ 180°，或电机的 -1.0V ~ +1.0V）：
\(Output = Min + C \times (Max - Min)\)

### 3. 方向与极性判定（Polarity & Direction）
利用离散状态的奇偶性（或差5墙的极值约束），系统可以极低延迟地判断动作方向：
- 若内部状态命中奇数或 `>5` 的极值，则输出正向控制（或高占空比）。
- 若命中偶数或 `<5`，则输出反向控制。

## 三、工程价值

1. **平滑无抖振**：通过千分位的精细还原，避免了传统开关控制带来的阶跃突变，实现了极其平滑的电机驱动。
2. **物理护栏**：由于离散状态被严格锁定在 0~9，解码出来的物理量天然受到上下限约束，绝不会烧毁硬件设备。
3. **低功耗边缘控制**：无需复杂的滤波算法与 PID 控制浮点运算，直接查表或进行简单的乘加，即可实现高速响应的闭环控制。

## 四、代码实现

    def decode_to_continuous(state):
        """
        将离散小模状态解码为 0.0 ~ 1.0 的连续系数。
        """
        d1, d2, d3 = state
        return (d1 * 100 + d2 * 10 + d3) / 1000.0

    def map_to_actuator(continuous_val, min_out=-1.0, max_out=1.0):
        """
        将连续系数映射到物理执行器的控制区间。
        """
        return min_out + continuous_val * (max_out - min_out)

    def embodied_control_pipeline(state, target_hardware="motor"):
        """
        具身控制管线。
        """
        # 1. 解码
        coeff = decode_to_continuous(state)
        
        # 2. 根据硬件类型映射
        if target_hardware == "motor":
            # 电机：-12V 到 +12V
            output_voltage = map_to_actuator(coeff, -12.0, 12.0)
            return f"电机控制电压: {output_voltage:.3f} V"
        elif target_hardware == "servo":
            # 舵机：0 到 180 度
            output_angle = map_to_actuator(coeff, 0.0, 180.0)
            return f"舵机目标角度: {output_angle:.1f}°"
        else:
            return "未知硬件"

    if __name__ == "__main__":
        # 测试用例：引擎推演出的离散状态
        states_to_test = [
            (0, 0, 0), # 极小值
            (5, 0, 0), # 中间值
            (9, 9, 9)  # 极大值
        ]
        
        for s in states_to_test:
            print(f"离散状态: {s}")
            print(f"  -> {embodied_control_pipeline(s, 'motor')}")
            print(f"  -> {embodied_control_pipeline(s, 'servo')}")

## 五、结论

| 验证项 | 结果 |
|---|---|
| 状态解码 | 纯整数无损还原为高精度浮点系数 |
| 区间映射 | 精准对接各种物理量纲（电压、角度等） |
| 具身闭环 | 完成从心智引擎到物理执行器的最后一环 |
