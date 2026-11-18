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
    "strymon-":       ("strymon",         "Strymon"),
    "walrus-":        ("walrus-audio",    "Walrus Audio"),
    "meris-":         ("meris",           "Meris"),
    "uafx-":          ("uafx",            "UAFX"),
    "line6-":         ("line-6",          "Line 6"),
    "chasebliss-":    ("chase-bliss",     "Chase Bliss"),
    "hologram-":      ("hologram",        "Hologram"),
    "eventide-":      ("eventide",        "Eventide"),  # excluded via AVAILABLE
    "alexander-":     ("alexander",       "Alexander Pedals"),
    "boss-":          ("boss",            "Boss"),
    "digitech-":      ("digitech",        "DigiTech"),
    "ehx-":           ("ehx",             "Electro-Harmonix"),
    "empress-":       ("empress",         "Empress Effects"),
    "gfi-":           ("gfi",             "GFI System"),
    "jacksonaudio-":  ("jackson-audio",   "Jackson Audio"),
    "keeley-":        ("keeley",          "Keeley Electronics"),
    "oldbloodnoise-": ("old-blood-noise", "Old Blood Noise"),
    "redpanda-":      ("red-panda",       "Red Panda"),
    "sourceaudio-":   ("source-audio",    "Source Audio"),
    "valeton-":       ("valeton",         "Valeton"),
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


def _slug_from_pid(pid, prefix):
    """Strip the brand prefix off a pid to get the per-pedal slug."""
    return pid[len(prefix):] if prefix and pid.startswith(prefix) else pid


def _soon_lede(profile):
    """Factual-only one-liner synthesised from the JSON for pedals that don't
    yet carry hand-authored brand-page copy. Mirrors the shape of the
    hand-written ledes: machines, controls, preset slots, clock support."""
    rows, total = machine_rows(profile)
    machines_n = len(rows)
    bits = []
    if machines_n > 1:
        bits.append(f"{machines_n} machines, {total} controls")
    else:
        bits.append(f"{total} controls")
    presets = profile.get("presetSlots") or profile.get("hardwareSlots")
    if isinstance(presets, int) and presets > 0:
        bits.append(f"{presets} preset slots")
    # MIDI clock / tap tempo flags live in a few places across the schema;
    # we check the ones that exist on today's profiles.
    takes_clock = bool(profile.get("takesMidiClock"))
    takes_tap = bool(profile.get("takesTapTempo"))
    if takes_clock and takes_tap:
        bits.append("takes MIDI clock or tap")
    elif takes_clock:
        bits.append("takes MIDI clock")
    elif takes_tap:
        bits.append("takes tap tempo")
    return ". ".join(s[0].upper() + s[1:] if s else s for s in bits) + "."


def load_brand_copy():
    """Return {pid: (display_name, one_liner, is_audited)}.

    Pulls hand-authored copy from brand-page `now` entries. For `soon`
    entries — pedals built but not yet audited — synthesises a factual
    one-liner from the JSON so the per-pedal page can still exist as a
    retrieval surface for search. Matching is name-first with a slug
    fallback for the few cases where the brand-page short name
    (e.g. "M5") doesn't equal the JSON name ("M5 Stompbox Modeler")."""
    by_brand_now = {b["slug"]: b.get("now", []) for b in bbp.BRANDS}
    by_brand_soon = {b["slug"]: b.get("soon", []) for b in bbp.BRANDS}

    # {brand_slug: {norm_json_name: pid, "slug:" + per-pedal-slug: pid}}
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
        lookup = profiles_by_brand.setdefault(bslug, {})
        lookup[norm_name(jname)] = pid
        lookup["slug:" + _slug_from_pid(pid, prefix)] = pid

    def resolve(bslug, display_name, explicit_slug=None):
        lookup = profiles_by_brand.get(bslug, {})
        if explicit_slug:
            pid = lookup.get("slug:" + explicit_slug)
            if pid:
                return pid
        pid = lookup.get(norm_name(display_name))
        if pid:
            return pid
        return lookup.get("slug:" + slugify_name(display_name))

    out = {}
    for bslug, entries in by_brand_now.items():
        for entry in entries:
            if len(entry) == 3:
                display_name, slug_hint, desc = entry
            else:
                display_name, desc = entry
                slug_hint = None
            pid = resolve(bslug, display_name, slug_hint)
            if pid:
                out[pid] = (display_name, desc, True)

    for bslug, entries in by_brand_soon.items():
        # Eventide is pulled brand-wide (CLAUDE.md, 2026-09-04) — no detail
        # pages for Eventide pedals. The profiles still ship in the app;
        # they're held back from the public retrieval surface.
        if bslug == "eventide":
            continue
        for entry in entries:
            if isinstance(entry, (list, tuple)):
                display_name = entry[0]
                slug_hint = entry[1] if len(entry) > 1 else None
            else:
                display_name, slug_hint = entry, None
            pid = resolve(bslug, display_name, slug_hint)
            if not pid or pid in out:
                continue
            try:
                profile = load_profile(pid)
            except Exception:
                continue
            out[pid] = (display_name, _soon_lede(profile), False)
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


