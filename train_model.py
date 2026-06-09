import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle

print("Loading dataset...")
df = pd.read_csv('data/phishing_email.csv')
print(f"Loaded {len(df)} emails")
print(f"Phishing: {df['label'].sum()} | Legitimate: {len(df) - df['label'].sum()}")

# Clean the data
df = df.dropna(subset=['text_combined'])
df['text_combined'] = df['text_combined'].astype(str)

print("\nPreparing features...")
X = df['text_combined']
y = df['label']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training on {len(X_train)} emails")
print(f"Testing on {len(X_test)} emails")

# Convert text to numbers using TF-IDF
print("\nConverting text to features...")
vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words='english',
    ngram_range=(1, 2)
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train the model
print("\nTraining ML model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_vec, y_train)

# Test accuracy
print("\nEvaluating model...")
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy * 100:.2f}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred,
      target_names=['Legitimate', 'Phishing']))

# Save the model
print("\nSaving model...")
with open('phishing_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("\nModel saved as phishing_model.pkl")
print("Vectorizer saved as vectorizer.pkl")
print("\nPhishGuard ML model is ready!")
