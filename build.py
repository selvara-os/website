"""Builds the static SelvaraOS website (GitHub Pages) into _site/.
No JavaScript, no external requests, light and dark themes.
News posts are Markdown files in news/; see news/_template.md."""
import datetime
import html
import math
import pathlib
import re
import shutil
import sys
from urllib.parse import urljoin

import markdown
from PIL import Image

SRC = pathlib.Path(__file__).parent
OUT = SRC / "_site"
SITE_URL = "https://selvara-os.github.io/website/"
GITHUB = "https://github.com/selvara-os"
DISCORD = "https://discord.gg/3zVqjyQsq6"
TESTER_FORM = "https://forms.gle/Z6By2JMZiq7L3i2GA"
BUILD_DATE = "12 November 2026"
POSTS_PER_PAGE = 10
CATEGORIES = {"Release": "release", "Announcement": "announcement",
              "Behind the scenes": "behind", "Changelog": "changelog"}

shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(SRC / "assets", OUT / "assets")
if (SRC / "news/img").is_dir():
    shutil.copytree(SRC / "news/img", OUT / "news/img")


def rings(cls="", animated=False):
    g = (lambda n, body: f'<g class="ring r{n}">{body}</g>') if animated else (lambda n, body: body)
    return (f'<svg{f" class=\"{cls}\"" if cls else ""} viewBox="0 0 200 200" aria-hidden="true">'
            + g(1, '<circle cx="100" cy="100" r="70" fill="none" stroke="#2FAE85" stroke-width="10" stroke-linecap="round" stroke-dasharray="380 60" transform="rotate(-30 100 100)"/>')
            + g(2, '<circle cx="100" cy="100" r="52" fill="none" stroke="#2FAE85" stroke-width="10" stroke-linecap="round" stroke-dasharray="280 47" opacity="0.8" transform="rotate(60 100 100)"/>')
            + g(3, '<circle cx="100" cy="100" r="34" fill="none" stroke="#2FAE85" stroke-width="10" stroke-linecap="round" stroke-dasharray="180 34" opacity="0.6" transform="rotate(150 100 100)"/>')
            + '<circle class="core" cx="100" cy="100" r="12" fill="#8FD6B4"/></svg>')


LOGO = rings()
NAV = [("features.html", "Features"), ("privacy.html", "Privacy"),
       ("screenshots.html", "Screenshots"), ("releases.html", "Releases"), ("news.html", "News"), ("faq.html", "FAQ")]


def page(file, title, desc, body, current=None):
    # 404.html is served at any missing address, so it needs absolute paths
    base = "/website/" if file == "404.html" else "../" * file.count("/")
    current = current or file
    nav = "".join(
        f'<a href="{base}{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>'
        for href, label in NAV)
    foot = "".join(f'<li><a href="{base}{href}">{label}</a></li>' for href, label in NAV)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self'; font-src 'self'; script-src 'none'; base-uri 'self'; form-action 'none'">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}assets/img/og.png">
<link rel="icon" href="{base}assets/img/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/atom+xml" title="SelvaraOS news" href="{base}feed.xml">
<link rel="preload" href="{base}assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/interdisplay-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{base}index.html" aria-label="SelvaraOS home">{LOGO}<span class="word">Selvara<span class="os">OS</span></span></a>
    <div class="head-right"><nav class="nav" aria-label="Main">{nav}</nav><div class="head-btns"><a class="btn btn-quiet btn-sm" href="{GITHUB}" rel="noopener">GitHub</a><a class="btn btn-primary btn-sm" href="{DISCORD}" rel="noopener">Discord</a></div></div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <a class="brand" href="{base}index.html" aria-label="SelvaraOS home">{LOGO}<span>Selvara<span class="os">OS</span></span></a>
      <ul class="foot-nav">{foot}<li><a href="{GITHUB}" rel="noopener">GitHub</a></li><li><a href="{DISCORD}" rel="noopener">Discord</a></li></ul>
    </div>
    <div class="foot-note fine">
      <p>This website sets no cookies, runs no scripts, has no analytics and loads nothing from other servers.</p>
      <p>SelvaraOS is free software under the GPL-3.0 licence, built on Debian and KDE technologies. Debian is a registered trademark of Software in the Public Interest, Inc. SelvaraOS is an independent project and is not affiliated with Debian, KDE or Apple.</p>
      <p>Screenshots show development builds and will change.</p>
    </div>
  </div>
