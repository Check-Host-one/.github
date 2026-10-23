# Pings check-host.one from servers around the world, draws the result as a
# card in the style of the check-host.one embed widget (profile/ping-dark.svg,
# profile/ping-light.svg) and stamps the time into profile/README.md.
# Run by .github/workflows/ping.yml.
import base64
import math
import re
import time
from datetime import datetime, timezone
from html import escape

from checkhost import Client

TARGET = "check-host.one"
COUNTRIES = ["DE", "GB", "US", "CA", "BR", "JP", "SG", "IN", "AU", "ZA"]
README = "profile/README.md"
LOGO = base64.b64encode(open("scripts/logo.png", "rb").read()).decode()

# Palettes of the embed widget (html[data-embed-theme] in the site's styles.css).
THEMES = {
    "dark": dict(bg="#0f1113", alt="#191c20", border="#262a30", fg="#edeef1", fg2="#a3aab4", fg3="#6e7681",
                 ok="#34d399", warn="#fbbf24", err="#f87171", brand_bg="#151b26", brand_fg="#7aa5f5"),
    "light": dict(bg="#ffffff", alt="#f5f7f9", border="#e4e8ec", fg="#0f1319", fg2="#545d6b", fg3="#8892a0",
                  ok="#15803d", warn="#b45309", err="#b91c1c", brand_bg="#f3f6fd", brand_fg="#2b5ed6"),
}
RAMP = [(50, "#22c55e"), (150, "#84cc16"), (300, "#eab308"), (600, "#f97316"), (math.inf, "#ef4444")]
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def flag(cc, x, y):
    """The site's flag-icons flag (MIT, github.com/lipis/flag-icons); emoji
    flags render as bare letters on Windows."""
    try:
        svg = open(f"scripts/flags/{cc.lower()}.svg", "rb").read()
    except OSError:
        return f'<text x="{x}" y="{y + 10}" font-family="{MONO}" font-size="9" fill="#6e7681">{escape(cc)}</text>'
    return (f'<image x="{x}" y="{y}" width="17" height="12.75" preserveAspectRatio="none" '
            f'href="data:image/svg+xml;base64,{base64.b64encode(svg).decode()}"/>')


def fmt_ms(v):
    return f"{v:.1f} ms" if v < 10 else f"{v:.0f} ms"


def run_check():
    for attempt in range(3):
        try:
            return Client().ping(TARGET, limit=len(COUNTRIES), locations=COUNTRIES)
        except Exception as e:  # rate limited or network blip: try again shortly
            print("attempt", attempt, e)
            time.sleep(30)
    raise SystemExit("ping failed")


def card(m, theme, checked):
    c = THEMES[theme]
    W, ROW, TOP = 640, 26, 112
    rows = sorted(m["results"], key=lambda r: (r["result"].get("stats") or {}).get("avg") or math.inf)
    lat = [s["avg"] for r in rows if (s := r["result"].get("stats")) and s.get("avg") is not None]
    online, total = len(lat), len(rows)
    state, color = (("Online", c["ok"]) if online == total else ("Down", c["err"]) if online == 0
                    else ("Partially down", c["warn"]))
    slowest = max(lat, default=0)
    H = TOP + ROW * total + 50

    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}">
<title>Live ping of {TARGET} from {total} countries</title>
<style>
  @keyframes grow {{ from {{ transform: scaleX(0) }} }}
  @keyframes fade {{ from {{ opacity: 0 }} }}
  @keyframes ring {{ 0% {{ r: 4; opacity: .8 }} 80%, 100% {{ r: 8; opacity: 0 }} }}
  .bar {{ transform-box: fill-box; transform-origin: left; animation: grow .7s cubic-bezier(.2,.8,.2,1) both }}
  .row {{ animation: fade .4s ease both }}
  .ring {{ animation: ring 2.4s ease-out infinite }}
