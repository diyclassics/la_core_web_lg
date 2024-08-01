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
            # check that token ids are in consecutive order
            # cf. error in LASLA # sent_id = OvMETAM06-M-06-3
            # also, `nonne` passim; TODO: Check LASLA files for other errors
            ids = [token["id"] for token in sentence if type(token["id"]) is int]
            if ids != list(range(1, len(ids) + 1)):
                continue
            metadata = sentence.metadata
            # PREPROCESS: Handle uppercase for first character
            if metadata["text"]:
                metadata_lower_start = re.search(r"[a-zA-Z]", metadata["text"])
                if metadata_lower_start:
                    metadata_lower_start = metadata_lower_start.start()
                    metadata["text"] = (
                        metadata["text"][:metadata_lower_start]
                        + metadata["text"][metadata_lower_start].upper()
                        + metadata["text"][metadata_lower_start + 1 :]
                    )
            for token in sentence:
                if token["form"].isalpha():
                    token["form"] = token["form"].title()
                    break
            # PREPROCESS: Add final punctuation to Proiel metadata text
            if "proi" in file or "lasl" in file or "lila" in file:
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
            if "proi" in file or "lila" in file:
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
            elif "lasl" in file:
                sentence.append(
                    {
                        "id": last_token + 1,
                        "form": ".",
                        "lemma": ".",
                        "upos": None,
                        "xpos": "punc",
                        "feats": None,
                        "head": None,
                        "deprel": None,
                        "deps": None,
                        "misc": None,
                    }
                )
            else:
                pass
            # Take out combined tokens; TODO: Learn to handle combined tokens in spaCy training
            sentence = sentence.filter(id=lambda x: "-" not in str(x))
            sentence.metadata = metadata
            serialization.append(sentence.serialize())
    outfile = os.path.join(UPDATE_PATH, os.path.basename(file))

    with open(outfile, "w") as f:
        f.write("".join([sentence for sentence in serialization]))
