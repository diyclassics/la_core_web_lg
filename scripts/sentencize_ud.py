import pandas as pd
import re
from string import punctuation


def tokenize(text):
    text = re.sub(rf"([{punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])", r" \1 ", text)
    text = " ".join(text.split())
    return text


df = pd.read_csv("assets/preprocess/ud-parse-temp.tsv", sep="\t", low_memory=False)

df["text"] = df["text"].apply(tokenize)
texts = df["text"].unique().tolist()

with open("vectors/tokenized/la_ud.txt", "w") as f:
    for text in texts:
        f.write(f"{text}\n")
