import pandas as pd


# clean takes pandas dataframe as argument
def clean(my_dataframe):
    print("Möp")
    print(my_dataframe.columns)
# Spalte Anmerkungen raus
    my_dataframe.drop(columns=["OCR-Absatz"])
# führende kommata, semikolon, anführungszeichen
# asterisken
# lösche alle zeilen mit relation out of scope
# lösche alle zeilen mit problemanmerkungen in der letzten spalte

# Moment, ich muss das alles gar nicht machen. Ich habe ja die Passage-Spalte, in der das schon annotiert drin steht.
# Ich muss: das alles in ein txt-file packen. Hintereinanderpacken 1 sentence/line.
