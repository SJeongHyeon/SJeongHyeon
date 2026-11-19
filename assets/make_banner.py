"""프로필 상단 배너(터미널 창 모양)와 연락처 칩(SVG)을 만든다. 표준 라이브러리만 쓴다.

실행: python assets/make_banner.py
외부 서비스에 기대지 않는 정적 이미지다. 배너는 라이트/다크 두 벌, 칩은 한 벌씩이다.
모바일(폭 375px)에서 0.47배로 줄어도 읽히도록 800x250에 글자를 크게 둔다.
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

W, H = 800, 250
SANS = "'Pretendard','Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "light": {
        "bg": "#ffffff", "bar": "#f6f8fa", "line": "#d0d7de", "text": "#1f2328",
        "green": "#1a7f37", "sub": "#3C3489", "muted": "#59636e",
    },
    "dark": {
        "bg": "#0d1117", "bar": "#161b22", "line": "#30363d", "text": "#e6edf3",
        "green": "#3fb950", "sub": "#AFA9EC", "muted": "#8b949e",
    },
}


def banner(mode: str) -> str:
    t = THEMES[mode]
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">',
            "<title>서정현 | AI Agent Developer</title>",
            "<desc>서정현의 프로필 배너. AI Agent Developer. RAG, 평가, FastAPI.</desc>",
            f'<clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>',
            f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/>'
            f'<rect width="{W}" height="40" fill="{t["bar"]}"/>'
            f'<path d="M0 40.5H{W}" stroke="{t["line"]}"/></g>',
            f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>',
            '<circle cx="24" cy="20" r="6" fill="#ff5f57"/>',
            '<circle cx="44" cy="20" r="6" fill="#febc2e"/>',
            '<circle cx="64" cy="20" r="6" fill="#28c840"/>',
            f'<text x="{W // 2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{t["muted"]}">SJeongHyeon — ~/profile</text>',
            f'<text x="36" y="88" font-family="{MONO}" font-size="22" font-weight="700" fill="{t["green"]}">$</text>',
            f'<text x="60" y="88" font-family="{MONO}" font-size="22" fill="{t["text"]}">whoami</text>',
            f'<text x="36" y="152" font-family="{SANS}" font-size="56" font-weight="700" fill="{t["text"]}">서정현</text>',
            f'<text x="36" y="194" font-family="{SANS}" font-size="28" font-weight="600" fill="{t["sub"]}">AI Agent Developer</text>',
            f'<text x="36" y="228" font-family="{SANS}" font-size="24" fill="{t["muted"]}">RAG · 평가 · FastAPI</text>',
            "</svg>",
        ]
    ) + "\n"
    ET.fromstring(svg)
    return svg


def chip(label: str, fill: str, width: int) -> str:
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28" '
            f'role="img" font-family="{SANS}">',
            f"<title>{label}</title>",
            f'<rect width="{width}" height="28" rx="6" fill="{fill}"/>',
            f'<text x="{width // 2}" y="14" fill="#FFFFFF" font-size="14" font-weight="600" '
            f'text-anchor="middle" dominant-baseline="central">{label}</text>',
            "</svg>",
        ]
    ) + "\n"
    ET.fromstring(svg)
    return svg


def main() -> None:
    here = Path(__file__).resolve().parent
    for mode in ("light", "dark"):
        p = here / f"banner-{mode}.svg"
        p.write_text(banner(mode), encoding="utf-8", newline="\n")
        print("wrote", p.name, p.stat().st_size, "bytes")
    for name, label, fill, width in [
        ("chip-portfolio.svg", "Portfolio ↗", "#24292f", 130),
        ("chip-email.svg", "Email · chvodhkd8525@gmail.com", "#C5221F", 280),
    ]:
        p = here / name
        p.write_text(chip(label, fill, width), encoding="utf-8", newline="\n")
        print("wrote", p.name, p.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
