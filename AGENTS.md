# 数学建模项目协作

组员用自然语言提出数模需求时，先读取 [mcm-skill-router](.agents/skills/mcm-skill-router/SKILL.md)。用户带来题面或附件并要求开题、解题或继续某一问时，按[新题协作流程](.agents/skills/mcm-skill-router/references/new-problem.md)接手。点名专项技能时使用对应资料。整题阶段与交付证据统一记在 `CASE.md`。

已有 `cases/<题目名>/CASE.md` 时，从该记录接上当前小问。首次收到附件时，用 [CASE 模板](templates/CASE.md) 补齐记录。原始附件保留在 `inputs/`，程序、结果、论文源稿分别放在 `src/`、`outputs/`、`paper/`。

用户问进度时，只读 `CASE.md` 和关联证据。整题推进或交接时，按[分阶段流程](docs/competition-run.md)记录队伍决定、复核状态及下一步。上游改动后回查受影响的小问、图表及稿件位置。

禁止伪造、篡改数据、文献、实验记录和数值。证据不足时标记待核，仿真、估计和合成数据须如实标注。正式比赛先核对当届 AI 使用范围，据实保留记录，交稿前按 [ai-usage-disclosure](.agents/skills/ai-usage-disclosure/SKILL.md) 核对披露材料。
