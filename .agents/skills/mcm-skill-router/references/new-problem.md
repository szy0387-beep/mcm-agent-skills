# 用自己的题目开题

先找到用户指定的题面、附件和小问。已有 `CASE.md` 时，从其中记录的下一步接手。用户给的是练习题时，按其意愿选择陪练或直接完成所需环节。比赛期间按当届规则确定辅助范围与披露要求。

## 建立案例

从仓库根目录可运行 `python scripts/new_case.py <题目名>`。如果组员已建好 `cases/<题目名>/inputs/`，从已有附件入手，按需创建 `src/`、`outputs/`、`paper/`，并用 [CASE 模板](../../../../templates/CASE.md) 建立交接记录。用 `CASE.md` 记录题号、交付物和关键假设。若必要资料确实缺失，列出缺项，同时推进可独立完成的任务。

## 按小问推进

| 阶段 | 主技能 | 该阶段的验收 |
| --- | --- | --- |
| 审题与建模 | [mcm-model-training](../../mcm-model-training/SKILL.md) | 把题意写成输入、输出、约束与指标。选择一个简单基准，登记一个能手算的预期。 |
| 代码与求解 | [mcm-code-training](../../mcm-code-training/SKILL.md) | 从 `inputs/` 读原始数据，程序放 `src/`，结果放 `outputs/`。运行后记录工作目录、命令和依赖。 |
| 仿真与图表 | [mcm-simulation-training](../../mcm-simulation-training/SKILL.md) 或 [mcm-visualization-training](../../mcm-visualization-training/SKILL.md) | 按本问需要做情景实验或生成图。检查结果表、单位、基准和图中数字。 |
| 论文与结果审查 | [mcm-paper-training](../../mcm-paper-training/SKILL.md) 和 [mcm-training-review](../../mcm-training-review/SKILL.md) | 从已验算的结果写 `paper/`，独立复核关键数值、边界条件与结论。交付来源、重跑命令、产物路径及尚待验证的部分。 |

优先使用能运行和验算的现有工具。有实质性改善时再加复杂模型。需要某个专项技能时查[专项技能](specialist-skills.md)，把必须安装的 Python 依赖按实际采用的实现写进当前案例。编译条件未齐时先交源稿和可执行的编译步骤，标明 PDF 的验证状态。

每阶段更新 `CASE.md`。拆题和建模时登记数据、参数及方法的来源，写稿时把引用放到相应句子旁，交稿前由队友对照原文和最终 PDF。[参考文献指南](../../../../docs/references-guide.md)

结束时检查每个已做小问都交清答案、代码和证据，换输入后仍可从原始数据重跑。需要用对照试验确认验错能力时，加一个只造成单项失败的反例。
