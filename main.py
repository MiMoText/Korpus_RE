import pandas as pd
import open_files
import clean


# read files - check :-)
# my_data = open_files.open_files()
# anpassung: pandas read excel

# wo liegen die ganzen files von pojoni - check :-)


# clean data (remove punctuation and special characters)
my_data = pd.read_pickle("./my_buffer/my_dataframe.infer")
clean.clean(my_data)
# Do I need a simple split here?

# Tagging semeval, one sentence per line

# write output (write to csv)