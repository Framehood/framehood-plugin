---
name: framehood
description: Use when creating or editing images, video, or audio with Framehood — covers reading the overview first, the image/video/audio/qa/files tools, uploading a LOCAL file (data: URI or the create_upload + upload.py flow), the job→poll workflow, choosing a model (defaults + explicit model/params), prompt improvement, and credits. Trigger on requests to generate, edit, upscale, animate, lipsync, swap, caption, voice, compose, or upload media via the `framehood` MCP server.
allowed-tools: Bash(python3 *skills/framehood/scripts/upload.py *)
---

# Framehood

Framehood exposes a small set of **functional** MCP tools. You think in outcomes
(an image, a clip, a voiceover); each tool routes to the right model.

## Start here — read the overview

**Before your first Framehood action in a session, read the `zvs://overview` MCP
resource.** It is the canonical, always-current tool guide: it reflects exactly
which tools, actions, and models are available on *this* account (some
capabilities are gated by plan, so this skill's lists are a guide, not a
guarantee). Re-read it whenever a request doesn't map cleanly to a tool. Treat
the overview — not this skill — as the source of truth.

The overview also prints the live **server version**. If it advertises a tool or
action this skill doesn't mention, use it (the overview wins) and let the user
know Framehood has new capabilities; if the server looks older than what this
skill describes, suggest they reconnect the Framehood connector (for server
changes) or run `/plugin marketplace update framehood` (for plugin/skill changes).

## Tools

| Tool | Actions | Output |
|------|---------|--------|
| `image` | `create` (text→image), `edit`, `upscale`, `animate` (image→video) | image (video for animate) |
| `video` | `edit`, `edit_ref`, `swap`, `lipsync`, `captions`, `upscale`, `assemble`, `mix_audio` | video |
| `audio` | `speak` (text→voice), `sfx`, `music`, `mix`, `trim`, `concat` | audio |
| `qa` | quality-check a generated asset | pass/fail report |
| `files` | list / manage your stored outputs | file list |
| `models` | `list` (browse models), `guide` (one model's params) | model catalog |
| `billing` | `balance`, `plan`, `plans`, `subscribe`, `manage`, `request_upgrade` | billing info / links |
| `get_status` | poll a job by `job_id` | job record |

Every domain tool requires an `out` filename (e.g. `out: "portrait.jpg"`). Some
accounts also expose an `actor` tool (reusable characters) and extra actions —
the overview shows what's actually enabled for you.

## Choosing a model

You usually **don't** name a model — each tool picks a sensible **default** from
your `action` and `tier`:

- `image(create)` → `tier` `draft` < `fine` < `photo` (quality/cost ladder).
- `image(animate)` and video motion → `tier` `standard` | `pro`.
- Every other action maps to one good default model.

To use a **specific** model instead:

1. **Browse** — `models(action="list")` returns every available model grouped by
   tool, with the default action/tier that reaches it, its category, description,
   and credit cost. Pass `tool: "image"` (etc.) to narrow.
2. **Learn its parameters** — `models(action="guide", model="<id>")` returns that
   model's specific parameters and prompt guide.
3. **Call it explicitly** — pass `model: "<id>"` plus any model-specific
   `params: { … }` to the domain tool. The explicit model overrides the
   tier default. For example:
   `image(action="create", model="flux_pro", params={ … }, out="hero.jpg")`.

Explicit models go through the same checks as defaults: they're billed in
credits and blocked if a model isn't available on your plan. Don't pass both
`model` and `actor_id` — pick one.

## Improve the prompt first

Before you submit any **generation** (image/video/audio create·edit·speak·sfx·
music), tune the request to the model you'll use — models prompt differently:

1. **Consult the model's guide** — `models(action="guide", model="<id>")`, or
   `GET /v1/models/{kind}/prompt-guide`. It gives the preferred structure, ideal
   length, phrasing, and what to avoid.
2. **Rewrite** the request to follow it.
3. **Offer, don't impose.** Show your improved prompt and one line on what you
   changed ("tightened this for FLUX — use it, or your original?"), then generate
   with whichever the user picks.

Skip this only for trivial/explicit prompts, or when the user says "use exactly
this".

## The workflow

1. **Call the tool.** Fast actions return the finished result inline. Slower ones
   return a queued job: `{ "job_id": "job_…", "status": "queued" }`.
2. **Poll** queued jobs with `get_status(job_id=…)` every few seconds until
   `status` is `succeeded` (the result URL is in `outputs`: `image_url` /
   `video_url` / `audio_url`) or `failed` (read `error`). Give up after ~20 polls
   and report the `job_id` so the user can check later.
3. **Report the output URL** to the user.

## Conventions

- On an error, read the `hints` / `error` field and retry with corrected
  arguments rather than repeating the same call.
- `tier` trades quality for cost/speed; an explicit `model` gives exact control.
- To keep a character consistent across generations, use an **actor** (if enabled
  on your plan): pass its `actor_id` (`act_…`) to `image(create/animate)`.
- **Credits:** every job costs credits. On an insufficient-credits error, surface
  the balance and upgrade guidance from the error — never loop retrying. Org
  members without payment access can call `billing(request_upgrade)` to email
  their owner.

## Using a local file (from the user's computer)

Any `*_url` input (image_url, video_url, audio_url) needs a hosted URL — a local
path won't work. Two ways to get one:

**Small file (≤ 25 MB) — inline `data:` URI.** Read the file and pass it as a
data URI directly to the media input; the server uploads it and uses the hosted
URL automatically:
`image(action="edit", image_url="data:image/png;base64,<...>", prompt, out)`.
Also works via `files(upload, data="data:...")`.

**Large / original-quality file — `create_upload` + the bundled `upload.py`.**
The bytes go straight to storage over HTTP (not through the chat), so quality is
preserved and there's no message-size limit (server cap applies):

1. Call `files(action="create_upload", filename, content_type)` → you get
   `{ upload_url, token, url }`.
2. Run the bundled helper (it PUTs the file and prints the hosted URL):
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/upload.py <local_file> --url <upload_url> --token <token>
   ```
3. Use the printed URL as the `image_url` / `video_url` / `audio_url`.

The token is short-lived and scoped to your own storage; `upload.py` only ever
sends the file to a `framehood.ai` host.

## Examples

- "make a hero image" → `image(create, prompt, out, tier)`
- "edit this photo on my disk" → `files(create_upload, filename, content_type)` → `python3 ${CLAUDE_SKILL_DIR}/scripts/upload.py <file> --url <upload_url> --token <token>` → `image(edit, image_url=<printed url>, prompt, out)`
- "use FLUX pro specifically" → `models(list)` → `image(create, model="flux_pro", params, out)`
- "which models can I use?" → `models(list)`
- "upscale this" → `image(upscale, image_url, out)`
- "turn this photo into a clip" → `image(animate, image_url, out, duration)`
- "voice this script" → `audio(speak, text, out, voice)`
- "add captions" → `video(captions, video_url, out)`
- "lip-sync to this VO" → `video(lipsync, video_url, audio_url, out)`
