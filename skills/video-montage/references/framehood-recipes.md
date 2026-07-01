# Framehood assembly recipes — concrete tool calls

This is the wiring layer: how the format rules map to actual Framehood tool
calls, with real parameters, ordering, and audio levels. Read the format
reference for *what* to build; read this for *how* to call the tools.

All outputs are files. Chain them: each tool returns a file you feed to the next.

---

## The workhorse: `video(assemble)`

Combines clips + audio into one finished video in a single pass. It sequences
clips, lays music/VO/SFX beds at set levels, applies intro/ending treatment and
inter-clip transitions. Prefer ONE well-planned `assemble` over many patch calls.

Key parameters (and sane defaults):

| Param | What it does | Default / guidance |
|---|---|---|
| `clips[]` | ordered clip URLs | required; order = your cut plan |
| `music` | background music URL | fit to video length (trim/loop), never extends video |
| `music_level` | music bed dB | **-24** (under VO/clips). Doc: -24 to -20. Reel w/o VO: 0 to -6 |
| `vo` | voiceover URL mixed over clips | must fit within video length |
| `vo_level` | VO dB | **0** (reference level; everything else sits under it) |
| `sfx_ambient` | ambient bed URL | fit to length |
| `sfx_level` | ambient SFX dB | **-18** |
| `keep_clip_audio` | keep clips' own audio, mix music under it | **true**. Set false only for a music-only bed that replaces clip audio |
| `clip_audio_level` | dB on kept clip audio | 0 (with keep_clip_audio) |
| `xfade_duration` | visual transition seconds | **0.2**. Social 0.1–0.3; cinematic 0.5–1.0; loop = 0 (hard cut) |
| `intro` | `{fade_in, fade_in_duration, sfx}` | social/ads: `fade_in:false` (hard start). Doc: `fade_in:true` |
| `ending` | `{type, black_tail, end_sfx, ...}` | `social` = fast fade + end hit; `cinematic` = 1s fade + black tail; `loop` = hard cut |
| `format` | aspect | `9:16` social/vertical ad; `1:1` feed; `16:9` YT/doc |
| `tier` | `standard`\|`pro` | `pro` for client deliverables |

**Audio hierarchy rule of thumb:** VO at 0 → clip audio at 0 → SFX at -18 →
music at -24. Voice always wins.

---

## Length reconciliation — NEVER truncate the voiceover

The most common assembly bug: the VO/narration is longer than the video, so its
tail gets silently cut off. Root cause — these tools do **not** auto-extend video
to fit audio:

- `video(assemble)` `vo`: *"must fit within the assembled video length."* Longer
  VO → tail dropped. **No auto-extend.**
- `video(assemble)` `music` / `sfx_ambient`: auto-fit to video (trim if long,
  loop if short) — these never extend the video either.
- `audio(mix)` `music` bed: auto-fit to the **voice** length + ducked (safe).
- `video(lipsync)` `sync_mode`: `loop` = video repeats to cover longer audio
  (**never drops speech** — the safe default); `cut_off` = trims to shorter and
  **silently drops the longer audio's tail** (only when audio provably fits);
  `silence` = pads shorter audio; `remap` = speeds video to match.

### The protocol (run before every voice-led assemble)

1. **Measure the spine.** Note the duration of the `audio(speak)` output. If you
   only have a script, estimate: `seconds ≈ words / 2.7` (TTS ≈ 2.5–3 wps).
2. **Sum the planned clips.** Add up every clip's duration (you set these:
   `image(animate)` `duration`, `video(create)` `duration`, or known lengths of
   uploaded clips).
