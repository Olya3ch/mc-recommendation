import pandas as pd


def filter_similar_articles(
    similarities, article_idx, input_article, articles_df, min_similarity
):
    article = articles_df.loc[article_idx]
    return (
        similarities[article_idx] >= min_similarity
        and article["author"] == input_article["author"]
        and (
            not pd.isna(article["category"])
            and any(
                category in input_article["category"]
                for category in article["category"]
            )
        )
    )


def get_recommended_article_ids(
    similar_articles,
    similarities,
    article_id_mapping,
    articles_df,
    input_article,
    min_similarity,
):
    recommended_article_ids = []
    inverted_mapping = {v: k for k, v in article_id_mapping.items()}

    for article_idx in similar_articles:
        if filter_similar_articles(
            similarities, article_idx, input_article, articles_df, min_similarity
        ):
            recommended_article_ids.append(inverted_mapping[article_idx])

    return recommended_article_ids


def recommend_articles(
    article_id, similarity_matrix, article_id_mapping, articles_df, min_similarity=0.8
):
    index = article_id_mapping[article_id]
    input_article = articles_df.loc[index]

    similarities = similarity_matrix[index]
    similar_articles = sorted(
        range(len(similarities)), key=lambda i: similarities[i], reverse=True
    )

    recommended_article_ids = get_recommended_article_ids(
        similar_articles,
        similarities,
        article_id_mapping,
        articles_df,
        input_article,
        min_similarity,
    )

    return [id for id in recommended_article_ids if id != article_id]
