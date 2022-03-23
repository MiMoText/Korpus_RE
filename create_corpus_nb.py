import glob
import pandas as pd
import re
from nltk import tokenize

# by KD
# Alle Entities in handannotierten Texten finden

filelist = glob.glob("./data_in/*.csv")
print("The following files were found: \n")
print(filelist)

for file in filelist:
    f = open(file, encoding="ansi")
    print(file + "has been opened ")
    full_text = pd.read_csv(f, delimiter=";")
    # print(full_text)
    f.close()

    full_text_passage = full_text.filter(["Passage"])
    full_text_passage.to_csv("test.csv")

f = open("test.csv", encoding="utf-8")
full_text_string = f.read()
f.close()


print(full_text_string)
print(type(full_text_string))


entities = re.findall("<e2>.*</e2>", full_text_string)
print(entities)

my_string = "test <e2> test"
my_string_stripped = my_string.replace("<e2>", "")
print(my_string_stripped)


# filename = glob.glob("./data_out/NB_Corpus/*.txt")





