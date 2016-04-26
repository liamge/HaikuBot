__author__ = 'liamgeron'
from nltk import FreqDist, ConditionalFreqDist, bigrams
from numpy import cumsum
from numpy.random import rand
from nltk.corpus import brown, cmudict
import itertools


""" TO DO:
    - Deal with OOV items for syllable dictionary
    - Switch to bigrams
    - Specify .join() for punctuation (i.e. periods don't get a space)
"""



class MarkovChain:
    def __init__(self):
        self.d = cmudict.dict()
        self.transitionMatrix = {}

    def train(self,states):
        self.states = states
        fdist = FreqDist(states)
        cfd = ConditionalFreqDist(bigrams(states))
        for s in states:
            self.transitionMatrix[s] = {}
            for a in states:
                self.transitionMatrix[s][a] = float(cfd[s][a] / fdist[s])

    # Takes input of list of objects that correspond to list of weights for the objects
    def weightedChoice(self, objects, weights):
        cs = cumsum(weights)
        idx = sum(cs < rand())
        return objects[idx]

    # How the fuck is this working
    def syllableCount(self, word):
        sylList = [list(y for y in x if y[-1].isdigit()) for x in self.d[word.lower()]]
        for l in sylList:
            return len(l)

    # Decision is the line generation that takes in desired number of syllables
    # and outputs a line with that many syllables
    def decision(self, goalSylCount):
        line = []
        sylCount = 0
        while sylCount < goalSylCount:
            choiceKeys = list(self.transitionMatrix[self.seed].keys())
            choiceWeights = list(self.transitionMatrix[self.seed].values())
            nextSeed = self.weightedChoice(choiceKeys,choiceWeights)
            if nextSeed == 'START' or nextSeed == 'END':
                choiceKeys = list(self.transitionMatrix[self.seed].keys())
                choiceWeights = list(self.transitionMatrix[self.seed].values())
                nextSeed = self.weightedChoice(choiceKeys,choiceWeights)
                self.seed = nextSeed
            elif nextSeed.isalpha():
                line.append(nextSeed)
                sylCount += self.syllableCount(nextSeed)
                self.seed = nextSeed
            else:
                line.append(nextSeed)
                self.seed = nextSeed
        return line

    def generate(self):
        self.seed = "START"
        line1 = self.decision(5)
        line2 = self.decision(7)
        line3 = self.decision(5)
        return ' '.join(line1) + '\n' + ' '.join(line2) + '\n' + ' '.join(line3)


training_set = list(brown.sents(categories='fiction')[:300])
for sent in training_set:
    sent.append("END")
    sent.insert(0,"START")
training_set = list(itertools.chain(*training_set))
mc = MarkovChain()
mc.train(training_set)
print(mc.generate())