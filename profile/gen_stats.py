"""Gera os cards de atividade com dados reais da conta (inclui repositórios privados).

Roda no GitHub Actions todo dia. Precisa da variável GH_TOKEN com um token pessoal
(classic) com escopos `repo` e `read:user` — é ele que enxerga os repositórios privados.

Uso local sem token (só para testar o visual):  python profile/gen_stats.py --mock profile/mock.json
"""
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from theme import BORDER, CYAN, GREEN, MONO, MUTED, PANEL, SANS, TEXT, VIOLET, svg, text

OUT = Path(__file__).parent
USER = os.environ.get("GH_USER", "dutrapedro06")

# Forks que contam como projeto seu (você programou de verdade neles)
INCLUDE_FORKS = {"LegixTech", "krilltech", "Rede-De-Computadores"}
# Repositórios de outras pessoas em que você programa e que entram nas linguagens
EXTRA_REPOS = {"LucasRD3105/Akto"}
# Linguagens que só fazem barulho no gráfico
IGNORED_LANGS = {"Jupyter Notebook", "TeX", "Monkey C", "M4", "HTML", "CSS", "SCSS", "Dockerfile", "Shell", "Makefile",
                 "Procfile", "Batchfile", "PowerShell", "Mako", "PLpgSQL", "TSQL"}

LANG_COLORS = {"TypeScript": "#3178c6", "Python": "#3572A5", "JavaScript": "#f1e05a", "C": "#a8b9cc",
               "C++": "#f34b7d", "COBOL": "#22d3ee", "Java": "#b07219", "SQL": "#e38c00"}


