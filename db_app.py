from flask import Flask, render_template, request
import mysql.connector

cnx = mysql.connector.connect(user='root', database='chatbot')
cursor = cnx.cursor()


app = Flask(__name__)
import nltk

from nltk.stem.lancaster import LancasterStemmer
# word stemmer
stemmer = LancasterStemmer()

import json
training_data = []
with open(r"intents.json", encoding="utf8") as f:
    reader = json.load(f)
read = [{}]
dicti = {}
j=0
for i in reader['intents']:
    for k in i['patterns']:
        dicti = {"class":i["tag"],"sentence":k}
        training_data.append(dicti)
#print(training_data)

#print(len(training_data))

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = set([a['class'] for a in training_data])

for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1
            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
#print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
#print ("Class words: %s" % class_words)

#calculate a score for a given class taking into account word commonality
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])
            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])
            if show_details:
                print ("match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score
    return high_class, high_score

import random
import csv
with open(r"intents.json", encoding="utf8") as f:
    reader = json.load(f)
reader = reader
def response(sentence):
    result = classify(sentence)
    print(result)
    dat = []
    dat.append(sentence)    
    if (result[0] == None):
        add = ("INSERT IGNORE INTO question_table "
              "(question) "
              "VALUES (%s)")
        # Insert new employee
        cursor.execute(add, (sentence,))
        # Make sure data is committed to the database
        cnx.commit()
        return "Sorry I didnt get you!"
    for i in reader['intents']:
        if(i['tag']==result[0]):
            return random.choice(i['responses'])

        

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')   
    #return render_template("homee.html", respondses=str(response(userText)), query=userText)
    a = str(response(userText))
    return str(response(userText)) 
if __name__ == "__main__":    
    app.run(debug=True)