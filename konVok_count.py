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

df = pd.read_excel('data_in/KonVok_count/KonVok Stringabgleich Seklit.xlsx', sheet_name='Themen-KonVok')
df.info()

df = df.drop(columns=['Wikidata Ids (zu DEL-Begriffen)','Wikidata URLs','Quelle','Match quality',
                        'Wikidata Label (fr)', 'Wikidata Label (en)','Wikidata Label (de)'])
#print column names
print(df.columns)


print("\n Counting (fr) Labels...")
df['MiMoText Label (fr) - COUNT'] = df['MiMoText Label (fr)'].progress_apply(lambda x: count_label(x,tokenizer_fr))
df.drop(columns=['MiMoText Label (fr)'], inplace=True) # Drop the original column

# Sort the aux dataframe by the count in the column and replace it in the original dataframe
df_aux = df['MiMoText Label (fr) - COUNT'].tolist()
df_aux.sort(key=lambda x: x[0], reverse=True)
df_aux = pd.DataFrame(df_aux)
df_aux['MiMoText Label (fr) - COUNT'] = df_aux[0].map(str) + ' - ' + df_aux[1]
df_aux = df_aux['MiMoText Label (fr) - COUNT']
df.drop(columns=['MiMoText Label (fr) - COUNT'], inplace=True)
df = pd.concat([df, df_aux], axis=1)


print("\n Counting (en) Labels...")
df['MiMoText Label (en) - COUNT'] = df['MiMoText Label (en)'].progress_apply(lambda x: count_label(x,tokenizer_en))
df.drop(columns=['MiMoText Label (en)'], inplace=True) # Drop the original column

# Sort the aux dataframe by the count in the column and replace it in the original dataframe
df_aux = df['MiMoText Label (en) - COUNT'].tolist()
df_aux.sort(key=lambda x: x[0], reverse=True)
df_aux = pd.DataFrame(df_aux)
df_aux['MiMoText Label (en) - COUNT'] = df_aux[0].map(str) + ' - ' + df_aux[1]
df_aux = df_aux['MiMoText Label (en) - COUNT']
df.drop(columns=['MiMoText Label (en) - COUNT'], inplace=True)
df = pd.concat([df, df_aux], axis=1)



print("\n Counting (de) Labels...")
df['MiMoText Label (de) - COUNT'] = df['MiMoText Label (de)'].progress_apply(lambda x: count_label(x,tokenizer_de))
df.drop(columns=['MiMoText Label (de)'], inplace=True) # Drop the original column

# Sort the aux dataframe by the count in the column and replace it in the original dataframe
df_aux = df['MiMoText Label (de) - COUNT'].tolist()
df_aux.sort(key=lambda x: x[0], reverse=True)
df_aux = pd.DataFrame(df_aux)
df_aux['MiMoText Label (de) - COUNT'] = df_aux[0].map(str) + ' - ' + df_aux[1]
df_aux = df_aux['MiMoText Label (de) - COUNT']
df.drop(columns=['MiMoText Label (de) - COUNT'], inplace=True)
df = pd.concat([df, df_aux], axis=1)

print(df.head(50).to_string())

df.to_excel('data_out/KonVok_count/KonVok_count.xlsx', index=False) #Output All
df.head(50).to_excel('data_out/KonVok_count/KonVok_count_TOP50.xlsx', index=False) #Output Top 50

