#!/usr/bin/env python3
"""Regenerate a per-pedal marketing page for every audited profile.

    python3 build_pedal_pages.py

The audited-and-shipped set comes from AVAILABLE_IDS + AVAILABLE_PREFIXES
in build_profiles_page.py (single source of truth). Per-pedal one-liners
come from the "now" tuples in build_brand_pages.py (no new copy is
authored here). Everything else — machine names, control counts,
preset slots — is read from the profile JSON.

Emits: PedalEditor/{brand-slug}/{pedal-slug}/index.html

Screenshots: if PedalEditor/screenshots/iphone/{pedal-slug}.png (or .jpg)
exists, it's wired in; otherwise a labelled placeholder frame renders.
Same for iPad.
"""

import datetime
import glob
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_ROOT = os.path.join(HERE, "PedalEditor")
PROFILE_DIR = os.path.join(
    os.path.dirname(HERE), "PedalEditor",
    "PedalEditorCore", "Sources", "PedalEditorCore",
    "Resources", "PedalProfiles",
)
SHOTS_DIR = os.path.join(OUT_ROOT, "screenshots")

sys.path.insert(0, HERE)
from build_profiles_page import AVAILABLE_IDS, AVAILABLE_PREFIXES, is_available
import build_brand_pages as bbp


# JSON id prefix → (site brand slug, human brand name)
BRAND_MAP = {
    "strymon-":    ("strymon",      "Strymon"),
    "walrus-":     ("walrus-audio", "Walrus Audio"),
    "meris-":      ("meris",        "Meris"),
    "uafx-":       ("uafx",         "UAFX"),
    "line6-":      ("line-6",       "Line 6"),
    "chasebliss-": ("chase-bliss",  "Chase Bliss"),
    "hologram-":   ("hologram",     "Hologram"),
    "eventide-":   ("eventide",     "Eventide"),  # excluded via AVAILABLE
}

SKIP_IDS = {"custom-midi"}  # not a pedal, no per-pedal page


def brand_for(pid):
    for prefix, (slug, name) in BRAND_MAP.items():
        if pid.startswith(prefix):
            return prefix, slug, name
    return None, None, None


def slugify_name(name):
    """Turn a brand-page display name into the same slug used in the JSON id."""
    s = html.unescape(name)  # &rsquo; → ’, &#8209; → non-breaking hyphen
    s = s.replace("\u2019", "").replace("'", "")  # curly and straight apostrophes
    s = s.replace("\u2011", "-")                  # non-breaking hyphen → dash
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def norm_name(name):
    """Aggressively normalise a display name for cross-source matching."""
    s = html.unescape(name)
    s = re.sub(r"[^A-Za-z0-9]+", "", s).lower()
    return s


def load_brand_copy():
    """Return {json_id: (display_name, one_liner)} by matching each brand-page
    display name to a profile JSON's `name` field, per brand."""
    # {brand_slug: [(display_name, desc), ...]}
    by_brand = {b["slug"]: b.get("now", []) for b in bbp.BRANDS}

    # {brand_slug: {norm_json_name: pid}}
    profiles_by_brand = {}
    for path in glob.glob(os.path.join(PROFILE_DIR, "*.json")):
        pid = os.path.basename(path)[:-5]
        prefix, bslug, _ = brand_for(pid)
        if not bslug:
            continue
        try:
            with open(path) as fh:
                jname = json.load(fh).get("name", "")
        except Exception:
            continue
        profiles_by_brand.setdefault(bslug, {})[norm_name(jname)] = pid

    out = {}
    for bslug, entries in by_brand.items():
        lookup = profiles_by_brand.get(bslug, {})
        for entry in entries:
            # `now` tuples were 2-tuples (name, desc) originally; a later
            # revision added an explicit slug: (name, slug, desc). Accept both.
            if len(entry) == 3:
                display_name, _slug, desc = entry
            else:
                display_name, desc = entry
            key = norm_name(display_name)
            pid = lookup.get(key)
            if pid:
                out[pid] = (display_name, desc)
    return out


