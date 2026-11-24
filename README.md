# Math Modeling Agent Skills

面向数模小组的 Codex 技能。组员可以用自己的题面和附件开题，从拆解小问、建模和求解走到出图、论文与结果复核。也可以按个人陪练或 AI 自主训练的方式使用。

## 快速开始

1. 在 GitHub 选 **Code → Download ZIP** 并解压。用 Codex 打开包含本页和 `AGENTS.md` 的文件夹。9 个核心 Skill 随仓库一起提供。
2. 把题面和附件复制到该文件夹下的 `cases/我的题/inputs/`。已有代码、结果或论文时告诉 Codex 位置，方便从当前步骤接手。也可以在 Codex 中附上文件并说明它们对应哪一问。
3. 在这个项目的聊天里输入下面的一句。也可以点名 `$mcm-skill-router`。

> 这是我自己的练习题。题面和附件在 `cases/我的题/inputs/`。按新题流程帮我完成第一问，交付模型说明、复跑命令、结果表和验算证据。完成后我会用另外一组输入复核。

想自己推模型时，可以说「用 `$mcm-team-drill` 带我做第一问。每次给我一步，等我作答后再验算」。想先选方案时，可以说「我已有结果表，帮我推荐出图和写论文的技能组合」。[新题协作流程](.agents/skills/mcm-skill-router/references/new-problem.md)

### 我该准备什么

使用核心技能需要可用的 Codex。运行内置案例和 Python 解题代码还需要 Python 3.10 或更新版本。可选专项和第三方 Python 包按你的题目安装。生成论文源稿后，可用题目指定的本地编译器或 Overleaf 生成 PDF。

如希望在终端建立完整案例目录，在项目根目录运行 `python scripts/new_case.py team-q1`。它会建立 `inputs/`、`src/`、`outputs/`、`paper/` 和 `CASE.md`。组员各用自己的案例目录，附件与结果默认保存在本地。

### 验证安装

下面的合成案例只用 Python 标准库。从仓库根目录运行：

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
