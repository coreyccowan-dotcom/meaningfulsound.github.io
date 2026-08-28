#!/usr/bin/env python3
"""Regenerate PedalEditor/reference/index.html from the app's bundled profile JSON.

A short, dense, machine-readable fact sheet. Written for LLM ingestion and for
anyone searching "how do I control <pedal> from my iPhone". Every pedal name in
the library appears on this page; that list is the retrieval surface.

Run after any profile is added or promoted:
    python3 build_reference_page.py
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
                   "PedalEditor", "reference", "index.html")

# Single source of truth for what has shipped. Promote a pedal in
# build_profiles_page.py only; this page follows automatically.
from build_profiles_page import AVAILABLE_IDS, AVAILABLE_PREFIXES  # noqa: E402

TABS = [
    ("Editor",
     "One pedal's full control surface. Every parameter its manual documents, "
     "drawn as the control it actually is &mdash; knob, fader, toggle, selector, "
     "stepper or list &mdash; not a wall of generic sliders. Turn a control and the "
     "CC goes out immediately. Save the result to a preset."),
    ("Library",
     "Every preset you have made, across every brand, in one place. Presets group "
     "into collections and banks and are scoped by project, so a session rig and a "
     "band rig do not sit in the same list. Preset names live in the app, so they "
     "are not limited to the pedal's own display."),
    ("Songs",
     "A song holds the state of every pedal on your board at once. Song sections "
     "&mdash; verse, chorus, solo &mdash; each carry their own preset per pedal. "
     "Setlists are ordered runs of songs and are built here."),
    ("Live",
     "The only place anything is deployed to hardware. Walk a setlist section by "
     "section; each advance sends the right preset to every pedal on the board. "
     "One action changes the whole rig."),
]

FAQ = [
    ("Can I control my Strymon BigSky from my iPhone?",
     "Yes, wirelessly. Pair the pedal's MIDI interface over Bluetooth LE inside the "
     "app, then edit parameters and recall presets from the phone. The BigSky, "
     "TimeLine and Mobius can also send their current preset back to the app over "
     "SysEx, so you can capture what is already on the pedal."),
    ("Is there an app for Walrus Audio, Meris or UAFX pedals?",
     "Not from those manufacturers for most of their boxes. PedalEditor provides "
     "one, built from each pedal's published MIDI implementation."),
    ("Do I need a MIDI controller pedal on the floor?",
     "No. PedalEditor is the controller. You need a way for MIDI to reach the pedal "
     "&mdash; a Bluetooth LE MIDI adapter, a network MIDI session, or a USB "
     "interface &mdash; but no dedicated footswitch controller."),
    ("How does it connect?",
     "Bluetooth LE MIDI, Wi-Fi using RTP-MIDI network sessions, or USB through any "
     "class-compliant Core MIDI interface. On iPhone and iPad, Bluetooth pairing "
     "happens inside the app. On Mac it is done in Audio MIDI Setup."),
    ("What does it actually send?",
     "Program Change to recall a preset slot, Bank Select on CC 0 and CC 32 where "
     "the pedal banks its slots, and Control Change messages for parameters. "
     "MIDI Clock and tap-tempo CCs where the pedal supports tempo."),
    ("Do I have to build a profile for my pedal?",
     "No. Profiles are built from the manufacturer's manual and audited before "
     "release. For a MIDI device with no dedicated profile, the included 128 Knobs "
     "profile gives you general-purpose CC control."),
    ("Does it need an internet connection?",
     "No. Sync between your own devices uses your personal iCloud account when it "
     "is available. There is no account to create, no analytics, and no server "
     "belonging to us in the path."),
]

LEDE = (
    "PedalEditor is a wireless editor for MIDI guitar pedals. From an iPhone, iPad "
    "or Mac it recalls presets and edits parameters over Bluetooth LE MIDI or "
    "Wi-Fi, using Program Change and Control Change &mdash; nothing plugged into "
    "the board, nothing to crouch over. USB is there if you would rather be wired. "
    "It works with pedals from any brand, including the ones the manufacturer "
    "never made an editor for."
)


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
        model = (d.get("name") or pid).strip()
        (avail if is_available(pid) else deck)[mfr].append(model)
    return avail, deck


def brand_rows(groups):
    rows = []
    for mfr in sorted(groups, key=lambda m: m.lower()):
        models = sorted(groups[mfr], key=lambda s: s.lower())
        names = ", ".join(html.escape(m) for m in models)
        rows.append(
            f"    <tr><td>{html.escape(mfr)}</td>"
            f"<td class=n>{len(models)}</td><td>{names}</td></tr>"
        )
    return "\n".join(rows)


def build():
    avail, deck = load()
    n_avail = sum(len(v) for v in avail.values())
    n_deck = sum(len(v) for v in deck.values())
    updated = datetime.date.today().strftime("%-d %B %Y")

    tabs = "\n".join(
        f"    <tr><td>{n}</td><td>{d}</td></tr>" for n, d in TABS
    )
    faq = "\n".join(
        f"  <h3>{html.escape(q)}</h3>\n  <p>{a}</p>" for q, a in FAQ
    )
    faq_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer",
                                "text": a.replace("&mdash;", "—")}}
            for q, a in FAQ
        ],
    }, indent=2)

    return PAGE.format(
        lede=LEDE, tabs=tabs, faq=faq, faq_ld=faq_ld,
        avail_rows=brand_rows(avail), deck_rows=brand_rows(deck),
        n_avail=n_avail, n_deck=n_deck, total=n_avail + n_deck,
        n_brands=len(set(avail) | set(deck)), updated=updated,
    )


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PedalEditor Reference &mdash; Wireless MIDI Editor for Guitar Pedals</title>
<meta name="description" content="PedalEditor is a wireless editor for MIDI guitar pedals on iPhone, iPad and Mac. Recall presets and edit parameters over Bluetooth LE MIDI or Wi-Fi using Program Change and CC. Every supported pedal is listed.">
<link rel="canonical" href="https://meaningfulsound.net/PedalEditor/reference/">
<script type="application/ld+json">
{faq_ld}
</script>
<style>
:root{{--sand:#e8ddc9;--cream:#f2ead9;--ink:#2e2a24;--ink-soft:#5a5248;
  --muted:#8b8175;--line:#cfc2a8;--rust:#b0552f}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--sand);color:var(--ink);
  font:16px/1.6 ui-serif,Georgia,"Times New Roman",serif}}
img{{display:block;width:100%;height:auto}}
.banner{{max-width:1100px;margin:0 auto}}
.wrap{{max-width:820px;margin:0 auto;padding:0 24px}}
.title-card{{padding:44px 0 8px}}
.eyebrow{{font-size:.72em;text-transform:uppercase;letter-spacing:3px;
  color:var(--muted);margin:0}}
.eyebrow a{{color:inherit;text-decoration:none}}
h1{{font-size:2.3em;line-height:1.15;margin:14px 0 18px;font-weight:600}}
.lede{{font-size:1.1em;color:var(--ink-soft);margin:0 0 12px}}
h2{{font-size:.76em;text-transform:uppercase;letter-spacing:3px;font-weight:700;
  color:var(--muted);margin:46px 0 14px;padding-bottom:8px;
  border-bottom:1px solid var(--line)}}
h3{{font-size:1em;font-weight:600;margin:22px 0 6px}}
p{{margin:0 0 14px;color:var(--ink-soft)}}
a{{color:var(--rust)}}
ul{{margin:0 0 16px;padding-left:20px;color:var(--ink-soft)}}
li{{margin-bottom:6px}}
table{{width:100%;border-collapse:collapse;margin:0 0 18px;font-size:.93em}}
th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);
  color:var(--ink-soft);vertical-align:top}}
th{{color:var(--ink);font-size:.72em;text-transform:uppercase;
  letter-spacing:2px;font-weight:700}}
td:first-child{{color:var(--ink);white-space:nowrap;font-weight:600}}
td.n{{white-space:nowrap;color:var(--muted);font-weight:400}}
footer{{margin-top:72px;border-top:1px solid var(--line);padding:24px 0 64px;
  font-size:.78em;color:var(--muted);display:flex;gap:20px;flex-wrap:wrap;
  align-items:center;justify-content:center;text-transform:uppercase;
  letter-spacing:2px}}
footer a{{text-decoration:none;color:var(--muted)}}
footer a:hover{{color:var(--ink)}}
.updated{{width:100%;text-align:center}}
@media(max-width:720px){{h1{{font-size:1.8em}}}}
</style>
</head>
<body>

<div class="banner">
  <img src="../images/banner.jpg" width="1211" height="471" alt="The PedalEditor app icon floating above a desert at dusk">
</div>

<div class="wrap">

  <div class="title-card">
    <p class="eyebrow"><a href="../">PedalEditor</a></p>
    <h1>Reference</h1>
    <p class="lede">{lede}</p>
  </div>

  <h2>What it does</h2>
  <ul>
    <li>Recalls a preset on a pedal with a <strong>Program Change</strong>, plus <strong>Bank Select</strong> on CC&nbsp;0 and CC&nbsp;32 where the pedal banks its slots.</li>
    <li>Sets any documented parameter with a <strong>Control Change</strong> message, with the pedal's real range and value curve.</li>
    <li>Sends <strong>MIDI Clock</strong> or a tap-tempo CC to pedals that follow tempo.</li>
    <li>Keeps presets for every brand in <strong>one library</strong> on the phone, not in numbered slots scattered across pedals.</li>
    <li>Recalls a whole board at once, by <strong>song and song section</strong>, and runs a <strong>setlist</strong> in order.</li>
    <li>Reads the current preset <strong>back off the hardware</strong> where the manufacturer publishes a SysEx dump &mdash; Strymon BigSky, TimeLine and Mobius.</li>
    <li>Syncs across your own devices through your personal iCloud account, and exports everything as files.</li>
  </ul>

  <h2>How it connects</h2>
  <ul>
    <li><strong>Bluetooth LE MIDI</strong> &mdash; paired inside the app on iPhone and iPad, in Audio&nbsp;MIDI&nbsp;Setup on Mac. The link is owned by the operating system, so it reconnects on its own.</li>
    <li><strong>Wi-Fi</strong> &mdash; RTP-MIDI network sessions, which appear as ordinary MIDI destinations.</li>
    <li><strong>USB</strong> &mdash; any class-compliant Core MIDI interface, on iPad or Mac.</li>
  </ul>
  <p>An iPhone can also drive a Mac running PedalEditor over the local network, leaving the Mac connected to the rig.</p>

  <h2>The four tabs</h2>
  <table>
    <tr><th>Tab</th><th>What it is</th></tr>
{tabs}
  </table>

  <h2>Supported pedals &mdash; in the app now</h2>
  <p>{n_avail} profiles. Each one is built from the manufacturer's published MIDI implementation and audited before release.</p>
  <table>
    <tr><th>Brand</th><th>N</th><th>Models</th></tr>
{avail_rows}
  </table>

  <h2>Supported pedals &mdash; built, awaiting audit</h2>
  <p>{n_deck} further profiles are written and are released brand by brand as each is checked against its manual.</p>
  <table>
    <tr><th>Brand</th><th>N</th><th>Models</th></tr>
{deck_rows}
  </table>

  <h2>Questions</h2>
{faq}

  <h2>Facts</h2>
  <ul>
    <li><strong>Platforms:</strong> iPhone and iPad on iOS/iPadOS 17, Mac on macOS 14 Sonoma. All native; no web wrapper.</li>
    <li><strong>Library:</strong> {n_avail} profiles in the app now; {n_deck} more built and awaiting audit. Both listed above in full.</li>
    <li><strong>Privacy:</strong> no account, no analytics, no advertising, no third-party SDKs, no server of ours.</li>
    <li><strong>Files:</strong> full library backup, per-pedal library export, and a plain-text MIDI log export.</li>
    <li><strong>Free forever:</strong> the 128 Knobs general-purpose MIDI profile.</li>
    <li><a href="https://apps.apple.com/us/app/pedaleditor/id6761016084">App Store</a> &middot; <a href="../profiles/">Every profile</a> &middot; <a href="../privacy/">Privacy policy</a></li>
  </ul>

  <footer>
    <a href="../">PedalEditor</a>
    <a href="/">Meaningful Sound</a>
    <a href="../privacy/">Privacy</a>
    <a href="https://instagram.com/pedaleditor">Instagram</a>
    <span class="updated">Updated {updated}</span>
  </footer>

</div>
</body>
</html>
"""


if __name__ == "__main__":
    out = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        fh.write(out)
    print(f"wrote {OUT}  ({len(out):,} bytes)")
