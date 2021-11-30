import pandas as pd


# clean takes pandas dataframe as argument
def clean(my_dataframe):
    print("Cleaning Files:")
    my_dataframe.reset_index(drop=True, inplace=True)
    print(my_dataframe.info()) # why are there less non-null values in index (Unnamed) column? might be important

    print("\nInitial Shape:",my_dataframe.shape)

    # Spalte(n) raus / Anmerkung too?
    my_dataframe.drop(columns=["OCR-Absatz","Unnamed: 0"], inplace=True)# inplace=True: changes are made in original dataframe

    # Zeichen Clean-Up
    to_check_for = ["*", ";", ",", "\""] #List of characters to check for, we might be missing some though
    for index, row in my_dataframe.iterrows():# Go over each row
        for i in range(len(row)):               # Go over each cell
            cell_string = str(row[i])

            if cell_string[0] in to_check_for:
               #print("test",cell_string)

                cell_string = cell_string[1:].strip() # or just lstrip ? check later
                row[i] = cell_string # works apparently...

                #print("chec",row[i])

    # Zeilen-Clean-Up / un-/filtered split
    df_ungefiltert = my_dataframe.copy()


    for index in my_dataframe.index:
        check_rel = str(my_dataframe.loc[index, 'Relation'])
        check_post = (my_dataframe.loc[index, 'POST'])          #NaN values do not appear to be a problem
        if (check_rel == "relation out of scope") or (check_post == "ND") or (check_post == "RTS"): # RSU too?
            my_dataframe.drop([index], inplace=True)

    my_dataframe.reset_index(drop=True)

    #my_dataframe.info()
    print("Shape ungefiltert", df_ungefiltert.shape)
    print("Shape gefiltert", my_dataframe.shape)
    rows_droped = df_ungefiltert.shape[0] - my_dataframe.shape[0]
    print("Rows dropped:", rows_droped, "(", round(rows_droped*100/df_ungefiltert.shape[0],2), "% )\n")

    df_ungefiltert.to_csv("data_out/ungefiltert_cleaned.csv", index=False)
    my_dataframe.to_csv("data_out/gefiltert_cleaned.csv", index=False)

    return my_dataframe


