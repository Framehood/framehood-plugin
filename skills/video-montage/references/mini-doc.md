# Mini-doc / storytelling

A different craft from short-form and ads. Here the story is found in the edit,
not front-loaded. You have hours of raw parts (interview A-roll, B-roll, nat
sound) and you sculpt them into something that feels inevitable. Pacing lets the
story breathe. Length runs 60s to several minutes.

## The golden rule: radio edit first

Build the story on **audio alone** before touching a single visual.

1. Lay the interview/VO sync into the timeline with video tracks OFF.
2. Cut it down — sentence, then word, then syllable — until the audio is tight
   and makes sense as a standalone thing you could air on radio / as a podcast.
3. Only when the **story arc** works on audio do you paint visuals over it.

If you can hold attention with audio alone, the visual layer becomes easy. If you
can't, no amount of pretty B-roll saves it.

## Structure — three-act arc

Beginning → Middle → End, with rising tension to a crescendo, then a fast
denouement. Even a 90s piece needs the arc:

- **Beginning:** establish where we are / the problem / the stakes.
- **Middle:** the process, the turn, the tension climbing. Each scene ends with
  the viewer asking "what happens next?" — that question is what keeps them.
- **End:** the outcome / the change / the takeaway. The subject returns changed.

Every scene must have a purpose: advancing the arc. Ask of each one, "what does
this scene do?" If the answer is "it's a nice shot" — cut it.

## Workflow (assembly → rough → fine)

1. **Paper edit** — plan scene order, interview bites, B-roll on paper first, so
   you're not aimlessly shuffling clips.
2. **Assembly edit** — get all the good bits into one timeline fast. Don't
   finesse; you'll restructure. This is where you see the shape.
3. **Rough cut** — the hard part: assembly → coherent story. Most of the work
   lives here. Add temp music, SFX, transitions.
4. **Fine cut** — pacing, colour, sound mix, titles, graphics.

Biggest mistakes: finessing too early, falling in love with footage, skipping the
organise/log step.

## B-roll — structure, not wallpaper

B-roll exists to *structure the story*, not to "cover cuts". Two axes:

- **Horizontal (shot-flow):** chain B-roll to show progression of action over
  time — walking in, packing, warming up. Micro-stories, shot by shot.
- **Vertical (emotional alignment):** match the image to the *meaning* of the
  word under it. When the subject says "those seconds are the most terrifying",
  don't cut to generic warm-up wallpaper — cut to an image that embodies
  "terrifying". Make the viewer *feel* the word.

Place B-roll at precise moments in the dialogue arc to amplify subtext. Use it to
draw parallels, foreshadow a later reveal, or replace a weak talking-head stretch
entirely (showing > telling).

## Cuts and transitions

- **Cut on action** — cut as the subject moves (looks off-camera, shifts in seat)
  for a seamless, invisible transition.
- **J-cut** — next scene's *audio* starts before its visuals. Great going into
  B-roll: start the next clip's sound, then bring its picture.
- **L-cut** — current audio carries over into the next scene's visuals. Lets the
  story breathe across a transition.
- **Fill jump cuts with B-roll or a close-up.** Cutting filler ("umm", "ahh")
  mid-sentence creates jump cuts — cover them. A close-up also transitions
  cleanly between two similarly-framed interview shots.
- Gentle fades / cross-dissolves bridge tonal gaps; keep grade + audio consistent
  across footage for a unified feel.

## Audio

- Interview A-roll is the spine, always intelligible on top.
- Music sits **under** the voice, supporting emotion, never fighting it.
- Nat sound / SFX add texture and realism between sync.
- Captions on interview content — accessibility + mute viewing.

## Ethics (documentary-specific)

You have enormous power to reshape someone's words. Don't misrepresent through
selective cutting. The edit should be true to what the subject meant.

## Framehood assembly sketch

1. Place interview audio; tighten to the **radio edit** (`audio(trim)` /
   `audio(concat)` to sequence sync bites).
2. Generate/lay music bed with `audio(music)` (instrumental, under voice).
3. `video(assemble)` — interview clips + B-roll in planned order, `music` under
   at low level (`keep_clip_audio: true` so interview audio stays on top),
   `xfade_duration` a touch longer than social (0.5–1.0 for cinematic feel),
   `intro.fade_in: true`, `ending.type:"cinematic"`.
4. For talking-head over VO, `video(lipsync)` the clip first (`sync_mode:"loop"`).
5. `video(captions)` on interview sections.
6. `qa(action:"transcript")` + `qa(action:"scene")` against the paper edit.

See `framehood-recipes.md` for parameters and levels.
