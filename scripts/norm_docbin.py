import glob
import spacy
from spacy.tokens import DocBin

nlp = spacy.blank("la")

files = glob.glob("corpus/**/*.spacy", recursive=True)

for file in files:
    db_in = DocBin()
    db_out = DocBin()
    input = db_in.from_disk(path=file)
    docs = input.get_docs(nlp.vocab)
    for doc in docs:
        for token in doc:
            token.norm_ = (
                token.norm_.replace("v", "u")
                .replace("j", "i")
                .replace("V", "U")
                .replace("J", "I")
            )
        db_out.add(doc)
    db_out.to_disk(path=file)
