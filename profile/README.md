<p align="center">
  <a href="https://check-host.one"><img src="https://check-host.one/logo-96.png" width="88" alt="check-host.one logo"></a>
</p>

<h1 align="center">check-host.one</h1>

<p align="center">
  <b>Free global network checks.</b> Ping, TCP ping, HTTP, traceroute and DNS from measurement servers in 100+ countries, with live results on a world map.<br>
  Find out in seconds whether a site is down for everyone or just you.
</p>

<p align="center">
  <a href="https://check-host.one"><b>check-host.one</b></a> ·
  <a href="https://check-host.one/docs">Docs</a> ·
  <a href="https://check-host.one/docs#api">API</a> ·
  <a href="https://github.com/Check-Host-one/check-host-mcp">MCP server</a> ·
  <a href="https://check-host.one/embed/builder">Widgets</a> ·
  <a href="https://x.com/checkhostone">X</a> ·
  <a href="https://t.me/checkhostone">Telegram</a>
</p>

---

### 🔧 Tools

| | |
| --- | --- |
| [**Ping**](https://check-host.one/ping) | ICMP latency and packet loss from every region |
| [**Port check**](https://check-host.one/port-check) | Is a port open and reachable worldwide? |
| [**Website check**](https://check-host.one/website-check) | HTTP status code and response time from many countries |
| [**Traceroute**](https://check-host.one/traceroute) | Where on the path does the connection break? |
| [**DNS lookup**](https://check-host.one/dns-lookup) | Compare DNS answers between regions, check propagation |
| [**IP lookup**](https://check-host.one/ip-lookup) | ASN, network operator and geolocation of any host |

No account and no API key, for the website, the API or the MCP server.

### 📡 Live: pinging check-host.one right now

<a href="https://check-host.one/?type=ping&target=check-host.one">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Check-Host-one/.github/main/profile/ping-dark.svg">
    <img src="https://raw.githubusercontent.com/Check-Host-one/.github/main/profile/ping-light.svg" width="640" alt="Live ping of check-host.one from 10 countries">
  </picture>
</a>

<sub>Click the card to run a fresh check · [last result with map](https://check-host.one/r/srkr7nrsm2) · drawn every 6 hours by a [GitHub Action](https://github.com/Check-Host-one/.github/blob/main/.github/workflows/ping.yml) with the [Python SDK](https://github.com/Check-Host-one/check-host-python)</sub>

### 🤖 For AI agents

Add the hosted MCP server and let Claude, Cursor, Copilot or any MCP client run checks for you:

```sh
claude mcp add --transport http check-host https://check-host.one/mcp
```

Setup for every client: [**check-host-mcp**](https://github.com/Check-Host-one/check-host-mcp)

### 📦 SDKs

| Language | Repository | Install |
| --- | --- | --- |
| Python | [check-host-python](https://github.com/Check-Host-one/check-host-python) | `pip install git+https://github.com/Check-Host-one/check-host-python` |
| JavaScript / TypeScript | [check-host-js](https://github.com/Check-Host-one/check-host-js) | `npm i github:Check-Host-one/check-host-js` |
| Go | [check-host-go](https://github.com/Check-Host-one/check-host-go) | `go get github.com/Check-Host-one/check-host-go` |
| Rust | [check-host-rust](https://github.com/Check-Host-one/check-host-rust) | `cargo add check-host-one --git https://github.com/Check-Host-one/check-host-rust` |
| Java | [check-host-java](https://github.com/Check-Host-one/check-host-java) | JitPack: `com.github.Check-Host-one:check-host-java` |
| PHP | [check-host-php](https://github.com/Check-Host-one/check-host-php) | Composer: `check-host-one/check-host` |
| Ruby | [check-host-ruby](https://github.com/Check-Host-one/check-host-ruby) | `gem "check-host-one", git: "https://github.com/Check-Host-one/check-host-ruby"` |
| C# / .NET | [check-host-dotnet](https://github.com/Check-Host-one/check-host-dotnet) | `CheckHost.One` |

All SDKs are small, MIT licensed and mostly dependency-free.

```python
from checkhost import Client

m = Client().ping("example.com", locations=["DE", "US", "Tokyo"])
print("https://check-host.one/r/" + m["resultSlug"])
```

### 🌍 Embed a live check

Put a live status or latency widget for your site on any page: [widget builder](https://check-host.one/embed/builder).
