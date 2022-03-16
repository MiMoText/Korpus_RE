import glob
import pandas as pd
import re


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

    # print(full_text_passage)


        #entities = re.search("<e.*</e", passage_string)
        #print(entities)

        # todo change pandas dtype to string
        # dtype=string
        
        # filename = glob.glob("./data_out/NB_Corpus/*.txt")