</footer>
</body>
</html>
"""
    (OUT / file).parent.mkdir(parents=True, exist_ok=True)
    (OUT / file).write_text(doc)


def terms(items, one=False):
    rows = "".join(f"<div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in items)
    return f'<dl class="terms{" terms-1" if one else ""}">{rows}</dl>'


REPORT = f"""<div class="report-wrap">
<p class="fine">Development build, {BUILD_DATE}</p>
<table class="report" aria-label="Test results of the development build of {BUILD_DATE}">
<tr><th scope="row">Outgoing connections during start-up, login and five minutes at rest</th><td>0</td></tr>
<tr><th scope="row">Login to a ready desktop</th><td>3.7 s</td></tr>
<tr><th scope="row">Memory in use at rest</th><td>1.06 GB</td></tr>
<tr><th scope="row">Processor use at rest</th><td>0.3%</td></tr>
</table>
<p class="fine">Test machine: 4 GB of memory, 2 processor cores, no graphics acceleration.</p>
</div>"""

# ------------------------------------------------------------------ news
def fail(path, msg):
    sys.exit(f"news/{path.name}: {msg}")


def read_post(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        fail(path, "missing the --- block with title, date and category at the top")
    meta = {}
    for line in m.group(1).splitlines():
        if line.strip():
            key, sep, value = line.partition(":")
            if not sep:
                fail(path, f"this line needs 'name: value': {line!r}")
            meta[key.strip().lower()] = value.strip()
    if meta.get("draft", "").lower() in ("true", "yes"):
        return None
    for key in ("title", "date", "category"):
        if not meta.get(key):
            fail(path, f"'{key}' is missing")
    try:
        date = datetime.date.fromisoformat(meta["date"])
    except ValueError:
        fail(path, f"date must look like 2026-11-12, got {meta['date']!r}")
    if meta["category"] not in CATEGORIES:
        fail(path, f"category must be one of: {', '.join(CATEGORIES)}")
    cover = meta.get("cover")
    if cover and not (SRC / "news" / cover).is_file():
        fail(path, f"cover image not found: news/{cover}")
    body = markdown.markdown(m.group(2), extensions=["extra", "sane_lists", "smarty"])
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    summary = meta.get("summary")
    if not summary:
        first = re.search(r"<p>(.*?)</p>", body, re.S)
        summary = re.sub(r"<[^>]+>", "", first.group(1)) if first else ""
        if len(summary) > 220:
            summary = summary[:217].rsplit(" ", 1)[0] + "…"
    else:
        summary = html.escape(summary)
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    return {
        "slug": slug, "url": f"news/{slug}.html", "title": html.escape(meta["title"]),
        "date": date, "nice_date": f"{date.day} {date:%B %Y}", "category": meta["category"],
        "author": html.escape(meta.get("author") or "SelvaraOS team"),
        "cover": cover, "cover_alt": html.escape(meta.get("cover_alt", "")),
        "summary": summary, "minutes": max(1, math.ceil(words / 220)), "body": body,
    }


POSTS = [p for p in (read_post(f) for f in sorted((SRC / "news").glob("*.md"))
                     if not f.name.startswith("_")) if p]
POSTS.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
_slugs = [p["slug"] for p in POSTS]
for s in set(_slugs):
    if _slugs.count(s) > 1:
        sys.exit(f"news: two posts would both be published as news/{s}.html; rename one file")


def meta_line(p):
    return (f'<p class="meta"><span class="cat cat-{CATEGORIES[p["category"]]}">{p["category"]}</span>'
            f'<time datetime="{p["date"].isoformat()}">{p["nice_date"]}</time>'
            f'<span>{p["minutes"]} min read</span></p>')


def news_item(p, base="", thumb=True):
    img = ""
    if thumb and p["cover"]:
        img = (f'<a class="thumb" href="{base}{p["url"]}" tabindex="-1" aria-hidden="true">'
               f'<img src="{base}news/{p["cover"]}" width="16" height="9" alt=""></a>')
    return (f'<li class="news-item{" has-thumb" if img else ""}">{img}<div class="txt">{meta_line(p)}'
            f'<h3><a href="{base}{p["url"]}">{p["title"]}</a></h3>'
            f'<p class="muted">{p["summary"]}</p></div></li>')


LATEST = ""
if POSTS:
    LATEST = f"""
<section class="band rule">
  <div class="wrap">
    <div class="news-head">
      <div class="head"><h2>Latest from the project.</h2></div>
      <a class="btn btn-quiet" href="news.html">All news</a>
    </div>
    <ol class="news-list news-compact">{"".join(news_item(p, thumb=False) for p in POSTS[:3])}</ol>
  </div>
