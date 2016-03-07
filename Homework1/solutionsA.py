from __future__ import division
import math
import nltk
import time

# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):
    # three lines below were given by professor
    unigram_p = {}
    bigram_p = {}
    trigram_p = {}

    unigram_c = {}
    bigram_c = {}
    trigram_c = {}

    sentence_count = 0
    unigram_count = 0
    bigram_count = 0
    trigram_count = 0

    # John's edit starts here
    # First need to find the count of all the tuples, and put them in an outer dictionary
    for sentence in training_corpus:
        # passing this to helper function with the stripped version of each sentence
        unigram_tuples, bigram_tuples, trigram_tuples = sentence_split(sentence.strip())
        for phrase in unigram_tuples:
            if (phrase,) in unigram_c:
                unigram_c[(phrase,)] += 1
            else:
                unigram_c[(phrase,)] = 1

            unigram_count += 1

        for phrase in bigram_tuples:
            if phrase in bigram_c:
                bigram_c[phrase] += 1
            else:
                bigram_c[phrase] = 1

            bigram_count += 1

        for phrase in trigram_tuples:
            if phrase in trigram_c:
                trigram_c[phrase] += 1
            else:
                trigram_c[phrase] = 1

            trigram_count += 1

        sentence_count += 1 # keeps track of how many sentences there are

    # now that we have all the data, we now need to convert counts into probabilities
    for one_word in unigram_c:
        current_count = unigram_c[one_word]
        #print unigram_count
        #if one_word[0] == "captain":
            #print "captain", current_count
        unigram_p[one_word] = math.log(float(current_count) / float(unigram_count), 2)


    for two_words in bigram_c:
        count_both_words = bigram_c[two_words]
        if(two_words[0] == '*'):
            count_word_one = sentence_count
        else:
            count_word_one = unigram_c[(two_words[0],)]

        #count_word_two = unigram_c[(two_words[1],)]
        bigram_p[two_words] = math.log(float(count_both_words) / float(count_word_one), 2)

    testing_this = 1
    for three_words in trigram_c:
        count_three_words = trigram_c[three_words]

        prev_bigram = tuple([three_words[0],three_words[1]])
        #count_prev_bigram = bigram_c[prev_bigram]
        #above was previous code

        if(prev_bigram[0] == '*' and prev_bigram[1] == '*'):
            count_prev_bigram = sentence_count
        else:
            count_prev_bigram = bigram_c[prev_bigram]

        trigram_p[three_words] = math.log(float(count_three_words) / float(count_prev_bigram), 2)

        #if testing_this:
           # print three_words
            #print 'Count three words', count_three_words
           # print 'Previous Bigram', prev_bigram
           # testing_this = 0
    # return here was given by professor
    return unigram_p, bigram_p, trigram_p

