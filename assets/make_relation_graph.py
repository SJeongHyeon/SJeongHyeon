"""프로필의 '프로젝트와 기술의 관계' 그림(라이트/다크 SVG)을 만든다.

직접 그린 관계도다. 아래 데이터가 그림의 전부이고, 선별 근거는 README의 근거 표와
각 저장소의 CONTRIBUTIONS.md에 있다. 표준 라이브러리만 쓴다.

실행: python assets/make_relation_graph.py
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

W, H = 680, 500

# (id, 표시 이름, 색 계열, 선 색, 세로 위치)
PROJECTS = [
    ("p1", "CreditPulse", "purple", "#7F77DD", 150),
    ("p2", "말해봄 Mk.2", "coral", "#D85A30", 260),
    ("p3", "보이스가드", "teal", "#1D9E75", 370),
]
# (id, 표시 이름, 세로 위치, 사용한 프로젝트 id)
TECH = [
    ("t1", "LangGraph", 48, ["p1"]),
    ("t2", "RAG 검색·리랭크", 104, ["p1"]),
    ("t3", "Langfuse", 160, ["p1", "p2"]),
    ("t4", "평가·측정", 216, ["p1", "p2", "p3"]),
    ("t5", "pytest·CI", 272, ["p1", "p2", "p3"]),
    ("t6", "FastAPI", 328, ["p1", "p2", "p3"]),
    ("t7", "MCP·n8n", 384, ["p2"]),
    ("t8", "Whisper·KoELECTRA", 440, ["p3"]),
]
# 같은 기술로 모이는 선이 겹치지 않게 끝점을 살짝 어긋나게 한다.
OFFSET = {"p1": -4, "p2": 0, "p3": 4}

# 채움, 테두리, 글자 (라이트: 50/600/800, 다크: 800/200/100)
PALETTE = {
    "light": {
        "purple": ("#EEEDFE", "#534AB7", "#3C3489"),
        "coral": ("#FAECE7", "#993C1D", "#712B13"),
        "teal": ("#E1F5EE", "#0F6E56", "#085041"),
        "gray": ("#F1EFE8", "#5F5E5A", "#444441"),
        "amber": ("#FAEEDA", "#854F0B", "#633806"),
        "legend": "#5F5E5A",
    },
    "dark": {
        "purple": ("#3C3489", "#AFA9EC", "#CECBF6"),
        "coral": ("#712B13", "#F0997B", "#F5C4B3"),
        "teal": ("#085041", "#5DCAA5", "#9FE1CB"),
        "gray": ("#444441", "#B4B2A9", "#D3D1C7"),
        "amber": ("#633806", "#EF9F27", "#FAC775"),
        "legend": "#B4B2A9",
    },
}
FONT = "'Pretendard','Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"


def build(mode: str) -> str:
    pal = PALETTE[mode]
    py = {p[0]: p[4] for p in PROJECTS}
    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" font-family="{FONT}">'
    )
    out.append("<title>서정현의 프로젝트와 기술 관계도</title>")
    out.append(
        "<desc>서정현에서 CreditPulse, 말해봄 Mk.2, 보이스가드로 선이 이어지고, 각 프로젝트에서 사용한 "
        "기술로 프로젝트 색의 곡선이 이어진다. 평가·측정, pytest·CI, FastAPI는 세 프로젝트가 함께 쓰고 "
        "Langfuse는 두 프로젝트가 쓴다.</desc>"
    )
    # 선
    out.append('<g fill="none" stroke-width="1.8" stroke-linecap="round">')
    for pid, _, _, _, y in PROJECTS:
        out.append(
            f'<path d="M100,260 C125,260 125,{y} 150,{y}" stroke="#888780" opacity="0.5"/>'
        )
    for tid, _, ty, users in TECH:
        for pid, _, _, color, y in PROJECTS:
            if pid in users:
                e = ty + OFFSET[pid]
                out.append(
                    f'<path d="M278,{y} C372,{y} 372,{e} 466,{e}" stroke="{color}" opacity="0.9"/>'
                )
    out.append("</g>")

    def text(x, y, s, fill, size=14, weight=400):
        return (
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="middle" dominant-baseline="central">{s}</text>'
        )

    # 나
    f, s, t = pal["gray"]
    out.append(f'<circle cx="64" cy="260" r="36" fill="{f}" stroke="{s}" stroke-width="0.8"/>')
    out.append(text(64, 260, "서정현", t, 14, 500))
    # 프로젝트
    for pid, name, ramp, _, y in PROJECTS:
        f, s, t = pal[ramp]
        out.append(
            f'<rect x="150" y="{y - 25}" width="128" height="50" rx="10" fill="{f}" stroke="{s}" stroke-width="0.8"/>'
        )
        out.append(text(214, y, name, t, 14, 500))
    # 기술
    for tid, name, ty, users in TECH:
        shared = len(users) >= 2
        f, s, t = pal["amber" if shared else "gray"]
        out.append(
            f'<rect x="466" y="{ty - 17}" width="174" height="34" rx="17" fill="{f}" stroke="{s}" stroke-width="0.8"/>'
        )
        if shared:
            out.append(text(540, ty, name, t, 14, 500))
            out.append(f'<circle cx="618" cy="{ty}" r="10" fill="#FAC775" stroke="#854F0B" stroke-width="0.8"/>')
            out.append(text(618, ty, str(len(users)), "#412402", 12, 500))
        else:
            out.append(text(553, ty, name, t, 14, 400))
    # 범례
    out.append(
        f'<text x="40" y="486" fill="{pal["legend"]}" font-size="12" dominant-baseline="central">'
        "선 색 = 프로젝트 · 노란 기술 = 둘 이상 프로젝트에서 사용 · 숫자 = 사용한 프로젝트 수</text>"
    )
    out.append("</svg>")
    svg = "\n".join(out) + "\n"
    ET.fromstring(svg)  # 올바른 XML인지 확인한다
    return svg


def main() -> None:
    here = Path(__file__).resolve().parent
    for mode in ("light", "dark"):
        path = here / f"relation-graph-{mode}.svg"
        path.write_text(build(mode), encoding="utf-8", newline="\n")
        print("wrote", path.name, path.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
