import anthropic

client = anthropic.Anthropic(api_key="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")

def generate_listing(address, bedrooms, bathrooms, features):
    prompt = f"""
    Write 3 real estate listing descriptions for this property:
    
    Address: {address}
    Bedrooms: {bedrooms}
    Bathrooms: {bathrooms}
    Key features: {features}
    
    Write one description in each of these tones:
    1. LUXURY — elegant, aspirational, premium feel
    2. FRIENDLY — warm, approachable, family-oriented  
    3. INVESTMENT — facts-focused, ROI-driven, professional
    
    Keep each description to 3 sentences maximum.
    """
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

# Test it with a sample property
result = generate_listing(
    address="123 King Street West, Toronto, ON",
    bedrooms=2,
    bathrooms=2,
    features="floor-to-ceiling windows, rooftop terrace, open concept kitchen, downtown views"
)

print(result)