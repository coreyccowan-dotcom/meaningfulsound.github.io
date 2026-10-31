#!/usr/bin/env python3
"""Regenerate the PedalEditor brand pages from one template.

    python3 build_brand_pages.py

Brand order: Strymon, Walrus, Meris, UAFX, Line 6, Chase Bliss, Eventide,
Hologram, then new brands alphabetically.
Moving a pedal from soon[] to now[] is the weekly edit.
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
  ("BigSky", "bigsky", "12 reverb machines, 148 controls. Room to Nonlinear, and everything that lives in between."),
  ("BigSky MX", "bigsky-mx", "Two independent engines, each running all 12 machines. 24 combinations, 362 controls."),
  ("blueSky V2", "bluesky-v2", "Plate, Room, Spring. 3 machines, 28 controls. Three good answers to the same question."),
  ("Brig", "brig", "3 machines, 24 controls. The 3205, the 3005, and the Multi. It knows which one you meant."),
  ("Cloudburst", "cloudburst", "1 machine: Ambient Reverb. 14 controls. The simplicity is the point."),
  ("Compadre", "compadre", "2 machines, 4 modes, 13 controls. Compressor or Boost. Studio or Squeeze. Clean or Dirty. Small pedal, complete map."),
  ("Deco", "deco-v2", "Tape Saturation and Doubletracker. 5 modes across 2 machines. All 36 controls, including the ones that feel like accidents."),
  ("DIG", "dig-v2", "1 machine, 21 controls. A delay pedal with a lot to say about one thing."),
  ("EC&#8209;1", "ec1", "Tape Echo, and nothing else. 16 controls, every one of them doing something."),
  ("El Capistan V2", "elcapistan-v2", "3 tape&#8209;echo machines across 9 modes, 108 controls. Fixed heads, multi&#8209;head combinations, and Sound on Sound. The manual was long."),
  ("Flint", "flint-v2", "Tremolo and reverb, 6 modes, 39 controls. Three decades of each, laid out in order."),
  ("Iridium", "iridium", "Round, Chime, Punch. 3 amp machines, 35 controls. Pick a room and stand in it."),
  ("Lex V2", "lex-v2", "1 machine, 22 controls. Everything the rotary does, surfaced."),
  ("Mobius", "mobius", "12 machines: Chorus, Flanger, Rotary, Vibe, Phaser, Filter, Formant, Vintage Trem, Pattern Trem, Autoswell, Destroyer, Quadrature. 123 controls. It&rsquo;s a lot."),
  ("NightSky", "nightsky", "1 machine, 54 controls. The gap between those two numbers is what makes it a NightSky."),
  ("Riverside", "riverside", "1 machine, 16 controls. Drive, mapped cleanly. Not everything needs 12 modes."),
  ("Sunset", "sunset", "Dual Overdrive. 1 machine, 18 controls. Both sides of it."),
  ("TimeLine", "timeline", "12 delay machines, 193 controls. dTape to Lo&#8209;Fi, in order. Every parameter the manual published."),
  ("UltraViolet", "ultraviolet", "Chorus, Blend, Vibrato. 3 machines, 18 controls. The whole range of what it does."),
  ("Volante", "volante", "3 machines, 116 controls. Studio, Drum, Tape. The number is not a typo."),
  ("Zelzah", "zelzah", "2 machines, 6 modes, 35 controls. Four&#8209;stage and six&#8209;stage, from Classic to Strong. All of it mapped."),
 ],
 "soon": [],
 "cost": "21 manuals. Every parameter table read, every range confirmed, every control cross&#8209;checked against what the pedal actually receives. It isn&rsquo;t glamorous work &mdash; mostly it&rsquo;s a PDF and a MIDI monitor and a question about whether this knob goes to 127 or to 100. The app holds the answer so you don&rsquo;t have to.",
},
{
 "slug": "walrus-audio", "brand": "Walrus",
 "blurb": "All 10 Walrus Audio pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Walrus speaks in variety more than uniformity. Most boxes hold 128 preset slots &mdash; the Meraki carries one, the Qi Etherealizer 127. Tempo lives on the D1 and M1 families; the ACS1 and R1 don&rsquo;t ask for it. 10 pedals. All of them read.",
 "now": [
  ("ACS1", "acs1-mk1", "3 voices &mdash; Fullerton, London, Dartford &mdash; and 23 controls. The MkII would double it."),
  ("ACS1 MkII", "acs1-mk2", "6 voices, 46 controls. The same three rooms as the original, then three more added in the revision."),
  ("D1", "d1", "5 delay machines, 41 controls. Digital, Mod, Vintage, Dual, Reverse. The clean read on delay."),
  ("D1 MkII", "d1-mkii", "6 machines, 76 controls. Everything the D1 said, plus Grain. The number grew accordingly."),
  ("M1", "m1", "6 machines, 18 modes, 242 controls. Chorus, Phaser, Tremolo, Vibrato, Rotary, Filter &mdash; three readings of each."),
  ("M1 MkII", "m1-mkii", "The same 6 machines, modes renamed, 249 controls. 7 more than the original. The difference is in the details."),
  ("Meraki", "meraki", "3 machines, 3 modes, 40 controls, 1 preset slot. Stereo analog delay with more to say than the enclosure implies."),
  ("Qi Etherealizer", "qi", "1 machine, 24 controls, 127 preset slots. Unusual arithmetic for an unusual pedal."),
  ("R1", "r1", "6 reverb machines &mdash; Spring, Hall, Plate, BFR, RFRCT, Air &mdash; and 59 controls. The original map."),
  ("R1 MkII", "r1-mkii", "The same 6 machines, 81 controls. The pedal kept its rooms; the profile grew to match what the MkII added."),
 ],
 "soon": [],
 "cost": "10 manuals. The M1 family alone runs to nearly 250 controls across 6 machines and 18 modes &mdash; the kind of profile that takes a while to get right. The ACS1 doubled between versions. The R1 gained 22 controls without changing its machine list. Every range confirmed, one at a time.",
},
{
 "slug": "meris", "brand": "Meris",
 "blurb": "All 8 Meris pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Meris runs two dialects, depending on which era you&rsquo;re holding. The older boxes give you 16 preset slots and a full-knob expression morph &mdash; both endpoints live inside the hardware preset, and the expression pedal sweeps between them. The LVX holds 99 slots and takes MIDI clock. 8 pedals. All of them read.",
 "now": [
  ("LVX", "lvx", "7 machines, 38 modes, 266 controls. Preamp, Delay, Dynamic, Pitch, Filter, Modulation, and a Looper &mdash; each with its own set of modes."),
  ("Enzo", "enzo", "4 synth&#8209;stage modes &mdash; Dry, Mono, Arp, Poly &mdash; 4 categories, 36 controls, 16 preset slots. The downstream filter, ring mod, and delay run in series regardless of mode."),
  ("Enzo X", "enzo-x", "5 concurrent effect sections &mdash; Synth, Drive, Ambience, Modulate, Filter &mdash; 25 algorithms, 192 controls, 99 preset slots. Takes MIDI clock."),
  ("Hedra", "hedra", "3&#8209;voice pitch shifter. 4 delay&#8209;routing modes, 37 controls, 16 preset slots. Series, Dual, and cross&#8209;feedback combinations &mdash; different signal topologies, same 3 voices."),
  ("Mercury7", "mercury7", "ULTRAPLATE and CATHEDRA. 2 machines, 27 controls, 16 preset slots. Two rooms; nothing else."),
  ("Mercury X", "mercury-x", "Reverb plus 5 optional processing modules &mdash; Preamp, Dynamics, Pitch, Filter, Modulation &mdash; each independently on or off. 7 categories, 36 algorithms, 207 controls, 99 preset slots."),
  ("Ottobit Jr.", "ottobit-jr", "Bit crusher with a 6&#8209;step sequencer targeting Pitch, Sample Rate, or Filter. 3 modes, 41 controls, 16 preset slots."),
  ("Polymoon", "polymoon", "Multi&#8209;tap modulated delay with a stereo dual Barberpole phaser. 1 machine, 20 controls, 16 preset slots."),
 ],
 "soon": [],
 "cost": "8 manuals. The older Meris line shares a house convention &mdash; 16 preset slots, hold&#8209;Alt to save, expression pedal morphing between two complete knob&#8209;state sets stored inside the loaded preset &mdash; but each box has its own CC map, and Mercury X and Enzo X run concurrent multi&#8209;slot topologies that the simpler siblings don&rsquo;t need. The LVX is the same brand and a different machine entirely. Every range confirmed, one at a time.",
},
{
 "slug": "uafx", "brand": "UAFX",
 "blurb": "All 14 UAFX pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "UAFX speaks a consistent dialect. Every pedal holds 128 preset slots. The amp modelers don&rsquo;t take MIDI clock &mdash; these are amps &mdash; but the effects line has its own shapes: the Galaxy &rsquo;74 follows clock, the Del&#8209;Verb runs two concurrent modules, and the Max maps two independent compressor engines onto separate CC blocks. 14 pedals. All of them read.",
 "now": [
  ("Dream &rsquo;65", "dream-65", "1 voice, 19 controls. Small and self&#8209;contained. The whole pedal in one profile."),
  ("Lion &rsquo;68", "lion-68", "3 channels &mdash; Super Bass, Super Lead, Brown &mdash; and 65 controls. Each voice mapped on its own."),
  ("Ruby &rsquo;63", "ruby-63", "Brilliant, Normal, Vibrato. 3 channels, 42 controls. The channel names are the pedal&rsquo;s own."),
  ("Woodrow &rsquo;55", "woodrow-55", "1 voice, 15 controls. The smallest of the amp modelers, and none of it left out."),
  ("Knuckles &rsquo;92 Rev F", "knuckles-92", "3 channels &mdash; Clean, Orange, Red &mdash; and 78 controls. All three accounted for."),
  ("ANTI 1992", "anti-1992", "Rhythm, Crunch, Lead. 3 channels, 77 controls. Near&#8209;identical in size to the Knuckles and the Enigmatic. Different box entirely."),
  ("Enigmatic &rsquo;82", "enigmatic-82", "Rock, Jazz, Custom. 3 channels, 78 controls. The third of the three&#8209;channel cluster."),
  ("Astra", "astra", "5 modulation effects &mdash; Chorus Brigade, Flanger Dblr, Trem 65, Phaser X90, Dharma Trem 61 &mdash; 36 controls. One control surface, five different maps."),
  ("Del&#8209;Verb", "del-verb", "Delay and Reverb running concurrently &mdash; 3 modes each, 25 controls. Two modules, independent on/off."),
  ("Galaxy &rsquo;74", "galaxy-74", "Space Echo and spring reverb, 2 machines, 17 controls. Takes MIDI clock."),
  ("Golden Reverberator", "golden-reverberator", "Spring 65, Plate 140, Hall 224, Chamber &amp; Plate 224. 4 reverbs, 12 algorithm variations, 78 controls."),
  ("Max", "max", "2 independent compressor engines, each with its own UA 610 preamp and 3&#8209;way type menu &mdash; Dyna, Opto LA&#8209;2A, FET 1176. 6 machines, 46 controls."),
  ("OX Stomp", "ox-stomp", "Speaker emulator. 1 Rig engine: 22 cab options, 2 close mics, 1 room mic, 4 internal effects. 31 controls."),
  ("Starlight", "starlight", "4 delay flavors &mdash; Tape EP&#8209;III, Analog DMM, Precision, Cooper Time Cube &mdash; 34 controls. Different Color and Mod semantics per flavor."),
 ],
 "soon": [],
 "cost": "14 manuals. The amp modelers were the first chapter &mdash; seven pedals sharing a house style, with the three&#8209;channel cluster (Knuckles, ANTI, Enigmatic) each landing at 77 or 78 controls, which sounds like a coincidence until you&rsquo;ve read all three. The effects line is more varied: the Galaxy runs concurrent echo and reverb with clock, the Max maps two entirely independent compressor engines, the OX Stomp is a speaker cabinet emulator with close&#8209;mic positioning. Different boxes, same method.",
},
{
 "slug": "line-6", "brand": "Line 6",
 "blurb": "The Line 6 DL4 MkII in PedalEditor, all 46 modes mapped, with four more Line 6 profiles built and releasing.",
 "lede": "Line 6 doesn&rsquo;t ask for a simple dialect. The DL4 MkII carries 128 preset slots, takes MIDI clock, and holds more modes than most brands have pedals. 1 available now. 4 more built and releasing.",
 "now": [
  ("DL4 MkII", "dl4-mkii", "2 machines &mdash; 30 delays and 16 reverbs &mdash; 46 modes, 241 controls. Vintage Digital through to Glitch. Room through to Reverb Off."),
 ],
 "soon": ["HX One", "M13", "M5", "M9"],
 "cost": "One manual. It was a long one. 30 delay modes and 16 reverb modes in a single pedal means 241 controls to confirm, one at a time. The HX One, M13, M5 and M9 are built and releasing. The DL4 took as long as it took. So will they.",
},
{
 "slug": "chase-bliss", "brand": "Chase Bliss",
 "blurb": "5 Chase Bliss pedals in PedalEditor, each profile built from the manufacturer's manual, with 21 more built and releasing.",
 "lede": "Chase Bliss runs a consistent house style. Most boxes hold 122 preset slots and take MIDI clock or tap tempo &mdash; though Generation Loss MKII takes neither, which the profile notes plainly. Dark World is the exception in the other direction: two independent reverb engines on two footswitches, each with its own on/off state. 5 available now. 21 more built and releasing.",
 "now": [
  ("Mood MkII", "mood-mkii", "2 machines &mdash; Wet Channel and Micro&#8209;Looper, 3 modes each &mdash; 6 modes total, 64 controls, 122 preset slots. Takes MIDI clock or tap."),
  ("Habit", "habit", "1 machine, 16 controls, 122 preset slots. Takes MIDI clock or tap. Its 6 modifiers run as a two&#8209;CC matrix &mdash; one named choice writes two CCs at once &mdash; so the profile carries a mechanism no other pedal in the library needed."),
  ("Generation Loss MKII", "generation-loss-mkii", "2 machines &mdash; MKII with 13 modes, Classic with 1 &mdash; 14 modes total, 143 controls, 122 preset slots. Takes no MIDI clock and no tap tempo at all. The profile says so rather than pretending otherwise."),
  ("Blooper", "blooper", "Looper. 3 modes &mdash; NORM, ADD, SAMP &mdash; 46 controls, 16 loop slots, 122 preset slots. Takes MIDI clock or tap. Transport and modifier controls live as CC&#8209;emulated gestures."),
  ("Dark World", "dark-world", "Dual reverb &mdash; Dark channel (Cooper FX), World channel (Keeley) &mdash; 2 circuits, 6 algorithms, 18 controls, 122 preset slots. Both channels are independently on/off; the profile maps all 4 engagement states."),
 ],
 "soon": ["Bliss Factory", "Brothers", "Brothers AM", "Clean", "Condor", "CXM 1978", "Generation Loss", "Gravitas", "Lossy", "Lost + Found", "MOOD", "Onward", "Preamp MKII", "Reverse Mode C", "Spectre", "Thermae", "Tonal Recall", "Warped Vinyl HiFi", "Warped Vinyl MkII", "Wombtone MkI", "Wombtone MkII"],
 "cost": "5 available now. 21 more built and releasing. Chase Bliss publishes thorough MIDI specs, and the audits still turn up things worth knowing &mdash; Generation Loss MKII has 143 controls and no clock input at all; Habit&rsquo;s modifier matrix meant extending the profile model before it could be expressed correctly; Dark World is a multi&#8209;circuit pedal with a composite bypass encoding. Every control confirmed against the manual before it ships.",
},
{
 "slug": "eventide", "brand": "Eventide",
 "blurb": "7 Eventide profiles built for PedalEditor and held back from release while the brand's MIDI implementation is worked through.",
 "lede": "Eventide is the one brand we have pulled back. The pedals are superb and their MIDI is not: nothing in the line can change algorithm over MIDI by any message, and on Space and TimeFactor every control knob arrives unassigned &mdash; you have to patch all 10 by hand in the pedal&rsquo;s System Mode before an app can reach any of them. Profiles exist for 7 Eventide pedals. None are listed as available, because &ldquo;works after you configure the pedal for 20 minutes&rdquo; is not what available should mean.",
 "now": [],
 "soon": ["H9 Harmonizer", "Knife Drop", "Rose", "Space", "TimeFactor", "TriceraChorus", "UltraTap"],
 "cost": "0 available. 7 built, none released yet. The work is done &mdash; the H9 profile alone runs to 520 controls across 52 modes. What is not done is an honest answer to the setup problem. Every other brand here works the moment you connect it, and until Eventide can say the same, listing these as available would be selling a manual&rsquo;s worth of homework as a feature.",
},
{
 "slug": "hologram", "brand": "Hologram",
 "blurb": "All 3 Hologram Electronics pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Hologram builds pedals with unusual internal structures. The Microcosm runs 4 concurrent machines. The Chroma Console puts 4 independent effect slots in series, each running any of 5 effects or Off, in a per&#8209;preset order set on the pedal. The Dream Sequence is a 3&#8209;voice rhythmic pitch shifter driven by a step sequencer &mdash; its voice&#8209;level CCs double as real&#8209;time trigger events after a MIDI Start. 3 pedals. All of them read.",
 "now": [
  ("Microcosm", "microcosm", "4 machines &mdash; Micro Loop, Granules, Glitch, Multidelay &mdash; 11 modes total, 205 controls, 60 preset slots. Takes MIDI clock or tap."),
  ("Chroma Console", "chroma-console", "4 concurrent effect slots &mdash; Character, Movement, Diffusion, Texture &mdash; 24 algorithms across 4 machine families, 100 controls, 80 preset slots. Takes MIDI clock or tap."),
  ("Dream Sequence", "dreamsequence", "3&#8209;voice pitch shifter with step sequencer. 4 controls, 35 preset slots across 3 banks. Takes MIDI clock."),
 ],
 "soon": [],
 "cost": "3 manuals. The Microcosm runs to 205 controls across 4 machines. The Chroma Console is a different shape &mdash; 4 independent effect slots, each with its own algorithm menu, the per&#8209;slot Off state tracked so the LED dims honestly when a slot is muted. The Dream Sequence is the smallest in surface area and has the most unusual MIDI behavior: voice&#8209;level CCs become pattern&#8209;recording triggers after a MIDI Start. Every pedal was its own read.",
},
{
 "slug": "alexander", "brand": "Alexander Pedals",
 "blurb": "The Alexander Radical Delay DX in PedalEditor, built from the manufacturer's manual.",
 "lede": "Alexander Neo&#8209;series pedals share a consistent MIDI template: 8 knob CCs, 1 mode&#8209;select CC, 4 utility CCs for tap, ramp, expression and bypass, and 16 preset slots across 4 color banks. 1 available now.",
 "now": [
  ("Radical Delay DX", "radical-delay-dx", "6 delay modes &mdash; MOD, BEND, DUAL, REV, ARP, DYNA &mdash; 51 controls, 16 preset slots. Takes MIDI clock or tap. Five of the six modes transform the signal beyond standard delay."),
 ],
 "soon": [],
 "cost": "1 manual. The Neo&#8209;series template means the CC map is consistent &mdash; knob positions, tap, ramp, expression, bypass &mdash; but the 6 modes each do something different to the signal, and the profile names what each one is. That part still required reading the manual.",
},
{
 "slug": "boss", "brand": "Boss",
 "blurb": "2 Boss pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Boss runs a deep MIDI spec. The DD&#8209;500 has 12 delay modes and an 8&#8209;slot assign system that lets the user route any of 62 CCs to any editable target &mdash; the profile maps what the factory gives you. The RE&#8209;202 models 12 Space Echo head configurations, 112 controls, and takes MIDI clock. 2 available now.",
 "now": [
  ("DD&#8209;500", "dd500", "12 delay modes, 55 controls. Factory assign slots documented; the ASSIGN system&rsquo;s 62&#8209;CC target space is in the manual notes."),
  ("RE&#8209;202", "re202", "12 Space Echo modes &mdash; Mode 1 through Mode 12 &mdash; 112 controls. Takes MIDI clock."),
 ],
 "soon": [],
 "cost": "2 manuals. The DD&#8209;500&rsquo;s assign system runs 8 slots, each routable to any of 62 MIDI sources &mdash; mapping the factory defaults and documenting the space is not the same work as mapping a fixed CC table. The RE&#8209;202 has 112 controls across 12 head configurations. Both rewarded a close read.",
},
{
 "slug": "digitech", "brand": "DigiTech",
 "blurb": "The DigiTech Whammy in PedalEditor, built from the manufacturer's manual.",
 "lede": "The Whammy has 21 factory pitch effects and 1 control &mdash; the expression pedal. MIDI selects effects via Program Change; CC 11 is the only CC. 1 available now.",
 "now": [
  ("Whammy", "whammy", "3 families &mdash; Whammy (10), Detune (2), Harmony (9) &mdash; 21 algorithms, 1 global control. No user preset slots; factory effects are the map."),
 ],
 "soon": [],
 "cost": "1 manual. The Whammy is the shortest profile in the library by control count and one of the more structurally unusual ones: 21 mutually exclusive factory algorithms, no user editable state, and a bypass encoding where PC 0-20 means engaged and PC 21-41 means the same effect bypassed. Both halves documented.",
},
{
 "slug": "ehx", "brand": "Electro-Harmonix",
 "blurb": "The Electro-Harmonix POG3 in PedalEditor, built from the manufacturer's manual.",
 "lede": "The POG3 is a single&#8209;algorithm pedal with 100 preset slots and 37 controls covering six independent voice levels, six voice pans, EQ, envelope, and output routing. 1 available now.",
 "now": [
  ("POG3", "pog3", "Polyphonic octave generator. 1 algorithm, 37 controls, 100 preset slots. Six voices &mdash; dry, &minus;2 oct, &minus;1 oct, +5th, +1 oct, +2 oct &mdash; each with its own level and pan."),
 ],
 "soon": [],
 "cost": "1 manual. 37 controls in one algorithm means every parameter is visible at once: voice levels, voice pans, Q, envelope, spread, attack, filter, detune, dry routing toggles per voice, focus, expression enable, three output enables. Reading the CC map end to end and confirming the ranges is the whole job.",
},
{
 "slug": "empress", "brand": "Empress Effects",
 "blurb": "2 Empress Effects pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Empress runs a compact house spec: Program Change recall, a dedicated save CC (CC 39 with slot value), and a mode&#8209;formula selector where the wire value encodes category and submachine in a single byte. The Echosystem extends that with a dual&#8209;engine structure &mdash; two independent delay engines, each with 43 sub&#8209;modes, combined by a 4&#8209;state routing selector. 2 available now.",
 "now": [
  ("Echosystem", "echosystem", "Dual&#8209;engine delay. 2 engines, 43 sub&#8209;modes each, 14 controls. Routing between engines &mdash; Trails, Parallel, Serial, Left&#8209;Right &mdash; is itself a CC."),
  ("Reverb", "reverb", "12 reverb machines, 32 sub&#8209;modes, 233 controls. Hall through Lo&#8209;Fi, each with its own parameter set."),
 ],
 "soon": [],
 "cost": "2 manuals. The Reverb profile runs to 233 controls across 12 machines and 32 sub&#8209;modes &mdash; the mode&#8209;formula encoding means every sub&#8209;mode is a distinct wire value from a sparse 128&#8209;slot space. The Echosystem layers a dual&#8209;engine structure on top: two independent trees, each a 43&#8209;submode version of the same machine list, routed against each other. Both required reading the formula before reading the map.",
},
{
 "slug": "gfi", "brand": "GFI System",
 "blurb": "The GFI System Specular Tempus in PedalEditor, built from the manufacturer's manual.",
 "lede": "The Specular Tempus holds 36 algorithms &mdash; 13 reverbs, 17 delays, 6 hybrids &mdash; and 32 preset slots. Algorithm selection is on&#8209;pedal only; MIDI Program Change loads whichever algorithm was last saved to a slot. 1 available now.",
 "now": [
  ("Specular Tempus", "specular-tempus", "3 banks &mdash; Reverb (13), Delay (17), Hybrid (6) &mdash; 36 algorithms, 151 controls, 32 preset slots. Algorithm choice is per&#8209;preset, set from the panel."),
 ],
 "soon": [],
 "cost": "1 manual. The Specular Tempus has no MIDI algorithm&#8209;select at any transport, which means the 36 algorithms can only be reached by loading a saved preset that already has one. The profile documents the on&#8209;pedal algorithm&#8209;select gesture and maps all 151 controls across the three banks. The firmware v3.8 manual was the source.",
},
{
 "slug": "jackson-audio", "brand": "Jackson Audio",
 "blurb": "5 Jackson Audio pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Jackson Audio runs a small, consistent MIDI spec: 5 CCs over TRS RING, Program Change for the pedals that have selectable modes. Most of the line is multi&#8209;circuit &mdash; two independent footswitches with no single master&#8209;off &mdash; so the profiles map separate on/off states for each circuit. 5 available now.",
 "now": [
  ("ASABI", "asabi", "Dual&#8209;circuit overdrive/distortion &mdash; DIST + DRIVE &mdash; 2 circuits, 5 controls. Mateus Asato signature. No preset slots."),
  ("Bloom V2 MIDI", "bloom-v2", "Compressor + EQ + Boost. 3 circuits &mdash; comp, eq, boost &mdash; 6 factory compression modes via PC, 5 controls. No user preset slots."),
  ("Broken Arrow", "broken-arrow", "Dual&#8209;circuit drive &mdash; TS&#8209;808&#8209;style DRIVE + MOSFET BOOST &mdash; 2 circuits, 5 controls. No preset slots."),
  ("Golden Boy", "golden-boy", "Dual&#8209;circuit drive &mdash; transparent DRIVE (4 selectable clipping modes) + MOSFET BOOST &mdash; 2 circuits, 5 controls. No preset slots."),
  ("New Wave", "new-wave", "Analog BBD chorus/vibrato/rotary. 7 factory&#8209;curated modes via PC, 10 controls. User&#8209;editable slots; save is a panel gesture."),
 ],
 "soon": [],
 "cost": "5 manuals. Three of the five are structurally identical &mdash; ASABI, Broken Arrow, Golden Boy all run two circuits with a shared Gain Cycle gesture and per&#8209;circuit clipping program modes reachable via CC. The Bloom V2 adds a third circuit and factory compression modes. The New Wave is the modulation outlier: 7 BBD modes, mode&#8209;specific parameter states, and an EEPROM that holds what the factory set unless the user overwrites it. Each read separately.",
},
{
 "slug": "keeley", "brand": "Keeley Electronics",
 "blurb": "The Keeley Nocturne in PedalEditor, built from the manufacturer's manual.",
 "lede": "The Nocturne is an Andy Timmons HALO reverb with 3 modes &mdash; Nocturne, Spring, Plate &mdash; and 72 preset slots across 24 banks. MIDI is enabled by a power&#8209;up gesture; the jack defaults to Expression. 1 available now.",
 "now": [
  ("Nocturne", "nocturne", "3 reverb modes &mdash; Nocturne, Spring, Plate &mdash; sharing 7 CCs, 29 controls, 72 preset slots across 24 banks. MIDI enable is a power&#8209;up hold."),
 ],
 "soon": [],
 "cost": "1 manual. The Nocturne&rsquo;s 3 modes share the same 7 CCs, so the profile carries 3 sets of labeled controls for the same wire addresses &mdash; what each knob does in Spring is different from what it does in Plate. The 72&#8209;slot bank structure and the EXP&#8209;default jack behavior are both documented. Manual was the source.",
},
{
 "slug": "old-blood-noise", "brand": "Old Blood Noise",
 "blurb": "The Old Blood Noise Endeavors Dark Star Stereo in PedalEditor, built from the manufacturer's manual.",
 "lede": "The Dark Star Stereo is a single&#8209;algorithm stereo soundscape reverb with 127 preset slots and a two&#8209;step MIDI save gesture. 1 available now.",
 "now": [
  ("Dark Star Stereo", "dark-star-stereo", "Stereo reverb. 1 algorithm, 18 controls, 127 preset slots. Per&#8209;preset expression assignment via panel gesture; CC 11 is the expression wire."),
 ],
 "soon": [],
 "cost": "1 manual. The Dark Star Stereo&rsquo;s 18 controls include the three side trims (Volume, Mix, Spread) that are easy to miss on a first pass. The two&#8209;step MIDI save gesture &mdash; CC 25 arm, PC target, CC 25 confirm &mdash; is documented alongside the 5&#8209;second pedal&#8209;hold path. Firmware V3.0Q was the source.",
},
{
 "slug": "red-panda", "brand": "Red Panda",
 "blurb": "The Red Panda Particle V2 in PedalEditor, built from the manufacturer's manual.",
 "lede": "The Particle V2 is a granular pedal with 8 modes in 2 families &mdash; 3 Pitch modes and 5 Delay modes &mdash; each with 3 shared knobs and 2 mode&#8209;specific knobs. MIDI clock is supported. 1 available now.",
 "now": [
  ("Particle V2", "particle-v2", "8 granular modes &mdash; Pitch&plus;Density, Pitch&plus;LFO, Pitch&plus;Detune, Delay&plus;Random, Delay&plus;Pitch, Delay&plus;Reverse, Delay&plus;LFO, Delay&plus;Density &mdash; 61 controls, 127 preset slots. Takes MIDI clock."),
 ],
 "soon": [],
 "cost": "1 manual. Firmware 2.2.0+ is the source for the Particle V2&rsquo;s mode list and CC table. The PARAM knob remaps per mode &mdash; each destination has its own dedicated CC, and the profile maps all 8 destinations in their respective modes rather than collapsing them into aliases. 61 controls confirmed against the published map.",
},
{
 "slug": "source-audio", "brand": "Source Audio",
 "blurb": "2 Source Audio pedals in PedalEditor, each profile built from the manufacturer's manual.",
 "lede": "Source Audio publishes detailed MIDI maps but the structures behind them are not simple. The Nemesis has 24 addressable delay engines on a single CC; the engine load resets other parameter defaults, so engine&#8209;select arrives first in every deploy. The Ventris runs two independent 56&#8209;bit reverb processors simultaneously, each holding 14 engines, with a 4&#8209;state routing selector between them. 2 available now.",
 "now": [
  ("Nemesis ADT", "nemesis", "24 delay engines selected by CC 1, each with its own character. 1 category, 24 algorithms, and the shared control set: 40 parameters per engine including modulation, pitch, filter, tape, and pattern modes. 128 preset slots."),
  ("Ventris Dual Reverb", "ventris", "2 concurrent reverb processors, 14 engines each, 28 algorithms, 477 controls, 128 preset slots. Routing between them &mdash; A only, B only, Parallel, Cascade &mdash; is CC 50."),
 ],
 "soon": [],
 "cost": "2 manuals and 2 MIDI implementation PDFs. The Nemesis engine&#8209;load side effect &mdash; when you change engines, the other parameters reset to their per&#8209;engine defaults &mdash; is the kind of behavior that only surfaces if you read the MIDI implementation closely. The Ventris maps two independent 14&#8209;engine trees with per&#8209;engine assignable macro knobs (Engine Params 1-5), each named per the manual&rsquo;s per&#8209;engine tables. 477 controls confirmed end to end.",
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
.pedal h3 a{{text-decoration:none;transition:color .15s ease}}
.pedal h3 a:hover{{color:var(--terracotta)}}
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
footer .social{{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px}}
footer .social svg{{width:18px;height:18px;display:block}}
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

{now}
{soon}
  <h2>What fluency cost</h2>
  <div class="cost">
    <p>{cost}</p>
  </div>

  <h2>Facts</h2>
  <div class="facts">
    <p>Available on iPhone, iPad and Mac. Connects over Bluetooth LE MIDI, Wi&#8209;Fi (RTP&#8209;MIDI) and USB. Bluetooth pairing happens inside the app on iPhone and iPad; on Mac you pair in Audio MIDI Setup.</p>
    <p>No account. No ads. No cross&#8209;app tracking. Anonymous usage telemetry only &mdash; no personal data. iCloud sync across your devices at no extra cost, with a local fallback if iCloud isn&rsquo;t available. Presets, songs and full backups export as files.</p>
    <p class="price">Every profile is built from the manufacturer&rsquo;s manual and audited before it ships. <a href="../profiles/">The full list is here</a> &mdash; what&rsquo;s in the app today, and what&rsquo;s built and releasing.</p>
  </div>

  <footer>
    <a href="../">PedalEditor</a>
    <a href="/">Meaningful Sound</a>
    <a href="../reference/">Reference</a>
    <a href="../privacy/">Privacy</a>
    <a class="social" href="https://instagram.com/pedaleditor" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5" ry="5" fill="none" stroke="currentColor" stroke-width="1.75"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.75"/><circle cx="17.5" cy="6.5" r="1.15" fill="currentColor"/></svg></a>
    <a class="social" href="https://tiktok.com/@pedaleditor" target="_blank" rel="noopener" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M19.5 8.6a6.4 6.4 0 0 1-3.8-1.2v7.4a5.4 5.4 0 1 1-5.4-5.4v3a2.4 2.4 0 1 0 2.4 2.4V2.5h2.9a4.3 4.3 0 0 0 3.9 4z" fill="currentColor"/></svg></a>
    <a class="social" href="https://youtube.com/@meaningfulsound" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.6 3.6 12 3.6 12 3.6s-7.6 0-9.4.5A3 3 0 0 0 .5 6.2C0 8 0 12 0 12s0 4 .5 5.8a3 3 0 0 0 2.1 2.1c1.8.5 9.4.5 9.4.5s7.6 0 9.4-.5a3 3 0 0 0 2.1-2.1c.5-1.8.5-5.8.5-5.8s0-4-.5-5.8zM9.6 15.6V8.4L15.8 12z" fill="currentColor"/></svg></a>
    <span class="updated">Updated {updated}</span>
  </footer>

</div>
</body>
</html>
"""


