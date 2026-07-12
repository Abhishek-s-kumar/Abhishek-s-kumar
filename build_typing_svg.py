#!/usr/bin/env python3
"""
build_typing_svg.py
Turn ascii_output.txt into an animated "terminal typing" SVG.
Each line fades/types in, staggered, then a blinking cursor sits at the end.
GitHub renders README <img> SVGs live in-browser, so SMIL animation plays.

Usage: python build_typing_svg.py --in scripts/ascii_output.txt --out assets/ascii_typing.svg
"""
import argparse
import html

CHAR_W = 8.4       # monospace advance width per char at font-size 14
LINE_H = 15
FONT_SIZE = 14
PADDING = 20
LINE_DELAY = 0.12   # seconds between each line starting to appear
TYPE_SPEED = 0.012  # seconds per character within a line


def build_svg(lines: list[str], theme_bg="#0d1117", theme_fg="#39d353") -> str:
    max_len = max((len(l) for l in lines), default=0)
    width = int(max_len * CHAR_W + PADDING * 2)
    height = int(len(lines) * LINE_H + PADDING * 2 + 20)

    body = []
    t_cursor = PADDING
    for i, raw in enumerate(lines):
        line = html.escape(raw) if raw.strip() else " "
        y = PADDING + (i + 1) * LINE_H
        start = round(i * LINE_DELAY, 3)
        dur = round(max(len(raw), 1) * TYPE_SPEED, 3)
        # reveal via clip using a width-animated rect mask, per line
        clip_id = f"clip{i}"
        body.append(f'''
  <clipPath id="{clip_id}">
    <rect x="0" y="{y - LINE_H + 3}" height="{LINE_H}" width="0">
      <animate attributeName="width" from="0" to="{width}" begin="{start}s" dur="{dur}s" fill="freeze" />
    </rect>
  </clipPath>
  <text x="{PADDING}" y="{y}" font-family="monospace" font-size="{FONT_SIZE}"
        fill="{theme_fg}" clip-path="url(#{clip_id})" xml:space="preserve">{line}</text>''')
        t_cursor = start + dur

    cursor_x = PADDING
    cursor_y = PADDING + len(lines) * LINE_H + 14

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" rx="10" fill="{theme_bg}" />
  <g>
    <circle cx="18" cy="16" r="5" fill="#ff5f56" />
    <circle cx="36" cy="16" r="5" fill="#ffbd2e" />
    <circle cx="54" cy="16" r="5" fill="#27c93f" />
  </g>
  <g transform="translate(0,10)">
    {''.join(body)}
  </g>
  <rect x="{cursor_x}" y="{cursor_y - 11}" width="8" height="14" fill="{theme_fg}">
    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1"
              dur="1s" begin="{round(t_cursor,3)}s" repeatCount="indefinite" />
  </rect>
</svg>'''
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", default="scripts/ascii_output.txt")
    ap.add_argument("--out", default="assets/ascii_typing.svg")
    ap.add_argument("--bg", default="#0d1117")
    ap.add_argument("--fg", default="#39d353")
    args = ap.parse_args()

    with open(args.infile) as f:
        lines = f.read().splitlines()

    svg = build_svg(lines, theme_bg=args.bg, theme_fg=args.fg)
    with open(args.out, "w") as f:
        f.write(svg)
    print(f"Wrote SVG -> {args.out} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
