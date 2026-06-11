🌐 Live Demo: https://phishguard-rdrv.onrender.com/dashboard

# PhishGuard AI 🛡️

> AI-powered phishing detection that explains threats in plain English

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue)](https://phishguard-rdrv.onrender.com)
[![Accuracy](https://img.shields.io/badge/ML%20Accuracy-98.35%25-green)]()
[![Python](https://img.shields.io/badge/Python-3.14-blue)]()

## What it does

PhishGuard scans emails in real time and explains threats like a security analyst instead of just saying "dangerous email detected."

**Instead of:** `SPAM DETECTED`

**PhishGuard says:** *"This email pretends to be from PayPal but the sender domain uses 'paypa1.com' — the letter L replaced with the number 1 — and creates urgency to prevent you from noticing the deception."*

## Demo

![PhishGuard Dashboard](dashboard-screenshot.png)

## Features

- Chrome extension that scans Gmail emails with one click
- 98.35% accurate ML model trained on 82,486 real phishing emails
- AI explanation engine powered by Llama 3.3 70B
- Real-time analytics dashboard
- REST API built with FastAPI

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| ML Model | scikit-learn, TF-IDF, Logistic Regression |
| AI Explanations | Groq API, Llama 3.3 70B |
| Browser Extension | JavaScript, Chrome Manifest V3 |
| Deployment | Render |
| Training Data | Kaggle (CEAS, Enron, Nazario, Nigerian Fraud datasets) |

## ML Model Performance

- Training set: 65,988 emails
- Test set: 16,498 emails  
- Accuracy: **98.35%**
- Dataset: 82,486 real phishing + legitimate emails

## How it works

1. Chrome extension reads email from Gmail
2. Sends to FastAPI backend via HTTP POST
3. Rule-based checks run (domain spoofing, urgency words, fake login patterns)
4. ML model scores the email (98.35% accurate)
5. Groq LLM generates plain-English explanation
6. Result displayed in browser instantly

## Setup

```bash
git clone https://github.com/peejaygmulbah231-del/phishguard
cd phishguard
pip install -r requirements.txt
cp .env.example .env  # add your GROQ_API_KEY
uvicorn main:app --reload
```

## API

```bash
POST https://phishguard-rdrv.onrender.com/analyze

{
  "sender": "security@paypa1.com",
  "subject": "Urgent: verify your account",
  "body": "Click here immediately"
}
```
<img width="1877" height="872" alt="dashboard2" src="https://github.com/user-attachments/assets/cce32f47-ac61-4fbf-8133-ee4cc0a0724d" />
<img width="1895" height="867" alt="dashboard" src="https://github.com/user-attachments/assets/27ccb437-0bae-4b97-b2fe-1e7e48f2ef34" />

## Author

Built by Peejay Gayflor Mulbah — cybersecurity startup project

---
⭐ Star this repo if you found it useful!
