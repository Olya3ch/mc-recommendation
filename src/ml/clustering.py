import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_optimal_clusters(features):
    wcss = []
    clusters_range = range(1, 11)

    for num_clusters in clusters_range:
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(features)
        wcss.append(kmeans.inertia_)

    plt.plot(clusters_range, wcss)
    plt.xlabel("Number of Clusters")
    plt.ylabel("WCSS")
    plt.title("Elbow Method")
    plt.show()


def apply_clustering(vectors_df, n_clusters):
    kmeans_model = KMeans(n_clusters=n_clusters)
    kmeans_model.fit(vectors_df)
    return kmeans_model
