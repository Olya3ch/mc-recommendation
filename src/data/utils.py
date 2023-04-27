import nltk
import rowordnet as rwn
import re

nltk.download("stopwords")
nltk.download("punkt")

rown = rwn.RoWordNet()


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
        synsets = rown.synsets(stem)
        for synset in synsets:
            if isinstance(synset, rwn.Synset):
                for lemma in synset.lemmas():
                    synonyms[lemma.name()] = stem

    keywords = [(token, synonyms.get(stem, "")) for token, stem in zip(tokens, stems)]

    return keywords


def create_article_from_hit(hit):
    article = {
        "id": hit["_id"],
        "title": hit["_source"].get("post_title", ""),
        "keywords": get_keywords_in_romanian(hit["_source"].get("post_content", "")),
    }
    if "category" in hit["_source"]["terms"]:
        for category in hit["_source"]["terms"]["category"]:
            if "name" in category:
                article["category"] = category["name"]
    return article
