import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.preprocessing import normalize


def calculate_similarity_scores(vectors_df):
    n_topics = 10
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=30)
    topic_matrix = lda.fit_transform(vectors_df)

    normalized_topic_matrix = normalize(topic_matrix)
    similarity_matrix = cosine_similarity(normalized_topic_matrix)
    return similarity_matrix


def recommend_articles(
    article_id, similarity_matrix, article_id_mapping, articles_df, min_similarity=0.8
):
    inverted_mapping = {v: k for k, v in article_id_mapping.items()}
    index = article_id_mapping[article_id]
    input_article = articles_df.loc[index]

    similarities = similarity_matrix[index]

    similar_articles = sorted(
        range(len(similarities)), key=lambda i: similarities[i], reverse=True
    )

    recommended_article_ids = []
    for article_idx in similar_articles:
        article = articles_df.loc[article_idx]
        if similarities[article_idx] >= min_similarity and (
            article["author"] == input_article["author"]
            and (
                not pd.isna(article["category"])
                and any(
                    category in input_article["category"]
                    for category in article["category"]
                )
            )
        ):
            recommended_article_ids.append(inverted_mapping[article_idx])

    return [id for id in recommended_article_ids if id != article_id]
