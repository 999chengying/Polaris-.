# -*- coding: utf-8 -*-
"""
Polaris V2 核心补丁：中宫状态机 + 乘法 + 三头六臂联动
依据：V2-01/02/10/14 号文档。
说明：本文件未在运行环境验证，逻辑依据文档推演，自检函数打印预期输出供后续对账。
"""

from typing import Tuple, Optional, List, Dict

SmallModelState = Tuple[int, int, int]


# ============================================================
# 中宫状态机：V2-14 号声明的“唯一枢纽”
# ============================================================

class MiddlePalace:
    """
    中宫 5→0→5 状态机。
    所有跨模操作（进位/借位/溢出/归核）均挂载此对象。
    """

    def __init__(self):
        self.state = 5
        self.triggers = 0
        self.log: List[Tuple[int, int, int, str]] = []

    def trigger(self, reason: str = "") -> int:
        """执行一次 5→0→5 转换，返回转换后状态（恒为5）。"""
        self.log.append((5, 0, 5, reason))
        self.state = 0
        self.state = 5
        self.triggers += 1
        return self.state

    def reset(self):
        self.state = 5
        self.triggers = 0
        self.log.clear()

    def __repr__(self):
        return f"MiddlePalace(state={self.state}, triggers={self.triggers})"


# ============================================================
# 乘法：V2-02 号，从低位起乘，商进位
# ============================================================

def mul_k(state: SmallModelState, k: int,
          palace: Optional[MiddlePalace] = None
          ) -> Tuple[SmallModelState, int, MiddlePalace]:
    """
    连续值小模乘 k。
    规则（V2-02）：
      d3 = (d3 × k) mod 10
      d2 = (d2 × k + carry1) mod 10
      d1 = (d1 × k + carry2) mod 10
    每一位产生进位时触发中宫 5→0→5。
    返回: (新状态, 总进位次数, 中宫状态机)
    """
    if palace is None:
        palace = MiddlePalace()

    d1, d2, d3 = state
    total_carries = 0

    # 千分位（最低位）
    raw3 = d3 * k
    carry1 = raw3 // 10
    d3_new = raw3 % 10
    if carry1 > 0:
        palace.trigger(f"d3={d3}×{k}={raw3} 进位{carry1}")
        total_carries += carry1

    # 百分位
    raw2 = d2 * k + carry1
    carry2 = raw2 // 10
    d2_new = raw2 % 10
    if carry2 > 0:
        palace.trigger(f"d2={d2}×{k}+{carry1}={raw2} 进位{carry2}")
        total_carries += carry2

    # 十分位
    raw1 = d1 * k + carry2
    carry3 = raw1 // 10
    d1_new = raw1 % 10
    if carry3 > 0:
        palace.trigger(f"d1={d1}×{k}+{carry2}={raw1} 进位{carry3}")
        total_carries += carry3

    return (d1_new, d2_new, d3_new), total_carries, palace


# ============================================================
# 加减法改造版：挂载中宫状态机
# 依据 V2-01 号原文代码：d3/d2 进位触发中宫，d1 溢出/虚空翻转不触发
# ============================================================

def add_one_v2(state: SmallModelState,
               palace: Optional[MiddlePalace] = None
               ) -> Tuple[SmallModelState, MiddlePalace]:
    """V2-01 加1法，挂载中宫。d1 溢出重置不触发中宫（依原文）。"""
    if palace is None:
        palace = MiddlePalace()
    d1, d2, d3 = state

    if d3 < 9:
        d3 += 1
    else:
        d3 = 0
        palace.trigger("d3=9 加1进位")
        if d2 < 9:
            d2 += 1
        else:
            d2 = 0
            palace.trigger("d2=9 加1级联进位")
            if d1 < 9:
                d1 += 1
            else:
                d1 = 0  # 溢出重置，不触发中宫
    return (d1, d2, d3), palace


