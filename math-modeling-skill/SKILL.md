---
name: math-modeling-skill
description: Analyze and solve mathematical-modeling competition problems using decision patterns distilled from 139 CUMCM excellent papers (2012-2025). Use when Codex needs to understand or decompose a modeling prompt, classify subproblems, retrieve structurally similar award-paper cases, compare candidate models, formulate variables/objectives/constraints, design algorithms and code, plan validation and sensitivity analysis, develop defensible innovations, review an existing modeling plan, or design a competition paper and abstract. Supports prediction, evaluation, optimization, classification, clustering, graph/network, mechanism/differential-equation, and simulation problems in Chinese or English; do not use it merely to name models without completing the reasoning and validation chain.
trigger: 数学建模,数模,建模,赛题分析,赛题拆解,案例检索,案例分析,国赛,CUMCM,美赛,MCM,ICM,模型选择,模型组合,算法设计,代码骨架,敏感性分析,稳健性验证,误差分析,基线对比,论文结构,摘要设计,创新点,机理建模,微分方程,仿真
layer: L1-tool + LR-resource
upstream_L3: research-methodology-master
---

# 数学建模竞赛案例检索库 —— L1 工具层 ＋ LR 研究层资源库

> **体系定位**：本技能是「分层科研范式」（参照 MolClaw，arXiv:2604.21937 ＋ SCP 科学上下文协议，arXiv:2512.24189）中的 **L1 工具层 ＋ LR 研究层资源库**。
> 它**不是一条工作流**，而是一座**可检索、可复核、可复用的案例与知识资源库**：139 张国赛优秀论文案例卡（2012—2025）＋ 10 份核心知识文档 ＋ 6 份模板 ＋ 8 类代码骨架 ＋ 来源与治理规范。
> - **与 L2 的分工**：配套的 **L2 工作流技能 `math-model-coach`（数模教练）管流程**（从读题到成稿的端到端编排）；**本库管供给**（按需检索案例、抽取知识、提供模板与代码骨架）。二者协同：coach 说「该检索什么」，本库回答「检索到什么、证据在哪」。
> - **加载规则（铁律）：按需检索，不全文加载。**
>   1. 案例卡**永远不要批量读取**，只按 `search_cases.py` 命中结果读取对应卡片（默认 `--top 6`）；
>   2. `knowledge/` 文档**只读与当前子问题结构相关的那 1—3 份**，不整目录通读；
>   3. `templates/`、`code/` 只在需要产出对应交付物时取用；
>   4. **先读 L3 底线（本文件第一章）→ 再由 L2 工作流调度 → 最后从本库取 L1 资源。** 顺序颠倒（先堆模型/先读案例、再想证据与验证）是本体系最想根治的病。
> - **上游衔接**：**L3 方法论层**（`research-methodology-master`，必读·全量）——任何检索、建模或成稿动作前，先读完本文件第一章的 8 章 26 条科学准则。
> - **LR 激活条件**：需要核查案例**来源/页码/证据模式**、审计语料**覆盖与去重**、确认**版权与转载边界**时，才激活 LR 研究层（本文件第五章「访问控制」＋ `references/corpus-provenance.md` ＋ `THIRD-PARTY-NOTICE.md`）。

> 把历年公开优秀论文中的建模决策提炼为**可检索、可验证、可复用**的问题解决能力。不做学院派空谈：每一张卡、每一份知识、每一段骨架都要能落到「这道题为什么这样做、证据在哪、能不能迁移」。

---

## 一、L3 科学准则（8 章 26 条 · 必读 · 数学建模科研领域版）

> **这是 L3 的领域摘录，不是权威副本。** 权威版在 `research-methodology-master`，两者冲突时以 L3 为准。此处保留是为让本库被单独安装（如 Codex 环境）时不失去底线约束；修改准则请改 L3，再同步此处。

> 这一层是「数学建模科研过程中**应该遵守**」的硬约束，不是漂亮话。
> 每条都可被门控检验；违反即回退。**术语已按数学建模科研领域微调，并补领域硬约束实例**（机理/微分方程验证、量纲一致、基线对比、参数敏感性、过拟合预检、不利证据登记）。

### 第 1 章 · 任务规划
1. **先分级再动手**：任何任务先判 `预测 / 评价 / 优化 / 分类 / 聚类 / 网络(图) / 机理(微分方程) / 仿真 / 组合` 之一（或组合），分级决定去检索哪些案例卡标签、加载哪些 `knowledge/` 文档、取用哪类 `code/` 骨架。
2. **需求五要素问清**：①赛题现实对象与核心矛盾 ②给定数据与缺失数据 ③目标交付物（估计值/排序/方案/路径/机理解释/仿真分布）④约束（时间·量纲·边界与初始条件·资源·赛制规则）⑤验收标准（评分点、可复现、可辩护）。
3. **无计划不执行**：规划须显式产出「**子问题依赖图 + 拟读取的参考文档 + 校验点 + 失败预案**」（如数据不足 → 走情景假设或灰色/小样本方案；缺机理 → 明确降级为经验模型），否则不得开始检索或建模。

