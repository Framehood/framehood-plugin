---
name: video-montage
description: >
  Assemble a finished video from multiple parts — clips, voiceover, music, SFX,
  captions — following the editing conventions of the target format. Use this
  skill WHENEVER a client asks to build, cut, assemble, edit together, or
  "make a video out of these pieces", and especially when the deliverable is a
  Reel / Short / TikTok, a performance or brand ad, a scripted vertical
  mini-drama / micro-drama (ReelShort/DramaBox style — cliffhangers, emotional
  close-ups), or a mini-documentary / storytelling piece. Trigger even if the
  client doesn't name the format
  explicitly ("собери ролик из этих кусков", "make me a 30s ad", "cut this into
  a reel", "put these shots together with music and subtitles"). This skill maps
  format rules to concrete Framehood tool calls (video assemble / audio mix /
  video captions / video mix_audio / video lipsync / image animate / qa).
---

# Video Montage

You are editing raw parts into a finished video. Editing is **sequencing +
rhythm + audio design**, not decoration. Your job: identify the format, apply
its rules, then assemble it with Framehood tools and QA the result before
delivering.

Never dump all clips into one `assemble` call and hope. Plan the cut first.

---

## Step 0 — Detect the format

Pick ONE primary format. If the client is ambiguous, ask a single question, then
default to **Reel/Short/TikTok** (the most common request).

| Signal in the request | Format | Read this reference |
|---|---|---|
| "reel", "short", "tiktok", vertical, ≤60s, "for social", "hook" | Short-form vertical | `references/reels-shorts-tiktok.md` |
| "ad", "advert", "promo", "commercial", "UGC", "convert", "CTA", "perf/brand" | Ad video | `references/ad-video.md` |
| "mini-drama", "vertical drama", "micro-drama", "серия/эпизод", "cliffhanger", "scripted", "romance/revenge/CEO", acted scene | Mini-drama (scripted vertical) | `references/mini-drama.md` |
| "mini-doc", "documentary", "interview", "testimonial story", "brand film", real footage | Mini-doc / storytelling | `references/mini-doc.md` |

**Mini-drama vs mini-doc — don't confuse them.** Mini-drama is *scripted, acted*
vertical serialized fiction (ReelShort/DramaBox style): cliffhangers, emotional
close-ups, melodrama, time compression. Mini-doc is *real footage*: interviews,
B-roll, radio-edit, truth. Different craft. If the client says "драма",
"сериал", "эпизод", "актёры", "cliffhanger" → mini-drama. If "интервью",
"документалка", "реальная история" → mini-doc.

Load the matching reference file **before** planning the cut. Each reference
gives the exact length, aspect ratio, hook window, cut rhythm, caption rules, and
audio balance for that format.

For the concrete Framehood call patterns (parameters, defaults, ordering) that
every format shares, read `references/framehood-recipes.md`.

---

## Step 1 — Universal rules (apply to every format)

These hold regardless of format. They come first because they override
format-specific taste when in conflict.

1. **Mute-first.** 70–85% of social video is watched on mute. If the cut doesn't
   read with sound off, it doesn't work. Every hook, claim, and CTA needs an
   on-screen text/visual equivalent → always plan `video(captions)` unless the
   client says otherwise. Prefer **dynamic captions**: high-contrast, appearing
   word-by-word or phrase-by-phrase, key words emphasized (colour/scale) — not a
   static paragraph. They double as a pacing device.
2. **Front-load.** The most compelling frame goes first. No logo intro, no "hey
   guys", no slow build. In short-form and ads you have ~1.5–3s before the swipe.
3. **One idea per video.** If the parts carry two messages, cut the weaker one or
   split into two deliverables.
4. **Cut to motion, not to the clock.** Transition on an action, a beat, or a
   tonal shift — not at an arbitrary second. Trim hesitation and dead air hard.
   **Hard shot-length ceiling — a single shot must not hang:** short-form/ad
   body = **1.5–3s per shot**, nothing static longer than ~3–4s; mini-doc B-roll
   = change every 3–5s. If a shot has no internal motion and no reason to hold,
   it is too long — cut it shorter or cut away. Draggy, over-long shots are the
   #1 cause of a "slow" cut and kill completion rate. When in doubt, cut sooner.
5. **Kill your darlings.** A beautiful clip that doesn't serve the through-line
   gets cut. Serve the story/message, not the footage.
6. **Correct aspect ratio at export**, never a center-crop of 16:9 into 9:16.
   Keep text/faces inside the center-80% safe zone (platform UI covers edges).
7. **Audio has a hierarchy.** Voice/message on top, everything ducked beneath it.
   Music never fights the voice. (Concrete dB levels in the recipes file.)
8. **Audio never gets truncated — build the video TO the audio, not the reverse.**
   When there's a voiceover, narration, or interview spine, its length is the
   floor. `video(assemble)`'s `vo` must fit *within* the video length — if the VO
   is longer than the clips, its tail is silently cut off. So: **measure the
   spine audio FIRST, then make the clip sequence sum to ≥ that length** (add
   shots, extend, hold, or loop B-roll). For lip-sync, use `sync_mode:"loop"`,
   which never drops speech. Full protocol in `references/framehood-recipes.md`
   → "Length reconciliation". This is a mandatory pre-flight check, not optional.
9. **Vary shot size.** Alternate wide / medium / close-up so the eye never gets
   bored. Two adjacent shots of the same size + framing = a jump cut; break it up
   or cut on action. A cut to a *different* shot size is the cheapest way to keep
   a sequence alive.
10. **Favor emotional close-ups.** Close-ups of faces — tears, surprise, anger,
    a smile — carry more than any wide. The viewer empathizes with emotion they
    can see. In story/drama, when in doubt, push in on the face at the emotional
    beat.
11. **Compress time.** Cut connective/technical action that carries no meaning
    (walking, opening doors, pouring water, sitting down) unless it *is* the
    point. Jump straight to the meaningful beat. Especially ruthless in short
    drama — every second must earn its place.
12. **Sound design carries the cut.** Beyond the music/VO mix, place discrete SFX
    (whooshes, impacts, clicks, breaths, stings) that are slightly exaggerated and
    land exactly on the cut / action / beat. A hit on the transition makes an edit
    feel intentional and punchy. Sync SFX to picture, never floating.
13. **Grade for mood.** Aim for a cinematic look with a consistent colour palette
    across all parts — e.g. warm skin against cool shadows — chosen to set the
    mood (suspense, romance, drama). Inconsistent grades across clips read as
    amateur. How to achieve this in Framehood: see recipes → "Colour grading".

---

## Step 2 — Plan the cut (before any tool call)

Write a shot list in your head or to the user. For each segment decide:

- **What it does** (hook / body / proof / CTA / beat) — role, not just content.
- **How long** it runs (formats give target durations).
- **What audio sits under it** (VO line, music section, nat sound, SFX hit).
- **What text overlay** it carries (caption spine, hook text, CTA text).
- **How it enters and exits** (hard cut / J-cut / L-cut / crossfade / match cut).

The reference file for your format gives the arc to fill (e.g. ad =
Hook→Problem→Solution→Proof→CTA; mini-doc = radio-edit first, then B-roll over it).

## Step 3 — Assemble

Follow `references/framehood-recipes.md`. General order of operations:

0. **Length pre-flight (do this before assembling).** If the piece has a VO /
   narration / interview spine, get its duration first (note the length of the
   `audio(speak)` output, or estimate ~2.5–3 words/sec from the script). Then
   confirm the planned clip sequence sums to **≥ spine length + a short tail**.
   If it's shorter, extend it now — add shots, lengthen `image(animate)` clips,
   loop/hold B-roll — so nothing gets truncated at assembly. Likewise check no
   single shot violates the shot-length ceiling (rule 4).
1. **Prep the spine.** If the piece is voice-led (ad VO, doc interview), build or
   place the audio spine first (`audio(speak)` for VO, or the client's audio).
   In a doc, get the **radio edit** — a cut that makes sense on audio alone —
   before touching visuals.
2. **Trim parts** to their planned length (`audio(trim)` / prepare clip lengths).
3. **Assemble visuals + audio** with `video(assemble)` — this is the workhorse:
   it sequences clips, lays music/VO/SFX beds at the right levels, applies
   intro/ending treatment and transitions in one pass.
4. **Lip-sync** any talking-character clip to its VO with `video(lipsync)` BEFORE
   assembling that clip in (use `sync_mode: loop` so speech is never dropped).
5. **Caption** the assembled cut with `video(captions)`.
6. **Overlay extra audio** only if needed post-assembly with `video(mix_audio)`.

## Step 4 — QA before delivery

Run `qa` on the output. At minimum:

- `qa(action: "transcript")` if there's spoken/caption content — verify words are
  right (names, numbers, claims, CTA).
- `qa(action: "scene")` against your cut plan — did it assemble as intended.
- `qa(action: "full")` for anything the client will publish or pay for — poll
  `get_status` until `done: true`, then read the `verdict`.

If QA fails on pacing/hook/audio, fix that specific segment and re-assemble —
don't rebuild from scratch.

## Step 5 — Deliver + variant offer

Deliver the file. For **ads specifically**, proactively offer 2–3 hook variants
off the same body (swap only the first 3s / the hook caption) — that's how perf
creative is actually tested. Cheap to produce, and it's the single highest-impact
lever. See `references/ad-video.md` for the variant protocol.

---

## Quick reference: format cheat-sheet

| | Reel/Short/TikTok | Ad video | Mini-drama | Mini-doc |
|---|---|---|---|---|
| Aspect | 9:16 | 9:16 / 1:1 / 16:9 | 9:16 | 16:9 or 9:16 |
| Sweet-spot length | 15–34s | 15–30s (up to 60s) | 60–90s / episode | 60s–5min |
| Hook window | 1.5s | 1–3s | in medias res, 0–10s | first 15s |
| Shot length | 1.5–3s, on beat | 1.5–3s body | 1.5–3s (CU may hold) | B-roll 3–5s |
| Cut rhythm | fast, on beat | fast body, tight | dense, shot/reverse | breathe; J/L cuts |
| Captions | mandatory | mandatory | mandatory (dynamic) | mandatory |
| Audio | sound + VO | VO over bed | dialogue + score + SFX | A-roll + music under |
| Ending | loop / payoff | CTA + end card | cliffhanger | denouement |

Details, edge cases, and the reasoning behind each row live in the reference
files. Read the one for your format.
