# Math Modeling Agent Skills · v2.7 正式版

**给第一次参加数学建模竞赛的三人队。** 从英文题、附件和分工开始，把每个小问落到模型、可复跑结果、图表、论文和交稿证据。可用于赛前陪练、正式比赛中的合规辅助，以及换队员后的接续。

[下载 v2.7 完整 ZIP](https://github.com/szy0387-beep/mcm-agent-skills/archive/refs/tags/v2.7.0.zip) · [项目网页](https://szy0387-beep.github.io/mcm-agent-skills/) · [本次亚太赛分工](#本次亚太赛三人四日分工) · [实战手册](HANDBOOK.md) · [发布记录](https://github.com/szy0387-beep/mcm-agent-skills/releases/latest)

## 三步开始

1. 下载并解压发行包。用 Codex 打开包含 `AGENTS.md` 的包根目录。**14 个核心 Skill 和 21 个专项 Skill** 均已随包提供。
2. 用 Python 3.10 或更新版本，从包根目录运行 `python scripts/new_case.py 我的题`，把原题和附件放进 `cases/我的题/inputs/`。也可以在 Codex 中附上文件并让它建档。已有附件或 CASE 的目录可以用同一条命令补齐。
3. 选择「赛前练习」「正式比赛」或「接着做」。告诉 Codex 当前小问、已有材料和这次要交什么。组内共享 `CASE.md` 和相关产物，从同一份记录接续。

### 赛前练习

> 用 `$mcm-skill-router` 带我们做一道往年英文题。题面和附件在 `cases/我的题/inputs/`。先审第一问，翻译关键条件，列清输入、单位和交付物。等我们写一个手算预期，再进入建模。

### 正式比赛

> 用 `$mcm-skill-router` 协助本次正式比赛。先对照当届规则核实允许的 AI 辅助范围。下面是本队已独立完成的工作和本轮需要的辅助。请注明证据位置、待核事项和实际使用情况，交由队员复核。

2026 亚太赛的核心模型构建、算法设计与求解、结果分析由参赛队独立完成。实际使用随手记录，终审核对披露与提交文件。数据、引文和数值都须能回查，仿真及合成数据如实标注。 [当届规则归档](docs/rules/2026-apmcm-en.md) · [AI 使用与学术诚信](docs/ai-usage-disclosure.md)

### 接着做

> 用 `$mcm-skill-router` 看进度。请只读当前案例的 `CASE.md` 和相关证据，告诉我已通过的阶段、要返工的小问，以及接手人下一步可以做什么。

在终端可以运行 `python scripts/case_status.py cases/我的题`。要继续执行时，再指定小问和希望交付的文件。 [换人接手与局部返工](docs/competition-run.md) · [更多可复制指令](docs/codex-prompts.md)

## 本次亚太赛三人四日分工

| 日期 | 建模手 | 编程手 | 论文手 | 晚间验收 |
| --- | --- | --- | --- | --- |
| 11 月 26 日 | 拆题、定基线 | 查附件、跑第一问 | 查文献、搭英文稿骨架 | 小问表、首份结果、来源表 |
| 11 月 27 日 | 独立验算主结果 | 跑各问、记录复跑 | 写方法、协作出图 | 主结果表、验算记录、图表初稿 |
| 11 月 28 日 | 写中文模型与结论 | 优化图表、写结果段 | 翻译及合并英文初稿 | 覆盖各问且可编译的英文稿 |
| 11 月 29 日 | 审题意、推导和结论 | 独立复跑、核对数字 | 合稿、核对格式和披露 | 三人共审，队长当晚提交 |

官方截止为北京时间 **11 月 30 日 09:00**。队内以 11 月 29 日晚为上传目标。 [当届参赛计划与交稿清单](docs/apmcm-2026.md) · [网页版分工](https://szy0387-beep.github.io/mcm-agent-skills/#apmcm-plan)

## 从题面到论文，每一步留下什么

| 阶段 | 应交给下一位队友的东西 | 入口 |
| --- | --- | --- |
| 读题、选题和建模 | 逐问任务表、原文出处、假设和手算基线 | [三人全流程](docs/end-to-end.md) · [常见题型](docs/modeling-methods.md) |
| 编程、验证和仿真 | 可复跑命令、结果表、独立验算与失败范围 | [赛程与验收](docs/competition-run.md) · [宇树案例复盘](docs/robotics-case.md) |
| 出图、引用与写作 | 同版本的图表、真实来源、论文源码 | [可视化](docs/visualization-guide.md) · [参考文献](docs/references-guide.md) · [亚太赛 LaTeX 模板](templates/apmcm-paper/) |
| 终审与交稿 | 独立重编的 PDF、逐问证据、规则要求的附件 | [论文自审](docs/paper-review.md) · [终稿复核](docs/final-delivery.md) · [AI 披露模板](templates/AI_USAGE_DISCLOSURE.md) |

[查看从赛题到论文的路线图](figures/first-contest-mindmap.md)

## 先在空目录跑一个合成题

这条命令仅用 Python 标准库。它会从合成英文调度题的 CSV 生成两组结果和 Overleaf 源码包。

```sh
python examples/dispatch/run_paper.py --output outputs/dispatch-paper --overleaf-zip
```

验收时应得到基准费用 **980**、每小时需求增加 10 MW 后的费用 **1120**，以及 **141 MW** 超出容量的反例。将 `outputs/dispatch-paper/overleaf.zip` 上传至 Overleaf，或解压后从 `main.tex` 本地编译。 [英文题面](examples/dispatch/problem-en.md) · [复跑步骤](examples/dispatch/README.md) · [三人交接示例](examples/dispatch/team-handoff.md)

## 技能一览

整题交给 `$mcm-skill-router`。遇到单项问题可以直接描述目标，也可点名对应 Skill。三个旧流程名 `$mcm`、`$math-modeling-solver`、`$math-modeling-paper` 可用于定向查资料。

| 你要做什么 | 核心入口 |
| --- | --- |
| 开题、协作或陪练 | [总路由](.agents/skills/mcm-skill-router/SKILL.md) · [三人合练](.agents/skills/mcm-team-drill/SKILL.md) · [英译与审题](.agents/skills/mcm-problem-translate/SKILL.md) |
| 建模、比较和实现 | [建模](.agents/skills/mcm-model-training/SKILL.md) · [方案对照](.agents/skills/mcm-model-comparison/SKILL.md) · [代码](.agents/skills/mcm-code-training/SKILL.md) · [复跑现有案例](.agents/skills/mcm-fast/SKILL.md) |
| 验证、图表和合练复盘 | [仿真](.agents/skills/mcm-simulation-training/SKILL.md) · [可视化](.agents/skills/mcm-visualization-training/SKILL.md) · [训练复盘](.agents/skills/mcm-training-review/SKILL.md) |
| 论文、引用和交稿 | [写作与编译](.agents/skills/mcm-paper-training/SKILL.md) · [引用](.agents/skills/mcm-citation/SKILL.md) · [论文自审](.agents/skills/mcm-paper-self-review/SKILL.md) · [AI 披露](.agents/skills/ai-usage-disclosure/SKILL.md) |

[专项技能目录](.agents/skills/mcm-skill-router/references/specialist-skills.md)包含数据检查、求解器审查、统计、网络、地图及制图工具。按每项任务的说明安装所需依赖。

## 验收与贡献

`python scripts/check_package.py` 核对技能、链接与锚点、第三方校验和、调度结果、CASE 接续和披露。CI 另外跑月度预测测试并编译三个论文样例。 [贡献说明](CONTRIBUTING.md) · [GitHub Actions](https://github.com/szy0387-beep/mcm-agent-skills/actions) · [版本记录](CHANGELOG.md)

自制内容采用 [MIT](LICENSE)。第三方 Skill 按各自的许可证与固定提交随包发布。 [第三方说明](THIRD_PARTY.md)
