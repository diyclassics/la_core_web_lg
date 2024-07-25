# Preprocessing decisions

Scripts in this folder are used to preprocess the UD data and create common formatting, annotations, etc. for the data. Decisions made in the course of preprocessing are documented here.

## update_conllu.py
- UD & LASLA files are normalized to a common format using the `conllu` package

## analyze_feats.py
- The preprocessing decisions are documented in the file itself; the short version is that this script A. remaps UPOS tags to a smaller, more consistent set, esp. for POS tags that have different annotation schemes in the different treebanks (e.g. 'DET' and 'PRON' or 'ADJ'); B. limits morphological annotations; C. remaps XPOS to a smaller, more consistent set; some handling of case, etc.
