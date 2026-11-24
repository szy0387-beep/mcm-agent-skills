# Math Modeling Agent Skills

**给第一次参加数学建模竞赛的三人队。** 用自己的题面和附件开题，从读题、建模和求解走到出图、写论文与交叉验算。也支持个人陪练和 AI 自主训练。

[项目主页](https://szy0387-beep.github.io/mcm-agent-skills/) · [实战百科](HANDBOOK.md) · [本次亚太赛分工](#本次亚太赛三人四日分工) · [常用资料](#常用资料) · [下载完整 ZIP](https://github.com/szy0387-beep/mcm-agent-skills/archive/refs/heads/main.zip) · [发布说明](https://github.com/szy0387-beep/mcm-agent-skills/releases/latest) · [更新日志](CHANGELOG.md)

## 数学建模实战百科

| 现在要做什么 | 打开这一章 |
| --- | --- |
| 拿到题目，想和队友从读题走到提交 | [全流程与三人分工](docs/end-to-end.md) |
| 知道要交什么，想选模型、算法和验证方式 | [常见题型与方法](docs/modeling-methods.md) |
| 想看一套真实案例如何分析、运行、写进论文 | [宇树机器人赛题全流程复盘](docs/robotics-case.md) |
| 想亲手把英文题做成一篇可编译的练习稿 | [英文调度完整短例](examples/dispatch/README.md) |
| 计算已做完，准备核对结论、打包并交稿 | [终稿复核和源码包检查](docs/final-delivery.md) |

## 本次亚太赛三人四日分工

| 日期 | 建模手 | 编程手 | 论文手 | 晚间交付 |
| --- | --- | --- | --- | --- |
| 11 月 26 日 | 拆题、定基线 | 查数据，跑通第一问 | 找文献和相关方法，搭英文稿骨架 | 小问表、首份结果和文献表 |
| 11 月 27 日 | 验算并核对思路 | 跑各问主结果 | 理解项目，写方法段，协作出图 | 主结果、验算记录和图表初稿 |
| 11 月 28 日 | 写中文模型与结论 | 写中文结果段，优化图表 | 翻译并合并成英文初稿 | 覆盖各问、可导出 PDF 的英文稿 |
| 11 月 29 日 | 审模型、推导和结论 | 复跑并核对论文数字 | 合稿，核对英文、引用和格式 | 三人审定，队长当晚提交 |

[网页版分工表](https://szy0387-beep.github.io/mcm-agent-skills/#apmcm-plan) · [完整参赛计划与交接模板](docs/apmcm-2026.md)

## 常用资料

| 什么时候用 | 直接打开 |
| --- | --- |
| 开题、选题和三人分工 | [首赛实战手册](docs/team-playbook.md) · [赛题到论文路线图](figures/first-contest-mindmap.md) |
| 看本次日程、换人接手 | [亚太赛参赛计划](docs/apmcm-2026.md) · [CASE 交接模板](templates/CASE.md) |
| 找方法出处、写正文引用 | [参考文献指南](docs/references-guide.md) · [LaTeX 引用示例](examples/references/) |
| 调用 Codex、继续已有成果 | [可复制的分阶段指令](docs/codex-prompts.md) · [技能一览](#技能一览) |
| 先练一遍从题面到论文 | [英文题面](examples/dispatch/problem-en.md) · [完整练习与复跑命令](examples/dispatch/README.md) |
| 核对比赛要求和交稿 | [当届参赛规则](https://apmcm.org/detail/2513?language=cn) · [当届 AI 使用规定](https://m.saikr.com/contest/notice_detail/50212) |

[在网页首页展开查看资料要点](https://szy0387-beep.github.io/mcm-agent-skills/#resources)

## 快速开始

1. [下载完整 ZIP](https://github.com/szy0387-beep/mcm-agent-skills/archive/refs/heads/main.zip)并解压。用 Codex 打开包含本页和 `AGENTS.md` 的文件夹。**11 个核心 Skill 和 17 个专项 Skill 均已随包提供。**
2. 把题面和附件复制到该文件夹下的 `cases/我的题/inputs/`。已有代码、结果或论文时告诉 Codex 位置，方便从当前步骤接手。也可以在 Codex 中附上文件并说明它们对应哪一问。
3. 在这个项目的聊天里输入下面的一句。也可以点名 `$mcm-skill-router`。

> 这是我自己的练习题。题面和附件在 `cases/我的题/inputs/`。按新题流程帮我完成第一问，交付模型说明、复跑命令、结果表和验算证据。完成后我会用另外一组输入复核。

第一次拿到英文题，可以先说「用 `$mcm-problem-translate` 带我们读第一问。标出英文原文的位置，翻译约束，并列出输入、输出和本问要交什么」。找方法、数据出处或整理论文引用时，用 `$mcm-citation`。

已有模型、代码、结果表或论文时，可以从对应步骤继续。[可复制的 Codex 调用指令](docs/codex-prompts.md)

想自己推模型时，可以说「用 `$mcm-team-drill` 带我做第一问。每次给我一步，等我作答后再验算」。想先选方案时，可以说「我已有结果表，帮我推荐出图和写论文的技能组合」。[新题协作流程](.agents/skills/mcm-skill-router/references/new-problem.md)

### 我该准备什么

使用技能需要可用的 Codex。运行内置案例和 Python 解题代码还需要 Python 3.10 或更新版本。运行某个专项技能的示例时，按需安装它用到的 Python 库或求解器。生成论文源稿后，可用题目指定的本地编译器或 Overleaf 生成 PDF。

如希望在终端建立完整案例目录，在项目根目录运行 `python scripts/new_case.py team-q1`。它会建立 `inputs/`、`src/`、`outputs/`、`paper/` 和 `CASE.md`。组员各用自己的案例目录，附件与结果默认保存在本地。

### 验证安装

下面的合成案例只用 Python 标准库。从仓库根目录运行：

```sh
python .agents/skills/mcm-fast/scripts/dispatch.py examples/dispatch/units.csv examples/dispatch/demand.csv --output outputs/dispatch
```

输出总费用应为 **980**。还可以用同一例题从英文原题走一遍，得到可在 Overleaf 打开的英文稿。[从英文题到论文的完整短例](examples/dispatch/README.md)

## 技能一览

| Skill | 用途 |
| --- | --- |
| [mcm-skill-router](.agents/skills/mcm-skill-router/SKILL.md) | 推荐或执行当前最合适的流程 |
| [mcm-problem-translate](.agents/skills/mcm-problem-translate/SKILL.md) | 英文题逐问翻译、术语对照和中文任务表 |
| [mcm-model-training](.agents/skills/mcm-model-training/SKILL.md) | 审题、约束、假设、可验算基准 |
| [mcm-code-training](.agents/skills/mcm-code-training/SKILL.md) | 实现、复跑、求解状态和验错 |
| [mcm-simulation-training](.agents/skills/mcm-simulation-training/SKILL.md) | 过程仿真、情景和灵敏度 |
| [mcm-visualization-training](.agents/skills/mcm-visualization-training/SKILL.md) | 论文图、数据口径和视觉复核 |
| [mcm-paper-training](.agents/skills/mcm-paper-training/SKILL.md) | 竞赛论文源稿、Overleaf 和证据对照 |
| [mcm-citation](.agents/skills/mcm-citation/SKILL.md) | 找出处、插入正文引用、整理书目和终审 |
| [mcm-training-review](.agents/skills/mcm-training-review/SKILL.md) | 独立复算、单错反例、迁移与复盘 |
| [mcm-fast](.agents/skills/mcm-fast/SKILL.md) | 复跑本包的调度示例和可复用的月度预测脚本 |
| [mcm-team-drill](.agents/skills/mcm-team-drill/SKILL.md) | 个人陪练与三人队交接 |

## 随包专项技能

解压后可以直接点名专项 Skill，也可以让 `$mcm-skill-router` 按当前小问选择。专项设置为按需调用，适合在遇到具体方法或验收问题时使用。[17 个专项 Skill 的入口和用途](.agents/skills/mcm-skill-router/references/specialist-skills.md)

| 任务 | 可用 Skill |
| --- | --- |
| 拆题、看同类案例 | `$mcm`、`$math-modeling-solver` |
| 理解附件、预测和比较模型 | `$exploratory-data-analysis`、`$statsmodels`、`$scikit-learn` |
| 列优化模型、验算整数解、规划网络或权衡多目标 | `$problem-formulation`、`$mip-solver-and-solution-audit`、`$networkx`、`$pymoo` |
| 离散事件仿真、公式和单位验证 | `$simpy`、`$sympy`、`$uncertainty-and-units` |
| 画图、审图和共享可复跑笔记本 | `$matplotlib`、`$scientific-visualization`、`$jupyter-notebook` |
| 查写法、审查结论证据 | `$math-modeling-paper`、`$scientific-critical-thinking` |

维护者可用 `python scripts/install_extras.py --list` 查锁定版本和上游来源。[版本清单](third-party-skills.json)

在正式比赛中，按当届组委会规则确定 AI 使用范围、提交内容和披露要求。练习真题可从[亚太赛官网](https://www.apmcm.org/)等赛事站点获取。

## 许可证

本仓库自制内容采用 [MIT](LICENSE)。随包专项技能保留各自的上游许可证与版权说明。[第三方来源与许可证](THIRD_PARTY.md)
