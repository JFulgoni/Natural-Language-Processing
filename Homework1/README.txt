John Fulgoni
UNI: jsf2154
Homework 1 README

Part A:

Question 1:
UNIGRAM natural -13.766408817
BIGRAM natural that -4.05889368905
TRIGRAM natural that he -1.58496250072

Question 2:
Not sure why my answers are different, my lines match the ones given exactly
A2.uni.txt	The perplexity is 1027.72002851
A2.bi.txt	The perplexity is 53.68831425
A3.tri.txt	The perplexity is 5.7106793082

Question 3:
I know my answers in A3.txt are decimal places off, but here's the perplexity.
The perplexity is 12.5463387925

Question 4:
I originally thought that the interpolated model would do better than the trigrams.
After thinking about it, since we equally weight the unigrams, bigrams, and trigrams, I could see it being better.
If the weights were calibrated, then I imagine it would do even better than the trigrams.

Question 5:
python perplexity.py output/A3.txt data/Sample1.txt
The perplexity is 1173692.47966

python perplexity.py output/A3.txt data/Sample2.txt
The perplexity is 5.06447919859e+11

I will say that Sample 1 is the excerpt, because the perplexity for this is way lower than Sample 2.
Since the output was trained on the Brown Corpus, something else from the Brown Corpus should have a similar structure and vocabulary.


Part B:

Question 1: N/A

Question 2:
TRIGRAM CONJ ADV ADP -2.9755173148
TRIGRAM DET NOUN NUM -8.9700526163
TRIGRAM NOUN PRT PRON -11.0854724592

Question 3: N/A

Question 4:
* * 0.0
Night NOUN -13.8819025994
Place VERB -15.4538814891
prime ADJ -10.6948327183
STOP STOP 0.0
_RARE_ VERB -3.17732085089

Question 5:

Question 6:
python pos.py output/B6.txt data/Brown_tagged_dev.txt
Percent correct tags: 87.998514667
