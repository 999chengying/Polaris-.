# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Topological Poetry Engine
基于受限拓扑解码器与语法状态机的五言绝句生成引擎。
"""

from typing import List, Tuple, Dict

class TopologicalPoetryEngine:
    """
    纯整数诗词生成引擎。
    结合平仄校验、词性模板与纯整数拓扑推演。
    """
    
    def __init__(self, seed: int = 888):
        self.seed = seed
        
        # 词性分类 (0=名词, 1=动词/介词, 2=形容词/副词)
        self.vocab: Dict[int, List[str]] = {
            0: list(set("天地山月风雪花草江海星林岸舟波秋春夜日暮晓霜露松竹梅鹤雁沙烟阁楼琴剑酒梦影泉谷峰云水雨石径川泽")),
            1: list(set("落飞流去来入涌生照掩过寻泛望听问惊破点染舞醉笑泣宿隐起灭抱摘连度归行转落满照")),
            2: list(set("明暗高低远近空深幽寒静虚白青孤残芳翠苍冷暖新旧长短闲独满寂寞清愁断惊乱翠碧幽静"))
        }
        
        # 平声字表 (0=平, 1=仄)
        ping_words = "天寒来云腾阳飞流直三千河入海穷千层楼山春草木溅花鸟心空人闻深林青苔眠觉啼风雨声多少松童言师采药去只此中云不知千绝万径踪灭孤舟翁独钓江雪急高猿哀渚清白回无落木萧萧尽滚碧妆成树条垂绿丝绦细叶裁二月剪刀黄远白间片城仞羌笛须怨杨春度关门渭朝浥轻尘客舍青柳色新君更尽杯酒西阳故寒连江夜吴明送楚山孤洛阳亲友如相问片冰心壶青枝愁烟沉飞"
        self.ping_set = set(list(ping_words))
        
        # 五言绝句格律与语法模板
        self.ping_ze_patterns = [
            [1, 1, 0, 0, 1],
            [0, 0, 1, 1, 0],
            [1, 1, 0, 0, 1],
            [0, 0, 1, 1, 0]
        ]
        self.grammar_patterns = [
            [2, 0, 1, 2, 0], # 形-名-动-形-名 (如：寒山飞白云)
            [2, 0, 1, 0, 0], # 形-名-动-名-名 (如：孤舟寻夜月)
            [0, 0, 1, 0, 0], # 名-名-动-名-名 (如：风雨落残花)
            [2, 0, 1, 0, 0]  
        ]

    def _pseudo_random(self, max_val: int) -> int:
        """线性同余发生器 (LCG)"""
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed % max_val

    def _get_ping_ze(self, char: str) -> int:
        """平仄判定 (0=平, 1=仄)"""
        return 0 if char in self.ping_set else 1

    def _get_rhyme(self, char: str) -> int:
        """利用 Unicode 尾数模拟韵部"""
        return ord(char) % 6

    def generate(self, topic_char: str) -> List[str]:
        """
        生成五言绝句。
        
        Args:
            topic_char: 核心意象（如 '秋', '月', '雪'）
            
        Returns:
            包含 4 句诗的列表
        """
        poem = []
        target_rhyme = self._get_rhyme(topic_char)
        used_chars = set()

        for line_idx in range(4):
            line_chars = []
            for char_idx in range(5):
                target_ping_ze = self.ping_ze_patterns[line_idx][char_idx]
                target_grammar = self.grammar_patterns[line_idx][char_idx]
                is_rhyme_pos = (char_idx == 4 and line_idx in [1, 3])
                
                # 拓扑状态混沌扰动 (基于主题字与位置)
                final_val = (ord(topic_char) + line_idx + char_idx) % 10

                # 1. 严格状态机过滤
                candidates = []
                for word in self.vocab[target_grammar]:
                    if self._get_ping_ze(word) != target_ping_ze: continue
                    if word in used_chars: continue
                    if is_rhyme_pos and self._get_rhyme(word) != target_rhyme: continue
                    candidates.append(word)

                # 2. 兜底机制
                if not candidates:
                    candidates = [w for w in self.vocab[target_grammar] if self._get_ping_ze(w) == target_ping_ze]
                if not candidates:
                    candidates = self.vocab[target_grammar]

                # 3. 纯整数采样
                offset = (self._pseudo_random(len(candidates)) + final_val) % len(candidates)
                word = candidates[offset]
                
                used_chars.add(word)
                line_chars.append(word)
                
            poem.append("".join(line_chars))
            
        return poem