</section>
"""

# ------------------------------------------------------------------ home
WALLS =[("nucleo", "Nucleo"), ("vetro", "Vetro"), ("colline", "Colline"),
         ("dendro", "Dendro"), ("aurora", "Aurora"), ("grafite", "Grafite")]
walls = "".join(
    f'<figure><div class="wp">'
    f'<img class="d" src="assets/img/wp-{k}-dark-sm.webp" width="640" height="360" alt="{n} wallpaper, dark version">'
    f'<img class="l" src="assets/img/wp-{k}-light-sm.webp" width="640" height="360" alt="{n} wallpaper, light version">'
    f'</div><figcaption>{n}</figcaption></figure>' for k, n in WALLS)

HOME = f"""
<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div class="hero-copy">
        <h1>A computer that minds its own business.</h1>
        <p class="lead">SelvaraOS is a free desktop operating system for PCs. It collects nothing, stays smooth on older hardware, and is easy to use even if you have never touched Linux.</p>
        <div class="actions">
          <a class="btn btn-primary" href="features.html">See the features</a>
          <a class="btn btn-quiet" href="privacy.html">Read the privacy promise</a>
        </div>
        <p class="status">In development. Canopy Beta 1 release candidate planned for the second half of December.</p>
      </div>
      {rings("rings", animated=True)}
    </div>
    <figure class="hero-shot">
      <div class="frame"><img src="assets/img/shot-settings-canopy.webp" width="1600" height="900" alt="The SelvaraOS desktop in dark mode with Selvara Settings open on the General page, the top bar above and the dock below"></div>
      <figcaption>Selvara Settings in a current development build.</figcaption>
    </figure>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="head">
      <h2>Measured on every build.</h2>
      <p class="lead">Each build of SelvaraOS goes through automated tests that record all network traffic and time the desktop. These are the current results.</p>
    </div>
    {REPORT}
  </div>
</section>

<section class="band rule">
  <div class="wrap">
    <div class="head">
      <h2>Six rules decide every detail.</h2>
    </div>
    {terms([
        ("Private by design", "No telemetry, no accounts, no ads. Nothing connects to the internet unless you ask, and every build is tested for it."),
        ("Smooth on older PCs", "Built for computers with 4 GB of memory. Speed comes from careful engineering, and no effect is switched off to fake it."),
        ("Easy from the first minute", "Install apps, update, set up Wi-Fi and printers without opening a terminal. Plain words throughout."),
        ("Familiar if you come from a Mac", "A top bar, a dock, one search for everything and the keyboard shortcuts you already know."),
        ("Secure from the start", "Sandboxed apps, a firewall that blocks incoming connections and no services listening on your network."),
        ("The same everywhere", "One design and one vocabulary in every app, dialog and settings page."),
    ])}
  </div>
</section>

<section class="band rule">
  <div class="wrap">
    <div class="head">
      <h2>A desktop of its own.</h2>
      <p class="lead">The top bar, dock, search, settings and notifications are written from scratch for SelvaraOS and run on the KWin compositor.</p>
    </div>
    <div class="tour">
      <div class="tour-main">
        <div class="txt"><h3>One search for everything</h3><p class="muted">Apps, files, settings and quick sums. Press Super and Space, then start typing.</p></div>
        <div class="frame"><img src="assets/img/shot-search.webp" width="1600" height="908" alt="Search open on the desktop, listing apps and settings pages that match the letters s, e, t"></div>
      </div>
      <div class="pair">
        <figure><div class="frame"><img src="assets/img/shot-notifications.webp" width="1240" height="305" alt="A notification banner under the top bar"></div><figcaption><strong>Notifications that stay out of the way.</strong> A banner in the corner, the full history one click away.</figcaption></figure>
        <figure><div class="frame"><img src="assets/img/shot-bootmenu.webp" width="760" height="591" alt="The start-up menu with SelvaraOS, Recovery mode and Other versions"></div><figcaption><strong>Polished from the first second.</strong> No scrolling text at start-up, and a start-up menu that appears only when you ask for it.</figcaption></figure>
      </div>
    </div>
  </div>
</section>

<section class="band rule">
  <div class="wrap">
    <input class="vh" type="radio" name="wp" id="wp-dark" checked>
    <input class="vh" type="radio" name="wp" id="wp-light">
    <div class="walls-head">
      <div class="head">
        <h2>Six wallpapers, each in dark and light.</h2>
        <p class="lead">They follow your theme automatically.</p>
      </div>
      <div class="seg"><label for="wp-dark">Dark</label><label for="wp-light">Light</label></div>
    </div>
    <div class="walls">{walls}</div>
  </div>
</section>

<section class="band rule">
  <div class="wrap">
    <div class="head"><h2>Built on proven ground.</h2></div>
    <div class="cols">
      <div><h3>Debian 13</h3><p>The Debian stable base, with security updates until 2030 and thousands of apps.</p></div>
      <div><h3>KWin on Wayland</h3><p>A modern display system and one of the most mature compositors on Linux, underneath our own desktop.</p></div>
      <div><h3>Free software</h3><p>Everything we write is published under the GPL-3.0 licence. Read it, change it, share it.</p></div>
    </div>
  </div>
