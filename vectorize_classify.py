import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
from wordcloud import WordCloud
from PIL import Image
from sklearn.model_selection import train_test_split

# ###### Overview #################
# https://towardsdatascience.com/how-to-build-your-first-spam-classifier-in-10-steps-fdbf5b1b3870
# create dataframe
# column1: label
# column2: text
# used labels: e1, e2, rel, neg_ex
###################################

my_dataframe = pd.read_csv("./Corpus/corpus.csv", delimiter=",")
print(my_dataframe)

# exploring the dataset
print(my_dataframe["label"].value_counts())

df_e1 = my_dataframe[my_dataframe.label == "e1"]
# print(df_e1)
df_e2 = my_dataframe[my_dataframe.label == "e2"]
df_rel = my_dataframe[my_dataframe.label == "rel"]
df_neg_ex = my_dataframe[my_dataframe.label == "neg_ex"]


my_dataframe["label"] = my_dataframe["label"].apply(lambda x:
                                                    1 if x == "e1" or x == "e2" or x == "rel"
                                                    else 0)

x_train, x_test, y_train, y_test = train_test_split(my_dataframe["text"], my_dataframe["label"], test_size=0.3, random_state=0)

print("rows in test set: " + str(x_test.shape))
print("rows in train set: " + str(x_train.shape))
# 172 Elemente in Test
# 400 Elemente in Train

lst = x_train.tolist()
vectorizer = TfidfVectorizer(
    input=lst,
    lowercase=True,
)

features_train_transformed = vectorizer.fit_transform(x_train.values.astype("U"))
features_test_transformed = vectorizer.transform(x_test.values.astype("U"))

classifier = MultinomialNB()
result = classifier.fit(features_train_transformed, y_train)

print(result)

print("classifier accuracy {:.2f}%".format(classifier.score(features_test_transformed, y_test) * 100))


# TODO multilabel classifier
# todo mit zwei labeln
# e1 + alles andere
# e2 + alles andere
# rel + alles andere
# therefore change this statement:
"""my_dataframe["label"] = my_dataframe["label"].apply(lambda x:
                                                    1 if x == "e1" or x == "e2" or x == "rel"
                                                    else 0)"""