def _category_is_preset_browser(cat):
    if cat.get("tag", {}).get("role") == "preset-browser":
        return True
    algs = cat.get("algorithms", [])
    if algs and all(a.get("tag", {}).get("role") == "preset-browser" for a in algs):
        return True
    return False


def is_preset_browser_profile(profile):
    """True when every effectCategory is a Program-Change recall surface
    rather than an editable effect — e.g. Line 6 M9/M13/M5. The "What's
    inside" block for these pedals is recall-count + prose, not a
    machines list."""
    cats = profile.get("effectCategories", [])
    return bool(cats) and all(_category_is_preset_browser(c) for c in cats)


def preset_browser_block(profile, globals_n):
    """Inner HTML for the "What's inside" div, for preset-browser profiles.
    Prints each category as a count + its authored description, then the
    globals line reframed as infrastructure."""
    parts = ['  <div class="machines preset-browser">']
    for cat in profile.get("effectCategories", []):
        pcr = cat.get("pcRange")
        count = (pcr["end"] - pcr["start"] + 1) if pcr else len(cat.get("algorithms", []))
        name = html.escape(cat.get("name", ""))
        desc = cat.get("description", "").strip()
        parts.append(f'    <h3>{count} &middot; {name}</h3>')
        if desc:
            parts.append(f'    <p class="prose">{html.escape(desc)}</p>')
    parts.append(
        f'    <p class="globals">Plus <strong>{globals_n} infrastructure control{"" if globals_n == 1 else "s"}</strong> '
        '&mdash; tap tempo, expression routing, bypass mode, looper transport, MIDI channel, and the rest.</p>'
    )
    parts.append('  </div>')
    return "\n".join(parts)


def standard_block(rows, total_controls, globals_n, display_name):
    """Inner HTML for the "What's inside" div for a normal effect-based
    profile. Algorithms with 0 parameters print their name without the
    "— N controls" suffix (Whammy, Valeton cab list, etc.)."""
    machines_n = len(rows)
    if machines_n <= 1:
        heading = f"{total_controls} controls" if machines_n == 1 else f"{globals_n} controls"
        solo_cls = " solo"
    else:
        heading = f"{machines_n} machines"
        solo_cls = ""

    lis = []
    for name, n in rows:
        if n > 0:
            lis.append(
                f'      <li><span>{html.escape(name)}</span>'
                f'<span class="n">{n} control{"s" if n != 1 else ""}</span></li>'
            )
        else:
            lis.append(f'      <li><span>{html.escape(name)}</span></li>')
    machine_lis = "\n".join(lis)
    if not machine_lis:
        machine_lis = (
            f'      <li><span>{html.escape(display_name)}</span>'
            f'<span class="n">{globals_n} controls</span></li>'
        )

    return (
        f'  <div class="machines{solo_cls}">\n'
        f'    <h3>{heading}</h3>\n'
        f'    <ul>\n'
        f'{machine_lis}\n'
        f'    </ul>\n'
        f'    <p class="globals">Plus <strong>{globals_n} global control{"" if globals_n == 1 else "s"}</strong> shared across every machine &mdash; tap tempo, expression, bypass mode, MIDI channel, and the rest.</p>\n'
        f'  </div>'
    )


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

