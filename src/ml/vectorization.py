import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def vectorize_features(df):
    vectorizer = TfidfVectorizer(
        max_features=3000, min_df=100, max_df=0.6, sublinear_tf=True
    )
    features = vectorizer.fit_transform(df)

    vectors_df = pd.DataFrame(
        features.todense(), columns=vectorizer.get_feature_names_out()
    )

    return vectors_df
