#!/usr/bin/env python3
"""Regenerate the PedalEditor brand pages from one template.

    python3 build_brand_pages.py

Brand order on the main page and here is Corey's: Strymon, Walrus, Meris,
UAFX, Line 6. Moving a pedal from soon[] to now[] is the weekly edit.
"""

import datetime
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "PedalEditor")

BRANDS = [
{
 "slug": "strymon", "brand": "Strymon",
 "blurb": "All 21 Strymon pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Strymon keeps a steady dialect. 300 preset slots on nearly every box &mdash; 200 on TimeLine and Mobius &mdash; and tap tempo waiting on CC&nbsp;93 almost everywhere you look. 21 pedals. All of them read.",
 "now": [
  ("BigSky", "12 reverb machines, 148 controls. Room to Nonlinear, and everything that lives in between."),
  ("BigSky MX", "Two independent engines, each running all 12 machines. 24 combinations, 454 controls."),
  ("blueSky V2", "Plate, Room, Spring. 3 machines, 28 controls. Three good answers to the same question."),
  ("Brig", "3 machines, 24 controls. The 3205, the 3005, and the Multi. It knows which one you meant."),
  ("Cloudburst", "1 machine: Ambient Reverb. 14 controls. The simplicity is the point."),
  ("Compadre", "2 machines, 4 modes, 13 controls. Compressor or Boost. Studio or Squeeze. Clean or Dirty. Small pedal, complete map."),
  ("Deco", "Tape Saturation and Doubletracker. 5 modes across 2 machines. All 36 controls, including the ones that feel like accidents."),
  ("DIG", "1 machine, 21 controls. A delay pedal with a lot to say about one thing."),
  ("EC&#8209;1", "Tape Echo, and nothing else. 16 controls, every one of them doing something."),
  ("El Capistan V2", "3 tape&#8209;echo machines across 9 modes, 108 controls. Fixed heads, multi&#8209;head combinations, and Sound on Sound. The manual was long."),
  ("Flint", "Tremolo and reverb, 6 modes, 39 controls. Three decades of each, laid out in order."),
  ("Iridium", "Round, Chime, Punch. 3 amp machines, 35 controls. Pick a room and stand in it."),
  ("Lex V2", "1 machine, 22 controls. Everything the rotary does, surfaced."),
  ("Mobius", "12 machines: Chorus, Flanger, Rotary, Vibe, Phaser, Filter, Formant, Vintage Trem, Pattern Trem, Autoswell, Destroyer, Quadrature. 123 controls. It&rsquo;s a lot."),
  ("NightSky", "1 machine, 54 controls. The gap between those two numbers is what makes it a NightSky."),
  ("Riverside", "1 machine, 16 controls. Drive, mapped cleanly. Not everything needs 12 modes."),
  ("Sunset", "Dual Overdrive. 1 machine, 18 controls. Both sides of it."),
  ("TimeLine", "12 delay machines, 193 controls. dTape to Lo&#8209;Fi, in order. Every parameter the manual published."),
  ("UltraViolet", "Chorus, Blend, Vibrato. 3 machines, 18 controls. The whole range of what it does."),
  ("Volante", "3 machines, 116 controls. Studio, Drum, Tape. The number is not a typo."),
  ("Zelzah", "2 machines, 6 modes, 35 controls. Four&#8209;stage and six&#8209;stage, from Classic to Strong. All of it mapped."),
 ],
 "soon": [],
 "cost": "21 manuals. Every parameter table read, every range confirmed, every control cross&#8209;checked against what the pedal actually receives. It isn&rsquo;t glamorous work &mdash; mostly it&rsquo;s a PDF and a MIDI monitor and a question about whether this knob goes to 127 or to 100. The app holds the answer so you don&rsquo;t have to.",
},
{
 "slug": "walrus-audio", "brand": "Walrus",
 "blurb": "All 10 Walrus Audio pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Walrus speaks in variety more than uniformity. Most boxes hold 128 preset slots &mdash; the Meraki carries one, the Qi Etherealizer 127. Tempo lives on the D1 and M1 families; the ACS1 and R1 don&rsquo;t ask for it. 10 pedals. All of them read.",
 "now": [
  ("ACS1", "3 voices &mdash; Fullerton, London, Dartford &mdash; and 23 controls. The MkII would double it."),
  ("ACS1 MkII", "6 voices, 46 controls. The same three rooms as the original, then three more added in the revision."),
  ("D1", "5 delay machines, 41 controls. Digital, Mod, Vintage, Dual, Reverse. The clean read on delay."),
  ("D1 MkII", "6 machines, 76 controls. Everything the D1 said, plus Grain. The number grew accordingly."),
  ("M1", "6 machines, 18 modes, 242 controls. Chorus, Phaser, Tremolo, Vibrato, Rotary, Filter &mdash; three readings of each."),
  ("M1 MkII", "The same 6 machines, modes renamed, 249 controls. 7 more than the original. The difference is in the details."),
  ("Meraki", "3 machines, 3 modes, 40 controls, 1 preset slot. Stereo analog delay with more to say than the enclosure implies."),
  ("Qi Etherealizer", "1 machine, 24 controls, 127 preset slots. Unusual arithmetic for an unusual pedal."),
  ("R1", "6 reverb machines &mdash; Spring, Hall, Plate, BFR, RFRCT, Air &mdash; and 59 controls. The original map."),
  ("R1 MkII", "The same 6 machines, 81 controls. The pedal kept its rooms; the profile grew to match what the MkII added."),
 ],
 "soon": [],
 "cost": "10 manuals. The M1 family alone runs to nearly 250 controls across 6 machines and 18 modes &mdash; the kind of profile that takes a while to get right. The ACS1 doubled between versions. The R1 gained 22 controls without changing its machine list. Every range confirmed, one at a time.",
},
{
 "slug": "meris", "brand": "Meris",
 "blurb": "The Meris LVX in PedalEditor, with seven more Meris profiles built and waiting on audit.",
 "lede": "Meris runs two dialects, depending on which era you&rsquo;re holding. The older boxes give you 16 preset slots. The LVX holds 99 and takes MIDI clock. One pedal audited so far. 7 more built and waiting their turn.",
 "now": [
  ("LVX", "7 machines, 38 modes, 266 controls. Preamp, Delay, Dynamic, Pitch, Filter, Modulation, and a Looper &mdash; each with its own set of modes."),
 ],
 "soon": ["Enzo", "Enzo X", "Hedra", "Mercury7", "Mercury X", "Ottobit Jr.", "Polymoon"],
 "cost": "1 done. 7 built and sitting in the queue. The LVX took the longest because 266 controls across seven machines earns that. The others will follow the same way &mdash; manual first, then every parameter confirmed. That part doesn&rsquo;t get faster by rushing it.",
},
{
 "slug": "uafx", "brand": "UAFX",
 "blurb": "Seven UAFX amp modelers in PedalEditor, each profile built from the manufacturer's manual, with seven more on deck.",
 "lede": "UAFX speaks a consistent dialect. Every amp modeler holds 128 preset slots. None of them take MIDI clock &mdash; these are amps, and tempo isn&rsquo;t part of the conversation. 7 available now. 7 more on deck.",
 "now": [
  ("Dream &rsquo;65", "1 voice, 19 controls. Small and self&#8209;contained. The whole pedal in one profile."),
  ("Lion &rsquo;68", "3 channels &mdash; Super Bass, Super Lead, Brown &mdash; and 65 controls. Each voice mapped on its own."),
  ("Ruby &rsquo;63", "Brilliant, Normal, Vibrato. 3 channels, 42 controls. The channel names are the pedal&rsquo;s own."),
  ("Woodrow &rsquo;55", "1 voice, 15 controls. The smallest of the seven, and none of it left out."),
  ("Knuckles &rsquo;92 Rev F", "3 channels &mdash; Clean, Orange, Red &mdash; and 78 controls. All three accounted for."),
  ("ANTI 1992", "Rhythm, Crunch, Lead. 3 channels, 77 controls. Near&#8209;identical in size to the Knuckles and the Enigmatic. Different box entirely."),
  ("Enigmatic &rsquo;82", "Rock, Jazz, Custom. 3 channels, 78 controls. The third of the three&#8209;channel cluster."),
 ],
 "soon": ["Astra", "Del&#8209;Verb", "Galaxy &rsquo;74", "Golden Reverberator", "Max", "OX Stomp", "Starlight"],
 "cost": "7 manuals, 7 amp modelers. The three&#8209;channel pedals &mdash; Knuckles, ANTI, Enigmatic &mdash; each land at 77 or 78 controls, which sounds like a coincidence until you&rsquo;ve read all three. Dream and Woodrow are single&#8209;voice, and the profiles say so rather than padding.",
},
{
 "slug": "line-6", "brand": "Line 6",
 "blurb": "The Line 6 DL4 MkII in PedalEditor, all 46 modes mapped, with four more Line 6 profiles on deck.",
 "lede": "Line 6 doesn&rsquo;t ask for a simple dialect. The DL4 MkII carries 128 preset slots, takes MIDI clock, and holds more modes than most brands have pedals. 1 available now. 4 more built and waiting.",
 "now": [
  ("DL4 MkII", "2 machines &mdash; 30 delays and 16 reverbs &mdash; 46 modes, 236 controls. Vintage Digital through to Glitch. Room through to Reverb Off."),
 ],
 "soon": ["HX One", "M13", "M5", "M9"],
 "cost": "One manual. It was a long one. 30 delay modes and 16 reverb modes in a single pedal means 236 controls to confirm, one at a time. The HX One, M13, M5 and M9 are built and waiting. The DL4 took as long as it took. So will they.",
},
{
 "slug": "chase-bliss", "brand": "Chase Bliss",
 "blurb": "3 Chase Bliss pedals in PedalEditor, each profile built from the manufacturer's manual, with 23 more on deck.",
 "lede": "Chase Bliss runs a consistent house style. Most boxes hold 122 preset slots and take MIDI clock or tap tempo &mdash; though Generation Loss MKII takes neither, which the profile notes plainly. 3 pedals audited. 23 more built and waiting.",
 "now": [
  ("Mood MkII", "2 machines &mdash; Wet Channel and Micro&#8209;Looper, 3 modes each &mdash; 6 modes total, 64 controls, 122 preset slots. Takes MIDI clock or tap."),
  ("Habit", "1 machine, 16 controls, 122 preset slots. Takes MIDI clock or tap. Its 6 modifiers run as a two&#8209;CC matrix &mdash; one named choice writes two CCs at once &mdash; so the profile carries a mechanism no other pedal in the library needed."),
  ("Generation Loss MKII", "2 machines &mdash; MKII with 13 modes, Classic with 1 &mdash; 14 modes total, 143 controls, 122 preset slots. Takes no MIDI clock and no tap tempo at all. The profile says so rather than pretending otherwise."),
 ],
 "soon": ["Bliss Factory", "Blooper", "Brothers", "Brothers AM", "Clean", "Condor", "CXM 1978", "Dark World", "Generation Loss", "Gravitas", "Lossy", "Lost + Found", "MOOD", "Onward", "Preamp MKII", "Reverse Mode C", "Spectre", "Thermae", "Tonal Recall", "Warped Vinyl HiFi", "Warped Vinyl MkII", "Wombtone MkI", "Wombtone MkII"],
 "cost": "3 done. 23 built and waiting. Chase Bliss publishes thorough MIDI specs, and the audits still turn up things worth knowing &mdash; Generation Loss MKII has 143 controls and no clock input at all; Habit&rsquo;s modifier matrix meant extending the profile model before it could be expressed correctly. Every control confirmed against the manual before it ships.",
},
{
 "slug": "eventide", "brand": "Eventide",
 "blurb": "3 Eventide pedals in PedalEditor, each profile built from the manufacturer's manual, with 4 more on deck.",
 "lede": "Eventide&rsquo;s MIDI dialect is thorough on parameters and silent on algorithm switching &mdash; none of the three can change algorithms over MIDI at all. The profiles surface that honestly: the app prints the front&#8209;panel gesture instead of offering a control that does nothing. All three take MIDI clock. None have tap tempo. 3 pedals audited. 4 more built and waiting.",
 "now": [
  ("H9 Harmonizer", "5 machines &mdash; Space, PitchFactor, TimeFactor, ModFactor, New for H9 &mdash; 52 modes, 520 controls, 99 preset slots. The largest profile in the app. Changing algorithm means the PRESETS button on the pedal, and the app says so on the screen."),
  ("Space", "12 machines, 12 modes, 132 controls, 100 preset slots. Hall through Shimmer. Algorithm switching is press&#8209;then&#8209;turn on the Encoder; the profile prints the gesture."),
  ("TimeFactor", "10 machines, 10 modes, 110 controls, 100 preset slots. DigitalDelay through Looper. Algorithm switching is the Encoder alone; the profile prints the gesture."),
 ],
 "soon": ["Knife Drop", "Rose", "TriceraChorus", "UltraTap"],
 "cost": "3 done. 4 built and waiting. The H9 is the largest profile in the app &mdash; 520 controls across 52 modes takes a while to get right. Space and TimeFactor are smaller but carry the same accounting: where the pedal cannot do something over MIDI, the profile says what to press instead. That part doesn&rsquo;t change regardless of how long the manual is.",
},
{
 "slug": "hologram", "brand": "Hologram",
 "blurb": "The Hologram Microcosm in PedalEditor, with 2 more Hologram profiles built and waiting on audit.",
 "lede": "The Microcosm covers a lot of ground for a pedal with 4 machines &mdash; 205 controls, 60 preset slots, and MIDI clock or tap tempo either way. 1 pedal audited. 2 more built and waiting.",
 "now": [
  ("Microcosm", "4 machines &mdash; Micro Loop, Granules, Glitch, Multidelay &mdash; 11 modes total, 205 controls, 60 preset slots. Takes MIDI clock or tap."),
 ],
 "soon": ["Chroma Console", "Dream Sequence"],
 "cost": "1 done. 2 built and waiting. The Microcosm runs to 205 controls across 4 machines and 11 modes &mdash; a bigger number than the front panel suggests. Chroma Console and Dream Sequence follow the same path: manual first, every parameter confirmed, one at a time.",
},
]

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Speaks Fluent {brand} &mdash; PedalEditor | Meaningful Sound</title>
<meta name="description" content="{blurb} Control them from iPhone, iPad or Mac over Bluetooth.">
<meta name="author" content="Meaningful Sound">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#e8dfc8">
<link rel="canonical" href="https://meaningfulsound.net/PedalEditor/{slug}/">
<link rel="alternate" type="text/markdown" title="LLM-friendly summary" href="/llms.txt">
<meta name="apple-itunes-app" content="app-id=6761016084, app-argument=https://meaningfulsound.net/PedalEditor/{slug}/">

