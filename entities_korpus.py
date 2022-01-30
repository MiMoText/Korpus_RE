import spacy
import pandas as pd
from nltk.treeprettyprinter import TreePrettyPrinter
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
import glob
from nltk.tree import Tree
from tqdm import tqdm
import xml
#-----------------------------------------------------------------------------------------------------------------------

# load spacy, disable spacy lemmatizer ( we can also disable : disable=["tok2vec", "tagger", "parser", "attribute_ruler"]
nlp = spacy.load("de_core_news_md",disable = ["lemmatizer"])

xlsx_paths = glob.glob("data_in/*.xlsx")  # Save the (relative) paths of all .xlsx files in a list
xlsx_paths = sorted(xlsx_paths) # Sort list of paths by filename, so they correspond to the order of the files in our folder
print("{} text file(s) have been found. \n".format(len(xlsx_paths)))
print(xlsx_paths)

tags = ["<e1>", "<e2>", "<rel>", "</e1>", "</e2>", "</rel>"] #used for cleaning the text
bad_chars =[ "[", "]", ] # these chars may cause errors
#----------------------FUNCTIONS------------------------------------------------------------------------------------------
def clean_passage(txt):
    ''' clean the passage txt, remove tags, bad chars, etc'''
    for tag in tags:
        txt = txt.replace(tag, " ")
    for char in bad_chars:
        txt = txt.replace(char, "")
    while "  " in txt:
        txt = txt.replace("  ", " ")
    txt = txt.strip()

    return txt

def split_passage(txt):
  # not needed as of now, but we might want to split passages into sentences
  return txt


def get_entities(txt,nlp):
    '''returns spacy-identified entities in from doc, given a passage txt  '''
    doc = nlp(txt)
    entities = []
    for ent in doc.ents:
        entities.append(ent.text)
    return entities


def get_pos(txt,nlp):
    '''returns spacy-identified pos in from doc, given a passage txt '''
    doc = nlp(txt)
    pos = []
    for token in doc:
        pos.append(token.pos_)
    return pos

def get_noun_chunks(txt,nlp):
    '''returns spacy-identified noun-chunks in from doc, given a passage txt '''
    doc = nlp(txt)
    noun_chunks = []
    for chunk in doc.noun_chunks:
        noun_chunks.append(chunk.text)
    return noun_chunks


def tok_format(tok):
    '''used for ascii dep/pos tree'''
    #return "_".join([tok.orth_, tok.dep_])
    return "_".join([tok.orth_, tok.pos_])

def to_nltk_tree(node):
    '''used for ascii dep/pos tree'''
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

def get_dep(txt,nlp):
    ''' return list of dep if passage has multiple sentences
        return ascii dep/pos tree if only one sentence (see tok_format)'''

    doc = nlp(txt)
    doc_len = 0
    for sent in doc.sents:
        doc_len += 1

    if doc_len != 1:
        dep = []
        for token in doc:
            dep.append(token.dep_)
        return dep

    else:
        pptrees = [to_nltk_tree(sent.root) for sent in doc.sents]
        pptree = TreePrettyPrinter(pptrees[0]).text()
        return pptree

def get_subject_object(text,nlp):
    ''' reference function. not done yet'''
    doc = nlp(text)
    z =""
    y = ""
    for i, tok in enumerate(doc):
        # extract subject
        if tok.dep_.find("sb") == True:
            z = tok.text
            # extract object
        if tok.dep_.endswith("oa") == True:
            y = tok.text

    return z, y



def subtree_matcher(txt,nlp):
    ''' reference function. not done yet'''
    doc = nlp(txt)
    subjpass = 0

    for i, tok in enumerate(doc):
        # find dependency tag that contains the text "subjpass"
        if tok.dep_.find("subjpass") == True:
            subjpass = 1

    x = ''
    y = ''

    # if subjpass == 1 then sentence is passive
    if subjpass == 1:
        for i, tok in enumerate(doc):
            if tok.dep_.find("subjpass") == True:
                y = tok.text

            if tok.dep_.endswith("obj") == True:
                x = tok.text

    # if subjpass == 0 then sentence is not passive
    else:
        for i, tok in enumerate(doc):
            if tok.dep_.endswith("subj") == True:
                x = tok.text

            if tok.dep_.endswith("obj") == True:
                y = tok.text

    return x, y

#----------------------MAIN------------------------------------------------------------------------------------------

