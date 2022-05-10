import pandas as pd
import csv
import clean_stopwords
from tqdm import tqdm
tqdm.pandas()

#------
# MLP
#------

def lead_chars(text):
    '''
    Is applied to every column in the dataframe.
    Removes unwanted, leading characters from a string
     - eg. comma, semicolon, whitespace etc.
     - "<" is an exception, because it marks the begging of a tag
     - "(" is an exception too, if followed by alnum character
    '''

    #print("input:", text)
    text = str(text)

    #if len(text) > 2:
    while len(text) > 1 and (text[0].isalnum() == False):

        if (text[0] == "(") and (text[1].isalnum()):
            break
        if text[0] == "<":
            break

        text = text[1:].strip()

    #print("output:", text)
    return text

def clean(dataframe):
    '''
    Explanation:
    '''

    print("\n      Cleaning Files:\n")
    print("-----Data Table to be Cleaned:")

    dataframe.reset_index(drop=True, inplace=True)
    print(dataframe.info())
    print("\n")

    # Drop unnecessary columns
    # Unnamed:0 can be dropped too (legacy index)
    # inplace=True: changes are made in original dataframe
    dataframe.drop(columns=["OCR-Absatz", "Unnamed: 0", "Anmerkung", "Annotator*in"], inplace=True)

#----------Lead-Char Clean-Up for all columns with lambda function

    print("Leading-Char-Cleanup :")

    for i in range(len(dataframe.columns)):
        print("---> Column:", dataframe.columns[i])
        dataframe[dataframe.columns[i]] = dataframe[dataframe.columns[i]].apply(lambda x: lead_chars(x))


    print("-----> Done\n")

#-----------------------------------------------------
    # Before filtering, create a copy of the dataframe
    df_ungefiltert = dataframe.copy()

    print("Filter using Relation Values :")
    for index in tqdm(dataframe.index):
        check_rel = str(dataframe.loc[index, 'Relation'])

        # TODO comment
        check_post = str(dataframe.loc[index, 'POST'])

        #Check for marked (eg."ND") and unmarked errors
        if (check_rel == "relation out of scope") or (len(check_rel) < 2) or (check_rel == "nan") \
                or (check_post == "ND") or (check_post == "RTS"):
            dataframe.drop([index], inplace=True)

    dataframe.reset_index(drop=True)
    print("-----> Done\n")

    #-----------------

    print("Stopwords Clean-Up :")
    print("Columns to be cleaned: Relation, Passage, E1, E2")
    dataframe['Relation'] = dataframe['Relation'].progress_apply(lambda x: clean_stopwords.clean_sw(str(x)))
    dataframe['Passage'] = dataframe['Passage'].progress_apply(lambda x: clean_stopwords.clean_sw(str(x)))
    dataframe['E1'] = dataframe['E1'].progress_apply(lambda x: clean_stopwords.clean_sw(str(x)))
    dataframe['E2'] = dataframe['E2'].progress_apply(lambda x: clean_stopwords.clean_sw(str(x)))

    print("-----> Done\n")

    ##----------Post-Filter information
    rows_droped = df_ungefiltert.shape[0] - dataframe.shape[0]

    print("-----Data Tables after Cleaning:")
    print("Shape ungefiltert", df_ungefiltert.shape)
    print("Shape gefiltert", dataframe.shape)
    print("Rows dropped:", rows_droped, "(", round(rows_droped*100/df_ungefiltert.shape[0],2), "% )\n")
    # my_dataframe.info()

    df_ungefiltert.to_csv("data_out/ungefiltert_cleaned.csv", index=False, encoding="utf-8-sig", sep=";")
    dataframe.to_csv("data_out/gefiltert_cleaned.csv", index=False, encoding="utf-8-sig", sep=";")


    return dataframe
