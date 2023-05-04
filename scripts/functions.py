import spacy
from spacy.language import Language
import string
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


@Language.component("lemma_fixer")
def lemma_fixer(doc):

    for token in doc:
        if token.text == "que" and (
            token.pos_ == "CCONJ" or token.tag_ == "conjunction"
        ):
            token.lemma_ = token.text
        if token.text in string.punctuation:
            token.lemma_ = token.text
            token.pos_ = "PUNCT"
            token.tag_ = "punc"
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
