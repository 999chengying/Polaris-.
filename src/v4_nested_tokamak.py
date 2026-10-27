# -*- coding: utf-8 -*-
"""
Polaris V4: 分形嵌套托卡马克 (Fractal Nested Tokamak)
宏观：三头六臂外壳驱动
微观：嵌入中宫的八卦炉内核
依据：docs-v3/02-fractal-nested-tokamak.md
"""

def mod10(x):
    return x % 10

class TokamakCore:
    """微观内核：八卦炉（嵌于中宫）"""
    def __init__(self):
        self.base_plasma = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
        self.current_plasma = [row[:] for row in self.base_plasma]
        
    def inject_macro_state(self, macro_k):
        """接收宏观特征，执行炉底重燃与逆元干预"""
        k = macro_k
        if k == 6:
            print("  [炉内] 检测到算子6 (时间冻结)，自动切换为逆元算子3！")
            k = 3
        elif k == 0:
            k = 5
            
        print(f"  [炉内] 从炉底重燃，注入乘数算子: 乘{k}")
        # 每次从 base_plasma 重新计算，防累乘失真
        self.current_plasma = [[mod10(val * k) for val in row] for row in self.base_plasma]
        
    def extract_fire_level(self):
        """提取火候：奇数个数与十字交叉值"""
        odd_count = sum(1 for row in self.current_plasma for v in row if v % 2 != 0)
        
        center = self.current_plasma[1][1]
        top = self.current_plasma[0][1]
        bottom = self.current_plasma[2][1]
        left = self.current_plasma[1][0]
        right = self.current_plasma[1][2]
        cross_val = mod10(center + top + bottom + left + right)
        
        return odd_count, cross_val

class ThreeHeadsSixArms:
    """宏观外壳"""
    def __init__(self):
        self.body = (0, 0, 1) 
        self.core_furnace = TokamakCore()
        
    def evolve_body(self):
        self.body = tuple(mod10(x * 2) for x in self.body)
        return self.body

    def run_cycle(self, steps):
        print("\n=== 启动 V4 嵌套演化 (炉底重燃 + 奇偶火候) ===")
        
        for step in range(1, steps + 1):
            print(f"\n--- 第 {step} 步 ---")
            b = self.evolve_body()
            print(f"  [外层] 身: {b}")
            
            macro_k = b[2]
            self.core_furnace.inject_macro_state(macro_k)
            
            odd_count, cross_val = self.core_furnace.extract_fire_level()
            
            print(f"  [炉内] 当前火候(奇数个数): {odd_count}, 十字交叉值: {cross_val}")
            for row in self.core_furnace.current_plasma:
                print(f"        {row}")
            
            if odd_count == 0:
                print("  ❄️ [状态] 炉火熄灭，阴气弥漫 (纯偶数态)")
            elif odd_count >= 4:
                print("  🔥 [状态] 炉火纯青，阳气极盛 (奇数保留态)")
                if cross_val == 5:
                    print("  🌟 [炼丹成功] 孕育纯阳金丹！")

if __name__ == "__main__":
    print("=" * 50)
    print("☯️ Polaris V4: 分形嵌套托卡马克")
    print("=" * 50)
    polaris_sys = ThreeHeadsSixArms()
    polaris_sys.run_cycle(steps=5)