</section>
{LATEST}
<section class="band rule">
  <div class="wrap closing">
    <h2>Follow the project.</h2>
    <p class="lead">SelvaraOS isn't available to download yet. Apply as a beta tester to get nightly builds before everyone else, or join the Discord server for news and previews.</p>
    <div class="actions">
      <a class="btn btn-primary" href="{TESTER_FORM}" rel="noopener">Become a beta tester</a>
      <a class="btn btn-quiet" href="{DISCORD}" rel="noopener">Join the Discord</a>
      <a class="btn btn-quiet" href="releases.html">See the release plan</a>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ features
R, P, L = "ready", "progress", "planned"
LABEL = {R: "Working", P: "In progress", L: "Planned"}
GROUPS = [
    ("Desktop", [
        ("Top bar", "System menu, the menus of the app you're using, status icons and the clock.", R),
        ("Dock", "Magnification, live window previews, badges, and icons that bounce while an app starts.", R),
        ("App launcher", "Full screen or as a compact panel above the dock, with folders and search.", R),
        ("Search", "Apps, files, settings pages and calculations in one place.", R),
        ("Answers from AI in search", "Off by default. Works only with your own key and always says who receives your question.", R),
        ("Control Center", "Wi-Fi, Bluetooth, sound, brightness, dark mode and media controls.", R),
        ("Island", "Media, volume and brightness, plus a live indicator when the microphone or camera is in use.", R),
        ("Clipboard history", "Searchable and stored only on your computer.", R),
        ("Selvara Glass", "Translucent surfaces with adjustable strength and a Reduce transparency option.", R),
        ("Light, dark and accent colour", "Switch in one click. Wallpapers and icons follow.", R),
        ("Rounded windows", "Soft corners on every window.", P),
        ("Dock stacks and drag and drop", "Folders that fan out, files dropped onto apps, apps dragged in to pin.", L),
        ("Control Center you can rearrange", "Add, remove and reorder modules, or pin them to the top bar.", L),
        ("Window snapping and several desktops", "Drag windows to edges and corners, move between desktops with gestures.", L),
        ("Focus modes", "Work, Personal, Sleep: choose which apps and people can reach you.", L),
    ]),
    ("Apps", [
        ("Terminal", "Fast and minimal, with an automatic fallback for older graphics.", R),
        ("Settings", "Our own app with grouped pages and changes that apply at once.", P),
        ("Files", "Instant preview with the space bar, column and gallery views, a clean sidebar.", L),
        ("Store", "Apps from Flathub and Debian in one list, with clear permissions.", L),
        ("Preview, Text Editor, Notes, Reminders, Calendar", "Simple everyday apps that keep your data on your computer.", L),
        ("Keychain and Backup", "See your saved passwords. Automatic, encrypted backups you can browse by date.", L),
    ]),
    ("Privacy and security", [
        ("No telemetry, tested", "Network traffic is recorded on every build. The expected number of outgoing connections is zero.", R),
        ("Firewall and app confinement", "Incoming connections are blocked and no service is open to the network.", R),
        ("Network Guard", "See which app connects where, and block any app with one switch.", L),
        ("App permissions", "Camera, microphone, screen, files and location: asked the first time, listed per app.", L),
        ("Disk encryption", "Offered when you install.", L),
    ]),
    ("System", [
        ("Silent start-up", "A clean splash from power-on to login, with no scrolling text.", R),
        ("Start-up menu", "Hidden until you need it, in the same design as the rest of the system.", R),
        ("Protection when memory runs low", "Compressed memory and safeguards against freezes on 4 GB machines.", R),
        ("Accessibility", "Screen reader, zoom, reduced motion and transparency, sticky keys.", R),
        ("Installer", "Install from a USB stick, on its own or next to your current system.", P),
        ("Languages", "English and Italian today. French, German, Spanish and Dutch next.", P),
        ("Snapshots and roll back", "Return to the state before an update from the start-up menu.", L),
        ("Updates without interruptions", "Never a forced restart. You choose when.", L),
        ("System drivers", "Graphics and Wi-Fi drivers offered with a clear explanation.", L),
        ("Drop and phone link", "Send files to nearby devices, compatible with LocalSend, and see phone notifications on your desktop.", L),
        ("Migration assistant", "Bring files and bookmarks from your old computer.", L),
    ]),
]
count = {s: sum(1 for _, items in GROUPS for *_, st in items if st == s) for s in (R, P, L)}
bar_css = "".join(f".bar .b-{s}{{flex:{count[s]} 1 0}}\n" for s in (R, P, L))


def frows(items):
    return '<ul class="frows">' + "".join(
        f'<li><div><strong>{t}</strong><span class="d">{d}</span></div>'
        f'<span class="st st-{s}">{LABEL[s]}</span></li>' for t, d, s in items) + "</ul>"


