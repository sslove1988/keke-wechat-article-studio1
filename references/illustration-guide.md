# 小黑 IP 正文配图指南（自包含）

本指南整合了配图生成的全部规则。本 skill 不依赖外部 `ian-xiaohei-illustrations` skill，所有配图能力都在此文件中。

## 1. 风格 DNA

### 一句话

纯白、极简、手绘、留白、克制、怪诞、产品草图感、中文手写感、结构清楚但不说明书。

像一个长期做 AI、产品、设计、开发工具的人，在白纸上随手画出来的一张解释草图。

### 必须

- 16:9 横版正文配图。
- 纯白背景：不要米色、暖灰、纸张纹理、渐变、阴影、噪点、复古纸感。
- 黑色手绘线稿为主：细线、轻微抖动、不机械、不矢量、不厚重描边。
- 大量留白：主体占画面约 40%-60%，至少 35% 空白，最好有一整块安静区域。
- 少量中文手写批注：最多 5-8 处，每处尽量 2-8 个字。
- 一张图只讲一个核心动作、结构、状态或隐喻。
- 结构要自然表达，不要在图上写结构类型名称。

### 颜色

- 黑色：主体线稿、角色、框线、结构、主要文字、主体物件。
- 红色：重点批注、问题、情绪点、关键提醒、结果。
- 橙色：主流程、路径、箭头、自动化流向、从 A 到 B 的移动关系。
- 蓝色：补充说明、脑内状态、系统状态、第二层解释、AI/assistant/自动化提示。

蓝色不是每张都必须用。颜色要克制，宁可少不要多。

### 绝对不要

- 不要商业插画。
- 不要 PPT 信息图。
- 不要正式流程图。
- 不要课程课件。
- 不要可爱卡通海报。
- 不要儿童插画。
- 不要复杂架构图。
- 不要精致扁平插画。
- 不要科技感 UI。
- 不要真实 App 截图。
- 不要复杂背景、渐变、阴影、纹理。
- 不要把每个节点都解释清楚。
- 不要左上角写"Workflow 流程图 / 系统架构图 / 常见坑 / 路线图"等类型标题。

## 2. 小黑 IP

### 角色定义

小黑是正文配图的固定视觉 IP。默认每张图都要出现小黑。小黑不是吉祥物，不是贴纸，不是可爱装饰，而是正在认真参与系统运转的荒诞工作者。

### 外形

- 黑色实心小怪物。
- 白色圆点眼睛。
- 细腿，偶尔有细胳膊。
- 身体可以是圆柱、黑豆、黑盒、漏斗、影子、洞口、机器内部黑块。
- 轮廓略微不规则，有手绘感。
- 表情空、呆、冷静、认真。

### 性格

- 很认真，但做的事有点荒诞。
- 像一个低调的系统操作员。
- 冷幽默，不卖萌。
- 有点笨拙，但不蠢。
- 像在白板草图里真的负责某个工作。

### 常见职责

让小黑承担核心动作：

- 搬运素材。
- 拉线汇聚信息源。
- 卡在断点里。
- 在机器里操作"判断"杆。
- 变成筛选漏斗。
- 切开"素材鱼"。
- 盖章承接话术。
- 牵着承接路径。
- 举警告牌看坑。
- 从洞里伸手但接不住内容。
- 在旁边搬砖、搭桥、开门、分拣、记录。

### 禁止

- 不要把小黑画成过度可爱的吉祥物。
- 不要画成儿童卡通角色。
- 不要给小黑复杂服装、表情包、闪亮眼睛。
- 不要让小黑只是站在角落里看。
- 不要让小黑抢走结构表达。
- 不要把小黑画得太商业、太圆润、太精致。

### 判断标准

如果去掉小黑，图的核心隐喻还能完全成立，说明小黑太装饰了；要重写提示词，让小黑成为动作主体。

## 3. 构图模式与原创规则

### 基础结构类型

选择一种结构即可，不要混太多。

| 结构类型 | 适合场景 | 画法 |
|----------|----------|------|
| Workflow 流程 | 输入→处理→输出，AI 工作流 | 左侧输入，中间小黑处理，右侧输出，橙色箭头 |
| 系统局部 | 信息来源、过滤器、数据库 | 只画 3-5 个核心模块，小黑参与关键动作 |
| 前后对比 | 混乱/有序，手动/自动 | 左混乱，右稳定，中间橙色箭头 |
| 角色状态 | 用户痛点、创作者状态 | 2-4 个小状态，每个状态一个短标注 |
| 概念隐喻 | 内容工厂、信息仓库、工作流机器 | 一个大的怪物件或机器，少量输入，一个输出 |
| 方法分层 | 方法论框架、系统层级 | 一层层盒子，小黑在旁边搬砖或搭建 |
| 地图路线 | 从想法到上线、用户路径 | 一条弯曲路径，少量节点，小黑牵线或走路 |
| 小漫画分镜 | 失败到成功、使用前后变化 | 2-4 个小场景，每格只表达一个动作 |

