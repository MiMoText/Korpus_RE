import pandas as pd
import glob
from tqdm import tqdm

from spacy.tokenizer import Tokenizer
from spacy.lang.de import German
tokenizer_de = Tokenizer(German().vocab)

#---
#MLP
#---

def generate_alias_table(alias_txt_path):

    txt_paths = glob.glob("data_in/KonVok_count/text_data/*.txt")

    #initialize tokenizer, dataframe
    tokenizer = tokenizer_de
    df = pd.DataFrame(columns=['Anzahl', 'Wort aus Vokabular', 'Tokennummer im Text', 'Passage', 'Name Datei'])

    # read each line of the alias file into string list
    with open(alias_txt_path, 'r', encoding='utf-8') as f:
        alias_list = f.read().split('\n')

    alias_list = sorted(alias_list)
    print(alias_list)

    for path in txt_paths:

        path_split = path.split('/')[-1]
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().replace('\n', ' ')

        # Tokenize the text
        doc = tokenizer(text)

        print('\nChecking File: ',path_split)

        for label in tqdm(alias_list):

            # Count the number of tokens that = label in that file
            count = [1 for token in doc if token.text == label]
            count = sum(count)

            for i in range(len(doc)):

                if label == doc[i].text:

                    #genereate string with 3 tokens after and 3 tokens before the label
                    if i > 3:
                        before = ' '.join([token.text for token in doc[i-3:i]])
                    else:
                        before = ' '.join([token.text for token in doc[0:i]])
                    if i < len(doc)-3:
                        after = ' '.join([token.text for token in doc[i+1:i+4]])
                    else:
                        after = ' '.join([token.text for token in doc[i+1:]])


                    to_append = [count, label, i, before + ' ' + label + ' ' + after, path_split]
                    #print(to_append)

                    # to_append is added to the end of the dataframe
                    df.loc[len(df)] = to_append

    df.to_excel('data_out/alias/alias_table.xlsx', index=False)
    df.to_csv('data_out/alias/alias_table.csv', index=False)
    df.to_csv('data_out/alias/alias_table.tsv', sep="\t",index=False)

    print('Done')

#----Main----
generate_alias_table('data_in/alias_input.txt')