# 数学建模项目协作

组员用自然语言提出数模需求时，先读取 [mcm-skill-router](.agents/skills/mcm-skill-router/SKILL.md)。用户带来自己的题面或附件并要求开题、解题或继续某一问时，按[新题协作流程](.agents/skills/mcm-skill-router/references/new-problem.md)接手。用户点名其他技能或指定教学方式时，按该要求执行。

已有 `cases/<题目名>/CASE.md` 时，从该记录接上当前小问。首次收到附件时，用 [CASE 模板](templates/CASE.md) 补齐记录。原始附件保留在 `inputs/`，程序、结果、论文源稿分别放在 `src/`、`outputs/`、`paper/`。
