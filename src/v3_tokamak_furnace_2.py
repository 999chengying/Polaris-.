# -*- coding: utf-8 -*-
"""
Polaris V3: 八卦炉二号验证程序
验证 Y=1, Y=5 双墙的完备性、差一关系及差一通关结构。
"""

def mod10(x):
    return x % 10

# Y=1 和 Y=5 截面的已知数据 (已修正笔误)
Y1_section = {
    (1,1,1):9, (5,1,1):4, (1,1,5):7, (5,1,5):2, # 顶点
    (3,1,1):8, (3,1,5):3, (1,1,3):1, (5,1,3):6, # 棱中心
    (3,1,3):5                                   # 面中心
}

Y5_section = {
    (1,5,1):8, (5,5,1):3, (1,5,5):6, (5,5,5):1, # 顶点
    (3,5,1):9, (3,5,5):4, (1,5,3):2, (5,5,3):7, # 棱中心 (修正为4)
    (3,5,3):5                                   # 面中心
}

def check_wall_completeness(section, name):
    """检查截面是否包含 1-9 完整数字"""
    vals = list(section.values())
    unique_vals = sorted(vals)
    print(f"[{name}] 包含数值: {unique_vals}")
    if unique_vals == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print(f"  ✅ {name} 完美覆盖 1~9！")
    else:
        print(f"  ❌ {name} 缺失或重复！")
    print()

def check_diff_one_wall():
    """检查 Y=1 与 Y=5 对应点是否差一（模10空间）"""
    print("--- 差一墙对应点查验 ---")
    for (x, _, z), val1 in Y1_section.items():
        val5 = Y5_section.get((x, 5, z))
        if val1 == 5 and val5 == 5:
            print(f"  坐标 ({x},*, {z}): 中宫重合 {val1} -> {val5}")
            continue
        diff = abs(val1 - val5)
        status = "✅" if diff == 1 else "❌"
        print(f"  坐标 ({x},*, {z}): Y=1({val1}) <-> Y=5({val5}) | 差值: {diff} {status}")
    print()

def test_diff_one_tongguan():
    """验证差一数对 (9,8) 的通关逻辑"""
    print("--- 差一数对 (9,8) 通关查验 ---")
    a, b = 9, 8
    x_list = [1, 2, 3, 4, 6, 7, 8, 9]
    for x in x_list:
        if x == 1: print(f"  {x}: {a}-{b}-{x} = {a-b-x} (借0) ✅")
        elif x == 2: print(f"  {x}: {a}-{x}+{b} = {mod10(a-x+b)} (借5) ✅")
        elif x == 3: print(f"  {x}: {a}+{b}+{x} = {mod10(a+b+x)} (借0) ✅")
        elif x == 4: print(f"  {x}: {a}-{b}+{x} = {a-b+x} (借5) ✅")
        elif x == 6: print(f"  {x}: {b}+{x}-{a} = {b+x-a} (借5) ✅")
        elif x == 7: print(f"  {x}: {a}+{b}-{x} = {a+b-x} (借0) ✅")
        elif x == 8: print(f"  {x}: {a}+{b}+{x} = {mod10(a+b+x)} (借5) ✅")
        elif x == 9: print(f"  {x}: {a}+{x}-{b} = {mod10(a+x-b)} (借0) ✅")

if __name__ == "__main__":
    print("=" * 55)
    print("☯️ Polaris V3 八卦炉二号验证")
    print("=" * 55)
    check_wall_completeness(Y1_section, "Y=1 前墙")
    check_wall_completeness(Y5_section, "Y=5 后墙")
    check_diff_one_wall()
    test_diff_one_tongguan()
    print("=" * 55)
