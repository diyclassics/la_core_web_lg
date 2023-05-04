import re
import pandas as pd
from collections import namedtuple

df = pd.read_csv("assets/preprocess/ud-parse-temp.tsv", sep="\t", low_memory=False)

# A. Convert UPOS

# A.1. Drop X for known words

from collections import defaultdict, Counter

upos_multi = defaultdict(list)

for word, uposs in zip(df["lemma"], df["upos"]):
    upos_multi[word].append(uposs)

upos_multi = {k: Counter(v) for k, v in upos_multi.items()}


def update_upos_multi_x(row):
    if row["upos"] == "X" and row["lemma"] in upos_multi.keys():
        row["upos"] = upos_multi[row["lemma"]].most_common(1)[0][0]
    return row["upos"]


# A.2. Drop with review, single
# This section consists of an ongoing lists of words for review for UPOS; a minimal, (ideally) consistent set is retained, and all others are marked with an underscore (i.e. )

upos_single = {
    "sum": ["AUX"],
    "in": ["ADP"],
    "non": ["PART"],
    "per": ["ADP"],
    "ab": ["ADP"],
    "dico": ["VERB"],
    "uos": ["PRON"],
    "de": ["ADP"],
    "deus": ["NOUN"],
    "ex": ["ADP"],
    "sed": ["CCONJ"],
    "habeo": ["VERB"],
    "si": ["SCONJ"],
    "possum": ["VERB"],
    "sicut": ["ADV"],
    "quia": ["SCONJ"],
    "-": ["PUNCT"],
    "_": ["_"],
    "dementia": ["NOUN"],
    "ecce": ["INTJ"],
    "en": ["INTJ"],
    "equidem": ["ADV"],
    "heu": ["INTJ"],
    "met": ["PART"],
    "num": ["PART"],
    "o": ["INTJ"],
    "ouum": ["NOUN"],
    "quidem": ["ADV"],
    "quoque": ["ADV"],
    "trecenti": ["NUM"],
    "uiii": ["NUM"],
    "x": ["NUM"],
    "xi": ["NUM"],
    "non": ["PART"],
    "omnis": ["ADJ"],
    "suus": ["ADJ"],
    "meus": ["ADJ"],
    "tuus": ["ADJ"],
    "noster": ["ADJ"],
    "uester": ["ADJ"],
    "an": ["PART"],
    "aliquis": ["PRON"],
    "aliqui": ["PRON"],
    "que": ["CCONJ"],
    "aut": ["CCONJ"],
    "greek.expression": ["X"],
    "terra": ["NOUN"],
    "quis": ["PRON"],
    "finis": ["NOUN"],
    "causa": ["NOUN"],
    "casa": ["NOUN"],
    "presbyter": ["NOUN"],
    "multus": ["ADJ"],
    "notarius": ["NOUN"],
    "moueo": ["VERB"],
    "bonum": ["NOUN"],
    "humanus": ["ADJ"],
    "quondam": ["ADV"],
    "totus": ["ADJ"],
    "nullus": ["ADJ"],
    "Iesus": ["PROPN"],
    "proprius": ["ADJ"],
    "naturalis": ["ADJ"],
    "manifestus": ["ADJ"],
    "successor": ["NOUN"],
    "quantum": ["ADV"],
    "alter": ["ADJ"],
    "mitto": ["VERB"],
    "integer": ["ADJ"],
    "scilicet": ["ADV"],
    "huiusmodi": ["ADV"],
    "possibilis": ["ADJ"],
    "uerus": ["ADJ"],
    "ultimus": ["ADJ"],
    "item": ["ADV"],
    "tunc": ["ADV"],
    "malum": ["NOUN"],
    "qualiter": ["ADV"],
    "domus": ["NOUN"],
    "intelligibilis": ["ADJ"],
    "impossibilis": ["ADJ"],
    "diuersus": ["ADJ"],
    "intellectualis": ["ADJ"],
    "simul": ["ADV"],
    "tam": ["ADV"],
    "amplus": ["ADJ"],
    "bene": ["ADV"],
    "licet": ["VERB"],
    "missus": ["NOUN"],
    "similis": ["ADJ"],
    "similiter": ["ADV"],
    "infinitus": ["ADJ"],
    "relinquo": ["VERB"],
    "quoniam": ["SCONJ"],
    "mensis": ["NOUN"],
    "sui": ["PRON"],
    "malus": ["ADJ: NOUN"],
    "uniuersalis": ["ADJ"],
    "beatus": ["ADJ; NOUN"],
    "subiectum": ["NOUN"],
    "publicus": ["ADJ; NOUN"],
    "uterque": ["DET"],
    "populus": ["NOUN"],
    "corporalis": ["ADJ"],
    "aqua": ["NOUN"],
    "rego": ["VERB"],
    "puto": ["VERB"],
    "atque": ["CCONJ"],
    "solus": ["ADJ"],
    "tres": ["NUM"],
    "ille": ["DET"],
    "iste": ["DET"],
}


