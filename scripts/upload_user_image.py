# -*- coding: utf-8 -*-
"""
Upload user's own images (screenshots, photos, etc.) to WeChat material library.

Unlike process_images.py (which is for AI-generated illustrations),
this script does NOT remove watermarks or gray backgrounds.
It only does light processing:
  - Flatten transparency to white (for PNG screenshots with alpha)
  - Resize if wider than 1080px
  - Convert to RGB (strip ICC profiles etc.)

Usage:
    # Upload a single image
    python upload_user_image.py <image_path>

    # Upload all images in a directory
    python upload_user_image.py <directory>

    # Skip processing, upload as-is
    python upload_user_image.py <path> --no-process

Output: prints mmbiz.qpic.cn URLs and saves to <dir>/user_uploaded_urls.json
"""

import json
import os
import sys
import urllib.request
import mimetypes
import uuid
from pathlib import Path
from PIL import Image

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS_DIR)


def get_access_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if "access_token" not in data:
        raise RuntimeError(f"Failed to get access_token: {data}")
    return data["access_token"]


def light_process(file_path, output_path):
    """Light processing: flatten alpha, resize if too wide, convert to RGB."""
    img = Image.open(file_path)

    # Flatten alpha to white
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
        img = bg
    else:
        img = img.convert("RGB")

    # Resize if wider than 1080px
    w, h = img.size
    if w > 1080:
        new_h = int(h * 1080 / w)
        img = img.resize((1080, new_h), Image.LANCZOS)
        print(f"  Resized: {w}x{h} -> 1080x{new_h}")

    img.save(output_path, "PNG")
    return output_path


def upload_image(access_token, file_path):
    """Upload a permanent image. Returns {url, media_id}."""
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex[:16]}"
    file_path = Path(file_path)
    file_bytes = file_path.read_bytes()
    mime_type = "image/png"

    body = []
    body.append(f"--{boundary}".encode("utf-8"))
    body.append(
        b'Content-Disposition: form-data; name="media"; filename="'
        + file_path.name.encode("utf-8")
        + b'"'
    )
    body.append(f"Content-Type: {mime_type}".encode("utf-8"))
    body.append(b"")
    body.append(file_bytes)
    body.append(b"")
    body = b"\r\n".join(body) + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    if "media_id" not in result:
        raise RuntimeError(f"Upload failed: {result}")
    return {"url": result.get("url", ""), "media_id": result["media_id"]}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Upload user images to WeChat")
    parser.add_argument("path", help="Image file or directory")
    parser.add_argument("--no-process", action="store_true", help="Skip light processing")
    parser.add_argument(
        "--config",
        default=os.path.join(SKILL_DIR, "assets", "wechat_config.json"),
        help="Path to wechat_config.json",
    )
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    app_id = config["wechat"]["app_id"]
    app_secret = config["wechat"]["app_secret"]

    print("Getting access_token...")
    token = get_access_token(app_id, app_secret)
    print("  OK")

    # Collect image files
    input_path = Path(args.path)
    valid_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    if input_path.is_file():
        image_files = [input_path]
        output_dir = input_path.parent
    else:
        image_files = sorted(
            f for f in input_path.iterdir() if f.suffix.lower() in valid_exts
        )
        output_dir = input_path

    if not image_files:
        print("No image files found.")
        sys.exit(1)

    # Process and upload
    temp_dir = output_dir / "_user_temp"
    temp_dir.mkdir(exist_ok=True)

    results = {}
    for f in image_files:
        print(f"\nProcessing: {f.name}")
        if args.no_process:
            upload_path = str(f)
        else:
            upload_path = str(temp_dir / f"{f.stem}.png")
            light_process(f, upload_path)

        print(f"  Uploading...")
        try:
            info = upload_image(token, upload_path)
            print(f"  media_id: {info['media_id']}")
            print(f"  url: {info['url'][:80]}...")
            results[f.stem] = info
        except Exception as e:
            print(f"  FAILED: {e}")

    # Cleanup temp
    import shutil

    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    # Save results
    out_path = output_dir / "user_uploaded_urls.json"
    out_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n{'='*50}")
    print(f"Uploaded {len(results)} images")
    print(f"URLs saved to: {out_path}")
    print(f"\nInsert into article.json like this:")
    for key, info in results.items():
        print(f'  {{"type": "image", "src": "{info["url"][:60]}..."}}')


if __name__ == "__main__":
    main()
