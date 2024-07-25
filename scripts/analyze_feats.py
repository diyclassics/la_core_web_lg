import os.path
from glob import glob
from tqdm import tqdm
from conllu import parse
import re

UPDATE_PATH = "assets/preprocess"
files = [file for file in glob("assets/preprocess/*.conllu", recursive=True)]
print("\n\nUpdating conllu files for further processing...\n")


def update_feats_tense(token):
    feats = token.get("feats", None)
    if feats:
        if "Tense" in feats:
            if feats["Tense"] == "Pqp":
                feats["Tense"] = "Pqp"
            elif feats["Tense"] == "Pres":
                feats["Tense"] = "Pres"
            elif feats["Tense"] == "Fut":
                aspect = feats.get("Aspect", None)
                if aspect:
                    if aspect == "Perf":
                        feats["Tense"] = "FutPerf"
                    else:
                        feats["Tense"] = "Fut"
                else:
                    feats["Tense"] = "Fut"
            elif feats["Tense"] == "Past":
                aspect = feats.get("Aspect", None)
                if aspect:
                    if aspect == "Imp":
                        feats["Tense"] = "Imp"
                    else:
                        feats["Tense"] = "Perf"
                else:
                    feats["Tense"] = "Perf"
            else:
                pass
    return token


def update_feats_mood(token):
    feats = token.get("feats", None)
    misc = token.get("misc", None)

    def is_infinitive(feats, misc):
        return (feats and feats.get("VerbForm", None) == "Inf") or (
            misc and misc.get("TraditionalMood", None) == "Infinitivum"
        )

    def is_gerund(feats, misc):
        return (feats and feats.get("VerbForm", None) == "Ger") or (
            misc and misc.get("TraditionalMood", None) == "Gerundium"
        )

    def is_gerundive(feats, misc):
        return (feats and feats.get("VerbForm", None) == "Gdv") or (
            misc and misc.get("TraditionalMood", None) == "Gerundivum"
        )

    if is_infinitive(feats, misc):
        token["upos"] = "VERB"
        token["xpos"] = "verb"
        if feats.get("Aspect", None):
            if feats["Aspect"] == "Perf":
                feats["Tense"] = "Perf"
            elif feats["Aspect"] == "Imp":
                feats["Tense"] = "Pres"
            else:
                pass
    elif is_gerund(feats, misc):
        feats["Tense"] = "Fut"
        feats["Voice"] = "Pass"
        feats["VerbForm"] = "Part"
        feats["Mood"] = "Ger"
    elif is_gerundive(feats, misc):
        feats["VerbForm"] = "Part"
        feats["Tense"] = "Fut"
        feats["Voice"] = "Pass"
        feats["Mood"] = "Gdv"
    else:
        pass
    return token


def limit_features(token):
    feats = token.get("feats", None)
    if feats:
        allowed_keys = [
            "Gender",
            "Number",
            "Case",
            "VerbForm",
            "Person",
            "Tense",
            "Mood",
            "Voice",
        ]
        keys_to_delete = [key for key in feats if key not in allowed_keys]
        for key in keys_to_delete:
            del feats[key]

    return token


