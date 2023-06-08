<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: la_core_web_lg

Code required to train spaCy-compatible lg core model for Latin, i.e pipeline with POS tagger, morphologizer, lemmatizer, dependency parser, and NER trained on all available Latin UD treebanks, i.e. Perseus, PROIEL, ITTB, UDante, and LLCT (see below). The model contains floret vectors (200,000) trained on Wikipedia, Oscar, UD and CC100-Latin data. NER is based on custom tagged data based on tagger output and manual annotation, supplemented by data from the Herodotos Project; this data is included in `assets/ner/`.

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `assets` | Download assets |
| `preprocess` | Convert different UD treebanks so that they use shared formatting, feature defs, etc. |
| `convert` | Convert the data to spaCy's format |
| `norm-corpus` | Convert norm attribute to u-v and i-j norm |
| `init-labels` | Initialize labels for components |
| `train` | Train tagger/parser/etc. on Latin UD treebanks |
| `evaluate` | Evaluate model on the test data and save the metrics |
| `convert-ner` | Convert the NER data to spaCy's binary format |
| `train-ner` | Train the NER model for the model |
| `assemble` | Assemble core model, i.e. add NER component to dep model |
| `assemble-meta` | Assemble meta.json files so that all metrics are included |
| `package` | Package the trained core model |
| `document` | Document core_web_lg |
| `clean` | Remove intermediate files |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `assemble` &rarr; `assemble-meta` &rarr; `package` &rarr; `document` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/original/UD_Latin-Perseus` | Git |  |
| `assets/original/UD_Latin-PROIEL` | Git |  |
| `assets/original/UD_Latin-ITTB` | Git |  |
| `assets/original/UD_Latin-LLCT` | Git |  |
| `assets/original/UD_Latin-UDante` | Git |  |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->

## Install

- To install the current version...
    - `pip install https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl`

## Use in spaCy
```
import spacy
nlp = spacy.load("la_core_web_lg")
```

## Model repository

- The model itself can be found here:
    - https://huggingface.co/latincy/la_core_web_lg

## Current version

| Feature | Description |
| --- | --- |
| **Name** | `la_core_web_lg` |
| **Version** | `3.5.2` |
| **spaCy** | `>=3.5.2,<3.6.0` |
| **Default Pipeline** | `normer`, `tok2vec`, `tagger`, `morphologizer`, `trainable_lemmatizer`, `parser`, `lemma_fixer`, `ner` |
| **Components** | `senter`, `normer`, `tok2vec`, `tagger`, `morphologizer`, `trainable_lemmatizer`, `parser`, `lemma_fixer`, `ner` |
| **Vectors** | -1 keys, 200000 unique vectors (300 dimensions) |
| **Sources** | UD_Latin-Perseus<br />UD_Latin-PROIEL<br />UD_Latin-ITTB<br />UD_Latin-LLCT<br />UD_Latin-UDante |
| **License** | `MIT` |
| **Author** | [Patrick J. Burns; with Nora Bernhardt [ner], Tim Geelhaar [tagger, morphologizer, parser, ner], Vincent Koch [ner]](https://diyclassics.github.io/) |

### Accuracy

| Type | Score |
| --- | --- |
| `ENTS_F` | 89.97 |
| `ENTS_P` | 86.72 |
| `ENTS_R` | 93.46 |
| `NER_LOSS` | 3452.09 |
| `NER_TOK2VEC_LOSS` | 326.51 |
| `SENTS_F` | 93.22 |
| `SENTS_P` | 92.53 |
| `SENTS_R` | 93.93 |
| `TAG_ACC` | 94.14 |
| `POS_ACC` | 97.34 |
| `MORPH_ACC` | 92.79 |
| `LEMMA_ACC` | 94.61 |
| `DEP_UAS` | 83.37 |
| `DEP_LAS` | 77.88 |
| `TOK2VEC_LOSS` | 10891675.20 |
| `TAGGER_LOSS` | 746155.69 |
| `MORPHOLOGIZER_LOSS` | 1708216.08 |
| `TRAINABLE_LEMMATIZER_LOSS` | 607607.46 |
| `PARSER_LOSS` | 6177392.51 |

NB: For full details on tags etc., see the README.md in the model package.

### Bibliography
- Cecchini, F.M., Passarotti, M., Marongiu, P., and Zeman, D. 2018. “Challenges in Converting the Index Thomisticus Treebank into Universal Dependencies.” In Proceedings of the Second Workshop on Universal Dependencies (UDW 2018). 27–36.
- Cecchini, F.M., Sprugnoli, R., Moretti, G., and Passarotti, M. 2020. “UDante: First Steps Towards the Universal Dependencies Treebank of Dante’s Latin Works.” In Dell’Orletta, F., Monti, J., and Tamburini, F. eds. Proceedings of the Seventh Italian Conference on Computational Linguistics CLiC-It 2020. Accademia University Press. 99–105. doi:10.4000/books.aaccademia.8653. http://books.openedition.org/aaccademia/8653.
- Celano, G.G.A., Crane, G., Almas, B., and et al. 2014. “The Ancient Greek and Latin Dependency Treebank v.2.1.” https://perseusdl.github.io/treebank_data/.
- Erdmann, A., Wrisley, D.J., Allen, B., Brown, C., Bodénès, S.C., Elsner, M., Feng, Y., Joseph, B., Joyeaux-Prunel, B., and Marneffe, M.-C. 2019. “Practical, Efficient, and Customizable Active Learning for Named Entity Recognition in the Digital Humanities.” In Proceedings of North American Association of Computational Linguistics (NAACL 2019). Minneapolis, Minnesota.
- Haug, D.T., and Jøhndal, M. 2008. “Creating a Parallel Treebank of the Old Indo-European Bible Translations.” In Proceedings of the Second Workshop on Language Technology for Cultural Heritage Data (LaTeCH 2008). 27–34.
- Honnibal, M., and Montani, I. 2023. “SpaCy: Industrial-Strength Natural Language Processing in Python” (version v. 3.5.0). https://spacy.io/.
- Korkiakangas, T. 2021. “Late Latin Charter Treebank: Contents and Annotation.” Corpora 16 (2) (August 1): 191–203. doi:10.3366/cor.2021.0217.
- Passarotti, M., and Dell’Orletta, F. 2010. “Improvements in Parsing the Index Thomisticus Treebank. Revision, Combination and a Feature Model for Medieval Latin.” In Proceedings of the Seventh International Conference on Language Resources and Evaluation (LREC’10). Valletta, Malta: European Language Resources Association (ELRA). http://www.lrec-conf.org/proceedings/lrec2010/pdf/178_Paper.pdf.
