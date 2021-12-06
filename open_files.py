import glob
import os
import pandas as pd


def open_files():
    path = "data_in"
    files = os.listdir(path)
    print("-----Opening Files: ",len(files),"found")

    # merging the files
    joined_files = os.path.join("data_in", "*.xlsx")

    # A list of all joined files is returned
    joined_list = glob.glob(joined_files)

    # merge files into one dataframe using pd.concat()
    global my_dataframe

    my_dataframe = pd.concat(map(pd.read_excel, joined_list), ignore_index=False, axis=0, sort=False)
    # get content overview
    #      --> sample file to check for irregularities
    my_sample = my_dataframe.sample(n=7)
    print("Samples:")
    print(my_sample.to_string(),"\n")
    print("Column List:")
    print(my_dataframe.columns)


    # pickle dataframe
    my_dataframe.to_pickle("./my_buffer/my_dataframe.infer")

    return my_dataframe


