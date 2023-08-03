import pandas as pd
from src.ml.utils import create_mapping_between_article_id_and_index
from vectorization import vectorize_features
from recommendation import calculate_similarity_scores, build_recommendation_system


def main(article_id):
    articles = pd.read_csv("src/data/seed/ro_articles.csv")

    vectors_df = vectorize_features(articles)

    similarity_matrix = calculate_similarity_scores(vectors_df)

    article_id_mapping = dict(enumerate(articles["id"]))

    recommend_articles_func = build_recommendation_system(
        vectors_df, similarity_matrix, article_id_mapping
    )

    recommended_articles = recommend_articles_func(article_id)
    print("Recommended articles:", recommended_articles)


main(99270)
