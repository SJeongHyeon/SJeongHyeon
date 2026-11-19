"""프로필 상단 배너와 포트폴리오 칩(SVG)을 만든다. 표준 라이브러리만 쓴다.

실행: python assets/make_banner.py
외부 서비스에 기대지 않는 정적 이미지다. 배너는 라이트/다크 두 벌이고, 칩은 한 벌이다.
모바일(폭 375px)에서 0.47배로 줄어도 읽히도록 800x180에 글자를 크게 둔다.
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

W, H = 800, 180
FONT = "'Pretendard','Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"

THEMES = {
    "light": {"bg": ("#EEEDFE", "#E1F5EE"), "title": "#26215C", "sub": "#3C3489", "muted": "#444441"},
    "dark": {"bg": ("#26215C", "#04342C"), "title": "#F1EFE8", "sub": "#CECBF6", "muted": "#D3D1C7"},
}


def banner(mode: str) -> str:
    t = THEMES[mode]
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" font-family="{FONT}">',
            "<title>서정현 | AI Agent Developer — GitHub 공개 프로필</title>",
            "<desc>서정현의 GitHub 공개 프로필 배너. RAG, 평가, FastAPI.</desc>",
            "<defs>",
            f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg"][0]}"/>'
            f'<stop offset="1" stop-color="{t["bg"][1]}"/></linearGradient>',
            "</defs>",
            f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>',
            f'<text x="40" y="70" fill="{t["title"]}" font-size="48" font-weight="700">서정현</text>',
            f'<text x="40" y="112" fill="{t["sub"]}" font-size="28" font-weight="600">AI Agent Developer</text>',
            f'<text x="40" y="150" fill="{t["muted"]}" font-size="24">GitHub 공개 프로필 · RAG · 평가 · FastAPI</text>',
            "</svg>",
        ]
    ) + "\n"
    ET.fromstring(svg)
    return svg


def chip(label: str, fill: str = "#534AB7", width: int = 140) -> str:
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28" '
            f'role="img" font-family="{FONT}">',
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
    p = here / "chip-portfolio.svg"
    p.write_text(chip("Portfolio ↗"), encoding="utf-8", newline="\n")
    print("wrote", p.name, p.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
