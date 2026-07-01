# Ad video — performance & brand

An ad has a job: turn attention into a measurable next step. The through-line is
the **Hook → (Problem →) Solution → Proof → CTA** arc. This works for a 15s social
ad and a 60s brand story alike — you compress or expand, but the sequence holds.

## The arc (this is the spine — build to it)

| Segment | Job | Typical length (perf) |
|---|---|---|
| **Hook** | Stop the scroll, earn the next 3s | 1–3s |
| **Problem** | Create relevance — name a specific, felt pain | 2–5s |
| **Solution** | Position the product as the natural fix | 5–15s |
| **Proof** | Make it believable — demo, before/after, testimonial, number | 3–8s |
| **CTA** | One clear next step, on-screen AND in audio | 2–4s |

Each element must serve a purpose: hold the attention you earned and make the CTA
feel like the natural next step, not a jarring interruption.

## Hard specs

- **Length:** 15–30s has the highest survival rate in ad libraries. Awareness
  6–15s; consideration 30–60s; retargeting/direct-CTA under 30s.
- **Aspect:** 9:16 for Stories/Reels/TikTok; 1:1 for Meta/LinkedIn feed;
  16:9 for YouTube in-stream / CTV. Reformat per placement — don't ship one
  ratio everywhere.
- **Mute-first:** every Meta/LinkedIn ad must be fully understandable on mute.
  Text overlays are the narrative spine, not decoration.

## The hook (first 1–3s)

If the hook blends in, the ad is dead — the algorithm kills it and so does the
buyer. 65% drop off within 3s if not hooked. Match the hook to the niche, don't
follow a universal "best practice":

- **Pain-point opener** — mandatory for fitness; "Tired of [specific, under-
  articulated pain]?" (fails if the pain is so broad the viewer shrugs).
- **Bold claim / social proof** — outperform on Meta (skeptical audience).
- **Visual interrupt** — mandatory for home goods; a zoom, colour flash, motion.
- **Authority claim** — mandatory for supplements.
- **Relatable problem (UGC)** — open on the failure state in a slightly tired
  tone, not performative excitement. Specificity wins: "I spent six months doing
  this wrong" beats "This product is amazing." Avoid opening with your name,
  credentials, or the product itself.

Put urgency in the **CTA**, not the hook. "Limited time offer—" as the first
words is a scroll trigger now.

## UGC vs polished

UGC-style (authentic, low-production feel) is the default high-performer in most
feed environments — lower thumb-stop resistance, higher perceived authenticity,
cheap to produce at scale. Polished/brand still wins in some verticals (fashion
leans static; beauty is ~50/50). Decide by placement and niche, not by reflex.

## Text overlays

- The single most controllable performance lever. Treat them as the narrative
  spine because most viewers never turn sound on.
- Sequence the overlay to the arc: Problem → Agitation → Solution → Proof → CTA,
  one beat per frame.
- Hook text angle changes move performance 30–50%; design tweaks (font/colour)
  only 5–15%. So test the *message*, not the *font*.

## CTA

- One action. On-screen and in audio ("Try it free", "Shop now", "Learn more").
- Match to intent: retargeting/bottom-funnel → direct ("Shop now"); awareness →
  lower-friction ("Learn more"). Beauty/education-heavy → "Learn more" outperforms
  "Shop now".
- End card: brand cue + CTA, clean. Feels like the story's conclusion.

## The variant protocol (do this — it's the highest-leverage step)

Perf creative is *modular*. Don't think "edit a new video" — think "new
combination of proven hook + body + CTA". Concretely:

1. Lock a body that works (Problem→Solution→Proof).
2. Produce **3–5 hook variants** off that same body — swap only the first 3s
   and the hook overlay. Keep everything else identical.
3. Isolate one variable at a time. Changing hook + body + CTA + ratio at once
   teaches you nothing.
4. Naming convention: `[BaseID]_[HookAngle]_[CTAType]`, e.g.
   `V012_SocialProof_TimeToValue`.

Creative fatigues in ~2–3 weeks — a variant pipeline is a necessity, not a nicety.

## Framehood assembly sketch

1. Build VO with `audio(speak)` (tight, energetic; re-pace if the read is slow).
2. Order body clips to the arc; `video(assemble)` with the VO as `vo`, a music
   bed under it (`music` at a low `music_level`), `ending.type:"social"` for a
   fast fade + end hit, and an `end_sfx` on the CTA.
3. `video(captions)` — but for ads, also plan explicit hook/CTA **text overlays**
   as part of the plan, not just auto-captions.
4. For variants: re-run `assemble` swapping only the opening clip + hook line.
5. `qa(action:"transcript")` on the CTA wording; `qa(action:"full")` before ship.

See `framehood-recipes.md` for parameters and levels.
