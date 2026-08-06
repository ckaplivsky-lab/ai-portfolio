import os
import sys
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic

# Load the API key from the .env file
load_dotenv()

# Create the Claude client using your API key
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_ad_headlines(product_description):
    """Ask Claude for 5 ad headline variants for a product. Returns None if the call fails."""
    try:
        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Write 5 different ad headline variants for this product: "
                        f"{product_description}\n\n"
                        "Return only the 5 headlines, one per line, with no numbering, "
                        "bullets, or extra commentary."
                    )
                }
            ]
        )
    except anthropic.AuthenticationError:
        print("Error: invalid or missing ANTHROPIC_API_KEY.")
        return None
    except anthropic.RateLimitError:
        print("Error: rate limited while generating headlines. Try again shortly.")
        return None
    except anthropic.APIStatusError as e:
        print(f"Error calling Claude API: {e.status_code} {e.message}")
        return None
    except anthropic.APIConnectionError:
        print("Error: network issue while generating headlines. Check your connection.")
        return None

    if message.stop_reason == "refusal":
        print("Claude declined to generate headlines for this product.")
        return None

    text = next((block.text for block in message.content if block.type == "text"), None)
    if text is None:
        print("No text content returned.")
        return None

    if message.stop_reason == "max_tokens":
        print("Warning: response was cut off at the token limit and may be incomplete.")

    headlines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    return headlines


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 ad_headlines.py "<product description>"')
        sys.exit(1)

    product_description = sys.argv[1].strip()

    if not product_description:
        print("No product description provided — exiting.")
        sys.exit(1)

    headlines = get_ad_headlines(product_description)

    if headlines is None:
        print("Skipping output — no headlines were generated due to an error.")
        sys.exit(1)

    print()
    print("Ad Headlines:")
    for i, headline in enumerate(headlines, start=1):
        print(f"{i}. {headline}")
