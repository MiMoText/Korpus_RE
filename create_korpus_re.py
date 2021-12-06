import csv


def create_korpus_re(my_dataframe):

    print("-----Create Korpus RE")
    # Relevante Zeilen aus Dataframe auswählen
    selected_rows = my_dataframe[(my_dataframe["Code des Typs"] == "about") | (my_dataframe["Code des Typs"] == "topicInterest")]

    # Export korpus_re.csv
    my_column = selected_rows[["Passage", "Code des Typs", "Aussage"]].copy()
    my_column.to_pickle("my_buffer/korpus_passagen.infer")
    my_column.to_csv("data_out/korpus_re.csv", index=False, encoding="utf-8-sig",sep=";")
    print("korpus_re.csv written to data_out/")

    # Pickle korpus_entities.infer
    my_entity_korpus = selected_rows[["E1", "E2", "Relation", "Code des Typs"]].copy()
    my_entity_korpus.to_pickle("my_buffer/korpus_entities.infer")

    file_object = open('data_out/korpus_re.csv', 'r', encoding="utf-8")
    korpus_re_obj = csv.reader(file_object, delimiter=";")

        # delete korpus re, dann muss ich das neue nicht umbenennen *** # oder einfach überschreiben

    # in korpus_re2.csv schreiben wir für jede Zeile aus korpus_re.csv
    # Passage\n Code des Typs \n\n
    file_object2 = open('data_out/korpus_re2.csv', 'w', encoding="utf-8")
    korpus_re2_obj = csv.writer(file_object2, delimiter=";")

    # Wenn row ein String ist, wird dieser als Liste interpretiert.
    # ----> Beim Schreiben mit csv.writer.writerow(row) muss row eine Liste sein die den String enthält.
    passage_list = ["","\n"]
    code_des_typs_list = ["","\n"]

    for row in korpus_re_obj:
        passage_list[0] = row[0]
        korpus_re2_obj.writerow(passage_list)

        code_des_typs_list[0] = row[1]
        korpus_re2_obj.writerow(code_des_typs_list)

        korpus_re2_obj.writerow("\n")

    file_object.close()
    file_object2.close()
    print("korpus_re2.csv written to data_out/")



