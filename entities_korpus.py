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
#Passage Id can be split in sents and split over multiple lines/multiple lists
#relationship between entities and noun phrases
#print the nltk tree instead of the dep list
    # if there is only one sent
#-----------------------------------------------------------------------------------------------------------------------


# interessiern uns
# Multiple sent in passage:
    # - split and run, save in row with same passage_id?
    # - use json or txt or csv?

nlp = spacy.load("de_core_news_md",disable = ["lemmatizer"])
#nlp = spacy.load("en_core_web_md", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])

xlsx_paths = glob.glob("data_in/*.xlsx")  # Save the (relative) paths of all .txt files in a list
xlsx_paths = sorted(xlsx_paths)
print("{} text file(s) have been found. \n".format(len(xlsx_paths)))
print(xlsx_paths)

tags = ["<e1>", "<e2>", "<rel>", "</e1>", "</e2>", "</rel>"]
bad_chars =[ "[", "]", ] #If these chars appear they produce weird errors


def clean_passage(txt):
    for tag in tags:
        txt = txt.replace(tag, " ")
    for char in bad_chars:
        txt = txt.replace(char, "")
    while "  " in txt:
        txt = txt.replace("  ", " ")
    txt = txt.strip()

    return txt

def split_passage(txt):
    if "." in txt:
        txt = txt.split(".")[0]

def get_entities(txt,nlp):
    doc = nlp(txt)
    entities = []
    for ent in doc.ents:
        entities.append(ent.text)
    return entities

def subtree_matcher(text,nlp):
    doc = nlp(text)
    x = ''
    y = ''
    # iterate through all the tokens in the input sentence
    for i, tok in enumerate(doc):
        # extract subject
        if tok.dep_.find("subjpass") == True:
            y = tok.text
            # extract object
        if tok.dep_.endswith("obj") == True:
            x = tok.text

    return x, y

# now we define a function that will extract the subject and object of a sentence
def get_subject_object(text,nlp):
    doc = nlp(text)
    # iterate through all the tokens in the input sentence
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

def get_pos(txt,nlp):
    doc = nlp(txt)
    pos = []
    for token in doc:
        pos.append(token.pos_)
    return pos

def tok_format(tok):
    #return "_".join([tok.orth_, tok.dep_])
    return "_".join([tok.orth_, tok.pos_])

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

def get_dep(txt,nlp):
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

def get_noun_chunks(txt,nlp):
    doc = nlp(txt)
    noun_chunks = []
    for chunk in doc.noun_chunks:
        noun_chunks.append(chunk.text)
    return noun_chunks

def subtree_matcher(txt,nlp):
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

def pos_for_sentence(path,nlp):
    df = pd.DataFrame(columns=["id","token", "pos"])
    df_impo = pd.read_excel(path, sheet_name="Sheet1")


    for i, row in tqdm(df_impo.iterrows()):
        id0 = row["passage_id"]
        txt = row["passage_text"]

        id1= 1
        doc = nlp(txt)
        for token in doc:
            idx = str(id0) + "_" + str(id1)
            df = df.append({"id": idx, "token": token.text, "pos": token.pos_}, ignore_index=True)
            id1 += 1

    df.to_excel(path.replace(".xlsx", "_pos.xlsx"), index=False)
    return df

def create_df(xlsx_paths):
    df = pd.DataFrame(
        columns=["passage_id", "passage_text", "passage_entities", "noun_chunks", "subtree_match_1", "subtree_match_2", "aussage",
                 "filename", "pos", "dep"])

    for i in tqdm(range (len(xlsx_paths))):
        filename  = xlsx_paths[i].split("/")[1].split(".")[0]
        df_aux = pd.DataFrame(columns=["passage_id", "passage_text", "passage_entities", "noun_chunks","subtree_match_1","subtree_match_2", "aussage", "filename","pos","dep"])


        df_temp = pd.read_excel(xlsx_paths[i], sheet_name=0)


        df_aux["passage_text"] = df_temp["Passage"]
        df_aux["passage_text"] = df_aux["passage_text"].apply(lambda x :clean_passage(x))


        df_aux["passage_entities"] = df_aux["passage_text"].apply(lambda x: get_entities(x,nlp))
        df_aux["noun_chunks"] = df_aux["passage_text"].apply(lambda x: get_noun_chunks(x,nlp))
        df_aux["subtree_match_1"] = df_aux["passage_text"].apply(lambda x: get_subject_object(x,nlp))
        # df_aux["subject object"] = df_aux["passage_text"].apply(lambda x: get_subject_object(x,nlp))


        df_aux["pos"] = df_aux["passage_text"].apply(lambda x: get_pos(x,nlp))
        df_aux["dep"] = df_aux["passage_text"].apply(lambda x: get_dep(x,nlp))

        df_aux["aussage"] = df_temp["Aussage"]
        df_aux["filename"] = filename

        df = df.append(df_aux)

    df.reset_index(drop=True, inplace=True)
    df["passage_id"] = df.index
    df.to_excel("data_out/entity_korpus.xlsx", index=False)

    return df