def load_profile(pid):
    with open(os.path.join(PROFILE_DIR, pid + ".json")) as fh:
        return json.load(fh)


def machine_rows(profile):
    """Return [(machine_name, control_count), ...] and the total control count."""
    rows = []
    total = len(profile.get("globalParameters", []))
    for cat in profile.get("effectCategories", []):
        for alg in cat.get("algorithms", []):
            params = len(alg.get("parameters", []))
            rows.append((alg.get("name", cat.get("name", "?")), params))
            total += params
    return rows, total


def find_shot(pedal_slug, kind):
    """Return the site-relative path to a screenshot, or None."""
    for ext in ("png", "jpg", "jpeg", "webp"):
        rel = f"screenshots/{kind}/{pedal_slug}.{ext}"
        if os.path.isfile(os.path.join(OUT_ROOT, rel)):
            return "../../" + rel
    return None


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brand} {display_name} &mdash; PedalEditor | Meaningful Sound</title>
<meta name="description" content="{brand} {display_name_plain} in PedalEditor. {desc_plain} Control it from iPhone, iPad or Mac over Bluetooth.">
<meta name="author" content="Meaningful Sound">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#e8dfc8">
<link rel="canonical" href="https://meaningfulsound.net/PedalEditor/{bslug}/{pslug}/">
<link rel="alternate" type="text/markdown" title="LLM-friendly summary" href="/llms.txt">
<meta name="apple-itunes-app" content="app-id=6761016084, app-argument=https://meaningfulsound.net/PedalEditor/{bslug}/{pslug}/">

<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Meaningful Sound">
<meta property="og:title" content="{brand} {display_name} &mdash; PedalEditor">
<meta property="og:description" content="{desc_plain}">
<meta property="og:url" content="https://meaningfulsound.net/PedalEditor/{bslug}/{pslug}/">
<meta property="og:image" content="https://meaningfulsound.net/PedalEditor/images/banner.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{brand} {display_name} &mdash; PedalEditor">
<meta name="twitter:description" content="{desc_plain}">
<meta name="twitter:image" content="https://meaningfulsound.net/PedalEditor/images/banner.jpg">

<script type="application/ld+json">
{jsonld}
</script>

<style>
:root{{
  --sand:#e8dfc8; --sand-deep:#ded2b6; --cream:#f4eee1;
  --ink:#3a2a1e; --ink-soft:#6b5644; --muted:#8d7a63;
  --terracotta:#c0553a; --gold:#8a6f3d; --line:#d3c6a8;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --sans:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Helvetica,Arial,sans-serif;
}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:var(--sand);color:var(--ink)}}
body{{font-family:var(--sans);line-height:1.65;-webkit-font-smoothing:antialiased}}
img{{max-width:100%;display:block}}
a{{color:inherit}}

.banner{{width:100%;background:var(--sand)}}
.banner img{{width:100%;height:auto}}

.wrap{{max-width:820px;margin:0 auto;padding:0 24px;text-align:center}}
.eyebrow{{font-size:.72em;font-weight:700;text-transform:uppercase;letter-spacing:3px;
  color:var(--muted);margin:0 0 18px}}
.eyebrow a{{text-decoration:none}}
.eyebrow .sep{{color:var(--line);margin:0 8px}}

h1{{font-family:var(--serif);font-size:3.3em;line-height:1.04;letter-spacing:-1px;margin:0 0 12px;font-weight:700}}
.byline{{font-size:.9em;font-weight:600;text-transform:uppercase;letter-spacing:3px;color:var(--gold);margin:0 0 18px}}
.lede{{font-size:1.18em;color:var(--ink-soft);margin:0 auto 30px;max-width:33em;font-weight:300}}
.title-card{{padding:56px 0 8px;border-bottom:1px solid var(--line)}}
.title-card .rule{{width:64px;height:1px;background:var(--terracotta);margin:0 auto 26px}}

