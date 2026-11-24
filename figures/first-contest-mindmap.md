# 从赛题到可提交论文

拿到题面和附件后，从上往下走。每走完一格，就把该步产出的文件或记录交给队友，两次检查通过后再提交。返工支路标出了修完要重新执行的步骤。

第一步先在 `CASE.md` 给每问记下已知数据、要回答的问题和计划交付的结果。[小问交接模板](../templates/CASE.md)

参考文献从第 1–2 步就开始找。拆题记录数据来源，建模记录方法出处，第 5 步把引用放到正文用到它的地方，第 7 步对照原文和 PDF 核对。[参考文献怎么找、怎么用](../docs/references-guide.md)

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Microsoft YaHei, Noto Sans CJK SC, sans-serif","fontSize":"17px","background":"#ffffff","lineColor":"#49647C","primaryTextColor":"#182C40","edgeLabelBackground":"#ffffff"},"flowchart":{"curve":"linear","nodeSpacing":25,"rankSpacing":24,"padding":10,"wrappingWidth":320}}}%%
flowchart TB
    start(["拿到题面和附件"]) --> read["<b>1 拆成小问</b><br/>记下交付物、数据出处和单位"]
    read --> model["<b>2 建立基准模型</b><br/>写变量、目标、约束和手算预期<br/>记录方法出处"]
    model --> run["<b>3 跑通求解或仿真</b><br/>保存重跑命令、结果表和图"]
    run --> audit{{"<b>4 队友独立复算</b><br/>数据、约束和结果一致吗？"}}
    audit -->|需修正| fix["查数据、模型或程序<br/>修正后重跑并验算"]
    audit -->|通过| draft["<b>5 按小问写论文</b><br/>写答案、图表和局限，标注引用"]
    fix -.-> run
    draft --> pdf["<b>6 编译论文</b><br/>生成 PDF 并备齐当届附件"]
    pdf --> preflight{{"<b>7 队友审查最终版</b><br/>各问齐全，数字、引用、格式正确？"}}
    preflight -->|通过| finish(["<b>8 提交并核对回执</b><br/>交付论文 PDF 和附件"])
    preflight -->|需修正| revise["回对应小问补证据或改稿<br/>重新编译并检查"]
    revise -.-> draft

    classDef endpoint fill:#24405B,stroke:#24405B,color:#ffffff,stroke-width:2px;
    classDef stage fill:#EAF2FB,stroke:#5F7E9D,color:#172D43,stroke-width:1.4px;
    classDef gate fill:#E5F3EB,stroke:#52806A,color:#18392C,stroke-width:1.6px;
    classDef repair fill:#FFF0E1,stroke:#B77542,color:#623A24,stroke-width:1.3px;
    class start,finish endpoint;
    class read,model,run,draft,pdf stage;
    class audit,preflight gate;
    class fix,revise repair;
    linkStyle default stroke:#49647C,stroke-width:1.6px;
    linkStyle 4,6,10,11 stroke:#AA693E,stroke-width:1.5px;
```

## 卡在哪一步就用哪个 Skill

| 步骤 | 可以调用的入口 |
| --- | --- |
| 1–2 拆题和定基准 | [mcm-model-training](../.agents/skills/mcm-model-training/SKILL.md) |
| 3 求解或仿真、生成图 | [mcm-code-training](../.agents/skills/mcm-code-training/SKILL.md) · [mcm-simulation-training](../.agents/skills/mcm-simulation-training/SKILL.md) · [mcm-visualization-training](../.agents/skills/mcm-visualization-training/SKILL.md) |
| 4 和 7 验算或复核稿件 | [mcm-training-review](../.agents/skills/mcm-training-review/SKILL.md) |
| 5–6 写稿和编译 | [mcm-paper-training](../.agents/skills/mcm-paper-training/SKILL.md) |
| 8 核对文件与提交 | [首赛手册的交稿步骤](../docs/team-playbook.md#7-从干净目录复跑一次再提交) |

[首赛手册](../docs/team-playbook.md) · [Mermaid 源文件](first-contest-mindmap.mmd) · [图片版](first-contest-mindmap.png)