def dep_to_json(path):
    df = pd.read_excel(path, sheet_name=0)
    df_dep = df[["dep"]]
    #use pandas to convert df to .json
    df_dep.to_json("data_out/entity_korpus.json", orient="records")

def dep_to_xml(path):
    df = pd.read_excel(path, sheet_name=0)
    df_dep = df[["dep"]]
    #use pandas to convert df to .json
    df_dep.to_xml("data_out/entity_korpus.xml", parser="etree")

def pos_to_xml(path):
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


#dfx = create_df(xlsx_paths).sample(5)
#print(dfx.to_string())

#dep_to_xml("data_out/entity_korpus.xlsx")
pos_to_xml("data_out/entity_korpus.xlsx")
#pos_for_sentence("data_out/entity_korpus.xlsx",nlp)
#-----------------------------------------------------------------------------------------------------------------------
textz = ["<e1>Die erotische Libertinage der Aufklärung steht eindeutig in der ungebrochenen Tradition laizistischen, materialistischen Denkens das vom Gassendismus des XVII. Jahrhunderts bis zu Helvétius reicht.",
"Der völlig triebgeleitete Don Juan Tirsos hat keine irdische Rache zu fürchten, seine Sünden werden durch unmittelbaren Eingriff der göttlichen Autorität geahndet."
, "Pädagogisches Engagement und <e2>der Versuch der Rührung</e2> <rel>anstelle der rationalen Überzeugung gehören dazu. Interessanterweise zeichnet</rel> <e1>Molière</e1> diese Intervention Elvires keineswegs als Karikatur, so wie er die traditionellen theologischen Positionen im Munde Sganarelles diskreditiert."
, "[In Tirso de Molinas <e1>Burlador de Sevilla</e1> <rel>(1630) allerdings, der als Prototyp den langen Reigen europäischer Don Juans eröffnet, ist von dieser Verknüpfung noch nichts zu merken.] Tirso geht es um die Stilisierung eines ins überdimensionale gesteigerten Sünders, dessen grausames Ende der Christenheit als Exemplum für die gerechte </rel><e2> Strafe Gottes</e2> dienen soll."
]
text = clean_passage(textz[2])
print(text)
print(get_dep(text,nlp))
#text = clean_passage(textz[1])
print(text)
print(get_dep(text,nlp))

doc = nlp(text)
#print doc dependency tree
#displacy.serve(doc, style='dep')

tree = Tree.fromstring('(S (NP Mary) (VP walks))')
#print(TreePrettyPrinter(tree).text())




#pptree = [to_nltk_tree(sent.root).pretty_print().text() for sent in doc.sents]


#print(pptree[0])


#from pprint import pprint

# Build the tree somehow

#with open('tree.txt', 'wt') as out:
#    pprint(pptree[0], stream=out)

#pprint(pptree[0])
#write to file

# save print output to a string
import io
import sys



#for i, tok in enumerate(doc):
#    print(tok.text, tok.dep_)
    #if tok.dep_.endswith("subj") == True:
     #   x = tok.text


#print(text)

#https://stackoverflow.com/questions/36610179/how-to-get-the-dependency-tree-with-spacy
#displacy.render(doc, style='dep',jupyter=True)
#for tok in doc:
 # print (tok.text, "-->",tok.dep_,"-->", tok.pos_)

#e1Span = Span(doc, 0, 1, label = "e1")
