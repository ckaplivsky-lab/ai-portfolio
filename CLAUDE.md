# AI Automation Portfolio

Chelsea's portfolio of AI automation projects, built for job applications. Each `portfolio-N-*` folder is a standalone, self-contained project with its own README — treat them independently, not as parts of one app.

## Stack

- **Make.com** — automation/orchestration (forms, sheets, triggers, email, etc.)
- **Claude API** (Anthropic) — the AI logic inside each automation, via the `anthropic` Python library for local scripts
- **Python** — standalone scripts for practice and lightweight tooling (e.g. `listing_generator.py`, `weather_test.py`, `lead_scoring.py`, `company_summary.py`)
- **n8n** — workflow automation, used in earlier course exercises, will expand in later portfolio pieces
- Supporting glue scripts are plain Python where needed

## Structure

- `portfolio-N-<name>/README.md` — problem, solution, tools, how-it-works, results, and "what I'd scale next" for that project
- Root `README.md` and loose scripts (e.g. `listing_generator.py`, `company_summary.py`) are individual demos, not shared infrastructure — don't assume code in one folder is reused by another
- Site is deployed as static content to GitHub Pages via `.github/workflows/static.yml` on push to `main`

## Python Scripts

Standalone scripts living at the repo root are day-by-day sprint exercises, not part of a shared app:
- `weather_test.py` — calls the open-meteo.com weather API, parses temperature/wind speed
- `lead_scoring.py` — filters a list of lead dictionaries by score
- `company_summary.py` — calls the Claude API for a 3-sentence company summary, saves to `company_summaries.csv`; includes typed exception handling, refusal/truncation checks, and CSV formula-injection sanitization

**Dependencies used so far:** `requests`, `anthropic`, `python-dotenv` — install via `pip3 install <package>`

**Preferred model:** `claude-sonnet-5` for new API calls (current-gen, near-Opus quality) unless there's a specific reason to pin an older model.

## Conventions for README-per-project

When writing or editing a portfolio project README, follow the existing pattern (see `portfolio-1-customer-support-bot/README.md`):

1. One-line hook summarizing what was built and the standout result
2. Problem
3. Solution
4. Tools
5. How It Works (numbered steps)
6. Results (concrete test scenarios / outcomes, not vague claims)
7. What I'd Scale Next

## Security

- **Never commit API keys.** This repo is public and deployed via GitHub Pages — anything committed is live on the internet. Use environment variables (e.g. `os.environ["ANTHROPIC_API_KEY"]`) or a `.env` file excluded via `.gitignore`, never a literal key in source.
- Real key lives in `.env` at the repo root (`ANTHROPIC_API_KEY=...`), loaded via `python-dotenv`'s `load_dotenv()`. `.env.example` holds only the placeholder (`your-api-key-here`) and is safe to commit.
- Before debugging "API key not found" errors, check the `.env` file actually has content (`ls -la .env` — file size should be well above 0 bytes), not just that the file exists. An empty `.env` file will silently produce authentication errors.
- Before committing in GitHub Desktop, always double-check `.env` (the real one) is NOT in the changed-files list — only `.env.example` should ever be tracked.

## Working Style

- Chelsea is a coding beginner working through this via Cursor + Claude Code, mostly via screenshots and step-by-step guidance.
- When suggesting fixes or refactors, explain what changed and why in plain language — not just the diff.
- Prefer Plan Mode for any non-trivial change: explain the plan first, get approval, then execute and verify (e.g. syntax check, live smoke test) rather than declaring success without confirming.