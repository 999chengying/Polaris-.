# -*- coding: utf-8 -*-
"""
Polaris V19: 天香炉大阵 (Tianxiang Grid)
宏观：27宫赋值 + 11个5节点协同
微观：7个风火炉嵌套 + 连续小模数据流
依据：docs-v4/08-tianxiang-grid.md
"""

def mod10(x):
    return x % 10

class TianxiangGrid:
    def __init__(self):
        self.grid = {}
        
        # 活跃宫（顶点）
        vertices = {
            (1,1,1):9, (5,1,1):4, (5,5,1):3, (1,5,1):8,
            (1,1,5):7, (5,1,5):2, (1,5,5):6, (5,5,5):1
        }
        self.grid.update(vertices)
        
        # 面中心（5）
        faces = {
            (3,3,1):5, (3,3,5):5, (3,1,3):5, (3,5,3):5, (1,3,3):5, (5,3,3):5
        }
        self.grid.update(faces)
        
        # 棱中心（2 - Z轴通道）
        edges_z = {
            (5,5,3):2, (1,1,3):2, (1,5,3):2, (5,1,3):2
        }
        self.grid.update(edges_z)
        
        # 棱中心（5 - X轴通道）
        edges_5 = {
            (3,1,1):5, (3,5,5):5, (3,1,5):5, (3,5,1):5
        }
        self.grid.update(edges_5)
        
        # 棱中心（1 - Y轴通道）
        edges_1 = {
            (1,3,5):1, (5,3,1):1, (1,3,1):1, (5,3,5):1
        }
        self.grid.update(edges_1)
        
        self.grid[(3,3,3)] = 5
        
        # 嵌套七个风火炉的动量
        self.furnaces = {
            (1,3,3): 5, (5,3,3): 5, (3,1,3): 5, (3,5,3): 5,
            (3,3,1): 5, (3,3,5): 5, (3,3,3): 5
        }

    def print_cross_section(self, z):
        print(f"  [Z={z} 截面]")
        for y in [5, 3, 1]:
            row = []
            for x in [1, 3, 5]:
                val = self.grid.get((x, y, z), "?")
                mark = "*" if (x,y,z) in self.furnaces else " "
                row.append(f"{val}{mark}")
            print(f"    {row}")

    def route_and_process(self, state):
        d1, d2, d3 = state
        print(f"\n>>> 输入连续小模: {state}")
        
        # 宏观通道流向说明
        print(f"    - {d1} 走差5通道 -> X轴炉")
        print(f"    - {d2} 走差1通道 -> Y轴炉")
        print(f"    - {d3} 走差2通道 -> Z轴炉")
        
        # 微观并发运算
        out_X_l = mod10(d1 * 3 + self.furnaces[(1,3,3)])
        out_X_r = mod10(d1 * 7 + self.furnaces[(5,3,3)])
        
        out_Y_f = mod10(d2 * 1 + self.furnaces[(3,1,3)])
        out_Y_b = mod10(d2 * 9 + self.furnaces[(3,5,3)])
        
        out_Z_b = mod10(d3 * 2 + self.furnaces[(3,3,1)])
        out_Z_t = mod10(d3 * 8 + self.furnaces[(3,3,5)])
        
        # 垂拱而治：汇聚
        center_aggregate = mod10(out_X_l + out_X_r + out_Y_f + out_Y_b + out_Z_b + out_Z_t)
        
        print(f"  [微观] X: {out_X_l}/{out_X_r} | Y: {out_Y_f}/{out_Y_b} | Z: {out_Z_b}/{out_Z_t}")
        print(f"  🎯 [天香炉中心] 汇聚共识: {center_aggregate}")
        
        # 动量回写
        for coord in self.furnaces:
            self.furnaces[coord] = (center_aggregate * 7 + self.furnaces[coord] * 3) // 10
            
        return center_aggregate

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris V19: 天香炉大阵")
    print("=" * 60)
    
    grid = TianxiangGrid()
    grid.print_cross_section(3)
    
    test_states = [(3, 1, 4), (9, 9, 9), (1, 7, 2)]
    for state in test_states:
        grid.route_and_process(state)
