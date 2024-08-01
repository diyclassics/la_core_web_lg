import spacy
from spacy.language import Language
from typing import List
from spacy.util import registry, compile_suffix_regex

que_exceptions = []  # type: List[str]

# quisque / quique
que_exceptions += [
    "quisque",
    "quidque",
    "quicque",
    "quodque",
    "cuiusque",
    "cuique",
    "quemque",
    "quamque",
    "quoque",
    "quaque",
    "quique",
    "quaeque",
    "quorumque",
    "quarumque",
    "quibusque",
    "quosque",
    "quasque",
]

# uterque
que_exceptions += [
    "uterque",
    "utraque",
    "utrumque",
    "utriusque",
    "utrique",
    "utrumque",
    "utramque",
    "utroque",
    "utraque",
    "utrique",
    "utraeque",
    "utrorumque",
    "utrarumque",
    "utrisque",
    "utrosque",
    "utrasque",
]

# quiscumque
que_exceptions += [
    "quicumque",
    "quidcumque",
    "quodcumque",
    "cuiuscumque",
    "cuicumque",
    "quemcumque",
    "quamcumque",
    "quocumque",
    "quacumque",
    "quicumque",
    "quaecumque",
    "quorumcumque",
    "quarumcumque",
    "quibuscumque",
    "quoscumque",
    "quascumque",
]

# unuscumque
que_exceptions += [
    "unusquisque",
    "unaquaeque",
    "unumquodque",
    "unumquidque",
    "uniuscuiusque",
    "unicuique",
    "unumquemque",
    "unamquamque",
    "unoquoque",
    "unaquaque",
]

# plerusque
que_exceptions += [
    "plerusque",
    "pleraque",
    "plerumque",
    "plerique",
    "pleraeque",
    "pleroque",
    "pleramque",
    "plerorumque",
    "plerarumque",
    "plerisque",
    "plerosque",
    "plerasque",
]

# misc
que_exceptions += [
    "absque",
    "abusque",
    "adaeque",
    "adusque",
    "aeque",
    "antique",
    "atque",
    "circumundique",
    "conseque",
    "cumque",
    "cunque",
    "denique",
    "deque",
    "donique",
    "hucusque",
    "inique",
    "inseque",
    "itaque",
    "longinque",
    "namque",
    "neque",
    "oblique",
    "peraeque",
    "praecoque",
    "propinque",
    "qualiscumque",
    "quandocumque",
    "quandoque",
    "quantuluscumque",
    "quantumcumque",
    "quantuscumque",
    "quinque",
    "quocumque",
    "quomodocumque",
    "quomque",
    "quotacumque",
    "quotcumque",
    "quotienscumque",
    "quotiensque",
    "quotusquisque",
    "quousque",
    "relinque",
    "simulatque",
    "torque",
    "ubicumque",
    "ubique",
    "undecumque",
    "undique",
    "usque",
    "usquequaque",
    "utcumque",
    "utercumque",
    "utique",
    "utrimque",
    "utrique",
    "utriusque",
    "utrobique",
    "utrubique",
]


@Language.component("normer")
def normer(doc):
    def norm(text):
        return (
            text.replace("v", "u").replace("j", "i").replace("V", "U").replace("J", "I")
        )

    for token in doc:
        token.norm_ = norm(token.norm_)
    return doc


@registry.callbacks("customize_tokenizer")
def make_customize_tokenizer():
    def customize_tokenizer(nlp):
        suffixes = nlp.Defaults.suffixes + [
            "que",
            "qve",
        ]
        suffix_regex = compile_suffix_regex(suffixes)
        nlp.tokenizer.suffix_search = suffix_regex.search

        for item in que_exceptions:
            nlp.tokenizer.add_special_case(item, [{"ORTH": item}])
            nlp.tokenizer.add_special_case(item.lower(), [{"ORTH": item.lower()}])
            nlp.tokenizer.add_special_case(item.title(), [{"ORTH": item.title()}])
            nlp.tokenizer.add_special_case(item.upper(), [{"ORTH": item.upper()}])

    return customize_tokenizer


# ----- lookup_lemmatizer ----- #
from spacy.language import Language
from spacy.lookups import load_lookups
from spacy.tokens import Token
from spacy.lookups import Lookups
import string

blank_nlp = spacy.blank("la")
lookups = Lookups()


lookups_data = load_lookups(lang=blank_nlp.vocab.lang, tables=["lemma_lookup"])
LOOKUPS = lookups_data.get_table("lemma_lookup")

Token.set_extension(
    "predicted_lemma", default=None, force=True
)  # TODO: test that this works


@Language.component(name="lookup_lemmatizer")
def make_lookup_lemmatizer_function(doc):
    for token in doc:
        token._.predicted_lemma = token.lemma_

        # Handle punctuation
        if token.text in string.punctuation:
            token.lemma_ = token.text
            token.pos_ = "PUNCT"
            token.tag_ = "punc"

        # Handle "que" enclitics
        if token.text == "que" and (
            token.pos_ == "CCONJ" or token.tag_ == "conjunction"
        ):
            token.lemma_ = token.text

        # Lookup lemmatizer

        token.lemma_ = LOOKUPS.get(token.text, token.lemma_)

        # Better handle capitalization
        if token.text[0].isupper() and token.text not in LOOKUPS:
            token.lemma_ = LOOKUPS.get(token.text.lower(), token.lemma_)
    return doc


# ---------- #
