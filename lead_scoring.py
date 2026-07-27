leads = [
    {"name": "Sarah Cohen", "company": "TechFlow Inc", "email": "sarah@techflow.com", "score": 9},
    {"name": "Mike Chen", "company": "DataSync", "email": "mike@datasync.io", "score": 4},
    {"name": "Priya Patel", "company": "CloudNine Marketing", "email": "priya@cloudnine.com", "score": 8}
]

print("All leads with score above 7:")
print()

for lead in leads:
    if lead["score"] > 7:
        print(f"Name: {lead['name']}")
        print(f"Company: {lead['company']}")
        print(f"Email: {lead['email']}")
        print(f"Score: {lead['score']}")
        print()