def pos_for_sentence(path,nlp):
    ''' read a xlsx file to pandas.
            for each token in a passage: get its pos and write them both to row in a new xlsx file
            each passage has an id, which represents the first group of the id tag. The second group is the token id.
            !!! Takes a while to run. !!!
    '''
    df = pd.DataFrame(columns=["id","token", "pos"])
    df_impo = pd.read_excel(path, sheet_name="Sheet1")


    for i, row in tqdm(df_impo.iterrows()):
        id0 = row["passage_id"]
        txt = row["passage_text"]

        id1= 1
        doc = nlp(txt)
        for token in doc:
            idx = str(id0) + "_" + str(id1) # construct id
            df = df.append({"id": idx, "token": token.text, "pos": token.pos_}, ignore_index=True) #add data to new df
            id1 += 1 #increment token id

    df.to_excel(path.replace(".xlsx", "_pos.xlsx"), index=False)
    return df

def create_df(xlsx_paths):
    ''' create new df/xlsx file, that contains all passages, and multiple entity extraction results for comparison '''

    #initialize new df. we will append all aux dataframes to this one
    df = pd.DataFrame(
        columns=["passage_id", "passage_text", "passage_entities", "noun_chunks", "subtree_match_1", "subtree_match_2", "aussage",
                 "filename", "pos", "dep"])

    for i in tqdm(range (len(xlsx_paths))):
        filename  = xlsx_paths[i].split("/")[1].split(".")[0] #extract filename
        # init aux dataframe
        df_aux = pd.DataFrame(columns=["passage_id", "passage_text", "passage_entities", "noun_chunks","subtree_match_1","subtree_match_2", "aussage", "filename","pos","dep"])

        # read the i'th xlsx file
        df_temp = pd.read_excel(xlsx_paths[i], sheet_name=0)


        df_aux["passage_text"] = df_temp["Passage"] # add passage text to aux df
        df_aux["passage_text"] = df_aux["passage_text"].apply(lambda x :clean_passage(x)) # clean passage text


        df_aux["passage_entities"] = df_aux["passage_text"].apply(lambda x: get_entities(x,nlp)) # get spacy-entities from passage text
        df_aux["noun_chunks"] = df_aux["passage_text"].apply(lambda x: get_noun_chunks(x,nlp)) #get spacy-noun chunks from passage text
        df_aux["subtree_match_1"] = df_aux["passage_text"].apply(lambda x: get_subject_object(x,nlp)) # reserved for subtree matching
        # df_aux["subtree_match_2"] = df_aux["passage_text"].apply(lambda x: get_subject_object(x,nlp)) # reserved for subtree matching


        df_aux["pos"] = df_aux["passage_text"].apply(lambda x: get_pos(x,nlp)) # get pos from passage text
        df_aux["dep"] = df_aux["passage_text"].apply(lambda x: get_dep(x,nlp)) # get dep from passage text

        df_aux["aussage"] = df_temp["Aussage"] # add aussage to aux df
        df_aux["filename"] = filename # add filename to aux df

        df = df.append(df_aux) # append aux df to main df

    df.reset_index(drop=True, inplace=True)
    df["passage_id"] = df.index #give each passage an id
    df.to_excel("data_out/entity_korpus.xlsx", index=False)#write df to xlsx file

    return df


def dep_to_xml(path):
    'used to export ascii dep trees to xml'
    df = pd.read_excel(path, sheet_name=0)
    df_dep = df[["dep"]]
    #use pandas to convert df to .json
    df_dep.to_xml("data_out/entity_korpus.xml", parser="etree")

def pos_to_xml(path):
    'used to export ascii pos trees to xml'
    df = pd.read_excel(path, sheet_name=0)
    df_text = df[["passage_text"]]
    df_pos = pd.DataFrame(columns=["pos"])
    # iterate over df_pos
    for i, row in df_text.iterrows():

        text = row["passage_text"]
        doc = nlp(text)
        doc_len = 0
        for sent in doc.sents:
            doc_len += 1

        if doc_len != 1:
            dep = []
            for token in doc:
                dep.append(token.dep_)
            df_pos = df_pos.append({"pos": dep}, ignore_index=True)

        else:
            pptrees = [to_nltk_tree(sent.root) for sent in doc.sents]
            pptree = TreePrettyPrinter(pptrees[0]).text()
            df_pos = df_pos.append({"pos": pptree}, ignore_index=True)

    df_pos.to_xml("data_out/entity_korpus_pos.xml", parser="etree")


#dfx = create_df(xlsx_paths).sample(5) #create df with all passages and entity extraction results, sample 5 rows
#print(dfx.to_string()) # print sample

#dep_to_xml("data_out/entity_korpus.xlsx")
#pos_to_xml("data_out/entity_korpus.xlsx")
#pos_for_sentence("data_out/entity_korpus.xlsx",nlp)

#---------DISPLACY EXAMPLE (might be useful)-------------------------------------------------------------------------------------------------------------
text = "<e1>Die erotische Libertinage der Aufklärung steht eindeutig in der ungebrochenen Tradition laizistischen, materialistischen Denkens das vom Gassendismus des XVII. Jahrhunderts bis zu Helvétius reicht."
text = clean_passage(text)
doc = nlp(text)
#displacy.serve(doc, style='dep')
