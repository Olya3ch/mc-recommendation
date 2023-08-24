import pandas as pd
from src.ml.utils import article_id_mapping
from src.ml.recommendation import recommend_articles
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

    recommended_articles = []
    for recommended_id, similarity_score in similarity_scores_dict.items():
        article_info = articles_df.loc[mapped_ids[recommended_id]]
        recommended_articles.append(
            {
                "article_id": recommended_id,
                "similarity_score": similarity_score,
                "title": article_info["title"],
                "category": article_info["category"],
                "author": article_info["author"],
            }
        )

    sorted_recommendations = sorted(
        recommended_articles,
        key=lambda x: x["similarity_score"],
        reverse=True,
    )

    return sorted_recommendations, articles_df


if __name__ == "__main__":
    article_id = 329755
    recommended_articles = main(article_id)
    for article in recommended_articles[:10]:
        print("Article ID:", article["article_id"])
        print("Similarity Score:", article["similarity_score"])
        print("Title:", article["title"])
        print("Category:", article["category"])
        print("Author:", article["author"])
        print("========================")
    print("Length of recommendations:", len(recommended_articles))