# ------------------------------------------------------------------ coleta
def gql(query, variables, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.load(r)
    if "errors" in res:
        raise RuntimeError(res["errors"])
    return res["data"]


Q_YEAR = """query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){ createdAt
    contributionsCollection(from:$from,to:$to){
      totalCommitContributions totalPullRequestContributions
      contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } }
    } } }"""

Q_REPOS = """query($login:String!,$cursor:String){
  user(login:$login){
    repositories(first:100, after:$cursor, ownerAffiliations:[OWNER,COLLABORATOR,ORGANIZATION_MEMBER]){
      pageInfo{ hasNextPage endCursor }
      nodes{ name nameWithOwner isFork owner{ login }
        languages(first:15, orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name color } } } } } } }"""


def collect(token):
    now = datetime.now(timezone.utc)
    first = gql(Q_YEAR, {"login": USER, "from": (now - timedelta(days=365)).isoformat(),
                         "to": now.isoformat()}, token)["user"]
    created = datetime.fromisoformat(first["createdAt"].replace("Z", "+00:00"))
    last_year = first["contributionsCollection"]
    calendar = [[(d["date"], d["contributionCount"]) for d in w["contributionDays"]]
                for w in last_year["contributionCalendar"]["weeks"]]

    total = commits = prs = 0
    for year in range(created.year, now.year + 1):
        c = gql(Q_YEAR, {"login": USER, "from": f"{year}-01-01T00:00:00Z",
                         "to": f"{year}-12-31T23:59:59Z"}, token)["user"]["contributionsCollection"]
        total += c["contributionCalendar"]["totalContributions"]
        commits += c["totalCommitContributions"]
        prs += c["totalPullRequestContributions"]

    # repos = só os seus (igual ao contador do perfil, forks incluídos)
    # linguagens = média entre os projetos, cada repo pesa igual (um repo enorme não domina)
    shares, colors, repos, n_proj, cursor = {}, {}, 0, 0, None
    while True:
        r = gql(Q_REPOS, {"login": USER, "cursor": cursor}, token)["user"]["repositories"]
        for n in r["nodes"]:
            own = n["owner"]["login"].lower() == USER.lower()
            if own:
                repos += 1
            if not (own or n["nameWithOwner"] in EXTRA_REPOS):
                continue
            if n["isFork"] and n["name"] not in INCLUDE_FORKS:
                continue
            edges = [e for e in n["languages"]["edges"] if e["node"]["name"] not in IGNORED_LANGS]
            total_repo = sum(e["size"] for e in edges)
            if not total_repo:
                continue
            n_proj += 1
            for e in edges:
                name = e["node"]["name"]
                shares[name] = shares.get(name, 0) + e["size"] / total_repo
                colors[name] = e["node"]["color"] or "#8b949e"
        if not r["pageInfo"]["hasNextPage"]:
            break
        cursor = r["pageInfo"]["endCursor"]
    sizes = shares
    tot = sum(sizes.values()) or 1
    langs = sorted(([k, colors[k], v * 100 / tot] for k, v in sizes.items()), key=lambda x: -x[2])
    return {
        "total": total, "since": created.year, "commits": commits, "prs": prs, "repos": repos,
        "last_year": last_year["contributionCalendar"]["totalContributions"],
        "langs": langs, "calendar": calendar,
    }


# ------------------------------------------------------------------ desenho
def fmt(n):
    return f"{n:,}".replace(",", ".")


def stats_card(d):
    W, H = 880, 170
    tiles = [
        (fmt(d["total"]), "CONTRIBUIÇÕES", f"desde {d['since']}", VIOLET),
        (fmt(d["commits"]), "COMMITS", "inclui privados", CYAN),
        (fmt(d["last_year"]), "NO ÚLTIMO ANO", "contribuições", GREEN),
        (fmt(d["repos"]), "REPOSITÓRIOS", "públicos e privados", "#f472b6"),
    ]
    tw, gap = 205, 20
    out = []
    for i, (num, lab, sub, c) in enumerate(tiles):
        x = i * (tw + gap)
        dl = 0.15 + i * 0.15
        out.append(f"""<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".5s" begin="{dl:.2f}s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" from="0 10" to="0 0" dur=".5s" begin="{dl:.2f}s" fill="freeze"/>
<rect x="{x+.5}" y=".5" width="{tw-1}" height="{H-1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="{x+20}" y="22" width="26" height="4" rx="2" fill="{c}"/>
{text(x+20, 92, num, 46, TEXT, SANS, 800, "start", 'letter-spacing="-1"')}
{text(x+20, 124, lab, 11.5, c, MONO, 700, "start", 'letter-spacing="2"')}
{text(x+20, 145, sub, 12.5, MUTED, MONO)}
</g>""")
    return svg(W, H, "\n".join(out), "Estatísticas: " + ", ".join(f"{t[0]} {t[1].lower()}" for t in tiles))


def langs_card(d, limit=7):
    W, H = 880, 150
    langs = d["langs"][:limit]
    rest = 100 - sum(l[2] for l in langs)
    if rest > 0.5:
        langs = langs + [["Outras", "#3b4058", rest]]
    out = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>',
           text(24, 38, "LINGUAGENS MAIS USADAS", 11.5, VIOLET, MONO, 700, "start", 'letter-spacing="2"'),
           text(W - 24, 38, "média entre os projetos · inclui privados", 11.5, MUTED, MONO, 400, "end"),
           f'<clipPath id="bar"><rect x="24" y="54" width="{W-48}" height="12" rx="6"/></clipPath>',
           f'<rect x="24" y="54" width="{W-48}" height="12" rx="6" fill="#1b1f2e"/>']
    x, bw = 24.0, W - 48
    segs = []
    for i, (name, color, pct) in enumerate(langs):
        w = bw * pct / 100
        segs.append(f'<rect x="{x:.1f}" y="54" width="0" height="12" fill="{color}">'
                    f'<animate attributeName="width" from="0" to="{w:.1f}" dur=".7s" begin="{0.2 + i*0.12:.2f}s" fill="freeze"/></rect>')
        x += w
    out.append(f'<g clip-path="url(#bar)">{"".join(segs)}</g>')
    cols = 4
    for i, (name, color, pct) in enumerate(langs):
        cx = 24 + (i % cols) * ((W - 48) / cols)
        cy = 98 + (i // cols) * 26
        out.append(f'<circle cx="{cx+5:.1f}" cy="{cy-4}" r="5" fill="{color}"/>'
                   + text(cx + 18, cy, name, 14, TEXT, SANS, 600)
                   + text(cx + (W - 48) / cols - 28, cy, f"{pct:.1f}%", 12.5, MUTED, MONO, 400, "end"))
    return svg(W, H, "\n".join(out), "Linguagens: " + ", ".join(f"{l[0]} {l[2]:.1f}%" for l in langs))


def heatmap(d):
    W, H = 880, 200
    cal = d["calendar"][-53:]
    cell, gap = 12, 3
    x0, y0 = 52, 66
    levels = ["#1b1f2e", "#3b2a6b", "#5b3fb0", "#8b6cf0", "#c4b5fd"]
    mx = max([c for w in cal for _, c in w] + [1])

    def lvl(c):
        if c == 0:
            return 0
        r = c / mx
        return 1 if r <= .15 else 2 if r <= .35 else 3 if r <= .65 else 4

    out = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>',
           text(24, 38, "CONTRIBUIÇÕES NO ÚLTIMO ANO", 11.5, VIOLET, MONO, 700, "start", 'letter-spacing="2"'),
           f'<text x="{W-24}" y="38" text-anchor="end" font-family="{MONO}" font-size="12.5">'
           f'<tspan fill="{TEXT}" font-weight="700">{fmt(d["last_year"])}</tspan><tspan fill="{MUTED}"> contribuições</tspan></text>']
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    last_m = None
    for wi, week in enumerate(cal):
        x = x0 + wi * (cell + gap)
        m = int(week[0][0][5:7])
        if m != last_m and wi < len(cal) - 2:
            out.append(text(x, y0 - 10, meses[m - 1], 11, MUTED, MONO))
            last_m = m
        dl = 0.1 + wi * 0.025
        cells = []
        for day, cnt in week:
            wd = (date.fromisoformat(day).weekday() + 1) % 7  # domingo = 0
            cells.append(f'<rect x="{x}" y="{y0 + wd*(cell+gap)}" width="{cell}" height="{cell}" rx="3" '
                         f'fill="{levels[lvl(cnt)]}"><title>{day}: {cnt}</title></rect>')
        out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".3s" begin="{dl:.3f}s" fill="freeze"/>{"".join(cells)}</g>')
    for i, lab in [(1, "seg"), (3, "qua"), (5, "sex")]:
        out.append(text(x0 - 10, y0 + i * (cell + gap) + 10, lab, 10.5, MUTED, MONO, 400, "end"))
    lx = W - 24 - 5 * 15 - 40
    out.append(text(lx - 8, H - 14, "menos", 10.5, MUTED, MONO, 400, "end"))
    for i, c in enumerate(levels):
        out.append(f'<rect x="{lx + i*15}" y="{H-24}" width="11" height="11" rx="3" fill="{c}"/>')
    out.append(text(lx + 5 * 15 + 4, H - 14, "mais", 10.5, MUTED, MONO))
    return svg(W, H, "\n".join(out), f"{d['last_year']} contribuições no último ano")


