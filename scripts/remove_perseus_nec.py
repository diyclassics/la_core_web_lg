import re
import pandas as pd

print('Removing separated "nec" (= "c ne") and "neque" (= "que ne") [Perseus]')

df = pd.read_csv("assets/preprocess/ud-parse-temp.tsv", sep="\t", low_memory=False)

df["remove_nec"] = df["text"].apply(
    lambda x: 1
    if (
        re.search(r"\bc ne\b", x, flags=re.IGNORECASE)
        or re.search(r"\bque ne\b", x, flags=re.IGNORECASE)
    )
    else 0
)
df = df[df["remove_nec"] == 0]
df.drop(columns=["remove_nec"], inplace=True)

df.to_csv("assets/preprocess/ud-parse-temp.tsv", sep="\t", index=False)