def update_xpos(treebank, token):
    if treebank == "perseus":
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
        if token.get("xpos", None):
            xpos_initial = token["xpos"][0]
            token["xpos"] = perseus_map.get(xpos_initial, "_")
        else:
            token["xpos"] = "_"

    elif treebank == "proiel":
        proiel_map = {
            "_": "_",
            "Nb": "noun",
            "F-": "_",
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
            "G-": "conjunction",
            "I-": "interjection",
            "Df": "adverb",
            "Du": "adverb",
            "Dq": "adverb",
            "R-": "preposition",
            "X-": "unknown",
            "PUNCT": "punc",
        }
        token["xpos"] = proiel_map.get(token["xpos"], "_")
    elif treebank == "llct":
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
        if token.get("xpos", None):
            token["xpos"] = llct_map.get(token["xpos"].split("|")[0], "_")
        else:
            token["xpos"] = "_"
    elif treebank == "ittb":
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
        token["xpos"] = ittb_upos_map.get(token["upos"], "_")
    elif treebank == "udante":
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

        if token.get("xpos", None):
            token["xpos"] = udante_map.get(token["xpos"][0], "_")
        else:
            token["xpos"] = "_"
    elif treebank == "lasla":
        lasla_map = {
            "ADJ-C": "adjective",
            "ADJ-C1": "adjective",
            "ADJ-C2": "adjective",
            "ADJ-C3": "adjective",
            "ADJ-C4": "adjective",
            "ADJ-C5": "adjective",
            "ADJ-C6": "adjective",
            "ADJ-C7": "adjective",
            "ADJ-D2": "adjective",
            "ADJ-D3": "adjective",
            "ADJ-D4": "adjective",
            "ADP-R": "preposition",
            "ADV-D5": "adverb",
            "ADV-D6": "adverb",
            "ADV-M": "adverb",
            "ADV-N": "adverb",
            "ADV-O": "adverb",
            "ADV-P": "adverb",
            "ADV-Q": "adverb",
            "ADV-T": "adverb",
            "AUX-#": "verb",
            "AUX-B6": "verb",
            "AUX-Z1": "verb",
            "AUX-Z2": "verb",
            "AUX-Z3": "verb",
            "AUX-Z4": "verb",
            "AUX-Z5": "verb",
            "AUX-Z6": "verb",
            "CCONJ-M": "conjunction",
            "CCONJ-P": "conjunction",
            "CCONJ-Q": "conjunction",
            "CCONJ-S": "conjunction",
            "CCONJ-T": "conjunction",
            "DET-C1": "adjective",
            "DET-C2": "adjective",
            "DET-D1": "adjective",
            "DET-F": "adjective",
            "DET-H": "adjective",
            "DET-I": "adjective",
            "DET-J": "adjective",
            "DET-K": "adjective",
            "DET-L": "adjective",
            "DET-L2": "adjective",
            "DET-M": "adjective",
            "INTJ-U": "interjection",
            "NOUN-A1": "noun",
            "NOUN-A2": "noun",
            "NOUN-A3": "noun",
            "NOUN-A4": "noun",
            "NOUN-A5": "noun",
            "NOUN-A6": "noun",
            "NOUN-A7": "noun",
            "NOUN-A8": "noun",
            "NUM-D1": "number",
            "NUM-D2": "number",
            "NUM-D3": "number",
            "NUM-D6": "number",
            "PART-M": "particle",
            "PART-O": "particle",
            "PART-P": "particle",
            "PART-S": "particle",
            "PART-X": "particle",
            "PRON-E": "pronoun",
            "PRON-G": "pronoun",
            "PRON-J": "pronoun",
            "PRON-K": "pronoun",
            "PRON-L": "pronoun",
            "PROPN-A1": "proper_noun",
            "PROPN-A2": "proper_noun",
            "PROPN-A3": "proper_noun",
            "PROPN-A4": "proper_noun",
            "PROPN-A5": "proper_noun",
            "PROPN-A6": "proper_noun",
            "PROPN-A7": "proper_noun",
            "SCONJ-N": "conjunction",
            "SCONJ-S": "conjunction",
            "SCONJ-T": "conjunction",
            "VERB-B1": "verb",
            "VERB-B2": "verb",
            "VERB-B3": "verb",
            "VERB-B4": "verb",
            "VERB-B5": "verb",
            "VERB-B6": "verb",
            "VERB-Y1": "verb",
            "VERB-Y2": "verb",
            "VERB-Y3": "verb",
            "VERB-Y4": "verb",
            "VERB-Y5": "verb",
            "VERB-Y6": "verb",
            "X-0": "unknown",
            "_-punc": "punc",
        }
        if token["upos"] and token["xpos"]:
            token_key = "-".join([token["upos"], token["xpos"]])
            if token_key in lasla_map:
                token["xpos"] = lasla_map[token_key]
            else:
                token["xpos"] = "_"
        else:
            token["xpos"] = "_"
    else:
        pass
    return token


def update_numbers(token):
    if token["upos"] == "NUM":
        token["xpos"] = "number"
    return token


def update_participles(token):
    # Check, esp. UDante
    if token["upos"] == "VERB":
        token["xpos"] = "verb"
    return token


def update_sum(token):
    if token["lemma"] == "sum":
        token["upos"] = "AUX"
        token["xpos"] = "verb"
    return token


def update_det(token):
    if token["lemma"] == "is":
        token["upos"] = "PRON"
        token["xpos"] = "pronoun"
    elif token["lemma"] == "ipse":
        token["upos"] = "DET"
        token["xpos"] = "determiner"
    elif token["lemma"] == "suus":
        token["upos"] = "DET"
        token["xpos"] = "determiner"
    elif token["lemma"] == "sui":
        token["upos"] = "PRON"
        token["xpos"] = "pronoun"
    return token


def update_part(token):
    if token["lemma"] == "non":
        token["upos"] = "PART"
        token["xpos"] = "particle"
    return token


