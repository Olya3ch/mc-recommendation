import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def vectorize_features(df):
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(df["keywords"])
    vectors_df = pd.DataFrame(
        features.todense(), columns=vectorizer.get_feature_names_out()
    )
    return vectors_df
