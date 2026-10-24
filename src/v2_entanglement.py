# -*- coding: utf-8 -*-
"""
Polaris V2: 幂积纠缠与心智演化 (Power Entanglement)
自指收敛、双生/三生纠缠、混沌边缘判定。
"""

from typing import Tuple, List

def power_iteration(start: int, power: int, steps: int = 10) -> Tuple[List[int], str]:
    """
    单变量自指多次幂迭代。
    返回: (轨迹列表, 最终归宿: "不动点"/"周期循环"/"混沌")
    """
    d = start
    path = [d]
    for _ in range(steps):
        d = (d ** power) % 10
        path.append(d)
        if len(path) >= 5 and len(set(path[-5:])) == 1:
            return path, "不动点"
        if len(path) >= 4 and path[-1] == path[-3] and path[-2] == path[-4]:
            return path, "周期循环"
    return path, "混沌"

def dual_entanglement(A: int, B: int, m: int, n: int, steps: int = 10) -> Tuple[Tuple[int, int], int]:
    """
    双生幂积纠缠。返回最终状态和达到收敛/循环所需的步数。
    """
    for step in range(1, steps + 1):
        A_new = (A ** m * B ** n) % 10
        B_new = (B ** m * A ** n) % 10
        if A_new == A and B_new == B:
            return (A, B), step
        A, B = A_new, B_new
    return (A, B), steps

def triple_entanglement(A: int, B: int, C: int, m: int = 2, n: int = 2, p: int = 2, steps: int = 10) -> Tuple[Tuple[int, int, int], int]:
    """
    三生幂积纠缠（多智能体共识）。
    返回最终状态和收敛步数。
    """
    for step in range(1, steps + 1):
        A_new = (A ** m * B ** n * C ** p) % 10
        B_new = (B ** m * C ** n * A ** p) % 10
        C_new = (C ** m * A ** n * B ** p) % 10
        if A_new == A and B_new == B and C_new == C:
            return (A, B, C), step
        A, B, C = A_new, B_new, C_new
    return (A, B, C), steps
