# Pings check-host.one from servers around the world and writes the results
# into profile/README.md between the PING markers. Run by .github/workflows/ping.yml.
import re
import time
from datetime import datetime, timezone

from checkhost import Client

TARGET = "check-host.one"
COUNTRIES = ["DE", "GB", "US", "CA", "BR", "JP", "SG", "IN", "AU", "ZA"]
README = "profile/README.md"


def flag(cc):
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in cc.upper())


def ms(v):
    return f"{v:.1f} ms" if isinstance(v, (int, float)) else "–"


m = None
for attempt in range(3):
    try:
        m = Client().ping(TARGET, limit=len(COUNTRIES), locations=COUNTRIES)
        break
    except Exception as e:  # rate limited or network blip: try again shortly
        print("attempt", attempt, e)
        time.sleep(30)
if m is None:
    raise SystemExit("ping failed")

rows = []
for r in sorted(m["results"], key=lambda r: (r["result"].get("stats") or {}).get("avg") or 1e9):
    p, s = r["probe"], r["result"].get("stats") or {}
    loss = s.get("loss")
    status = "🟢" if loss == 0 else ("🔴" if loss == 100 or loss is None else "🟡")
    rows.append(f"| {status} | {flag(p['country'])} {p['city']}, {p['country']} | {p.get('network', '')} | "
                f"**{ms(s.get('avg'))}** | {ms(s.get('min'))} | {ms(s.get('max'))} | {'–' if loss is None else f'{loss:g}%'} |")

now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
block = "\n".join([
    "<!-- PING:START -->",
    "| | Server | Network | Avg | Min | Max | Loss |",
    "| :---: | --- | --- | ---: | ---: | ---: | ---: |",
    *rows,
    "",
    f"<sub>ICMP ping to `{TARGET}` from {len(rows)} servers, {now}. "
    f"[Full result with map](https://check-host.one/r/{m['resultSlug']}) · updated every 6 hours by a "
    "[GitHub Action](https://github.com/Check-Host-one/.github/blob/main/.github/workflows/ping.yml) "
    "using the [Python SDK](https://github.com/Check-Host-one/check-host-python).</sub>",
    "<!-- PING:END -->",
])

text = open(README, encoding="utf-8").read()
text = re.sub(r"<!-- PING:START -->.*<!-- PING:END -->", lambda _: block, text, flags=re.S)
open(README, "w", encoding="utf-8").write(text)
print(block)
