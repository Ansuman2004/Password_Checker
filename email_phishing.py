import re

# List of common phishing keywords and suspicious phrases
phishing_keywords = [
    "urgent", "password", "account", "verify", "click here", "login", "bank", 
    "social security", "ssn", "update", "confirm", "suspend", "security alert",
    "winner", "free", "prize", "risk", "attention", "immediately"
]

# Simple function to check phishing keywords
def detect_phishing(email_text):
    email_text_lower = email_text.lower()
    found_keywords = [kw for kw in phishing_keywords if kw in email_text_lower]

    # Simple scoring based on number of suspicious keywords found
    score = len(found_keywords)

    if score == 0:
        result = "Safe"
    elif 1 <= score <= 3:
        result = "Suspicious"
    else:
        result = "Phishing"

    return result, found_keywords

# Example usage
if __name__ == "__main__":
    print("Enter the email text to analyze:")
    email_input = ""
    print("(Type 'END' on a new line to finish input)")
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        email_input += line + "\n"

    verdict, keywords_found = detect_phishing(email_input)
    print(f"\nEmail Verdict: {verdict}")
    if keywords_found:
        print(f"Suspicious keywords found: {', '.join(keywords_found)}")
    else:
        print("No suspicious keywords detected.")
