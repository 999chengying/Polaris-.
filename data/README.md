# Polaris- 数据目录 (Data Directory)

本目录包含了 Polaris 引擎所需的静态基础数据与 V2 动力学配置。

## 1. V1 基础拓扑数据 (3.0时代)
这些文件定义了九宫八卦立方体的基础静态空间结构：
- `faces.json`：立方体的表面共面点。
- `diagonals.json`：对角截面数据。
- `generating_pairs.json`：生成对与合十对。
- `24_mountains.json`：二十四山圆序映射。
- `cycles.json`：K=5~9 的天层显象结果。
- `55_50_models.json`：天地之数55与大衍之数50配置。
- `four_images.json`：四象（老阴、少阳、少阴、老阳）结构数据。

## 2. V2 动力学与心智数据 (4.0时代)
这些文件为 Polaris 的纯整数算术与多智能体阵法提供核心参数：
- **`v2_bagua_mapping.json`**：八卦与数字的映射字典，定义了“上卦为十位，下卦为个位”的六十四卦编码规则。
- **`v2_three_heads_rules.json`**：三头六臂阵法（身、合十影、加5影）的演化规则、死锁判定条件、以及“裁成辅相”的容错机制配置。

## 使用建议
开发者在使用 `src/v2_small_model.py` 和 `src/v2_entanglement.py` 时，建议通过 `json.load()` 读取这里的配置，以保证算法逻辑与底层常数解耦。
