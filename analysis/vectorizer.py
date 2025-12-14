# TF-IDF vectorizer

from sklearn.feature_extraction.text import TfidfVectorizer


vectorizer = TfidfVectorizer(max_features=5000)


def vectorize(texts):
    return vectorizer.fit_transform(texts)