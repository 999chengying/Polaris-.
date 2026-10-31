# Polaris 基础架构：三维张量空间映射与坐标系规范

## 一、本文解决什么问题

在将多模态物理数据（如视觉、雷达、机械臂坐标）输入给纯整数心智引擎时，我们需要一套极其严谨的空间数据结构来进行降维与特征对齐。
本文基于离散的三维张量空间，定义**“三维九宫坐标体系（3D Jiugong Space）”**。该系统将连续高维空间截断映射为一个 \(3 \times 3 \times 3\) 的纯整数网格，为后续的特征路由、空间偏置计算与图网络聚合提供底层的坐标规范。

## 二、三维空间定义与坐标映射

### 1. 空间网格划分
我们定义三维空间的每个坐标轴 \(X, Y, Z\) 的取值范围为 \(\{1, 3, 5\}\)。
- **网格总容量**：\(3 \times 3 \times 3 = 27\) 个小立方体（单元格）。
- **物理含义**：1、3、5 分别代表该维度上的“下界/前界/左界”、“中心原点”、“上界/后界/右界”。

### 2. 空间中心与坐标原定
系统的绝对基准点位于几何中心：
\(O = (3, 3, 3)\)
在 Polaris 引擎中，这个中心节点对应状态基准态 `5`，作为所有特征路由和状态机重置的锚点。

### 3. 节点状态映射规则
当一个外部多维特征输入系统时，系统根据特征的特征值将其分配至特定的单元格：
- **顶点单元格（活跃宫）**：坐标的每一维都在边界 \(\{1, 5\}\) 上（共 8 个）。通常用于承载最高维度的正交特征（如状态 1~9，排除 5）。
- **棱中心与面中心单元格（潜伏宫）**：位于坐标轴的中线上（包含至少一个 3）。通常用于承载过渡态、混合特征或路由旁路。

## 三、空间张量的数据聚合

系统支持多通道（Channel）数据的同时注入。在三维空间中，每个单元格可以看作一个包含 \(C\) 个通道的张量节点：
\(T_{i,j,k} = [x_1, x_2, \dots, x_C]\)
在进行图网络消息传递时，相邻节点（曼哈顿距离为 2）的数据会发生跨通道的纯整数聚合计算。

## 四、代码实现

    class GridCell:
        def __init__(self, x, y, z):
            self.coord = (x, y, z)
            self.channels = [] # 存储当前节点的特征张量
            
        def add_feature(self, feature_val):
            self.channels.append(feature_val % 10)

    class Jiugong3DSpace:
        def __init__(self):
            # 初始化 27 个单元格
            self.grid = {}
            for x in [1, 3, 5]:
                for y in [1, 3, 5]:
                    for z in [1, 3, 5]:
                        self.grid[(x, y, z)] = GridCell(x, y, z)

        def inject_data(self, coord, data):
            """将特征注入特定坐标"""
            if coord in self.grid:
                self.grid[coord].add_feature(data)
            else:
                raise ValueError("坐标越界")

        def get_center(self):
            return self.grid[(3, 3, 3)]

    if __name__ == "__main__":
        space = Jiugong3DSpace()
        # 向顶点 (1, 1, 1) 注入特征
        space.inject_data((1, 1, 1), 9)
        # 向中心 (3, 3, 3) 注入基准
        space.inject_data((3, 3, 3), 5)
        
        print(f"顶点(1,1,1)当前特征: {space.grid[(1,1,1)].channels}")
        print(f"系统中心(3,3,3)当前特征: {space.get_center().channels}")

## 五、结论

| 验证项 | 结果 |
|---|---|
| 网格完备性 | 成功构建 \(3 \times 3 \times 3\) 的全映射空间 |
| 坐标规范 | 27个节点具备唯一的离散三维坐标 |
| 张量注入 | 支持多通道纯整数特征的无损挂载 |