# John made this function to help with the splitting
def sentence_split(sentence):
    sent_frags = sentence.split(' ') # gets each sentence from training_corpus

    sent_frags.append(STOP_SYMBOL)
    unigram_tuples = list(sent_frags) # is this necessary

    #now we can insert start symbols for bigrams and trigrams
    sent_frags.insert(0, START_SYMBOL)

    #now properly split into bigrams and trigrams
    bigram_tuples = list(nltk.bigrams(sent_frags))

    #do I add a second star for trigrams?
    sent_frags.insert(0, START_SYMBOL)

    trigram_tuples = list(nltk.trigrams(sent_frags))
    return unigram_tuples, bigram_tuples, trigram_tuples

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    scores = []
    # John's edit starts here
    # Note that ngram_p input is just one of the three cases
    # n is the size of the ngram

    # first set up sentence as before
    # using the function as before, so I can get the right tokens for my problem
    test_me = 1
    for sentence in corpus:
        prob_val = 1
        if(n == 1):
            tokens = sentence_split(sentence.strip())[0]
            #print(tokens)
            for unigram in tokens:
                if (unigram,) in ngram_p:
                    prob_val *= math.pow(2,ngram_p[(unigram,)]) # convert it back to a fraction
                else:
                    prob_val = MINUS_INFINITY_SENTENCE_LOG_PROB
                    break
                    # even if one value isn't present, then it fails
            if(prob_val == 0 or prob_val == MINUS_INFINITY_SENTENCE_LOG_PROB):
                scores.append(MINUS_INFINITY_SENTENCE_LOG_PROB)
            else:
                scores.append(math.log(prob_val,2))
            # so apparently the above works, and the same few numbers are good results
            # there are cases that just don't work, so we'll need to find a special way to deal with it

        elif(n == 2):
            tokens = sentence_split(sentence.strip())[1]
            for bigram in tokens:
                if bigram in ngram_p:
                    prob_val *= math.pow(2,ngram_p[bigram]) # convert it back to a fraction
                else:
                    prob_val = MINUS_INFINITY_SENTENCE_LOG_PROB
                    break
            if(prob_val == 0 or prob_val == MINUS_INFINITY_SENTENCE_LOG_PROB):
                scores.append(MINUS_INFINITY_SENTENCE_LOG_PROB)
            else:
                scores.append(math.log(prob_val,2))

        elif(n == 3):
            tokens = sentence_split(sentence.strip())[2]
            #if test_me:
            #    print tokens
            #    test_me = 0
            for trigram in tokens:
                if trigram in ngram_p:
                    prob_val *= math.pow(2,ngram_p[trigram]) # convert it back to a fraction
                else:
                    prob_val = MINUS_INFINITY_SENTENCE_LOG_PROB
                    break
            if(prob_val == 0 or prob_val == MINUS_INFINITY_SENTENCE_LOG_PROB):
                scores.append(MINUS_INFINITY_SENTENCE_LOG_PROB)
            else:
                scores.append(math.log(prob_val,2))


    # return provided by the professor
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []
    my_lambda = 1.0 / 3.0

    # John's edit starts here
    test_me = 1
    for sentence in corpus:
        # get score for unigrams
        unitokens, bitokens, tritokens = sentence_split(sentence.strip())
        #print(tokens)

        uni_val = 1
        bi_val = 1
        tri_val = 1
        # for unigram in unitokens:
        #     if (unigram,) in unigrams:
        #         uni_val *= math.pow(2,unigrams[(unigram,)]) # convert it back to a fraction
        #     else:
        #         uni_val = MINUS_INFINITY_SENTENCE_LOG_PROB
        #         break
        #         # even if one value isn't present, then it fails
        #
        # for bigram in bitokens:
        #     if bigram in bigrams:
        #         bi_val *= math.pow(2,bigrams[bigram])
        #     else:
        #         bi_val = MINUS_INFINITY_SENTENCE_LOG_PROB
        #         break
        #
        # for trigram in tritokens:
        #     if trigram in trigrams:
        #         tri_val *= math.pow(2,trigrams[trigram])
        #     else:
        #         tri_val = MINUS_INFINITY_SENTENCE_LOG_PROB
        #         break

        fail_flag = 0
        total_prob = 1
        for trigram in tritokens:

            unigram = (trigram[2],)
            bigram = (trigram[1], trigram[2])

            if unigram in unigrams:
                uni_val = math.pow(2,unigrams[unigram])
            else:
                #uni_val = MINUS_INFINITY_SENTENCE_LOG_PROB
                #fail_flag = 1
                uni_val = 0
                break

            if bigram in bigrams:
                bi_val = math.pow(2,bigrams[bigram])
            else:
                #bi_val = MINUS_INFINITY_SENTENCE_LOG_PROB
                #fail_flag = 1
                bi_val = 0
                break

            if trigram in trigrams:
                tri_val = math.pow(2, trigrams[trigram])
            else:
                #fail_flag = 1
                # or set flag?
                tri_val = 0
                break

            total_prob *= my_lambda * (uni_val + bi_val + tri_val)

        #print uni_val, bi_val, tri_val, total_prob
        if(fail_flag == 1):
            scores.append(MINUS_INFINITY_SENTENCE_LOG_PROB)
        elif(total_prob == 0):
            scores.append(MINUS_INFINITY_SENTENCE_LOG_PROB)
        else:
            scores.append(math.log(total_prob, 2))

    # professor provided this return statement
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
