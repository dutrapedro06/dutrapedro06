"""Gera os SVGs estáticos do perfil (banner, títulos, cards).

Uso: python profile/gen_assets.py   (gera tudo dentro de profile/)
Para mudar um texto, edite os dados abaixo e rode de novo.
"""
from pathlib import Path

from theme import (BG, BORDER, CYAN, GOLD, GREEN, MONO, MUTED, ORANGE, PANEL, PANEL2, PINK, SANS,
                   SILVER, TEXT, VIOLET, VIOLET2, chips, corners, esc, svg, text)

OUT = Path(__file__).parent


def save(name, content):
    (OUT / name).write_text(content, encoding="utf-8")


# ----------------------------------------------------------------- header
def header():
    W, H = 1200, 360
    phrases = [
        "construindo apps mobile com React Native",
        "escrevendo APIs com Python e FastAPI",
        "treinando modelos de machine learning",
        "rodando COBOL no mainframe",
    ]
    # cada frase: digita (1.2s), fica, apaga — ciclo total
    slot, total = 3.5, 3.5 * len(phrases)
    typer = []
    for i, p in enumerate(phrases):
        a = i * slot / total
        b = (i * slot + 1.3) / total
        c = (i * slot + slot - 0.35) / total
        d = (i * slot + slot) / total
        wfull = len(p) * 11.3 + 4
        kt = sorted({0.0, a, b, c, d, 1.0})
        vals = []
        for k in kt:
            if k < a or k >= d:
                vals.append(0)
            elif k < b:
                vals.append(0 if k == a else wfull)
            elif k <= c:
                vals.append(wfull)
            else:
                vals.append(0)
        # corrige: em d volta a 0
        typer.append(
            f'<clipPath id="ty{i}"><rect x="96" y="226" height="34" width="0">'
            f'<animate attributeName="width" dur="{total}s" repeatCount="indefinite" calcMode="linear" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(str(round(v, 1)) for v in vals)}"/>'
            f"</rect></clipPath>"
        )
    typer_txt = "".join(
        f'<g clip-path="url(#ty{i})">'
        + text(96, 250, p, 19, TEXT, MONO)
        + "</g>"
        for i, p in enumerate(phrases)
    )

    code = [
        ("const", " pedro", " = {", None),
        ("  local", ": ", '"Brasília, DF"', ","),
        ("  estudo", ": ", '"Ciência da Computação · IDP"', ","),
        ("  trabalho", ": ", '"Dev de Software · SENAI"', ","),
        ("  foco", ": ", '["mobile", "backend", "dados"]', ","),
        ("  hackathon", ": ", '"2º lugar · PMI-DF 2026"', ","),
        ("}", "", "", None),
    ]
    lines = []
    for i, (k, sep, v, end) in enumerate(code):
        y = 128 + i * 25
        delay = 0.6 + i * 0.22
        if i == 0:
            spans = (f'<tspan fill="{PINK}">const</tspan><tspan fill="{TEXT}"> pedro</tspan>'
                     f'<tspan fill="{MUTED}"> = {{</tspan>')
        elif k == "}":
            spans = f'<tspan fill="{MUTED}">}}</tspan>'
        else:
            spans = (f'<tspan fill="{CYAN}">{esc(k)}</tspan><tspan fill="{MUTED}">{esc(sep)}</tspan>'
                     f'<tspan fill="{GREEN}">{esc(v)}</tspan><tspan fill="{MUTED}">{esc(end or "")}</tspan>')
        lines.append(
            f'<text x="742" y="{y}" font-family="{MONO}" font-size="13.5" opacity="0" xml:space="preserve">{spans}'
            f'<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="{delay:.2f}s" fill="freeze"/></text>'
            f'<text x="722" y="{y}" font-family="{MONO}" font-size="12" fill="#3b4058" text-anchor="end">{i+1}</text>'
        )

    body = f"""
<defs>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="{VIOLET}" fill-opacity=".10"/>
  </pattern>
  <radialGradient id="g1" cx=".16" cy=".2" r=".55"><stop offset="0" stop-color="{VIOLET2}" stop-opacity=".30"/><stop offset="1" stop-color="{VIOLET2}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" cx=".85" cy=".9" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
  <clipPath id="rv"><rect x="0" y="0" width="0" height="{H}"><animate attributeName="width" from="0" to="700" dur="1.3s" begin=".15s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .2 1"/></rect></clipPath>
  <style>@keyframes bl{{50%{{opacity:0}}}} .cur{{animation:bl 1s steps(1) infinite}}</style>
  {''.join(typer)}
</defs>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#dots)"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#g1)"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#g2)"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{BORDER}"/>

<circle cx="66" cy="52" r="4.5" fill="{GREEN}"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>
{text(80, 57, "~/dutrapedro06  ·  online  ·  Brasília, DF", 12.5, MUTED, MONO, 400, "start", 'letter-spacing="1.5"')}

<g clip-path="url(#rv)">
{text(58, 150, "Pedro Dutra", 86, "url(#name)", SANS, 800, "start", 'letter-spacing="-2"')}
</g>
<rect x="62" y="170" width="0" height="4" rx="2" fill="{VIOLET}"><animate attributeName="width" from="0" to="120" dur=".9s" begin=".9s" fill="freeze"/></rect>
<rect x="188" y="170" width="0" height="4" rx="2" fill="{CYAN}"><animate attributeName="width" from="0" to="36" dur=".6s" begin="1.3s" fill="freeze"/></rect>
{text(62, 206, "CIÊNCIA DA COMPUTAÇÃO · IDP   /   DEV DE SOFTWARE · SENAI", 14, VIOLET, MONO, 600, "start", 'letter-spacing="2.5"')}

{text(64, 250, "›", 22, GREEN, MONO, 700)}
{typer_txt}
<g transform="translate(64 290)">
  {text(0, 0, "MOBILE · BACKEND · DADOS · IA · COBOL", 12, MUTED, MONO, 400, "start", 'letter-spacing="2.5"')}
</g>

<g>
  <rect x="690" y="70" width="456" height="224" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
  <path d="M690 82 a12 12 0 0 1 12 -12 h432 a12 12 0 0 1 12 12 v18 h-456z" fill="{PANEL2}"/>
  <circle cx="710" cy="86" r="5.5" fill="#ff5f57"/><circle cx="728" cy="86" r="5.5" fill="#febc2e"/><circle cx="746" cy="86" r="5.5" fill="#28c840"/>
  {text(918, 90, "pedro.ts", 12, MUTED, MONO, 400, "middle")}
  {''.join(lines)}
  <rect x="756" y="{128 + 6*25 - 13}" width="9" height="16" fill="{VIOLET}" class="cur" opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".1s" begin="2.2s" fill="freeze"/></rect>
</g>
"""
    save("header.svg", svg(W, H, body, "Pedro Dutra — Ciência da Computação no IDP e Dev de Software no SENAI"))