3. **Compare.** Require `sum(clips) ≥ VO_length + 0.5s` tail.
4. **If video is SHORTER, extend it (don't shorten the VO):**
   - add another B-roll/beat shot,
   - increase an `image(animate)` `duration`,
   - hold on a final frame,
   - loop a B-roll clip.
   Then re-sum and re-check.
5. **If video is LONGER,** that's fine for `vo` (VO ends, video continues) — but
   don't leave a silent draggy tail; end shortly after the VO with `ending`.
6. **Lip-sync case:** if a talking character clip is shorter than its VO line,
   `video(lipsync)` with `sync_mode:"loop"` — the video loops to cover the full
   line, speech is never cut. Never use `cut_off` unless you've confirmed the
   clip is longer than the audio.
7. **Verify after assembly:** `qa(action:"transcript")` — if the last words of
   the script are missing from the transcript, the VO was truncated → extend the
   video and re-assemble.

Quick worked example: VO = 22s (60-word script ÷ 2.7 ≈ 22s). Planned clips:
5 shots × ~3s = 15s → **7s short → VO tail would be cut.** Fix: add ~3 more shots
(or extend animate clips) to reach ≥ 22.5s before calling `assemble`.

---

## Shot pacing — enforce the shot-length ceiling

Do not hand `assemble` a few long clips. Break the footage into many short shots:

| Format | Shot length | Rough shot count |
|---|---|---|
| Reel/Short/TikTok | 1.5–3s, cut on beat | ~8–15 shots in 30s |
| Ad body | 1.5–3s (hook 1–3s, proof may hold 3–4s, CTA 2–4s) | ~6–12 in 20s |
| Mini-doc B-roll | change every 3–5s (interview A-roll runs as its bite needs) | as story needs |

Nothing static hangs longer than ~3–4s (short-form/ad) or ~5s (doc B-roll). If a
generated clip is longer than its slot, split it or trim it before assembly. If
you have too few parts to hit the pacing, generate more short beats or animate
stills — don't stretch three clips across 30 seconds.

### Recipe A — Reel/Short (music-led, no VO)

```
video(action="assemble",
  clips=[hook, beat1, beat2, payoff],
  music=trending_or_bed,          music_level=-3,   # music is the driver here
  format="9:16", tier="pro",
  xfade_duration=0.15,            # fast, cut on beat
  intro={fade_in:false},         # hard start, no intro
  ending={type:"loop"},          # loop for replays
  out="reel_v1.mp4")
→ video(action="captions", video_url="reel_v1.mp4", out="reel_v1_cc.mp4")
```

### Recipe B — Performance ad (VO-led over music bed, hard CTA)

```
audio(action="speak", text=vo_script, voice="Brian", out="vo.mp3")   # tight, energetic
video(action="assemble",
  clips=[hook, problem, solution, proof, cta],
  vo="vo.mp3",                   vo_level=0,
  music=bed,                     music_level=-24,   # sits under VO
  keep_clip_audio=true,
  format="9:16", tier="pro",
  xfade_duration=0.2,
  intro={fade_in:false},
  ending={type:"social", end_sfx=cta_hit, end_sfx_start=...},
  out="ad_body.mp4")
→ video(action="captions", video_url="ad_body.mp4", out="ad_v1.mp4")
```

Hook/CTA text overlays: plan them explicitly; `captions` covers the spoken spine,
but the hook line and CTA line often need their own emphasized overlay treatment.

### Recipe C — Mini-doc (interview A-roll + B-roll + music under)

```
# 1. Radio edit: sequence interview sync first
audio(action="concat", tracks=[bite1, bite2, bite3], out="sync.mp3")   # or trim per bite
# 2. Music bed
audio(action="music", prompt="warm restrained underscore", is_instrumental=true, out="score.mp3")
# 3. Assemble visuals over the sync, music under everything
video(action="assemble",
  clips=[establish_broll, interview1, process_broll, interview2, outcome_broll],
  vo="sync.mp3", vo_level=0,     # the interview spine — foreground voice over the clips
  music="score.mp3",             music_level=-22,
  keep_clip_audio=true, clip_audio_level=0,
  format="16:9", tier="pro",
  xfade_duration=0.6,            # let it breathe
  intro={fade_in:true, fade_in_duration:1},
  ending={type:"cinematic", black_tail:1},
  out="doc_rough.mp4")
→ video(action="captions", video_url="doc_rough.mp4", out="doc_v1.mp4")
```

---

## Voiceover: `audio(speak)`

```
audio(action="speak", text="...", voice="Rachel"|"Brian"|"George", out="vo.mp3")
```
- Keep ad VO tight and energetic; re-write the script shorter if the read drags.
- For a doc, the VO/interview IS the radio edit — get it right before visuals.

## Audio mixing: `audio(mix)` (music bed UNDER voice, auto-ducked)

Use when you need to pre-blend a voice track with a ducked music bed *before*
assembly (e.g. a narration + bed you'll then lay on the video):

```
audio(action="mix",
  tracks=[voice.mp3],            # primary program
  music=bed.mp3,                # auto-fit to voice length + ducked
  music_level=-18,              # bed dB relative to voice
  out="narration_mixed.mp3")
```
Note: in `audio(mix)`, `music_level` default is -18 (voice-relative). This differs
from `video(assemble)` where music sits at -24 under a full clip mix.

## Lip-sync: `video(lipsync)` — do this BEFORE assembling a talking clip

```
video(action="lipsync", video_url=character_clip, audio_url="vo.mp3",
      sync_mode="loop",          # NEVER drops speech; loops video to cover audio
      out="char_synced.mp4")
```
- `loop` is the safe default — if audio is longer than video, video repeats.
- `cut_off` silently drops the tail of longer audio — only when audio fits.

## Captions: `video(captions)` — near-always the last visual step

```
video(action="captions", video_url=assembled, out="final_cc.mp4")
```
Mandatory for every format (mute-first). Keep inside safe zone. Request
**dynamic** captions where the tool supports it: word-by-word / phrase reveal,
key words emphasized by colour or scale — they double as a pacing device. Don't
ship a static paragraph of text.

## Colour grading — consistent cinematic look

Framehood has no dedicated "grade" slider, so achieve grade two ways:

1. **Bake it at generation.** When creating/animating clips, put the palette and
   mood in the prompt: "warm skin tones, cool teal shadows, cinematic contrast,
   filmic". Cheapest and most consistent — every clip is born on-palette.
2. **Restyle pass with `video(edit)`.** For clips already shot/generated, run a
   grade as a light restyle and keep `strength` LOW (≈0.15–0.3) so content is
   preserved and only look shifts:
   ```
   video(action="edit", video_url=clip, strength=0.2,
     prompt="cinematic colour grade, warm highlights, cool teal shadows, filmic contrast",
     out="clip_graded.mp4")
   ```
   Apply the **same** grade prompt to every clip so the sequence matches — a
   mismatched grade across clips is the #1 "cheap" tell. Grade BEFORE `assemble`.

Pick the palette for mood: warm = romance/comfort; cool desaturated = thriller/
suspense; high-contrast = confrontation. Warm skin vs cool shadow is the default
"expensive" look.

## Sound design — exaggerated SFX on the beat

Music/VO levels handle the mix; discrete SFX hits make cuts feel intentional.

1. **Generate hits** with `audio(sfx)`:
   ```
   audio(action="sfx", prompt="cinematic whoosh into reveal", out="whoosh.mp3")
   audio(action="sfx", prompt="deep impact hit / boom", out="impact.mp3")
   ```
2. **Place them on the cut / action**, not floating:
   - Intro/opening hit → `assemble` `intro.sfx`.
   - Cliffhanger/CTA sting → `assemble` `ending.end_sfx` (+ `end_sfx_start`).
   - Mid-video hits synced to specific cuts → layer post-assembly with
     `video(mix_audio)` (tracks timed to the cut points), or include as
     `sfx_ambient` if it's a continuous tension bed (riser under a cliffhanger).
3. Keep them slightly exaggerated and tight to picture. A hit that lands 3 frames
   off feels wrong — sync to the transition/action.

Levels: SFX around -18 under a 0-level voice (see hierarchy above); a punctuation
sting on a cliffhanger can sit louder for impact.

## Overlay extra audio post-assembly: `video(mix_audio)`

Only when you need to layer VO/music/SFX onto an already-finished video:
```
video(action="mix_audio", video_url=final, tracks=[extra_sfx.mp3], out="final_mix.mp4")
```
Prefer doing audio inside `assemble`; use this for late additions.

## Animate stills into motion: `image(animate)`

If a "part" is a still image, animate it before assembly. Multi-shot timeline:
```
image(action="animate", image_url=still,
  multi_prompt=[{prompt:"slow push in", duration:3}, {prompt:"pan left", duration:2}],
  format="9:16", tier="pro", out="animated.mp4")
```
- Single-shot: use `prompt` + `duration` instead of `multi_prompt` (mutually exclusive).
- Cap: ≤6 shots, combined ≤15s. Start each prompt with the camera move, then motion.

---

## QA gates: `qa`

| Call | When |
|---|---|
| `qa(action="transcript", video=...)` | any spoken/caption content — verify names, numbers, claims, CTA wording |
| `qa(action="scene", video=..., plan={...})` | confirm the cut matches your plan |
| `qa(action="full", video=...)` | client deliverable — 9 checks; long-running, poll `get_status` until `done:true`, read `verdict` |
| `qa(action="voice", audio=...)` | consistent VO across a multi-clip piece |

Single checks return a verdict in one call. `full` is async → poll `get_status`.

---

## Ordering checklist (glue it together)

1. Stills → `image(animate)` into clips.
2. VO → `audio(speak)`; doc sync → `audio(concat)`/`audio(trim)` = radio edit.
3. **Length pre-flight** → measure VO/spine duration; ensure `sum(clips) ≥
   spine + 0.5s`; extend video if short (see "Length reconciliation"). Check no
   shot exceeds the shot-length ceiling.
4. Talking characters → `video(lipsync)` (`sync_mode:"loop"` — never drops speech).
5. Music → `audio(music)` (instrumental, under voice).
6. **`video(assemble)`** — the one pass that does the montage.
7. `video(captions)`.
8. `qa(...)` gates — including `transcript` to confirm the VO wasn't truncated →
   fix the failing segment → re-`assemble` (don't rebuild).
9. Deliver. For ads: offer 3–5 hook variants off the same body.
