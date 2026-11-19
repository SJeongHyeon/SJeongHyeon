"""프로필의 '기술 스택' 그림(라이트/다크 SVG)을 만든다. 글자는 svgtext로 윤곽선으로 바꾼다.

실행: python assets/make_stack.py
넣은 기술은 세 프로젝트에서 실제로 쓴 것만이며 근거는 README의 관계도 근거 표에 있다.
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

import svgtext

W = 800
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
THEMES = {
    "light": {
        "bg": "#ffffff", "bar": "#f6f8fa", "line": "#d0d7de", "text": "#1f2328", "green": "#1a7f37", "muted": "#59636e",
        "purple": ("#EEEDFE", "#534AB7", "#3C3489"),
        "teal": ("#E1F5EE", "#0F6E56", "#085041"),
        "coral": ("#FAECE7", "#993C1D", "#712B13"),
    },
    "dark": {
        "bg": "#0d1117", "bar": "#161b22", "line": "#30363d", "text": "#e6edf3", "green": "#3fb950", "muted": "#8b949e",
        "purple": ("#3C3489", "#AFA9EC", "#CECBF6"),
        "teal": ("#085041", "#5DCAA5", "#9FE1CB"),
        "coral": ("#712B13", "#F0997B", "#F5C4B3"),
    },
}
GROUPS = [
    ("Agent · LLM", "purple", ["LangGraph", "RAG 검색·리랭크", "MCP · n8n", "Whisper · KoELECTRA"]),
    ("Backend · Data", "teal", ["Python", "FastAPI", "PostgreSQL(pgvector)", "Docker"]),
    ("평가 · 품질", "coral", ["자체 평가셋", "Langfuse", "pytest", "GitHub Actions"]),
]
X0, XMAX, GAP, PAD, CH, FS = 36, W - 36, 10, 18, 44, 21


def build(mode: str) -> str:
    t = THEMES[mode]
    body: list[str] = []
    y = 124
    for name, ramp, items in GROUPS:
        fill, stroke, text = t[ramp]
        body.append(f'<circle cx="{X0 + 7}" cy="{y - 7}" r="7" fill="{stroke}"/>')
        body.append(svgtext.path(name, X0 + 24, y, 21, text if mode == "light" else stroke, bold=True, kr_wght=700))
        y += 16
        x = X0
        for it in items:
            w = svgtext.measure(it, FS, bold=True, kr_wght=600) + PAD * 2
            if x + w > XMAX:
                x = X0
                y += CH + GAP
            body.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{CH}" rx="{CH / 2}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            body.append(svgtext.path(it, x + PAD, y + CH / 2 + 7.5, FS, text, bold=True, kr_wght=600))
            x += w + GAP
        y += CH + 34
    H = y - 8
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">',
        "<title>서정현의 기술 스택</title>",
        "<desc>Agent·LLM: LangGraph, RAG 검색·리랭크, MCP·n8n, Whisper·KoELECTRA. Backend·Data: Python, FastAPI, PostgreSQL(pgvector), Docker. 평가·품질: 자체 평가셋, Langfuse, pytest, GitHub Actions.</desc>",
        f'<clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>',
        f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/><rect width="{W}" height="40" fill="{t["bar"]}"/><path d="M0 40.5H{W}" stroke="{t["line"]}"/></g>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>',
        '<circle cx="24" cy="20" r="6" fill="#ff5f57"/><circle cx="44" cy="20" r="6" fill="#febc2e"/><circle cx="64" cy="20" r="6" fill="#28c840"/>',
        f'<text x="{W // 2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{t["muted"]}">SJeongHyeon — ~/stack</text>',
        f'<text x="36" y="84" font-family="{MONO}" font-size="22" font-weight="700" fill="{t["green"]}">$</text>',
        f'<text x="60" y="84" font-family="{MONO}" font-size="22" fill="{t["text"]}">cat stack.txt</text>',
    ]
    svg = "\n".join(head + body + ["</svg>"]) + "\n"
    ET.fromstring(svg)
    return svg


def main() -> None:
    here = Path(__file__).resolve().parent
    for mode in ("light", "dark"):
        p = here / f"stack-{mode}.svg"
        p.write_text(build(mode), encoding="utf-8", newline="\n")
        print("wrote", p.name, p.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
