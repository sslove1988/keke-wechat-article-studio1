# -*- coding: utf-8 -*-
"""
Image post-processor for AI-generated illustrations.

Pipeline:
1. Gray background -> pure white (also erases semi-transparent watermarks on gray areas)
2. Remove "图片由AI生成" watermark: crop bottom 38px strip
3. Auto-crop to content bounding box (remove excess whitespace)
4. Re-pad with 6% balanced margins on all sides
5. Resize to 1080px wide

Usage:
    python process_images.py <input_dir> [--output <output_dir>] [--watermark-px <N>]

Input dir should contain .png files (from ImageGen).
Output dir defaults to <input_dir>/clean/.
Processed files are named clean_<original_name>.
"""

from PIL import Image
import numpy as np
import os
import argparse


WATERMARK_CROP_PX = 38


def process_image(img_path, output_path, watermark_px=WATERMARK_CROP_PX):
    """Process a single image: clean bg, remove watermark, auto-crop, re-pad, resize."""
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img)
    h, w = arr.shape[:2]

    # --- Step 1: Detect background color from 4 corners ---
    corner_size = 15
    corners = []
    for cs in [(0, 0), (0, w - corner_size), (h - corner_size, 0), (h - corner_size, w - corner_size)]:
        region = arr[cs[0]:cs[0] + corner_size, cs[1]:cs[1] + corner_size, :]
        corners.append(np.median(region.reshape(-1, 3), axis=0))
    bg_color = np.median(corners, axis=0).astype(int)

    # --- Step 2: Replace background pixels (within tolerance) with white ---
    tolerance = 28
    diff = np.abs(arr.astype(float) - bg_color.astype(float))
    bg_mask = np.all(diff < tolerance, axis=2)
    arr[bg_mask] = [255, 255, 255]

    # --- Step 3: Remove gray pixels (low saturation, high brightness) ---
    r, g, b = arr[:, :, 0].astype(float), arr[:, :, 1].astype(float), arr[:, :, 2].astype(float)
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    saturation = max_c - min_c
    brightness = (r + g + b) / 3
    gray_mask = (saturation < 30) & (brightness > 175) & (brightness < 252)
    arr[gray_mask] = [255, 255, 255]

    # --- Step 4: Crop watermark strip from bottom ---
    arr_clean = arr[:h - watermark_px, :, :]

    # --- Step 5: Auto-crop to content bounding box ---
    non_white = np.any(arr_clean < 240, axis=2)
    rows = np.any(non_white, axis=1)
    cols = np.any(non_white, axis=0)

    if not rows.any() or not cols.any():
        result = Image.fromarray(arr_clean)
        result.save(output_path)
        return

    content_top = np.argmax(rows)
    content_bottom = len(rows) - 1 - np.argmax(rows[::-1])
    content_left = np.argmax(cols)
    content_right = len(cols) - 1 - np.argmax(cols[::-1])

    margin = 5
    content_top = max(0, content_top - margin)
    content_bottom = min(arr_clean.shape[0] - 1, content_bottom + margin)
    content_left = max(0, content_left - margin)
    content_right = min(arr_clean.shape[1] - 1, content_right + margin)

    cropped = arr_clean[content_top:content_bottom + 1, content_left:content_right + 1, :]
    ch, cw = cropped.shape[:2]

    # --- Step 6: Re-pad with balanced margins ---
    pad_ratio = 0.06
    pad_v = int(ch * pad_ratio)
    pad_h = int(cw * pad_ratio)

    new_h = ch + 2 * pad_v
    new_w = cw + 2 * pad_h
    padded = np.ones((new_h, new_w, 3), dtype=np.uint8) * 255
    padded[pad_v:pad_v + ch, pad_h:pad_h + cw, :] = cropped

    # --- Step 7: Resize to 1080px wide ---
    target_w = 1080
    scale = target_w / new_w
    target_h = int(new_h * scale)

    result = Image.fromarray(padded)
    result = result.resize((target_w, target_h), Image.LANCZOS)
    result.save(output_path)

    print(f"  {os.path.basename(img_path)}: {w}x{h} -> {target_w}x{target_h} (balanced padding, no watermark)")


def process_directory(input_dir, output_dir=None, watermark_px=WATERMARK_CROP_PX):
    """Process all .png files in a directory."""
    if output_dir is None:
        output_dir = os.path.join(input_dir, "clean")
    os.makedirs(output_dir, exist_ok=True)

    processed = []
    for f in sorted(os.listdir(input_dir)):
        if f.endswith(".png") and not f.startswith("clean_"):
            input_path = os.path.join(input_dir, f)
            output_path = os.path.join(output_dir, f"clean_{f}")
            print(f"Processing: {f}")
            process_image(input_path, output_path, watermark_px)
            processed.append(output_path)

    return processed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process AI-generated illustrations for WeChat")
    parser.add_argument("input_dir", help="Directory containing original .png images")
    parser.add_argument("--output", "-o", default=None, help="Output directory (default: <input>/clean/)")
    parser.add_argument("--watermark-px", type=int, default=38, help="Pixels to crop from bottom for watermark removal")
    args = parser.parse_args()

    processed = process_directory(args.input_dir, args.output, args.watermark_px)
    print(f"\nProcessed {len(processed)} images to {args.output or os.path.join(args.input_dir, 'clean')}")
