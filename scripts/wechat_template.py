# -*- coding: utf-8 -*-
"""
WeChat Official Account Article Template Generator
Based on fresh minimalist article style - minimal, clean, reading-focused.

Key style traits:
- Font: Optima-Regular, PingFangSC-light
- letter-spacing: 2px, word-spacing: 2px
- line-height: 32px (generous)
- Paragraph margin: 30px 8px (big vertical spacing)
- No text-indent
- Emphasis via colored bold <strong>
- Quote blocks: light bg + left border + radius
- Images: rounded + shadow, centered
- Opening tag: colored background, centered
"""

import json
import os


class WeChatTemplate:
    """Generate WeChat-compatible HTML matching fresh minimalist style."""

    def __init__(self, config_path=None, theme=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "wechat_config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        if theme:
            self.set_theme(theme)
        self.c = self.config["colors"]
        self.f = self.config["fonts"]

    def set_theme(self, theme_name):
        presets = self.config.get("presets", {})
        if theme_name in presets:
            self.config["colors"].update(presets[theme_name])
            self.config["theme"] = theme_name

    # ---- Common style strings ----

    @property
    def _p_style(self):
        return (
            f"margin: 30px 8px; "
            f"font-family: {self.f['family']}; "
            f"letter-spacing: {self.f['letter_spacing']}; "
            f"word-spacing: {self.f['word_spacing']}; "
            f"line-height: {self.f['line_height']}; "
            f"font-size: {self.f['size_body']};"
        )

    @property
    def _p_style_justify(self):
        return self._p_style + " text-align: justify;"

    # ---- Component generators ----

    def page_open(self):
        return (
            f'<section style="color: {self.c["text_main"]}; '
            f'font-family: {self.f["family"]}; '
            f'letter-spacing: 1.5px; '
            f'padding: 8px; '
            f'font-size: {self.f["size_base"]};">'
        )

    def page_close(self):
        return "</section>"

    def opening_tag(self, text=None):
        if text is None:
            text = self.config.get("author_tag", "原创")
        return (
            f'<center><span style="background:{self.c["tag_bg"]};">'
            f'<span leaf="">{text}</span></span></center>'
        )

    def section_title(self, text):
        return (
            f'<p style="margin: 40px 8px 20px 8px; '
            f'font-family: {self.f["family"]}; '
            f'letter-spacing: {self.f["letter_spacing"]}; '
            f'line-height: {self.f["line_height"]}; '
            f'font-size: {self.f["size_h2"]}; '
            f'font-weight: bold; '
            f'color: {self.c["primary"]};">{text}</p>'
        )

    def paragraph(self, text, align="justify"):
        style = self._p_style_justify if align == "justify" else self._p_style
        return f'<p style="{style}"><span leaf="">{text}</span></p>'

    def body_block(self, paragraphs):
        inner = "\n".join(self.paragraph(p) for p in paragraphs)
        return inner

    def highlight(self, text, emoji=""):
        prefix = f"{emoji} " if emoji else ""
        return (
            f'<section style="margin: 20px 0px; padding: 10px 20px; '
            f'background-color: {self.c["quote_bg"]}; '
            f'border-left: 4px solid {self.c["quote_border"]}; '
            f'color: rgb(44, 62, 80); '
            f'font-size: {self.f["size_body"]}; '
            f'line-height: 1.6; '
            f'border-radius: 4px;">'
            f'<p style="margin: 0px; font-family: {self.f["family"]}; '
            f'letter-spacing: {self.f["letter_spacing"]}; '
            f'word-spacing: {self.f["word_spacing"]}; '
            f'line-height: {self.f["line_height"]}; '
            f'font-size: {self.f["size_body"]}; padding: 0px;">'
            f'{prefix}{text}</p></section>'
        )

    def steps_block(self, steps):
        parts = []
        for s in steps:
            title = s["title"]
            text = s.get("text", "")
            line = (
                f'<strong style="color: {self.c["primary"]}; font-weight: bold;">'
                f'{title}</strong>：{text}'
            )
            parts.append(self.paragraph(line))
        return "\n".join(parts)

    def numbered_block(self, items):
        parts = []
        circled_nums = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"]
        for i, item in enumerate(items):
            num = circled_nums[i] if i < len(circled_nums) else f"{i+1}."
            title = item["title"]
            text = item.get("text", "")
            line = (
                f'<strong style="color: {self.c["primary"]}; font-weight: bold;">'
                f'{num} {title}</strong><br/>{text}'
            )
            parts.append(self.paragraph(line))
        return "\n".join(parts)

    def table(self, headers, rows):
        head_cells = "".join(
            f'<th style="padding:10px 8px; font-weight:600;">{h}</th>'
            for h in headers
        )
        head = (
            f'<tr style="background:{self.c["primary"]}; color:{self.c["text_white"]};">'
            f"{head_cells}</tr>"
        )
        body_rows = ""
        for i, row in enumerate(rows):
            cells = ""
            for j, cell in enumerate(row):
                is_first = j == 0
                color = (
                    self.c["primary"]
                    if is_first
                    else (self.c["primary"] if cell.get("bold") else self.c["text_body"])
                )
                weight = "bold" if is_first or cell.get("bold") else "normal"
                cells += (
                    f'<td style="padding:9px 8px; '
                    f'color:{color}; font-weight:{weight};">{cell["text"]}</td>'
                )
            body_rows += f"<tr>{cells}</tr>"
        return (
            f'<section style="margin: 24px 8px;">'
            f'<table style="width:100%; border-collapse:collapse; '
            f'font-size:14px; text-align:center;">{head}{body_rows}</table>'
            f"</section>"
        )

    def image(self, src):
        return (
            f'<p style="text-align: center; margin: 20px 0px 30px; '
            f'padding: 0px; font-size: 0px;">'
            f'<img src="{src}" data-src="{src}" data-w="1080" '
            f'style="width: 100%; max-width: 1080px; height: auto; '
            f'border-radius: 6px; vertical-align: middle;" />'
            f'</p>'
        )

    def divider(self):
        return (
            f'<section style="margin: 30px 8px; '
            f'border-top: 1px dashed {self.c["text_muted"]};"></section>'
        )

    def ending_block(self, title, paragraphs):
        parts = [
            f'<p style="margin: 40px 8px 10px 8px; '
            f'font-family: {self.f["family"]}; '
            f'letter-spacing: {self.f["letter_spacing"]}; '
            f'line-height: {self.f["line_height"]}; '
            f'font-size: {self.f["size_body"]}; '
            f'font-weight: bold; '
            f'color: {self.c["primary"]};">{title}</p>'
        ]
        for p in paragraphs:
            parts.append(
                f'<p style="{self._p_style}"><span leaf="">{p}</span></p>'
            )
        return "\n".join(parts)

    def footer(self):
        footer_text = self.config.get("footer_text", "")
        return (
            f'<p style="margin: 30px 8px; text-align: center; '
            f'color: {self.c["text_muted"]}; '
            f'font-size: {self.f["size_small"]}; '
            f'font-family: {self.f["family"]};">{footer_text}</p>'
        )

    # ---- Full article renderer ----

    def render(self, article):
        """
        Render a full article from structured data.

        Supported section types:
            opening  - Top tag           {"type":"opening", "text":"..."}
            title    - Section header    {"type":"title", "text":"..."}
            body     - Paragraphs        {"type":"body", "paragraphs":["...", ...]}
            highlight- Quote block        {"type":"highlight", "text":"...", "emoji":"..."}
            steps    - Simple paragraphs  {"type":"steps", "items":[{"title":"...","text":"..."}]}
            numbered - Numbered paras     {"type":"numbered", "items":[{"title":"...","text":"..."}]}
            table    - Simple table       {"type":"table", "headers":[...], "rows":[[{"text":"..."}, ...]]}
            image    - Inline image       {"type":"image", "src":"url"}
            divider  - Dashed line        {"type":"divider"}
            ending   - Ending section     {"type":"ending", "title":"...", "paragraphs":["...", ...]}
        """
        parts = [self.page_open()]

        opening_text = article.get("opening_text")
        parts.append(self.opening_tag(opening_text))

        for section in article.get("sections", []):
            stype = section["type"]
            if stype == "title":
                parts.append(self.section_title(section["text"]))
            elif stype == "body":
                parts.append(self.body_block(section["paragraphs"]))
            elif stype == "highlight":
                parts.append(self.highlight(section["text"], section.get("emoji", "")))
            elif stype == "steps":
                parts.append(self.steps_block(section["items"]))
            elif stype == "numbered":
                parts.append(self.numbered_block(section["items"]))
            elif stype == "table":
                parts.append(self.table(section["headers"], section["rows"]))
            elif stype == "image":
                parts.append(self.image(section["src"]))
            elif stype == "divider":
                parts.append(self.divider())
            elif stype == "ending":
                parts.append(self.ending_block(section["title"], section["paragraphs"]))

        parts.append(self.footer())
        parts.append(self.page_close())
        return "\n".join(parts)


if __name__ == "__main__":
    tpl = WeChatTemplate(theme="blue")

    sample = {
        "opening_text": "这是第 1 篇原创！",
        "sections": [
            {"type": "title", "text": "一、这是一个标题"},
            {"type": "body", "paragraphs": [
                "这是第一段正文内容，用于演示模版效果。字间距和行距都很宽松，阅读感很好。",
                "这是第二段正文内容，包含<strong style='color:#165dff;'>高亮文字</strong>。"
            ]},
            {"type": "highlight", "text": "这是一个引用块，浅蓝背景加左边框。"},
            {"type": "image", "src": "https://mmbiz.qpic.cn/test.png"},
            {"type": "ending", "title": "最后说一句", "paragraphs": [
                "这是结尾内容。"
            ]}
        ]
    }

    html = tpl.render(sample)
    with open("template_preview.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Preview written to template_preview.html")