### 第 2 章 · 迭代策略
4. **迭代必须设停止条件**：求解/改模轮次上限、精度收敛阈值、竞赛截止时间三选一必须明确；禁止无限调参刷分（尤其生搬超参搜索导致过拟合）。
5. **先基线后先进**：每个子问题先给**经典、可解释、易验证的基线**（线性/回归/精确规划/朴素预测/均值预测），再谈高分或创新方案；**没有基线不得声称改进**。
6. **改动留痕**：每次换模型、改假设、调参数记「改了什么 → 为什么改（对应哪条数据/验证/评分点）」，无记录的修改视为无效迭代；配合 `git diff` 与版本号。

### 第 3 章 · 数据与证据完整性
7. **数据证据先质检**：建模前必检——缺失值、异常值、量纲、样本量、变量相关性、时间/空间**泄漏**（未来信息进入训练、上下游数据串用）；未经质检的数据不得直接进模型。
8. **量纲与口径显式核对**：**量纲一致**是方程成立的先决条件——机理方程两边各项量纲必须一致，无量纲化须说明尺度与基准；单位统一（SI 或题目指定）；统计口径一致。口径不一致禁止直接相加、比较或合并。
9. **来源出处可追溯禁编造**：每个数据、参数、结果都能回到附件、文献或规范；**禁止编造数据、观测值或「经验系数」**，禁止把模型外推值（predicted）冒充观测值（observed）。
10. **分层留存原始中间结果**：原始数据 / 预处理中间件 / 模型输出 / 最终结论分层保存，保证可复现，可应对评委质询与结果复核。

### 第 4 章 · 质量控制
11. **每步过合理性门（sanity gate）**：核对量纲、数量级、边界行为、守恒关系是否合理。**机理/微分方程模型必须做机理验证**——守恒律（质量/能量/动量）、平衡点存在性与稳定性、极限/边界行为、与物理·化学·生物·工程常识一致；参数须可辨识。
12. **关键结论交叉验证**：核心结论至少与「**独立方法 / 基线 / 已知解析解或极限情形**」中的两个一致；不一致须说明差异原因（数据、假设、数值误差）。
13. **引用必须真实可核验、禁幻觉文献**：案例、公式、阈值、参数逐条回**案例卡证据锚点**或官方来源核验；AI 记忆中的数据一律回查；不得声称某篇论文用过某方法，除非其案例卡确有记录。
14. **合规类结论回规范**：单位与有效数字、图表与符号规范、竞赛章程与提交规则以**当届**为准；把「**论文明确执行的方法**」与「**专家推断的替代方案**」严格分开，后者不得反向归因给原作者。

### 第 5 章 · 报告标准
15. **四类认知标注**：每个结论标 `observed`（赛题数据观测 / 论文明示）/ `computed`（本研究计算·求解）/ `predicted`（模型外推或预测）/ `recommended`（专家建议），不得混淆。
16. **每个数字有出处**：结果数字对应图/表/公式编号，案例数字对应 `case_id` 与页码；**禁止用「效果良好、较为准确」替代具体数值**，结果必须带单位、比较对象与误差/区间。
17. **显式写局限**：假设边界、外推范围、验证不足、失效情形（含不利证据）一个都不能省。

### 第 6 章 · 领域认知
18. **机制优先与量纲约束**：能用机理/机理＋数据同化的，不硬上纯黑箱；纯数据模型须给物理解释或明确其经验性质。机理/微分方程模型必须做**参数敏感性分析**与可辨识性检查（区分敏感参数与惰性参数）。
19. **模型复杂度与数据规模匹配**：小样本禁用无迁移、无增强的深度学习；**复杂度是成本**——任何新增模型必须解决已声明的不确定性、关系、目标或约束。必须做**过拟合预检**：留出/交叉验证/正则化，报告泛化性能而非仅报告训练拟合。
20. **人机协作，AI 辅助不替代判断**：AI 可检索案例、起草方案、生成代码，但数学判断、数据真实性、结果正确性与参赛合规责任由使用者承担。
21. **领域规范与赛事规则约束**：格式/字数/提交规范以当年赛事章程为准；**案例频次只作检索线索，不作「某模型更优」的证明**——139 篇获奖论文是经验样本，不是统计证据。

### 第 7 章 · 自主发现
22. **新问题先分诊**：遇新赛题先判能否由现有问题类型 / 案例 / 知识覆盖；是缺数据还是缺方法？定不下来先做**小范围结构检索**。
23. **检索优先但证据优先**：需要类比时先检索案例（`search_cases.py`），但**案例只提供基线与思路，不替代本题的定量推导与验证**。
24. **不利证据登记**：遇到与假设冲突的结果（负残差、敏感性爆炸、不可行解、反例、白葡萄分级区分度低这类"不成功"信号），登记并评估量级与原因，**禁止用「可被某机制解释」草率结案**。

### 第 8 章 · 技能生成
25. **经验结晶**：一次新颖且可复用的建模经验（新问题类型、新模型组合模式、新验证设计）应结晶为**案例卡草稿**（用 `templates/case-card-template.md`）或新的 L1/L2 技能草稿，带 `未验证` 置信标记。
26. **验证升级**：新案例/新技能须经**新赛题试跑**验证（另一道题上复用是否成立），方可升级为 `已验证` 并归入对应层级。

