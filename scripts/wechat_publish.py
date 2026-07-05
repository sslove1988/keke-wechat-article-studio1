# -*- coding: utf-8 -*-
"""
WeChat Publisher - Publish a structured article to WeChat draft box.

Enhanced version: automatically cleans up old drafts with the same title
before creating a new one, preventing duplicate drafts in the draft box.

Usage:
    python wechat_publish.py <article.json> <cover.png> [--config <config.json>]

cover.png is REQUIRED (media_id expires, cannot reuse cache).
Typically the first cleaned illustration from process_images.py output.

The article JSON must follow the schema in references/template-schema.md.
Config defaults to assets/wechat_config.json in the skill directory.
"""

import json
import sys
import os
import subprocess
import urllib.request

# Add scripts dir to path for template import
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS_DIR)
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")
sys.path.insert(0, SCRIPTS_DIR)
from wechat_template import WeChatTemplate


def get_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    with urllib.request.urlopen(url, timeout=15) as r:
        data = json.loads(r.read())
    if "access_token" not in data:
        raise Exception(f"Failed to get token: {data}")
    return data["access_token"]


def upload_image(token, image_path):
    """Upload image to WeChat material library, return (media_id, url)."""
    boundary = b"----FormBoundary123456"
    with open(image_path, "rb") as f:
        img_data = f.read()
    body = b"--" + boundary + b"\r\n"
    body += b'Content-Disposition: form-data; name="media"; filename="img.png"\r\n'
    body += b"Content-Type: image/png\r\n\r\n"
    body += img_data + b"\r\n"
    body += b"--" + boundary + b"--\r\n"
    headers = {
        "Content-Type": "multipart/form-data; boundary=----FormBoundary123456",
        "Content-Length": str(len(body)),
    }
    req = urllib.request.Request(
        f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
        data=body, headers=headers, method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        result = json.loads(r.read())
    return result.get("media_id"), result.get("url")


def upload_images_batch(token, image_paths):
    """Upload multiple images, return list of {media_id, url}."""
    results = []
    for path in image_paths:
        media_id, url = upload_image(token, path)
        results.append({"media_id": media_id, "url": url})
        print(f"  [OK] Uploaded {os.path.basename(path)}: {url}")
    return results


def delete_old_drafts(token, title):
    """Delete all drafts with the given title to prevent duplicates.

    Uses draft/batchget to list drafts, then draft/delete for each match.
    """
    list_url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
    list_payload = json.dumps({"offset": 0, "count": 20, "no_content": 1}, ensure_ascii=False)

    payload_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_list_payload.json")
    with open(payload_file, "w", encoding="utf-8") as f:
        f.write(list_payload)

    result = subprocess.run(
        ["curl", "-s", "-X", "POST", list_url,
         "-H", "Content-Type: application/json; charset=utf-8",
         "-d", f"@{payload_file}"],
        capture_output=True, encoding="utf-8"
    )
    drafts_data = json.loads(result.stdout)

    total = drafts_data.get("total_count", 0)
    deleted = 0
    for item in drafts_data.get("item", []):
        media_id = item.get("media_id")
        for art in item.get("content", {}).get("news_item", []):
            old_title = art.get("title", "")
            if old_title == title:
                print(f"  [CLEAN] Deleting old draft: {media_id}")
                del_url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"
                del_payload = json.dumps({"media_id": media_id}, ensure_ascii=False)
                del_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_del_payload.json")
                with open(del_file, "w", encoding="utf-8") as f:
                    f.write(del_payload)
                del_result = subprocess.run(
                    ["curl", "-s", "-X", "POST", del_url,
                     "-H", "Content-Type: application/json; charset=utf-8",
                     "-d", f"@{del_file}"],
                    capture_output=True, encoding="utf-8"
                )
                del_resp = json.loads(del_result.stdout)
                if del_resp.get("errcode") == 0:
                    print(f"    [OK] Deleted")
                    deleted += 1
                else:
                    print(f"    [FAIL] {del_resp}")

    if deleted:
        print(f"  Cleaned {deleted} old draft(s)")
    return deleted


def create_draft(token, title, author, digest, content, thumb_media_id):
    """Create a WeChat draft using curl to avoid encoding issues.

    CRITICAL: Never use requests.post(json=data) for Chinese content.
    requests uses ensure_ascii=True by default, causing mojibake.
    Always use: json.dumps(ensure_ascii=False) + curl + UTF-8 file.
    """
    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": content,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
    }
    payload = json.dumps({"articles": [article]}, ensure_ascii=False)

    payload_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_draft_payload.json")
    with open(payload_file, "w", encoding="utf-8", newline="") as f:
        f.write(payload)

    cmd = [
        "curl", "-s", "-X", "POST",
        f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}",
        "-H", "Content-Type: application/json; charset=utf-8",
        "-d", f"@{payload_file}",
    ]
    result = subprocess.run(cmd, capture_output=True, encoding="utf-8")
    return json.loads(result.stdout)