FEATURES = f"""
<section class="wrap page-head">
  <h1>What's inside</h1>
  <p class="lead">An honest list. Each feature is marked as working in development builds, being built now, or planned.</p>
  <div class="tally">
    <div class="bar" role="img" aria-label="{count[R]} working, {count[P]} in progress, {count[L]} planned"><span class="b-ready"></span><span class="b-progress"></span><span class="b-planned"></span></div>
    <ul class="key"><li class="st st-ready">{count[R]} working</li><li class="st st-progress">{count[P]} in progress</li><li class="st st-planned">{count[L]} planned</li></ul>
  </div>
</section>
<section class="wrap">
  {"".join(f'<div class="fgroup"><h2>{name}</h2>{frows(items)}</div>' for name, items in GROUPS)}
</section>
"""

# ------------------------------------------------------------------ privacy
PRIVACY = f"""
<section class="wrap page-head">
  <h1>Your computer works for you</h1>
  <p class="lead">Privacy is the first rule every part of SelvaraOS follows. Here is what that means in practice.</p>
</section>
<section class="wrap band-tight rule">
  {terms([
      ("No telemetry", "SelvaraOS collects no usage data, no crash data and no identifiers. There is no account to create."),
      ("Nothing connects unless you ask", "Checking for updates, setting the clock from the network and every other online feature is your choice, explained in plain words, and can be turned off."),
      ("Crash reports only if you send them", "When an app crashes you can choose to report it. You read the whole report first, and it goes to our public issue tracker."),
      ("Your browser, your choice", "The installer asks which browser you want and applies privacy-respecting settings."),
      ("AI is optional and open about it", "Search can answer questions with AI only after you add your own key. It always names the provider that receives your question."),
      ("Free software you can inspect", "Everything we write is public under the GPL-3.0 licence, so anyone can check these claims."),
  ])}
</section>
<section class="band rule">
  <div class="wrap split">
    <div class="head">
      <h2>We test it, every time.</h2>
      <p class="lead">An automated test records all network traffic while a fresh system starts, logs in and sits idle for five minutes. A build that contacts any server fails.</p>
    </div>
    {REPORT}
  </div>
</section>
<section class="band rule">
  <div class="wrap">
    <div class="head"><h2>Planned: see and control every connection.</h2></div>
    {terms([
        ("Network Guard", "A list of which app connected to which server, when, and how much data it used. One switch blocks any app."),
        ("App permissions", "Apps ask before using your camera, microphone, screen, files or location. Change your mind at any time in Settings."),
    ])}
  </div>
</section>
<section class="band rule">
  <div class="wrap closing">
    <h2>This website follows the same rule.</h2>
    <p class="lead">No cookies, no scripts, no analytics, and no fonts or files from other companies.</p>
  </div>
</section>
"""

