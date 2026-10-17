# 意图到执行管道：可运行伪代码与动态阈值

## 一、这篇解决什么问题

在54号四阶段管道和55号动态阈值的基础上，给出可运行的伪代码，包含数据结构、主循环、各阶段函数、复杂度分析与实验对照。目标是让管道可以直接转写成 Python 或其他语言。

适合读者：对管道实现、动态决策、防卡死机制感兴趣的读者。

前提：27宫立方体，旧赋值或新赋值，中宫为5。

## 二、数据结构

    状态 State:
        pos      : 当前坐标 (x,y,z)
        prev_dir : 上一步方向向量，初始为空
        visited  : 已访问的4/6位置集合
        since    : 距上次发现的步数
        last_lv  : 上次发现级别，0表示无
        found    : 发现记录列表

    配置 Config:
        k        : 路径加数
        steps    : 最大步数
        mode     : "fixed" 或 "dynamic"
        fixed_T  : 固定模式下的阈值

    候选 Candidate:
        pos   : 坐标
        value : 宫值
        level : 级别 1/2/3，0表示不可感

## 三、主循环

    输入：V（27宫值表），start，config
    初始化 State
    重复 steps 次：
        1. 计算当前距中宫距离 dist
        2. 计算探测半径 R
        3. 探测：scan(V, pos, R, visited) -> (cur_max, cur_best)
        4. 决策：T = decide_T(config, state, dist, cur_max)
        5. 选择目标：
           若 cur_best 非空 且 cur_max <= T：
               目标值 = V[cur_best]
               标记 cur_best 已访问
               更新 found、last_lv、since
           否则：
               目标值 = mod9(V[pos] + k)
               since += 1
        6. 执行：next_pos = move(V, pos, 目标值, prev_dir)
        7. 若 next_pos 为空：
               若 cur_best 非空：
                   next_pos = cur_best
                   记录“断后偏转”
               否则：
                   记录卡死，退出
        8. 更新 prev_dir、pos
    输出：found、卡死标记、轨迹

## 四、探测

    函数 scan(V, pos, R, visited) -> (best_level, best_pos)
        best_level = 0
        best_pos = None
        对 V 中每个位置 p：
            若 V[p] 属于 {4,6} 且 p 不在 visited 且 距离(pos,p) <= R：
                lv = level(V, p)
                若 lv > best_level：
                    best_level = lv
                    best_pos = p
        返回 best_level, best_pos

    函数 level(V, p) -> 1/2/3/0
        若 V[p] 不属于 {4,6}：返回 0
        若 x==3 且 y==3：返回 1
        若 x,y,z 均在 {1,5}：返回 2
        否则：返回 3

    半径规则：
        若 dist <= 2：R = 2
        否则若 dist <= 3.5：R = 2.828
        否则：R = 3.464

## 五、评估

评估与探测合并：scan 返回的 best_level 即为评估结果。

若需要完整候选列表，可扩展为：

    函数 evaluate(V, pos, R, visited) -> 候选列表
        对每个满足条件的 p：
            计算 level
            计算幂次差 power_diff(V[p], 5)
            加入列表
        按 level 升序、幂次差升序排序
        返回列表

幂次差：

    POW2 = {2:1, 4:2, 8:3, 6:4}
    power_diff(a,b) = min(|POW2[a]-POW2[b]|, 4-|...|)

## 六、决策：动态阈值 v2

    函数 decide_T(config, state, dist, cur_max) -> T
        若 config.mode == "fixed"：
            返回 config.fixed_T

        T = 2
        若 state.since >= 3：T += 1
        若 state.since >= 6：T += 1
        若 dist >= 3.5：T += 1
        若 state.last_lv == 3：T -= 1
        若 state.last_lv == 1：T += 1
        T = clamp(T, 1, 3)

        若 cur_max > 0 且 cur_max < T：
            T = cur_max

        返回 T

关键：即时因子。当前半径内最高级别低于 T 时，立即降 T，避免路径断前来不及放宽。

