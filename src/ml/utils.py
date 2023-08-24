def article_id_mapping(articles):
    return {article_id: index for index, article_id in enumerate(articles["id"])}


def get_article_by_id(article_id, articles_df):
    article = articles_df[articles_df["id"] == article_id].iloc[0]
    return {
        "id": article["id"],
        "title": article["title"],
        "author": article["author"],
        "category": article["category"],
        "keywords": article["keywords"],
    }
