import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

articles = pd.read_csv("src/data/seed/ro_articles.csv")
articles.fillna("", inplace=True)


def vectorize_features(df):
    vectorizer = TfidfVectorizer()
    df["text"] = df["author"] + " " + df["keywords"] + " " + df["categories"]

    features = vectorizer.fit_transform(df["text"])

    return features, vectorizer


print(vectorize_features(articles))
