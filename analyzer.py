import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_email(sender, subject):
    score = 0
    reasons = []

    # Check sender domain
    bad_domains = ["paypa1", "amaz0n", "g00gle", "micros0ft"]
    for domain in bad_domains:
        if domain in sender:
            score += 50
            reasons.append("sender domain looks suspicious")

    # Check subject urgency
    urgency_words = ["urgent", "verify", "suspended", "immediately", "action required"]
    for word in urgency_words:
        if word in subject.lower():
            score += 30
            reasons.append(f"urgency word detected: '{word}'")

    # ML model prediction
    email_text = f"{email.sender} {email.subject} {email.body}"
    email_vec = ml_vectorizer.transform([email_text])
    ml_prediction = ml_model.predict(email_vec)[0]
    ml_probability = ml_model.predict_proba(email_vec)[0][1]
    ml_score = int(ml_probability * 100)

    if ml_prediction == 1:
        score += ml_score
        reasons.append(f"ML model flagged this email ({ml_score}% confidence)")

    # Build AI explanation
    prompt = f"""You are a cybersecurity analyst.
Analyze this email and explain in 2 sentences why it is or is not a phishing attempt.
Be specific and clear for a non-technical user.

Sender: {sender}
Subject: {subject}
Threat signals found: {reasons if reasons else 'none'}
Threat score: {score}/100

Reply with only your explanation, nothing else."""

    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    ai_explanation = chat.choices[0].message.content

    return {
        "score": score,
        "label": "DANGEROUS" if score >= 70 else "SUSPICIOUS" if score >= 30 else "CLEAN",
        "ml_confidence": f"{ml_score}%",
        "reasons": reasons,
        "explanation": explanation
    }


# Test it
result = analyze_email("security@paypa1.com", "Urgent: verify your account now")
print(f"Score: {result['score']}/100")
print(f"Label: {result['label']}")
print(f"\nAI says: {result['ai_explanation']}")