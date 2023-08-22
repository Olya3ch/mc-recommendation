import pandas as pd
from src.ml.recommendation import recommend_articles
from src.ml.utils import article_id_mapping
from recommendation import recommend_articles
from src.ml.vector_similarity import (
    calculate_similarity_matrix,
    calculate_similarity_scores_dict,
)


def main(article_id):
    articles_df = pd.read_csv("src/data/seed/ro_articles.csv")
    articles_df.fillna("", inplace=True)
    mapped_ids = article_id_mapping(articles_df)

    similarity_matrix = calculate_similarity_matrix(articles_df)

    recommendations = recommend_articles(
        article_id, similarity_matrix, mapped_ids, articles_df
    )

    similarity_scores_dict = calculate_similarity_scores_dict(
        similarity_matrix, article_id, mapped_ids, recommendations
    )

    sorted_recommendations = sorted(
        similarity_scores_dict.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    return sorted_recommendations


if __name__ == "__main__":
    article_id = 51562
    recommended_articles = main(article_id)
    print("Recommended articles:", recommended_articles)
    print("Length of recommendations:", len(recommended_articles))
