import numpy as np
import pandas as pd
import glob
import time
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
#from spacy.lemmatizer import Lemmatizer
from spacy.lang.de.stop_words import STOP_WORDS
from spacy.language import Language
#import en_core_web_lg

from tqdm import tqdm
from pprint import pprint
#------------------------------------------------------------------------------
nlp = spacy.load('de_core_news_lg')
txt_paths = glob.glob("data_in/lda/*.txt")  # Save the (relative) paths of all .txt files in a list
print("{} text file(s) have been found. \n".format(len(txt_paths)))
print(txt_paths)

#iterate over all files in data_in/lda and read them into a list
txt_file_list = []
for txt_path in txt_paths:
    with open(txt_path, 'r') as f:
        txt_file_list.append(f.read().replace('\n', ' '))

for txt_file in txt_file_list:
    print("text file len:",len(txt_file))


# costum stopword list
stop_list = ["de","et","la","le","les","que","à","<",">","\t","all","S.","d´", ] #Examples:"Mrs.","Ms.","say","WASHINGTON","'s","Mr."

# Updates spaCy's default stop words list with my additional words.
nlp.Defaults.stop_words.update(stop_list)

# Iterates over the words in the stop words list and resets the "is_stop" flag.
for word in STOP_WORDS:
    lexeme = nlp.vocab[word]
    lexeme.is_stop = True

@Language.component("custom_lemma") # This decorator registers the component with spaCy.
def custom_lemma(doc): # Check if this is the case for german***
    # This takes in a doc of tokens from the NER and lemmatizes them.
    # Pronouns (like "I" and "you" get lemmatized to '-PRON-', so I'm removing those.
    doc = [token.lemma_ for token in doc if token.lemma_ != '-PRON-']
    doc = u' '.join(doc) # u for unicode?
    return nlp.make_doc(doc)

nlp.add_pipe("custom_lemma",after='ner')

@Language.component("remove_stopwords") # This decorator registers the component with spaCy.
def remove_stopwords(doc):
    # This will remove stopwords and punctuation.
    # Use token.text to return strings, which we'll need for Gensim.
    doc = [token.text for token in doc if token.is_stop != True and token.is_punct != True]
    return doc

nlp.add_pipe("remove_stopwords", last=True)

print(nlp.pipe_names)

# The add_pipe function appends our functions to the default pipeline.
#nlp.add_pipe(lemmatizer,name='lemmatizer',after='ner') got Error: [E966]
#`nlp.add_pipe` now takes the string name of the registered component factory, not a callable component. Expected string, but got <function lemmatizer at 0x7fbca03d61f0> (name: 'lemmatizer').




doc_list = []
# Iterates through each article in the corpus.
for doc in tqdm(txt_file_list):
    # Passes that article through the pipeline and adds to a new list.
    if len(doc) > 1000000:
        pass
    else:

        pr = nlp(doc)
        #print("this pr: ",pr)
        #stop for 5 sec
       #time.sleep(5)
        doc_list.append(pr)


# Creates, which is a mapping of word IDs to words.
words = corpora.Dictionary(doc_list)

# Turns each document into a bag of words.
corpus = [words.doc2bow(doc) for doc in doc_list]

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=words,
                                           num_topics=10,
                                           random_state=2,
                                           update_every=1,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

pprint(lda_model.print_topics(num_words=10))