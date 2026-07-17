# AI Automation Portfolio

Chelsea's portfolio of AI automation projects, built for job applications. Each `portfolio-N-*` folder is a standalone, self-contained project with its own README — treat them independently, not as parts of one app.

## Stack

- **Make.com** — automation/orchestration (forms, sheets, triggers, email, etc.)
- **Claude API** (Anthropic) — the AI logic inside each automation
- Supporting glue scripts are plain Python where needed (e.g. `listing_generator.py`)

## Structure

- `portfolio-N-<name>/README.md` — problem, solution, tools, how-it-works, results, and "what I'd scale next" for that project
- Root `README.md` and loose scripts (e.g. `listing_generator.py`) are individual demos, not shared infrastructure — don't assume code in one folder is reused by another
- Site is deployed as static content to GitHub Pages via `.github/workflows/static.yml` on push to `main`

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
