# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 13:42:31 2018

@author: drodr
"""

import numpy as np
import matplotlib.pyplot as mplot
import re
from os import listdir
from os.path import isfile, join

file=open("data_sent/sentiment_lex.csv", "r")
data=file.read()
data=data.split("\n")

lexicon_dictionary = {}

# populate the lexicon dictionary with keys (words) and value (value)
for line in data:
    lexicon_split = line.split(",")
    key = lexicon_split[0]
    value = lexicon_split[1]
    lexicon_dictionary[key] = float(value)

Negative = 0
Weakly_Negative = 0
Neutral = 0
Weakly_Positive = 0
Positive = 0

# ask for series name while ignoring the case of the name of the series
series_name = input("Enter the name of the series (A or B) : ").casefold()

# get all the files in the folder data_ch2
onlyfiles = [f for f in listdir("data_ch2") if isfile(join("data_ch2", f))]

# create a list of files to open depending on starting letter
openfiles = []
for file in onlyfiles:
    if file.startswith(series_name):
      openfiles.append(file)

for file in openfiles:

    script = open("data_ch2/" + file, "r")
    # reads the file
    words_unfiltered = script.read()
    # filters all the symbols and punctuations
    words_filtered = re.sub(r'[^\w\s]','', words_unfiltered)
    # lowers all lettters to lowercase
    words_filtered = words_filtered.lower()
    # splits the filtered words based on spaces
    words_split = words_filtered.split(" ")

    # dictionary to keep count of the words and their frequencies
    # checks if word is in dictionary
    # if word is in dictionary: it adds 1 to the count
    # if it is not in dictionary: it sets count equal to 1
    word_frequency_dictionary = {}
    for index in words_split:
        if index in word_frequency_dictionary:
            word_frequency_dictionary[index] += 1
        else:
            word_frequency_dictionary[index] = 1
    # checks if the word matches a word in the lexicon;
    # if it matches, it gets the value and adds it
    # to the count of the group it corresponds to
    for index in word_frequency_dictionary:
        if index in lexicon_dictionary:
           lexicon_value = lexicon_dictionary[index]
           if lexicon_value >= -1 and   lexicon_value < -0.6:
               Negative += word_frequency_dictionary[index]
           elif lexicon_value >= -0.6 and   lexicon_value < -0.2:
               Weakly_Negative += word_frequency_dictionary[index]
           elif lexicon_value >= -0.2 and   lexicon_value < 0.2:
               Neutral += word_frequency_dictionary[index]
           elif lexicon_value >= 0.2  and   lexicon_value < 0.6:
               Weakly_Positive += word_frequency_dictionary[index]
           elif lexicon_value >= 0.6 and   lexicon_value < 1:
               Positive += word_frequency_dictionary[index]


# populates xaxis with 5 bar graphs
xaxis=[1, 2, 3, 4, 5]
yaxis=[]

# populates y-axis with the values for each category
yaxis.append(Negative)
yaxis.append(Weakly_Negative)
yaxis.append(Neutral)
yaxis.append(Weakly_Positive)
yaxis.append(Positive)

# scales yaxis of the bar graph
yaxis=np.log10(yaxis)

mplot.bar(xaxis, yaxis)
mplot.xticks(xaxis, ["Neg", "W.Neg", "Neu", "W.Pos", "Pos"])
mplot.xlabel("Sentiment")
mplot.ylabel("Log Word Count")
mplot.title("Sentiment Analysis for Series " + series_name.upper())
mplot.show()
