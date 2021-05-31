import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
from tensorflow.python.framework import ops
import random
import json
import pickle
import os
import time
import speech_recognition as sr

with open("test.json") as file:
    data = json.load(file)


with open("models/data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

ops.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.load("models/model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

def speak(text):
    os.system('espeak -s 150 -v +f2 "'+text+'"')

def get_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        speak('Speak Anything : ')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            #print('You said: {}'.format(text))
        except:
            speak('Sorry could not recognize your voice')
            return
    return text

def chat():
    print("Start talking with the bot (type quit to stop)!")
    t1 = t2 = time.perf_counter()
    while True:
        #inp = input("You: ")
        txt = get_audio()
        if t2 - t1 > 20: 
            print("##################")
            break

        if not txt:
            t2 = time.perf_counter()
            continue

        t1 = time.perf_counter()
        if txt.lower() == "quit":
            break

        results = model.predict([bag_of_words(txt, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            speak(random.choice(responses))
        else:
            speak("I didn't get that, try again.")

chat()