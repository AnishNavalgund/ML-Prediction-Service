import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC

MODEL_PATH = "model.pkl"
vectorizer = CountVectorizer()
model = SVC(kernel="linear")


def train(samples):
    texts = [s["text"] for s in samples]
    labels = [s["label"] for s in samples]
    X = vectorizer.fit_transform(texts)
    model.fit(X, labels)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump((vectorizer, clf), f)


def predict(text):
    with open(MODEL_PATH, "rb") as f:
        vec, model = pickle.load(f)
    X = vec.transform([text])
    return model.predict(X)[0]
