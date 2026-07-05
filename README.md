# 公众号写作工作室（Keke WeChat Article Studio）

> © 2026 孙可可（keke）。本项目采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 协议授权。允许学习和交流使用，禁止商业用途，转载请注明原作者。

面向从未使用过的用户，一个 Skill 搞定公众号文章从选题、写作、配图、排版到发布草稿箱的全流程。

## 一句话介绍

`keke-wechat-article-studio1` 是一个面向公众号创作者的 WorkBuddy / Codex Skill，帮助用户把模糊想法快速变成一篇可发布的公众号文章，并完成配图、排版和发布前准备。

## 安装方式

### 方式一：在 WorkBuddy 里用自然语言安装

打开 WorkBuddy，对 Agent 说：

```text
安装这个 skill：https://github.com/sslove1988/keke-wechat-article-studio1
```

如果 Agent 需要你补充路径，请回复：

```text
路径是仓库根目录，path 是 .
```

也可以一次性这样说：

```text
安装这个 skill：https://github.com/sslove1988/keke-wechat-article-studio1，路径是仓库根目录，path 是 .
```

安装完成后，重启 WorkBuddy 或重新开启会话，让 skill 生效。

### 方式二：在 Codex 里用自然语言安装

对 Codex 说：

```text
安装这个 skill：sslove1988/keke-wechat-article-studio1，路径是仓库根目录，path 是 .
```

### 方式三：PowerShell 手动安装

如果自然语言安装没有成功，可以在 PowerShell 中运行：

```powershell
python "C:\Users\admin\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo sslove1988/keke-wechat-article-studio1 --path .
```

安装完成后，重启 Codex。

## 安装路径说明

本仓库的 `SKILL.md` 位于仓库根目录，因此安装路径是：

```text
.
```

如果安装时提示找不到 `SKILL.md`，请确认安装命令或自然语言指令里包含：

```text
path 是 .
```

## 特色

- **账号定位驱动**：首次使用填写 `USER-PROFILE.md`，AI 根据你的定位和风格写作。
- **深度长文写作**：支持观点先行、案例论证、短句表达的公众号文章结构。
- **配图辅助**：内置配图指南，可结合 ImageGen 生成正文配图。
- **清爽排版风格**：支持适合公众号阅读的简洁排版。
- **图片清洗**：支持图片去灰底、去水印和平衡留白等辅助处理。
- **发布草稿箱**：支持清理旧草稿、上传封面、创建新草稿等发布前动作。
- **自包含**：尽量减少对外部 Skill 的依赖。

## 快速开始

### 0. 安装 Python（如已安装可跳过）

本 Skill 需要 **Python 3.10+**。打开终端输入：

```bash
python --version
```

如果未安装或版本过低，请到 Python 官网下载：<https://www.python.org/downloads/>

Windows 安装时请勾选 **Add Python to PATH**。

### 1. 安装依赖

```bash
python scripts/setup.py
```

如果 `setup.py` 运行失败，可以手动安装依赖：

```bash
pip install -r requirements.txt
```

### 2. 配置账号

复制模板并填写：

```bash
cp USER-PROFILE-TEMPLATE.md USER-PROFILE.md
cp assets/wechat_config.template.json assets/wechat_config.json
```

在 `USER-PROFILE.md` 中填写：

- 账号定位：你是谁、做什么
- 目标用户
- 表达风格
- 微信公众号信息（AppID、AppSecret）

### 3. 开始使用

在 WorkBuddy 中说：

```text
帮我写一篇关于 XXX 的公众号文章
```

AI 会根据你的账号定位和需求，辅助完成：

```text
选题确认 → 大纲 → 正文 → 配图建议 → 排版 → 发布草稿箱
```

## 文件结构

```text
keke-wechat-article-studio1/
├── SKILL.md                         # Skill 主流程
├── USER-PROFILE-TEMPLATE.md         # 账号定位模板
├── USER-PROFILE.example.md          # 示例
├── requirements.txt                 # Python 依赖
├── .gitignore
├── scripts/
│   ├── setup.py                     # 一键环境检查
│   ├── wechat_template.py           # 排版引擎
│   ├── wechat_publish.py            # 发布脚本
│   ├── process_images.py            # 图片清洗
│   └── upload_user_image.py         # 用户图片上传
├── assets/
│   └── wechat_config.template.json  # 配置模板
└── references/
    ├── illustration-guide.md        # 配图指南
    ├── writing-style-guide.md       # 写作风格指南
    ├── template-schema.md           # 文章 JSON 格式
    └── wechat-api.md                # API 说明
```

## 适用人群

- 不知道公众号第一篇写什么的新手
- 有公众号但长期闲置的人
- 有想法但写不成完整文章的人
- 想把公众号写作、配图、排版流程固定下来的人
- 想用 AI 提高公众号发布效率的人

## 许可证

本项目采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)（署名-非商业性使用）协议。

- 允许学习、交流、引用和修改
- 必须署名：© 2026 孙可可（keke）
- 禁止商业用途
- 禁止闭源再发布