# ----------------------------------------------------------------- titles
def title(slug, num, cmd, tag):
    W, H = 880, 50
    body = f"""
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="0" y="12" width="4" height="26" rx="2" fill="{VIOLET}"/>
{text(22, 31, num, 13, VIOLET, MONO, 700)}
<text x="52" y="31" font-family="{MONO}" font-size="15"><tspan fill="{GREEN}">pedro@github</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{CYAN}">~</tspan><tspan fill="{MUTED}">$ </tspan><tspan fill="{TEXT}" font-weight="700">{esc(cmd)}</tspan></text>
<rect x="{52 + (len("pedro@github:~$ ") + len(cmd)) * 9.05 + 4}" y="18" width="9" height="17" fill="{VIOLET}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
{text(W - 22, 30, tag, 11, MUTED, MONO, 400, "end", 'letter-spacing="2"')}
"""
    save(f"title-{slug}.svg", svg(W, H, body, f"{num} / {cmd}"))


# ----------------------------------------------------------------- about
def about():
    W, H = 880, 330
    para = [
        "Estudante do 6º semestre de Ciência da Computação no IDP e estagiário",
        "em Desenvolvimento de Software no SENAI. Gosto de construir produtos",
        "de ponta a ponta: do app no celular à API e aos dados por trás dele.",
    ]
    rows = [
        ("AGORA", "Dev de Software no SENAI — automação, APIs, ETL e Power BI", CYAN),
        ("ESTUDO", "Ciência da Computação · IDP · 6º semestre", VIOLET),
        ("CONSTRUINDO", "Bola Cheia, Gestão Financeira, Receitas e Akto", GREEN),
        ("APRENDENDO", "Agentes de IA, compiladores e arquitetura de software", PINK),
        ("IDIOMAS", "Português nativo · Inglês avançado (C1)", ORANGE),
    ]
    out = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>',
           corners(W, H)]
    out.append(f"""<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath>
<linearGradient id="sc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/><stop offset="1" stop-color="{VIOLET}" stop-opacity=".08"/></linearGradient></defs>
<g clip-path="url(#c)"><rect x="0" y="-70" width="{W}" height="70" fill="url(#sc)"><animateTransform attributeName="transform" type="translate" values="0 0;0 {H+70}" dur="7s" repeatCount="indefinite"/></rect></g>""")
    for i, l in enumerate(para):
        out.append(text(40, 52 + i * 28, l, 18, TEXT))
    out.append(f'<line x1="40" y1="134" x2="{W-40}" y2="134" stroke="{BORDER}"/>'
               f'<rect x="40" y="132" width="0" height="4" rx="2" fill="{VIOLET}"><animate attributeName="width" from="0" to="56" dur="1s" begin=".3s" fill="freeze"/></rect>')
    for i, (k, v, c) in enumerate(rows):
        y = 172 + i * 32
        d = 0.4 + i * 0.15
        out.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".4s" begin="{d:.2f}s" fill="freeze"/>'
            f'<rect x="42" y="{y-10}" width="8" height="8" fill="{c}" transform="rotate(45 46 {y-6})"/>'
            + text(64, y - 1, k, 12, c, MONO, 700, "start", 'letter-spacing="2"')
            + text(200, y, v, 16, TEXT)
            + "</g>"
        )
    save("about-card.svg", svg(W, H, "\n".join(out), "Sobre Pedro Dutra"))


