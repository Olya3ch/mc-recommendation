import csv
from data.pagination import get_all_articles_info


def save_articles_info_to_csv(language: str, filename: str):
    articles = get_all_articles_info(language, 100)
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "title", "keywords", "category"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
    print(f"Saved {len(articles)} articles to {filename}")


print(save_articles_info_to_csv("ro", "ro.csv"))
