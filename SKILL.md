---
name: keke-wechat-article-studio
description: 公众号写作工作室。面向从未使用过的新用户，通过 USER-PROFILE.md 账号定位驱动写作风格、内容方向和目标读者。输入标题，自动完成写作、配图、排版、发布到草稿箱全流程。首次使用时会引导填写账号配置。
agent_created: true
---

# 公众号写作工作室

> © 2026 孙可可 (keke). CC BY-NC 4.0. 禁止商用，转载请注明出处。

## 这个 Skill 解决什么问题

你是一个有表达欲的人，想写公众号，但每次都卡在：
- 不知道写什么选题
- 写了开头写不下去
- 排版太丑没动力发
- 配图找不到合适的
- 发到草稿箱操作繁琐

这个 Skill 把整条链路自动化了。你只需要给一个标题或方向，它帮你完成从写作到草稿箱的全流程。

**但有一点必须先做好：账号定位。** 没有定位，AI 只能输出废话和通用鸡汤。

## 前置环境检查（首次使用必须完成）

### 一键检查（推荐）

运行 setup 脚本，自动完成所有环境检查和依赖安装：

```bash
python <skill_dir>/scripts/setup.py
```

脚本会自动：
1. 检查 Python 版本（需 3.10+）
2. 检查 pip 是否可用
3. 安装 Python 依赖（Pillow, numpy）
4. 检查 USER-PROFILE.md 是否已填写
5. 检查 wechat_config.json 是否已配置
6. 运行脚本导入自测

全部通过后就可以直接使用了。

### 手动安装依赖（如果 setup.py 未通过）

```bash
pip install -r <skill_dir>/requirements.txt
```

**如果 pip 不可用或权限不足**，用以下方式在隔离环境中安装：
```bash
python -m venv <skill_dir>/.venv
<skill_dir>/.venv/Scripts/pip install Pillow numpy   # Windows
# 或
<skill_dir>/.venv/bin/pip install Pillow numpy         # macOS/Linux
```

然后运行脚本时用 venv 的 Python：
```bash
<skill_dir>/.venv/Scripts/python process_images.py ...   # Windows
# 或
<skill_dir>/.venv/bin/python process_images.py ...        # macOS/Linux
```

### 本 Skill 完全自包含

**不依赖任何其他 skill。** 配图能力（小黑 IP 手绘风格）已内置于 `references/illustration-guide.md`，包含风格 DNA、小黑 IP 定义、构图模式、提示词模板和 QA 检查表。

## Step 0: 检查账号配置（首次使用必须完成）

### 0.1 检查 USER-PROFILE.md

读取本 skill 目录下的 `USER-PROFILE.md`。

**如果文件不存在或关键字段为空（含「替换为」「______」等占位符）：**

告诉用户：

> 你的账号配置还没填写。这是最重要的一步——没有定位，我只能输出通用内容。
>
> 请复制 `USER-PROFILE-TEMPLATE.md` 为 `USER-PROFILE.md`，填入以下关键信息：
> 1. **你是谁**：你的职业、正在做的事、专长领域
> 2. **目标用户**：你的读者是谁，他们有什么痛点
> 3. **表达风格**：你希望文章读起来什么感觉，什么风格是你不要的
> 4. **微信公众号信息**：AppID、AppSecret、作者署名
>
> 填好后告诉我，我们就可以开始写文章了。

等待用户填写后再继续。**不要在配置缺失时强行写文章。**

### 0.2 检查 wechat_config.json

读取 `assets/wechat_config.json`。如果文件不存在，或 `app_id` 含「替换为」：

1. 复制 `assets/wechat_config.template.json` 为 `assets/wechat_config.json`
2. 从 `USER-PROFILE.md` 中提取信息填入：
   - `wechat.app_id` ← USER-PROFILE 第 6 节
   - `wechat.app_secret` ← USER-PROFILE 第 6 节
   - `author` ← USER-PROFILE 第 6 节
   - `theme` ← USER-PROFILE 第 7 节（默认 blue）
3. 告诉用户配置已生成

### 0.3 提醒 IP 白名单

如果 API 调用报 40164 错误，提醒用户：

> 你的服务器 IP 不在公众号白名单中。请在公众号后台「设置与开发 → 基本配置 → IP白名单」添加以下 IP：[显示当前出口 IP]

获取出口 IP 命令：`curl -s https://api.ipify.org`

## Step 1: 写文章

### 读取配置

从 `USER-PROFILE.md` 中提取：
- 账号定位 → 决定选题方向和内容深度
- 目标用户 → 决定用词难度和案例选择
- 表达风格 → 决定语气、句式、结构
- 内容边界 → 决定不写什么

### 读取写作风格指南

读取 `references/writing-style-guide.md`，结合 USER-PROFILE 的表达风格来写。

