# Polaris 基础架构：离散空间中的动态目标追踪与状态预测

## 一、本文解决什么问题

在具身智能（如无人机跟随、机械臂抓取）与视觉 Transformer 架构中，实时追踪高速移动的动态目标是一项核心挑战。传统的目标追踪算法（如卡尔曼滤波、粒子滤波）高度依赖连续的浮点矩阵求逆与概率分布计算，在边缘计算芯片上功耗极大。
本文提出一种**“纯整数离散追踪算法（Discrete Target Tracking）”**。系统将目标的物理位置映射至 \(3 \times 3 \times 3\) 的离散网格中，通过拓扑动量记忆预测其运动轨迹，并利用空间偏移定则进行比对锁定，实现了零浮点误差的高效追踪。

## 二、核心机制：预测与匹配

### 1. 离散动量预测（Discrete Momentum Prediction）
系统为追踪目标维护一个历史状态队列（记忆池）。基于前两个时刻的坐标 \(P_{t-1}\) 和 \(P_t\)，系统利用纯整数差分预测下一时刻的预估坐标：
\(\hat{P}_{t+1} = P_t + (P_t - P_{t-1})\)
所有坐标均在模 10 空间中取余，防止数据越界。

### 2. 拓扑空间匹配（Spatial Matching）
当下一时刻的外部传感器发回实际观测坐标 \(O_{t+1}\) 时，系统计算预测值与观测值之间的曼哈顿距离：
\(D = |\hat{X}_{t+1} - X_{obs}| + |\hat{Y}_{t+1} - Y_{obs}| + |\hat{Z}_{t+1} - Z_{obs}|\)
- 若 \(D\) 小于设定的安全阈值，则判定追踪成功，用观测值更新状态并重新计算速度。
- 若 \(D\) 超过阈值，则判定“目标丢失”或遭遇“对抗性欺骗”，触发元观测者机制。

### 3. 丢失重捕获（Re-capture）
若目标丢失，系统暂时切换到“全局扫描模式”，通过扩展搜索半径（利用图网络的广度优先搜索），在周边拓扑节点重新寻找匹配特征。

## 三、工程价值

1. **极低延迟**：整个追踪过程只有纯整数的加减法和绝对值比较，无需处理浮点矩阵，能在毫秒级内完成极高帧率的实时追踪。
2. **抗噪性能强**：由于离散状态机自带的“吸附效应（将微小抖动固定在同一个网格节点内）”，系统天然具备对传感器高频噪声的滤波能力。
3. **算力极度节省**：适合部署在单片机上，仅靠纯逻辑电路就能让扫地机器人或玩具无人机实现基础的视觉目标跟随。

## 四、代码实现

    def predict_and_track(history_coords, observation, threshold=3):
        """
        离散目标追踪器。
        history_coords: 历史位置列表 [(x,y,z), ...]，至少需要两个
        observation: 当前的观测坐标 (x,y,z)
        """
        if len(history_coords) < 2:
            return observation, "初始化追踪"
            
        p_prev = history_coords[-2]
        p_curr = history_coords[-1]
        
        # 1. 离散动量预测 (纯整数)
        velocity = tuple((p_curr[i] - p_prev[i]) for i in range(3))
        predicted = tuple((p_curr[i] + velocity[i]) % 10 for i in range(3))
        
        # 2. 计算与观测值的曼哈顿距离
        dist = sum(abs(predicted[i] - observation[i]) for i in range(3))
        
        # 3. 阈值判定
        if dist <= threshold:
            return observation, f"追踪成功 (误差:{dist})"
        else:
            return predicted, f"目标丢失或受骗 (误差:{dist})，执行盲预测"

    if __name__ == "__main__":
        # 模拟历史轨迹
        history = [(1, 1, 1), (2, 2, 2)] 
        
        # 场景 1：正常跟随
        obs_1 = (3, 3, 3)
        print(predict_and_track(history, obs_1))
        
        # 场景 2：遭遇对抗性跳跃（无人机突然瞬移）
        obs_2 = (8, 8, 8)
        print(predict_and_track(history, obs_2))

## 五、结论

| 验证项 | 结果 |
|---|---|
| 动量预测 | 基于历史位移进行纯整数外推 |
| 距离匹配 | 利用曼哈顿距离进行拓扑误差校验 |
| 抗噪与防骗 | 利用阈值过滤传感器噪声与对抗性瞬移 |
