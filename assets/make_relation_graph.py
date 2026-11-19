"""프로필의 '프로젝트와 기술의 관계' 그림(라이트/다크 SVG, 세로형)을 만든다.

직접 그린 관계도다. 아래 데이터가 그림의 전부이고, 선별 근거는 README의 근거 표와
각 저장소의 CONTRIBUTIONS.md에 있다. 표준 라이브러리만 쓴다.

실행: python assets/make_relation_graph.py
선 모양: 실선 = 근거 확인, 점선 = 검증이거나 공개 사본에서 실행한 기록이 없음.
모바일(폭 375px)에서 0.89배라 글자 16px이 약 14px로 보이도록 420x620에 그린다.
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

W, H = 420, 620

# (id, 표시 이름, 색 계열, 선 색, 세로 위치)
PROJECTS = [
    ("p1", "CreditPulse", "purple", "#7F77DD", 150),
    ("p2", "말해봄 Mk.2", "coral", "#D85A30", 310),
    ("p3", "보이스가드", "teal", "#1D9E75", 470),
]
# (id, 표시 이름, 세로 위치)
TECH = [
    ("t1", "LangGraph", 48),
    ("t2", "RAG 검색·리랭크", 110),
    ("t3", "Langfuse", 172),
    ("t4", "평가·측정", 234),
    ("t5", "pytest", 296),
    ("t6", "CI(Actions)", 358),
    ("t7", "FastAPI", 420),
    ("t8", "MCP·n8n", 482),
    ("t9", "Whisper·KoELECTRA", 544),
]
# (프로젝트, 기술, 선 모양)
EDGES = [
    ("p1", "t1", "solid"), ("p1", "t2", "solid"), ("p1", "t3", "solid"), ("p1", "t4", "solid"),
    ("p1", "t5", "solid"), ("p1", "t6", "solid"), ("p1", "t7", "solid"),
    ("p2", "t3", "solid"), ("p2", "t4", "solid"), ("p2", "t5", "solid"), ("p2", "t6", "solid"),
    ("p2", "t7", "dashed"), ("p2", "t8", "solid"),
    ("p3", "t4", "solid"), ("p3", "t5", "solid"), ("p3", "t7", "solid"), ("p3", "t9", "solid"),
]
OFFSET = {"p1": -5, "p2": 0, "p3": 5}

PALETTE = {
    "light": {
        "purple": ("#EEEDFE", "#534AB7", "#3C3489"),
        "coral": ("#FAECE7", "#993C1D", "#712B13"),
        "teal": ("#E1F5EE", "#0F6E56", "#085041"),
        "gray": ("#F1EFE8", "#5F5E5A", "#444441"),
        "amber": ("#FAEEDA", "#854F0B", "#633806"),
        "legend": "#444441",
    },
    "dark": {
        "purple": ("#3C3489", "#AFA9EC", "#CECBF6"),
        "coral": ("#712B13", "#F0997B", "#F5C4B3"),
        "teal": ("#085041", "#5DCAA5", "#9FE1CB"),
        "gray": ("#444441", "#B4B2A9", "#D3D1C7"),
        "amber": ("#633806", "#EF9F27", "#FAC775"),
        "legend": "#D3D1C7",
    },
}
FONT = "'Pretendard','Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"
PX, PW, PH = 14, 112, 54  # 프로젝트 칸
TX, TW, TH = 250, 156, 34  # 기술 칸


def build(mode: str) -> str:
    pal = PALETTE[mode]
    py = {p[0]: p[4] for p in PROJECTS}
    pcolor = {p[0]: p[3] for p in PROJECTS}
    ty = {t[0]: t[2] for t in TECH}
    users: dict[str, set[str]] = {}
    for p, t, _ in EDGES:
        users.setdefault(t, set()).add(p)

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" font-family="{FONT}">',
        "<title>서정현의 프로젝트와 기술 관계도</title>",
        "<desc>CreditPulse, 말해봄 Mk.2, 보이스가드에서 쓴 기술을 프로젝트 색의 곡선으로 이은 관계도. "
        "실선은 근거가 확인된 관계이고 점선은 검증이거나 공개 사본에서 실행한 기록이 없는 관계다. "
        "평가·측정, pytest, FastAPI는 세 프로젝트가 함께 쓴다.</desc>",
        '<g fill="none" stroke-width="2" stroke-linecap="round">',
    ]
    for p, t, style in EDGES:
        y1 = py[p]
        y2 = ty[t] + OFFSET[p]
        dash = ' stroke-dasharray="7 5"' if style == "dashed" else ""
        o.append(
            f'<path d="M{PX + PW},{y1} C{PX + PW + 62},{y1} {TX - 62},{y2} {TX},{y2}" '
            f'stroke="{pcolor[p]}" opacity="0.9"{dash}/>'
        )
    o.append("</g>")

    def text(x, y, s, fill, size=16, weight=400):
        return (
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="middle" dominant-baseline="central">{s}</text>'
        )

    for pid, name, ramp, _, y in PROJECTS:
        f, s, t = pal[ramp]
        o.append(
            f'<rect x="{PX}" y="{y - PH // 2}" width="{PW}" height="{PH}" rx="10" fill="{f}" stroke="{s}" stroke-width="1"/>'
        )
        o.append(text(PX + PW // 2, y, name, t, 16, 600))
    for tid, name, y in TECH:
        n = len(users.get(tid, ()))
        shared = n >= 2
        f, s, t = pal["amber" if shared else "gray"]
        o.append(
            f'<rect x="{TX}" y="{y - TH // 2}" width="{TW}" height="{TH}" rx="17" fill="{f}" stroke="{s}" stroke-width="1"/>'
        )
        if shared:
            o.append(text(TX + 62, y, name, t, 16, 600))
            o.append(f'<circle cx="{TX + TW - 18}" cy="{y}" r="11" fill="#FAC775" stroke="#854F0B" stroke-width="1"/>')
            o.append(text(TX + TW - 18, y, str(n), "#412402", 14, 600))
        else:
            o.append(text(TX + TW // 2, y, name, t, 16, 400))
    # 범례
    lg = pal["legend"]
    for i, line in enumerate(
        ["선 색 = 프로젝트 · 노란 칸 = 둘 이상 프로젝트(숫자)", "실선 = 근거 확인 · 점선 = 검증·미실행"]
    ):
        o.append(f'<text x="14" y="{588 + i * 22}" fill="{lg}" font-size="14" dominant-baseline="central">{line}</text>')
    o.append("</svg>")
    svg = "\n".join(o) + "\n"
    ET.fromstring(svg)
    return svg


def main() -> None:
    here = Path(__file__).resolve().parent
    for mode in ("light", "dark"):
        p = here / f"relation-graph-{mode}.svg"
        p.write_text(build(mode), encoding="utf-8", newline="\n")
        print("wrote", p.name, p.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
