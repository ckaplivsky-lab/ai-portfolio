import os
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic

# Load the API key from the .env file
load_dotenv()

# Create the Claude client using your API key
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

INPUT_FILE = "companies.csv"
OUTPUT_FILE = "lead_research_results.csv"

# Leading characters spreadsheet apps (Excel/Sheets) treat as formula triggers
CSV_FORMULA_PREFIXES = ("=", "+", "-", "@")


def sanitize_for_csv(value):
    """Neutralize leading characters that spreadsheet apps interpret as formulas."""
    if isinstance(value, str) and value.startswith(CSV_FORMULA_PREFIXES):
        return "'" + value
    return value


def get_company_brief(company_name):
    """Ask Claude for a 3-sentence brief on a company. Returns None if the call fails."""
    try:
        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"Give me a 3-sentence brief on the company {company_name}. Focus on what they do, their market, and any notable facts."
                }
            ]
        )
    except anthropic.AuthenticationError:
        print("  Error: invalid or missing ANTHROPIC_API_KEY.")
        return None
    except anthropic.RateLimitError:
        print(f"  Error: rate limited while researching '{company_name}'.")
        return None
    except anthropic.APIStatusError as e:
        print(f"  Error calling Claude API: {e.status_code} {e.message}")
        return None
    except anthropic.APIConnectionError:
        print(f"  Error: network issue while researching '{company_name}'.")
        return None

    if message.stop_reason == "refusal":
        print(f"  Claude declined to research '{company_name}'.")
        return None

    text = next((block.text for block in message.content if block.type == "text"), None)
    if text is None:
        print(f"  No text content returned for '{company_name}'.")
        return None

    if message.stop_reason == "max_tokens":
        print("  Warning: brief was cut off at the token limit and may be incomplete.")

    return text.strip()


def read_company_names(filename):
    """Read company names from the input CSV. Expects a 'company_name' column header."""
    companies = []
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.get("company_name", "").strip()
            if name:
                companies.append(name)
    return companies


def write_results(results, filename):
    """Write all results (successes and failures) to the output CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["company_name", "brief", "status", "timestamp"])
        for row in results:
            writer.writerow([
                sanitize_for_csv(row["company_name"]),
                sanitize_for_csv(row["brief"]),
                row["status"],
                row["timestamp"],
            ])


if __name__ == "__main__":
    if not os.path.isfile(INPUT_FILE):
        print(f"Error: '{INPUT_FILE}' not found. Make sure it's in the same folder as this script.")
        exit(1)

    companies = read_company_names(INPUT_FILE)

    if not companies:
        print(f"No company names found in '{INPUT_FILE}'. Check that it has a 'company_name' column.")
        exit(1)

    print(f"Found {len(companies)} companies to research.\n")

    results = []
    succeeded = 0
    failed = 0

    for i, company in enumerate(companies, start=1):
        print(f"[{i}/{len(companies)}] Researching '{company}'...")
        brief = get_company_brief(company)

        if brief is None:
            print(f"  Failed — logging and continuing.\n")
            results.append({
                "company_name": company,
                "brief": "ERROR: research failed, see terminal log",
                "status": "failed",
                "timestamp": datetime.now().isoformat(),
            })
            failed += 1
        else:
            print(f"  Done.\n")
            results.append({
                "company_name": company,
                "brief": brief,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
            })
            succeeded += 1

        # Small delay between calls to be gentle on the API / avoid rate limits
        time.sleep(0.5)

    write_results(results, OUTPUT_FILE)

    print("=" * 40)
    print(f"Done: {succeeded} succeeded, {failed} failed.")
    print(f"Results saved to {OUTPUT_FILE}")
