import csv
from data.elasticsearch import get_result_of_a_language
from data.utils import get_keywords_in_romanian


def get_articles_info_for_a_page(language: str, page_size: int, page_number: int):
    result = get_result_of_a_language(language, page_size, page_number)
    articles = []
    for hit in result["hits"]["hits"]:
        article = {
            "id": hit["_id"],
            "title": hit["_source"]["post_title"],
            "keywords": get_keywords_in_romanian(hit["_source"]["post_content"]),
        }
        if "category" in hit["_source"]["terms"]:
            for category in hit["_source"]["terms"]["category"]:
                if "name" in category:
                    article["category"] = category["name"]
        articles.append(article)
    return articles


def get_all_articles_info(language: str, page_size: int):
    all_articles = []
    while True:
        result = get_articles_info_for_a_page(language, page_size, page_number)
        articles = result["hits"]["hits"]
        if not articles:
            break
        all_articles.extend(articles)
        page_number += 1
    return all_articles
