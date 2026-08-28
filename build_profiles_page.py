#!/usr/bin/env python3
"""Regenerate PedalEditor/profiles/index.html from the app's bundled profile JSON.

Run after any profile is added or promoted:
    python3 build_profiles_page.py

Promoting a brand to Available Now: add its id prefix (or exact ids) to AVAILABLE.
"""

import collections
import datetime
import glob
import html
import json
import os

PROFILE_DIR = os.path.expanduser(
    "~/Developer/PedalEditor/PedalEditorCore/Sources/PedalEditorCore/"
    "Resources/PedalProfiles"
)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "PedalEditor", "profiles", "index.html")

AVAILABLE_PREFIXES = ("strymon-", "walrus-")
AVAILABLE_IDS = {
    "uafx-dream-65", "uafx-lion-68", "uafx-ruby-63", "uafx-woodrow-55",
    "uafx-knuckles-92", "uafx-anti-1992", "uafx-enigmatic-82",
    "line6-dl4-mkii", "meris-lvx", "custom-midi",
}


def is_available(pid):
    return pid.startswith(AVAILABLE_PREFIXES) or pid in AVAILABLE_IDS


def load():
    avail, deck = collections.defaultdict(list), collections.defaultdict(list)
    for path in sorted(glob.glob(os.path.join(PROFILE_DIR, "*.json"))):
        pid = os.path.basename(path)[:-5]
        if "AUTHORING" in pid.upper():
            continue
        try:
            with open(path) as fh:
                d = json.load(fh)
        except (ValueError, OSError):
            continue
        mfr = (d.get("manufacturer") or "Other").strip()
        model = (d.get("modelName") or d.get("name") or pid).strip()
        (avail if is_available(pid) else deck)[mfr].append(model)
    return avail, deck


def section(groups):
    out = []
    for mfr in sorted(groups, key=lambda m: m.lower()):
        models = sorted(groups[mfr], key=lambda s: s.lower())
        names = " &middot; ".join(html.escape(m) for m in models)
        out.append(
            '    <div class="brandblock">\n'
            f'      <h3>{html.escape(mfr)} <span class="n">{len(models)}</span></h3>\n'
            f'      <p>{names}</p>\n'
            "    </div>"
        )
    return "\n".join(out)


def main():
    avail, deck = load()
    n_avail = sum(len(v) for v in avail.values())
    n_deck = sum(len(v) for v in deck.values())
    updated = datetime.date.today().strftime("%-d %B %Y")

    page = TEMPLATE.format(
        n_avail=n_avail,
        n_deck=n_deck,
        n_total=n_avail + n_deck,
        n_avail_brands=len(avail),
        n_deck_brands=len(deck),
        available=section(avail),
        ondeck=section(deck),
        updated=updated,
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        fh.write(page)
    print(f"wrote {OUT}\n  available {n_avail} / on deck {n_deck} / total {n_avail + n_deck}")


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Every Profile &mdash; PedalEditor | Meaningful Sound</title>
<meta name="description" content="The complete PedalEditor profile reference: {n_avail} pedal profiles available now, from Strymon, Walrus Audio, Meris, UAFX and Line 6, plus {n_deck} more built and awaiting audit.">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#e8dfc8">
<link rel="canonical" href="https://meaningfulsound.net/PedalEditor/profiles/">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Meaningful Sound">
<meta property="og:title" content="Every Profile &mdash; PedalEditor">
<meta property="og:description" content="{n_avail} profiles available now, {n_deck} on deck.">
<meta property="og:url" content="https://meaningfulsound.net/PedalEditor/profiles/">
<style>
:root{{
  --sand:#e8dfc8; --cream:#f4eee1;
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
.title-card{{padding:64px 0 30px;border-bottom:1px solid var(--line)}}
.rule{{width:64px;height:1px;background:var(--terracotta);margin:0 auto 26px}}
h1{{font-family:var(--serif);font-size:3em;line-height:1.05;letter-spacing:-1px;margin:0 0 18px}}
.lede{{font-size:1.14em;color:var(--ink-soft);margin:0 auto;max-width:32em;font-weight:300}}
h2{{font-family:var(--sans);font-weight:700;text-transform:uppercase;font-size:.72em;
  letter-spacing:3px;color:var(--gold);margin:60px 0 10px;display:flex;align-items:center;gap:16px}}
h2::before,h2::after{{content:"";flex:1;height:1px;background:var(--line)}}
.note{{font-size:.9em;color:var(--muted);margin:0 auto 26px;max-width:32em}}
.brandblock{{background:var(--cream);border:1px solid var(--line);border-radius:4px;
  padding:20px 22px;margin-bottom:10px}}
.brandblock h3{{font-family:var(--serif);font-size:1.24em;margin:0 0 8px;font-weight:700}}
.brandblock h3 .n{{font-family:var(--sans);font-size:.6em;font-weight:700;color:var(--muted);
  letter-spacing:1.5px;vertical-align:middle;margin-left:6px}}
.brandblock p{{margin:0;font-size:.93em;color:var(--ink-soft);line-height:1.6}}
footer{{margin-top:76px;border-top:1px solid var(--line);padding:24px 0 64px;font-size:.78em;
  color:var(--muted);display:flex;gap:20px;flex-wrap:wrap;align-items:center;
  justify-content:center;text-transform:uppercase;letter-spacing:2px}}
footer a{{text-decoration:none}}
footer a:hover{{color:var(--ink)}}
.updated{{width:100%}}
@media(max-width:720px){{h1{{font-size:2.3em}}}}
</style>
</head>
<body>

<div class="banner">
  <img src="../images/banner.jpg" width="1211" height="471" alt="The PedalEditor app icon floating above a desert at dusk">
</div>

<div class="wrap">

  <div class="title-card">
    <p class="eyebrow"><a href="/PedalEditor/">PedalEditor</a></p>
    <div class="rule"></div>
    <h1>Every Profile</h1>
    <p class="lede">{n_avail} available now. {n_deck} on deck. Every one built from the manufacturer&rsquo;s manual.</p>
  </div>

  <h2>Available Now &mdash; {n_avail} pedals</h2>
  <p class="note">Audited and in the app today.</p>
{available}

  <h2>On Deck &mdash; {n_deck} pedals</h2>
  <p class="note">Built and waiting on audit. They arrive brand by brand.</p>
{ondeck}

  <footer>
    <a href="/PedalEditor/">PedalEditor</a>
    <a href="/">Meaningful Sound</a>
    <a href="/PedalEditor/reference/">Reference</a>
    <a href="/PedalEditor/privacy/">Privacy</a>
    <span class="updated">Updated {updated}</span>
  </footer>

</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
