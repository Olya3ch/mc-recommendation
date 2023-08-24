import csv
from data.es_queries import get_result_of_a_language
from data.utils import create_article_from_hit


def get_articles_info_for_a_page(language: str, page_size: int, page_number: int):
    result = get_result_of_a_language(language, page_size, page_number)
    if "hits" not in result or "hits" not in result["hits"]:
        return []
    articles = [create_article_from_hit(hit) for hit in result["hits"]["hits"]]
    return articles


def get_all_articles_info(language: str, page_size: int):
    page_number = 1
    all_articles = []
    while True:
        articles = get_articles_info_for_a_page(language, page_size, page_number)
        if not articles:
            break
        all_articles.extend(articles)
        page_number += 1
    return all_articles


def save_articles_info_to_csv(language: str, filename: str):
    try:
        articles = get_all_articles_info(language, 100)
        if not articles:
            print("No articles found")
            return
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "id",
                "title",
                "author",
                "category",
                "keywords",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for article in articles:
                writer.writerow(article)
        print(f"Saved {len(articles)} articles to {filename}")
    except Exception as e:
        print(f"Error saving articles to CSV: {e}")
