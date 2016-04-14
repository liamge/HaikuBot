from nltk import pos_tag
from nltk.corpus import cmudict

class HaikuGenerator:
	def __init__(self, words):
		self.d = cmudict.dict()
		self.word_tags = pos_tag(words.split())
		self.adjectives1 = [w for (w, t) in self.word_tags if t == 'JJ' or t == 'VBG' and self.syllables(w) == 3]
		self.nouns2 = [w for (w, t) in self.word_tags if (t == 'NN' or t == 'NNS') and self.syllables(w) == 2]
		
	def syllables(word):
		return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]

hg = HaikuGenerator('Enchanting')
print(hg.adjectives1)