def sub_one_v2(state: SmallModelState,
               palace: Optional[MiddlePalace] = None
               ) -> Tuple[SmallModelState, MiddlePalace]:
    """
    V2-01 减1法，含虚空翻转，挂载中宫。
    注意：(0,0,0)-1 触发中宫 2 次（d3借位、d2级联借位），
    d1 的虚空翻转不触发中宫——与原文“中宫连跳两次”一致。
    """
    if palace is None:
        palace = MiddlePalace()
    d1, d2, d3 = state

    if d3 > 0:
        d3 -= 1
    else:
        d3 = 9
        palace.trigger("d3=0 减1借位")
        if d2 > 0:
            d2 -= 1
        else:
            d2 = 9
            palace.trigger("d2=0 减1级联借位")
            if d1 > 0:
                d1 -= 1
            else:
                d1 = 9  # 虚空翻转，不触发中宫
    return (d1, d2, d3), palace


# ============================================================
# 三头六臂联动：V2-10 号
# 影1 = 合十态 (10 - x) mod 10；影2 = 加5态 (x + 5) mod 10
# ============================================================

def shadow_he_shi(x: int) -> int:
    """影1：合十态。1↔9, 6↔4, 5↔5, 0↔0。"""
    return (10 - x) % 10


def shadow_jia_wu(x: int) -> int:
    """影2：加5态。1↔6, 6↔1, 0↔5, 5↔0。"""
    return (x + 5) % 10


def three_head_six_arms(state: SmallModelState) -> Dict[str, SmallModelState]:
    """返回身、影1合十、影2加5 三组三元组。"""
    d1, d2, d3 = state
    return {
        "身": (d1, d2, d3),
        "影1_合十": (shadow_he_shi(d1), shadow_he_shi(d2), shadow_he_shi(d3)),
        "影2_加5": (shadow_jia_wu(d1), shadow_jia_wu(d2), shadow_jia_wu(d3)),
    }


# ============================================================
# 自检：打印逻辑推演结果，供后续运行环境对账
# ============================================================

def self_check():
    print("=" * 60)
    print("V2 核心补丁自检（逻辑推演，未在运行环境验证）")
    print("=" * 60)

    # 1. 乘法：8×2=16 应触发下爻动，得 (0,1,6)
    s, c, p = mul_k((0, 0, 8), 2)
    print(f"[乘2] (0,0,8)×2 -> {s}, 进位{c}, 中宫触发{p.triggers}次")
    assert s == (0, 1, 6) and c == 1 and p.triggers == 1, "乘2偏差"
    print("  预期 (0,1,6)，进位1，中宫1次 —— OK")

    # 2. 乘9合十：2×9=18 -> (0,1,8)
    s, c, p = mul_k((0, 0, 2), 9)
    print(f"[乘9] (0,0,2)×9 -> {s}, 进位{c}")
    assert s == (0, 1, 8), "乘9合十偏差"
    print("  预期 (0,1,8) —— OK")

    # 3. 乘9：5×9=45 -> (0,4,5)，合十对 5↔5
    s, c, p = mul_k((0, 0, 5), 9)
    print(f"[乘9] (0,0,5)×9 -> {s}")
    assert s == (0, 4, 5), "乘9对5偏差"
    print("  预期 (0,4,5) —— OK")

    # 4. 加1进位：(0,0,9)+1 -> (0,1,0)，中宫1次
    s, p = add_one_v2((0, 0, 9))
    print(f"[加1] (0,0,9)+1 -> {s}, 中宫触发{p.triggers}次")
    assert s == (0, 1, 0) and p.triggers == 1, "加1进位偏差"
    print("  预期 (0,1,0)，中宫1次 —— OK")

    # 5. 虚空翻转：(0,0,0)-1 -> (9,9,9)，中宫2次（非3次）
    s, p = sub_one_v2((0, 0, 0))
    print(f"[减1] (0,0,0)-1 -> {s}, 中宫触发{p.triggers}次")
    assert s == (9, 9, 9) and p.triggers == 2, "虚空翻转偏差"
    print("  预期 (9,9,9)，中宫2次（d1虚空翻转不触发） —— OK")

    # 6. 三头六臂：身 (1,6,7) 的影1/影2
    t = three_head_six_arms((1, 6, 7))
    print(f"[三头六臂] 身(1,6,7) -> 影1{t['影1_合十']}, 影2{t['影2_加5']}")
    assert t["影1_合十"] == (9, 4, 3), "影1合十偏差"
    assert t["影2_加5"] == (6, 1, 2), "影2加5偏差"
    print("  预期 影1(9,4,3)，影2(6,1,2) —— OK")

    print("=" * 60)
    print("自检全部通过（逻辑推演）")


if __name__ == "__main__":
    self_check()
