import os
import csv
from datetime import datetime
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic

# Load the API key from the .env file
load_dotenv()

# Create the Claude client using your API key
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Leading characters spreadsheet apps (Excel/Sheets) treat as formula triggers
CSV_FORMULA_PREFIXES = ("=", "+", "-", "@")


def sanitize_for_csv(value):
    """Neutralize leading characters that spreadsheet apps interpret as formulas."""
    if value.startswith(CSV_FORMULA_PREFIXES):
        return "'" + value
    return value


def get_company_summary(company_name):
    """Ask Claude for a 3-sentence summary of a company. Returns None if the call fails."""
    try:
        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"Give me a 3-sentence summary of the company {company_name}. Focus on what they do, their market, and any notable facts."
                }
            ]
        )
    except anthropic.AuthenticationError:
        print("Error: invalid or missing ANTHROPIC_API_KEY.")
        return None
    except anthropic.RateLimitError:
        print(f"Error: rate limited while summarizing '{company_name}'. Try again shortly.")
        return None
    except anthropic.APIStatusError as e:
        print(f"Error calling Claude API for '{company_name}': {e.status_code} {e.message}")
        return None
    except anthropic.APIConnectionError:
        print(f"Error: network issue while summarizing '{company_name}'. Check your connection.")
        return None

    if message.stop_reason == "refusal":
        print(f"Claude declined to summarize '{company_name}'.")
        return None

    text = next((block.text for block in message.content if block.type == "text"), None)
    if text is None:
        print(f"No text content returned for '{company_name}'.")
        return None

    if message.stop_reason == "max_tokens":
        print("Warning: summary was cut off at the token limit and may be incomplete.")

    return text

def save_to_csv(company_name, summary, filename="company_summaries.csv"):
    """Append a new row to the CSV file, creating it with headers if needed."""
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["company_name", "summary", "timestamp"])
        writer.writerow([
            sanitize_for_csv(company_name),
            sanitize_for_csv(summary),
            datetime.now().isoformat(),
        ])

if __name__ == "__main__":
    company = input("Enter a company name: ").strip()

    if not company:
        print("No company name entered — exiting.")
    else:
        summary = get_company_summary(company)

        if summary is None:
            print("Skipping save — no summary was generated due to an error.")
        else:
            print()
            print("Summary:")
            print(summary)
            save_to_csv(company, summary)
            print()
            print(f"Saved to company_summaries.csv")