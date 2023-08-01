from os import environ as env
from dotenv import load_dotenv
import pandas as pd
from src.ml.clustering import apply_clustering
from src.ml.vectorization import vectorize_features

load_dotenv()

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def main():
    articles = pd.read_csv("src/data/seed/ro_articles.csv")
    vectors_df = vectorize_features(articles)
    kmeans_model = apply_clustering(vectors_df, int(env["NUMBER_OF_CLUSTERS"]))

    # Apply PCA to reduce dimensionality to 2D for visualization
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(vectors_df)

    # Plot the clusters
    plt.figure(figsize=(8, 6))
    plt.scatter(
        reduced_vectors[:, 0],
        reduced_vectors[:, 1],
        c=kmeans_model.labels_,
        cmap="rainbow",
    )
    plt.scatter(
        kmeans_model.cluster_centers_[:, 0],
        kmeans_model.cluster_centers_[:, 1],
        s=300,
        c="black",
        marker="X",
    )
    plt.title("KMeans Clustering Results")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.show()


main()
