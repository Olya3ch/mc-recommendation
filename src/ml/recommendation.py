import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.preprocessing import normalize


def calculate_similarity_scores(vectors_df):
    n_topics = 10
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    topic_matrix = lda.fit_transform(vectors_df)

    normalized_topic_matrix = normalize(topic_matrix)
    similarity_matrix = cosine_similarity(normalized_topic_matrix)
    return similarity_matrix


def build_recommendation_system(
    similarity_matrix, article_id_mapping, min_similarity=0.5
):
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
            inverted_mapping[article_idx]
            for article_idx in similar_articles
            if similarities[article_idx] >= min_similarity
        ]

        return recommended_article_ids

    return recommend_articles
