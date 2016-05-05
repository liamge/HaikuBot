__author__ = 'liamgeron'
from numpy import cumsum
from numpy.random import rand
from nltk.corpus import cmudict
import pickle

class MarkovChain:
    def __init__(self):
        self.d = cmudict.dict()
        self.transitionMatrix = pickle.load(open('save.p','rb'))

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

    def generateHaiku(self):
        self.seed = "START"
        line1 = self.decision(5)
        line2 = self.decision(7)
        line3 = self.decision(5)
        return ' '.join(line1) + '\n' + ' '.join(line2) + '\n' + ' '.join(line3)

    def generateSent(self):
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

mc = MarkovChain()
print(mc.generateHaiku())
