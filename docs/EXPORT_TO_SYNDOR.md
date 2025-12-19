# Export to Syndor

**Intended destination:** `Syndor/altius/nate-avatar/`

## What to copy
- Copy the entire repository contents to the destination path.
- Preserve folder structure (including `architecture/`, `persona/`, `agents/`, `modules/`, `web/`, and all root files).

## Path assumptions
- Files are referenced using relative paths; no root-relative web paths are required after import.
- Static assets in `web/` and the root `index.html` load locally without requiring a `/`-prefixed base path.
- Backend sketches (if enabled) should compute file paths relative to their module location rather than absolute filesystem roots.

## Configuration expectations
- This repo ships with example scaffolding only. If you add runtime configuration, keep real credentials outside of version control.
- Expected local-only files (do **not** check in):
  - `config.json`
  - `.env` or `.env.*`
  - API tokens or secrets
  - Embedding indexes or vector store outputs
  - Logs and trace dumps
  - Local SQLite/DB files

## Import steps
1. Copy all files into `Syndor/altius/nate-avatar/`.
2. Ensure any local-only config files are kept out of the repo and placed alongside the deployment environment as needed.
3. If you are serving the static UI, open `index.html` or `web/index.html` in a browser or serve via a static file server.
4. If you wire up the optional backend sketch, verify your endpoint path matches the relative fetch path (e.g., `./api/altius`).

## Quick verification
- Open `index.html` locally and confirm the mock response renders and the interface loads without missing assets.
- Run any existing scripts or checks you maintain locally to confirm nothing references absolute paths.

## Fragile files — "Do not edit unless you know why"
- `identity-schema.json`
- Prompts under `PROMPTS/`
- Persona and safeguards materials (`persona/`, `safeguards/`)
- Any agent behavior definitions under `agents/`

Changes to the above can alter behavior; review carefully before modifying.
