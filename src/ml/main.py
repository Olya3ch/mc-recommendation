import pandas as pd
from src.ml.utils import article_id_mapping
from vectorization import vectorize_features
from recommendation import calculate_similarity_scores, build_recommendation_system


def main(article_id, n_recommendations=5):
    articles = pd.read_csv("src/data/seed/ro_articles.csv")
    mapped_ids = article_id_mapping(articles)

    combined_features = (
        articles["title"]
        + " "
        + articles["content"]
        + " "
        + articles["category"]
        + " "
        + articles["author"]
    )

    vectors = vectorize_features(combined_features)

    similarity_matrix = calculate_similarity_scores(vectors)
    recommend_articles_func = build_recommendation_system(similarity_matrix, mapped_ids)

    recommendations = recommend_articles_func(article_id)

    sorted_recommendations = sorted(
        recommendations,
        key=lambda x: similarity_matrix[mapped_ids[article_id]][mapped_ids[x]],
        reverse=True,
    )

    return sorted_recommendations[:n_recommendations]


recommended_articles = main(340622)
print("Recommended articles:", recommended_articles)
