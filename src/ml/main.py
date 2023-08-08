import pandas as pd
from src.ml.utils import article_id_mapping
from vectorization import vectorize_features
from recommendation import calculate_similarity_scores, build_recommendation_system


def main(article_id):
    articles = pd.read_csv("src/data/seed/ro_articles.csv")
    articles.fillna("", inplace=True)
    mapped_ids = article_id_mapping(articles)

    features = ["title", "content", "category", "author"]

    all_recommendations = []

    for feature in features:
        if articles[feature] is None:
            print(f"Skipping empty {feature}")
            continue

        vectors = vectorize_features(articles, feature)

        similarity_matrix = calculate_similarity_scores(vectors, method="cosine")
        recommend_articles_func = build_recommendation_system(
            similarity_matrix, mapped_ids
        )

        recommendations = recommend_articles_func(article_id)
        all_recommendations.extend(recommendations)

    sorted_recommendations = sorted(
        all_recommendations, key=lambda x: all_recommendations.count(x), reverse=True
    )

    print("Recommended articles:", sorted_recommendations[:5])


main(340622)