/* Screenshots framed in real Apple device artwork — iPhone 17 Pro Max
   Deep Blue + iPad Pro 13" (M5) Space Black. Both devices share
   --device-h (the visible frame height). The PNG sits on top of the
   screenshot, its rounded-corner cutout revealing the shot through it.

   Measurements (pixel-exact, derived from the PNGs' alpha channel):
     iPhone PNG 1470x3000  visible device 98.6333% of image height
       screen rect:  left 5.1020% top 2.2000% width 89.7959% height 95.6000%
     iPad PNG 3000x2300  visible device 97.7826% of image height
       screen rect:  left 4.1333% top 5.1304% width 91.7333% height 89.7391%
*/
.shots{{--device-h:440px;
  display:flex;gap:28px;justify-content:center;align-items:center;flex-wrap:wrap;
  width:min(96vw,1040px);margin-left:calc((100% - min(96vw,1040px)) / 2)}}
.shot{{display:flex;flex-direction:column;align-items:center;gap:12px}}
.shot .device{{position:relative;flex:0 0 auto}}
.shot .device .screenshot{{position:absolute;display:block;object-fit:cover;object-position:center top;
  background:var(--cream)}}
.shot .device .bezel{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;
  display:block}}
.shot .device .placeholder{{position:absolute;display:flex;align-items:center;justify-content:center;
  text-align:center;background:var(--cream);color:var(--muted);font-size:.74em;font-weight:600;
  text-transform:uppercase;letter-spacing:2px;line-height:1.5}}
.shot.iphone .device{{
  height:calc(var(--device-h) / 0.986333);
  width:calc(var(--device-h) / 0.986333 * 0.49)}}
.shot.iphone .screenshot,.shot.iphone .placeholder{{
  left:5.1020%;top:2.2000%;width:89.7959%;height:95.6000%;
  border-radius:11%/5.2%}}
.shot.ipad .device{{
  height:calc(var(--device-h) / 0.977826);
  width:calc(var(--device-h) / 0.977826 * 1.30435)}}
.shot.ipad .screenshot,.shot.ipad .placeholder{{
  left:4.1333%;top:5.1304%;width:91.7333%;height:89.7391%;
  border-radius:2.4%/3.2%}}
.shot .caption{{font-size:.72em;font-weight:700;text-transform:uppercase;letter-spacing:2px;
  color:var(--muted)}}
.shot a.zoom{{position:absolute;display:block;cursor:zoom-in}}
.shot.iphone a.zoom{{
  left:5.1020%;top:2.2000%;width:89.7959%;height:95.6000%;
  border-radius:11%/5.2%;overflow:hidden}}
.shot.ipad a.zoom{{
  left:4.1333%;top:5.1304%;width:91.7333%;height:89.7391%;
  border-radius:2.4%/3.2%;overflow:hidden}}
.shot a.zoom .screenshot{{position:static;width:100%;height:100%;border-radius:0}}
.shot a.zoom:focus-visible{{outline:2px solid var(--terracotta);outline-offset:2px}}

/* Lightbox */
.lb{{position:fixed;inset:0;background:rgba(30,20,12,.88);display:none;
  align-items:center;justify-content:center;z-index:9999;padding:24px;cursor:zoom-out}}
.lb.open{{display:flex}}
.lb img{{max-width:100%;max-height:100%;width:auto;height:auto;border-radius:4px;
  box-shadow:0 20px 60px rgba(0,0,0,.5);object-fit:contain}}
.lb-close{{position:fixed;top:16px;right:20px;background:none;border:0;color:var(--cream);
  font-size:2em;line-height:1;cursor:pointer;padding:6px 12px;font-family:var(--sans)}}
.lb-close:focus-visible{{outline:2px solid var(--terracotta);outline-offset:2px}}

