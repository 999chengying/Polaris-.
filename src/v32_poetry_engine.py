# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
#
# 纯整数平仄押韵诗词引擎 (Topological Poetry Generator)
# 基于五行、平仄与纯整数推演，生成五言绝句。
#
# Licensed under the Apache License, Version 2.0

def mod10(x):
    return x % 10

# 扩充词库
VOCAB = {
    "自然": ["山", "水", "风", "云", "雨", "雪", "花", "月", "江", "海", "天", "星", "林", "岸", "舟", "波", "秋", "春"],
    "动作": ["落", "飞", "流", "去", "来", "入", "涌", "生", "照", "掩", "过", "寻", "泛"],
    "形容": ["明", "暗", "高", "低", "远", "近", "空", "深", "幽", "寒", "静", "虚", "白", "青"]
}

def get_rhyme_group(char):
    return mod10(ord(char))

class TopoEmbedder:
    def encode_char(self, char):
        cat = 0
        for k, v in VOCAB.items():
            if char in v:
                cat = list(VOCAB.keys()).index(k)
                break
        d2 = mod10(ord(char))
        d3 = ord(char) % 2 # 0平 1仄
        return (cat, d2, d3)

class PoetryEngine:
    def __init__(self, memory_size=3):
        self.embedder = TopoEmbedder()
        self.memory = []
        self.memory_size = memory_size
        self.seed = 42
        
    def pseudo_random(self, max_val):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed % max_val
        
    def generate_poem(self, topic):
        print(f"\n[人类命题]：以【{topic}】为题，作五言绝句")
        print("-" * 60)
        
        poem_lines = []
        target_rhyme = None
        
        for line_idx in range(4):
            line_chars = []
            for char_idx in range(5):
                if line_idx == 0 and char_idx == 4:
                    candidates = [w for w in VOCAB["自然"] if ord(w) % 2 == 0]
                    rhyme_char = candidates[self.pseudo_random(len(candidates))]
                    target_rhyme = get_rhyme_group(rhyme_char)
                    line_chars.append(rhyme_char)
                    continue
                
                if not self.memory:
                    state = self.embedder.encode_char(topic)
                else:
                    state = self.memory[-1]
                
                self.memory.append(state)
                if len(self.memory) > self.memory_size: self.memory.pop(0)
                
                cat_target = self.pseudo_random(3)
                ping_ze_target = char_idx % 2 
                
                candidates = []
                for cat_name, words in VOCAB.items():
                    if list(VOCAB.keys()).index(cat_name) == cat_target:
                        for w in words:
                            if ord(w) % 2 == ping_ze_target:
                                if char_idx == 4 and (line_idx == 1 or line_idx == 3):
                                    if get_rhyme_group(w) == target_rhyme:
                                        candidates.append(w)
                                else:
                                    candidates.append(w)
                
                if not candidates:
                    candidates = ["风", "月", "山", "水"]
                    
                word = candidates[self.pseudo_random(len(candidates))]
                line_chars.append(word)
                self.memory.append(self.embedder.encode_char(word))
                
            poem_lines.append("".join(line_chars))
            
        return poem_lines

if __name__ == "__main__":
    engine = PoetryEngine()
    poem = engine.generate_poem("秋")
    for line in poem:
        print(f"    {line}")
