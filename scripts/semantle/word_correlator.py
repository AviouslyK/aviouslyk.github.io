import math
import pandas as pd
import nltk
#from nltk.corpus import brown
from nltk.corpus import gutenberg
from nltk.corpus import reuters
from nltk.corpus import webtext, nps_chat
from gensim.models import Word2Vec
import gensim
import random
from nltk.data import find
import string


class WordCorrelator:
    def __init__(self, target="placeholder"):
        self.target = target.lower() # for case-insensitive comparison
        self.closest_score = -1
        self.model = None

    def set_target(self, target):
        self.target = target.lower()

    def setup_data(self):
        # Download collection of English Words as a 2D list [sentence][word]
        # nltk.download('all') has already been run
        literature = gutenberg.sents()  
        news       = reuters.sents()
        web        = webtext.sents()

        allwords =  literature + news + web 

        '''
        print("len(literature) = ", len(literature))
        print("len(news) = ", len(news))
        print("len(web) = ", len(web))
        print("len(allwords) = ", len(allwords))
        '''

        # remove 1 and 2 letter words 
        allwords = [[word for word in sentence if len(word) > 2] for sentence in allwords]

        # remove words with special characters
        allwords = [[word for word in sentence if all(char not in string.punctuation for char in word)] for sentence in allwords]

        # remove proper nouns
        allwords = [[word for word in sentence if word.islower()] for sentence in allwords]

        # remove empty sentences
        allwords = [sentence for sentence in allwords if len(sentence) > 0]
  
        # Choose random word to be the target
        rand_sentence = random.choice(allwords)
        rand_word = random.choice(rand_sentence)
        #self.set_target(rand_word)
        self.set_target("previously")
        print("target = ", self.target)
 

        # Create and train model -OR- load previously trained model
        self.model = Word2Vec.load("web_news_lit_1k_epochs_all_sentences.bin")
        #self.model = Word2Vec(allwords)
        #self.model.train(allwords, total_examples=len(allwords), epochs=1000)
        
        # Save the model
        #self.model.save('web_news_lit_1k_epochs_all_sentences.bin')

        sim = self.model.wv.most_similar(positive=[self.target], topn = 1)
        closest_word, self.closest_score = sim[0]

    # should be fraction of most_similar word
    def calculate_similarity_score(self, guess):
        if self.model is None:
            raise ValueError("Model is not trained. Call setup_data first")

        similarity_score = self.model.wv.similarity(guess, self.target)
        return similarity_score

    # User guesses a word, return how close it is to the Target
    def doGuess(self):
        guess = user_input = input("Enter a Guess:\n")

        # previous and previously should give the same score. Same for all suffixes
        suffixes = ['ly','ed','ing','s']

        guesses = [guess + s for s in suffixes]
        similarity_score = -1
        final_score = -1

        # calc correlation between word and target
        # do for all variations of the word
        for g in guesses:
            if g == self.target:
                similarity_score = 100
            elif g in self.model.wv:
                similarity_score = self.calculate_similarity_score(g)
                similarity_score = (similarity_score / self.closest_score * 100) - 1
            
            if similarity_score > final_score:
                final_score = similarity_score
        
        if final_score == -1:
            print("hmmm, I don't know that word. Try another") 
        else:
            print("similarity score = ", final_score)
        

        return final_score