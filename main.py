import pandas as pd
from clean import clean
from open_files import open_files
from create_korpus_re import create_korpus_re
#from classification import classification
# --! causes exit code 139 (interrupted by signal 11: SIGSEGV) error on import

#read xlsx file(s) into df; return df /+write dataframe to .infer pickle file
open_files()
my_data = pd.read_pickle("./my_buffer/my_dataframe.infer")

# clean data (remove punctuation and special characters, drop some columns & rows)
# ; return df /+ pickle df /+ write .csv(s) to data_out/
my_data_clean = clean(my_data)
#print(my_data_clean.head())

# create korpus; selected columns /+ pickle df /+ write .csv(s) to data_out/
create_korpus_re(my_data_clean)

# classification
#classification()

# Tagging semeval, one sentence per line