def update_upos_single(row):
    if row["lemma"] in upos_single.keys():
        row["upos"] = upos_single[row["lemma"]][0]
    return row["upos"]


df["upos"] = df.apply(update_upos_single, axis=1)

upos_multi = {
    "et": {"CCONJ": "CCONJ", "SCONJ": "CCONJ", "ADP": "_", "ADV": "ADV", "ADJ": "_"},
    "qui": {
        "PRON": "PRON",
        "DET": "PRON",
        "SCONJ": "PRON",
        "NOUN": "_",
        "ADJ": "_",
        "ADV": "ADV",
    },
    "is": {"PRON": "PRON", "ADJ": "DET", "DET": "DET"},
    "ad": {"ADP": "ADP", "ADV": "ADP", "SCONJ": "ADP"},
    "hic": {"DET": "DET", "ADV": "ADV", "PRON": "DET", "ADJ": "DET"},
    "quod": {"SCONJ": "SCONJ", "PRON": "PRON", "ADV": "ADV", "ADP": "_"},
    "autem": {"PART": "CCONJ", "CCONJ": "CCONJ", "ADV": "ADV"},
    "ut": {"SCONJ": "SCONJ", "ADV": "ADV", "ADP": "_", "CCONJ": "SCONJ"},
    "ipse": {"PRON": "PRON", "ADJ": "DET", "DET": "DET"},
    "cum": {"SCONJ": "SCONJ", "ADP": "ADP", "CCONJ": "SCONJ", "ADV": "SCONJ"},
    "uel": {"CCONJ": "CCONJ", "SCONJ": "CCONJ", "ADV": "ADV"},
    "enim": {"PART": "PART", "CCONJ": "PART", "SCONJ": "PART", "ADV": "ADV"},
    "igitur": {"PART": "PART", "CCONJ": "PART", "SCONJ": "PART", "ADV": "ADV"},
    "etiam": {"ADV": "ADV", "CCONJ": "CCONJ", "SCONJ": "CCONJ"},
    "ne": {"SCONJ": "PART", "PART": "PART", "ADV": "ADV", "INTJ": "_"},
    "nam": {"PART": "PART", "CCONJ": "PART", "ADV": "ADV"},
    "itaque": {"PART": "PART", "SCONJ": "PART", "ADV": "ADV"},
    "etenim": {"PART": "PART", "SCONJ": "PART", "ADV": "ADV"},
    "uiii": {"NUM": "NUM", "ADV": "NUM"},
    "namque": {"PART": "PART", "CCONJ": "PART", "ADV": "ADV"},
    "siquidem": {"PART": "PART", "SCONJ": "PART", "ADV": "ADV"},
    "nempe": {"SCONJ": "PART", "PART": "PART"},
    "secundum": {"ADP": "ADP", "ADV": "ADV", "SCONJ": "ADV"},
    "unus": {"DET": "ADJ", "NUM": "NUM", "ADV": "NUM", "ADJ": "ADJ"},
    "diuinus": {"ADJ": "ADJ", "NOUN": "NOUN", "ADV": "ADJ"},
    "ago": {"VERB": "VERB", "NOUN": "NOUN", "AUX": "VERB"},
    "bonus": {"ADJ": "ADJ", "NOUN": "NOUN", "ADV": "_"},
    "quidam": {"DET": "DET", "PRON": "PRON", "ADJ": "DET"},
    "quam": {"SCONJ": "SCONJ", "CCONJ": "SCONJ", "ADV": "ADV", "ADP": "_", "PRON": "_"},
    "idem": {"DET": "DET", "ADV": "ADV", "PRON": "PRON", "ADJ": "_"},
    "propter": {"ADP": "ADP", "SCONJ": "ADV"},
    "nam": {"PART": "PART", "CCONJ": "PART", "ADV": "ADV"},
    "magnus": {"ADJ": "ADJ", "NOUN": "NOUN", "ADV": "_", "PROPN": "PROPN"},
    "inter": {"ADP": "ADP", "SCONJ": "_", "ADV": "ADV"},
    "post": {"ADP": "ADP", "ADV": "ADV", "SCONJ": "_", "ADJ": "_"},
    "duo": {"NUM": "NUM", "NOUN": "_", "ADJ": "NUM"},
    "nihil": {"PRON": "NOUN", "ADV": "ADV", "NOUN": "NOUN", "DET": "NOUN", "ADJ": "_"},
    "latus": {"NOUN": "NOUN", "ADV": "_", "ADJ": "ADJ", "ADP": "_"},
    "ante": {"ADP": "ADP", "ADV": "ADV", "SCONJ": "_"},
    "quicumque": {"DET": "ADJ", "PRON": "PRON", "ADJ": "ADJ"},
    "dum": {"SCONJ": "SCONJ", "ADP": "_", "ADV": "_", "CCONJ": "SCONJ"},
    "malus": {"ADJ": "ADJ", "NOUN": "NOUN", "ADV": "ADJ"},
    "beatus": {"ADJ": "ADJ", "NOUN": "NOUN", "VERB": "ADJ"},
    "publicus": {"ADJ": "ADJ", "ADV": "ADJ", "NOUN": "NOUN"},
    "paruus": {"ADV": "ADJ", "ADJ": "ADJ", "NOUN": "NOUN", "DET": "ADJ"},
}


