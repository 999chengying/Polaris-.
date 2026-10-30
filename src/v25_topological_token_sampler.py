# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# 
# This is the core implementation of the Topological Token Sampler (PTPP Protocol).
#
# Licensed under the Apache License, Version 2.0

def mod10(x):
    return x % 10

# 模拟的微型词表
SIMULATED_VOCAB = [
    "天", "地", "玄", "黄", "宇", "宙", "洪", "荒", 
    "日", "月", "盈", "昃", "辰", "宿", "列", "张",
    "寒", "来", "暑", "往"
]

class TianxiangTai:
    def process(self, history_states):
        if not history_states: return 5
        total_sum = sum(sum(state) for state in history_states)
        return 5 if total_sum % 10 == 0 else total_sum % 10

class TianxiangLu:
    def process(self, current_state, aggregated_tai):
        d1, d2, d3 = current_state
        diff = abs(d1 - aggregated_tai) + abs(d2 - aggregated_tai) + abs(d3 - aggregated_tai)
        return 5 if diff == 0 else diff % 10

class MetaObserver:
    def __init__(self, threshold=3):
        self.history = []
        self.threshold = threshold
    def check_and_anchor(self, current_val):
        self.history.append(current_val)
        if len(self.history) >= self.threshold:
            recent = self.history[-self.threshold:]
            if len(set(recent)) == 1:
                self.history.clear()
                return 5
        return current_val

class TopoLanguageModel:
    def __init__(self, memory_size=3):
        self.tai = TianxiangTai()
        self.lu = TianxiangLu()
        self.observer = MetaObserver(threshold=3)
        self.memory = [] 
        self.memory_size = memory_size
        self.seed = 42 # 伪随机种子
        
    def pseudo_random(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed
        
    def generate_next(self, current_state):
        self.memory.append(current_state)
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)
            
        tai_val = self.tai.process(self.memory)
        lu_val = self.lu.process(current_state, tai_val)
        final_val = self.observer.check_and_anchor(lu_val)
        
        next_state = (
            mod10(final_val + current_state[0] + 1),
            mod10(final_val + current_state[1] + 3),
            mod10(final_val + current_state[2] + 5)
        )
        
        base_index = (next_state[0] * 100) + (next_state[1] * 10) + next_state[2]
        random_offset = self.pseudo_random() % len(SIMULATED_VOCAB)
        token_id = (base_index + random_offset) % len(SIMULATED_VOCAB)
        
        return next_state, token_id

if __name__ == "__main__":
    engine = TopoLanguageModel(memory_size=3)
    current = (3, 8, 1)
    generated_sentence = []
    
    print("=" * 60)
    print("☯️ Polaris V25: 拓扑语素采样")
    print("=" * 60)
    print(f"种子输入: {current}\n" + "-" * 60)
    
    for step in range(1, 16):
        next_state, token_id = engine.generate_next(current)
        word = SIMULATED_VOCAB[token_id]
        generated_sentence.append(word)
        print(f"步 {step:02d} | 状态: {next_state} | 采样词: 【{word}】")
        current = next_state
        
    print("-" * 60)
    print(f"🎯 最终生成的拓扑语：{''.join(generated_sentence)}")
