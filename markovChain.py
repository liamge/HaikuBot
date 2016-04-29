__author__ = 'liamgeron'
from nltk import FreqDist, ConditionalFreqDist, bigrams
from numpy import cumsum
from numpy.random import rand
from nltk.corpus import brown
import itertools

""" TO DO:
    - Switch to bigrams
    - Maybe ditch the haiku idea
        - If not move on to practical solution w/r/t syllable structure
    - Specify .join() for punctuation (i.e. periods don't get a space)
"""

class MarkovChain:
    def __init__(self):
        self.transitionMatrix = {}
        self.start_states = {}

    def train(self,states):
        self.states = states
        fdist = FreqDist(states)
        cfd = ConditionalFreqDist(bigrams(states))
        for s in states:
            self.transitionMatrix[s] = {}
            for a in states:
                self.transitionMatrix[s][a] = float(cfd[s][a] / fdist[s])


    def weightedChoice(self, objects, weights):
        cs = cumsum(weights)
        idx = sum(cs < rand())
        return objects[idx]


    # Get some start probabilities and initiate a sentence with them
    def generate(self):
        generated_text = []
        seed = "START"
        while seed != "END":
            choiceKeys = list(self.transitionMatrix[seed].keys())
            choiceWeights = list(self.transitionMatrix[seed].values())
            nextSeed = self.weightedChoice(choiceKeys,choiceWeights)
            if nextSeed == "END":
                break
            else:
                generated_text.append(nextSeed)
                seed = nextSeed

        return ' '.join(generated_text)
        
"""
For Training Model:
    - Input arrays of sentences that begin with "START" and end with "END"
    - e.g. [['START', 'This', 'is', 'a', 'sentence', 'END']]
"""

training_set = list(brown.sents(categories='fiction')[:300])
for sent in training_set:
    sent.append("END")
    sent.insert(0,"START")
training_set = list(itertools.chain(*training_set))
mc = MarkovChain()
mc.train(training_set)
print(mc.generate())