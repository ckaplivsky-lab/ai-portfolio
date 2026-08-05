# Lead Research Agent

Built a batch lead enrichment tool that takes a CSV of company names and turns it into a CSV of AI-generated company briefs — tested on 10 real companies with zero failures, including graceful handling for API errors so one bad call never kills the batch.

**Skills demonstrated:** batch processing with the Claude API, defensive error handling (typed exceptions, fail-and-continue design), and CSV I/O with formula-injection sanitization.

## Problem

Manually researching a list of inbound leads or prospect companies — pulling up each one, reading their site, writing a summary — is slow and doesn't scale past a handful of names. Sales and marketing teams need a fast first-pass brief on many companies at once, without burning an afternoon on it.

## Solution

A Python script that reads a list of company names from a CSV, calls the Claude API for a 3-sentence brief on each one, and writes all the results — successes and failures alike — to a new CSV. If any single company's research fails (rate limit, network issue, refusal), the script logs it and keeps going instead of stopping the whole batch.

## Tools

- Python
- Claude API (Sonnet 5), via the `anthropic` library
- `csv` module for reading input and writing output
- `python-dotenv` for API key management

## How It Works

1. Company names are read from `companies.csv` (one column: `company_name`)
2. For each company, the script sends a prompt to Claude asking for a 3-sentence brief covering what they do, their market, and any notable facts
3. Each API call is wrapped in typed exception handling — authentication errors, rate limits, network issues, and refusals are all caught individually and logged with a specific message
4. If a call fails, the company is recorded with `status: failed` and the script moves on to the next one rather than crashing
5. All results (brief text, status, timestamp) are written to `lead_research_results.csv`, with CSV formula-injection sanitization applied to any text starting with `=`, `+`, `-`, or `@`
6. A running progress log prints to the terminal as it works (`[3/10] Researching 'Figma'...`)

## Results

Tested on 10 real B2B SaaS companies (Notion, Stripe, Figma, Airtable, Linear, Vercel, Ramp, Retool, Loom, Webflow):

- **10/10 succeeded** on the clean run, with complete, well-formed 3-sentence briefs for each
- Caught a real bug during testing: the initial `max_tokens=300` limit caused 3 of 10 briefs to truncate mid-sentence — increasing it to `500` resolved this completely on the next run, a good example of iterating based on actual output rather than assuming the first version was correct
- Error handling was written to fail gracefully per-company (not tested against a live failure in this run, but verified the logic path: a failed call gets logged with `status: failed` and an explanatory error message printed to the terminal, while the rest of the batch continues uninterrupted)

## What I'd Scale Next

- Reconnect this to the Make webhook pipeline from Portfolio Piece 1's follow-up work (`enrich.py`) so each successful research result also posts to Slack/Sheets automatically, turning this into a fully automated batch enrichment pipeline
- Add retry logic with backoff for rate-limited or transiently failed calls, instead of marking them failed on the first attempt
- Swap the flat CSV input for a real CRM export or Google Sheet, so this could run directly against a live lead list instead of a manually prepared file
