#coding: utf-8

NOT_AVAILABLE = "n/a"
UNMATCHED = "unmatched"
CURRENT_DIRECTORY = "/home/tural/not_univer/experiments/brat_statistics/sources"
ALLOWED_MISTAKES = [
    "Content",
        "content_reference",
            "omission",
            "non-sense",
        "content_cohesion",
            "theme",
            "rheme",
            "connector",
            "logic",
        "content_pragmatics",
            "register",
            "use",
    "Language",
    "Language_lexical",
        "lexical",
        "combinability",
    "Language_morphology",
    "Language_syntax",
        "incomplete_structure",
        "ungrammatical",
        "word_order",
    "Laguage_spelling",
        "capitals",
    "Language_punctuation",
    "Delete",
    "All:",
    "Content:",
    "Language:"
]

LANG_MISTAKES = {
    "Language",
    "language_lexical",
        "choice-of-word",
        "combinability",
    "language_morphology",
        "wrong_wordform",
    "language_syntax",
        "incomplete_structure",
        "ungrammatical",
        "word_order",
        "preposition",
    "language_spelling",
        "capitals",
        "typo",
    "language_punctuation",
    "Delete"
}

CONTENT_MISTAKES = {
    "Content",
    "content_reference",
        "omission",
        "distortion",
        "nonsense",
        "unclear",
    "content_cohesion",
        "ThemeRheme",
        "logic",
    "content_pragmatics",
        "register"
}
