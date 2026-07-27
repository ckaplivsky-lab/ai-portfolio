import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

# Load the API key from the .env file
load_dotenv()

# Create the Claude client using your API key
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_company_summary(company_name):
    """Ask Claude for a 3-sentence summary of a company. Returns None if the call fails."""
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"Give me a 3-sentence summary of the company {company_name}. Focus on what they do, their market, and any notable facts."
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error calling Claude API for '{company_name}': {e}")
        return None

def save_to_csv(company_name, summary, filename="company_summaries.csv"):
    """Append a new row to the CSV file, creating it with headers if needed."""
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["company_name", "summary", "timestamp"])
        writer.writerow([company_name, summary, datetime.now().isoformat()])

if __name__ == "__main__":
    company = input("Enter a company name: ")
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