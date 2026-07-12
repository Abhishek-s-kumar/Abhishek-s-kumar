#!/usr/bin/env python3
"""
build_neofetch_svg.py
Static neofetch-style panel: small ASCII glyph on left, key:value stats on right.
Edit the DATA dict below, then rerun. No external deps beyond stdlib.

Usage: python build_neofetch_svg.py --out assets/neofetch.svg
"""
import argparse
import html

GLYPH = [
    "      /\\_/\\  ",
    "     ( o.o ) ",
    "      > ^ <  ",
]

DATA = [
    ("user", "abhishek@github"),
    ("-----", "----------------"),
    ("Role", "Cybersecurity Engineer"),
    ("Stack", "Python, Java, Kotlin, C++"),
    ("Focus", "Secure systems, RE, automation"),
    ("Tools", "Burp Suite, Wireshark, Metasploit"),
    ("Projects", "5 (see pinned repos)"),
    ("Status", "Open to collab"),
]

FONT_SIZE = 14
LINE_H = 20
PADDING = 20
GLYPH_COL_W = 200


def build_svg(bg="#0d1117", accent="#39d353", fg="#c9d1d9") -> str:
    rows = max(len(GLYPH), len(DATA))
    height = PADDING * 2 + rows * LINE_H
    width = GLYPH_COL_W + 340

    glyph_lines = "".join(
        f'<text x="{PADDING}" y="{PADDING + (i+1)*LINE_H}" font-family="monospace" '
        f'font-size="{FONT_SIZE}" fill="{accent}" xml:space="preserve">{html.escape(g)}</text>\n'
        for i, g in enumerate(GLYPH)
    )

    data_lines = ""
    for i, (k, v) in enumerate(DATA):
        y = PADDING + (i + 1) * LINE_H
        key_color = accent if not k.startswith("-") else fg
        data_lines += (
            f'<text x="{GLYPH_COL_W}" y="{y}" font-family="monospace" font-size="{FONT_SIZE}" '
            f'fill="{key_color}" xml:space="preserve">{html.escape(k)}</text>\n'
            f'<text x="{GLYPH_COL_W + 110}" y="{y}" font-family="monospace" font-size="{FONT_SIZE}" '
            f'fill="{fg}" xml:space="preserve">{html.escape(v)}</text>\n'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" rx="10" fill="{bg}" />
  {glyph_lines}
  {data_lines}
</svg>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="assets/neofetch.svg")
    args = ap.parse_args()
    svg = build_svg()
    with open(args.out, "w") as f:
        f.write(svg)
    print(f"Wrote -> {args.out}")


if __name__ == "__main__":
    main()
