# -*- coding: utf-8 -*-
"""
Polaris V14: 全息七炉阵 (Full 3D-MoE)
- 连续小模输入
- 纯整数注意力内容路由
- 动量记忆牵引
依据：docs-v4/03-full-3d-moe-furnace.md
"""

def mod10(x):
    return x % 10

def encode_continuous(val):
    s = f"{val:.3f}".split('.')
    return (int(s[1][0]), int(s[1][1]), int(s[1][2]))

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
        return (f_d1, f_d2, f_d3), axis

if __name__ == "__main__":
    router = Full3DMoE()
    inputs = [3.141, 3.149, 3.172, 3.279]
    for v in inputs:
        state = encode_continuous(v)
        out, axis = router.dispatch(state)
        print(f"输入: {v} | 路由轴: {axis} | 输出状态: {out}")
