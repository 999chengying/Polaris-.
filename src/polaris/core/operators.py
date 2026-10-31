# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Core Operators
纯整数拓扑基础算子库（包含状态机、进位、逆元与空间偏移）。
"""

from typing import Tuple, Dict

State = Tuple[int, int, int]

class MiddlePalace:
    """
    中宫状态机：所有跨模操作（进位/借位/溢出）的唯一触发枢纽。
    """
    def __init__(self):
        self.state = 5
        self.trigger_count = 0

    def trigger(self) -> int:
        """执行 5 → 0 → 5 转换"""
        self.state = 0
        self.state = 5
        self.trigger_count += 1
        return self.state


class ArithmeticOperators:
    """
    纯整数算术算子，完全挂载于中宫状态机。
    """
    @staticmethod
    def add_one(state: State, palace: MiddlePalace) -> State:
        d1, d2, d3 = state
        if d3 < 9:
            d3 += 1
        else:
            d3 = 0
            palace.trigger()
            if d2 < 9:
                d2 += 1
            else:
                d2 = 0
                palace.trigger()
                d1 = (d1 + 1) % 10
        return (d1, d2, d3)

    @staticmethod
    def mul_k(state: State, k: int, palace: MiddlePalace) -> State:
        d1, d2, d3 = state
        raw3 = d3 * k
        carry1, d3_new = divmod(raw3, 10)
        if carry1 > 0: palace.trigger()

        raw2 = d2 * k + carry1
        carry2, d2_new = divmod(raw2, 10)
        if carry2 > 0: palace.trigger()

        raw1 = d1 * k + carry2
        carry3, d1_new = divmod(raw1, 10)
        if carry3 > 0: palace.trigger()

        return (d1_new, d2_new, d3_new)


class TopologicalOperators:
    """
    拓扑与空间偏移算子（逆元、破对称、三维十字路由）。
    """
    @staticmethod
    def inverse_rotate(state: State, k: int = 3) -> State:
        """逆元旋转（如乘3），纯整数无溢出"""
        return tuple((v * k) % 10 for v in state) # type: ignore

    @staticmethod
    def topological_offset_consensus(
        val_left: int, val_right: int, 
        addr_left: int, addr_right: int
    ) -> int:
        """
        拓扑偏移定则（核心公理）：打破 3+7=0 的对称死锁。
        """
        return (val_left * addr_left + val_right * addr_right) % 10

    @staticmethod
    def three_head_six_arms(state: State) -> Dict[str, State]:
        """
        三头六臂联动：生成身、影1（合十）、影2（加5）。
        """
        d1, d2, d3 = state
        return {
            "body": (d1, d2, d3),
            "shadow_1": ((10 - d1) % 10, (10 - d2) % 10, (10 - d3) % 10),
            "shadow_2": ((d1 + 5) % 10, (d2 + 5) % 10, (d3 + 5) % 10)
        }
