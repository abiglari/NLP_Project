import sys
text = unicode(open(sys.argv[1], 'r').read())

import spacy
nlp = spacy.load('en_core_web_sm')
index = text.find(u'[TEXT]') + 7
text = text[index:]
text = '\n\n'.join([sent.replace('\n', ' ') for sent in text.split('\n\n')])
doc = nlp(text.lower())

from nltk.corpus import framenet as fn

excludes = {'Repel'}

def excluded(token):
	for f in fn.frames_by_lemma(token.lemma_):
		if f.name in excludes:
			return True
	return False

incidents = {'Arson':0, 'Attack':0, 'Kidnapping':0, 'Robbery':0, 'Committing_crime':0, 'Offenses':0} # bombing

key_verbs = [] # could be nouns
weapons = []
for token in doc:
	lemma = token.lemma_
	if lemma != 'be' and (token.pos_ == 'NOUN' or token.pos_ == 'VERB'):
		for f in fn.frames_by_lemma(lemma):
			if f.name in incidents:
				incidents[f.name] += 1
				key_verbs.append(token)
			elif f.name == 'Weapon' and token.pos_ == 'NOUN':
				weapons.append(token)
print incidents
# print key_verbs
print 'weapon', weapons

def get_child(token, dep_):
	for child in token.children:
		if child.dep_ == dep_:
			return child

def get_conjs(token):
	tokens = []
	while token:
		tokens.append(token)
		token = get_child(token, 'conj')
	return tokens


def get_subjs(sent, verb):
	subjs = []
	for token in sent:
		if token.dep_ == 'nsubj' and token.head == verb:
			# subjs.append(token)
			# print token, verb
			subjs.extend(get_conjs(token))
			break
		elif token.dep_ == 'pobj' and token.head.dep_ == 'agent' and token.head.head == verb:
			subjs.extend(get_conjs(token))
			break
		elif token == verb and token.pos_ == 'NOUN':
			if token.dep_ == 'dobj':
				new_verb = token.head
				if not excluded(new_verb):
					# print new_verb
					subjs.extend(get_subjs(sent, new_verb))
					break
			elif token.dep_ == 'pobj':
				new_verb = token.head.head
				subjs.extend(get_subjs(sent, new_verb))
				break
	return subjs

def get_objs(sent, verb):
	objs = []
	for token in sent:
		# print token, token.dep_, token.head
		if token.dep_ == 'dobj' and token.head == verb or token.dep_ == 'pobj' and token.head.dep_ != 'agent' and token.head.head == verb:
			# objs.append(token)
			objs.extend(get_conjs(token))
			break
	return objs
	
def get_np(token):
	for np in doc.noun_chunks:
		if np.root == token:
			return np

subjs = []
objs = []
for sent in doc.sents:
	for verb in key_verbs:
		if verb in sent:
			subjs.extend(get_subjs(sent, verb))
			objs.extend(get_objs(sent, verb))
for subj in set(subjs):
	print 'prep', get_np(subj).text.upper()
for obj in set(objs):
	print 'target', get_np(obj).text.upper()
print

