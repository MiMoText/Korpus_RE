import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# ###### Overview #################
# https://towardsdatascience.com/how-to-build-your-first-spam-classifier-in-10-steps-fdbf5b1b3870
# create dataframe
# 1 row lable, 1 row string
# lables: e1, e2, rel, neg
# every entry gets its own line
###################################

# create dataframe pos e1
# becomes useless ift countvectorizer reads csv
df_e1 = pd.read_csv("./Corpus/e1_pos_ex.csv", delimiter="\n")
df_e2 = pd.read_csv("./Corpus/e2_pos_ex.csv", delimiter="\n")
df_rel = pd.read_csv("./Corpus/rel_pos_ex.csv", delimiter="\n")
df_neg = pd.read_csv("./Corpus/neg_ex.csv", delimiter="\n")

dataframes = [df_e1, df_e2, df_rel, df_neg]

final_frame = pd.concat(dataframes, sort=False)
final_frame.columns =["e1", "e2", "rel", "neg"]

print(final_frame)

print(final_frame["e1"].value_counts())







"""
# ####### vectorize ###########
with open("./Corpus/e1_pos_ex.csv", encoding="utf-8") as file:
    data = file.readlines()

# print(type(data))
# print(data)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data)
vectorizer.get_feature_names()

# print(X.toarray)
"""

