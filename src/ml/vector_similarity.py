import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.preprocessing import normalize


def vectorize_features(df):
    vectorizer = TfidfVectorizer(
        max_features=1000, min_df=100, max_df=0.4, sublinear_tf=True
    )
    features = vectorizer.fit_transform(df)

    vectors_df = pd.DataFrame(
        features.todense(), columns=vectorizer.get_feature_names_out()
    )

    return vectors_df


def calculate_similarity_matrix(articles_df):
    combined_features = articles_df["title"] + articles_df["content"]

    vectors_df = vectorize_features(combined_features)

    n_topics = 10
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=10)
    topic_matrix = lda.fit_transform(vectors_df)

    normalized_topic_matrix = normalize(topic_matrix)
    similarity_matrix = cosine_similarity(normalized_topic_matrix)
    return similarity_matrix


def calculate_similarity_scores_dict(
    similarity_matrix, article_id, mapped_ids, recommendations
):
    similarity_scores_dict = {}
    for recommended_id in recommendations:
        similarity_score = similarity_matrix[mapped_ids[article_id]][
            mapped_ids[recommended_id]
        ]
        similarity_scores_dict[recommended_id] = similarity_score
    return similarity_scores_dict