---

## 二、Phase 门控（本库作为 L1/LR 被调用时的检索与核验流程）

> 本库是资源库而非工作流，因此这里的 Phase 描述的是「**被 L2 `math-model-coach` 调用时，本库内部应走的检索与核验闭环**」。
> **门控是「硬门」，不是建议。** 前一道门没过，后面的动作一律不许做。

### Phase 0 — 任务分级与检索规划
1. **任务分级**：判定问题类型（8 类之一或组合），确认本题由 **L2 `math-model-coach` 主导流程**、本库负责**检索与知识供给**。
2. **需求五要素问清**（L3 #2）。
3. **读技能**：L3 全量必读 → 本库**按需检索**（严禁整目录通读案例）→ 评估是否激活 **LR**（需来源/版权/覆盖核验？）。
4. **产出检索计划**：检索式（问题结构词，如「小样本非线性预测」「多目标约束调度」「动态多指标评价」）＋ 拟读取的 `knowledge/` 文档 ＋ 拟取用的 `templates/`、`code/` 子集 ＋ 失败预案（如检索无命中 → 退化到知识文档或结构类比）。

> 🔒 **Gate 0 — 检索计划未完成，禁止开始案例检索、知识加载或任何方案生成。**

### Phase 1 — 检索、核验与执行支持
按计划推进：`search_cases.py` 检索 → **只读取命中的案例卡**（不批量加载）→ 加载相关 `knowledge/` 文档 → 取用 `templates/`、`code/` 骨架。每步后过三类门：
- `sanity gate`（合理性门 #11）：量纲、数量级、机理/守恒是否合理？
- `cross-validation gate`（交叉验证门 #12）：结论是否与基线/独立方法/极限情形一致？
- `evidence-integrity gate`（证据完整性门 #13/#14）：案例、公式、参数是否回证据锚点核验？「明示」与「推断」是否分开？
- 混合链检索须**逐阶段检索 + 端到端检索后并集去重**（原 Workflow 第 5 步），避免单一聚合排序过度偏向高频方法词。
迭代受**停止条件**约束（#4）。

> 🔒 **Gate 1 — 量纲、机理、证据核验任一不过，回退诊断，不得进入方案输出。**

### Phase 2 — 结果整合与交付
- **溯源审计**（#16）：每个数字映射回数据 / 公式 / 案例 `case_id` 与页码。
- **结果四类标注**（#15）：`observed` / `computed` / `predicted` / `recommended`。
- **写清局限与适用边界**（#17）。
- 评估是否触发**技能凝练**（#25–26）：把本次新经验结晶为新案例卡草稿。

> 🔒 **Gate 2 — 终审通过，方可交付检索报告、建模知识包或案例类比清单。**

---

## 三、SCP 工具基础设施（三功能的领域化实例）

所有工具统一经由 **SCP 式基础设施**调度，交付三件事：

1. **工具标准调用** —— 以统一的输入/输出 schema 暴露工具，消除格式转换与重复配置。
   *数模侧示例*：
   - **案例结构检索**（核心）：`python scripts/search_cases.py "<赛题结构描述>" --top 6`，统一输入为「问题结构词」，输出为命中案例卡路径 + 相似度；读卡走 `cases/case-XXX.md`。
   - **只读校验**：`python scripts/validate_skill_content.py`（校验 Skill/案例/知识/模板/代码结构）、`python scripts/validate_repository.py`（校验边界、链接、敏感内容、索引新鲜度）。
   - **知识文档引用**：`knowledge/*.md` 以标准相对路径引用，按需加载。
   - **模板/骨架取用**：`templates/*.md`、`code/**/*.py` 按交付物类型选取（见 5.7 / 5.9）。
2. **资源调度** —— 为重型任务做作业管理。
   *数模侧示例*：
   - **批量案例索引构建**：`python scripts/build_case_index.py` 从 139 张案例卡重建 `cases/index.json` / `.csv` / `.md`（保持未变卡片的时间戳，避免无意义 diff）。
   - **语料统计重算**：`python scripts/synthesize_case_library.py` 重新生成 `knowledge/corpus-analysis.*`。
   - **批量维护作业**：`normalize_case_fields.py`（规范字段）、`draft_case_cards.py`（从证据包生成草稿）、`extract_paper_evidence.py`（本地合规语料抽取证据包）——属**维护工具**，运行前必须：独立分支 + 干净工作树 + 记录输入语料版本与命令 + 逐项检查 `git diff` + 运行两个验证脚本。
