# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
Polaris 纯整数诗词生成演示。
向中华古典文化致敬。
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.polaris.nn.poetry_engine import TopologicalPoetryEngine

def run_poetry_demo():
    print("=" * 50)
    print("☯️ Polaris 纯整数拓扑诗词引擎演示")
    print("=" * 50)
    print("提示：本引擎在纯整数域内（模10）推演，不使用任何浮点运算。\n")

    # 每次更换 seed，可以生成完全不同的诗词
    engine = TopologicalPoetryEngine(seed=999)
    
    topics = ["秋", "月", "雪", "江", "风"]
    
    for topic in topics:
        print(f"🎯 命题：【{topic}】")
        poem_lines = engine.generate(topic)
        for line in poem_lines:
            print(f"    {line}")
        print("-" * 30)

if __name__ == "__main__":
    run_poetry_demo()