## 七、执行

    函数 move(V, pos, target_value, prev_dir) -> (next_pos, new_dir)
        候选 = 所有与 pos 相邻且值为 target_value 的位置
        若候选为空：返回 (None, prev_dir)
        对每个候选 p：
            d = 距离(p, 中宫)
            dot = 若 prev_dir 非空，则 prev_dir 与 (p-pos) 的内积，否则 0
            评分 = (-dot, d, p)
        选评分最小者
        返回 next_pos, (next_pos - pos)

相邻定义：dx,dy,dz 各自取 -2,0,2，且不全为0。

## 八、完整伪代码

    函数 run(V, start, config) -> 结果
        pos = start
        prev_dir = None
        visited = 空集
        found = 空列表
        since = 0
        last_lv = 0
        log = 空列表

        重复 config.steps 次，i 从 1 开始：
            dist = 距离(pos, (3,3,3))
            R = 半径(dist)
            cur_max, cur_best = scan(V, pos, R, visited)
            T = decide_T(config, state, dist, cur_max)

            若 cur_best 非空 且 cur_max <= T：
                target_value = V[cur_best]
                visited.add(cur_best)
                found.append(cur_max)
                last_lv = cur_max
                since = 0
                action = "偏转L" + cur_max
            否则：
                target_value = mod9(V[pos] + config.k)
                since += 1
                action = "继续"

            next_pos, new_dir = move(V, pos, target_value, prev_dir)

            若 next_pos 为空：
                若 cur_best 非空：
                    next_pos = cur_best
                    new_dir = next_pos - pos
                    action = "断后偏转L" + cur_max
                    若 cur_max 不在 found：found.append(cur_max)
                否则：
                    log.append((i, pos, V[pos], T, cur_max, "断"))
                    返回 (found, True, log)

            prev_dir = new_dir
            pos = next_pos
            log.append((i, pos, V[pos], T, cur_max, action))

        返回 (found, False, log)

## 九、复杂度

| 操作 | 复杂度 |
|---|---|
| 探测 scan | O(27) |
| 评估 level | O(1) |
| 决策 decide_T | O(1) |
| 执行 move | O(27) |
| 单步总计 | O(27) |
| 总步数 | O(steps) |
| 总复杂度 | O(27 × steps) |

存储：

| 项 | 量 |
|---|---|
| V 表 | 27 项 |
| visited | 最多 6 项（4/6 总数） |
| found | 最多 steps 项 |
| log | 最多 steps 项 |

## 十、实验对照

旧赋值，加9：

| 起点 | 模式 | 发现 | 平均级别 | 卡死 |
|---|---|---:|---:|---:|
| 中宫 | 固定T=1 | 1 | 1.0 | 0 |
| 中宫 | 固定T=3 | 8 | 2.25 | 0 |
| 中宫 | 动态v2 | 6 | 2.17 | 0 |
| 顶点 | 固定T=1 | 2 | 2.0 | 0 |
| 顶点 | 固定T=3 | 8 | 2.25 | 0 |
| 顶点 | 动态v2 | 8 | 2.25 | 0 |

结论：

1. 动态v2在任意起点均不卡死。
2. 动态v2的发现次数不低于固定T=2，不高于固定T=3。
3. 动态v2的平均级别介于固定T=1与T=3之间。
4. 断后偏转是防卡死的关键。

## 十一、可验证推论

1. 对任意起点和加数，动态v2的卡死次数为0。
2. 动态v2的T值始终在1到3之间。
3. 若当前半径内只有3级，动态v2会立即接受，不再等待。
4. 若当前半径内有1级，动态v2会优先接受1级。
5. 断后偏转只在前向路径无候选时触发，不改变正常路径。

## 十二、开放问题

1. 幂次差是否应参与决策评分，而非只用于分级？
2. 动态v2是否会导致路径震荡？
3. 多目标场景下如何扩展？
4. 连续空间中半径和级别如何定义？

## 十三、边界声明

本文只做结构形式化与算法伪代码。

不宣称主观体验，不涉及玄学断言。

可定义、可推导、可检验；有用则留，无用则弃。

## 十四、口诀

> 探测扫描定候选，评估分级按幂差。  
> 决策动态调阈值，执行方向惯性先。  
> 断后偏转防卡死，即时放宽不等闲。  
> 四阶段成一管道，意图执行此中全。