def update_upos_multi(row):
    if row["lemma"] in upos_multi.keys():
        updates = upos_multi[row["lemma"]]
        row["upos"] = updates.get(row["upos"], "_")
    return row["upos"]


df["upos"] = df.apply(update_upos_multi, axis=1)


# # B. Normalize feats

# B.1. feats_Gender: 'Masc', 'Fem', Neut', nan
# There are annotations in feats_Gender that are comma-separated, e.g. "Fem,Neut"; return first in list


def split_gender(entry):
    if pd.isna(entry):
        return None
    if "," in entry:
        return entry.split(",")[0]
    else:
        return entry


df["feats_Gender"] = df["feats_Gender"].apply(lambda x: split_gender(x))

# B.2. feats_Number: 'Sing', 'Plur', nan
# OK

# B.3. feats_Case: 'Nom', 'Gen', 'Dat', 'Acc', 'Abl', 'Voc', 'Loc', nan
# OK

# B.4. feats_Person: '1', '2', '3', nan
# Needs to be kept as string


def update_person(entry):
    if pd.isna(entry):
        return None
    return str(int(entry))


df["feats_Person"] = df["feats_Person"].apply(lambda x: update_person(x))

# B.5. feats_Tense: 'Pqp', 'Past', 'Pres', 'Fut', nan
# OK

# B.6. feats_Mood: 'Ind', 'Imp', 'Sub', nan
# OK

# B.7. feats_Voice: 'Act', 'Pass', nan
# OK

# B.8 Combine features as necessary for form

Noun = namedtuple("Noun", ["Gender", "Number", "Case"])
Verb = namedtuple(
    "Verb", ["Person", "Number", "Tense", "Mood", "Voice", "Gender", "Case"]
)


def get_pos_feats(row):
    if (
        row["upos"] == "NOUN"
        or row["upos"] == "PROPN"
        or row["upos"] == "PRON"
        or row["upos"] == "ADJ"
        or row["upos"] == "DET"
    ):
        return Noun(row["feats_Gender"], row["feats_Number"], row["feats_Case"])
    elif row["upos"] == "VERB":
        return Verb(
            row["feats_Person"],
            row["feats_Number"],
            row["feats_Tense"],
            row["feats_Mood"],
            row["feats_Voice"],
            row["feats_Gender"],
            row["feats_Case"],
        )
    else:
        return None


df["feats"] = df.apply(get_pos_feats, axis=1)

# C. Normalize xpos
# Difficult to map as annotations are all different; using Treetagger tagset as guide for now
# cf. https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/tagsetdocs.txt


def extract_treebank_name(treebank):
    # e.g. assets/UD_Latin-ITTB/la_ittb-ud-test.conllu
    treebank = re.match(r".*UD_Latin-(.*)/.*", treebank).group(1)
    return treebank.lower()


df["treebank"] = df["file"].apply(lambda x: extract_treebank_name(x))


