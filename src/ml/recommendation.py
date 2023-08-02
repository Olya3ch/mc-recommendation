import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity_scores(vectors_df):
    similarity_matrix = cosine_similarity(vectors_df)
    return pd.DataFrame(
        similarity_matrix, index=vectors_df.index, columns=vectors_df.index
    )


def build_recommendation_system(vectors_df, similarity_matrix):
    article_id_to_cluster = dict(vectors_df["cluster_labels"].reset_index().values)

    def recommend_articles(article_id, num_recommendations=5):
        cluster_label = article_id_to_cluster.get(article_id)
        if cluster_label is None:
            return []

        similar_articles = similarity_matrix[
            similarity_matrix.index.isin(
                vectors_df[vectors_df["cluster_labels"] == cluster_label].index
            )
        ]
        similar_articles = similar_articles.sort_values(by=article_id, ascending=False)
        similar_articles = similar_articles[1 : num_recommendations + 1]

        recommended_articles = similar_articles.index.tolist()

        return recommended_articles

    return recommend_articles
