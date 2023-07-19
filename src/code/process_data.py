import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


articles = pd.read_csv("src/data/seed/ro_articles.csv")


def vectorize_features(df):
    vectorizer = TfidfVectorizer()

    features = vectorizer.fit_transform(df["keywords"])

    vectors = pd.DataFrame(
        features.todense(), columns=vectorizer.get_feature_names_out()
    )

    vectors.to_csv("src/vectorized_features.csv", index=False)

    return vectors


vectors = vectorize_features(articles)


def choose_number_of_clusters():
    wcss = []

    clusters_range = range(1, 11)

    for num_clusters in clusters_range:
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(vectors)
        wcss.append(kmeans.inertia_)

    plt.plot(clusters_range, wcss)
    plt.xlabel("Number of Clusters")
    plt.ylabel("WCSS")
    plt.title("Elbow Method")
    plt.show()


print(choose_number_of_clusters())
