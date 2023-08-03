def create_mapping_between_article_id_and_index(articles):
    return {article_id: index for index, article_id in enumerate(articles["id"])}
