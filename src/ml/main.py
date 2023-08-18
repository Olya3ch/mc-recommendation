import pandas as pd
from src.ml.utils import article_id_mapping
from vectorization import vectorize_features
from recommendation import calculate_similarity_scores, build_recommendation_system


def main(article_id):
    articles = pd.read_csv("src/data/seed/ro_articles.csv")
    mapped_ids = article_id_mapping(articles)

    combined_features = articles["title"] + " " + articles["content"]
    combined_features.fillna("", inplace=True)

    vectors = vectorize_features(combined_features)

    similarity_matrix = calculate_similarity_scores(vectors)

    recommend_articles_func = build_recommendation_system(similarity_matrix, mapped_ids)
    recommendations = recommend_articles_func(article_id)

    similarity_scores_dict = {}

    for recommended_id in recommendations:
        similarity_score = similarity_matrix[mapped_ids[article_id]][
            mapped_ids[recommended_id]
        ]
        similarity_scores_dict[recommended_id] = similarity_score

    sorted_recommendations = sorted(
        similarity_scores_dict.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    return sorted_recommendations


recommended_articles = main(65551)

print("Recommended articles:", recommended_articles)
print("Length of recommendations", len(recommended_articles))
