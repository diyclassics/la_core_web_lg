import os.path
from glob import glob
from tqdm import tqdm
from conllu import parse
import re

UPDATE_PATH = "assets/preprocess"

files = [file for file in glob("assets/original/**/*.conllu", recursive=True)]
print(f"\n\nUpdating conllu files for further processing...\n")


def latin_norm(text):
    return text.replace("v", "u").replace("j", "i").replace("V", "U").replace("J", "I")


def lemma_norm(token):
    token["lemma"] = latin_norm(token["lemma"])
    return token


def lemma_replace(token):
    if token["lemma"] == "ego" and token["form"].lower().startswith("n"):
        token["lemma"] = "nos"

    if token["lemma"] == "tu" and (
        token["form"].lower().startswith("v") or token["form"].lower().startswith("u")
    ):
        token["lemma"] = "uos"

    return token


for file in tqdm(files):
    serialization = []
    print(f"Processing {file}...")
    with open(file) as f:
        contents = f.read()
        sentences = parse(contents)
        for sentence in tqdm(sentences):
            metadata = sentence.metadata
            # PREPROCESS: Handle lowercase for first character
            if metadata["text"]:
                metadata_lower_start = re.search(r"[a-zA-Z]", metadata["text"])
                if metadata_lower_start:
                    metadata_lower_start = metadata_lower_start.start()
                    metadata["text"] = (
                        metadata["text"][:metadata_lower_start]
                        + metadata["text"][metadata_lower_start].lower()
                        + metadata["text"][metadata_lower_start + 1 :]
                    )
            for token in sentence:
                if token["form"].isalpha():
                    token["form"] = token["form"].lower()
                    break
            # PREPROCESS: Add final punctuation to Proiel metadata text
            if "proi" in file:
                sentence.metadata["text"] = f'{sentence.metadata["text"]}.'
            for token in sentence:
                # PREPROCESS: Norms lemmas
                token = lemma_norm(token)
                # PREPROCESS: Replace lemmas
                token = lemma_replace(token)

                # Get data for Proiel updates
                last_token = token["id"]
                if token["deprel"] == "root":
                    last_root = token["id"]
            # PREPROCESS: Add final punctuation to Proiel sents
            if "proi" in file:
                sentence.append(
                    {
                        "id": last_token + 1,
                        "form": ".",
                        "lemma": ".",
                        "upos": None,
                        "xpos": "punc",
                        "feats": None,
                        "head": last_root,
                        "deprel": "punct",
                        "deps": None,
                        "misc": None,
                    }
                )
            # Take out combined tokens; TODO: Learn to handle combined tokens in spaCy training
            sentence = sentence.filter(id=lambda x: type(x) is int)
            sentence.metadata = metadata
            serialization.append(sentence.serialize())
    outfile = os.path.join(UPDATE_PATH, os.path.basename(file))

    with open(outfile, "w") as f:
        f.write("".join([sentence for sentence in serialization]))
