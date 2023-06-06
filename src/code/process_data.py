import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

articles = pd.read_csv("src/data/seed/ro_articles.csv")


def vectorize_features(df):
    vectorizer = TfidfVectorizer()

    features = vectorizer.fit_transform(df["keywords"])

    return features, vectorizer


features, vectorizer = vectorize_features(articles)

print(features.toarray())