### 原创隐喻生成法

每次都从当前文章重新发明隐喻，不能照搬旧图。

**三步：**

1. 把抽象概念换成一个物理动作：卡住、漏掉、变重、分拣、沉淀、发酵、开门、折叠、拆包、回流。
2. 把系统结构换成一个低科技物件：坏掉的机器、纸箱、抽屉、水管、邮筒、怪表盘、秤、井、梯子、奇怪工位。
3. 让小黑承担动作：不是站旁边，而是卡在机器里、拉错线、守门、搬运、修补、称重、扶梯子、记录、把东西塞进某个怪装置。

**可用物件池：**
纸箱、抽屉、旧机器、漏斗、秤、邮筒、门、井、梯子、水管、线团、闸门、转盘、黑盒、打孔器、压面机、晾衣绳、怪工位。用时只选 1-2 个，不要堆满。

**小黑动作池：**
拉、扛、塞、捞、压、称、缝、剪、拧、守、推、接、拆、标记、回收。动作要服务核心意思，不要为了怪而怪。

## 4. 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring IP character required:
小黑, a small solid-black absurd creature with white dot eyes, tiny thin legs, blank serious expression, slightly uneven hand-drawn body shape. 小黑 must perform the core conceptual action, not decorate the scene. Make 小黑 serious, deadpan, and slightly bizarre, not cute.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：小黑在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use:
Black for main line art and 小黑. Orange for main flow/path/arrows. Red only for key warnings/problems/results. Blue only for secondary notes or feedback/system state.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

### 图像编辑提示

去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

增强怪诞感：

```text
Regenerate this illustration with the same core meaning and simple layout, but make 小黑 more central to the conceptual action. 小黑 should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, and not cute.
```

## 5. QA 检查表

### 必过项

- [ ] 是 16:9 横版。
- [ ] 背景是干净白底。
- [ ] 有小黑。
- [ ] 小黑承担核心动作，不只是装饰。
- [ ] 没有复刻旧案例构图，而是为当前文章生成了新隐喻。
- [ ] 画面怪诞、有创意、有意思。
- [ ] 简洁清爽，主体不超过画面约 60%。
- [ ] 一张图只讲一个核心结构。
- [ ] 中文标注少、短、能读。
- [ ] 橙色只用于主路径或箭头。
- [ ] 红色只用于重点、问题、提醒或结果。
- [ ] 蓝色只用于补充说明、反馈或系统状态。

### 失败信号

出现以下情况，重生成或局部编辑：

- 左上角有"常见坑 / Workflow / 系统架构图 / 路线图"等标题。
- 小黑像吉祥物、表情包或可爱卡通。
- 画面像 PPT、课程课件、正式流程图。
- 元素太多、箭头太多、节点太多。
- 文字变成大段解释。
- 背景有纸纹、阴影、渐变、米色、噪点。
- 真实 UI 截图或科技感界面。
- 中文错字严重或标注不可读。
- 画面太死板，没有荒诞隐喻。

### 迭代方法

- 太普通：让小黑成为动作主体，加入一个奇怪但成立的隐喻。
- 太复杂：删节点，只保留一个动作和 3-5 个短标注。
- 太可爱：强调 deadpan、blank serious expression、not cute、not mascot。
- 太 PPT：去掉标题、边框、整齐网格和过多箭头，改成手绘场景。
- 太像旧案例：保留核心意思，换掉主物件和小黑动作。
- 文字错：优先局部编辑；错得多就重生成并减少标注数量。

### 交付判断

高质量图应该让读者先觉得"有点怪"，然后 1 秒内看懂结构。如果第一眼像教程页，而不是白纸上的怪诞产品草图，就不合格。

## 6. 配图工作流

### 消化正文

先读正文内容。提炼：
- 核心观点是什么
- 哪些段落承担认知转折
- 哪些内容适合用图解释
- 哪些地方只适合文字，不需要图

不要平均配图。优先选择"认知锚点"：核心判断、两个断点、输入输出闭环、分流、前后对比、一鱼多吃、承接路径、常见坑、角色状态变化。

### 配图策略

每张图写清楚：
- 放在哪个段落后
- 图的主题
- 核心意思
- 结构类型
- 小黑在图里做什么
- 建议元素
- 建议中文标注词

默认 4-5 张（标题图 + 每个大节后 1 张）。文章很短时 1-3 张；长文也不要轻易超过 8 张。

### 逐张生成

**关键：每张图必须逐个生成，不能批量。** 同秒生成会因时间戳冲突导致文件覆盖。

用 ImageGen 工具，每张图单独调用。保存到工作目录 `assets/<article-slug>-illustrations/`。

### 图片清洗

生成后运行 `process_images.py` 清洗：
- 灰底转纯白
- 裁掉底部 38px 水印
- 自动裁切到内容边界
- 6% 均匀留白
- 缩放到 1080px 宽