.machines{{background:var(--cream);border:1px solid var(--line);border-radius:4px;padding:24px 26px;text-align:left}}
.machines h3{{font-family:var(--serif);font-size:1.24em;margin:0 0 14px;font-weight:700;letter-spacing:-.2px;text-align:center}}
.machines ul{{list-style:none;margin:0;padding:0;
  display:grid;grid-template-columns:repeat(2,1fr);gap:6px 24px}}
.machines.solo ul{{grid-template-columns:1fr;max-width:24em;margin:0 auto}}
.machines li{{display:flex;justify-content:space-between;gap:12px;font-size:.95em;
  color:var(--ink-soft);padding:4px 0;border-bottom:1px dotted var(--line)}}
.machines li .n{{color:var(--muted);font-variant-numeric:tabular-nums}}
.machines .prose{{font-size:.95em;color:var(--ink-soft);margin:0 0 10px;max-width:46em;
  margin-left:auto;margin-right:auto;text-align:center;line-height:1.55}}
.globals{{margin-top:14px;text-align:center;font-size:.9em;color:var(--muted)}}
.globals strong{{color:var(--ink);font-weight:600}}

.facts p{{color:var(--ink-soft);max-width:34em;margin:0 auto 16px}}
.facts .price{{border-top:1px solid var(--line);padding-top:22px;margin-top:26px;color:var(--ink)}}

footer{{margin-top:80px;border-top:1px solid var(--line);padding:24px 0 64px;font-size:.78em;
  color:var(--muted);display:flex;gap:20px;flex-wrap:wrap;align-items:center;
  justify-content:center;text-transform:uppercase;letter-spacing:2px}}
footer a{{text-decoration:none}}
footer a:hover{{color:var(--ink)}}
footer .social{{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px}}
footer .social svg{{width:18px;height:18px;display:block}}
.updated{{width:100%}}