# ------------------------------------------------------------------ releases
RELEASES = f"""
<section class="wrap page-head">
  <h1>Releases</h1>
  <p class="lead">Every SelvaraOS release will be listed here, betas included. There isn't one yet: the first will be SelvaraOS Canopy Beta 1, with a release candidate planned for the second half of December.</p>
  <div class="actions">
    <a class="btn btn-primary" href="{TESTER_FORM}" rel="noopener">Become a beta tester</a>
    <a class="btn btn-quiet" href="{DISCORD}" rel="noopener">Join the Discord</a>
    <a class="btn btn-quiet" href="news/straight-to-canopy-beta-1.html">Read the latest plan</a>
  </div>
</section>
<section class="band rule">
  <div class="wrap">
    <div class="head"><h2>Release plan</h2><p class="lead">Estimates, and they may move.</p></div>
    <ol class="timeline">
      <li class="now"><span class="when">Soon</span><h3>Nightly builds</h3><p>For approved beta testers. Install once, and a new build arrives every night and installs when you restart.</p></li>
      <li><span class="when">Late December</span><h3>Canopy Beta 1 release candidate</h3><p>The first build everyone can download, for PCs with Intel or AMD processors.</p></li>
      <li><span class="when">Next</span><h3>Canopy Beta 1 and Beta 2</h3><p>The release candidate with the last problems fixed, then the final step before stable.</p></li>
      <li><span class="when">When it's ready</span><h3>SelvaraOS Canopy 1.0</h3><p>The stable release, tested on real hardware by real people.</p></li>
      <li><span class="when">Later</span><h3>Canopy 1.5</h3><p>Native support for Apple Silicon Macs.</p></li>
    </ol>
  </div>
</section>
<section class="band rule">
  <div class="wrap">
    <div class="head"><h2>Become a beta tester</h2><p class="lead">Approved testers get nightly builds before the public betas. They update themselves, and there is never a downgrade: if you leave the nightly channel, your computer stays where it is until the next public beta catches up.</p></div>
    <div class="actions">
      <a class="btn btn-primary" href="{TESTER_FORM}" rel="noopener">Apply now</a>
    </div>
  </div>
</section>
<section class="band rule">
  <div class="wrap">
    <div class="head"><h2>What you'll need</h2><p class="lead">Expected requirements for the first release.</p></div>
    <dl class="reqs">
      <div><dt>Processor</dt><dd>64-bit Intel or AMD</dd></div>
      <div><dt>Memory</dt><dd>4 GB or more</dd></div>
      <div><dt>Storage</dt><dd>25 GB free</dd></div>
      <div><dt>To install</dt><dd>A USB stick, 8 GB</dd></div>
    </dl>
  </div>
</section>
<section class="band rule">
  <div class="wrap closing">
    <h2>Join the official Discord server for updates.</h2>
    <p class="lead">Be the first to hear about new builds, see previews and talk with the people making SelvaraOS.</p>
    <div class="actions">
      <a class="btn btn-primary" href="{DISCORD}" rel="noopener">Join the Discord</a>
      <a class="btn btn-quiet" href="{GITHUB}" rel="noopener">Open GitHub</a>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ screenshots
# Layout: screenshots/<Dark|Light>/<YYYY-MM-DD>/<NN-name>.<png|jpg|webp>
# The date folder is the day the screenshots were taken; newest first on the page.
# Inside a day they are sorted by file name. The caption comes from the name:
# "03-control-center.png" becomes "Control Center".
SHOT_EXT = {".png", ".jpg", ".jpeg", ".webp"}
SHOT_FULL, SHOT_THUMB = 1920, 800
SHOT_THEMES = ("Dark", "Light")
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def shot_caption(stem):
    words = re.sub(r"^\d+[-_ ]*", "", stem).replace("_", " ").replace("-", " ").split()
    return html.escape(" ".join(w[:1].upper() + w[1:] for w in words) if words else stem)


def shot_date(name, where):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", name)
    if not m or not (1 <= int(m.group(2)) <= 12 and 1 <= int(m.group(3)) <= 31):
        sys.exit(f"{where}: date folders must be named YYYY-MM-DD, like 2026-11-15")
    y, mo, d = (int(x) for x in m.groups())
    return f"{d} {MONTHS[mo - 1]} {y}"


shot_root = SRC / "screenshots"
(OUT / "screenshots").mkdir(parents=True, exist_ok=True)
for f in sorted(shot_root.glob("*")) if shot_root.exists() else []:
    if f.name.startswith(".") or f.name.lower() == "readme.md":
        continue
    if not (f.is_dir() and f.name.lower() in ("dark", "light")):
        sys.exit(f"screenshots/{f.name}: put screenshots in screenshots/Dark/<date>/ or screenshots/Light/<date>/")

shot_sections, shot_total = [], 0
for theme in SHOT_THEMES:
    tdir = next((d for d in shot_root.glob("*") if d.is_dir() and d.name.lower() == theme.lower()), None) if shot_root.exists() else None
    if tdir is None:
        continue
    days = []
    for ddir in sorted((d for d in tdir.iterdir() if not d.name.startswith(".")), key=lambda d: d.name, reverse=True):
        where = f"screenshots/{tdir.name}/{ddir.name}"
        if not ddir.is_dir():
            sys.exit(f"{where}: put screenshots inside a date folder, like screenshots/{tdir.name}/2026-11-15/")
        nice = shot_date(ddir.name, where)
        items = []
        for f in sorted(ddir.iterdir(), key=lambda x: x.name.lower()):
            if f.name.startswith(".") or f.suffix.lower() not in SHOT_EXT:
                continue
            try:
                im = Image.open(f)
                im.load()
            except Exception:
                sys.exit(f"{where}/{f.name}: this file can't be opened as an image")
            im = im.convert("RGB")
            stem = re.sub(r"[^a-z0-9]+", "-", f.stem.lower()).strip("-") or "screenshot"
            slug = f"{theme.lower()}-{ddir.name}-{stem}"
            for width, name in ((SHOT_FULL, f"{slug}.webp"), (SHOT_THUMB, f"{slug}-sm.webp")):
                out = im if im.width <= width else im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
                out.save(OUT / "screenshots" / name, quality=86, method=6)
            cap = shot_caption(f.stem)
            items.append(
                f'<figure><a class="frame" href="screenshots/{slug}.webp">'
                f'<img src="screenshots/{slug}-sm.webp" alt="{cap}, {theme.lower()} theme, {nice}" loading="lazy"></a>'
                f'<figcaption>{cap} <span class="shot-date">{nice}</span></figcaption></figure>')
        if items:
            shot_total += len(items)
            days.append(f'<h3 class="shot-day">Taken {nice}</h3><div class="shots">{"".join(items)}</div>')
    if days:
        shot_sections.append(f'<section class="band" id="{theme.lower()}"><div class="wrap">'
                             f'<h2 class="shot-theme">{theme}</h2>{"".join(days)}</div></section>')

shot_jump = " ".join(f'<a class="btn btn-quiet" href="#{t.lower()}">{t}</a>' for t in SHOT_THEMES
                     if f'id="{t.lower()}"' in "".join(shot_sections))
SHOTS = f"""
<section class="wrap page-head">
  <h1>Screenshots</h1>
  <p class="lead">SelvaraOS as it looks today, straight from current development builds.</p>
  <div class="shot-note">
    <p><strong>SelvaraOS is still changing.</strong> If you see anything unpolished or inconsistent in these screenshots, it's already on my list and will be fixed before Beta 1.</p>
    <p>If some of them show CachyOS as the host, it's because they were taken while testing the new shell on my main PC, which runs CachyOS.</p>
  </div>
  {f'<div class="shot-jump">{shot_jump}</div>' if shot_jump else ''}
