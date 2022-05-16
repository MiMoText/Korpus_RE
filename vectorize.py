import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ###### Overview #################
# create dataframe
# 1 row lable, 1 row string
# every entry gets its own line
###################################

# create dataframe pos e1
# becomes useless ift countvectorizer reads csv
df_e1 = pd.read_csv("./Corpus/e1_pos_ex.csv", delimiter="\n")
# print(df_e1)

# ####### vectorize ###########
with open("./Corpus/e1_pos_ex.csv", encoding="utf-8") as file:
    data = file.readlines()

# print(type(data))
# print(data)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data)
vectorizer.get_feature_names()

print(X.toarray)


