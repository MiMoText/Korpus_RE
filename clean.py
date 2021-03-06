import pandas as pd
import csv
import clean_stopwords

# clean takes pandas dataframe as argument
def clean(my_dataframe):
    print("-----Cleaning Files:\n")
    my_dataframe.reset_index(drop=True, inplace=True)

    print("-----Data Table to be Cleaned:")
    print(my_dataframe.info())# Unnamed:0 can be dropped (legacy index)
    print("\n")

    # Spalte(n) raus
    my_dataframe.drop(columns=["OCR-Absatz","Unnamed: 0","Anmerkung","Annotator*in"], inplace=True)# inplace=True: changes are made in original dataframe

    # Lead-Zeichen Clean-Up
    for index, row in my_dataframe.iterrows():  # Go over each row
        for i in range(len(row)):               # Go over each cell
            cell_string = str(row[i])          # strip? ***
            if len(cell_string) > 2:
                while len(cell_string) > 0 and (cell_string[0].isalnum() == False):

                    if (cell_string[0] == "(") and (cell_string[1].isalnum()):
                        break
                    if cell_string[0] == "<":
                        break

                    cell_string = cell_string[1:].strip()
                    row[i] = cell_string
                    #print("check",row[i])

    # Zeilen-Clean-Up & un-/filtered split
    df_ungefiltert = my_dataframe.copy()
    for index in my_dataframe.index:
        check_rel = str(my_dataframe.loc[index, 'Relation'])
        check_post = str(my_dataframe.loc[index, 'POST'])          #NaN values do not appear to be a problem
        #Check for marked and unmarked errors
        if (check_rel == "relation out of scope") or (len(check_rel) < 2) or (check_rel == "nan") \
                or (check_post == "ND") or (check_post == "RTS"):# RSU too? ***
            my_dataframe.drop([index], inplace=True)

    my_dataframe.reset_index(drop=True)

    # Stopwords clean-up, small fixes ---> gefiltert.csv
    # columns : Passage, Relation, E1&E2
    counter = 0 # für Laufzeit Abschätzung

    for index in my_dataframe.index:
        counter += 1
        check_rel = str(my_dataframe.loc[index, 'Relation'])
        check_pass = str(my_dataframe.loc[index, 'Passage'])
        check_e1 = str(my_dataframe.loc[index, 'E1'])
        check_e2 = str(my_dataframe.loc[index, 'E2'])

        my_dataframe.loc[index, 'Relation'] = clean_stopwords.clean_sw(check_rel)
        my_dataframe.loc[index, 'Passage'] = clean_stopwords.clean_sw(check_pass)
        my_dataframe.loc[index, 'E1'] = clean_stopwords.clean_sw(check_e1)
        my_dataframe.loc[index, 'E2'] = clean_stopwords.clean_sw(check_e2)

        if counter % 100 == 0:
            print("Zeilen auf sw gecheckt:",counter)


    #Drop information
    #my_dataframe.info()
    print("-----Data Tables after Cleaning:")
    print("Shape ungefiltert", df_ungefiltert.shape)
    print("Shape gefiltert", my_dataframe.shape)
    rows_droped = df_ungefiltert.shape[0] - my_dataframe.shape[0]
    print("Rows dropped:", rows_droped, "(", round(rows_droped*100/df_ungefiltert.shape[0],2), "% )\n")

    df_ungefiltert.to_csv("data_out/ungefiltert_cleaned.csv", index=False, encoding="utf-8-sig", sep=";")
    my_dataframe.to_csv("data_out/gefiltert_cleaned.csv", index=False, encoding="utf-8-sig", sep=";")


    return my_dataframe


