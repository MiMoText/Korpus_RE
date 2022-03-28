import pandas as pd
import glob
from tqdm import tqdm
tqdm.pandas()

from spacy.tokenizer import Tokenizer

from spacy.lang.de import German
from spacy.lang.fr import French
from spacy.lang.en import English

tokenizer_de = Tokenizer(German().vocab)
tokenizer_fr = Tokenizer(French().vocab)
tokenizer_en = Tokenizer(English().vocab)

df_overall = pd.read_excel('data_out/KonVok_Korpus/KonVok_overall_count.xlsx')

df_de = df_overall[['MiMoText Label (de)','Count (de)']].copy()
df_fr = df_overall[['MiMoText Label (fr)','Count (fr)']].copy()
df_en = df_overall[['MiMoText Label (en)','Count (en)']].copy()

#print(df_de.info())

def count_label (label,tokenizer):
    txt_paths = glob.glob("data_in/KonVok_count/text_data/*.txt")  # Save the (relative) paths of all .xlsx files in a list
    count = 0

    for path in txt_paths:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        doc = tokenizer(text)   # Tokenize the text

        count_list = [1 for token in doc if token.text == label] # Counts the number of times the label occurs in the doc
        count += sum(count_list) # Sums up all the counts

    return [count, label]

def generate_count_table():

    df = pd.read_excel('data_in/KonVok_Korpus/KonVok Stringabgleich Seklit.xlsx', sheet_name='Themen-KonVok')
    df.info()

    df = df.drop(columns=['Wikidata Ids (zu DEL-Begriffen)','Wikidata URLs','Quelle','Match quality',
                        'Wikidata Label (fr)', 'Wikidata Label (en)','Wikidata Label (de)'])
    #print column names
    print(df.columns)


    print("\n Counting (fr) Labels...")
    df['MiMoText Label (fr) - Temp'] = df['MiMoText Label (fr)'].progress_apply(lambda x: count_label(x,tokenizer_fr))
    df.drop(columns=['MiMoText Label (fr)'], inplace=True) # Drop the original column

    # Sort the aux dataframe by the count in the column and replace it in the original dataframe
    df_aux = df['MiMoText Label (fr) - Temp'].tolist()
    df.drop(columns=['MiMoText Label (fr) - Temp'], inplace=True)

    df_aux.sort(key=lambda x: x[0], reverse=True)
    df_aux = pd.DataFrame(df_aux)

    df_aux.rename(columns={1: 'MiMoText Label (fr)'}, inplace=True)
    df_aux.rename(columns={0: 'Count (fr)'}, inplace=True)

    df = pd.concat([df, df_aux], axis=1)


    print("\n Counting (en) Labels...")
    df['MiMoText Label (en) - Temp'] = df['MiMoText Label (en)'].progress_apply(lambda x: count_label(x,tokenizer_en))
    df.drop(columns=['MiMoText Label (en)'], inplace=True) # Drop the original column

    # Sort the aux dataframe by the count in the column and replace it in the original dataframe
    df_aux = df['MiMoText Label (en) - Temp'].tolist()
    df.drop(columns=['MiMoText Label (en) - Temp'], inplace=True)

    df_aux.sort(key=lambda x: x[0], reverse=True)
    df_aux = pd.DataFrame(df_aux)

    df_aux.rename(columns={1: 'MiMoText Label (en)'}, inplace=True)
    df_aux.rename(columns={0: 'Count (en)'}, inplace=True)

    df = pd.concat([df, df_aux], axis=1)


    print("\n Counting (de) Labels...")
    df['MiMoText Label (de) - Temp'] = df['MiMoText Label (de)'].progress_apply(lambda x: count_label(x,tokenizer_de))
    df.drop(columns=['MiMoText Label (de)'], inplace=True) # Drop the original column

    # Sort the aux dataframe by the count in the column and replace it in the original dataframe
    df_aux = df['MiMoText Label (de) - Temp'].tolist()
    df.drop(columns=['MiMoText Label (de) - Temp'], inplace=True)

    df_aux.sort(key=lambda x: x[0], reverse=True)
    df_aux = pd.DataFrame(df_aux)

    df_aux.rename(columns={1: 'MiMoText Label (de)'}, inplace=True)
    df_aux.rename(columns={0: 'Count (de)'}, inplace=True)

    df = pd.concat([df, df_aux], axis=1)


    print(df.head(50).to_string())

    df.to_excel('data_out/KonVok_Korpus/KonVok_overall_count.xlsx', index=False) #Output All



def generate_top25_tables(df, lang):

    limit = 25
    txt_paths = glob.glob("data_in/KonVok_count/text_data/*.txt")  # Save the (relative) paths of all .xlsx files in a list
    df_all_labels = pd.DataFrame(columns=['Anzahl', 'Wort aus Vokabular', 'Tokennummer im Text', 'Passage', 'Name Datei'])

    if lang == '(en)':
        tokenizer = tokenizer_en
        suffix = '_en'
    elif lang == '(fr)':
        tokenizer = tokenizer_fr
        suffix = '_fr'
    elif lang == '(de)':
        tokenizer = tokenizer_de
        suffix = '_de'
    else:
        print('Language input not valid')
        return

    for row in tqdm(df.iterrows()):
        #create blank dataframe
        df_label_rows = pd.DataFrame(columns=['Anzahl','Wort aus Vokabular','Tokennummer im Text','Passage','Name Datei'])

        if limit == 0:
            break

        # save value at index i of column Count (en) to variable
        count = row[1]['Count ' + lang]
        label = row[1]['MiMoText Label ' + lang]


        limit -= 1
        #print(label, count,limit)

        # Generate entries for label
        for path in txt_paths:
            path_split = path.split('/')[-1]

            with open(path, "r", encoding="utf-8") as f:
                text = f.read().replace('\n', ' ')

            doc = tokenizer(text)  # Tokenize the text

            for i in range(len(doc)):
                #save the i th token in doc
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

                    to_append = [count, label, i, before+ ' ' + label + ' ' + after, path_split]
                    df_label_rows.loc[len(df_label_rows)] = to_append

        df_label_rows.to_excel('data_out/KonVok_Korpus/'+suffix+'/'+label+'.xlsx', index=False)
        #print(df_label_rows.sample(10).to_string())
        # Append the rows in df_label_rows to df_all_labels
        df_all_labels = df_all_labels.append(df_label_rows, ignore_index=True)
        #reset index
        df_all_labels.reset_index(drop=True, inplace=True)

    #export to excel
    df_all_labels.to_excel('data_out/KonVok_Korpus/KonVok_top25_occur' + suffix + '.xlsx', index=False)


#-------------Main-------------

#generate_count_table()

generate_top25_tables(df_de, '(de)')
generate_top25_tables(df_fr, '(fr)')
generate_top25_tables(df_en, '(en)')