from os import environ as env
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

es = Elasticsearch(
    cloud_id=env["ELASTIC_CLOUD_ID"],
    http_auth=(env["ELASTIC_USERNAME"], env["ELASTIC_PASSWORD"]),
)


def get_result_of_a_language(language: str, page_size: int, page_number: int):
    query = {
        "size": page_size,
        "from": (page_number - 1) * page_size,
        "query": {
            "bool": {
                "must": [
                    {"match": {"post_lang": language}},
                    {"match": {"post_status": "publish"}},
                ]
            }
        },
    }
    return es.search(index="moldovacrestinamd-post-1", body=query)
