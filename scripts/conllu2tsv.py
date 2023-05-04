from glob import glob
import pandas as pd
from conllu import parse
from tqdm import tqdm

files = [file for file in glob("assets/original/**/*.conllu", recursive=True)]

print(f"Converting conllu files in /assets to tsv for further processing...\n")

rows = []

for file in tqdm(files):
    print(f"Processing {file}...")
    with open(file) as f:
        contents = f.read()
        sentences = parse(contents)
        for sentence in tqdm(sentences):
            if "proi" in file:
                sentence.metadata["text"] = f'{sentence.metadata["text"]}.'
            for token in sentence:
                row = {}
                row.update({"file": file})
                row.update(sentence.metadata)
                row.update(token)
                rows.append(row)
                last_token = token["id"]
                if token["deprel"] == "root":
                    last_root = token["id"]
            if "proi" in file:
                row = {}
                row.update({"file": file})
                row.update(sentence.metadata)
                token["id"] = last_token + 1
                token["form"] = "."
                token["lemma"] = "."
                token["upos"] = None
                token["xpos"] = "punc"
                token["feats"] = None
                token["deprel"] = "punct"
                token["deps"] = None
                token["misc"] = None
                token["head"] = last_root
                row.update(token)
                rows.append(row)
df = pd.DataFrame(rows)


def join_id(id):
    if isinstance(id, tuple):
        id = [str(i) for i in id]
        return "".join(id)
    else:
        return id


df["feats"] = df["feats"].fillna({i: {} for i in df.index})
df["id"] = df["id"].apply(join_id)

print("Concatentaing feats and misc columns...")  # TODO: Faster way to do this?

df = pd.concat(
    (
        df.drop(["feats", "misc"], axis=1),
        df["feats"].apply(lambda x: pd.Series(x, dtype="object")).add_prefix("feats_"),
        df["misc"].apply(lambda x: pd.Series(x, dtype="object")).add_prefix("misc_"),
    ),
    axis=1,
)

df.to_csv("assets/preprocess/ud-parse.tsv", sep="\t", index=False)
