# Preprocessing decisions

The scripts in this folder are used to preprocess the UD data and create common formatting, annotations, etc. for the data. Decisions made in the course of preprocessing are documented here.

## conllu2tsv.py
- UD conllu files are converted to .tsv file
- 'features' and 'misc' columns are separated into multiple (prefixed) columns as necessary

## lemma_norm.py
- u/v and i/j normalization, i.e. all lemmas are normalized to u and i
- Convert lemma for forms of 'nos' from 'ego' and 'uos' from 'tu' \[UDDante\]

## remove_perseus_nec.py
- Remove sentences in UD files that have *nec* parsed as 'c ne' and *neque* parsed as 'que ne' \[Perseus\]
- TODO: Restore these sentences after writing script to recombine the tokens into the preferred UD format

## analyze_feats.py
- The preprocessing decisions are documented in the file itself; the short version is that this script A. remaps UPOS tags to a smaller, more consistent set, esp. for POS tags that have different annotation schemes in the different treebanks (e.g. 'DET' and 'PRON' or 'ADJ'); B. limits morphological annotations to NOUN, VERB, ADJ, DET, and PRON and retains only gender, number, case and person, number, tense, mood, and voice, which are mapped consistent in a named tuple; C. remaps XPOS to a smaller, more consistent set

## norm_docbin.py
- Since `trainable_lemmatizer` will use the `norm_` token attribute for backoff, ensure that this attribute is normalized for u/v and i/j