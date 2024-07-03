<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: la_core_web_xx

Code required to train spaCy-compatible sm, md, and lg core models for Latin, i.e pipeline with POS tagger, morphologizer, lemmatizer, dependency parser, and NER trained on all available Latin UD treebanks, i.e. Perseus, PROIEL, ITTB, UDante, and LLCT (see below). The md and lg models contains floret vectors trained on Wikipedia, Oscar, UD and—for lg—CC100-Latin data. NER is based on custom tagged data based on tagger output and manual annotation, supplemented by data from the Herodotos Project; this data is included in `assets/ner/`.

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[Weasel documentation](https://github.com/explosion/weasel).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `assets` | Download assets |
| `preprocess` | Convert different UD treebanks so that they use shared formatting, feature defs, etc. |
| `convert` | Convert the data to spaCy's format |
| `init-labels` | Initialize labels for components |
| `train_sm` | Train tagger/parser/etc. on Latin UD treebanks |
| `train_md` | Train tagger/parser/etc. on Latin UD treebanks |
| `train_lg` | Train tagger/parser/etc. on Latin UD treebanks |
| `evaluate_sm` | Evaluate model on the test data and save the metrics |
| `evaluate_md` | Evaluate model on the test data and save the metrics |
| `evaluate_lg` | Evaluate model on the test data and save the metrics |
| `convert-ner` | Convert the NER data to spaCy's binary format |
| `train-ner_sm` | Train the NER model for the model |
| `train-ner_md` | Train the NER model for the model |
| `train-ner_lg` | Train the NER model for the model |
| `assemble_sm` | Assemble core model, i.e. add NER component to dep model |
| `assemble_md` | Assemble core model, i.e. add NER component to dep model |
| `assemble_lg` | Assemble core model, i.e. add NER component to dep model |
| `assemble-meta_sm` | Assemble meta.json files so that all metrics are included |
| `assemble-meta_md` | Assemble meta.json files so that all metrics are included |
| `assemble-meta_lg` | Assemble meta.json files so that all metrics are included |
| `package_sm` | Package the trained core model |
| `package_md` | Package the trained core model |
| `package_lg` | Package the trained core model |
| `document` | Document core_web_xx |
| `clean` | Remove intermediate files |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `assets` &rarr; `preprocess` &rarr; `convert` &rarr; `init-labels` &rarr; `train_sm` &rarr; `evaluate_sm` &rarr; `convert-ner` &rarr; `train-ner_sm` &rarr; `assemble_sm` &rarr; `assemble-meta_sm` &rarr; `package_sm` &rarr; `document` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`weasel assets`](https://github.com/explosion/weasel/tree/main/docs/cli.md#open_file_folder-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/original/` | Git |  |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->

### Install

- To install the current version of the lg model...
    - `pip install https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl`

- Lookup lemmatizer requires custom Latin spaCy Lookups; install as follows...
    - `pip install -U git+https://github.com/diyclassics/spacy-lookups-data.git#egg=spacy-lookups-data`

### Use in spaCy

- To load the lg model in spaCy...

```
import spacy
nlp = spacy.load("la_core_web_lg")
```

### Model repository

- The models can be found here:
    - https://huggingface.co/latincy

### Changelog
- v3.7.5: Replaces UD training data with "harmonized" treebanks (cf. [Gamba and Zeman 2023](https://github.com/fjambe/Latin-variability/tree/main)); introduces “backoff”-style Lookup Lemmatizer to catch large numbers of unambiguous forms (+850K); NB: uses a custom fork of spaCy’s `space-lookup-data`, cf. https://github.com/diyclassics/spacy-lookups-data/tree/master; support for Latin-specific verb tenses, i.e. `perf` (perfect) or `imp` (imperfect) as opposed to `past`; simplification and speed-up of LatinCy-specific UD preprocessing workflow. \[07.03.2024\]
- v3.7.4: Retrain with release of spaCy v3.7.4 \[04.12.2023\]
- v3.6.0: Retrain with release of spaCy v3.6.0 \[07.08.2023\]
- v3.5.3: Add Verbform to morph labels; allows better handling of infinitives, gerunds, and gerundives \[6.22.2023\]

### Bibliography
- Cecchini, F.M., Passarotti, M., Marongiu, P., and Zeman, D. 2018. “Challenges in Converting the Index Thomisticus Treebank into Universal Dependencies.” In Proceedings of the Second Workshop on Universal Dependencies (UDW 2018). 27–36.
- Cecchini, F.M., Sprugnoli, R., Moretti, G., and Passarotti, M. 2020. “UDante: First Steps Towards the Universal Dependencies Treebank of Dante’s Latin Works.” In Dell’Orletta, F., Monti, J., and Tamburini, F. eds. Proceedings of the Seventh Italian Conference on Computational Linguistics CLiC-It 2020. Accademia University Press. 99–105. doi:10.4000/books.aaccademia.8653. http://books.openedition.org/aaccademia/8653.
- Celano, G.G.A., Crane, G., Almas, B., and et al. 2014. “The Ancient Greek and Latin Dependency Treebank v.2.1.” https://perseusdl.github.io/treebank_data/.
- Erdmann, A., Wrisley, D.J., Allen, B., Brown, C., Bodénès, S.C., Elsner, M., Feng, Y., Joseph, B., Joyeaux-Prunel, B., and Marneffe, M.-C. 2019. “Practical, Efficient, and Customizable Active Learning for Named Entity Recognition in the Digital Humanities.” In Proceedings of North American Association of Computational Linguistics (NAACL 2019). Minneapolis, Minnesota.
- Gamba, F., and Zeman, D. 2023. “Universalising Latin Universal Dependencies: A Harmonisation of Latin Treebanks in UD.” In Grobol, L. and Tyers, F. eds. *Proceedings of the Sixth Workshop on Universal Dependencies (UDW, GURT/SyntaxFest 2023)*. Washington, D.C.: Association for Computational Linguistics. 7–16. https://aclanthology.org/2023.udw-1.2.
- Haug, D.T., and Jøhndal, M. 2008. “Creating a Parallel Treebank of the Old Indo-European Bible Translations.” In Proceedings of the Second Workshop on Language Technology for Cultural Heritage Data (LaTeCH 2008). 27–34.
- Honnibal, M., and Montani, I. 2023. “SpaCy: Industrial-Strength Natural Language Processing in Python” (version v. 3.5.0). https://spacy.io/.
- Korkiakangas, T. 2021. “Late Latin Charter Treebank: Contents and Annotation.” Corpora 16 (2) (August 1): 191–203. doi:10.3366/cor.2021.0217.
- Passarotti, M., and Dell’Orletta, F. 2010. “Improvements in Parsing the Index Thomisticus Treebank. Revision, Combination and a Feature Model for Medieval Latin.” In Proceedings of the Seventh International Conference on Language Resources and Evaluation (LREC’10). Valletta, Malta: European Language Resources Association (ELRA). http://www.lrec-conf.org/proceedings/lrec2010/pdf/178_Paper.pdf.
