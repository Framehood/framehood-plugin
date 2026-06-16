---
description: Generate or edit an image, video, or audio clip with Framehood
argument-hint: [what to create, e.g. "a red fox in the snow as fox.jpg"]
---

Use the Framehood MCP tools (server `framehood`) to fulfill this request:

> $ARGUMENTS

Guidance:

- Pick the right tool by output type: `image` (create/edit/upscale/animate),
  `video` (edit/swap/lipsync/captions/scene/reframe/…), `audio`
  (speak/sfx/music/mix/concat).
- Every domain tool needs an `out` filename. Infer a sensible one from the
  request if the user didn't give one.
- If you're unsure how the tools fit together, read the `zvs://overview`
  resource first.
- Tools may return a queued job (`job_id`, `status: queued`). Poll it with
  `get_status(job_id=…)` until `status` is `succeeded`, then report the output
  URL from `outputs`. On `failed`, read the `error` and retry with corrected
  arguments.
- If a call returns an insufficient-credits error, tell the user their balance
  and how to top up (the error includes guidance); do not retry blindly.

Report the final result URL(s) plainly when the job completes.
