# 文章 JSON Schema

## 顶层结构

```json
{
  "title": "文章标题（≤32字节，约10个汉字）",
  "author": "作者名",
  "digest": "摘要（≤54字节，约18个汉字）",
  "theme": "blue | green | red | purple | orange",
  "opening_text": "这是XXX的第 N 篇原创！",
  "sections": [ ... ]
}
```

## 注意事项

- **title**: 微信限制 32 字节（UTF-8 下约 10 个汉字），超长会报错 45003
- **digest**: 微信限制 54 字节（UTF-8 下约 18 个汉字），超长会报错 45004
- **author**: 从 config 读取，也可在 article JSON 中覆盖
- **theme**: 从 config 的 presets 中选择，默认 blue

## section 类型

所有类型共用 `type` 字段指定：

### title - 小节标题
```json
{"type": "title", "text": "一、AI 到底改变了什么"}
```

### body - 正文段落
```json
{"type": "body", "paragraphs": [
  "第一段正文。",
  "第二段正文，包含<strong style='color:#165dff;'>高亮文字</strong>。"
]}
```
- 段落中可嵌入 `<strong style='color:#165dff;'>高亮</strong>` 标签实现彩色强调
- 每段自动加 30px 上下间距，无首行缩进

### highlight - 引用块
```json
{"type": "highlight", "text": "核心金句放在这里。"}
```
- 浅色背景 + 左侧彩色边框 + 圆角
- 用于放核心判断或金句

### steps - 步骤段落
```json
{"type": "steps", "items": [
  {"title": "第一步：选题", "text": "描述内容..."},
  {"title": "第二步：写作", "text": "描述内容..."}
]}
```
- 标题加粗变色，正文普通
- 自动用「：」连接标题和内容

### numbered - 编号列表
```json
{"type": "numbered", "items": [
  {"title": "先跑通一个小流程", "text": "不要一开始就想着全自动化。"},
  {"title": "建立风格模版", "text": "把最好的文章喂给 AI。"}
]}
```
- 自动加 ①②③ 圆圈编号
- 标题和内容用 `<br/>` 换行

### image - 配图
```json
{"type": "image", "src": "http://mmbiz.qpic.cn/..."}
```
- 必须使用微信素材库的 mmbiz.qpic.cn URL
- 外链图片无法在微信正文显示
- 图片自动居中、圆角、加阴影

### divider - 分割线
```json
{"type": "divider"}
```
- 虚线分割，上下 30px 间距

### ending - 结尾
```json
{"type": "ending", "title": "最后说一句", "paragraphs": [
  "结尾第一段。",
  "结尾第二段。"
]}
```
- 标题加粗变色
- 段落普通样式

## 完整示例

```json
{
  "title": "我用AI做自媒体降维打击",
  "author": "孙可可",
  "digest": "AI把自媒体内容生产从体力活变成系统能力",
  "theme": "blue",
  "opening_text": "这是孙可可的第 1 篇原创！",
  "sections": [
    {"type": "body", "paragraphs": [
      "大家好，我是孙可可。",
      "今天聊聊<strong style='color:#165dff;'>降维打击</strong>。"
    ]},
    {"type": "image", "src": "http://mmbiz.qpic.cn/xxx"},
    {"type": "title", "text": "一、AI 到底改变了什么"},
    {"type": "body", "paragraphs": [
      "很多人把 AI 理解为写文章的工具，太浅了。",
      "AI 改变的是<strong style='color:#165dff;'>整个链路</strong>。"
    ]},
    {"type": "highlight", "text": "核心区别：体力驱动 vs 系统驱动。"},
    {"type": "title", "text": "四、你现在应该做什么"},
    {"type": "numbered", "items": [
      {"title": "先跑通一个小流程", "text": "不要想着全自动化。"},
      {"title": "建立风格模版", "text": "把最好的文章喂给 AI。"}
    ]},
    {"type": "ending", "title": "最后说一句", "paragraphs": [
      "完成比完美重要。"
    ]}
  ]
}
```
