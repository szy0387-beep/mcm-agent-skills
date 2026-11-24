---
name: mcm-fast
description: 用仓库自带的脚本快速复跑合成调度或月度预测，交付机器可读结果、简短摘要与验算证据。
---

从仓库根目录运行以下入口，先读取摘要，再按需要打开逐条结果。新数据先核对目标、时间粒度、单位和适用假设。

- **两机组调度。** 运行 `python .agents/skills/mcm-fast/scripts/dispatch.py examples/dispatch/units.csv examples/dispatch/demand.csv --output outputs/dispatch`。换输入时写入新的输出目录。计算设定、手算与迁移案例见[调度示例](../../../examples/dispatch/README.md)。
- **月度预测。** 安装 NumPy 和 Matplotlib，然后运行 `python .agents/skills/mcm-fast/scripts/monthly.py <CSV> --date <年月列> --value <数值列> --unit <单位> --output <目录>`。输入连续月度观测。脚本使用扩展训练窗口，支持用 `--folds`、`--horizon` 调整留出窗口。先查脚本的 `--help` 核对输入。

汇报关键指标、验证状态和产物路径。出现未覆盖的题型时，让调度入口按当前小问选择建模、实现或仿真流程。
