"""글자를 SVG 경로(윤곽선)로 바꾸는 도우미. fontTools가 필요하다(pip install fonttools).

SVG 안의 <text>는 보는 사람의 기기에 있는 글꼴로 그려져서 기기마다 모양이 달라진다.
윤곽선으로 바꿔 두면 어떤 기기에서도 같은 모양으로 보이고, 글자 폭을 재서 칸 크기도 정확히 맞출 수 있다.
글꼴: Noto Sans(영문·숫자)와 Noto Sans KR(한글), 둘 다 SIL Open Font License 1.1.
Windows에서는 C:/Windows/Fonts에 있고, 다른 곳에서는 FONT_DIR 환경 변수로 폴더를 알려 준다.
"""
from __future__ import annotations

import os
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path(os.environ.get("FONT_DIR", "C:/Windows/Fonts"))


class Face:
    def __init__(self, file: str, wght: int | None = None):
        self.font = TTFont(str(FONT_DIR / file))
        self.loc = {"wght": wght} if wght else None
        self.gs = self.font.getGlyphSet(location=self.loc) if self.loc else self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upm = self.font["head"].unitsPerEm

    def has(self, ch: str) -> bool:
        return ord(ch) in self.cmap

    def glyph(self, ch: str):
        return self.gs[self.cmap[ord(ch)]]


_cache: dict[tuple[str, int | None], Face] = {}


def face(file: str, wght: int | None = None) -> Face:
    key = (file, wght)
    if key not in _cache:
        _cache[key] = Face(file, wght)
    return _cache[key]


def _pick(ch: str, bold: bool, kr_wght: int) -> Face:
    latin = face("NotoSans-Bold.ttf" if bold else "NotoSans-Regular.ttf")
    kr = face("NotoSansKR-VF.ttf", kr_wght)
    code = ord(ch)
    hangul = 0xAC00 <= code <= 0xD7AF or 0x1100 <= code <= 0x11FF or 0x3130 <= code <= 0x318F
    if not hangul and latin.has(ch):
        return latin
    return kr


def measure(text: str, size: float, bold: bool = False, kr_wght: int = 500) -> float:
    w = 0.0
    for ch in text:
        f = _pick(ch, bold, kr_wght)
        w += f.glyph(ch).width * size / f.upm
    return w


def path(text: str, x: float, y: float, size: float, fill: str, bold: bool = False,
         kr_wght: int = 500, anchor: str = "start") -> str:
    """baseline 좌표 (x, y)에 text를 그리는 <path>를 돌려준다."""
    total = measure(text, size, bold, kr_wght)
    cx = x - total / 2 if anchor == "middle" else x - total if anchor == "end" else x
    parts: list[str] = []
    for ch in text:
        f = _pick(ch, bold, kr_wght)
        g = f.glyph(ch)
        s = size / f.upm
        if ch != " ":
            pen = SVGPathPen(f.gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
            g.draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
            d = pen.getCommands()
            if d:
                parts.append(d)
        cx += g.width * s
    return f'<path fill="{fill}" d="{"".join(parts)}"/>'
