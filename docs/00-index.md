# 九宫八卦立方体：文档总索引

## 一、快速上手

如果你第一次来，按以下顺序读：

| 顺序 | 文档 | 内容 |
|---:|---|---|
| 1 | `README.md` | 项目总览 |
| 2 | `docs/00-overview.md` | 体系总览 |
| 3 | `docs/01-jiugong.md` | 九宫编码器与剪枝 |
| 4 | `docs/03-55-50.md` | 天地之数55与大衍之数50 |
| 5 | `docs/04-four-images.md` | 四象结构 |

读完后可跳到你感兴趣的方向：

| 兴趣 | 推荐文档 |
|---|---|
| 三维结构 | `docs/11-3d-jiugong-space.md` |
| 路径动力学 | `docs/10-path-dynamics.md` |
| 自指回路 | `docs/12-self-reference-experiments.md` |
| 顺逆规则 | `docs/13-shun-ni-rules.md` |
| AI架构 | `docs/06-ai-architecture.md`、`docs/18-ai-mapping.md` |
| 通信架构 | `docs/27-inference-interconnect.md`、`docs/34-cross-domain-communication.md` |
| 新赋值 | `docs/30-new-assignment.md` |
| 省算力对比 | `docs/31-arithmetic-routing.md`、`docs/32-scale-comparison.md` |

## 二、文档地图

### 第一层：基础结构

| 编号 | 文档 | 内容 |
|---|---|---|
| 00 | `00-overview.md` | 体系总览 |
| 01 | `01-jiugong.md` | 九宫编码器与剪枝 |
| 02 | `02-cycle.md` | 二十四山循环 |
| 03 | `03-55-50.md` | 天地之数55与大衍之数50 |
| 04 | `04-four-images.md` | 四象结构24/28/32/36 |

### 第二层：路径与自指

| 编号 | 文档 | 内容 |
|---|---|---|
| 10 | `10-path-dynamics.md` | 洛书九宫阵路径动力学 |
| 11 | `11-3d-jiugong-space.md` | 三维九宫空间 |
| 12 | `12-self-reference-experiments.md` | 自指回路实验 |
| 13 | `13-shun-ni-rules.md` | 顺逆规则 |
| 14 | `14-jing-yi-zhidao.md` | 精一之道 |
| 15 | `15-multiple-cycles.md` | 多次显隐循环 |
| 16 | `16-sanjie-correction.md` | 三界修正 |
| 17 | `17-uniqueness.md` | 唯一性验证 |

### 第三层：AI架构映射

| 编号 | 文档 | 内容 |
|---|---|---|
| 05 | `05-recursive-fault-tolerance.md` | 递归容错与虚实转换 |
| 06 | `06-ai-architecture.md` | AI帝宫架构 |
| 18 | `18-ai-mapping.md` | 从九宫路径到AI架构 |
| 19 | `19-path-planner.md` | 路径规划对比 |
| 20 | `20-consistency.md` | 三链一致性收敛 |
| 21 | `21-parallel-decision.md` | 三链并行决策 |
| 22 | `22-resource-scheduling.md` | 资源约束调度 |
| 23 | `23-independent-coordination.md` | 独立自主与全局协调 |
| 24 | `24-central-observer.md` | 中宫感知实验 |
| 25 | `25-three-chain-classification.md` | 三链独立分类 |

### 第四层：通信与市场

| 编号 | 文档 | 内容 |
|---|---|---|
| 26 | `26-dynamic-target.md` | 动态目标通信模型 |
| 27 | `27-inference-interconnect.md` | 推理互联架构分析 |
| 28 | `28-event-poll-hybrid.md` | 事件驱动与定时轮询 |
| 29 | `29-phase-diagram.md` | 最优策略相图 |
| 34 | `34-cross-domain-communication.md` | 跨域通信 |

### 第五层：新赋值与省算力

| 编号 | 文档 | 内容 |
|---|---|---|
| 30 | `30-new-assignment.md` | 新27宫赋值 |
| 31 | `31-arithmetic-routing.md` | 等差差值法预置路由 |
| 32 | `32-scale-comparison.md` | 放大场景对比 |
| 33 | `33-fixed-vs-learned.md` | 固定拓扑vs可训练网络 |

### 附录

| 编号 | 文档 | 内容 |
|---|---|---|
| 07 | `07-military-analogy.md` | 军事理论映射 |
| 08 | `08-experiment-checklist.md` | 实验清单 |
| 09 | `09-file-manifest.md` | 文件清单 |

## 三、核心概念表

| 术语 | 含义 |
|---|---|
| 九宫八卦立方体 | 8顶点配八卦数，中心为5 |
| 数卦映射 | 乾9兑4离3震8巽2坎7艮6坤1 |
| 五形 | 生、化、变、恒、空 |
| 共面 | 四点在同一平面，体积为0 |
| 合十对 | 1-9、2-8、3-7、4-6，和10 |
| 生成对 | 1-6、2-7、3-8、4-9，差5 |
| 三条链 | 147自转、258换链、369归核 |
| 27宫 | 立方体三等分后的27个小单元 |
| 活跃宫 | 9个（8顶点+1体心） |
| 潜伏宫 | 18个（12棱中+6面心） |
| 顺行 | 按序列走，方向惯性 |
| 逆行 | 锁定5，逐步归中 |
| 等差差值法 | 用差值1、2、3、4沿链计算路径 |
| 固定拓扑 | 规则硬编码，零训练 |

## 四、三条主线

### 主线一：结构

九宫立方体 → 27宫 → 新赋值 → 五行俱全。

### 主线二：路径

自指回路 → 顺逆规则 → 精一之道 → 线性归中。

### 主线三：通信

动态目标 → 事件vs轮询 → 相图 → 跨域通信。

## 五、关键数据

### 线性规律

帝5顺行后逆行归中：

步数 = 0.5 × 距离（新赋值）

步数 = 0.48 × 距离（旧赋值）

### 连接统计

跨单元连接：

| 差值 | 次数 | 占比 |
|---:|---:|---:|
| 1 | 8 | 33.3% |
| 2 | 8 | 33.3% |
| 5 | 8 | 33.3% |

### 唯一性

九种锁定，唯5归中。

### 省算力

等差差值法 vs 搜索法：

| 场景 | 节省比例 |
|---|---:|
| 27宫 | 88.9% |
| 1000宫 | 99.7% |
| 100000宫 | 99.997% |

## 六、未解问题

1. 从离散到连续的嵌入方案；
2. 固定拓扑与神经网络的混合架构；
3. 新赋值的实测验证；
4. 等差差值法在真实任务上的表现；
5. 事件驱动与轮询的最优混合比例；
6. 三条链并行的实际加速比。

## 七、仓库结构

```
jiugong-bagua-cube/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── docs/         文档
├── src/          代码
├── tests/        测试
├── data/         数据
└── benchmark/    基准测试
```

## 八、边界声明

本仓库只做结构形式化与架构映射，不宣称预测效力。

可定义、可推导、可检验；有用则留，无用则弃。

## 九、口诀

基础结构一二三四，路径自指十到十七。
AI架构十八二五，通信市场二六二九。
新赋值三十到三三，跨域通信三十四。
先读总览再入门，按图索骥不迷路。
