import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity_scores(vectors_df):
    similarity_matrix = cosine_similarity(vectors_df)
    return pd.DataFrame(
        similarity_matrix, index=vectors_df.index, columns=vectors_df.index
    )


def build_recommendation_system(similarity_matrix, article_id_mapping):
    inverted_mapping = {v: k for k, v in article_id_mapping.items()}

    def recommend_articles(article_id):
        index = article_id_mapping[article_id]

        similarities = similarity_matrix[index]

        similar_articles = sorted(
            range(len(similarities)), key=lambda i: similarities[i], reverse=True
        )

        similar_articles = [
            article_idx for article_idx in similar_articles if article_idx != index
        ]

        recommended_article_ids = [
            inverted_mapping[article_idx] for article_idx in similar_articles
        ]

        return recommended_article_ids

    return recommend_articles