def main():
    updated = datetime.date.today().strftime("%-d %B %Y")
    for b in BRANDS:
        now = ""
        if b["now"]:
            n_now = f'{len(b["now"])} pedal' + ("" if len(b["now"]) == 1 else "s")
            cards = "\n".join(
                f'  <div class="pedal">\n    <h3><a href="{slug}/">{name}</a></h3>\n    <p>{line}</p>\n  </div>'
                for name, slug, line in b["now"]
            )
            now = (
                f'  <h2>Available Now &mdash; {n_now}</h2>\n'
                '  <p class="note">In the app today. Every one built to spec.</p>\n'
                f'{cards}'
            )
        soon = ""
        if b["soon"]:
            names = " &middot; ".join(b["soon"])
            soon = (
                f'\n  <h2>Coming Soon &mdash; {len(b["soon"])} pedals</h2>\n'
                '  <p class="note">Already built. Each is checked against its manual before it ships.</p>\n'
                f'  <div class="soonlist">{names}</div>\n'
            )
        page = PAGE.format(
            brand=b["brand"], slug=b["slug"], blurb=html.escape(b["blurb"], quote=True),
            lede=b["lede"], now=now, soon=soon, cost=b["cost"],
            updated=updated,
        )
        d = os.path.join(OUT, b["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w") as fh:
            fh.write(page)
        print(f'wrote PedalEditor/{b["slug"]}/  ({len(b["now"])} now, {len(b["soon"])} soon)')


if __name__ == "__main__":
    main()
