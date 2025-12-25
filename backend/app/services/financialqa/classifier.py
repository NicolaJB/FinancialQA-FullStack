# classifier.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle

# Import tiny dataset
from tiny_dataset import texts, labels

# Build a simple pipeline: TF-IDF + Naive Bayes
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train
model.fit(texts, labels)

# Save model
with open("text_classifier.pkl", "wb") as f:
    pickle.dump(model, f)

print("Classifier trained and saved.")
