def article_id_mapping(articles):
    return {article_id: index for index, article_id in enumerate(articles["id"])}
