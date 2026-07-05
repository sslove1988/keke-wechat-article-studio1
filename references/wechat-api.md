# 微信公众号 API 要点

## 编码问题（最重要）

**永远不要用 `requests.post(json=data)` 发送中文内容到微信 API。**

`requests` 默认 `ensure_ascii=True`，会把中文转成 `\uXXXX` 转义序列。微信 API 会把这些转义序列当字面文本存储，导致文章内容全是乱码。

### 正确做法

```python
import json, subprocess

payload = json.dumps(data, ensure_ascii=False)

# 写入临时文件
with open('_draft_payload.json', 'w', encoding='utf-8', newline='') as f:
    f.write(payload)

# 用 curl 发送
cmd = [
    'curl', '-s', '-X', 'POST',
    f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}',
    '-H', 'Content-Type: application/json; charset=utf-8',
    '-d', '@_draft_payload.json',
]
result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
```

## 核心 API

### 1. 获取 access_token
```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}
```
- token 有效期 2 小时
- 每天限 2000 次调用

### 2. 上传图片到素材库
```
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image
```
- multipart/form-data 格式
- 返回 `media_id` 和 `url`（mmbiz.qpic.cn 域名）
- 这个 URL 才能在正文 `<img src="">` 中使用
- `media_id` 可作为草稿的封面 thumb_media_id

### 3. 创建草稿
```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}
```
Body:
```json
{
  "articles": [{
    "title": "标题",
    "author": "作者",
    "digest": "摘要",
    "content": "HTML内容",
    "content_source_url": "",
    "thumb_media_id": "封面media_id",
    "need_open_comment": 0
  }]
}
```

**重要：每次调用 `draft/add` 都会创建一个新草稿，不会覆盖旧草稿。**
重新发布同一篇文章前，必须先删除旧草稿。

### 4. 获取草稿列表
```
POST https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}
```
Body:
```json
{"offset": 0, "count": 20, "no_content": 1}
```
- `no_content: 1` 不返回正文内容，减少数据量

### 5. 删除草稿
```
POST https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}
```
Body:
```json
{"media_id": "要删除的media_id"}
```

## 限制

| 字段 | 限制 | 超限错误码 |
|------|------|-----------|
| title | 32 字节 (UTF-8 约 10 汉字) | 45003 |
| digest | 54 字节 (UTF-8 约 18 汉字) | 45004 |
| content | 20000 字符 | 45005 |
| author | 8 字节 (UTF-8 约 2-3 汉字) | 45006 |

## 常见错误

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| 40164 | IP 不在白名单 | 在公众号后台「设置→开发→IP白名单」添加出口 IP |
| 45003 | 标题超长 | 缩短标题 |
| 45004 | 摘要超长 | 缩短 digest |
| 48001 | API 未授权 | 订阅号无群发权限，只能手动从草稿发布 |
| 40007 | media_id 无效 | 重新上传图片获取新的 media_id |

## HTML 标签兼容性（关键）

微信编辑器会**静默移除**不支持的 HTML 标签，不会报错。

### 被移除的标签（会导致内容丢失）
- `<figure>` — 移除后内部 `<img>` 也会丢失，**图片完全不显示**
- `<figcaption>` — 同上
- `<picture>` — 同上
- `<video>` / `<audio>` / `<canvas>` — 不支持
- `<style>` / `<script>` — 移除
- `<form>` / `<input>` — 移除

### 图片正确写法
```html
<p style="text-align: center; margin: 20px 0px 30px; padding: 0px; font-size: 0px;">
  <img src="http://mmbiz.qpic.cn/..." data-src="http://mmbiz.qpic.cn/..." data-w="1080"
       style="width: 100%; max-width: 1080px; height: auto; border-radius: 6px; vertical-align: middle;" />
</p>
```
要点：
- 用 `<p>` 包裹，不用 `<figure>`
- `data-src` 和 `src` 同时写
- `data-w` 设为图片实际宽度
- `font-size: 0px` 消除 `<p>` 底部间隙
- `vertical-align: middle` 消除图片底部基线间隙
- 图片 URL 必须是 `mmbiz.qpic.cn` 域名（上传到素材库后获取）

## 图片处理要点

ImageGen 生成的图片有两个问题：
1. **灰色背景**：ImageGen 输出不是纯白底，而是 RGB ~146,147,144 的灰底
2. **水印**：右下角有「图片由AI生成」白色半透明水印

解决方案见 `scripts/process_images.py`：
- 四角采样检测背景色 → 容差 ±28 强制白
- 灰像素清除（饱和度<30 且 亮度>175）
- 裁掉底部 38px（水印区域）
- 自动裁切到内容边界
- 6% 均匀留白重新填充
- 缩放到 1080px 宽
