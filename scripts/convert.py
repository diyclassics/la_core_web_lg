"""Convert entity annotation from spaCy v2 TRAIN_DATA format to spaCy v3
.spacy format."""
import srsly
import typer
import warnings
from pathlib import Path

import spacy
from spacy.tokens import DocBin


def convert(lang: str, input_path: Path, output_path: Path):
    nlp = spacy.blank(lang)
    db = DocBin()
    for json in srsly.read_json(input_path):
        text = json["text"]
        doc = nlp.make_doc(text)
        ents = []
        if json["spans"]:
            for span_json in json["spans"]:
                start = int(span_json["start"])
                end = int(span_json["end"])
                label = span_json["label"]
                span = doc.char_span(
                    start,
                    end,
                    label=label,
                )
                if span is None:
                    msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                    warnings.warn(msg)
                else:
                    ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)


if __name__ == "__main__":
    typer.run(convert)
