---
name: framehood
description: Use when creating or editing images, video, or audio with Framehood — covers the image/video/audio/qa/files/actor tools, the job→poll workflow, actors, and credits. Trigger on requests to generate, edit, upscale, animate, lipsync, swap, caption, voice, or compose media via the `framehood` MCP server.
---

# Framehood

Framehood exposes a small set of **functional** MCP tools. You think in terms of
what you want (an image, a video, a voiceover); the server picks the model.

## Tools

| Tool | Actions | Output |
|------|---------|--------|
| `image` | `create` (text→image), `edit`, `upscale`, `animate` (image→video), `actor_sheet` | image (or video for animate) |
| `video` | `edit`, `edit_ref`, `swap`, `lipsync`, `captions`, `upscale`, `assemble`, `mix_audio`, `scene`, `reframe` | video |
| `audio` | `speak` (text→voice), `sfx`, `music`, `mix`, `concat` | audio |
| `qa` | quality check a generated asset | report |
| `files` | list / manage your stored outputs | file list |
| `actor` | create and manage reusable actors (LoRAs) | actor record |
| `billing` | `balance`, `plan`, `plans`, `subscribe`, `manage`, `request_upgrade` | billing info / links |
| `get_status` | poll a job by `job_id` | job record |

Every domain tool requires an `out` filename (e.g. `out: "portrait.jpg"`).

## The workflow

1. **Read `zvs://overview`** (an MCP resource) the first time you use Framehood
   in a session, or whenever a request doesn't map cleanly to a tool. It is the
   canonical tool guide.
2. **Call the tool.** Fast actions return the finished result inline. Slower
   ones return a queued job: `{ "job_id": "job_…", "status": "queued" }`.
3. **Poll** queued jobs with `get_status(job_id=…)` every few seconds until
   `status` is `succeeded` (then the result URL is in `outputs`:
   `image_url` / `video_url` / `audio_url`) or `failed` (read `error`). Give up
   after ~20 polls and report the `job_id` so the user can check it later.
4. **Report the output URL** to the user.

## Conventions

- On an error, read the `hints` / `error` field and retry with corrected
  arguments rather than repeating the same call.
- `tier` trades quality for cost/speed (image: `draft` < `fine` < `photo`).
- To keep a character consistent across generations, create an **actor** and
  pass its `actor_id` (`act_…`) to `image(create/animate)`. Training custom
  actors is a paid feature; the free tier can use built-in actors.
- **Credits:** every job costs credits. If a call fails with insufficient
  credits, surface the balance and the upgrade guidance from the error — never
  loop retrying. Organization members without payment access can call
  `billing(request_upgrade)` to email their owner.

## Examples

- "make a hero image" → `image(create, prompt, out, tier)`
- "upscale this" → `image(upscale, image_url, out)`
- "turn this photo into a clip" → `image(animate, image_url, out, duration)`
- "voice this script" → `audio(speak, text, out, voice)`
- "add captions" → `video(captions, video_url, out)`
- "lip-sync to this VO" → `video(lipsync, video_url, audio_url, out)`
