# Mini-drama / micro-drama (scripted vertical)

Serialized scripted vertical fiction — ReelShort / DramaBox / ShortMax style
("duanju"). NOT documentary: this is acted, plotted, melodramatic. The
cliffhanger is the product. Editing serves density, emotion, and momentum.

If the client sent real interview/B-roll footage instead of acted scenes, you're
in the wrong reference — use `mini-doc.md`.

## Hard specs

- **Aspect:** 9:16 vertical. Framing is tight — close-ups and eye-level shots
  dominate; the narrow frame centers faces and emotion. Wide shots are rare;
  split screens, tight compositions and text overlays replace them.
- **Episode length:** 60–90s typical (up to ~3min). One episode = one escalation
  + one cliffhanger.
- **Subtitles:** always on, dynamic. Audiences watch fast and often muted.

## Episode structure (the beat spine)

| Beat | Length | Job |
|---|---|---|
| **Cold open / hook** | 0–10s | Start *in medias res* — mid-conflict, not build-up. Re-hook fast if continuing a cliffhanger from the previous episode. |
| **Setup** | 10–15s | Establish the immediate conflict/stakes of THIS episode. |
| **Development** | ~1–2min | Escalate through rapid, high-impact beats. Dense — frequent narrative turns, lean dialogue, minimal exposition. |
| **Cliffhanger** | final 10–15s | Cut off at peak tension — a reveal, a slap, a return, a betrayal. Leave the viewer needing the next episode. |

Open in the middle of conflict. Every episode has its own beginning-middle-end
*and* a cliffhanger. Momentum never sags — if a beat doesn't escalate, cut it.

## Editing rules specific to drama

- **Emotional close-ups are the currency.** Push in on the face at every emotional
  beat — tears, shock, rage, the slow smile. This is where the viewer bonds.
- **Compress time hard.** Cut every non-meaningful action — walking in, sitting,
  pouring, door-opening — unless it carries tension. Jump to the charged moment.
- **Shot/reverse-shot for confrontation.** Dialogue duels cut tight between two
  close-ups; let reactions land. The reaction shot often matters more than the line.
- **Vary shot size beat to beat** (medium to establish → CU for emotion → insert
  for a key object). Never two same-size shots back to back.
- **Reveal on the cut.** Time the edit so the reveal/twist lands on a hard cut,
  reinforced by a sound sting.
- **Dramatic irony where possible** — show the viewer what the protagonist can't
  see (the gaslighter's face, the hidden text). The gap drives hate-watch
  engagement and comments.

## Sound design (drama leans on it hard)

- Exaggerated, on-beat SFX: slaps, gasps, heartbeat, door slam, whoosh into a
  reveal, tension riser under the cliffhanger.
- Music swells to the emotional peak and cuts (or stings) on the cliffhanger.
- Voice/dialogue always intelligible on top; score under it (levels in recipes).

## Colour grade

- Consistent cinematic palette across the episode to set genre mood: warm romance,
  cold desaturated thriller, high-contrast for confrontation. Warm skin vs cool
  shadow is the default "expensive" look. Grade all clips to match — mismatched
  grades read as cheap.

## Serialized continuity (if cutting a series, not a one-off)

- **Recap/re-hook** the prior cliffhanger in the first ~10s, then deliver a NEW
  hook in the final ~5s. That resolve-then-re-hook rhythm is what sustains binge.
- Keep character look/grade/audio consistent episode to episode.

## Framehood assembly sketch

1. Dialogue clips → `video(lipsync)` each acted line to its audio
   (`sync_mode:"loop"` so no line is cut).
2. **Length pre-flight** (recipes → "Length reconciliation"): make the picture
   cover the full dialogue/VO; never truncate a line.
3. Order beats: cold-open → setup → development → cliffhanger. Keep shots
   1.5–3s except where a held CU earns the emotion.
4. `video(assemble)`: `format:"9:16"`, `tier:"pro"`, dialogue as `keep_clip_audio`,
   score via `music` under it (`music_level` -22 to -24), tension SFX via
   `sfx_ambient`/added tracks, `ending.type:"social"` with an `end_sfx` sting on
   the cliffhanger, `xfade_duration` 0.1–0.3 (hard, punchy — not dreamy).
5. Colour grade pass (recipes → "Colour grading").
6. `video(captions)` — dynamic, keyword-emphasized.
7. `qa(action:"transcript")` (lines intact, not truncated) + `qa(action:"scene")`
   against the beat spine; `qa(action:"full")` before delivery.

See `framehood-recipes.md` for exact parameters, levels, grading and SFX how-to.
