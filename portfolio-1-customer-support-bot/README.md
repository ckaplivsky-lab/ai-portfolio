Built a working AI support automation from scratch: Google Forms → Sheets → Make → Claude API → Gmail. Tested across 9 scenarios including angry customers, edge cases, and questions outside the bot's knowledge — it never hallucinated a policy it didn't have.
Problem
Small businesses get repetitive customer support questions — order tracking, returns, shipping, policy questions — that eat up time better spent elsewhere, but customers still expect fast, personalized responses rather than a canned FAQ page.
Solution
An automated pipeline that takes a customer's question from a form, generates a thoughtful, personalized response using Claude, and emails it back automatically — no human in the loop for first-response triage.
Tools
Google Forms, Google Sheets, Make (automation), Claude API (Sonnet 4.6), Gmail
How It Works

Customer submits a question via a Google Form (question + email)
The response lands as a new row in a linked Google Sheet
Make's "Watch New Rows" module detects the new submission and triggers the scenario
An HTTP module sends the question to the Claude API along with a system prompt defining the bot's role and tone
Claude's response is parsed out of the API's JSON reply
A Gmail module sends that response back to the customer's email automatically

Results
Tested across 9 realistic scenarios covering a range of difficulty:

Frustrated/angry customer (late packages) → responded with genuine empathy and a clear resolution path, without being saccharine
Questions outside its knowledge (shipping rates, return policy, gift cards, phone number) → consistently declined to guess and redirected to official channels instead of inventing false information
Edge cases (nonsense input, bare "hi") → degraded gracefully rather than breaking or producing a confusing reply
Specific requests (refund not replacement, address change) → correctly followed the customer's actual ask rather than defaulting to a generic script

The standout result: the bot never hallucinated a policy, price, or contact detail it didn't actually have — a common failure mode in beginner AI support demos. That behavior came directly from prompt design, not luck.
What I'd Scale Next

Connect it to a real order/CRM lookup (via tool use) so it can check actual order status instead of asking the customer to look it up themselves
Add an escalation path — if the bot detects high frustration or a request it can't resolve, auto-flag it for human follow-up instead of just redirecting
Log every question + response to a dashboard to spot common question patterns over time (an early version of what a real support team would use to justify adding an FAQ or fixing a process issue)