def map_xpos(row):
    if row["treebank"] == "perseus":
        perseus_map = {
            "_": "_",
            "n": "noun",
            "a": "adjective",
            "m": "number",
            "v": "verb",
            "t": "verb",  # participle
            "p": "pronoun",
            "l": "adverb",
            "c": "conjunction",
            "g": "particle",
            "i": "interjection",
            "e": "interjection",
            "d": "adverb",
            "r": "preposition",
            "x": "unknown",
            "-": "unknown",
            "u": "punc",
        }
        update = perseus_map.get(row["xpos"][0], "_")
        return update
    elif row["treebank"] == "proiel":
        proiel_map = {
            "_": "_",
            "Nb": "noun",
            "F-": "noun",
            "Ne": "proper_noun",
            "A-": "adjective",
            "Ma": "number",
            "Mo": "adjective",
            "Py": "adjective",
            "V-": "verb",
            "N-": "verb",
            "Pd": "pronoun",
            "Px": "pronoun",
            "Pi": "pronoun",
            "Pp": "pronoun",
            "Pk": "pronoun",
            "Ps": "pronoun",
            "Pt": "pronoun",
            "Pc": "pronoun",
            "Pr": "pronoun",
            "S-": "adverb",
            "C-": "conjunction",
            "G-": "conjuntion",
            "I-": "interjection",
            "Df": "adverb",
            "Du": "adverb",
            "Dq": "adverb",
            "R-": "preposition",
            "X-": "unknown",
            "PUNCT": "punc",
        }
        update = proiel_map.get(row["xpos"], "_")

        return update
    elif row["treebank"] == "llct":
        llct_map = {
            "_": "_",
            "Propn": "proper_noun",
            "Punc": "punc",
            "SYM": "punc",
            "a": "adjective",
            "c": "conjunction",
            "d": "adverb",
            "e": "interjection",
            "m": "number",
            "n": "noun",
            "p": "pronoun",
            "r": "preposition",
            "t": "verb",  # participle
            "v": "verb",
        }
        try:
            update = llct_map.get(row["xpos"].split("|")[0], "_")
        except:
            update = "_"

        return update
    elif row["treebank"] == "ittb":
        ittb_upos_map = {
            "_": "_",
            "PART": "particle",
            "ADP": "preposition",
            "PRON": "pronoun",
            "PUNCT": "punc",
            "SCONJ": "conjunction",
            "ADV": "adverb",
            "DET": "adjective",  # determiner REVIEW—comp. ipse vs. suus; pronoun vs. adjective
            "AUX": "verb",
            "NOUN": "noun",
            "CCONJ": "conjunction",
            "ADJ": "adjective",
            "VERB": "verb",
            "PROPN": "proper_noun",
            "NUM": "number",
            "X": "unknown",
        }
        update = ittb_upos_map.get(row["upos"], "_")

        return update
    elif row["treebank"] == "udante":
        udante_map = {
            "_": "_",
            "9": "particle",
            "0": "conjunction",
            "P": "punc",
            "S": "proper_noun",
            "s": "noun",
            "c": "conjunction",
            "d": "adjective",  # determiner REVIEW—comp. ipse vs. suus; pronoun vs. adjective
            "p": "pronoun",
            "r": "adverb",
            "v": "verb",
            "a": "adjective",
        }
        try:
            update = udante_map.get(row["xpos"][0], "_")
        except:
            update = "_"

        return update
    else:
        return "_"


df["xpos"] = df.apply(lambda x: map_xpos(x), axis=1)
df["xpos"] = df.apply(
    lambda x: "number" if x["upos"] == "NUM" else x["xpos"], axis=1
)  # UDANTE numbers from UPOS
df["xpos"] = df.apply(
    lambda x: "verb" if x["upos"] == "VERB" else x["xpos"], axis=1
)  # UDANTE participle from UPOS


def get_perseus_proper_noun(row):
    if row["treebank"] == "perseus":
        if row["xpos"] == "noun" and row["lemma"][0].isupper():
            return "proper_noun"
    return row["xpos"]


df["xpos"] = df.apply(lambda x: get_perseus_proper_noun(x), axis=1)
df["misc"] = "_"

df.to_csv("assets/preprocess/ud-parse-temp.tsv", sep="\t", index=False)
df[
    [
        "id",
        "form",
        "lemma",
        "upos",
        "xpos",
        "feats",
        "head",
        "deprel",
        "deps",
        "misc",
        "file",
        "sent_id",
        "text",
        "reference",
        "newdoc id",
        "source",
        "citation_hierarchy",
    ]
].to_pickle("assets/preprocess/ud-parse-temp.pkl")
