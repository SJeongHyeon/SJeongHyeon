"""프로필 상단 배너(라이트/다크 SVG)를 만든다. 표준 라이브러리만 쓴다.

실행: python assets/make_banner.py
외부 서비스에 기대지 않는 정적 이미지이며, 오른쪽 그림은 관계도와 같은 모양의 장식이다.
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

W, H = 1200, 260
FONT = "'Pretendard','Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"

THEMES = {
    "light": {
        "bg": ("#EEEDFE", "#E1F5EE"),
        "title": "#26215C",
        "sub": "#3C3489",
        "muted": "#5F5E5A",
        "tech": "#B4B2A9",
        "me": ("#F1EFE8", "#5F5E5A"),
    },
    "dark": {
        "bg": ("#26215C", "#04342C"),
        "title": "#F1EFE8",
        "sub": "#CECBF6",
        "muted": "#B4B2A9",
        "tech": "#5F5E5A",
        "me": ("#444441", "#D3D1C7"),
    },
}
PROJ = [("#7F77DD", 70), ("#D85A30", 130), ("#1D9E75", 190)]
TECH_Y = [44, 87, 130, 173, 216]
# 프로젝트 → 기술 연결(장식)
LINKS = {0: [0, 1, 2, 3], 1: [2, 3, 4], 2: [3, 4]}
SHARED = {2, 3, 4}  # 노란색으로 보이는 공통 기술 위치


def build(mode: str) -> str:
    t = THEMES[mode]
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" font-family="{FONT}">',
        "<title>서정현 | AI Agent Developer — GitHub 공개 프로필</title>",
        "<desc>서정현의 GitHub 공개 프로필 배너. RAG, 평가, FastAPI. 오른쪽은 프로젝트와 기술의 관계를 나타낸 장식 그림이다.</desc>",
        "<defs>",
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg"][0]}"/>'
        f'<stop offset="1" stop-color="{t["bg"][1]}"/></linearGradient>',
        "</defs>",
        f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>',
        # 글
        f'<text x="64" y="92" fill="{t["title"]}" font-size="46" font-weight="700">서정현</text>',
        f'<text x="64" y="140" fill="{t["sub"]}" font-size="26" font-weight="600">AI Agent Developer</text>',
        f'<text x="64" y="178" fill="{t["muted"]}" font-size="19">RAG · 평가 · FastAPI</text>',
        f'<text x="64" y="222" fill="{t["muted"]}" font-size="15" opacity="0.85">GitHub public profile · github.com/SJeongHyeon</text>',
    ]
    # 장식 그림(관계도 축소판)
    me_f, me_s = t["me"]
    mx, my = 740, 130
    px, tx = 900, 1080
    o.append('<g fill="none" stroke-width="2" stroke-linecap="round">')
    for i, (c, py) in enumerate(PROJ):
        o.append(f'<path d="M{mx + 16},{my} C{mx + 60},{my} {px - 60},{py} {px - 14},{py}" stroke="#888780" opacity="0.5"/>')
    for i, (c, py) in enumerate(PROJ):
        for j in LINKS[i]:
            ty = TECH_Y[j]
            o.append(f'<path d="M{px + 14},{py} C{px + 90},{py} {tx - 90},{ty} {tx - 9},{ty}" stroke="{c}" opacity="0.85"/>')
    o.append("</g>")
    o.append(f'<circle cx="{mx}" cy="{my}" r="16" fill="{me_f}" stroke="{me_s}" stroke-width="1.5"/>')
    for c, py in PROJ:
        o.append(f'<circle cx="{px}" cy="{py}" r="14" fill="{c}"/>')
    for j, ty in enumerate(TECH_Y):
        fill = "#EF9F27" if j in SHARED else t["tech"]
        o.append(f'<circle cx="{tx}" cy="{ty}" r="9" fill="{fill}"/>')
    o.append("</svg>")
    svg = "\n".join(o) + "\n"
    ET.fromstring(svg)
    return svg


def main() -> None:
    here = Path(__file__).resolve().parent
    for mode in ("light", "dark"):
        p = here / f"banner-{mode}.svg"
        p.write_text(build(mode), encoding="utf-8", newline="\n")
        print("wrote", p.name, p.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
