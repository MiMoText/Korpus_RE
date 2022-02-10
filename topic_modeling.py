import glob
import textwrap
from tqdm import tqdm
from pprint import pprint

import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel

import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
from spacy.language import Language

#-----------------------Prep Raw Text-----------------------------------------------------
nlp = spacy.load('de_core_news_lg')
txt_paths = glob.glob("data_in/lda/*.txt")  # Save the (relative) paths of all .txt files in a list
print(txt_paths)
print("{} text file(s) have been found. \n".format(len(txt_paths)))

#iterate over all files in data_in/lda and read them into a list
txt_file_list = []
for txt_path in txt_paths:

    filename = txt_path.split("/")[-1]
    with open(txt_path, 'r') as f:
        prepared_text = f.read()
        prepared_text = prepared_text.replace('\n', ' ').replace('\t', ' ').replace("  "," ").replace('ſ', 's') # old german "s"-sign
        txt_file_list.append((prepared_text,filename)) # add the filename as a second element to the tuple

print("Splitting files that are too long into multiple files...")

txt_file_list_aux = txt_file_list # make an aux file so that we can delete from original list if needed

for txt_file in txt_file_list_aux:
    if len(txt_file[0]) > 1000000: # if the text file is longer than 1 million characters (spacy can't handle that)

        file_len = len(txt_file[0])
        mcount = 1 # million count. mcount is used to name the new files, and split text evenly
                        # example : 2.4 million characters -> 3x ~0.8 million characters


        while file_len/(1000000*mcount) > 1:
            mcount += 1


        split_len = int(file_len/(mcount)) +10 # add 10 to account for int rounding
        print("Splitting file {} into {} files of approx. {} characters each. \n".format(txt_file[1], mcount, split_len))

        split_text = textwrap.wrap(txt_file[0], split_len) # text is split into a list of strings
                                                                # textwrap should split on whitespaces

        filename = txt_file_list.pop(txt_file_list.index(txt_file))[1] # remove the original file from the list (not aux list)
                                                                            # save the original file name from tupel
        for i in range(len(split_text)):
            txt_file_list.append((split_text[i], filename+"_"+str(i+1)))    # add the split text list to the list

print("Text tuples processed \n\n")

#-----------------Prep Pipeline------------------------------------------------------------------
# Additional stopword list --> Updates spaCy's default stop words list with my additional words.
stop_list = ['welch','sogar'] # add your own stop words here
nlp.Defaults.stop_words.update(stop_list)

# Iterates over the words in the stop words list (french) and resets the "is_stop" flag.
for word in STOP_WORDS:
    lexeme = nlp.vocab[word]
    lexeme.is_stop = True


# Since spacy 3.0, we need decorators to register components...
@Language.component("custom_lemma") # This decorator registers the component with spaCy.
def custom_lemma(doc):
    # This takes in a doc of tokens from the NER and lemmatizes them.
    # Pronouns (like "I" and "you" get lemmatized to '-PRON-', so I'm removing those.
    doc = [token.lemma_ for token in doc if token.lemma_ != '-PRON-']
    doc = u' '.join(doc) # u for unicode?
    return nlp.make_doc(doc)

# The add_pipe function appends our functions to the default pipeline. (would not word this way without decorators)
nlp.add_pipe("custom_lemma",after='ner')

@Language.component("remove_stopwords") # This decorator registers the component with spaCy.
def remove_stopwords(doc):
    # This will remove stopwords and punctuation.
    # Use token.text to return !strings!, which we'll need for Gensim.
    doc = [token.text for token in doc if token.is_stop != True and token.is_punct != True and len(token.text) > 3]
    return doc

nlp.add_pipe("remove_stopwords", last=True)

print("The nlp pipeline has been set up:")
print(nlp.pipe_names)

#-----------------LDA------------------------------------------------------------------
# Iterates through each doc in our list
for doc in tqdm(txt_file_list):
    print("\n-------------Topics in file {}---------------\n".format(doc[1]))
    # Passes that article through the pipeline
    pr = nlp(doc[0])

    # Creates gensim corpus, which is a mapping of word IDs to words.
            #It is used to determine the vocabulary size, as well as for debugging and topic printing.
    words = corpora.Dictionary([pr])# note that pr is passed as list

    # Turns each document into a bag of words.
    corpus = [words.doc2bow(pr)]

    # We'll assume that the number of topics is 3 for now.
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=words,
                                           num_topics=25,
                                           random_state=2,
                                           update_every=1,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

    pprint(lda_model.print_topics(num_words=3))

    # Write to file using pprint
    with open("data_out/lda/"+doc[1].replace(".txt","") +"_topics.txt", "wt") as text_file:
        pprint(lda_model.print_topics(num_words=50), stream=text_file)

    lda_model.clear() # clear memory

