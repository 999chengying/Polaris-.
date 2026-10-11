# -*- coding: utf-8 -*-
"""
三链一宫：离散状态空间模拟器
验证顺行与逆行规则。
"""

import math

def mod9(x):
    r = x % 9
    return 9 if r == 0 else r

GRID = {
    (1,1,1):9,(3,1,1):5,(5,1,1):4,
    (1,3,1):1,(3,3,1):6,(5,3,1):1,
    (1,5,1):8,(3,5,1):5,(5,5,1):3,
    (1,1,3):6,(3,1,3):1,(5,1,3):6,
    (1,3,3):5,(3,3,3):5,(5,3,3):5,
    (1,5,3):4,(3,5,3):9,(5,5,3):4,
    (1,1,5):7,(3,1,5):5,(5,1,5):2,
    (1,3,5):1,(3,3,5):4,(5,3,5):1,
    (1,5,5):6,(3,5,5):5,(5,5,5):1,
}

CENTER = (3, 3, 3)

def canonical(c):
    return ((c - 1) % 6) + 1

def value_at(pos):
    x, y, z = pos
    return GRID.get((canonical(x), canonical(y), canonical(z)), None)

def geo_dist(pos):
    return math.sqrt(sum((pos[i] - CENTER[i])**2 for i in range(3)))

def neighbors(pos):
    x, y, z = pos
    result = []
    for dx in (-2, 0, 2):
        for dy in (-2, 0, 2):
            for dz in (-2, 0, 2):
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                p = (x+dx, y+dy, z+dz)
                v = value_at(p)
                if v is not None:
                    result.append((p, v))
    return result

def find_next_shun(target_num, current_pos, prev_dir):
    candidates = []
    for p, v in neighbors(current_pos):
        if v != target_num:
            continue
        d = tuple(p[i] - current_pos[i] for i in range(3))
        candidates.append((p, d))
    if not candidates:
        return None, None
    if prev_dir is None:
        return min(candidates, key=lambda x: (sum(abs(a) for a in x[1]), x[0]))
    return max(candidates, key=lambda x: (
        sum(a*b for a,b in zip(prev_dir, x[1])) /
        (math.sqrt(sum(a*a for a in prev_dir)) * math.sqrt(sum(a*a for a in x[1])) or 1),
        -sum(abs(a) for a in x[1]),
        tuple(-x for x in x[0])
    ))

def find_next_ni(current_pos, prev_dir):
    candidates = [p for p, v in neighbors(current_pos) if v == 5]
    if not candidates:
        return None
    best = None
    best_score = None
    for p in candidates:
        d = geo_dist(p)
        dot = sum(prev_dir[i]*(p[i]-current_pos[i]) for i in range(3)) if prev_dir else 0
        score = (d, -abs(dot), p)
        if best_score is None or score < best_score:
            best_score = score
            best = p
    return best

class ThreeChainNet:
    """三链一宫网络。"""

    def __init__(self, seq=None):
        self.seq = seq or [3, 5, 9, 5, 6, 5, 3]
        self.pos = CENTER
        self.prev_dir = None

    def shun(self, steps):
        """顺行steps步。"""
        seq_cycle = self.seq[1:] + [self.seq[0]]
        for _ in range(steps):
            target = seq_cycle.pop(0)
            seq_cycle.append(target)
            if value_at(self.pos) == target:
                continue
            p, d = find_next_shun(target, self.pos, self.prev_dir)
            if p is None:
                break
            self.pos = p
            if d and d != (0,0,0):
                self.prev_dir = d
        return self.pos

    def ni(self, max_steps=500):
        """逆行归中。"""
        prev_dir = None
        for step in range(max_steps):
            if self.pos == CENTER:
                return step
            p = find_next_ni(self.pos, prev_dir)
            if p is None:
                return None
            d = tuple(p[i]-self.pos[i] for i in range(3))
            self.pos = p
            prev_dir = d
        return None

    def reset(self):
        self.pos = CENTER
        self.prev_dir = None

if __name__ == "__main__":
    net = ThreeChainNet()
    print("=" * 50)
    print("三链一宫模拟器")
    print("=" * 50)
    print(f"初始位置：{net.pos}")
    net.shun(9 * 7)
    print(f"顺行9圈后：{net.pos}，距中宫{geo_dist(net.pos):.2f}")
    steps = net.ni()
    print(f"逆行{steps}步后：{net.pos}，距中宫{geo_dist(net.pos):.2f}")
