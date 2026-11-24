# 数学建模可视化怎么选

先写下图要回答的小问、结果文件与列、数据单位和图的用途，再选工具。每次先选一项专项 Skill，论文版再按需要做一次审图。

| 你要做什么 | 先用哪个 Skill | 交图前看什么 |
| --- | --- | --- |
| 生成论文里的折线、柱状或多面板图 | [matplotlib](../.agents/skills/matplotlib/SKILL.md) | 缩到论文中的实际宽度，看图例、单位、标记与限值线是否清楚。 |
| 看分布、组间差异、相关性或统计区间 | [seaborn](../.agents/skills/seaborn/SKILL.md) | 标样本量和聚合规则，区分散布与估计不确定性。设定区间时确认独立单位与重复观测。 |
| 用悬停、缩放和切换图例检查情景 | [visualization · Plotly](../.agents/skills/visualization/SKILL.md) | 交付可离线打开的 HTML 与数据表。如果论文需要这张图，用赛事允许的静态格式导出或复画。 |
| 画分区指标、选址、运输路线或覆盖范围 | [geopandas](../.agents/skills/geopandas/SKILL.md) | 核对边界来源、坐标参考系、连接失败数和缺失值图例。计算距离和面积时选合适的投影。 |
| 画解题流程、小问依赖或算法步骤 | [mermaid-diagrams](../.agents/skills/mermaid-diagrams/SKILL.md) | 保留 Mermaid 源码。检查方向、分支文字和返工路径，导出后核对裁切与字体。 |
| 核对已有论文图的误差带、颜色和可读性 | [scientific-visualization](../.agents/skills/scientific-visualization/SKILL.md) | 从结果表独立复算标出的数字，核对同量指标的刻度、区间定义和图文一致性。 |

想从题设要求一路做到可复跑的论文图，先用 [竞赛可视化训练](../.agents/skills/mcm-visualization-training/SKILL.md)。图式、署名和匿名要求以用户指定模板与赛事规则为准。

## 用已有结果做一张离线交互图

先生成英文调度练习的结果。Plotly 仅在做交互图时需要，可在当前案例的 Python 环境安装。

```sh
python examples/dispatch/run_paper.py --output outputs/dispatch-viz
python -m pip install plotly
```

在仓库根目录新建自己的绘图脚本，运行下面的示例。两组数据都直接来自求解结果。打开 `outputs/dispatch-viz/costs.html` 后，可以逐小时核对费用。

```python
from csv import DictReader
from pathlib import Path

import plotly.graph_objects as go

folder = Path("outputs/dispatch-viz")
figure = go.Figure()
for directory, label in (("base", "Base"), ("plus10", "Demand +10 MW per hour")):
    with (folder / directory / "schedule.csv").open(encoding="utf-8", newline="") as source:
        rows = list(DictReader(source))
    figure.add_bar(
        x=[f"Hour {row['hour']}" for row in rows],
        y=[int(row["cost"]) for row in rows],
        name=label,
        hovertemplate="%{x}<br>Cost: %{y}<extra>%{fullData.name}</extra>",
    )
figure.update_layout(barmode="group", xaxis_title="Hour", yaxis_title="Cost units")
figure.update_yaxes(rangemode="tozero")
figure.write_html(folder / "costs.html", include_plotlyjs=True)
```

基准总费用应为 980，增加需求后为 1120。这三个小时是三个确定的调度时段，图比较逐小时费用。论文中的静态图可用同一份结果表生成。[调度练习与验算](../examples/dispatch/README.md) · [图与正文的证据对照](final-delivery.md)

## 一张图从试跑到可入稿

1. **先定一句结论。** 例如「每小时需求加 10 MW，总费用从 980 升到 1120」。把基准和情景费用放在相同刻度，以总费用复算 140 的绝对差额和约 14.3% 的相对增幅。图注写明分母为基准费用。
2. **把不可行和费用区分开。** 141 MW 是独立的不可行情景，容量总上限为 140 MW。可以在需求图画 140 MW 限值线，并以单独标记说明 141 MW 越界，保留单位和失败时段。在费用图中把缺失结果明示为不可行。
3. **按最终版面复核。** 从结果表抽查两点，打开论文尺寸下的 PDF，确认两种线型或标记在灰度下仍能区分，轴量纲和图例完整。把图文件、制图命令、结果版本和图号一起交给论文手。 [出图 Skill](../.agents/skills/mcm-visualization-training/SKILL.md)

## 调用时把输入和目的说清楚

- 「用 `$seaborn` 看这批残差按模型怎样分布，写清每组样本量和单位。」
- 「用 `$visualization` 从两份结果表做离线 HTML，鼠标悬停显示方案名和数值。」
- 「用 `$geopandas` 把各区覆盖率按区划代码连接，先列连接失败的行，再画一张区分缺失与零值的地图。」
- 「用 `$mermaid-diagrams` 画出这四问的依赖关系，标出验收失败后要返回的步骤。」
