from glob import glob
from tqdm import tqdm

files = glob("assets/temp/lasla/*.conllup")

conllus = []

print("Prepping LASLA files...")

for file in tqdm(files):
    # Skip files now in LILA treebanks
    if "HerculesFurens" in file or "Agamemnon" in file or "Germania" in file:
        print(f"Skipping {file}...")
        continue
    else:
        with open(file) as f:
            contents = f.read().strip()

            conllu_recs = [
                line.split("\t")[:10] for line in contents.split("\n")
            ]  # only keep first 10 columns; i.e. drop LILA:FLCAT LILA:SENTID LILA:LINE
            conllu_lines = "\n".join(["\t".join(rec) for rec in conllu_recs][1:])
            conllus.append(conllu_lines)

conllu = "\n\n".join(conllus)

with open("assets/temp/lasla/lasla.conllu", "w") as f:
    f.write(conllu)
    f.write("\n")