# ----------------------------------------------------------------- achievements
def achievements():
    W, H = 880, 190
    cards = [
        ("1º", "LUGAR", "Melhor Pitch e Projeto", "IDP · 2024", "Startup WoofGo + 1 ano de incubação", GOLD),
        ("2º", "LUGAR", "Hackathon PMI-DF", "2026 · desafio Krill Tech", "Krill Radar: IA para risco de crédito no agro", SILVER),
        ("</>", "HACKATHON", "COBOL · Stefanini", "Bootcamp 2026", "Sistema financeiro batch em mainframe", CYAN),
    ]
    cw, gap = 280, 20
    out = []
    for i, (big, small, t1, t2, t3, c) in enumerate(cards):
        x = i * (cw + gap)
        d = 0.2 + i * 0.2
        out.append(f"""<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".5s" begin="{d:.1f}s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" from="0 12" to="0 0" dur=".5s" begin="{d:.1f}s" fill="freeze"/>
<rect x="{x+.5}" y=".5" width="{cw-1}" height="{H-1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="{x}" y="0" width="{cw}" height="4" rx="2" fill="{c}"/>
<circle cx="{x+52}" cy="62" r="30" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".6" stroke-width="2"/>
<circle cx="{x+52}" cy="62" r="36" fill="none" stroke="{c}" stroke-opacity=".25" stroke-dasharray="3 5"><animateTransform attributeName="transform" type="rotate" from="0 {x+52} 62" to="360 {x+52} 62" dur="14s" repeatCount="indefinite"/></circle>
{text(x+52, 71 if len(big) < 3 else 68, big, 24 if len(big) < 3 else 17, c, SANS, 800, "middle")}
{text(x+100, 54, small, 11, c, MONO, 700, "start", 'letter-spacing="2.5"')}
{text(x+100, 78, t1 if len(t1) < 22 else t1, 17 if len(t1) < 22 else 15, TEXT, SANS, 700)}
{text(x+24, 124, t2, 12.5, MUTED, MONO)}
{''.join(text(x+24, 152 + j*19, ln, 13.5, TEXT) for j, ln in enumerate(wrap(t3, 33)))}
</g>""")
    save("achievements.svg", svg(W, H, "\n".join(out), "Conquistas: 1º lugar Melhor Pitch IDP 2024, 2º lugar Hackathon PMI-DF 2026, Hackathon COBOL Stefanini"))


