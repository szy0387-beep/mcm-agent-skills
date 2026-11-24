# Math Modeling Agent Skills

一套面向数学建模备赛的 Codex 技能。从审题、建模、代码、仿真和可视化，走到论文交付与结果审查。既可带人练真题，也可让 AI 自主训练并留下可复用的结果。

## 快速开始

1. 克隆或下载本仓库，用 Codex 打开仓库根目录。Codex 会从 `.agents/skills/` 发现项目技能。
2. 输入「用 `$mcm-skill-router` 帮我推荐一套流程。我已经有结果表，需要论文图和可编译的 Overleaf 论文」。
3. 想直接执行时，输入「按这个做」。只想了解路线时，描述目标和手头已有材料即可。

用 Python 3.10 或更新版本复跑内置合成案例。该案例只用 Python 标准库：

```sh
python .agents/skills/mcm-fast/scripts/dispatch.py examples/dispatch/units.csv examples/dispatch/demand.csv --output outputs/dispatch
```

输出总费用应为 **980**。[题目、手算对照与迁移验收](examples/dispatch/README.md)

## 技能一览

| Skill | 用途 |
| --- | --- |
| [mcm-skill-router](.agents/skills/mcm-skill-router/SKILL.md) | 推荐或执行当前最合适的流程 |
| [mcm-model-training](.agents/skills/mcm-model-training/SKILL.md) | 审题、约束、假设、可验算基准 |
| [mcm-code-training](.agents/skills/mcm-code-training/SKILL.md) | 实现、复跑、求解状态和验错 |
| [mcm-simulation-training](.agents/skills/mcm-simulation-training/SKILL.md) | 过程仿真、情景和灵敏度 |
| [mcm-visualization-training](.agents/skills/mcm-visualization-training/SKILL.md) | 论文图、数据口径和视觉复核 |
| [mcm-paper-training](.agents/skills/mcm-paper-training/SKILL.md) | 竞赛论文源稿、Overleaf 和证据对照 |
| [mcm-training-review](.agents/skills/mcm-training-review/SKILL.md) | 独立复算、单错反例、迁移与复盘 |
| [mcm-fast](.agents/skills/mcm-fast/SKILL.md) | 复跑本包的调度示例和可复用的月度预测脚本 |
| [mcm-team-drill](.agents/skills/mcm-team-drill/SKILL.md) | 个人陪练与三人队交接 |

## 可选专项技能

核心流程开箱可用。需要统计、优化、仿真或审图方面的专项参考时，可从锁定的上游版本安装：

```sh
python scripts/install_extras.py --list
python scripts/install_extras.py exploratory-data-analysis statsmodels
python scripts/install_extras.py --all
```

安装脚本调用本机 Codex 的系统 Skill Installer。可通过 `--installer` 指定其路径。安装目标为此仓库的 `.agents/skills/`，新增专项可按需点名调用。专项技能使用的 Python 包按各自说明另行安装。[专项技能版本及来源](third-party-skills.json)

在正式比赛中，按当届组委会规则确定 AI 使用范围、提交内容和披露要求。练习真题可从[亚太赛官网](https://www.apmcm.org/)等赛事站点获取。

## 许可证

本仓库自制内容采用 [MIT](LICENSE)。通过可选安装器取得的技能由[各自上游许可证](third-party-skills.json)授权。
