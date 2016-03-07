__author__ = 'johnfulgoni'

import nltk

# may need to do this in console
# nltk.download()
# needed the Models/Punkt package
sentence = "At eight o'clock on Thursday morning on Thursday morning on Thursday morning."

#Tokenize the Sentence
tokens = nltk.word_tokenize(sentence)
# remember to not use this when doing the actual assignment - TAs
# print(tokens)

#N-Gram Generation
bigram_tuples = list(nltk.bigrams(tokens))
trigram_tuples = list(nltk.trigrams(tokens))
#print(trigram_tuples)

#count the number of each n-gram
count = {item : bigram_tuples.count(item) for item in set(bigram_tuples)}
print count

#find the distinct n-grams that contain the word 'on'
ngrams = [item for item in set(bigram_tuples) if "on" in item]

#Create naive Default Tagger
default_tagger = nltk.DefaultTagger('NN')
tagged_sentence = default_tagger.tag(tokens)

# download tagsets from .download()
nltk.help.upenn_tagset('NN')

#Regular Expression Tagset
patterns = [(r'.*ing$', 'VBG'),(r'.*ed$', 'VBD'),(r'.*es$', 'VBZ'),(r'.*ed$', 'VB')]
regexp_tagger = nltk.RegexpTagger(patterns)
regexp_tagger.tag(tokens)

from nltk.corpus import brown
training = brown.tagged_sents(categories='news')

# Create Unigram, Bigram, Trigram taggers based on the training set.
unigram_tagger = nltk.UnigramTagger(training)
bigram_tagger = nltk.BigramTagger(training)
trigram_tagger = nltk.TrigramTagger(training)

#Combination of taggers
default_tagger = nltk.DefaultTagger('NN')
bigram_tagger = nltk.BigramTagger(training, backoff=default_tagger)
trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)

print("done!")