</section>
{"".join(shot_sections) if shot_total else '<section class="band"><div class="wrap"><p class="lead">No screenshots yet. Check back soon.</p></div></section>'}
{'<section class="wrap"><p class="fine">Click a screenshot to open it at full size.</p></section>' if shot_total else ''}
"""

# ------------------------------------------------------------------ faq
QA = [
    ("Is SelvaraOS free?", "Yes. It is free to download and use, and everything we write is free software under the GPL-3.0 licence."),
    ("Do I need to know Linux?", "No. SelvaraOS is designed for people who have never used Linux. Everyday tasks never need a terminal."),
    ("Will it run on my old computer?", "If it has a 64-bit Intel or AMD processor and at least 4 GB of memory, it is a computer we build for. We measure performance on a machine like that on every build."),
    ("Is it a copy of macOS?", "No. The design and the code are our own. If you come from a Mac, the layout and the shortcuts will feel familiar, which makes switching easier."),
    ("What is it built on?", "Debian 13, one of the most stable Linux distributions, and the KWin compositor. The desktop, the settings and the system apps are written by us."),
    ("Does it collect any data?", "No. There is no telemetry, and nothing connects to the internet unless you ask. An automated test checks this on every build."),
    ("Can I install the apps I use?", "Yes. Thousands of apps are available from Flathub and Debian, and the installer lets you pick popular apps and your browser before you start."),
    ("Can I keep Windows next to it?", "Yes. The installer will let you install SelvaraOS alongside the system you already have."),
    ("When will it be released?", "The release candidate of SelvaraOS Canopy Beta 1, the first public release, is planned for the second half of December. Approved beta testers get nightly builds before that."),
    ("How do I become a beta tester?", f'Fill in the <a href="{TESTER_FORM}" rel="noopener">beta tester application</a>. We review every application and email you if you are in.'),
    ("Will it run on a Mac?", "Native support for Apple Silicon Macs is planned for SelvaraOS Canopy 1.5."),
]
FAQ = f"""
<section class="wrap page-head"><h1>Questions and answers</h1></section>
<section class="wrap faq">
  {"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in QA)}
</section>
"""

NOTFOUND = """
<section class="wrap page-head">
  <h1>This page doesn't exist</h1>
  <p class="lead">The address may be mistyped, or the page may have moved.</p>
  <div class="actions"><a class="btn btn-primary" href="index.html">Go to the home page</a></div>
</section>
"""

page("index.html", "SelvaraOS",
     "SelvaraOS is a free, private desktop operating system: smooth on older PCs and easy for everyone.", HOME)
page("features.html", "SelvaraOS features",
     "Everything inside SelvaraOS, with an honest status for each feature.", FEATURES)
page("privacy.html", "SelvaraOS privacy",
     "No telemetry, nothing connects unless you ask, tested on every build.", PRIVACY)
page("releases.html", "SelvaraOS releases",
     "Every SelvaraOS release, the release plan and how to become a beta tester.", RELEASES)
page("screenshots.html", "SelvaraOS screenshots",
     "Screenshots of SelvaraOS from current development builds.", SHOTS)
page("faq.html", "SelvaraOS questions and answers",
     "Frequently asked questions about SelvaraOS.", FAQ)
page("404.html", "Page not found, SelvaraOS", "This page doesn't exist.", NOTFOUND)

# ------------------------------------------------------------------ news pages
NEWS_HEAD = """
<section class="wrap page-head">
  <h1>News</h1>
  <p class="lead">Releases, announcements and notes from building SelvaraOS.</p>
  <p class="fine"><a href="feed.xml">Follow with RSS</a></p>
</section>
"""
pages = [POSTS[i:i + POSTS_PER_PAGE] for i in range(0, len(POSTS), POSTS_PER_PAGE)] or [[]]
for n, chunk in enumerate(pages, 1):
    name = "news.html" if n == 1 else f"news-{n}.html"
    items = "".join(news_item(p) for p in chunk) or '<li class="news-empty muted">No posts yet.</li>'
    pager = ""
    if len(pages) > 1:
        links = "".join(
            f'<a href="{"news.html" if k == 1 else f"news-{k}.html"}"'
            f'{" aria-current=\"page\"" if k == n else ""}>{k}</a>' for k in range(1, len(pages) + 1))
        pager = f'<nav class="pager" aria-label="News pages">{links}</nav>'
    title = "SelvaraOS news" if n == 1 else f"SelvaraOS news, page {n}"
    page(name, title, "Releases, announcements and notes from building SelvaraOS.",
         NEWS_HEAD + f'<section class="wrap news-page"><ol class="news-list">{items}</ol>{pager}</section>',
         current="news.html")

for p in POSTS:
    cover = ""
    if p["cover"]:
        cover = (f'<figure class="post-cover"><div class="frame"><img src="{p["cover"]}" width="16" height="9" '
                 f'alt="{p["cover_alt"]}"></div></figure>')
    body = f"""
<article class="wrap post">
  <header class="post-head">
    {meta_line(p)}
    <h1>{p["title"]}</h1>
    <p class="byline">{p["author"]}</p>
  </header>
  {cover}
  <div class="prose">{p["body"]}</div>
  <footer class="post-foot">
    <p class="muted">Questions or ideas about this post?</p>
    <div class="actions">
      <a class="btn btn-primary" href="{DISCORD}" rel="noopener">Discuss on Discord</a>
      <a class="btn btn-quiet" href="../news.html">All news</a>
    </div>
  </footer>
</article>
"""
    plain = re.sub(r"<[^>]+>", "", p["summary"])
    page(p["url"], f'{p["title"]}, SelvaraOS', plain, body, current="news.html")

# Atom feed, full content with absolute links
def absolute(content):
    return re.sub(r'(src|href)="(?![a-z]+:|#)([^"]+)"',
                  lambda m: f'{m.group(1)}="{urljoin(SITE_URL + "news/", m.group(2))}"', content)


updated = (POSTS[0]["date"] if POSTS else datetime.date.today()).isoformat()
entries = "".join(f"""
  <entry>
    <title type="html">{html.escape(p["title"])}</title>
    <link href="{SITE_URL}{p["url"]}"/>
    <id>{SITE_URL}{p["url"]}</id>
    <published>{p["date"].isoformat()}T00:00:00Z</published>
    <updated>{p["date"].isoformat()}T00:00:00Z</updated>
    <author><name>{p["author"]}</name></author>
    <category term="{p["category"]}"/>
    <summary type="html">{html.escape(p["summary"])}</summary>
    <content type="html">{html.escape(absolute(p["body"]))}</content>
  </entry>""" for p in POSTS[:20])
(OUT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>SelvaraOS news</title>
  <subtitle>Releases, announcements and notes from building SelvaraOS.</subtitle>
  <link href="{SITE_URL}feed.xml" rel="self"/>
  <link href="{SITE_URL}news.html"/>
  <id>{SITE_URL}news.html</id>
  <updated>{updated}T00:00:00Z</updated>{entries}
</feed>
""")

