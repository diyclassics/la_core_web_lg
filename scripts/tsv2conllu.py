import re
import pandas as pd
from collections import namedtuple

Noun = namedtuple("Noun", ["Gender", "Number", "Case"])
Verb = namedtuple(
    "Verb", ["Person", "Number", "Tense", "Mood", "Voice", "Gender", "Case"]
)

df = pd.read_pickle("assets/preprocess/ud-parse-temp.pkl")

df.assign(**{"reference": df["reference"].fillna(df["source"])}, inplace=True)

df["head"] = df["head"].astype(float).astype("Int64").astype(str)
df["sent_id"] = df["sent_id"].astype(str)
df.fillna("_", inplace=True)

df_files = dict(tuple(df.groupby("file")))
df_refs = {k: dict(tuple(v.groupby(["sent_id", "text"]))) for k, v in df_files.items()}


def format_feats(feats):
    if feats != "_":
        feats_format = []
        feats_dict = feats._asdict()
        for k, v in feats_dict.items():
            feats_format.append(f"{k.title()}={v}")
        feats_format = [
            item for item in feats_format if "=None" not in item and "=nan" not in item
        ]
        feats_format = "|".join(feats_format)
        return feats_format
    else:
        return feats


def extract_treebank_name(treebank):
    # e.g. assets/UD_Latin-ITTB/la_ittb-ud-test.conllu
    treebank = re.match(r".*UD_Latin-(.*)/(.*\.conllu)", treebank).group(2)
    return treebank.lower()


for k, v in df_refs.items():
    filename = f"assets/processed/mod-{extract_treebank_name(k)}"
    with open(filename, "w") as f:
        for k_, v_ in v.items():
            f.write(f"# sent_id = {k_[0]}\n")
            f.write(f"# text = {k_[1]}\n")
            for row in v_.iterrows():
                feats = format_feats(row[1]["feats"])
                f.write(
                    f"{row[1]['id']}\t{row[1]['form']}\t{row[1]['lemma']}\t{row[1]['upos']}\t{row[1]['xpos']}\t{feats}\t{row[1]['head']}\t{row[1]['deprel']}\t{row[1]['deps']}\t{row[1]['misc']}\n"
                )
            f.write("\n")