@media(max-width:720px){{
  h1{{font-size:2.4em}}
  .title-card{{padding-top:36px}}
  .shots{{--device-h:320px;gap:18px}}
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
      <div class="device">
        {iphone_frame}
        <img class="bezel" src="../../images/devices/iphone-17-pm-deep-blue.png" alt="">
      </div>
      <p class="caption">iPhone</p>
    </div>
    <div class="shot ipad">
      <div class="device">
        {ipad_frame}
        <img class="bezel" src="../../images/devices/ipad-pro-13-space-black-landscape.png" alt="">
      </div>
      <p class="caption">iPad</p>
    </div>
  </div>

  <h2>What&rsquo;s inside</h2>
{machines_block}

  <h2>Facts</h2>
  <div class="facts">
    <p>Available on iPhone, iPad and Mac. Connects over Bluetooth LE MIDI (with a WIDI Jack or equivalent), Wi&#8209;Fi (RTP&#8209;MIDI) or USB. Bluetooth pairing happens inside the app on iPhone and iPad; on Mac you pair in Audio MIDI Setup.</p>
    <p>Presets live in the app library. Save what you want to the pedal from any preset, in any order. Every knob on the front of the {display_name} and every parameter behind it are on the same screen.</p>
    <p class="price">{build_note} <a href="../">The rest of the {brand_short} line is here.</a></p>
  </div>

  <footer>
    <a href="../../">PedalEditor</a>
    <a href="/">Meaningful Sound</a>
    <a href="../">{brand_short}</a>
    <a href="../../reference/">Reference</a>
    <a href="../../privacy/">Privacy</a>
    <a class="social" href="https://instagram.com/pedaleditor" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5" ry="5" fill="none" stroke="currentColor" stroke-width="1.75"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.75"/><circle cx="17.5" cy="6.5" r="1.15" fill="currentColor"/></svg></a>
    <a class="social" href="https://tiktok.com/@pedaleditor" target="_blank" rel="noopener" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M19.5 8.6a6.4 6.4 0 0 1-3.8-1.2v7.4a5.4 5.4 0 1 1-5.4-5.4v3a2.4 2.4 0 1 0 2.4 2.4V2.5h2.9a4.3 4.3 0 0 0 3.9 4z" fill="currentColor"/></svg></a>
    <a class="social" href="https://youtube.com/@meaningfulsound" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.6 3.6 12 3.6 12 3.6s-7.6 0-9.4.5A3 3 0 0 0 .5 6.2C0 8 0 12 0 12s0 4 .5 5.8a3 3 0 0 0 2.1 2.1c1.8.5 9.4.5 9.4.5s7.6 0 9.4-.5a3 3 0 0 0 2.1-2.1c.5-1.8.5-5.8.5-5.8s0-4-.5-5.8zM9.6 15.6V8.4L15.8 12z" fill="currentColor"/></svg></a>
    <span class="updated">Updated {today}</span>
  </footer>

</div>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Screenshot preview" hidden>
  <button class="lb-close" type="button" aria-label="Close preview">&times;</button>
  <img id="lb-img" alt="">
</div>
<script>
(function(){{
  var lb=document.getElementById('lb'),img=document.getElementById('lb-img');
  document.querySelectorAll('.shot a.zoom').forEach(function(a){{
    a.addEventListener('click',function(e){{
      e.preventDefault();
      img.src=a.getAttribute('href');
      img.alt=a.querySelector('img').alt;
      lb.hidden=false;lb.classList.add('open');
      document.body.style.overflow='hidden';
    }});
  }});
  function close(){{lb.classList.remove('open');lb.hidden=true;img.src='';document.body.style.overflow=''}}
  lb.addEventListener('click',close);
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')close()}});
}})();
</script>
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


def render_page(pid, profile, brand_slug, brand_name, display_name, desc, is_audited):
    pedal_slug = pid[pid.index("-") + 1:]  # e.g. walrus-r1-mkii → r1-mkii
    # For chasebliss- / line6- the JSON prefix is one token; peel it off:
    for prefix in BRAND_MAP:
        if pid.startswith(prefix):
            pedal_slug = pid[len(prefix):]
            break

    rows, total_controls = machine_rows(profile)
    globals_n = len(profile.get("globalParameters", []))
    machines_n = len(rows)

    if is_preset_browser_profile(profile):
        machines_block = preset_browser_block(profile, globals_n)
    else:
        machines_block = standard_block(rows, total_controls, globals_n, display_name)

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
    iphone_alt = f"{brand_name} {strip_html(display_name)} on iPhone in PedalEditor"
    ipad_alt = f"{brand_name} {strip_html(display_name)} on iPad in PedalEditor"
    iphone_frame = (
        f'<a class="zoom" href="{iphone}" aria-label="Open full-size iPhone screenshot">'
        f'<img class="screenshot" src="{iphone}" alt="{iphone_alt}"></a>'
        if iphone else
        '<div class="placeholder">iPhone screenshot<br>coming soon</div>'
    )
    ipad_frame = (
        f'<a class="zoom" href="{ipad}" aria-label="Open full-size iPad screenshot">'
        f'<img class="screenshot" src="{ipad}" alt="{ipad_alt}"></a>'
        if ipad else
        '<div class="placeholder">iPad screenshot<br>coming soon</div>'
    )

    desc_plain = strip_html(desc)
    display_name_plain = strip_html(display_name)
    jsonld = build_jsonld(brand_name, brand_slug, display_name, pedal_slug, desc_plain)

    if is_audited:
        build_note = (
            f"Built from the {brand_name} {display_name} user manual "
            f"and audited before it shipped."
        )
    else:
        build_note = (
            f"Built from the {brand_name} {display_name} user manual "
            f"and releasing soon."
        )

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
        machines_block=machines_block,
        iphone_frame=iphone_frame,
        ipad_frame=ipad_frame,
        build_note=build_note,
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
        prefix, brand_slug, brand_name = brand_for(pid)
        if not brand_slug:
            skipped.append((pid, "unknown brand prefix"))
            continue
        if pid not in copy:
            missing_copy.append(pid)
            continue

        display_name, desc, is_audited = copy[pid]
        profile = load_profile(pid)
        pedal_slug, html_out = render_page(
            pid, profile, brand_slug, brand_name, display_name, desc, is_audited,
        )

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