# ----------------------------------------------------------------- project cards
def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines


def project(slug, kicker, name, desc, stack, color, status, badge=None, small=False):
    W = 430
    H = 186 if small else 230
    lines = wrap(desc, 50)[: (2 if small else 4)]
    st_color = {"PÚBLICO": GREEN, "EM CONSTRUÇÃO": ORANGE, "PRIVADO": MUTED}.get(status, MUTED)
    stw = len(status) * 7.2 + 26
    out = [f"""<defs><linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="{color}" stop-opacity="0"/><stop offset=".5" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath>
<radialGradient id="gl" cx="1" cy="0" r=".9"><stop offset="0" stop-color="{color}" stop-opacity=".16"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
<rect width="{W}" height="{H}" rx="12" fill="url(#gl)"/>
<g clip-path="url(#c)"><rect x="-160" y="0" width="160" height="3" fill="url(#t)"><animate attributeName="x" values="-160;{W};{W}" keyTimes="0;.6;1" dur="4s" repeatCount="indefinite"/></rect></g>
{text(24, 36, kicker, 11, color, MONO, 700, "start", 'letter-spacing="2.5"')}
{text(24, 70, name, 25, TEXT, SANS, 800)}
<rect x="{W-24-stw}" y="20" width="{stw}" height="22" rx="11" fill="{st_color}" fill-opacity=".12" stroke="{st_color}" stroke-opacity=".5"/>
<circle cx="{W-24-stw+12}" cy="31" r="3.5" fill="{st_color}"><animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
{text(W-24-stw/2+6, 35, status, 10.5, st_color, MONO, 700, "middle", 'letter-spacing="1"')}"""]
    if badge:
        bx = 24 + len(name) * 14.2 + 14
        out.append(f'<g transform="translate({bx:.0f} 52)"><rect width="112" height="24" rx="12" fill="{GOLD}" fill-opacity=".10" stroke="{SILVER}" stroke-opacity=".7"/>'
                   f'<circle cx="16" cy="12" r="7" fill="{SILVER}"/>' + text(16, 16, "2", 10, BG, SANS, 800, "middle")
                   + text(30, 16.5, badge, 10.5, SILVER, MONO, 700, "start", 'letter-spacing="1"') + "</g>")
    for i, l in enumerate(lines):
        out.append(text(24, 100 + i * 22, l, 14.5, "#b9bccb"))
    out.append(chips(24, H - 44, stack, color, 7, 11))
    save(f"project-{slug}.svg", svg(W, H, "\n".join(out), f"{name}: {desc}"))


