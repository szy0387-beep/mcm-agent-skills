# 合成例题 · 两台机组的三小时调度

两台机组的出力和成本见 [units.csv](units.csv)，每小时需求见 [demand.csv](demand.csv)。每台机组可以关停，或按整数 MW 在出力上下限内发电。两台出力之和等于当时的需求。开机小时费用等于固定费用加上出力乘以单位费用。本例按小时独立计算。

从仓库根目录运行：

```sh
python .agents/skills/mcm-fast/scripts/dispatch.py examples/dispatch/units.csv examples/dispatch/demand.csv --output outputs/dispatch
```

| 小时 | 需求（MW） | A 出力（MW） | B 出力（MW） | 费用 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 35 | 35 | 0 | 200 |
| 2 | 95 | 80 | 15 | 500 |
| 3 | 55 | 55 | 0 | 280 |

正确的总费用为 **980**。在第 2 小时，两台都必须启用。A 的每 MW 成本更低，因此给 A 分配最大可行出力 80 MW，B 补 15 MW。结果文件包括逐时的 `schedule.csv` 和总费用 `summary.json`。

训练时可以把第二小时的需求换成 141 MW，程序应拒绝不可行输入。再把三小时需求都提高 10 MW，先手算新排班，再核对程序总费用 **1120**。做图时用 `schedule.csv`，让图和英文结果段引用同一份计算输出。
