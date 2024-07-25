from glob import glob
from tqdm import tqdm
from conllu import parse
from collections import defaultdict, Counter


files = glob("assets/preprocess/*.conllu")

lemmas = []
upos_data = defaultdict(Counter)
xpos_data = defaultdict(Counter)

for file in tqdm(files):
    with open(file, "r") as f:
        sentences = parse(f.read())
        for sentence in sentences:
            for token in sentence:
                lemmas.append(token["lemma"])
                upos_data[token["lemma"]][token["upos"]] += 1
                xpos_data[token["lemma"]][token["xpos"]] += 1

lemma_counts = Counter(lemmas)

# get most frequent lemmas that have more than one upos tag
for lemma, count in lemma_counts.most_common(150):
    if len(set(upos_data[lemma])) > 1:
        print(lemma, upos_data[lemma])
