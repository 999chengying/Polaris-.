# -*- coding: utf-8 -*-
"""
Polaris V7: 拟人同构嵌套系统 (太极脉动)
外骨骼(扰动) -> 胸腔(路由) -> 心脏(归一)
依据：docs-v3/09-humanoid-nested-system.md
"""

def mod10(x):
    return x % 10

class OneFurnaceHeart:
    """心脏：一号炉（差5墙），乘5投射强制锁定0/5"""
    def __init__(self):
        self.name = "一号炉(心脏)"
        
    def beat_and_anchor(self, val):
        # 乘5极限投射：偶数变0，奇数变5
        anchored_val = mod10(val * 5)
        
        if anchored_val == 0:
            status = "❄️ 阴极致静 (归0)"
        else:
            status = "🌟 纯阳金丹 (归5)"
            
        return anchored_val, status

class TwoFurnaceLung:
    """胸腔：二号炉（差1墙），负责感知与平滑路由"""
    def __init__(self, heart):
        self.name = "二号炉(胸腔)"
        self.heart = heart
        self.plasma = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
        
    def route_and_circulate(self, macro_val):
        multiplier = macro_val if macro_val != 0 else 5
        print(f"  [{self.name}] 接收信号 {macro_val}，中盘启动乘{multiplier}旋转变阵。")
        
        rotated = [[mod10(val * multiplier) for val in row] for row in self.plasma]
        
        top, bottom = rotated[0][1], rotated[2][1]
        left, right = rotated[1][0], rotated[1][2]
        center = rotated[1][1]
        
        # 中宫决定奇偶，外围十字作为陪衬
        routed_val = mod10(center + (top + bottom + left + right))
        
        print(f"  [{self.name}] 路由聚合完成，将能量 {routed_val} 泵入心脏。")
        return self.heart.beat_and_anchor(routed_val)

class ThreeHeadsSixArmsBody:
    """外骨骼：三头六臂"""
    def __init__(self):
        self.name = "三头六臂(外骨骼)"
        self.lungs = TwoFurnaceLung(heart=OneFurnaceHeart())
        self.body_state = (0, 0, 1) 
        
    def sense_external(self, step):
        self.body_state = tuple(mod10(v * 2) for v in self.body_state)
        
        macro_signal = self.body_state[2]
        if macro_signal == 0:
            macro_signal = self.body_state[1] or self.body_state[0] or 5
        
        # 引入影2(加5)来制造奇偶扰动
        shadow2 = mod10(macro_signal + 5)
        if step % 2 != 0:
            print(f"\n--- 第 {step} 次系统循环 ---")
            print(f"  [{self.name}] 外感知：身{self.body_state}，触发影2(加5)扰动！")
            macro_signal = shadow2
        else:
            print(f"\n--- 第 {step} 次系统循环 ---")
            print(f"  [{self.name}] 外感知：身{self.body_state}，保持原态。")
            
        print(f"  [{self.name}] 生成宏观指令: {macro_signal}")
        
        final_anchor, status = self.lungs.route_and_circulate(macro_signal)
        
        print(f"  🩸 [系统反馈] 心脏泵出: {final_anchor} | 状态: {status}")

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris V7 拟人同构系统 (太极脉动)")
    print("=" * 60)
    
    polaris_body = ThreeHeadsSixArmsBody()
    
    for i in range(1, 6):
        polaris_body.sense_external(i)