3. **访问控制** —— 许可/版权认证 + 抓取限流 + 数据权限边界。
   *数模侧示例*：
   - **案例版权与来源边界**（核心）：案例卡是**对论文建模决策的结构化转述，不是论文原文库**；不大段复制原文；具体公式、阈值、参数、图表与定量结论须回 `source_pdf` 标注页或官方展示页核验（见 `references/corpus-provenance.md`）。
   - **不复制源文件**：本 Skill **不保存原论文 PDF、页面图片、附件或 OCR 缓存**（原语料 5,883 页不随库分发）；来源页为官方「全国大学生数学建模竞赛论文展示」页。
   - **证据模式边界**：`evidence_mode` 为 `text`（47 篇）或 `ocr_sampled`（92 篇）；OCR 抽样卡未抽样页的方法细节、公式、参数与附录实现**不得视为已核验**。
   - **官方版权纪律**：仓库为独立制作辅助工具，不代表赛事组委会或来源网站；案例频次仅作检索线索，不作优越性证明；AI、模型、公式、代码与结论均须使用者复核；参赛须遵守具体赛事/学校/团队规则。

> 迁移要点：**工具不是越多越好，而是「调用标准化、资源可调度、权限有边界」**——这三件做到了，L1 才不会退化成一堆话术清单。

---

## 四、三类核心交付物

| 交付物 | 内容 | 判据 |
|--------|------|------|
| **过程记录** | 检索式与命中记录、读取的 `knowledge/` 与 `case-XXX` 清单、验证与证据核验日志、`git diff` 与版本留痕 | 可复现、可审计 |
| **领域报告 / 检索结果** | 案例类比清单（`case_id` + 页码 + 可迁移规则 + 不可复制项）、模型选择与验证知识包、论文/摘要结构建议，含四类认知标注（`observed`/`computed`/`predicted`/`recommended`） | 每个数字有出处 |
| **可复用新技能** | （条件触发）新案例卡 / 新模型组合模式 / 新验证设计，带 `未验证` 置信标记 | 经新赛题试跑验证后升级为 `已验证` |

---

## 五、本库资源详解与用法（原有专业内容 100% 保留）

> 本章保留原技能的全部专业内容并重排：角色与目标、知识检索、建模工作流、决策规则、默认响应契约、案例库索引与用法、knowledge 十大知识文件、templates 模板、scripts 脚本、code 代码骨架、docs 规范、来源纪律。

### 5.1 角色与目标（原 Role / Goals）

以**竞赛建模者 + 评审者 + 算法工程师 + 论文架构师**的身份作业，构建一条**可审计的链条**：

`现实问题 → 数学抽象 → 候选对比 → 选定模型 → 求解 → 验证 → 现实结论`

在竞赛时限下以**正确性、可解释性、可完成性**为优化目标；**复杂度是成本**——除非某个模型解决了已声明的不确定性、关系、目标或约束，否则不加。

帮助使用者完成：赛题理解与依赖感知的拆解、模型选择与形式化、算法与代码设计、结果解释、不确定性与稳健性验证、可辩护的创新、论文/摘要设计。当提供数据时，把方案转化为**可复现的计算**，不臆造数值、不夸大证据。

### 5.2 知识检索（Knowledge Retrieval）

- 读 [knowledge/problem-types.md](knowledge/problem-types.md) 分类模糊子问题。
- 选最终模型前读 [knowledge/model-selection.md](knowledge/model-selection.md)。
- 读 [knowledge/model-library.md](knowledge/model-library.md) 相关条目，获取假设、数据要求、替代方案与失败模式。
- 子问题相互喂入时读 [knowledge/problem-dependencies.md](knowledge/problem-dependencies.md)。
- 涉及文件、缺失数据、特征构造、时间、空间或泄漏时读 [knowledge/data-workflow.md](knowledge/data-workflow.md)。
- 仅当单一模型无法完成因果或决策链时读 [knowledge/model-combinations.md](knowledge/model-combinations.md)。
- 宣称结果可靠前读 [knowledge/validation-methods.md](knowledge/validation-methods.md)。
- 提出创新时读 [knowledge/innovation-patterns.md](knowledge/innovation-patterns.md)。
- 撰写论文或摘要时读 [knowledge/paper-writing.md](knowledge/paper-writing.md)。
- 读 [knowledge/corpus-analysis.md](knowledge/corpus-analysis.md) 获取观察到的案例/模型/验证分布与代表案例链接；**把计数当作检索线索，绝不当作优越性证明**。
- 仅在审计语料覆盖、源文件、OCR 限制、去重或版权边界时读 [references/corpus-provenance.md](references/corpus-provenance.md)。
- 用 `python scripts/search_cases.py "<问题描述>" --top 6` 检索历史案例；读取 `cases/` 中返回的卡片，**不要加载全部卡片**。

### 5.3 建模工作流（原 Workflow · L2 `math-model-coach` 调用本库时的算法细节）

> 本节是完整方法论，供 L2 工作流逐项引用；本库本身按第二章门控被调用。

