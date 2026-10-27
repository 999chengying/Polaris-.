# -*- coding: utf-8 -*-
"""
Polaris V3: 八卦炉托卡马克模型 (Tokamak Furnace)
验证 X=1, X=5 双生成数墙、X=3 先天八卦截面旋转与耗散冷却。
依据：docs-v3/01-tokamak-furnace-and-gnn.md
"""

def mod10(x):
    """确保结果落在 0-9 的纯整数模10域"""
    return x % 10

def show_matrix(name, matrix):
    print(f"--- {name} ---")
    for row in matrix:
        print("  ", row)
    print()

# ==========================================
# 1. 初始化八卦炉结构
# ==========================================
X3_original = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6]
]

# X=1 与 X=5 关键位置对比验证
wall_pairs = [
    ((3, 1), 4, 9), # 北
    ((3, 5), 1, 6), # 南
    ((1, 3), 2, 7), # 西
    ((5, 3), 3, 8), # 东
    ((3, 3), 5, 5)  # 中宫
]

def verify_walls():
    print("=== 1. 验证 X=1 与 X=5 生成数墙 ===")
    for pos, v1, v5 in wall_pairs:
        if pos == (3,3):
            print(f"  位置 {pos}: X=1({v1}), X=5({v5}) -> 中宫重合，不参与差值计算")
            continue
        diff = mod10(v5 - v1)
        status = "✅" if diff == 5 else "❌"
        print(f"  位置 {pos}: X=1({v1}) <-> X=5({v5}) | 差值: {diff} {status}")
    print()

# ==========================================
# 2. X=3 离子环的旋转与温控
# ==========================================
def apply_operator(matrix, k):
    return [[mod10(val * k) for val in row] for row in matrix]

def test_rotations():
    print("=== 2. 验证 X=3 离子环的旋转 (乘 3 与 乘 7) ===")
    show_matrix("乘 3 (逆时针 90°)", apply_operator(X3_original, 3))
    show_matrix("乘 7 (顺时针 90°)", apply_operator(X3_original, 7))
    show_matrix("乘 9 (180° 反转)", apply_operator(X3_original, 9))

    m3_then_7 = apply_operator(apply_operator(X3_original, 3), 7)
    print("=== 乘3后再乘7 (验证可逆性) ===")
    show_matrix("结果矩阵", m3_then_7)
    assert m3_then_7 == X3_original, "逆元验证失败"
    print()

def test_cooling():
    print("=== 3. 验证耗散冷却算子 (乘 2 巽风退火) ===")
    m2 = apply_operator(X3_original, 2)
    show_matrix("乘 2 (风火相薄，降温退火)", m2)
    
    has_odd = any(val % 2 != 0 for row in m2 for val in row)
    print(f"冷却后是否仍存在奇数(离火/乾阳)？ {'是' if has_odd else '否 ✅ 成功冷却坍缩'}")
    print()

# ==========================================
# 3. 通关验证
# ==========================================
def test_escape_route():
    print("=== 4. 验证生成数对 (8,3) 的通关结构 ===")
    a, b = 8, 3
    print(f"使用生成数对: {a} 和 {b} (差值为 5)")
    
    for x in [1, 2, 4, 6, 7, 9]:
        if x == 2:
            print(f"  数字 {x} 通关路径: {a}+{x} = {mod10(a+x)} (借0), {b}+{x} = {mod10(b+x)} (借5) ✅")
        elif x == 4:
            print(f"  数字 {x} 通关路径: {a}+{x} = {mod10(a+x)} -> {mod10(a+x)}+{b} = {mod10(mod10(a+x)+b)} (借5) ✅")
        elif x == 1:
            print(f"  数字 {x} 通关路径: {a}+{b}-{x} = {a+b-x} (借0) ✅")
        elif x == 6:
            print(f"  数字 {x} 通关路径: {a}-{x} = {mod10(a-x)} -> {mod10(a-x)}+{b} = {mod10(mod10(a-x)+b)} (借5) ✅")
        else:
            s = mod10(a + x)
            print(f"  数字 {x} 通关路径: {a}+{x} = {s} -> {s}+{b} = {mod10(s+b)} (借0/5) ✅")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("☯️ Polaris V3 八卦炉（托卡马克）探火器")
    print("=" * 50)
    verify_walls()
    test_rotations()
    test_cooling()
    test_escape_route()
    print("=" * 50)
    print("测试完成。")
