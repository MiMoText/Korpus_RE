import pandas as pd
import create_korpus_re
from collections import Counter

# gibt es Sinn als einfachste Variante erstmal eine
# binäre Klassifikation zu implementieren, also relation - keine relation?
# ich glaube nicht

df = pd.read_pickle("my_buffer/korpus_entities.infer")
#print(df)
#print(df.columns)
# most frequent words in relation

# print(df.loc["relation out of scope"])
df_test = df.set_index("Relation")
print(df_test)


df_topic_interest = df[df["Code des Typs"] == "topicInterest"]

list_topic_interest = df_topic_interest["Relation"].tolist()
print(list_topic_interest)

print(Counter(list_topic_interest))
# man sieht, dass sich hier noch gar nichts doppelt
# --> bag of word für weitere Einblicke