.pill{{display:inline-block;padding:10px 20px;border-radius:999px;font-size:.9em;font-weight:600;
  text-decoration:none;border:1px solid var(--ink);color:var(--ink);background:transparent;
  transition:background .15s ease,color .15s ease}}
.pill:hover{{background:var(--ink);color:var(--cream)}}
.pill.filled{{background:var(--terracotta);border-color:var(--terracotta);color:#fff}}
.pill.filled:hover{{background:#a8452e;border-color:#a8452e}}
.links{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px;justify-content:center}}

h2{{font-family:var(--sans);font-weight:700;text-transform:uppercase;font-size:.72em;letter-spacing:3px;
  color:var(--gold);margin:62px 0 22px;display:flex;align-items:center;gap:16px}}
h2::before,h2::after{{content:"";flex:1;height:1px;background:var(--line)}}

.shots{{--shot-h:440px;display:flex;gap:18px;justify-content:center;align-items:flex-end;flex-wrap:wrap;
  width:min(96vw,960px);margin-left:calc((100% - min(96vw,960px)) / 2)}}
.shot{{background:var(--cream);border:1px solid var(--line);border-radius:4px;padding:14px;
  display:flex;flex-direction:column;align-items:center;gap:10px}}
.shot .frame{{height:var(--shot-h);background:var(--sand-deep);border:1px solid var(--line);border-radius:6px;
  color:var(--muted);font-size:.78em;font-weight:600;text-transform:uppercase;letter-spacing:2px;
  display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.shot .frame img{{height:100%;width:auto;display:block}}
.shot.iphone .frame{{width:calc(var(--shot-h) * 9 / 19.5)}}
.shot.ipad .frame{{width:calc(var(--shot-h) * 4 / 3)}}
.shot .caption{{font-size:.72em;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:var(--muted)}}

.machines{{background:var(--cream);border:1px solid var(--line);border-radius:4px;padding:24px 26px;text-align:left}}
.machines h3{{font-family:var(--serif);font-size:1.24em;margin:0 0 14px;font-weight:700;letter-spacing:-.2px;text-align:center}}
.machines ul{{list-style:none;margin:0;padding:0;
  display:grid;grid-template-columns:repeat(2,1fr);gap:6px 24px}}
.machines.solo ul{{grid-template-columns:1fr;max-width:24em;margin:0 auto}}
.machines li{{display:flex;justify-content:space-between;gap:12px;font-size:.95em;
  color:var(--ink-soft);padding:4px 0;border-bottom:1px dotted var(--line)}}
.machines li .n{{color:var(--muted);font-variant-numeric:tabular-nums}}
.globals{{margin-top:14px;text-align:center;font-size:.9em;color:var(--muted)}}
.globals strong{{color:var(--ink);font-weight:600}}

.facts p{{color:var(--ink-soft);max-width:34em;margin:0 auto 16px}}
.facts .price{{border-top:1px solid var(--line);padding-top:22px;margin-top:26px;color:var(--ink)}}

footer{{margin-top:80px;border-top:1px solid var(--line);padding:24px 0 64px;font-size:.78em;
  color:var(--muted);display:flex;gap:20px;flex-wrap:wrap;align-items:center;
  justify-content:center;text-transform:uppercase;letter-spacing:2px}}
footer a{{text-decoration:none}}
footer a:hover{{color:var(--ink)}}
.updated{{width:100%}}

@media(max-width:720px){{
  h1{{font-size:2.4em}}
  .title-card{{padding-top:36px}}
  .shots{{--shot-h:360px}}
  .machines ul{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>

<div class="banner">
  <img src="../../images/banner.jpg" width="1211" height="471" alt="The PedalEditor app icon floating above a desert at dusk">
</div>

<div class="wrap">

  <div class="title-card">
    <p class="eyebrow"><a href="../../">PedalEditor</a><span class="sep">&middot;</span><a href="../">{brand}</a></p>
    <div class="rule"></div>
    <h1>{display_name}</h1>
    <p class="byline">{byline}</p>
    <p class="lede">{desc}</p>
    <div class="links">
      <a class="pill filled" href="https://apps.apple.com/us/app/pedaleditor/id6761016084">App Store</a>
      <a class="pill" href="../">All {brand_short}</a>
    </div>
  </div>

  <h2>In the app</h2>
  <div class="shots">
    <div class="shot iphone">
      <div class="frame">{iphone_frame}</div>
      <p class="caption">iPhone</p>
    </div>
    <div class="shot ipad">
      <div class="frame">{ipad_frame}</div>
      <p class="caption">iPad</p>
    </div>
  </div>

  <h2>What&rsquo;s inside</h2>
  <div class="machines{solo_cls}">
    <h3>{machines_heading}</h3>
    <ul>
{machine_lis}
    </ul>
    <p class="globals">Plus <strong>{globals_n} global controls</strong> shared across every machine &mdash; tap tempo, expression, bypass mode, MIDI channel, and the rest.</p>
  </div>

  <h2>Facts</h2>
  <div class="facts">
    <p>Available on iPhone, iPad and Mac. Connects over Bluetooth LE MIDI (with a WIDI Jack or equivalent), Wi&#8209;Fi (RTP&#8209;MIDI) or USB. Bluetooth pairing happens inside the app on iPhone and iPad; on Mac you pair in Audio MIDI Setup.</p>
    <p>Presets live in the app library. Save what you want to the pedal from any preset, in any order. Every knob on the front of the {display_name} and every parameter behind it are on the same screen.</p>
    <p class="price">Built from the {brand} {display_name} user manual and audited before it shipped. <a href="../">The rest of the {brand_short} line is here.</a></p>
  </div>

  <footer>
    <a href="../../">PedalEditor</a>
    <a href="/">Meaningful Sound</a>
    <a href="../">{brand_short}</a>
    <a href="../../reference/">Reference</a>
    <a href="../../privacy/">Privacy</a>
    <a href="https://instagram.com/pedaleditor">Instagram</a>
    <span class="updated">Updated {today}</span>
  </footer>

</div>
</body>
</html>
"""


def strip_html(s):
    """Turn brand-page HTML-ish copy into plain text safe for meta tags."""
    s = html.unescape(s)
    s = s.replace("\u2019", "'").replace("\u2011", "-")
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build_jsonld(brand_name, brand_slug, display_name, pedal_slug, desc_plain):
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "PedalEditor",
             "item": "https://meaningfulsound.net/PedalEditor/"},
            {"@type": "ListItem", "position": 2, "name": brand_name,
             "item": f"https://meaningfulsound.net/PedalEditor/{brand_slug}/"},
            {"@type": "ListItem", "position": 3, "name": strip_html(display_name),
             "item": f"https://meaningfulsound.net/PedalEditor/{brand_slug}/{pedal_slug}/"},
        ],
    }
    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": f"{brand_name} {strip_html(display_name)}",
        "brand": {"@type": "Brand", "name": brand_name},
        "category": "Musical Instrument Accessory",
        "description": desc_plain,
        "url": f"https://meaningfulsound.net/PedalEditor/{brand_slug}/{pedal_slug}/",
        "image": "https://meaningfulsound.net/PedalEditor/images/banner.jpg",
        "isRelatedTo": {
            "@type": "MobileApplication",
            "name": "PedalEditor",
            "applicationCategory": "MusicApplication",
            "url": "https://meaningfulsound.net/PedalEditor/",
        },
    }
    return json.dumps([breadcrumbs, product], indent=2, ensure_ascii=False)


def render_page(pid, profile, brand_slug, brand_name, display_name, desc):
    pedal_slug = pid[pid.index("-") + 1:]  # e.g. walrus-r1-mkii → r1-mkii
    # For chasebliss- / line6- the JSON prefix is one token; peel it off:
    for prefix in BRAND_MAP:
        if pid.startswith(prefix):
            pedal_slug = pid[len(prefix):]
            break

    rows, total_controls = machine_rows(profile)
    globals_n = len(profile.get("globalParameters", []))
    machines_n = len(rows)

    if machines_n <= 1:
        machines_heading = f"{total_controls} controls" if machines_n == 1 else f"{globals_n} controls"
        solo_cls = " solo"
    else:
        machines_heading = f"{machines_n} machines"
        solo_cls = ""

    machine_lis = "\n".join(
        f'      <li><span>{html.escape(name)}</span>'
        f'<span class="n">{n} control{"s" if n != 1 else ""}</span></li>'
        for name, n in rows
    )
    if not machine_lis:
        machine_lis = f'      <li><span>{html.escape(display_name)}</span><span class="n">{globals_n} controls</span></li>'

    byline_parts = []
    if machines_n > 1:
        byline_parts.append(f"{machines_n} machines")
    byline_parts.append(f"{total_controls} controls")
    byline = " &middot; ".join(byline_parts)

    # Short brand name for tighter phrases ("All Strymon" vs "All Walrus Audio")
    brand_short = "Walrus" if brand_slug == "walrus-audio" else brand_name

    # Screenshots
    iphone = find_shot(pedal_slug, "iphone")
    ipad = find_shot(pedal_slug, "ipad")
    iphone_frame = (
        f'<img src="{iphone}" alt="{brand_name} {strip_html(display_name)} on iPhone in PedalEditor">'
        if iphone else "iPhone screenshot<br>coming soon"
    )
    ipad_frame = (
        f'<img src="{ipad}" alt="{brand_name} {strip_html(display_name)} on iPad in PedalEditor">'
        if ipad else "iPad screenshot<br>coming soon"
    )

    desc_plain = strip_html(desc)
    display_name_plain = strip_html(display_name)
    jsonld = build_jsonld(brand_name, brand_slug, display_name, pedal_slug, desc_plain)

    return pedal_slug, PAGE.format(
        brand=brand_name,
        brand_short=brand_short,
        bslug=brand_slug,
        pslug=pedal_slug,
        display_name=display_name,
        display_name_plain=display_name_plain,
        byline=byline,
        desc=desc,
        desc_plain=desc_plain,
        machines_heading=machines_heading,
        solo_cls=solo_cls,
        machine_lis=machine_lis,
        globals_n=globals_n,
        iphone_frame=iphone_frame,
        ipad_frame=ipad_frame,
        jsonld=jsonld,
        today=datetime.date.today().strftime("%-d %B %Y"),
    )


def main():
    copy = load_brand_copy()
    written = 0
    missing_copy = []
    skipped = []

    for path in sorted(glob.glob(os.path.join(PROFILE_DIR, "*.json"))):
        pid = os.path.basename(path)[:-5]
        if pid in SKIP_IDS or "AUTHORING" in pid.upper():
            continue
        if not is_available(pid):
            continue
        prefix, brand_slug, brand_name = brand_for(pid)
        if not brand_slug:
            skipped.append((pid, "unknown brand prefix"))
            continue
        if pid not in copy:
            missing_copy.append(pid)
            continue

        display_name, desc = copy[pid]
        profile = load_profile(pid)
        pedal_slug, html_out = render_page(pid, profile, brand_slug, brand_name, display_name, desc)

        out_dir = os.path.join(OUT_ROOT, brand_slug, pedal_slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w") as fh:
            fh.write(html_out)
        written += 1
        print(f"  wrote {brand_slug}/{pedal_slug}/")

    print(f"\n{written} pages written.")
    if missing_copy:
        print(f"\n{len(missing_copy)} available pedal(s) with no brand-page copy — skipped:")
        for pid in missing_copy:
            print(f"  - {pid}")
    if skipped:
        print("\nSkipped:")
        for pid, why in skipped:
            print(f"  - {pid}: {why}")


if __name__ == "__main__":
    main()
