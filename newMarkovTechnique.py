from nltk import pos_tag

class HaikuGenerator:
	def __init__(self, words):
		self.word_tags = pos_tag(words.split())
		self.adjectives1 = [w for (w, t) in self.word_tags if t == 'JJ']
		self.adjectives2 = []

hg = HaikuGenerator('blue green yellow orange')
print(hg.adjectives1)