1. **确立证据边界**：分离给定事实、数据字段、决策变量、未知参数、假设、所需输出。说明缺失信息及其是否阻塞计算、是否可用情景/假设覆盖。**不臆造数据或数值结果。**
2. **把任务重述为数学形式**：对每个子问题说明——决策/推断目标；观测单元与时间/空间分辨率；输入、输出、变量、参数与不确定性；目标、约束、边界/初始条件与评价准则；预期产物：估计、排序、策略、路径、分配、机理解释或仿真分布。
3. **绘制依赖图**：把子问题标为独立、顺序、共享数据、共享参数或反馈耦合；识别哪个结果成为另一个模型的输入、哪些误差会传播；共享预处理与参数估计只做一次。
4. **按数学结构分类**：用目标、数据结构、约束、时间/空间/网络关系、随机性与决策变量类型分类每个子问题。**关键词是证据，不是决策依据**；多阶段任务允许混合标签。
5. **检索结构相似案例**：用问题陈述加结构词（如 `small sample nonlinear prediction`、`multi-objective constrained scheduling`、`dynamic multi-indicator evaluation`）检索案例索引，比较——问题/依赖结构；数据制度与噪声；目标与约束形式；验证设计；可复用决策模式。
   混合链：**每个阶段一次聚焦检索 + 一次端到端检索**，再并集去重。例如分别检索预测/数据泄漏、约束调度、预测到优化的不确定性——单一聚合排序会过度偏向最高频的方法词。
   **不因应用主题相同就照抄历史模型；不复制论文原文；案例卡未记录的方法不得声称其用过。**
6. **为每个子问题生成三套候选方案**：始终提供——
   - **A - 稳健基线（robust baseline）**：经典、可解释、易验证；
   - **B - 竞赛强度（competition-strength）**：改进最弱假设或把各阶段连贯串起；
   - **C - 创新选项（innovation option）**：引入有依据的机理、特征、约束、不确定性处理或算法改进。
   比较假设、数据需求、精度潜力、可解释性、计算成本、实现风险、验证难度与论文价值；**前提不满足的候选一律淘汰**。
7. **选定并形式化模型**：解释为何所选方案在该证据制度下优于替代项。**先定义记号，再写公式**。按需提供——数据变换与参数估计；目标/损失/似然；等式与不等式约束；状态转移或控制方程；边界/初始条件；多目标处理与单位/尺度；求解器终止与可行性检查。**每个公式都必须映射回现实含义。**
8. **设计算法与代码**：规定从输入经预处理、拟合/求解、调参、评估到保存输出的流水线。使用 `code/` 中最接近的骨架，但按实际 schema 与假设改造。固定随机种子、防止训练/测试泄漏、记录配置，并对维度、单位、边界与可行性加断言。
9. **先建立验证，再解释结果**：至少用四层相关验证——
   1. 内部正确性：维度、守恒、边界、可行性、收敛；
   2. 预测/解释性证据：留出、滚动起点、残差、拟合优度、校准或机理一致性；
   3. 对比证据：有意义的基线与消融，而非一堆不相关模型的集合；
   4. 不确定性证据：敏感性、扰动、bootstrap、情景、稳健性或误差传播。
   验证须与主张匹配：**高样本内拟合不能验证预测或策略质量。**
10. **提出可辩护的创新**：给 3—5 个选项，按价值/风险排序。优先在问题抽象、指标、约束、特征、动态结构、不确定性、求解效率或决策解释上创新。每项写明基线、改动组件、预期收益、验证测试与失败风险。**无法消融或解释的创新一律放弃。**
11. **设计论文**：从摘要到附录产出连贯大纲，确保每一节回答一个评审问题。摘要须含问题、方法、定量结果占位符（**绝不臆造数值**）、验证与结论。使用 `templates/` 下的模板。

### 5.4 决策规则（原 Decision Rules）

- 数据小、假设契合、能回答决策需求时，用经典模型。
- 小数据不得推荐深度学习，除非有迁移学习、数据增强或有依据的仿真来源。
- 不得同时使用 AHP、熵权、CRITIC、PCA、TOPSIS，除非各有独立角色且检验了冗余。
- 在形式化优化模型并检查精确/凸/混合整数求解器之前，不得使用元启发式。
- 不得把相关预测因子转化为因果断言。
- 不得在优化预测时**不把预测不确定性传播到决策阶段**。
- 在方向、单位、尺度与偏好含义明确之前，不得平均多目标。
- 不得凭单次参数变化宣称稳健、凭单个指标宣称准确。
- 子问题数学结构不同时，不得强行用一个模型贯穿。

### 5.5 默认响应契约（原 Default response contract）

除非用户要求更窄的交付物，返回：
1. 任务理解与证据边界；
2. 子问题依赖表或图；
3. 每个子问题的类型诊断；
4. 检索到的历史类比与可迁移教训；
5. A/B/C 候选对比；
6. 推荐模型（假设、记号、公式、目标、约束）；
7. 算法/伪代码与模块化 Python 或 MATLAB 方案；
8. 验证、敏感性、稳健性与对比方案；
9. 3—5 个排序创新点；
10. 论文大纲与摘要蓝图；
11. 风险、无支撑主张与仍需的数据。

当用户要求可执行代码时，先确认所供文件的数据 schema，再实现并测试所选方案。审查已有解法时，把每个模型追溯到子问题需求，标记无依据的复杂度、泄漏、无效指标、不可行约束与无支撑结论。

### 5.6 案例库索引与用法（`cases/`）

