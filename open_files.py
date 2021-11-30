import glob
import os
import pandas as pd

# pd.options.display.max_columns = 999

def open_files():
    path = "data_in"
    files = os.listdir(path)
    print("Opening Files: ")

    # merging the files
    joined_files = os.path.join("data_in", "*.xlsx")

    # A list of all joined files is returned
    joined_list = glob.glob(joined_files)

    # merge files into one dataframe using pd.concat()
    global my_dataframe
    # It's worth noting that some tables do not have the "POST" column,
    #       this seems to be handled well by the concat() function. Keep in mind that columns may have different order in different files.
    #                                                                                    worst case: they have different names
    my_dataframe = pd.concat(map(pd.read_excel, joined_list), ignore_index=False, axis=0, sort=False)
    # get content overview
    #      --> sample file to check for irregularities
    my_sample = my_dataframe.sample(n=5)
    print("Sample Shape:", my_sample.shape)
    print(my_sample.to_string(),"\n")
    #print(my_sample.info())                        #print column names, Non-Null count, types
    #my_sample.to_csv("data_out/my_sample.csv")     #might be useful for debugging

    # pickle dataframe
    my_dataframe.to_pickle("./my_buffer/my_dataframe.infer")

    return my_dataframe


