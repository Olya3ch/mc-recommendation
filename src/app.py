from flask import Flask, request, jsonify
import pandas as pd

from src.ml.main import main

app = Flask(__name__)
# import connexion

# app = connexion.App(__name__, specification_dir="./")
# app.add_api("./openapi.yaml")


@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    article_id = int(request.args.get("article_id"))
    limit = int(request.args.get("limit"))
    print(limit)

    recommendations_ids = main(article_id)

    recommendations = []
    for rec_article_id in recommendations_ids:
        recommendations.append({"article_id": rec_article_id})

    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)