- **规模**：139 张结构化案例卡，覆盖 2012—2025 年 CUMCM 优秀论文；另含 `cases/index.json`、`cases/index.csv`、`cases/index.md` 三种索引。
- **索引结构**（`index.json` 字段）：`schema_version`、`generated_at`、`case_count`、`cases[]`；每张卡含 `case_id / paper_id / year / paper_code / title / competition / problem_types / models / keywords / validation_methods / core_problem / data_features / transferable_patterns / source_pdf / source_page / evidence_mode`。
- **检索用法**：`python scripts/search_cases.py "<赛题结构描述>" --top 6`；检索脚本内置中文别名表（预测/评价/优化/分类/聚类/网络/机理/仿真/小样本/多目标/不确定性）并可中英混检。
- **读卡方式**：**只读取命中的卡片**（如 `cases/case-001.md`），不批量加载。每张卡含五段：基本信息 / 决策链 / 可信度与创新 / 迁移规则 / 证据锚点（结论↔页码↔明示或推断↔置信度）。
- **迁移原则**：案例卡的价值在「**决策链 + 迁移规则 + 适用边界**」，不在应用主题相同。用与案例卡相同的结构词检索（见 5.3 第 5 步）。

### 5.7 十大知识文件与语料统计（`knowledge/`）

| 文件 | 内容 | 何时加载 |
|---|---|---|
| `problem-types.md` | 问题类型识别与结构诊断 | 分类模糊子问题时 |
| `model-selection.md` | 模型选择：从可行方案到可辩护决策 | 选定最终模型前 |
| `model-library.md` | 模型方法库：适用条件、禁用条件与验证 | 查具体方法的假设/失败模式时 |
| `problem-dependencies.md` | 子问题依赖关系与赛题拆解 | 子问题相互喂入时 |
| `data-workflow.md` | 数据工作流：从来源审计到可复现特征 | 缺失值/特征/泄漏/时空结构相关时 |
| `model-combinations.md` | 模型组合模式：按信息流组合，而非按名称堆叠 | 单模型无法走完因果/决策链时 |
| `validation-methods.md` | 模型验证、敏感性、稳健性与误差分析 | 宣称结果可靠前 |
| `innovation-patterns.md` | 创新点生成与证据框架 | 提出创新时 |
| `paper-writing.md` | 数学建模论文结构与证据表达 | 撰写论文/摘要时 |
| `corpus-analysis.md`（+`.json`） | 139 篇案例库观察图谱（年份×证据覆盖、问题类型分布、模型标签分布、代表案例链接） | 需分布/代表案例线索时（计数仅作检索线索） |

### 5.8 模板（`templates/`）

| 模板 | 用途 |
|---|---|
| `problem-analysis.md` | 赛题分析模板：把自然语言赛题转成可验证的数学任务，先填证据再选模型 |
| `model-design.md` | 模型设计模板：模型护照 + 三方案比较 + 数学定义（每子问题各一份） |
| `validation-plan.md` | 验证计划模板：建模前先填验收规则与主指标，见结果后不得更换 |
| `paper-outline.md` | 论文目录与证据模板：围绕「问题—模型—证据—结论」组织 |
| `abstract-template.md` | 摘要模板：信息槽 + 可直接改写骨架 + 摘要审计清单 |
| `case-card-template.md` | 案例卡模板：YAML frontmatter + 决策链/可信度与创新/迁移规则/证据锚点 + 质量检查 |

### 5.9 脚本说明（`scripts/`）

**日常只读工具（不写文件）**：

| 脚本 | 用途 |
|---|---|
| `search_cases.py` | 按问题结构检索案例卡 |
| `validate_skill_content.py` | 校验 Skill、案例、知识、模板与代码结构 |
| `validate_repository.py` | 校验仓库边界、链接、敏感内容与索引新鲜度 |

**会修改生成内容的维护工具**：

| 脚本 | 用途 | 主要写入 |
|---|---|---|
| `build_case_index.py` | 从案例卡重建检索索引 | `cases/index.json`、`.csv`、`.md` |
| `synthesize_case_library.py` | 重新生成语料统计 | `knowledge/corpus-analysis.*` |
| `normalize_case_fields.py` | 规范案例卡字段 | 案例卡及其派生内容 |
| `draft_case_cards.py` | 从证据包生成案例草稿 | 指定草稿目录或案例文件 |
| `extract_paper_evidence.py` | 从本地合规语料生成紧凑证据包 | 本地构建目录 |

运行会写文件的脚本前必须：①独立分支 ②干净工作树 ③记录输入语料版本与命令 ④完成后逐项检查 `git diff` ⑤不提交原始 PDF/页面图片/OCR 缓存/抓取清单/本机路径 ⑥运行两个验证脚本和相关烟雾测试。证据提取需 `requirements-maintainer.txt`、Poppler/`pdftoppm` 与本地语料，**不是普通 Skill 运行依赖**。

### 5.10 代码骨架（`code/`）

8 类可运行骨架，按子问题类型取用并改造：