# generated CSS for the tally bar (kept out of inline styles for the CSP)
css = (SRC / "assets/style.css").read_text()
css = re.sub(r"/\* tally:start \*/.*?/\* tally:end \*/\n?", "", css, flags=re.S)
(OUT / "assets/style.css").write_text(css.rstrip() + f"\n/* tally:start */\n{bar_css}/* tally:end */\n")

# real image dimensions on every page
for f in OUT.rglob("*.html"):
    s = f.read_text()

    def fix(m, f=f):
        src = m.group(2)
        if re.match(r"[a-z]+:", src):
            return m.group(0)
        target = (f.parent / src).resolve()
        if not target.is_file():
            sys.exit(f"{f.relative_to(OUT)}: image not found: {src}")
        w, h = Image.open(target).size
        tag = re.sub(r'\s(width|height)="\d+"', "", m.group(0))
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)
    f.write_text(re.sub(r'<img ([^>]*?)src="([^"]+)"[^>]*>', fix, s))

(OUT / "assets/img/favicon.svg").write_text(
    LOGO.replace('<svg viewBox', '<svg xmlns="http://www.w3.org/2000/svg" viewBox').replace(' aria-hidden="true"', ''))
(OUT / ".nojekyll").write_text("")
# old address of the releases page
(OUT / "download.html").write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>SelvaraOS releases</title>'
    '<meta http-equiv="refresh" content="0; url=releases.html"><link rel="canonical" href="'
    f'{SITE_URL}releases.html"></head><body><p><a href="releases.html">SelvaraOS releases</a></p></body></html>\n')
print("built", count, f"{len(POSTS)} news posts")
