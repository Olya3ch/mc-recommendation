import nltk
import rowordnet as rwn
import re


def get_keywords_in_romanian(text: str):
    html_tags_pattern = re.compile(r"<.*?>")
    filtered_text = re.sub(html_tags_pattern, "", text)

    nltk.download("stopwords")
    nltk.download("punkt")

    rown = rwn.RoWordNet()

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
