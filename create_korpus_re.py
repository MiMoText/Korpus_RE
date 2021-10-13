import pandas as pd
import open_files
import csv


my_dataframe = open_files.open_files()

selected_rows = my_dataframe[(my_dataframe["Code des Typs"] == "about") | (my_dataframe["Code des Typs"] == "topicInterest")]

print(selected_rows.sample(n=15))

# keep column D "Aussage"
my_column = selected_rows[["Passage", "Code des Typs"]].copy()
my_column.to_csv("data_out/korpus_re.csv")

with open('data_out/korpus_re.csv', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile)
    # delete korpus re, dann muss ich das neue nicht umbenennen
    # oder einfach überschreiben
    with open("data_out/korpus_re2.csv", "w", encoding="utf-8") as csvfile2:
        for row in spamreader:
            csvfile2.writelines(row[1:2])
            csvfile2.write("\n")
            csvfile2.writelines(row[2])
            csvfile2.write("\n\n")
            # tut was es soll
            # zeilen rausfischen, die den falschen Zusammenhang haben mache ich im open/clean modul


# auf der konsole erscheint noch info zu sample data
# das muss weg



my_column.to_csv("data_out/korpus_re.csv", index=False)