def get_proper_noun(token):
    if token["xpos"] == "noun" and token["lemma"][0].isupper():
        token["xpos"] = "proper_noun"
    if token["xpos"] == "proper_noun" or token["upos"] == "PROPN":
        token["xpos"] = "proper_noun"
        token["upos"] = "PROPN"
        token["form"] = token["form"].title()
        token["lemma"] = token["lemma"].title()
    return token


def update_punct(token):
    if token["upos"] == "PUNCT" or token["xpos"] == "punc":
        token["upos"] = "PUNCT"
        token["xpos"] = "punc"
    return token


def norm_form(token):
    if "(" in token["lemma"] and ")" in token["lemma"]:
        token["lemma"] = token["lemma"].replace("(", "").replace(")", "")
    if token["form"] == "sì":
        token["form"] = "si"
        token["lemma"] = "si"
    if token["xpos"] == "proper_noun" or token["upos"] == "PROPN":
        token["form"] = token["form"].title()
        token["lemma"] = token["lemma"].title()
    return token


def norm_nec(token):
    if token["form"] == "nec":
        token["lemma"] = "neque"
    return token


def norm_defective_verbs(token):
    if token["lemma"] == "coepio":
        token["form"] = "coepi"
    elif token["lemma"] == "odio":
        token["form"] = "odi"
    else:
        pass
    return token


def norm_greek(token):
    # check if the token is a Greek word
    # if so, update xpos and upos
    import re

    if re.search(r"[Α-Ωα-ω]", token["form"]):
        token["lemma"] = "greek.expression"  # TODO: Add a lemma for Greek expressions
        token["xpos"] = "_"
        token["upos"] = "X"
    return token


def misc_fix(token):
    # Correcting any systematic errors that appear in the UD annotations.
    # TODO: Push these corrections to the UD repository
    if token["form"] == "ad":
        token["lemma"] = "ad"
    if token["form"] == "ab":
        token["lemma"] = "ab"
    if token["form"] == "deus,":
        token["form"] = "deus"
        token["lemma"] = "deus"
    if token["form"] == "esse" and token["lemma"] == "esse":
        token["lemma"] = "sum"
    if token["lemma"] == "*lyrcea":
        token["lemma"] = "Lyrcea"
    # Correcting misc harmonization issues
    if token["form"] == "dii":
        token["lemma"] = "deus"
    if token["lemma"] == "pena":
        token["lemma"] = "poena"
    if token["lemma"] == "seipsum":
        token["lemma"] = "seipse"
    if token["form"] == "subito":
        token["lemma"] = "subito"
        token["xpos"] = "adverb"
        token["upos"] = "ADV"
    return token


for file in tqdm(files):
    treebank = re.match(r".*preprocess/MM-la_(.*)-(ud|xx).*", file).group(1)
    serialization = []
    print(f"Processing {file} to update features...")
    with open(file) as f:
        contents = f.read()
        sentences = parse(contents)
        for sentence in tqdm(sentences):
            for token in sentence:
                # PREPROCESS: Update tense for Latin
                token = update_feats_tense(token)
                # PREPROCESS: Update mood for Latin
                token = update_feats_mood(token)
                # PREPROCESS: Update xpos for Latin
                token = update_xpos(treebank, token)
                # PREPROCESS: Update numbers for Latin
                token = update_numbers(token)
                # PREPROCESS: Update participles for Latin
                token = update_participles(token)
                # PREPROCESS: Update 'sum'
                token = update_sum(token)
                # PREPROCESS: Update 'det'
                token = update_det(token)
                # PREPROCESS: Update 'part'
                token = update_part(token)
                # PREPROCESS: Get proper nouns
                token = get_proper_noun(token)
                # PREPROCESS: Update punctuation
                token = update_punct(token)
                # PREPROCESS: Normalize form
                token = norm_form(token)
                # PREPROCESS: Normalize "nec"
                token = norm_nec(token)
                # PREPROCESS: Normalize defective verbs
                token = norm_defective_verbs(token)
                # PREPROCESS: Normalize Greek
                token = norm_greek(token)
                # PREPROCESS: Limit features to those necessary for form
                token = limit_features(token)
                # PREPROCESS: Miscellaneous fixes
                token = misc_fix(token)

            serialization.append(sentence.serialize())

    outfile = os.path.join(UPDATE_PATH, os.path.basename(file))

    with open(outfile, "w") as f:
        f.write("".join([sentence for sentence in serialization]))
