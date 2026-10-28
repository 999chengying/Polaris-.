# -*- coding: utf-8 -*-
"""
Polaris V10: 七宫分布式大阵 (3D-Cross MoE)
包含中央路由、三维空间偏置与纯整数算子。
依据：docs-v4/02-7-furnaces-cross-moe.md
"""

def mod10(x):
    return x % 10

class SubFurnace:
    def __init__(self, coord, wall_type):
        self.coord = coord
        self.wall_type = wall_type
        self.center = 5
        self.spatial_bias = sum(coord) % 10

    def activate_and_rotate(self, input_val):
        if self.wall_type == 'diff5':
            k = 3
        elif self.wall_type == 'diff1':
            k = 7
        elif self.wall_type == 'diff2':
            k = 2
        else:
            k = 1
        return mod10(input_val * k + self.center + self.spatial_bias)

class MasterRouter:
    def __init__(self):
        self.furnaces = {
            'X_left':   SubFurnace((1,3,3), 'diff5'),
            'X_right':  SubFurnace((5,3,3), 'diff5'),
            'Y_front':  SubFurnace((3,1,3), 'diff1'),
            'Y_back':   SubFurnace((3,5,3), 'diff1'),
            'Z_bottom': SubFurnace((3,3,1), 'diff2'),
            'Z_top':    SubFurnace((3,3,5), 'diff2')
        }

    def dispatch(self, input_val):
        if input_val % 2 != 0:
            # X轴 (差5/逻辑)
            v_left = self.furnaces['X_left'].activate_and_rotate(input_val)
            v_right = self.furnaces['X_right'].activate_and_rotate(input_val)
            final_val = mod10(v_left * 7 + v_right * 3 + input_val)
            axis = "X轴(逻辑)"
        elif input_val > 5:
            # Z轴 (差2/动作)
            v_bot = self.furnaces['Z_bottom'].activate_and_rotate(input_val)
            v_top = self.furnaces['Z_top'].activate_and_rotate(input_val)
            final_val = mod10(v_bot * 2 + v_top * 5)
            axis = "Z轴(动作)"
        else:
            # Y轴 (差1/感知)
            v_front = self.furnaces['Y_front'].activate_and_rotate(input_val)
            v_back = self.furnaces['Y_back'].activate_and_rotate(input_val)
            final_val = mod10(v_front * 4 + v_back * 6)
            axis = "Y轴(感知)"

        return final_val, axis

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris V10: 七炉阵")
    print("=" * 60)
    
    router = MasterRouter()
    test_inputs = [3, 7, 2, 8, 4]
    
    for val in test_inputs:
        out, axis = router.dispatch(val)
        print(f"输入: {val} | 路由至: {axis} | 最终决策值: {out}")