PUBLIC = [
    ("krill", "HACKATHON · IA · AGRO", "Krill Radar",
     "Protótipo que cruza dados de várias fontes e calcula indicadores de risco de crédito no agronegócio, com score e alertas acionáveis.",
     ["JavaScript", "Node", "IA"], VIOLET, "PÚBLICO", "PMI-DF 2026"),
    ("legix", "MOBILE · IA · CIDADANIA", "LegixTech",
     "App de monitoramento legislativo: classifica projetos de lei por ODS com IA (Gemini) e traduz textos jurídicos para linguagem simples.",
     ["FastAPI", "PostgreSQL", "React Native"], CYAN, "PÚBLICO", None),
    ("ml", "ML · MLOPS", "Machine Learning",
     "Classificação, regressão e clusterização com otimização em cascata, e uma API Flask em Docker para prever a qualidade do ar.",
     ["Python", "scikit-learn", "XGBoost", "Docker"], GREEN, "PÚBLICO", None),
    ("cobol", "MAINFRAME · BATCH", "Hackathon COBOL",
     "Sistema financeiro batch da Stefanini: geração de dados, transações, validação, logs, extratos e saída em JSON.",
     ["COBOL", "GnuCOBOL", "Linux"], ORANGE, "PÚBLICO", None),
]
SMALL = [
    ("compiladores", "COMPILADORES", "Compiladores", "Etapas de um compilador, começando por um analisador léxico para a linguagem MiniC.", ["C", "C++"], PINK, "PÚBLICO"),
    ("taa", "ALGORITMOS", "TAA", "Grafos, ordenação, recursão, bitwise e programação competitiva em C e C++.", ["C", "C++"], PINK, "PÚBLICO"),
]
BUILDING = [
    ("bolacheia", "SAAS · PWA · ESPORTE", "Bola Cheia",
     "Agendamento de quadras society: o jogador reserva em poucos toques e o dono gerencia agenda e preços, sem depender do WhatsApp.",
     ["PWA", "JavaScript", "HTML/CSS"], GREEN, "EM CONSTRUÇÃO"),
    ("financas", "WEB · FINANÇAS", "Gestão Financeira",
     "Finanças pessoais para uso diário: lançamento rápido no celular, dashboard, projeções, importação de extratos OFX e CI.",
     ["FastAPI", "PostgreSQL", "HTMX", "Docker"], CYAN, "EM CONSTRUÇÃO"),
    ("receitas", "MOBILE · SOCIAL", "Receitas",
     "App e site para guardar e compartilhar receitas com fotos e passo a passo, com espaços privados para família e amigos.",
     ["Expo", "TypeScript", "Supabase"], PINK, "EM CONSTRUÇÃO"),
    ("akto", "MOBILE · PRODUTIVIDADE", "Akto",
     "App de hábitos, tarefas e eventos com conjuntos, progresso, lembretes e login com Google. Desenvolvido em dupla.",
     ["Expo", "Hono", "Cloudflare"], VIOLET, "EM CONSTRUÇÃO"),
]


# ----------------------------------------------------------------- footer
def footer():
    W, H = 1200, 150
    body = f"""
<defs><linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET2}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient></defs>
<path fill="url(#w)" fill-opacity=".18" d="M0 70 C 200 30 400 110 600 70 S 1000 30 1200 70 V150 H0Z">
  <animate attributeName="d" dur="9s" repeatCount="indefinite" values="M0 70 C 200 30 400 110 600 70 S 1000 30 1200 70 V150 H0Z;M0 80 C 200 110 400 30 600 80 S 1000 110 1200 60 V150 H0Z;M0 70 C 200 30 400 110 600 70 S 1000 30 1200 70 V150 H0Z"/></path>
<path fill="url(#w)" fill-opacity=".35" d="M0 100 C 250 80 450 130 650 100 S 1000 80 1200 105 V150 H0Z">
  <animate attributeName="d" dur="7s" repeatCount="indefinite" values="M0 100 C 250 80 450 130 650 100 S 1000 80 1200 105 V150 H0Z;M0 105 C 250 125 450 85 650 108 S 1000 125 1200 95 V150 H0Z;M0 100 C 250 80 450 130 650 100 S 1000 80 1200 105 V150 H0Z"/></path>
<text x="600" y="34" text-anchor="middle" font-family="{MONO}" font-size="14"><tspan fill="{GREEN}">✓</tspan><tspan fill="{MUTED}">  build passed · </tspan><tspan fill="{TEXT}">obrigado pela visita</tspan><tspan fill="{VIOLET}"> ▌</tspan></text>
"""
    save("footer.svg", svg(W, H, body, "Obrigado pela visita"))


if __name__ == "__main__":
    header()
    for slug, num, cmd, tag in [
        ("about", "01", "whoami", "SOBRE"),
        ("wins", "02", "cat conquistas.log", "CONQUISTAS"),
        ("projects", "03", "ls projetos/ --destaque", "PROJETOS"),
        ("building", "04", "git checkout em-construcao", "EM CONSTRUÇÃO"),
        ("stack", "05", "cat stack.json", "TECNOLOGIAS"),
        ("stats", "06", "git log --stat --all", "ATIVIDADE"),
        ("contact", "07", "./contato.sh", "CONTATO"),
    ]:
        title(slug, num, cmd, tag)
    about()
    achievements()
    for p in PUBLIC:
        project(*p)
    for p in SMALL:
        project(*p, small=True)
    for p in BUILDING:
        project(*p)
    footer()
    print("ok")
