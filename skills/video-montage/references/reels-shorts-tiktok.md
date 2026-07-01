# Reels / Shorts / TikTok — short-form vertical

The default format when a client says "make a video / ролик" for social. Optimized
for **completion rate** — that is the dominant algorithmic signal. A video watched
to the end (and especially rewatched) gets exponentially more distribution.

## Hard specs

- **Aspect:** 9:16 vertical. Export at that ratio; never center-crop a 16:9.
- **Length:** algorithmic sweet spot **15–34s**. When in doubt, go shorter.
  Max is minutes, but longer ≠ better here.
- **Safe zone:** keep faces + text in the center 80%. Platform UI (captions,
  buttons, username) eats the bottom ~15% and right edge.
- **Frame 1 works on mute.** The very first frame must telegraph what this is
  with sound off.

## The hook (first 1.5s)

You have ~1.5s before the swipe reflex fires. The first 3 seconds drive ~80% of
completion variance. Hook types that work:

- **Pattern interrupt** — unexpected visual/motion/text that breaks the scroll.
- **Curiosity gap** — an incomplete statement demanding resolution.
- **Direct address** — speak to the viewer's exact situation.
- **Visual contrast** — a striking image distinct from typical feed content.

What kills it: slow intros, logo animations, "Hey everyone, welcome back."
By the time the greeting ends, the viewer is gone. **Cut the intro. Open on the
action or the payoff.**

## Cut rhythm

- **Shot-length ceiling: 1.5–3s per shot.** Nothing static hangs past ~3–4s.
  A 30s reel is roughly **8–15 shots**, not 4 long ones. Over-long shots read as
  "slow" and tank completion — this is the single most common montage mistake.
- Fast pacing, faster than long-form — but *fast cuts, not rushed edits*.
- Cut on the beat of the trending sound where one is used.
- Trim every pause, filler, and dead frame. Keep natural rhythm, not machine-gun.
- One idea, one video. Don't dilute.

## Captions

Mandatory. 85% watch on mute. Rules:
- Clean, readable, high-contrast. Big enough to read on a phone.
- Captions **enhance, don't echo** — don't just transcribe if the audio is
  redundant; add value or emphasis.
- Keep them inside the safe zone so platform UI doesn't cover them.

## Audio

- Trending sound drives discoverability (especially TikTok/Reels) — but the
  **visual** hook is what stops the scroll.
- If there's VO, it sits on top; music ducks beneath it.
- Original audio over reposts on Reels (watermarks from other platforms hurt
  distribution — never leave a TikTok watermark on a Reel).

## Ending

- **Loop** (hard cut back to a frame that matches the open) for replay-driven
  content — replays are a top ranking signal.
- Or a clean **payoff** that rewards watching to the end.
- No long outro. No "like and subscribe" tail that tanks completion.

## Platform nuance (don't serve one cut three ways — platforms penalize it)

- **TikTok** — rewards raw completion + personality; fastest pattern-interrupt
  needed; trend-driven, casual.
- **Reels** — rewards polish + original content; strong visual hook + trending
  audio; lifestyle/brand aesthetic.
- **Shorts** — punchy; searchable/evergreen; feeds long-form channel growth;
  strong first-frame + replay rate matter.

Same source parts, but re-lead with a different first 3s / caption per platform
rather than exporting one identical file everywhere.

## Framehood assembly sketch

1. Order clips hook→body→payoff; trim each to its beat.
2. `video(assemble)` with `format: "9:16"`, music bed under any VO, and an
   `ending.type: "loop"` for loop-back content (or `"social"` for a fast fade).
3. `video(captions)` on the result.
4. `qa(action:"transcript")` to verify caption text, then `qa(action:"scene")`.

See `framehood-recipes.md` for exact parameters and dB levels.
