import re
from pathlib import Path

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

emails = ["Sarah@example.com", "not-an-email", "JAMES@Company.COM", "missing.com", "Maria@Test.org"]

clean_emails = sorted({e.strip().lower() for e in emails if EMAIL_RE.match(e.strip())})

print(clean_emails)

path = Path("sample.txt")
if not path.exists():
    print(f"{path} not found")
else:
    with path.open("r", encoding="utf-8") as file:
        for i, line in enumerate(file, start=1):
            print(f"Line {i}: {line.strip()}")