<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Meaningful Sound">
<meta property="og:title" content="Speaks Fluent {brand} &mdash; PedalEditor">
<meta property="og:description" content="{blurb}">
<meta property="og:url" content="https://meaningfulsound.net/PedalEditor/{slug}/">
<meta property="og:image" content="https://meaningfulsound.net/PedalEditor/images/banner.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Speaks Fluent {brand} &mdash; PedalEditor">
<meta name="twitter:description" content="{blurb}">
<meta name="twitter:image" content="https://meaningfulsound.net/PedalEditor/images/banner.jpg">

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
h1{{font-family:var(--serif);font-size:3.3em;line-height:1.04;letter-spacing:-1px;margin:0 0 18px;font-weight:700}}
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
  color:var(--gold);margin:62px 0 10px;display:flex;align-items:center;gap:16px}}
h2::before,h2::after{{content:"";flex:1;height:1px;background:var(--line)}}
.note{{font-size:.9em;color:var(--muted);margin:0 auto 26px;max-width:32em}}
.pedal{{background:var(--cream);border:1px solid var(--line);border-radius:4px;
  padding:20px 22px;margin-bottom:10px}}
.pedal h3{{font-family:var(--serif);font-size:1.34em;margin:0 0 6px;font-weight:700;letter-spacing:-.2px}}
.pedal p{{margin:0;font-size:.95em;color:var(--ink-soft);line-height:1.6}}
.soonlist{{background:var(--cream);border:1px solid var(--line);border-radius:4px;
  padding:20px 22px;font-size:.95em;color:var(--ink-soft)}}
