# For 'prep' part of script, cf. https://github.com/explosion/spaCy/discussions/6926

from glob import glob
from tqdm import tqdm
from conllu import parse
import re


import spacy
from spacy.tokens import Doc
from spacy.tokens import DocBin
import random


UPDATE_PATH = "assets/preprocess"

files = [file for file in glob("assets/preprocess/**/*.conllu", recursive=True)]
print(f"\n\nExtracting/converting sentence data...\n")

senter_data = []

for file in tqdm(files):
    # serialization = []
    print(f"Processing {file}...")
    with open(file) as f:
        contents = f.read()
        sentences = parse(contents)
        for sentence in tqdm(sentences):
            text = sentence.metadata["text"]
            # use regex to split anywhere there is a ; or : in the middle of the text
            # make sure the ; or the : is not first or last character
            # retain split character at the end of each split sentence
            if ";" in text or ":" in text:
                split_sents = re.split(r"([;:?])", text)
                split_sents = [
                    split_sents[i] + split_sents[i + 1]
                    for i in range(0, len(split_sents) - 1, 2)
                ] + [split_sents[-1]]
                for sent in split_sents:
                    if sent:
                        upper_sent = sent[0].upper() + sent[1:]
                        lower_sent = sent[0].lower() + sent[1:]
                        senter_data.append(upper_sent.strip())
                        senter_data.append(lower_sent.strip())
            else:
                upper_sent = text[0].upper() + text[1:]
                lower_sent = text[0].lower() + text[1:]
                senter_data.append(upper_sent.strip())
                senter_data.append(lower_sent.strip())

senter_data = list(set(senter_data))

with open("assets/senter/senter_data.txt", "w") as f:
    for sent in senter_data:
        f.write(sent + "\n")

random.seed(42)
random.shuffle(senter_data)

# split senter_data into train, dev, test
train_size = int(0.8 * len(senter_data))
dev_size = int(0.1 * len(senter_data))
test_size = len(senter_data) - train_size - dev_size

train_data = senter_data[:train_size]
dev_data = senter_data[train_size : train_size + dev_size]
test_data = senter_data[train_size + dev_size :]

datasets = ["train", "dev", "test"]

for dataset, data in zip(datasets, [train_data, dev_data, test_data]):

    nlp = spacy.blank("la")
    db = DocBin()

    i = 0
    while i < len(senter_data):
        para_size = random.randint(3, 15)
        sent_docs = [nlp(sent) for sent in senter_data[i : i + para_size]]
        doc = Doc.from_docs(sent_docs, ensure_whitespace=True)
        db.add(doc)
        i += para_size

    db.to_disk(f"corpus/senter/{dataset}.spacy")