def _shade(hex_color, f):
    """Escurece uma cor (#rrggbb) multiplicando os canais por f."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))


def heatmap_3d(d):
    """Mesmo calendário do heatmap, com um terceiro eixo: a altura de cada dia
    é proporcional à raiz das contribuições (a raiz evita que um dia atípico
    achate todo o resto)."""
    W, H = 880, 350
    cal = d["calendar"][-53:]
    days = [(day, cnt) for w in cal for day, cnt in w]
    mx = max([c for _, c in days] + [1])

    # projeção axonométrica: semanas andam para a direita, dias da semana para a frente
    WX, WY = 13.6, 2.2      # vetor de 1 semana na tela
    DX, DY = -8.0, 7.0      # vetor de 1 dia na tela
    ZMAX = 92               # altura do dia mais ativo
    S = 0.78                # tamanho do bloco dentro da célula (o resto é o vão)
    ox, oy = 92, 150

    def P(w, dd, z=0.0):
        return ox + w * WX + dd * DX, oy + w * WY + dd * DY - z

    def pts(*ps):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)

    levels = ["#1b1f2e", "#3b2a6b", "#5b3fb0", "#8b6cf0", "#c4b5fd"]

    def lvl(c):
        if c == 0:
            return 0
        r = (c / mx) ** 0.5
        return 1 if r <= .2 else 2 if r <= .4 else 3 if r <= .65 else 4

    def faces(w, dd, h):
        a, b = w, dd
        top = pts(P(a, b, h), P(a + S, b, h), P(a + S, b + S, h), P(a, b + S, h))
        front = pts(P(a, b + S, 0), P(a + S, b + S, 0), P(a + S, b + S, h), P(a, b + S, h))
        side = pts(P(a + S, b, 0), P(a + S, b + S, 0), P(a + S, b + S, h), P(a + S, b, h))
        return top, front, side

    out = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>',
           text(24, 38, "CONTRIBUIÇÕES NO ÚLTIMO ANO · 3D", 11.5, VIOLET, MONO, 700, "start", 'letter-spacing="2"'),
           f'<text x="{W-24}" y="38" text-anchor="end" font-family="{MONO}" font-size="12.5">'
           f'<tspan fill="{TEXT}" font-weight="700">{fmt(d["last_year"])}</tspan><tspan fill="{MUTED}"> contribuições</tspan></text>']

    # chão: sombra suave sob a grade
    n = len(cal)
    out.append(f'<polygon points="{pts(P(-.3, -.3), P(n + .1, -.3), P(n + .1, 7.1), P(-.3, 7.1))}" '
               f'fill="#0d0f16" stroke="{BORDER}" stroke-width="1"/>')

    # ordem do pintor: de trás (w+d pequeno) para a frente
    cells = []
    for wi, week in enumerate(cal):
        for day, cnt in week:
            wd = (date.fromisoformat(day).weekday() + 1) % 7  # domingo = 0
            cells.append((wi + wd, wi, wd, day, cnt))
    cells.sort()

    for _, wi, wd, day, cnt in cells:
        c = levels[lvl(cnt)]
        h = 2.0 if cnt == 0 else 4 + ZMAX * (cnt / mx) ** 0.5
        top, front, side = faces(wi, wd, h)
        polys = [(top, c), (front, _shade(c, .62)), (side, _shade(c, .42))]
        if cnt == 0:
            out.append("<g>" + "".join(f'<polygon points="{p}" fill="{f}"/>' for p, f in polys)
                       + f"<title>{day}: 0</title></g>")
            continue
        flat = faces(wi, wd, 2.0)
        dl = 0.25 + wi * 0.03
        anim = []
        for (p, f), p0 in zip(polys, flat):
            anim.append(f'<polygon points="{p}" fill="{f}"><animate attributeName="points" from="{p0}" to="{p}" '
                        f'dur=".6s" begin="{dl:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .3 1" keyTimes="0;1"/></polygon>')
        out.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{dl:.2f}s" fill="freeze"/>'
                   f'{"".join(anim)}<title>{day}: {cnt}</title></g>')

    # meses na borda da frente e dias da semana na lateral
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    last_m = None
    for wi, week in enumerate(cal):
        m = int(week[0][0][5:7])
        if m != last_m and wi < n - 2:
            x, y = P(wi, 7.9)
            out.append(text(round(x, 1), round(y + 4, 1), meses[m - 1], 11, MUTED, MONO))
            last_m = m
    for i, lab in [(1, "seg"), (3, "qua"), (5, "sex")]:
        x, y = P(-.7, i + .5)
        out.append(text(round(x, 1), round(y + 4, 1), lab, 10.5, MUTED, MONO, 400, "end"))

    # destaque do dia mais ativo
    peak_day, peak = max(days, key=lambda x: x[1])
    pw = next(i for i, w in enumerate(cal) if any(dd == peak_day for dd, _ in w))
    pd = (date.fromisoformat(peak_day).weekday() + 1) % 7
    px, py = P(pw + S / 2, pd + S / 2, 4 + ZMAX + 2)
    dd_, mm_ = peak_day[8:10], meses[int(peak_day[5:7]) - 1]
    out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".4s" begin="{0.9 + pw*0.03:.2f}s" fill="freeze"/>'
               f'<path d="M{px:.1f} {py:.1f} V{py-22:.1f}" stroke="{VIOLET}" stroke-width="1" stroke-dasharray="2 3"/>'
               f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.5" fill="{VIOLET}"/>'
               + text(round(px, 1), round(py - 28, 1), f"{peak} em {dd_} {mm_}", 11.5, TEXT, MONO, 700, "middle")
               + "</g>")

    # resumo no canto vazio (alto à direita)
    active = sum(1 for _, c in days if c)
    best = cur = 0
    for _, c in days:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    info = [(f"{active}", "dias ativos", CYAN), (f"{best} dias", "maior sequência", GREEN),
            (f"{d['last_year'] / max(active, 1):.1f}".replace(".", ","), "média por dia ativo", VIOLET)]
    for i, (num, lab, col) in enumerate(info):
        x = 24 + i * 140
        out.append(f'<rect x="{x}" y="58" width="18" height="3" rx="1.5" fill="{col}"/>'
                   + text(x, 86, num, 20, TEXT, SANS, 800)
                   + text(x, 103, lab, 10.5, MUTED, MONO))

    # legenda: altura e cor
    lx = W - 24 - 5 * 15 - 30
    out.append(text(lx - 8, 86, "menos", 10.5, MUTED, MONO, 400, "end"))
    for i, c in enumerate(levels):
        hh = 3 + i * 3
        out.append(f'<rect x="{lx + i*15}" y="{87-hh}" width="11" height="{hh}" rx="1.5" fill="{c}"/>')
    out.append(text(lx + 5 * 15 + 4, 86, "mais", 10.5, MUTED, MONO))
    out.append(text(W - 24, 103, "altura = contribuições do dia", 10.5, MUTED, MONO, 400, "end"))
    return svg(W, H, "\n".join(out), f"{d['last_year']} contribuições no último ano, em 3D")


def render(d):
    (OUT / "stats.svg").write_text(stats_card(d), encoding="utf-8")
    (OUT / "langs.svg").write_text(langs_card(d), encoding="utf-8")
    (OUT / "heatmap.svg").write_text(heatmap(d), encoding="utf-8")
    (OUT / "heatmap-3d.svg").write_text(heatmap_3d(d), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--mock":
        data = json.loads(Path(sys.argv[2]).read_text())
    else:
        token = os.environ.get("GH_TOKEN")
        if not token:
            sys.exit("GH_TOKEN não definido; nada foi alterado.")
        data = collect(token)
        print(json.dumps({k: v for k, v in data.items() if k != "calendar"}, ensure_ascii=False))
    render(data)
    print("ok")