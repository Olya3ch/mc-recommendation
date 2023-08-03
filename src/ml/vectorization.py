import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def vectorize_features(df):
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(df["keywords"])
    vectors_df = pd.DataFrame(
        features.todense(), columns=vectorizer.get_feature_names_out()
    )
    kmeans_model = KMeans(n_clusters=3)
    clusters = kmeans_model.fit_predict(features)

    vectors_df["cluster_labels"] = clusters
    return vectors_df
