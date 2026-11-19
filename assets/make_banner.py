"""프로필 상단 배너(터미널 창 모양)와 연락처 칩(SVG)을 만든다. 글자는 svgtext로 윤곽선으로 바꿔 기기와 상관없이 같게 보인다.

실행: python assets/make_banner.py
외부 서비스에 기대지 않는 정적 이미지다. 배너는 라이트/다크 두 벌, 칩은 한 벌씩이다.
모바일(폭 375px)에서 0.47배로 줄어도 읽히도록 800x250에 글자를 크게 둔다.
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

import svgtext

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
            svgtext.path("서정현", 34, 150, 54, t["text"], bold=True, kr_wght=700),
            svgtext.path("AI Agent Developer", 36, 192, 27, t["sub"], bold=True, kr_wght=700),
            svgtext.path("RAG · 평가 · FastAPI", 36, 227, 23, t["muted"], bold=False, kr_wght=400),
            "</svg>",
        ]
    ) + "\n"
    ET.fromstring(svg)
    return svg


ICONS = {
    # 14x14 안에 흰색으로 그린 아이콘
    "mail": '<rect x="0.8" y="2.5" width="12.4" height="9" rx="1.5" fill="none" stroke="#fff" stroke-width="1.6"/>'
            '<path d="M1.5 3.8L7 8L12.5 3.8" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/>',
    "triangle": '<path d="M7 1.5L13.2 12.3H0.8Z" fill="#fff"/>',
}


def badge(label: str, value: str, icon: str, right_fill: str, left_fill: str = "#555555") -> str:
    """왼쪽(아이콘+이름)과 오른쪽(값)이 색으로 나뉜 두 칸짜리 배지."""
    size, pad, gap, icon_w, h = 14, 10, 6, 14, 28
    lw = pad + icon_w + gap + svgtext.measure(label, size, bold=True, kr_wght=700) + pad
    rw = pad + svgtext.measure(value, size, bold=True, kr_wght=700) + pad
    w = lw + rw
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" viewBox="0 0 {w:.1f} {h}" role="img">',
            f"<title>{label}: {value}</title>",
            f'<clipPath id="r"><rect width="{w:.1f}" height="{h}" rx="4"/></clipPath>',
            f'<g clip-path="url(#r)"><rect width="{lw:.1f}" height="{h}" fill="{left_fill}"/>'
            f'<rect x="{lw:.1f}" width="{rw:.1f}" height="{h}" fill="{right_fill}"/></g>',
            f'<g transform="translate({pad},7)">{ICONS[icon]}</g>',
            svgtext.path(label, pad + icon_w + gap, 19, size, "#FFFFFF", bold=True, kr_wght=700),
            svgtext.path(value, lw + pad, 19, size, "#FFFFFF", bold=True, kr_wght=700),
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
    for name, svg in [
        ("badge-email.svg", badge("Email", "chvodhkd8525@gmail.com", "mail", "#EA4335")),
        ("badge-portfolio.svg", badge("Portfolio", "ai-agent-portfolio-theta.vercel.app", "triangle", "#111111")),
    ]:
        p = here / name
        p.write_text(svg, encoding="utf-8", newline="\n")
        print("wrote", p.name, p.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
