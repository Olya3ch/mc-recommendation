import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

articles = pd.read_csv("src/data/seed/ro_articles.csv")


def vectorize_features(df):
    vectorizer = TfidfVectorizer()

    features = vectorizer.fit_transform(df["keywords"])

    vectors = pd.DataFrame(
        features.todense(), columns=vectorizer.get_feature_names_out()
    )

    vectors.to_csv("src/vectorized_features.csv", index=False)

    return vectors
