import re

def extract_role(text):
    patterns = [
        r"(?:looking for|hiring|seek(?:ing)?)\s+(?:a|an|the)?\s*([^,\.\n\r]+)",
        r"(?:role|position|job)\s+(?:is|of|as)\s+(?:a|an|the)?\s*([^,\.\n\r]+)",
        r"^([^,\.\n\r]+?)\s+(?:required|needed|wanted)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            role = re.split(r'\s+(?:who|with|that|for|at|to)\b', role, flags=re.IGNORECASE)[0]
            role = re.sub(r"^(?:a|an|the)\s+", "", role, flags=re.IGNORECASE).strip()
            if len(role.split()) <= 5:
                return role.strip()
    words = text.split()
    if len(words) < 10:
        return text.strip()
    return None

def extract_experience(text):
    patterns = [
        r"(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience",
        r"experience\s*(?:of|in)?\s*(\d+)\+?\s*(?:years?|yrs?)",
        r"(\d+)\+?\s*(?:years?|yrs?)\s+in\b",
        r"worked\s+for\s+(\d+)\+?\s*(?:years?|yrs?)"
    ]
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            try:
                val = int(m)
                if val < 50:
                    years.append(val)
            except:
                pass
    return max(years) if years else 0

# Test cases
test_jds = [
    "I am looking for an advocate with 5 years of experience",
    "Senior Java Developer wanted. 8+ years experience in coding.",
    "Hiring a Python Engineer for a high-growth startup",
    "We seek an experienced litigation lawyer who has worked for 10 years"
]

print("--- Testing Role & Experience Extraction ---")
for jd in test_jds:
    role = extract_role(jd)
    exp = extract_experience(jd)
    print(f"JD: {jd}")
    print(f"  Result -> Role: '{role}', Exp: {exp}")
    print("-" * 20)
