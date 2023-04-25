from os import environ as env
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from pprint import pprint

load_dotenv()

es = Elasticsearch(
    cloud_id=env["ELASTIC_CLOUD_ID"],
    http_auth=(env["ELASTIC_USERNAME"], env["ELASTIC_PASSWORD"]),
)


def get_result_of_a_language(language: str):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"post_lang": language}},
                    {"match": {"post_status": "publish"}},
                ]
            }
        }
    }
    return es.search(index="moldovacrestinamd-post-1", body=query)


ro_result = get_result_of_a_language("ro")

for hit in ro_result["hits"]["hits"]:
    article = {
        "title": hit["_source"]["post_title"],
    }
    if "category" in hit["_source"]["terms"]:
        for category in hit["_source"]["terms"]["category"]:
            if "name" in category:
                article["category"] = category["name"]
    pprint(article)
