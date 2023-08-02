import pandas as pd
from vectorization import vectorize_features
from recommendation import calculate_similarity_scores, build_recommendation_system


def main():
    articles = pd.read_csv("src/data/seed/ro_articles.csv")

    vectors_df = vectorize_features(articles)

    similarity_matrix = calculate_similarity_scores(vectors_df)

    recommend_articles_func = build_recommendation_system(vectors_df, similarity_matrix)

    article_id = 123
    recommended_articles = recommend_articles_func(article_id)
    print("Recommended articles:", recommended_articles)
