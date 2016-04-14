__author__ = 'liamgeron'
import nltk
import random
from numpy.random import choice
from nltk.corpus import cmudict

class MarkovChain:
    def __init__(self):
        self.transitionMatrix = {}
        self.d = cmudict.dict()

    def train(self,states):
        self.states = states
        fdist = nltk.FreqDist(states)
        cfd = nltk.ConditionalFreqDist(nltk.bigrams(states))
        for s in states:
            self.transitionMatrix[s] = {}
            for a in states:
                self.transitionMatrix[s][a] = cfd[s][a] / fdist[s]
                
    def syllables(self,word):
    	return [len(list(y for y in x if isdigit(y[-1]))) for x in self.d[word.lower()]]
    	
    def haiku_search(self, words):
    	syl_count = 0
    	word_count = 0
    	haiku_line_count = 0
    	lines = []
    	for word in words:
        	syl_count += self.syllables(word)
        	if haiku_line_count == 0:
            	if syl_count == 5:
                	lines.append(word)
                	haiku_line_count += 1
        	elif haiku_line_count == 1:
            	if syl_count == 12:
                	lines.append(word)
                	haiku_line_count += 1
        	else:
            	if syl_count == 17:
                	lines.append(word)
                	haiku_line_count += 1

    # Get some start probabilities and instigate a sentence with them
    # incorporate random choice using numpy, that'll end the infinite loop
    
        

training_set = nltk.corpus.brown.words(categories='news')[:100]
training_set = [w.lower() for w in training_set]
mc = MarkovChain()
mc.haiku_search('sand scatters the beach waves crash on the sandy shore blue watter shimmers