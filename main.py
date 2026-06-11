import os
import pickle
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup
engine = create_engine("sqlite:///phishguard.db")
Base = declarative_base()

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender = Column(String)
    subject = Column(String)
    score = Column(Integer)
    label = Column(String)
    ml_confidence = Column(String)
    reasons = Column(String)
    explanation = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

load_dotenv()

app = FastAPI(title="PhishGuard API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load the trained ML model
print("Loading ML model...")
with open('phishing_model.pkl', 'rb') as f:
    ml_model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    ml_vectorizer = pickle.load(f)
print("ML model loaded successfully!")

class EmailRequest(BaseModel):
    sender: str
    subject: str
    body: str = ""

@app.get("/")
def home():
    return {"status": "PhishGuard API is running", "version": "2.0 with ML"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("dashboard.html")

@app.get("/metrics")
def get_metrics():
    session = Session()
    total = session.query(Scan).count()
    dangerous = session.query(Scan).filter(Scan.label == "DANGEROUS").count()
    suspicious = session.query(Scan).filter(Scan.label == "SUSPICIOUS").count()
    clean = session.query(Scan).filter(Scan.label == "CLEAN").count()
    recent = session.query(Scan).order_by(Scan.timestamp.desc()).limit(10).all()
    session.close()

    return {
        "total_scans": total,
        "dangerous": dangerous,
        "suspicious": suspicious,
        "clean": clean,
        "recent_scans": [
            {
                "timestamp": s.timestamp.strftime("%Y-%m-%d %H:%M"),
                "sender": s.sender,
                "label": s.label,
                "score": s.score
            } for s in recent
        ]
    }

@app.get("/milestone")
def get_milestone():
    session = Session()
    total = session.query(Scan).count()
    session.close()

    if total >= 1000:
        milestone = "1000 scans reached!"
        next_goal = 5000
    elif total >= 500:
        milestone = "500 scans reached!"
        next_goal = 1000
    elif total >= 100:
        milestone = "100 scans reached!"
        next_goal = 500
    elif total >= 50:
        milestone = "50 scans reached!"
        next_goal = 100
    else:
        milestone = "Building momentum"
        next_goal = 100

    return {
        "total_scans": total,
        "current_milestone": milestone,
        "next_goal": next_goal,
        "progress_percent": round((total / next_goal) * 100, 1)
    }

@app.post("/analyze")
def analyze_email(email: EmailRequest):
    score = 0
    reasons = []

    # Check sender domain
    bad_domains = ["paypa1", "amaz0n", "g00gle", "micros0ft"]
    for domain in bad_domains:
        if domain in email.sender:
            score += 50
            reasons.append("sender domain looks suspicious")

    # Check urgency words
    urgency_words = ["urgent", "verify", "suspended", "immediately", "action required"]
    for word in urgency_words:
        if word in email.subject.lower() or word in email.body.lower():
            score += 30
            reasons.append(f"urgency word detected: '{word}'")

    # Check for fake login patterns
    login_words = ["confirm your password", "enter your details", "login to verify"]
    for phrase in login_words:
        if phrase in email.body.lower():
            score += 40
            reasons.append("fake login page pattern detected")

    # ML model prediction
    email_text = f"{email.sender} {email.subject} {email.body}"
    email_vec = ml_vectorizer.transform([email_text])
    ml_prediction = ml_model.predict(email_vec)[0]
    ml_probability = ml_model.predict_proba(email_vec)[0][1]
    ml_score = int(ml_probability * 100)

    if ml_prediction == 1:
        score += ml_score
        reasons.append(f"ML model flagged this email ({ml_score}% confidence)")

    # Get AI explanation
    prompt = f"""You are a cybersecurity analyst.
Analyze this email and explain in 2 sentences why it is or is not a phishing attempt.
Be specific and clear for a non-technical user.

Sender: {email.sender}
Subject: {email.subject}
Body: {email.body[:500]}
Threat signals: {reasons if reasons else 'none'}
Score: {score}/100

Reply with only your explanation."""

    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    explanation = chat.choices[0].message.content

    # Save to database
    session = Session()
    scan = Scan(
        sender=email.sender,
        subject=email.subject,
        score=score,
        label="DANGEROUS" if score >= 70 else "SUSPICIOUS" if score >= 30 else "CLEAN",
        ml_confidence=f"{ml_score}%",
        reasons=json.dumps(reasons),
        explanation=explanation
    )
    session.add(scan)
    session.commit()
    session.close()

    return {
        "score": score,
        "label": "DANGEROUS" if score >= 70 else "SUSPICIOUS" if score >= 30 else "CLEAN",
        "ml_confidence": f"{ml_score}%",
        "reasons": reasons,
        "explanation": explanation
    }