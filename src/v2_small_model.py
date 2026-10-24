# -*- coding: utf-8 -*-
"""
Polaris V2: 连续值小模（Continuous Small Model）
纯整数分形嵌套，支持无限精度四则运算，告别浮点误差。
"""

from typing import List, Tuple, Optional

# 状态表示：三元组 (十分位, 百分位, 千分位)
SmallModelState = Tuple[int, int, int]

def add_one(state: SmallModelState) -> Tuple[SmallModelState, bool]:
    """
    连续值小模加1法。
    返回: (新状态, 是否触发中宫进位转换)
    """
    d1, d2, d3 = state
    carry_triggered = False
    
    if d3 < 9:
        d3 += 1
    else:
        d3 = 0
        carry_triggered = True
        
        if d2 < 9:
            d2 += 1
        else:
            d2 = 0
            if d1 < 9:
                d1 += 1
            else:
                d1 = 0
                
    return (d1, d2, d3), carry_triggered

def sub_one(state: SmallModelState) -> Tuple[SmallModelState, bool]:
    """
    连续值小模减1法（含虚空翻转）。
    返回: (新状态, 是否触发中宫借位转换)
    """
    d1, d2, d3 = state
    borrow_triggered = False
    
    if d3 > 0:
        d3 -= 1
    else:
        d3 = 9
        borrow_triggered = True
        
        if d2 > 0:
            d2 -= 1
        else:
            d2 = 9
            if d1 > 0:
                d1 -= 1
            else:
                d1 = 9 # 虚空翻转
                
    return (d1, d2, d3), borrow_triggered

def add_k(state: SmallModelState, k: int) -> Tuple[SmallModelState, int]:
    """
    在最低位(千分位)加上k。返回总进位次数（即中宫触发次数）。
    """
    d1, d2, d3 = state
    raw_d3 = d3 + k
    carry1 = raw_d3 // 10
    d3 = raw_d3 % 10
    
    raw_d2 = d2 + carry1
    carry2 = raw_d2 // 10
    d2 = raw_d2 % 10
    
    raw_d1 = d1 + carry2
    carry3 = raw_d1 // 10
    d1 = raw_d1 % 10
    
    total_carries = carry1 + carry2 + carry3
    return (d1, d2, d3), total_carries

def decimal_division(dividend: int, divisor: int, depth: int = 10) -> Tuple[List[int], bool]:
    """
    连续值小模的除法（无限嵌套）。
    返回: (各位上的商列表, 是否在depth步内除尽)
    """
    remainder = dividend
    digits = []
    for _ in range(depth):
        val = remainder * 10
        q = val // divisor
        remainder = val % divisor
        digits.append(q)
        if remainder == 0:
            return digits, True
    return digits, False
