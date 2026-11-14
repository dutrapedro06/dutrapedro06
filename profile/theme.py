"""Paleta e helpers compartilhados pelos geradores de SVG do perfil."""
from html import escape

BG = "#0a0b10"
PANEL = "#11131b"
PANEL2 = "#151826"
BORDER = "#23273a"
TEXT = "#e6e7ee"
MUTED = "#7d8197"
VIOLET = "#a78bfa"
VIOLET2 = "#7c3aed"
CYAN = "#22d3ee"
GREEN = "#4ade80"
GOLD = "#fbbf24"
SILVER = "#cbd5e1"
PINK = "#f472b6"
ORANGE = "#fb923c"

SANS = "'Segoe UI',Inter,Roboto,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code',Consolas,'SF Mono',Menlo,monospace"


def esc(s: str) -> str:
    return escape(str(s), quote=True)


def svg(w, h, body, title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">\n'
        f"<title>{esc(title)}</title>\n{body}\n</svg>\n"
    )


def text(x, y, s, size=16, fill=TEXT, font=SANS, weight=400, anchor="start", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
    )


def chip(x, y, label, color=VIOLET, size=12):
    """Etiqueta arredondada; devolve (svg, largura)."""
    w = int(len(label) * size * 0.62) + 20
    body = (
        f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="{color}" fill-opacity=".12" '
        f'stroke="{color}" stroke-opacity=".45"/>'
        + text(x + w / 2, y + 16.5, label, size, color, MONO, 600, "middle")
    )
    return body, w


def chips(x, y, labels, color=VIOLET, gap=8, size=12):
    out = []
    for lab in labels:
        b, w = chip(x, y, lab, color, size)
        out.append(b)
        x += w + gap
    return "".join(out)


def corners(w, h, pad=10, ln=14, color=BORDER):
    return (
        f'<path d="M{pad} {pad+ln} V{pad} H{pad+ln} M{w-pad-ln} {pad} H{w-pad} V{pad+ln} '
        f'M{pad} {h-pad-ln} V{h-pad} H{pad+ln} M{w-pad-ln} {h-pad} H{w-pad} V{h-pad-ln}" '
        f'fill="none" stroke="{color}" stroke-width="1.5"/>'
    )
