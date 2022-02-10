
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS # need stopwords here?

import spacy
from spacy.lang.fr.stop_words import STOP_WORDS

topic_list = []
nlp = spacy.load('de_core_news_sm')

for word in STOP_WORDS: #add french stopwords to spacy stopwords
    lexeme = nlp.vocab[word]
    lexeme.is_stop = True

def korpus_wordcloud(path):
#-----------------LDA Topics------------------
    if "_topics" in path: # if it is a lda topic file :
        with open(path, 'r') as f:
            test = f.read()

             # Here we might want to adjust the code for the lda topic file
                # to get the topic number and the topic names, and then words
                    # for now, however, we will just use frequency of words within the topics
                        # to keep the code flexible. further adjustments will be made when lda is done

        doc = nlp(test)
        doc = [token.text for token in doc if not token.is_stop and not token.is_punct and len(token.text) > 2]
                                #token critera: not stopword, not punctuation, not too short

        #-----------------
        test_fq = []
        for token in doc: # iterate over tokens to create unique word list first
            if token not in test_fq:  # that way we avoid O(n^3) complexity
                test_fq.append(token)


        test_fq = [(doc.count(word),word) for word in test_fq] #(count,word) tupel list

        #sort by count, which is first element of each tuple
        test_fq.sort(key=lambda x: x[0], reverse=True)
        test_fq = [x[1] for x in test_fq[:75]] # take only the top 75 words

        #------------------------------------
        # Create a WordCloud object
        wordcloud = WordCloud(width=1600, height=900, max_words=75, background_color='white',
                              stopwords=STOPWORDS, min_font_size=10).generate(' '.join(test_fq))

        # Display the generated image:
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        #plt.savefig("lda/LDA_wordcloud_" + path.split("/")[-1].replace(".txt","") + ".png")

    # ---------------TXT FQ-----------------------------------------
    else: # if it is a txt file

        with open(path, 'r') as f:
            test = f.read().replace('\n', ' ')

        doc = nlp(test)
        doc = [token.text for token in doc if not token.is_stop and not token.is_punct and len(token.text) > 2]
                                #token critera: not stopword, not punctuation, not too short

        #------------------------------------
        test_fq = []
        for token in doc: # iterate over tokens to create unique word list first
            if token not in test_fq:  # that way we avoid O(n^3) complexity
                test_fq.append(token)

        test_fq = [(doc.count(word),word) for word in test_fq] #(count,word) tupel list

        #sort by count, which is first element of each tuple
        test_fq.sort(key=lambda x: x[0], reverse=True)
        test_fq = [x[1] for x in test_fq[:75]] # take only the top 75 words

        #------------------------------------
        # Create a WordCloud object
        wordcloud = WordCloud(width=1600, height=900, max_words=75, background_color='white',
                              stopwords=STOPWORDS, min_font_size=10).generate(' '.join(test_fq))

        # Display the generated image:
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        #plt.savefig("lda/FQ_wordcloud_" + path.split("/")[-1].replace(".txt","") + ".png")


def korpus_pie(table_path):

    #table = pd.read_csv(table_path, sep=";")
    df = pd.read_excel(table_path) # testing

    # ------------- Example logic here ------
    dfx = df['Code des Typs'].value_counts() # returns a df with (value,count) rows for each value
    dfx = dfx.to_dict() # convert to dict
    total = sum(dfx.values())# sum of all values in dict, needed for % calculation
                        # there are only "about" and "tI" values in this table
    sizes = []

    sizes.append((dfx["topicInterest"] *100)  /total) # Order of the values in the list is important
    sizes.append((dfx["about"] * 100) / total)
    if "other" in dfx.keys():
        sizes.append((dfx["other"] * 100) / total)
    else:
        sizes.append(0)

    # ------------------------------------

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = ["topicInterest","about","other"] #['Nicht-Sinnvoll', 'Sinnvoll', 'Neutral']
    #sizes = [14.5, 29.5, 55] # size of the slices in percentages (from Table logic)
    explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Sinvoll')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%' ,shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
    # plt.savefig("data_out/lda/piechart_" + path.split("/")[-1].replace(".txt","") + ".png")

#-----------------Visualisation------------------------------------------------------------------

#korpus_pie("data_out/lda/table.csv")
#korpus_pie("data_in/Baasner Libertinage und Empfindsamkeit_156.xlsx") # for testing

korpus_wordcloud("data_in/lda/Brockmeier_Wetzel.txt")
korpus_wordcloud("data_out/lda/Brockmeier_Wetzel_topics.txt")