</style>
<clipPath id="r"><rect width="{W}" height="{H}" rx="12"/></clipPath>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{c['bg']}"/>
<rect width="{W}" height="38" fill="{c['brand_bg']}"/>
<line x1="0" y1="38.5" x2="{W}" y2="38.5" stroke="{c['border']}"/>
<image x="16" y="10" width="18" height="18" href="data:image/png;base64,{LOGO}"/>
<text x="41" y="24" font-size="13" font-weight="700" fill="{c['fg']}">check-host<tspan fill="{c['fg3']}">.one</tspan></text>
<text x="{W - 16}" y="24" font-size="12" font-weight="600" fill="{c['brand_fg']}" text-anchor="end">Run your own check →</text>
<text x="16" y="70" font-size="17" font-weight="650" fill="{c['fg']}">{TARGET}</text>
<rect x="{16 + len(TARGET) * 9.4}" y="57" width="38" height="17" rx="4" fill="{c['alt']}"/>
<text x="{16 + len(TARGET) * 9.4 + 19}" y="69" font-family="{MONO}" font-size="9" font-weight="600" letter-spacing="1" fill="{c['fg3']}" text-anchor="middle">PING</text>
<circle cx="{W - 186}" cy="64" r="4" fill="{color}"/>''']
    if state == "Online":
        out.append(f'<circle class="ring" cx="{W - 186}" cy="64" r="4" fill="none" stroke="{color}"/>')
    out.append(f'''<text x="{W - 172}" y="69" font-size="15" font-weight="650" fill="{color}">{state}</text>
<text x="{W - 186}" y="88" font-size="11" fill="{c['fg3']}">{online}/{total} responding</text>''')
    if lat:
        out.append(f'''<text x="{W - 16}" y="71" font-family="{MONO}" font-size="20" font-weight="600" fill="{c['fg']}" text-anchor="end">{fmt_ms(sum(lat) / len(lat))}</text>
<text x="{W - 16}" y="88" font-size="11" fill="{c['fg3']}" text-anchor="end">avg</text>''')

    for i, r in enumerate(rows):
        p, s = r["probe"], r["result"].get("stats") or {}
        y = TOP + i * ROW
        label = escape(f"{p['city']}, {p['country']} · {p.get('network', '')}")
        out.append(f'<g class="row" style="animation-delay:{i * 45}ms">')
        out.append(flag(p["country"], 16, y + 3))
        out.append(f'<text x="42" y="{y + 13}" font-size="12.5" fill="{c["fg2"]}">{label}</text>')
        avg = s.get("avg")
        if avg is None:
            out.append(f'<text x="{W - 16}" y="{y + 13}" font-size="12" font-weight="600" fill="{c["err"]}" text-anchor="end">No reply</text>')
        else:
            bar_w = max(math.sqrt(avg / slowest) * 150, 6) if slowest else 6
            ramp = next(col for limit, col in RAMP if avg < limit)
            out.append(f'<rect x="{W - 246}" y="{y + 6}" width="150" height="5" rx="2.5" fill="{c["alt"]}"/>')
            out.append(f'<rect class="bar" style="animation-delay:{150 + i * 45}ms" x="{W - 246}" y="{y + 6}" width="{bar_w:.1f}" height="5" rx="2.5" fill="{ramp}"/>')
            out.append(f'<text x="{W - 16}" y="{y + 13}" font-family="{MONO}" font-size="12" fill="{c["fg"]}" text-anchor="end">{fmt_ms(avg)}</text>')
        out.append("</g>")

    fy = H - 38
    out.append(f'''<line x1="0" y1="{fy + .5}" x2="{W}" y2="{fy + .5}" stroke="{c['border']}"/>
<text x="16" y="{fy + 23}" font-size="11" fill="{c['fg3']}">Checked {checked} · refreshed every 6 hours</text>
<rect x="{W - 104}" y="{fy + 8}" width="88" height="24" rx="6" fill="{c['brand_fg']}"/>
<text x="{W - 60}" y="{fy + 24}" font-size="12" font-weight="650" fill="{c['bg']}" text-anchor="middle">Check now</text>
<rect width="{W}" height="{H}" rx="12" fill="none" stroke="{c['border']}" stroke-width="2"/>
</g>
</svg>
''')
    return "\n".join(out)


m = run_check()
checked = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
for theme in THEMES:
    open(f"profile/ping-{theme}.svg", "w", encoding="utf-8").write(card(m, theme, checked))

# The README only points at the SVGs; refresh the link to the latest full result
# so the card always opens the check it shows.
text = open(README, encoding="utf-8").read()
text = re.sub(r"https://check-host\.one/r/\w+", f"https://check-host.one/r/{m['resultSlug']}", text)
open(README, "w", encoding="utf-8").write(text)
print(checked, m["resultSlug"])
