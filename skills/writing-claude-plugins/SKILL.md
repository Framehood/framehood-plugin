---
name: writing-claude-plugins
description: Use when authoring or packaging a Claude Code plugin — scaffolding the directory, writing .claude-plugin/plugin.json and marketplace.json, adding commands/skills/agents/hooks, bundling MCP servers (local stdio or remote HTTP), and publishing so users can install via /plugin marketplace add.
---

# Writing a Claude Code plugin

A plugin is a self-contained directory that adds skills, commands, agents,
hooks, and MCP servers to Claude Code. This skill is a build checklist.

## Directory layout

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # manifest (REQUIRED — only this file lives here)
├── commands/                # slash commands (*.md)
│   └── do-thing.md
├── skills/                  # skills (each a dir with SKILL.md)
│   └── my-skill/SKILL.md
├── agents/                  # subagents (*.md, optional)
├── hooks/hooks.json         # hooks (optional)
├── .mcp.json                # bundled MCP servers (optional)
└── README.md
```

Everything except `plugin.json` lives at the plugin **root**, not inside
`.claude-plugin/`.

## plugin.json

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "One line on what it does.",
  "author": { "name": "You", "url": "https://example.com" },
  "homepage": "https://docs.example.com",
  "keywords": ["tag"]
}
```

Only `name` (kebab-case) is required. Component folders (`commands/`, `skills/`,
`agents/`) are auto-discovered; override their locations with the `commands`,
`skills`, `agents`, `hooks`, `mcpServers` fields (each a path or array of paths
relative to the plugin root, starting `./`). Setting a field **replaces** the
default folder, so list it explicitly to keep both: `"commands": ["./commands/", "./extras/"]`.

## Commands

A markdown file in `commands/` with optional frontmatter:

```markdown
---
description: What it does and when to use it
argument-hint: [issue-number]
---

Fix issue $ARGUMENTS. Steps: …
```

`$ARGUMENTS` is the full argument string; `$1`, `$2` are positional.

## Skills

A directory `skills/<name>/SKILL.md`:

```markdown
---
name: my-skill
description: Use when … (this is how Claude decides to invoke it — be specific about triggers)
---

Instructions and reference material.
```

`description` is the most important field — Claude matches it against the task.
Lead with "Use when …" and name concrete triggers. May include supporting files
beside `SKILL.md`.

## MCP servers

Put servers in `.mcp.json` at the plugin root (or inline under `mcpServers` in
plugin.json). Use the standard MCP server config.

Local (stdio) — runs under the plugin dir; use `${CLAUDE_PLUGIN_ROOT}`:

```json
{ "mcpServers": { "db": { "command": "${CLAUDE_PLUGIN_ROOT}/servers/db", "args": [] } } }
```

Remote (HTTP) — Claude Code connects and runs the OAuth flow on first use:

```json
{ "mcpServers": { "svc": { "type": "http", "url": "https://mcp.example.com/mcp" } } }
```

## Publishing (marketplace)

Add `.claude-plugin/marketplace.json` at the **repo root**:

```json
{
  "name": "my-marketplace",
  "owner": { "name": "You" },
  "plugins": [ { "name": "my-plugin", "source": "./my-plugin" } ]
}
```

`source` is a path relative to the repo root (or a `{ "source": "github", "repo": "owner/repo" }`
object for plugins in another repo).

Users install with:

```
/plugin marketplace add owner/repo
/plugin install my-plugin@my-marketplace
```

## Validate

- `claude plugin validate .` checks the manifest and structure.
- `/doctor` flags ignored default folders and config problems.
- Reload after edits with `/reload-plugins`.
