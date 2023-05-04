import json
import argparse

# get dep_meta, ner_meta, assembled_meta from command line
parser = argparse.ArgumentParser()
parser.add_argument("--dep_meta", type=str, required=True)
parser.add_argument("--ner_meta", type=str, required=True)
parser.add_argument("--assembled_meta", type=str, required=True)
args = parser.parse_args()

dep_meta = args.dep_meta
ner_meta = args.ner_meta
assembled_meta = args.assembled_meta


def get_assembled_meta_performance_json(dep_meta, ner_meta):
    dep_meta_json = json.load(open(dep_meta))
    ner_meta_json = json.load(open(ner_meta))
    ner_meta_json["performance"]["ner_tok2vec_loss"] = ner_meta_json["performance"].pop(
        "tok2vec_loss"
    )

    assembled_meta_json = dep_meta_json.copy()
    assembled_meta_json["performance"] = (
        ner_meta_json["performance"] | dep_meta_json["performance"]
    )
    return assembled_meta_json["performance"]


def update_assembled_meta_performance_json(dep_meta, ner_meta, assembled_meta):
    assembled_meta_json = json.load(open(assembled_meta))
    if "performance" not in assembled_meta_json:
        assembled_meta_json["performance"] = get_assembled_meta_performance_json(
            dep_meta, ner_meta
        )
        with open(assembled_meta, "w") as f:
            json.dump(assembled_meta_json, f, indent=4)
    else:
        print("Performance already in assembled meta.json")


if __name__ == "__main__":
    update_assembled_meta_performance_json(dep_meta, ner_meta, assembled_meta)
