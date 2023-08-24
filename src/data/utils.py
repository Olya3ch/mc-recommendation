import nltk
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("omw-1.4")
nltk.download("wordnet")


def get_synonyms(word):
    synonyms = set()
    for synset in wordnet.synsets(word, lang="ron"):
        for lemma in synset.lemmas(lang="ron"):
            synonyms.add(lemma.name())
    return list(synonyms)


def preprocess_text(text):
    filtered_text = re.sub(r"<.*?>", "", text)
    filtered_text = re.sub(r"http\S+", "", filtered_text)

    tokens = nltk.word_tokenize(filtered_text)

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("romanian"))

    filtered_tokens = []
    for token in tokens:
        if token not in string.punctuation and not token.isdigit():
            token = re.sub(r"[^\w\s]", "", token)
            lemma = lemmatizer.lemmatize(token.lower())
            if (
                lemma
                and lemma not in stop_words
                and not re.match(r"^[a-z0-9_]+$", lemma)
                and re.match(r"^[^\d]*$", lemma)
            ):
                filtered_tokens.append(lemma)

    return filtered_tokens


def get_keywords_in_romanian(text: str):
    text_tokens = preprocess_text(text)
    tokens = [token for token in text_tokens if len(token) > 3]

    stemmer = nltk.stem.SnowballStemmer("romanian")
    stems = [stemmer.stem(token) for token in tokens]

    synonyms = {}
    for stem in stems:
        synonyms[stem] = get_synonyms(stem)

    keywords = [token.lower() for token in tokens]
    for stem, syns in synonyms.items():
        if syns:
            keywords.append(stem)
            keywords.extend(syns)

    return list(set(keywords))


def create_article_from_hit(hit):
    source = hit["_source"]
    title = source.get("post_title", "")

    content_keywords = get_keywords_in_romanian(source.get("post_content", ""))
    title_keywords = get_keywords_in_romanian(title)
    keywords = title_keywords + content_keywords

    categories = []
    if "terms" in source and "category" in source["terms"]:
        categories = [
            category["slug"]
            for category in source["terms"]["category"]
            if "slug" in category
        ]

    author = source["post_author"]["login"].lower() if "post_author" in source else ""

    article = {
        "id": hit["_id"],
        "title": title,
        "author": author,
        "category": categories,
        "keywords": keywords,
    }
    return article