**风格优先级：**
1. 用户本轮明确说明的要求
2. `USER-PROFILE.md` 中的表达风格
3. 写作风格指南的通用方法论

### 写作

根据用户给的标题或方向写一篇文章：

- 开头 1-2 段引入 + 核心观点
- 3-4 个编号小节（一、二、三、四）
- 每节 2-3 段论证
- 1-2 个 highlight 引用块放金句
- 结尾收束段落
- 总字数 1500-3000 字（根据 USER-PROFILE 配置调整）

标题限制：≤32 字节（约 10 个汉字），digest 限制：≤54 字节（约 18 个汉字）。

### 原创篇数

从 `wechat_config.json` 的 `article_count` 字段读取当前篇数，用于 `opening_text`。
发布成功后自动 +1，下次文章递增。

## Step 2: 生成配图

根据 USER-PROFILE 第 8 节的配图偏好：

### 选项 1：小黑 IP 手绘配图（内置，无需安装其他 skill）

1. 读取 `references/illustration-guide.md`，理解小黑 IP 风格 DNA、构图模式和提示词模板
2. 根据文章内容提炼 4-5 个配图点（标题图 + 每个大节后 1 张）
3. 按提示词模板填写每张图的 Theme / Structure type / Core idea / Composition / Elements / Labels
4. 每张图用 ImageGen 单独生成（**逐张生成，不能批量**，否则同秒时间戳会覆盖）
5. 16:9 横版，纯白底，小黑 IP
6. 保存到工作目录 `assets/<article-slug>-illustrations/`
7. 重命名为有意义的名字（如 `00-title.png`, `01-breakdown.png` 等）
8. 生成后对照 `illustration-guide.md` 第 5 节 QA 检查表验证质量

### 选项 2：用户自己上传图片

跳到 Step 4 直接上传。

### 选项 3：不需要配图

跳到 Step 5。

## Step 3: 清洗图片

运行图片清洗脚本处理所有原始图片：

```bash
python <skill_dir>/scripts/process_images.py <illustrations_dir>
```

自动完成：
- 灰底转纯白
- 裁掉底部 38px 水印（「图片由AI生成」）
- 自动裁切到内容边界
- 6% 均匀留白重新填充
- 缩放到 1080px 宽

输出在 `<illustrations_dir>/clean/` 目录。

## Step 4: 上传图片到微信

用 Python 上传清洗后的图片到微信素材库，获取 `mmbiz.qpic.cn` URL：

```python
import json, urllib.request

config = json.load(open("<skill_dir>/assets/wechat_config.json", encoding="utf-8"))
token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={config['wechat']['app_id']}&secret={config['wechat']['app_secret']}"
token = json.loads(urllib.request.urlopen(token_url, timeout=15).read())["access_token"]

# 上传每张图片（multipart/form-data）
# 返回 media_id 和 url (mmbiz.qpic.cn)
```

**注意**：这里上传的是正文中的配图（`<img src="">` 用的 URL）。封面图（`thumb_media_id`）由 Step 6 的发布脚本自动上传，不需要在这里处理。

### 用户自有图片

```bash
python <skill_dir>/scripts/upload_user_image.py <图片路径>
# 或上传整个目录
python <skill_dir>/scripts/upload_user_image.py <目录路径>
```

## Step 5: 组装文章 JSON

按 `references/template-schema.md` 的格式组装文章 JSON，将上传后的 mmbiz.qpic.cn URL 填入对应 image section。

保存为 `<工作目录>/article.json`。

## Step 6: 发布到草稿箱

封面图是**必须的**（微信 API 要求 `thumb_media_id`，且 media_id 会过期不能复用缓存）。

**封面图来源**：第一张清洗后的配图（`<illustrations_dir>/clean/` 目录下排序第一张）。

```bash
python <skill_dir>/scripts/wechat_publish.py <工作目录>/article.json <illustrations_dir>/clean/clean_00-title.png --config <skill_dir>/assets/wechat_config.json
```

如果用户选择了「不需要配图」，仍需要一个封面图。可以让 AI 用 ImageGen 单独生成一张，或让用户提供一张图片。

**脚本会自动：**
1. 清理同名旧草稿（防止草稿箱堆积重复文章）
2. 上传封面图（每次都重新上传，不复用缓存）
3. 生成小清新风格 HTML
4. 创建新草稿
5. article_count 自动 +1
6. 保存 HTML 预览到 `article_preview.html`

成功后会在 `https://mp.weixin.qq.com` 草稿箱中看到文章。

## 关键注意事项

### 编码问题（最重要）

**永远不要用 `requests.post(json=data)` 发送中文到微信 API。**
始终用 `json.dumps(ensure_ascii=False)` + `curl -d @file` + `Content-Type: application/json; charset=utf-8`。
详见 `references/wechat-api.md`。

