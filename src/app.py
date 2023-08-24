from flask import Flask, render_template, request, redirect, url_for
from src.ml.main import main
from src.ml.utils import get_article_by_id

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        article_id = int(request.form.get("article_id"))
        return redirect(url_for("show_recommendations", article_id=article_id))
    return render_template("index.html")


@app.route("/recommendations/<int:article_id>")
def show_recommendations(article_id):
    try:
        recommended_articles, articles_df = main(article_id)
        input_article = get_article_by_id(article_id, articles_df)

        return render_template(
            "recommendations.html",
            recommendations=recommended_articles,
            input_article=input_article,
        )
    except Exception as e:
        print(f"Error processing recommendations: {e}")


if __name__ == "__main__":
    app.run(debug=True)
