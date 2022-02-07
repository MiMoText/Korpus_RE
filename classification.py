import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import create_korpus_re
from collections import Counter
import os
from wordcloud import WordCloud
from PIL import Image

def classification():
    df = pd.read_pickle("my_buffer/korpus_entities.infer")
    print(df.info())

    # print(df.loc["relation out of scope"])
    df_test = df.set_index("Relation")
    print(df_test)


    df_topic_interest = df[df["Code des Typs"] == "topicInterest"]

    list_topic_interest = df_topic_interest["Relation"].tolist()
   # print(list_topic_interest)

    print(Counter(list_topic_interest))
    # man sieht, dass sich hier noch gar nichts doppelt
    # --> bag of word für weitere Einblicke
    # todo relation out of scope rauskicken
    string_topic_interest = "".join(list_topic_interest)
    # print(string_topic_interest)
    string_topic_interest = string_topic_interest.lower()
    # wordcloud = WordCloud().generate(list_topic_interest)

    wordcloud = WordCloud(background_color="white").generate(string_topic_interest)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()