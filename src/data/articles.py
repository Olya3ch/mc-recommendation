import csv
from data.queries import get_result_of_a_language
from data.utils import get_keywords_in_romanian


def get_articles_info_for_a_page(language: str, page_size: int, page_number: int):
    result = get_result_of_a_language(language, page_size, page_number)
    if "hits" not in result or "hits" not in result["hits"]:
        return []
    articles = []
    for hit in result["hits"]["hits"]:
        article = {
            "id": hit["_id"],
            "title": hit["_source"].get("post_title", ""),
            "keywords": get_keywords_in_romanian(
                hit["_source"].get("post_content", "")
            ),
        }
        if "category" in hit["_source"]["terms"]:
            for category in hit["_source"]["terms"]["category"]:
                if "name" in category:
                    article["category"] = category["name"]
        articles.append(article)
    return articles


def get_all_articles_info(language: str, page_size: int):
    page_number = 1
    all_articles = []
    while True:
        result = get_articles_info_for_a_page(language, page_size, page_number)
        articles = result["hits"]["hits"]
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
            fieldnames = ["id", "title", "keywords", "category"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for article in articles:
                writer.writerow(article)
        print(f"Saved {len(articles)} articles to {filename}")
    except Exception as e:
        print(f"Error saving articles to CSV: {e}")


print(save_articles_info_to_csv("ro", "data/ro_articles.csv"))
