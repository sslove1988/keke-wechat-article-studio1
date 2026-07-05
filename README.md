# 公众号写作工作室 (Keke WeChat Article Studio)

面向从未使用过的用户，一个 Skill 搞定公众号文章从写作到发布草稿箱的全流程。

## 特性

- **账号定位驱动**：首次使用填写 USER-PROFILE.md，AI 根据你的定位和风格写作
- **深度长文写作**：观点先行、案例论证、短句为主
- **小黑 IP 配图**：内置配图指南，用 ImageGen 生成手绘风格正文配图
- **小清新风格排版**：Optima-Regular 字体、蓝色主题、极简设计
- **图片清洗**：自动去灰底、去水印、平衡留白
- **一键发布**：自动清理旧草稿、上传封面、创建新草稿
- **自包含**：不依赖任何外部 Skill

## 快速开始

### 1. 安装

将本目录放到 WorkBuddy 的 skills 目录：

```bash
# macOS / Linux
cp -r keke-wechat-article-studio ~/.workbuddy/skills/

# Windows
xcopy /E /I keke-wechat-article-studio %USERPROFILE%\.workbuddy\skills\keke-wechat-article-studio
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 配置账号

复制模板并填写：

```bash
cp USER-PROFILE-TEMPLATE.md USER-PROFILE.md
cp assets/wechat_config.template.json assets/wechat_config.json
```

在 `USER-PROFILE.md` 中填写：
- 账号定位（你是谁、做什么）
- 目标用户
- 表达风格
- 微信公众号信息（AppID、AppSecret）

### 4. 开始使用

在 WorkBuddy 中说：

> 帮我写一篇关于 XXX 的公众号文章

AI 会自动完成：写作 → 配图 → 清洗 → 排版 → 发布到草稿箱

## 文件结构

```
keke-wechat-article-studio/
├── SKILL.md                          # 主流程
├── USER-PROFILE-TEMPLATE.md          # 账号定位模板
├── USER-PROFILE.example.md           # 示例
├── requirements.txt                  # Python 依赖
├── .gitignore
├── scripts/
│   ├── setup.py                      # 一键环境检查
│   ├── wechat_template.py            # 小清新排版引擎
│   ├── wechat_publish.py             # 发布脚本
│   ├── process_images.py             # 图片清洗
│   └── upload_user_image.py          # 用户图片上传
├── assets/
│   └── wechat_config.template.json   # 配置模板
└── references/
    ├── illustration-guide.md         # 小黑配图完全指南
    ├── writing-style-guide.md        # 写作风格指南
    ├── template-schema.md            # 文章 JSON 格式
    └── wechat-api.md                 # API 避坑
```

## 许可证

MIT License
