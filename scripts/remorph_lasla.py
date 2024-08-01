from conllu import parse
from tqdm import tqdm
from tabulate import tabulate

import spacy

# Load spaCy model
nlp = spacy.load("la_core_web_lg")


def update_gender_feats(sentence):
    # Parse the sentence using spaCy
    doc = nlp(sentence.metadata["text"])
    gender_dict = {token.text: token.morph.get("Gender") for token in doc}
    # values are single item lists, should be string or None
    gender_dict = {k: v[0] if v else None for k, v in gender_dict.items()}

    for token in sentence:
        if token["feats"] and "," in token["feats"].get("Gender", ""):
            updated_gender = gender_dict.get(token["form"])
            if updated_gender:
                token["feats"]["Gender"] = updated_gender
            else:
                import random

                random.seed(42)
                # TODO: Selecting at random for now, could be improved
                token["feats"]["Gender"] = random.choice(
                    token["feats"]["Gender"].split(",")
                )
    return sentence


print(f"Fixing morphology for LASLA and CIRCSE files")

files = [
    "assets/preprocess/MM-la_circse-ud-train.conllu",
    "assets/preprocess/MM-la_lasla-xx-train.conllu",
]


for file in files:

    serialization = []

    with open(file, "r") as f:
        data = f.read()
        sentences = parse(data)
        for sentence in tqdm(sentences[:5]):
            sentence = update_gender_feats(sentence)
            serialization.append(sentence.serialize())

    with open(file, "w") as f:
        f.write("".join([sentence for sentence in serialization]))
