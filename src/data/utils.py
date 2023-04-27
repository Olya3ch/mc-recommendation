import nltk
import re

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("omw-1.4")
nltk.download("wordnet")


def get_synonyms(word):
    synonyms = set()
    for synset in nltk.corpus.wordnet.synsets(word, lang="ron"):
        for lemma in synset.lemmas(lang="ron"):
            synonyms.add(lemma.name())
    return list(synonyms)


def get_keywords_in_romanian(text: str):
    html_tags_pattern = re.compile(r"<.*?>")
    filtered_text = re.sub(html_tags_pattern, "", text)

    stop_words = set(nltk.corpus.stopwords.words("romanian"))
    stop_words.update(
        [
            "vasile",
            "filat",
            "pastorul",
            "buna",
            "vestirea",
            "chișinău",
            ".",
            "serviciile",
            "divine",
            "bisericii",
            "loc",
            "duminică",
            ",",
            "14.00",
            "16.00",
            ",",
            "str.ciocârliei",
            "2/8",
            "sectorul",
            "telecentru",
            ":",
            "așa",
            "și",
            "?",
        ]
    )

    tokens = [
        word.lower()
        for word in nltk.word_tokenize(filtered_text)
        if word.lower() not in stop_words
    ]

    stemmer = nltk.stem.SnowballStemmer("romanian")
    stems = [stemmer.stem(token) for token in tokens]

    synonyms = {}
    for stem in stems:
        synonyms[stem] = get_synonyms(stem)

    keywords = [(token, synonyms.get(stem, [])) for token, stem in zip(tokens, stems)]

    return keywords


def create_article_from_hit(hit):
    content_keywords = get_keywords_in_romanian(hit["_source"].get("post_content", ""))
    title_keywords = get_keywords_in_romanian(hit["_source"].get("post_title", ""))
    article = {
        "id": hit["_id"],
        "author": hit["_source"]["post_author"]["display_name"],
        "keywords": content_keywords + title_keywords,
    }
    if "category" in hit["_source"]["terms"]:
        for category in hit["_source"]["terms"]["category"]:
            if "slug" in category:
                article["category"] = category["slug"]
    return article
