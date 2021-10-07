import glob
import os
import pandas as pd

# pd.options.display.max_columns = 999

def open_files():
    path = "data_in"
    files = os.listdir(path)

    # merging the files
    joined_files = os.path.join("data_in", "*.xlsx")

    # A list of all joined files is returned
    joined_list = glob.glob(joined_files)
    # merge files into one dataframe using pd.concat()
    global my_dataframe
    my_dataframe = pd.concat(map(pd.read_excel, joined_list), ignore_index=False, axis=0, sort=False)

    # show all column heads
    my_columns = list(my_dataframe.columns)
    print(my_columns)

    # get content overview
    my_sample = my_dataframe.sample(n=15)
    print(my_sample)
    my_sample.to_csv("data_out/my_sample.csv")
    # chart too wide to get content overview
    # --> get sample file to check for irregularities

    # pickle dataframe
    my_dataframe.to_pickle("./my_buffer/my_dataframe.infer")

    return my_dataframe


