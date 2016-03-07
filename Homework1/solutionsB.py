from __future__ import division
import sys
import nltk
import math
import time

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []

    # John's edit starts here
    test_me = 1
    for sentence in brown_train:
        current_words = []
        current_tags = []
        stripped_sent = sentence.strip() # get rid of the trailing garbage
        sent_frags = stripped_sent.split(' ') # first split by space to get the combinations of words

        # first going to append two start symbols
        current_words.append(START_SYMBOL)
        current_words.append(START_SYMBOL)
        current_tags.append(START_SYMBOL)
        current_tags.append(START_SYMBOL)

        #now deal with frags
        for frag in sent_frags:
            sep_slash = frag.split('/')
            slash_len = len(sep_slash)
            if(slash_len > 2):
                my_word = sep_slash[0]
                for x in range (1, slash_len - 1):
                    my_word = my_word + '/' + sep_slash[x]
                current_words.append(my_word)
                current_tags.append(sep_slash[slash_len - 1])
            else:
                current_words.append(sep_slash[0])
                current_tags.append(sep_slash[1])

        #now append an end symbol
        current_words.append(STOP_SYMBOL)
        current_tags.append(STOP_SYMBOL)

        #if test_me:
        #    print current_words
        #    print current_tags
        #    test_me = 0

        brown_words.append(list(current_words))
        brown_tags.append(list(current_tags))

    #for i in range (0, 2):
    #    print brown_words[i]


    # professor provided return here
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    q_values = {}

    #John's edit starts here
    #should be very simple from the other file

    unigram_c = {}
    bigram_c = {}
    trigram_c = {}

    unigram_p = {}
    bigram_p = {}

    sentence_count = 0
    unigram_count = 0
    bigram_count = 0
    trigram_count = 0

    # John's edit starts here
    # First need to find the count of all the tuples, and put them in an outer dictionary
    test_me = 1
    for sentence in brown_tags:
        # passing this to helper function with the stripped version of each sentence
        #unigram_tuples, bigram_tuples, trigram_tuples = sentence_split(sentence.strip())

        trigram_tuples = list(nltk.trigrams(sentence))
        # if test_me:
        #     print trigram_tuples
        #     test_me = 0

        #sentence.pop(0) #remove first start symbol
        new_sent = list(sentence[1:])
        bigram_tuples = list(nltk.bigrams(new_sent))

        newnew_sent = list(new_sent[1:]) #remove other start symbol
        unigram_tuples = list(newnew_sent)

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

        q_values[three_words] = math.log(float(count_three_words) / float(count_prev_bigram), 2)


    #professor provided return value here
    return q_values

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    known_words = set([])

    #John's edit starts here
    word_count = {}
    for sentence in brown_words:
        list_words = list(sentence) #just getting a list of words
        #count all the words and add them to the list
        for phrase in list_words:
            if (phrase,) in word_count:
                word_count[(phrase,)] += 1
            else:
                word_count[(phrase,)] = 1

    test_me = 1
    for word in word_count:
        # if test_me < 10:
        #      print word, word_count[word]
        #      test_me += 1
        if word_count[word] > 5:
            known_words.add(word)

    #print word_count[('*',)]
    # return here provided by professor
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    brown_words_rare = []

    #John's edit starts here
    test_me = 1

    for sentence in brown_words:
        list_words = list(sentence)

        for i in range (0, len(list_words)):
            if (list_words[i],) not in known_words:
                list_words[i] = RARE_SYMBOL

        # if test_me < 10:
        #     print list_words
        #     test_me += 1
        brown_words_rare.append(list(list_words))

    #professor provided return statement
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    e_values = {}
    taglist = set([])

    #John's edit starts here

    #first get the count of all the tags
    tag_c = {}
    for tag_sent in brown_tags:
        for my_tag in tag_sent:
            if (my_tag,) in tag_c:
                tag_c[(my_tag,)] += 1
            else:
                tag_c[(my_tag,)] = 1
            #add tags to the set as you go!
            if (my_tag,) not in taglist:
                taglist.add(my_tag)

    #then get the count of all the combinations
    #words is the sentence, need corresponding tags
    pair_c = {}
    test_me = 1

    number_of_sentences = len(list(brown_words_rare))
    #print number_of_sentences

    for i in range (0, number_of_sentences): # for each sentence
        sentence = list(brown_words_rare[i])
        number_of_words = len(sentence)
        tags = list(brown_tags[i])
        #number_of_tags = len(tags)

        # if test_me < 10:
        #     print sentence
        #     print tags
        #     print number_of_words, number_of_tags
        #     test_me += 1
            #test_me = 0

        for j in range (0, number_of_words): # for each word of the sentence
            my_pair =tuple([sentence[j], tags[j]])
            # if test_me:
            #     print my_pair
            #     test_me = 0
            if my_pair in pair_c:
                pair_c[my_pair] += 1
            else:
                pair_c[my_pair] = 1

    for combination in pair_c:
        tag_part = combination[1]
        current_tag_count = tag_c[(tag_part,)]
        current_pair_count = pair_c[combination]

        pair_fraction = float(current_pair_count) / float(current_tag_count)

        # if test_me < 10:
        #     print current_pair_count, current_tag_count, pair_fraction
        #     test_me += 1

        if pair_fraction <= 0:
            e_values[combination] = LOG_PROB_OF_ZERO
        else:
            e_values[combination] = math.log(pair_fraction, 2)



    #professor provided the return values here
    return e_values, taglist

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    tagged = []

    # John's edit starts here
    # brown_dev_words are observations
    # taglist is states
    # known_words is the set of known words (i.e. to get RARE)
    # q_values are the transition probabilities
    # e_values are the emission probabilities
    # return tagged which is a list of sentences

    #separate e_values into a dictionary?
    derp = 1
    e_collection = dict()
    for item in e_values:
        if item[0] in e_collection:
            e_collection[item[0]].append(item[1])
        else:
            e_collection[item[0]] = []
            e_collection[item[0]].append(item[1])


    print e_collection[RARE_SYMBOL]

    test_me = 1
    counter = 0
    sentence_test = 0
    for sentence in brown_dev_words:
        # each sentence is a sentence separated into words

        sent_frags = list(sentence)
        #print sent_frags

        V = {}
        bp = {}

        V[(START_SYMBOL, START_SYMBOL, 0)] = 1 # initialization step

        #print "initial: ", V[('*', '*', 0)]

        # for s1 and s2
        # find the s that gives the highest probability for a given s1, s2, and the current word that we're talking about

        # do I add start and stop symbols?
        # sent_frags.insert(0, START_SYMBOL)
        # sent_frags.insert(0, START_SYMBOL)
        # sent_frags.append(STOP_SYMBOL)
        sentence_length = len(sent_frags)

        counter += 1
        #print 'Sentence Number', counter
        #print sent_frags[0]

        for t in range (1, sentence_length + 1):
            current_word = sent_frags[t-1]
            if (current_word,) not in known_words: # if the current word being test
                current_word = RARE_SYMBOL

            for second_previous_tag in taglist: #s2 is the second previous tag

                for first_previous_tag in taglist: #s1 is the previous tag

                    best_prob = 0 #set some probability

                    try:
                        v_step = V[(second_previous_tag, first_previous_tag, t-1)]
                    except KeyError:
                        #v_step = LOG_PROB_OF_ZERO
                        v_step = 0
                        #V[(second_previous_tag, first_previous_tag, t-1)] = 0

                    if v_step > 0:

                        better_taglist = list(e_collection[current_word])

                        for optimal_tag in better_taglist:
                            #for each combination of s1 and s2, you have to find a max
                            #probably rearrange to find an 's' that maximizes (s2, s1)

                            try:
                                e_step = math.pow(2,e_values[(current_word, optimal_tag)])
                                #e_step = e_values[(current_word, optimal_tag)]
                                #print 'found word/tag combo'
                            except KeyError:
                                #e_step = LOG_PROB_OF_ZERO
                                e_step = 0

                            try:
                                q_step = math.pow(2, q_values[(second_previous_tag, first_previous_tag, optimal_tag)])
                                #q_step = q_values[(second_previous_tag, first_previous_tag, optimal_tag)]
                            except KeyError:
                                #q_step = LOG_PROB_OF_ZERO
                                q_step = 0

                            current_prob = v_step * q_step * e_step

                            if current_prob > best_prob:
                                best_prob = current_prob
                                V[(first_previous_tag, optimal_tag, t)] = best_prob
                                bp[(first_previous_tag, optimal_tag, t)] = second_previous_tag
                                #print "T = ", t, first_previous_tag, optimal_tag, best_prob, bp[(first_previous_tag, optimal_tag, t)]
                                #prints the best prob for a given s2 and s1

                    #end s loop

            #break #ends word loop

        #print "\n"
        #print "Start End Sequence"
        # START END SEQUENCE
        best_end_prob = 0
        end_s2 = ""
        second_last_tag = ""
        last_tag = ""
        #print "number of tags: ", len(taglist)
        tag_counter = 0
        q_counter = 0

        path_s1 = ""
        path_s = ""
        for second_previous_tag in taglist:
            for first_previous_tag in taglist:

                try:
                    v_step_end = V[(second_previous_tag, first_previous_tag, sentence_length)]
                    #v_step_end = V[(second_previous_tag, '.', sentence_length)]
                except KeyError:
                    v_step_end = 0
                    tag_counter += 1

                # if(v_step_end != 0):
                #     print "v_step: ", second_previous_tag, first_previous_tag, v_step_end

                try:
                    end_trigram = (second_previous_tag, first_previous_tag, STOP_SYMBOL)
                    #end_trigram = (second_previous_tag, '.', STOP_SYMBOL)
                    #print end_trigram
                    q_step_end = math.pow(2, q_values[end_trigram])
                except KeyError:
                    q_step_end = 0
                    q_counter += 1

                #if(q_step_end != 0):
                    #print end_trigram
                    #print "values:", v_step_end, q_step_end

                temp_prob = v_step_end * q_step_end

                #print s2, s1, temp_prob
                if temp_prob > best_end_prob:
                    best_end_prob = temp_prob
                    second_last_tag = second_previous_tag
                    last_tag = first_previous_tag
                    #print "second last: ", second_last_tag, "last: ", last_tag
                    path_s1 = second_last_tag
                    path_s = last_tag

        #print "tag_counter: ", tag_counter, "q_counter: ", q_counter


        #print "\n"
        #print "Now we backtrack!"
        # NOW WE HAVE TO BACKTRACK TO FIND ALL THE KEYS
        # this might work? who knows...

        try:
            path = []
            # path_s1 = second_last_tag
            # path_s = last_tag
            path.append(path_s1)
            path.append(path_s)
            for i in range (sentence_length, 0, -1):
                next_tag =  bp[(path_s1, path_s, i)]
                #print "last tag:", path_s, 'second last tag:', path_s1, 'next tag:', next_tag
                path_s = path_s1
                path_s1 = next_tag
                path.insert(0, next_tag)

            #print path

            sent_tags = path[2:]
            #print sent_tags
            #print sent_frags
            #print len(sent_tags), len(sent_frags)

            final_sentence_combos = []
            for x in range (0, len(sent_tags)):
                final_sentence_combos.append(sent_frags[x] + '/' + sent_tags[x])

            #print final_sentence_combos

            tagged.append(' '.join(final_sentence_combos) + '\n')

        except KeyError:
            tagged.append('\n')

        # sentence_test += 1
        # if sentence_test > 1000:
        #     print "Number of Total Sentences:", sentence_test
        #     break #ends sentence loop

    #professor provided return statement here
    return tagged

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]

    # IMPLEMENT THE REST OF THE FUNCTION HERE
    tagged = []

    #John's edit starts here

    unigram_tagger = nltk.DefaultTagger("NOUN")
    bigram_tagger = nltk.BigramTagger(training, backoff=unigram_tagger)
    trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)

    # for sentence in brown_dev_words:
    #     tri_tags = trigram_tagger.tag(sentence)

    tri_tags = trigram_tagger.tag_sents(brown_dev_words)

    for sentence in tri_tags:
        final_sentence_combos = []
        for phrase in sentence:
            final_sentence_combos.append(phrase[0] + '/' + phrase[1])

        tagged.append(' '.join(final_sentence_combos) + '\n')

    #return provided by professor
    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