def publish(article_data, cover_image_path=None, config_path=None):
    """Main publish function.

    Args:
        article_data: dict with title, author, digest, theme, opening_text, sections
        cover_image_path: path to cover image (optional, reuses cached media_id)
        config_path: path to wechat_config.json (optional, defaults to skill assets)
    Returns:
        media_id of the created draft, or None on failure.
    """
    if config_path is None:
        config_path = os.path.join(ASSETS_DIR, "wechat_config.json")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    wechat = config["wechat"]
    token = get_token(wechat["app_id"], wechat["app_secret"])
    print(f"[OK] Token acquired")

    article_title = article_data["title"]

    # Step 0: Clean up old drafts with the same title
    print(f"\n--- Cleaning old drafts with title: {article_title} ---")
    delete_old_drafts(token, article_title)

    # Upload cover image (REQUIRED — cached media_id expires, never rely on it)
    thumb_media_id = None
    if cover_image_path and os.path.exists(cover_image_path):
        thumb_media_id, img_url = upload_image(token, cover_image_path)
        print(f"[OK] Cover uploaded: {thumb_media_id}")
        # Save to cache (for reference only, not for reuse)
        cover_id_file = os.path.join(ASSETS_DIR, "cover_media_id.txt")
        with open(cover_id_file, "w") as f:
            f.write(thumb_media_id)
    else:
        print("[ERROR] 封面图是必须的！media_id 会过期，不能复用缓存。")
        print("  用法: python wechat_publish.py <article.json> <cover.png> --config <config.json>")
        print("  cover.png 通常是第一张清洗后的配图（clean/ 目录下的第一张）")
        return None

    # Generate HTML from template
    theme = article_data.get("theme", config.get("theme", "blue"))
    tpl = WeChatTemplate(config_path, theme=theme)
    html = tpl.render(article_data)

    # Save HTML preview
    preview_path = os.path.join(os.getcwd(), "article_preview.html")
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] HTML preview saved: {preview_path}")

    # Create draft
    result = create_draft(
        token,
        article_title,
        article_data.get("author", config.get("author", "")),
        article_data.get("digest", ""),
        html,
        thumb_media_id,
    )

    if "media_id" in result:
        print(f"\n[SUCCESS] Draft created!")
        print(f"  media_id: {result['media_id']}")
        print(f"  title: {article_title}")
        print(f"  theme: {theme}")
        print(f"\nView at: https://mp.weixin.qq.com")

        # Update article count in config
        count = config.get("article_count", 1)
        config["article_count"] = count + 1
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return result["media_id"]
    else:
        errcode = result.get("errcode", 0)
        if errcode == 40007:
            print(f"\n[FAILED] media_id 无效（可能已过期）")
            print(f"  解决方案：重新提供封面图片路径，不要复用缓存。")
            print(f"  用法: python wechat_publish.py <article.json> <cover.png> --config <config.json>")
        elif errcode == 40164:
            import subprocess as _sp
            ip_result = _sp.run(["curl", "-s", "https://api.ipify.org"], capture_output=True, encoding="utf-8")
            current_ip = ip_result.stdout.strip() if ip_result.stdout else "未知"
            print(f"\n[FAILED] IP 不在白名单")
            print(f"  当前出口 IP: {current_ip}")
            print(f"  请在公众号后台「设置与开发 → 基本配置 → IP白名单」添加此 IP")
        elif errcode == 45003:
            print(f"\n[FAILED] 标题超长（限制 32 字节，约 10 个汉字）")
            print(f"  当前标题: {article_title}")
        elif errcode == 45004:
            print(f"\n[FAILED] 摘要超长（限制 54 字节，约 18 个汉字）")
        else:
            print(f"\n[FAILED] {result}")
        return None


if __name__ == "__main__":
    # Parse args
    article_path = None
    cover_path = None
    config_path = None

    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--config" and i + 1 < len(args):
            config_path = args[i + 1]
        elif not arg.startswith("--") and article_path is None:
            article_path = arg
        elif not arg.startswith("--") and cover_path is None:
            cover_path = arg

    if article_path is None:
        print("Usage: python wechat_publish.py <article.json> <cover.png> [--config <config.json>]")
        print("  cover.png is REQUIRED. Use the first cleaned illustration.")
        sys.exit(1)

    if cover_path is None:
        print("[ERROR] Missing cover image (second argument).")
        print("  cover.png is REQUIRED — media_id expires and cannot be reused from cache.")
        print("  Typically: clean/clean_00-title.png from your illustrations directory.")
        sys.exit(1)

    with open(article_path, "r", encoding="utf-8") as f:
        article_data = json.load(f)

    publish(article_data, cover_path, config_path)
