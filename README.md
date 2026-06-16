# Framehood plugin for Claude Code

Generate and edit images, video, and audio directly from Claude. The plugin
wires Claude Code to the Framehood MCP server and adds a command and skills.

## What's inside

- **MCP server** (`framehood`) — the remote endpoint `https://mcp.framehood.ai/mcp`.
  On first use Claude Code runs the OAuth sign-in flow in your browser.
- **`/framehood`** — a command for one-line generation requests.
- **`framehood` skill** — teaches Claude the image/video/audio tools and the
  job→poll workflow so it uses them well.
- **`writing-claude-plugins` skill** — a guide for authoring your own plugins.

## Install

```
/plugin marketplace add Framehood/framehood-plugin
/plugin install framehood@framehood
```

Then connect/authenticate the MCP server when prompted (or run `/mcp`). You'll
need a Framehood account — sign up at https://framehood.ai.

## Use

```
/framehood a cinematic portrait of a lighthouse keeper as keeper.jpg
```

Or just ask Claude naturally ("make me a 5-second clip of waves at sunset") —
the `framehood` skill guides it to the right tool.

## Links

- Docs: https://docs.framehood.ai
- Site: https://framehood.ai

## License

Framehood is a proprietary, source-available product. See [LICENSE](LICENSE).
