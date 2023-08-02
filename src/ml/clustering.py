from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def apply_clustering(vectors_df, num_clusters):
    kmeans_model = KMeans(n_clusters=num_clusters)
    vectors_df["cluster_labels"] = kmeans_model.fit_predict(vectors_df)
    return kmeans_model


def plot_clusters(vectors_df, kmeans_model):
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(vectors_df)

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
