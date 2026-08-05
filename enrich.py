import os
import sys
import json
import requests
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic

# Load the API key from the .env file
load_dotenv()

# Create the Claude client using your API key
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Your Make.com webhook URL — paste the one from your "lead-enrichment" scenario
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")


def get_company_research(company_name):
    """Ask Claude to research a company and return structured data as a dict.
    Returns None if the call fails or the response can't be parsed."""
    try:
        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=400,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Research the company '{company_name}' and respond with ONLY a JSON object "
                        f"(no other text, no markdown formatting, no code fences) with exactly these keys:\n"
                        f'"company_name": the company\'s proper name,\n'
                        f'"summary": a 3-sentence summary of what they do and their market,\n'
                        f'"industry": their primary industry in a few words,\n'
                        f'"website": their best-guess official website URL, or "unknown" if you are not confident.'
                    )
                }
            ]
        )
    except anthropic.AuthenticationError:
        print("Error: invalid or missing ANTHROPIC_API_KEY.")
        return None
    except anthropic.RateLimitError:
        print(f"Error: rate limited while researching '{company_name}'. Try again shortly.")
        return None
    except anthropic.APIStatusError as e:
        print(f"Error calling Claude API for '{company_name}': {e.status_code} {e.message}")
        return None
    except anthropic.APIConnectionError:
        print(f"Error: network issue while researching '{company_name}'. Check your connection.")
        return None

    if message.stop_reason == "refusal":
        print(f"Claude declined to research '{company_name}'.")
        return None

    text = next((block.text for block in message.content if block.type == "text"), None)
    if text is None:
        print(f"No text content returned for '{company_name}'.")
        return None

    if message.stop_reason == "max_tokens":
        print("Warning: response was cut off at the token limit and may be incomplete.")

    # Strip markdown code fences if Claude adds them despite instructions
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        print(f"Error: could not parse Claude's response as JSON for '{company_name}'.")
        print("Raw response was:")
        print(text)
        return None

    return data


def send_to_make(data):
    """POST the enrichment data to the Make webhook. Returns True on success."""
    if not MAKE_WEBHOOK_URL:
        print("Error: MAKE_WEBHOOK_URL is not set in your .env file — skipping webhook send.")
        return False

    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=data, timeout=10)
    except requests.exceptions.ConnectionError:
        print("Error: could not connect to the Make webhook. Check your internet connection or the URL.")
        return False
    except requests.exceptions.Timeout:
        print("Error: the request to Make timed out.")
        return False

    if response.status_code == 200:
        return True
    else:
        print(f"Error: Make webhook responded with status {response.status_code}: {response.text}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python enrich.py "Company Name"')
        sys.exit(1)

    company = " ".join(sys.argv[1:]).strip()

    if not company:
        print("No company name entered — exiting.")
        sys.exit(1)

    print(f"Researching '{company}'...")
    data = get_company_research(company)

    if data is None:
        print("Skipping webhook send — no data was generated due to an error.")
        sys.exit(1)

    print()
    print("Results:")
    print(f"  Company:  {data.get('company_name', 'N/A')}")
    print(f"  Industry: {data.get('industry', 'N/A')}")
    print(f"  Website:  {data.get('website', 'N/A')}")
    print(f"  Summary:  {data.get('summary', 'N/A')}")
    print()

    print("Sending to Make...")
    success = send_to_make(data)

    if success:
        print("Sent successfully — check Slack and Google Sheets.")
    else:
        print("Failed to send to Make. See error above.")
