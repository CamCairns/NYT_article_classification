#! /bin/bash

# extract corpus from nyt api
python ../nyt_corpus_creator.py

# clean up extraneous lines
python ../nyt_article_remove_line.py