# -*- coding: utf-8 -*-
"""
Polaris V15: 具身双向车道 (Embodied Bidirectional Bridge)
核心功能：连续感知编码 -> 纯整数七炉阵运算 -> 离散小模解码 -> 物理控制信号输出
依据：docs-v4/04-bidirectional-bridge-embodied-action.md
"""

def mod10(x):
    return x % 10

def encode_continuous(val):
    """编码：连续值 -> 小模三元组 (保留前三位小数)"""
    s = f"{val:.3f}".split('.')
    return (int(s[1][0]), int(s[1][1]), int(s[1][2]))

def decode_to_continuous(state):
    """解码：小模三元组 -> 连续值 (0.000 ~ 0.999)"""
    d1, d2, d3 = state
    return (d1 * 100 + d2 * 10 + d3) / 1000.0

def map_to_action(continuous_val):
    """物理映射：映射为具身控制信号 (-1.0 ~ 1.0)"""
    return (continuous_val * 2.0) - 1.0

class MomentumFurnace:
    def __init__(self, coord, base_role, anchor=5):
        self.coord = coord
        self.base_role = base_role
        self.spatial_bias = sum(coord) % 10
        self.anchor = anchor
        self.momentum = 5
        
    def evolve_and_process(self, state):
        d1, d2, d3 = state
        if self.momentum == 0: self.momentum = self.anchor
        history_k = mod10(self.momentum + self.spatial_bias) or self.anchor
            
        if self.base_role == 'left':
            k = mod10(d1 + history_k) or 3
        else:
            k = mod10(d2 + history_k) or 7
            
        raw3 = d3 * k
        carry1 = raw3 // 10
        new_d3 = raw3 % 10
        
        raw2 = d2 * k + carry1 + self.spatial_bias
        carry2 = raw2 // 10
        new_d2 = raw2 % 10
        
        raw1 = d1 * k + carry2
        new_d1 = raw1 % 10
        
        current_sum = mod10(new_d1 + new_d2 + new_d3)
        self.momentum = (current_sum * 7 + self.momentum * 3) // 10
        
        return (new_d1, new_d2, new_d3), k

class Full3DMoE:
    def __init__(self):
        self.furnaces = {
            'X': (MomentumFurnace((1,3,3), 'left'), MomentumFurnace((5,3,3), 'right')),
            'Y': (MomentumFurnace((3,1,3), 'left'), MomentumFurnace((3,5,3), 'right')),
            'Z': (MomentumFurnace((3,3,1), 'left'), MomentumFurnace((3,3,5), 'right'))
        }
        self.axis_weights = {
            'X': [7, 2, 1],
            'Y': [2, 7, 2],
            'Z': [1, 2, 7]
        }

    def content_route(self, state):
        best_axis = 'X'
        best_score = -1
        for axis, w in self.axis_weights.items():
            score = mod10(state[0]*w[0] + state[1]*w[1] + state[2]*w[2])
            if score > best_score:
                best_score = score
                best_axis = axis
        return best_axis, best_score

    def dispatch(self, state):
        axis, score = self.content_route(state)
        left_furnace, right_furnace = self.furnaces[axis]
        out_l, _ = left_furnace.evolve_and_process(state)
        out_r, _ = right_furnace.evolve_and_process(state)
        
        f_d3 = mod10(out_l[2] + out_r[2])
        f_d2 = mod10(out_l[1] + out_r[1])
        f_d1 = mod10(out_l[0] + out_r[0])
        final_state = (f_d1, f_d2, f_d3)
        
        return final_state, axis

if __name__ == "__main__":
    router = Full3DMoE()
    inputs = [3.141, 3.149, 3.172, 3.279]
    
    print(f"{'连续输入':<8} | {'编码小模':<12} | {'路由轴':<6} | {'输出小模':<12} | {'解码连续值':<10} | {'控制信号'}")
    print("-" * 70)
    
    for v in inputs:
        state = encode_continuous(v)
        out_state, axis = router.dispatch(state)
        out_cont = decode_to_continuous(out_state)
        action_signal = map_to_action(out_cont)
        
        print(f"{v:<10.3f} | {str(state):<14} | {axis:<8} | {str(out_state):<14} | {out_cont:<12.3f} | {action_signal:>+6.3f}")