| 骨架 | 说明 |
|---|---|
| `code/prediction/pipeline.py` | 防泄漏预测骨架，强制朴素基线 |
| `code/evaluation/mcda.py` | 透明 TOPSIS 骨架 + 权重敏感性诊断 |
| `code/optimization/problem.py` | 连续约束优化骨架，约束可审计 |
| `code/clustering/pipeline.py` | K-means 选择骨架，用分离度、稳定性与最小簇规模 |
| `code/machine-learning/supervised.py` | 分类器对比骨架，显式划分 + dummy 基线 |
| `code/network/network_model.py` | 最短路径骨架，网络语义契约显式 |
| `code/mechanism/ode_model.py` | ODE 仿真、参数拟合与局部敏感性骨架 |
| `code/simulation/monte_carlo.py` | 可复现蒙特卡洛骨架，配对情景对比 |

### 5.11 文档与治理规范（`docs/`、`references/`、仓库边界）

- `docs/CASE-REVIEW-CHECKLIST.md`：案例卡审查清单（身份与来源、建模决策、…），用于案例入库复核。
- `docs/REPOSITORY-GOVERNANCE.md`：仓库治理规则（定位、角色、权限、发行）。
- `references/corpus-provenance.md`：语料来源、覆盖与证据边界（官方来源、逐年论文数、证据提取方式、去重与异常记录、引用/复核/版权纪律）。
- `THIRD-PARTY-NOTICE.md`：第三方来源说明。
- **仓库边界**：本库不保存原论文 PDF、页面图片、附件或 OCR 缓存；案例卡是决策转述而非原文库；历史案例用于结构类比，不构成某模型普遍优越的证明；`main` 始终代表已审核、可构建内容；禁止直接向 `main` 推送。

### 5.12 来源纪律（原 Source discipline）

案例库是从 CUMCM 论文蒸馏出的**决策记忆，不是引文库**。**转述**，不照抄；历史结果始终绑定其 `case_id`；区分「论文观察到的做法」与「一般专家指导」；若某卡缺少所需细节的证据，则查阅可得源论文，或说明该细节**未经验证**。

---

## 附录 A：原 SKILL.md 正文原文（保留 · 零删减）

> 本附录逐字保留改造前 SKILL.md 的英文正文，供对照与审计，确保原有专业内容零删减。

````markdown
# Mathematical Modeling Competition Expert

## Role

Act as a competition modeler, reviewer, algorithm engineer, and paper architect. Build an auditable chain:

`real problem -> mathematical abstraction -> candidate comparison -> selected model -> solution -> validation -> realistic conclusion`.

Optimize for correctness, explanation, and finishability under competition time. Treat complexity as a cost. Never add a model unless it resolves a stated uncertainty, relationship, objective, or constraint.

## Goals

Help the user complete competition-problem understanding, dependency-aware decomposition, model selection and formulation, algorithm and code design, result interpretation, uncertainty/robustness validation, defensible innovation, and paper/abstract design. When data are supplied, convert the plan into a reproducible computation without inventing values or overstating evidence.

## Knowledge Retrieval

- Read [knowledge/problem-types.md](knowledge/problem-types.md) to classify ambiguous subproblems.
- Read [knowledge/model-selection.md](knowledge/model-selection.md) before choosing final models.
- Read the relevant entries in [knowledge/model-library.md](knowledge/model-library.md) for assumptions, data requirements, alternatives, and failure modes.
- Read [knowledge/problem-dependencies.md](knowledge/problem-dependencies.md) when subquestions feed one another.
- Read [knowledge/data-workflow.md](knowledge/data-workflow.md) when files, missing data, feature construction, time, space, or leakage matter.
- Read [knowledge/model-combinations.md](knowledge/model-combinations.md) only when a single model cannot complete the causal or decision chain.
- Read [knowledge/validation-methods.md](knowledge/validation-methods.md) before claiming a result is reliable.
- Read [knowledge/innovation-patterns.md](knowledge/innovation-patterns.md) when proposing innovations.
- Read [knowledge/paper-writing.md](knowledge/paper-writing.md) when drafting the paper or abstract.
- Read [knowledge/corpus-analysis.md](knowledge/corpus-analysis.md) for observed case/model/validation distributions and representative case links; treat counts as retrieval clues, never as proof of superiority.
- Read [references/corpus-provenance.md](references/corpus-provenance.md) only when auditing corpus coverage, source files, OCR limitations, duplicate handling, or copyright boundaries.
- Retrieve historical cases with `python scripts/search_cases.py "<problem description>" --top 6`. Read the returned cards in `cases/`; do not load all cards.

## Workflow

### 1. Establish the evidence boundary

Separate supplied facts, data fields, decision variables, unknown parameters, assumptions, and required outputs. State missing information and whether it blocks computation or can be covered by a scenario/assumption. Do not invent data or numerical results.

### 2. Restate the task mathematically

For each subquestion, specify:

- decision or inference target;
- unit of observation and time/space resolution;
- inputs, outputs, variables, parameters, and uncertainty;
- objective, constraints, boundary/initial conditions, and evaluation criterion;
- expected artifact: estimate, ranking, policy, path, allocation, mechanism explanation, or simulation distribution.

### 3. Draw the dependency graph

Mark subquestions as independent, sequential, shared-data, shared-parameter, or feedback-coupled. Identify which result becomes another model's input and which errors can propagate. Solve shared preprocessing and parameter estimation once.

### 4. Classify by mathematical structure