### 图片 URL

正文中的 `<img src="">` 必须使用微信素材库的 `mmbiz.qpic.cn` URL。外链图片在微信中不显示。

### 字数限制

- title: ≤32 字节（约 10 个汉字）
- digest: ≤54 字节（约 18 个汉字）
- content: ≤20000 字符

### 草稿管理

每次 `draft/add` 都创建新草稿，旧草稿不会自动覆盖。
`wechat_publish.py` 已内置旧草稿清理逻辑（`delete_old_drafts`），发布前自动删除同名旧草稿。

### 封面图

- **每次发布都必须重新上传封面图**，media_id 会过期不能复用
- 封面图通常是第一张清洗后的配图（`clean/clean_00-*.png`）
- 如果用户选了「不需要配图」，仍需单独生成或提供一张封面图
- `wechat_publish.py` 不再回退到缓存，未提供封面图会直接报错退出

### Python 依赖

运行 `process_images.py` 和 `upload_user_image.py` 前必须安装 Pillow 和 numpy。
推荐运行 `python <skill_dir>/scripts/setup.py` 自动安装和验证。
手动安装：`pip install -r <skill_dir>/requirements.txt`

## 使用自己的图片

用户可以插入自己的截图、照片等图片，不依赖 AI 生成：

```bash
# 上传单张图片
python <skill_dir>/scripts/upload_user_image.py <图片路径>

# 上传整个目录
python <skill_dir>/scripts/upload_user_image.py <目录路径>

# 不做任何处理，直接上传原图
python <skill_dir>/scripts/upload_user_image.py <路径> --no-process
```

脚本会自动：
- 透明背景（PNG alpha）合成到白底
- 宽度超过 1080px 的自动缩放
- 支持 png / jpg / jpeg / gif / bmp / webp
- 输出 `user_uploaded_urls.json`，包含每张图的 mmbiz URL

在 `article.json` 的 `sections` 中添加：
```json
{"type": "image", "src": "http://mmbiz.qpic.cn/..."}
```

排版模版会自动适配任何尺寸的图片（居中、圆角、响应式宽度）。

## 文件结构

```
keke-wechat-article-studio/
├── SKILL.md                          # 本文件
├── USER-PROFILE-TEMPLATE.md          # 账号定位模板（用户复制为 USER-PROFILE.md）
├── USER-PROFILE.example.md           # 示例配置（仅参考格式）
├── requirements.txt                  # Python 依赖（Pillow, numpy）
├── scripts/
│   ├── setup.py                      # 一键环境检查（首次使用运行）
│   ├── wechat_template.py            # 小清新风格 HTML 模版引擎
│   ├── wechat_publish.py             # 发布脚本（含旧草稿清理+错误处理）
│   ├── process_images.py             # AI配图清洗（去灰底/水印/平衡留白）
│   └── upload_user_image.py          # 用户自有图片上传（截图/照片等）
├── assets/
│   ├── wechat_config.template.json   # 配置模板（用户复制为 wechat_config.json）
│   └── wechat_config.json            # 实际配置（首次使用时自动生成）
└── references/
    ├── writing-style-guide.md        # 写作风格指南（自适应 USER-PROFILE）
    ├── illustration-guide.md         # 小黑IP配图完全指南（自包含，无需外部skill）
    ├── template-schema.md            # 文章 JSON 格式说明
    └── wechat-api.md                 # 微信 API 要点与避坑
```

## 依赖

**无外部依赖。** 本 skill 完全自包含：
- 配图能力内置（`references/illustration-guide.md`）
- 图片清洗内置（`scripts/process_images.py`）
- 排版引擎内置（`scripts/wechat_template.py`）
- 发布脚本内置（`scripts/wechat_publish.py`）
- 仅需 Python 3.10+ 和 Pillow/numpy（`setup.py` 自动安装）

## 新用户快速上手

1. **运行环境检查**：`python <skill_dir>/scripts/setup.py`
2. **填写 `USER-PROFILE.md`**：复制模板，填入账号定位、目标用户、表达风格、微信信息
3. **告诉 AI**："帮我写一篇关于 XXX 的公众号文章"
4. AI 自动完成：写作 → 配图 → 清洗 → 上传 → 小清新排版 → 发布到草稿箱
5. 去 https://mp.weixin.qq.com 草稿箱审阅，满意后手动发布

**首次使用时 AI 会**：
- 运行 `setup.py` 检查环境（或手动检查）
- 检查 `USER-PROFILE.md` 是否已填写
- 检查 `wechat_config.json` 是否已生成
- 读取 `references/illustration-guide.md` 生成小黑IP配图（无需安装其他 skill）
- 如果 API 报 40164 错误，自动获取出口 IP 并提醒添加白名单
