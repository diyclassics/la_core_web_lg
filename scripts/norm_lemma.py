import pandas as pd

df = pd.read_csv("assets/preprocess/ud-parse.tsv", sep="\t", low_memory=False)

# 1. Normalizing v/j


def lemma_norm(lemma):
    return lemma.replace("v", "u").replace("j", "i").replace("V", "U").replace("J", "I")


df["lemma"] = df["lemma"].apply(lambda x: lemma_norm(x))

# 2. Normalizing ego/nos and tu/vos

# Standardize ego/nos and tu/vos
# TODO: Are there more cases to consider?


def lemma_replace(row):
    if row["lemma"] == "ego" and row["form"].lower().startswith("n"):
        row["lemma"] = "nos"

    if row["lemma"] == "tu" and (
        row["form"].lower().startswith("v") or row["form"].lower().startswith("u")
    ):
        row["lemma"] = "uos"

    return row


df = df.apply(lambda x: lemma_replace(x), axis=1)

df.to_csv("assets/preprocess/ud-parse-temp.tsv", sep="\t", index=False)
