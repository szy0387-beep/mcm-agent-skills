# 数学建模自主训练

用户要求开始或继续自主训练时，执行对应练习并留下可复用产物。先从项目训练记录确认最新完成和待验证的阶段。衔接已有工作时，从当前缺口推进。开新轮时选用户提供的往年题或[合成调度例题](../../../../examples/dispatch/README.md)，在独立输出目录保存产物。

| 阶段 | 主技能 | 交给下一阶段 |
| --- | --- | --- |
| 英文题理解 | [mcm-problem-translate](../../mcm-problem-translate/SKILL.md) | 需要翻译时，交逐问译文、任务表和原文位置 |
| 审题与建模 | [mcm-model-training](../../mcm-model-training/SKILL.md) | 题面出处、输入单位、模型、手算预期 |
| 代码与求解 | [mcm-code-training](../../mcm-code-training/SKILL.md) | 重跑命令、机器可读结果、独立检查 |
| 仿真与敏感性 | [mcm-simulation-training](../../mcm-simulation-training/SKILL.md) | 有仿真或灵敏度问题时，交情景、结果与适用范围 |
| 做图与审图 | [mcm-visualization-training](../../mcm-visualization-training/SKILL.md) | 可复现的图、数据来源和图注 |
| 生成训练论文 | [mcm-paper-training](../../mcm-paper-training/SKILL.md) | 稿件、导出文件、关键结论的证据位置 |
| 结果审查与复盘 | [mcm-training-review](../../mcm-training-review/SKILL.md) | 独立复算、反例、新输入、下一轮的改进点 |

需要找外部依据、插入书目或核查正文引用时，用 [mcm-citation](../../mcm-citation/SKILL.md)。

按需要读取一个主技能。每阶段核验交付物再继续。后续核验若发现上游有误，修复最早出错的环节，再重跑受影响的表、图和正文。外置数据、软件或账户缺失时，记录影响范围并完成可独立验收的部分。需要更换题目才能验证迁移时保留当前记录，复用接口与核验方法。

汇报保留实际复跑命令、核心指标、检查结果和产物路径。可复用实现先验证再接入 `$mcm-fast`。衡量技能开销时保留实际量测口径。个人陪练和三人合练由 `$mcm-team-drill` 接手。