.cost p,.facts p{{color:var(--ink-soft);max-width:34em;margin:0 auto 16px}}
.facts .price{{border-top:1px solid var(--line);padding-top:22px;margin-top:26px;color:var(--ink)}}
footer{{margin-top:80px;border-top:1px solid var(--line);padding:24px 0 64px;font-size:.78em;
  color:var(--muted);display:flex;gap:20px;flex-wrap:wrap;align-items:center;
  justify-content:center;text-transform:uppercase;letter-spacing:2px}}
footer a{{text-decoration:none}}
footer a:hover{{color:var(--ink)}}
.updated{{width:100%}}
@media(max-width:720px){{h1{{font-size:2.4em}}.title-card{{padding-top:36px}}}}
</style>
</head>
<body>

<div class="banner">
  <img src="../images/banner.jpg" width="1211" height="471" alt="The PedalEditor app icon floating above a desert at dusk">
</div>

<div class="wrap">

  <div class="title-card">
    <p class="eyebrow"><a href="../">PedalEditor</a></p>
    <div class="rule"></div>
    <h1>Speaks Fluent {brand}</h1>
    <p class="lede">{lede}</p>
    <div class="links">
      <a class="pill filled" href="https://apps.apple.com/us/app/pedaleditor/id6761016084">App Store</a>
      <a class="pill" href="../profiles/">Every Profile</a>
    </div>
  </div>

  <h2>Available Now &mdash; {n_now}</h2>
  <p class="note">In the app today. Every one built to spec.</p>
{now}
{soon}
  <h2>What fluency cost</h2>
  <div class="cost">
    <p>{cost}</p>
  </div>

  <h2>Facts</h2>
  <div class="facts">
    <p>Available on iPhone, iPad and Mac. Connects over Bluetooth LE MIDI, Wi&#8209;Fi (RTP&#8209;MIDI) and USB. Bluetooth pairing happens inside the app on iPhone and iPad; on Mac you pair in Audio MIDI Setup.</p>
    <p>No account. No analytics. No third&#8209;party SDKs. iCloud sync across your devices at no extra cost, with a local fallback if iCloud isn&rsquo;t available. Presets, songs and full backups export as files.</p>
    <p class="price">Every profile is built from the manufacturer&rsquo;s manual and audited before it ships. <a href="../profiles/">The full list is here</a> &mdash; what&rsquo;s in the app today, and what&rsquo;s on deck.</p>
  </div>

  <footer>
    <a href="../">PedalEditor</a>
    <a href="/">Meaningful Sound</a>
    <a href="../reference/">Reference</a>
    <a href="../privacy/">Privacy</a>
    <a href="https://instagram.com/pedaleditor">Instagram</a>
    <span class="updated">Updated {updated}</span>
  </footer>

</div>
</body>
</html>
"""


def main():
    updated = datetime.date.today().strftime("%-d %B %Y")
    for b in BRANDS:
        now = "\n".join(
            f'  <div class="pedal">\n    <h3>{name}</h3>\n    <p>{line}</p>\n  </div>'
            for name, line in b["now"]
        )
        soon = ""
        if b["soon"]:
            names = " &middot; ".join(b["soon"])
            soon = (
                f'\n  <h2>Coming Soon &mdash; {len(b["soon"])} pedals</h2>\n'
                '  <p class="note">Built and waiting on audit.</p>\n'
                f'  <div class="soonlist">{names}</div>\n'
            )
        n_now = f'{len(b["now"])} pedal' + ("" if len(b["now"]) == 1 else "s")
        page = PAGE.format(
            brand=b["brand"], slug=b["slug"], blurb=html.escape(b["blurb"], quote=True),
            lede=b["lede"], now=now, soon=soon, cost=b["cost"],
            n_now=n_now, updated=updated,
        )
        d = os.path.join(OUT, b["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w") as fh:
            fh.write(page)
        print(f'wrote PedalEditor/{b["slug"]}/  ({len(b["now"])} now, {len(b["soon"])} soon)')


if __name__ == "__main__":
    main()
