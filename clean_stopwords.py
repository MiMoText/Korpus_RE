import spacy

# sm Model -> (klein) && Anzahl von Zeilen -> ca 4k
# =>> Laufzeit von ca 30 sek für sw filter.
nlp = spacy.load("de_core_news_sm")

special_char_excep = [" ","<",">","/"]

# string - > string ohne Stopwords und Sonderzeichen
def clean_sw(text):
    #alnum check
    for char in text:
        if (char.isalnum() == False) and (char not in special_char_excep):
            text = text.replace(char, "")

    # stopwords
    doc = nlp(text)     # token.lemma_ = base string
    stri = " ".join([token.lemma_ for token in doc if not token.is_stop])
    stri = stri.strip()

    #remove s and chen - case sensitive check, this

    if len(stri) > 4:
        if stri[:3] == "che":

            if stri[3] != " ":
                stri = stri[4:]
            else:
                stri = stri[3:]

        if ((stri[:2] == "n ") or (stri[:2] == "r ")):
            stri = stri[2:]

        if stri[:2] == "s ":
            stri = stri[2:]


        if "<rel>che" in stri:

            #only one will apply
            stri = stri.replace("<rel>chen ", "<rel>")
            stri = stri.replace("<rel>cher ", "<rel>")
            stri = stri.replace("<rel>ches ", "<rel>")
            stri = stri.replace("<rel>che ","<rel>")###

        if "<rel>s " in stri:
            stri = stri.replace("<rel>s ","<rel>")

    # whitespace check #do the tag strip here?
    while "  " in stri:
        stri = stri.replace("  ", " ")

    if "< " in stri:
        stri = stri.replace("< ", "<")

    if " >" in stri:
        stri = stri.replace(" >", ">")

    stri = stri.strip()
    return stri


####-------for Testing
#with open('Strings4Test_clean_sw.txt', 'r') as f:
 #   for line in f:
  #      print(line[:-1]) # -1 ist "newline"
   #     print(clean_sw(line)+"\n")