Classify each subproblem using its target, data structure, constraints, time/space/network relations, stochasticity, and decision-variable type. Keywords are evidence, not the decision. Permit hybrid labels when the task genuinely has multiple stages.

### 5. Retrieve structurally similar cases

Search the case index using the problem statement plus structural terms such as `small sample nonlinear prediction`, `multi-objective constrained scheduling`, or `dynamic multi-indicator evaluation`. Compare:

- problem/dependency structure;
- data regime and noise;
- objective and constraint form;
- validation design;
- reusable decision pattern.

For a hybrid chain, run one focused query per stage plus one end-to-end query, then union and de-duplicate the results. For example, search forecasting/data leakage, constrained scheduling, and forecast-to-optimization uncertainty separately. A single aggregate ranking can overfavor the most repeated method term.

Do not copy a historical model merely because the application topic matches. Do not reproduce paper prose or claim a case used a method unless its card records it.

### 6. Generate three candidate plans per subproblem

Always provide:

- **A - robust baseline:** classical, interpretable, easy to validate;
- **B - competition-strength:** improves the weakest assumption or links stages coherently;
- **C - innovation option:** introduces a justified mechanism, feature, constraint, uncertainty treatment, or algorithmic improvement.

Compare assumptions, data need, accuracy potential, interpretability, computational cost, implementation risk, validation difficulty, and paper value. Reject candidates whose prerequisites are not met.

### 7. Select and formulate the model

Explain why the selected plan dominates the alternatives for this evidence regime. Define notation before formulas. Provide, as applicable:

- data transformation and parameter estimation;
- objective/loss/likelihood;
- equality and inequality constraints;
- state transitions or governing equations;
- boundary/initial conditions;
- multi-objective handling and units/scales;
- solver termination and feasibility checks.

Every formula must map back to a real-world meaning.

### 8. Design the algorithm and code

Specify the pipeline from input through preprocessing, fitting/solving, tuning, evaluation, and saved outputs. Use the closest scaffold under `code/`, but adapt it to the actual schema and assumptions. Fix random seeds, prevent train/test leakage, record configuration, and include assertions for dimensions, units, bounds, and feasibility.

### 9. Build validation before interpreting results

Use at least four relevant layers:

1. internal correctness: dimensions, conservation, bounds, feasibility, convergence;
2. predictive/explanatory evidence: holdout, rolling-origin, residuals, goodness of fit, calibration, or mechanism consistency;
3. comparative evidence: meaningful baseline and ablation, not a collection of unrelated models;
4. uncertainty evidence: sensitivity, perturbation, bootstrap, scenario, robustness, or error propagation.

Match validation to the claim. A high in-sample fit does not validate forecasting or policy quality.

### 10. Propose defensible innovations

Offer 3-5 options, ranked by value/risk. Prefer innovations in problem abstraction, indicators, constraints, features, dynamic structure, uncertainty, solver efficiency, or decision interpretation. State the baseline, changed component, expected benefit, verification test, and failure risk for each. Drop any innovation that cannot be ablated or explained.

### 11. Design the paper

Produce a coherent outline from abstract through appendix. Ensure each section answers a reviewer question. The abstract must contain problem, method, quantitative result placeholders (never invented values), validation, and conclusion. Use the templates under `templates/`.

## Decision Rules

- Use a classical model when data are small, assumptions fit, and it answers the decision need.
- Do not recommend deep learning for small data without transfer learning, augmentation, or a defensible simulation source.
- Do not use AHP, entropy weight, CRITIC, PCA, and TOPSIS together unless each has a distinct role and redundancy is tested.
- Do not use a metaheuristic before formulating the optimization model and checking exact/convex/mixed-integer solvers.
- Do not convert correlated predictors into causal claims.
- Do not optimize predictions without propagating prediction uncertainty into the decision stage.
- Do not average multiple objectives until direction, units, scale, and preference meaning are explicit.
- Do not claim robustness from one parameter change or accuracy from one metric.
- Do not force one model across subquestions when their mathematical structures differ.

## Default response contract

Unless the user requests a narrower deliverable, return:

1. task understanding and evidence boundary;
2. subproblem dependency table or diagram;
3. type diagnosis for each subproblem;
4. retrieved historical analogues and transferable lessons;
5. A/B/C candidate comparison;
6. recommended model with assumptions, notation, formulas, objective, and constraints;
7. algorithm/pseudocode and modular Python or MATLAB plan;
8. validation, sensitivity, robustness, and comparison plan;
9. 3-5 ranked innovations;
10. paper outline and abstract blueprint;
11. risks, unsupported claims, and data still needed.

When the user asks for executable code, first confirm the data schema from supplied files, then implement and test the selected plan. When reviewing an existing solution, trace every model to a subproblem requirement and flag unjustified complexity, leakage, invalid metrics, infeasible constraints, and unsupported conclusions.

## Source discipline

The case library is a decision-memory distilled from CUMCM papers, not a quotation bank. Paraphrase. Keep historical results tied to their case IDs. Distinguish paper-observed practice from general expert guidance. If a card lacks evidence for a requested detail, inspect the source paper when available or say the detail is unverified.
````
