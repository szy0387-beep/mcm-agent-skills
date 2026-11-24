# 数学建模论文怎么找和用参考文献

拿到题后，先在每个小问里标出**需要外部依据的句子**。可能是一个背景事实、一列外部数据、一个参数、某种模型或一种检验方法。明确要支持的内容，再去找能给出直接证据的来源。

可以在 Codex 里说「用 `$mcm-citation` 帮我核对第一问的方法出处，为已验证的来源写 BibTeX，并指出应放在哪一句旁边」。[引用 Skill](../.agents/skills/mcm-citation/SKILL.md)

## 在论文哪里引用

| 你用了什么 | 正文放哪里 | 记录到什么程度 |
| --- | --- | --- |
| 背景事实、行业规范、公开统计结论 | 引言或对应小问的背景句 | 发布机构或作者、年份、对应的条款或数据指标 |
| 赛题附件、外部数据集、别人制作的图表 | 数据准备、对应图注或表注 | 文件名与表号，或发布者、数据集名、版本、覆盖范围、单位和实际取数位置。图表改绘时说明来源及改动。 |
| 外部给出的参数、假设依据 | 假设与依据，紧跟参数或假设 | 数值、单位、适用范围和页码。队伍自己设定的情景写清设定理由和检验方式。 |
| 借用的模型、算法、指标或验证办法 | 模型、求解或检验部分，放在首次实质使用处 | 原论文、可靠教材或技术文档的具体章节、公式或 API。说明你们在这道题上怎样使用。 |
| 队伍自己算出的数值、图和结论 | 结果、图表和结论 | 指向自己的公式、实验、图号或表格行列。例如「见表 3」属于交叉引用。若计算用到了外部数据或方法，在相应位置引用它们。 |

正文先引，文末 **References** 汇总实际引用的条目。赛题附件按当届模板标明来源。有单独格式时，以赛事规定为准。

## 去哪里找

| 缺什么 | 从哪里开始 | 用什么作最终出处 |
| --- | --- | --- |
| 题面、提交要求、赛题附件 | 当届赛事页和题目附件 | 组委会的公告、下载页或原始题面，写到具体问题、表或条款。[亚太赛官网](https://www.apmcm.org/) |
| 方法和同类应用 | 用英文关键词在 Google Scholar 搜，或用学校图书馆的知网入口找中文文献 | 首选可核对的原论文、出版方页面或可靠教材。已有 DOI 时用 Crossref / DOI 链接核对元数据。[Google Scholar](https://scholar.google.com/) · [中国知网](https://www.cnki.net/) · [Crossref](https://search.crossref.org/) · [DOI](https://doi.org/) |
| 公开数据 | 按地区、指标、时间粒度查官方数据门户 | 引具体数据集或指标页，保留单位、下载日期或版本。核对该题是否允许自行补充外部数据。[国家统计局国家数据](https://data.stats.gov.cn/) · [世界银行开放数据](https://data.worldbank.org/) |
| 软件接口、求解器参数 | 查对应库的官方文档，按实际版本和函数名检索 | 引实际使用的版本和接口。方法依据和软件实现可以分别引用。[SciPy `milp` 文档](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html) |

试着用“问题对象 + 方法或验证词”组合检索，例如 `unit commitment mixed integer programming`、`load forecasting rolling origin cross validation`。找到候选后，打开原文查看支撑那句话的段落、公式或表格，再核对作者、标题、年份、版本、DOI 或链接。若目前只能看到摘要或搜索片段，就把正文才有的细节留待核实。

## 三人怎么交接

1. **拆题时**，建模手写哪条假设或方法需要来源，编程手标出要从哪里取原始数据，论文手在 `CASE.md` 建一行记录。[案例模板](../templates/CASE.md)
2. **建模和求解时**，找到来源的人在记录里补上具体页、章节或表号，以及它支持的说法。练习时可以让 AI 推荐关键词和候选来源，由队员打开原文核实后再采用。比赛中按当届规则使用 AI。
3. **写作时**，论文手把来源放在使用它的句子旁，维护 Word 的来源列表或 LaTeX 的 `references.bib`。从正文回查文末条目，再从文末检查有无未实际引用的文献。
4. **交稿前**，另一位队友打开最终 PDF 和原出处，确认编号和条目一致、来源真实可查、原文确实支持对应说法。需要改变数字、方法或结论时，回对应小问修正，再重新编译。

## 跑一遍正文和 BibTeX

示例把引用放在 **Validation**，紧跟“用滚动起点验证，训练集只用预测起点之前的观测”这句话。来源是 Hyndman 与 Athanasopoulos 的《Forecasting: Principles and Practice》第三版 §5.10。引用支持验证设计，你们的模型误差仍由自己的实验结果给出。[方法原文](https://otexts.com/fpp3/toolbox.html#time-series-cross-validation) · [作者给出的引用格式](https://otexts.com/fpp3/preface.html)

把 [main.tex](../examples/references/main.tex) 和 [references.bib](../examples/references/references.bib) 放进同一个 Overleaf 项目，选择 `main.tex` 为主文件并编译。正文的 `\cite{...}` 会生成编号，文末会自动列出条目。向已有模板接入时，沿用模板原来的 BibTeX 或 `biblatex` 设置。[Overleaf BibTeX 指南](https://www.overleaf.com/learn/latex/Bibliography_management_with_bibtex)

用 Word 时，在“引用”菜单插入来源和书目，选择赛事要求的格式。交稿前打开导出的 PDF 检查实际编号与条目。
