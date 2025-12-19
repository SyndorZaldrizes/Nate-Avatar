# Starter Pack Contents

Use this list to assemble a public-friendly starter zip.

## Safe to include
- Documentation (`README.md`, `docs/` contents)
- Structural references (`architecture/`, `theory/`, `research/`)
- Non-sensitive persona and prompt scaffolding (`PROMPTS/`, `persona/`, `agents/` without private keys)
- Static web assets (`index.html`, `web/`)
- Changelogs and notices (`CHANGELOG.md`, `NOTICE.md`)

## Must exclude
- Any `.env` or environment-specific files
- `config.json` containing real endpoints or secrets
- Token files, API keys, or credential stores
- Embedding/vector indexes and cache outputs
- Logs, traces, or analytics dumps
- Local database files (e.g., `*.sqlite`, `*.db`)
- Virtual environments or dependency caches (`venv/`, `.venv/`, `node_modules/` if created)
