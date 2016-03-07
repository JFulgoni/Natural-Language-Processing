import A
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import SelectKBest, chi2

from sklearn import svm
import string
import nltk
from nltk.corpus import wordnet as wn
from nltk.data import load
from nltk.corpus import cess_esp
from nltk.corpus import cess_cat
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from math import log10


# You might change the window size
window_size = 10

english_window = 15
catalan_window = 10
spanish_window = 5

english_stopwords = stopwords.words('english')
spanish_stopwords = stopwords.words('spanish')

# set up tagger
def set_tagger(language):
    if language == 'English':
        _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
        tagger = load(_POS_TAGGER)
    elif language == 'Catalan':
        training = cess_cat.tagged_sents()
        default_tagger = nltk.DefaultTagger('NN')
        unigram_tagger = nltk.UnigramTagger(training,backoff=default_tagger)
        bigram_tagger = nltk.BigramTagger(training, backoff=unigram_tagger)
        tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)
    elif language == 'Spanish':
        training = cess_esp.tagged_sents()
        default_tagger = nltk.DefaultTagger('NN')
        unigram_tagger = nltk.UnigramTagger(training,backoff=default_tagger)
        bigram_tagger = nltk.BigramTagger(training, backoff=unigram_tagger)
        tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)

    return tagger

# set up stemmer
def set_stemmer(language):
    if language == 'English':
        stemmer = SnowballStemmer('english')
    else:
        stemmer = SnowballStemmer('spanish')
    return stemmer

# B.1.a,b,c,d
def extract_features(data, language, tagger, stemmer, s):
    '''
    :param data: list of instances for a given lexelt with the following structure:
        {
			[(instance_id, left_context, head, right_context, sense_id), ...]
        }
    :return: features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
            labels: A dictionary with the following structure
            { instance_id : sense_id }
    '''
    features = {}
    labels = {}

    '''
    In extract_features function (part B), you should return a dictionary where the keys are instance_ids
    and the values are dictionaries such that: the key is a feature, and the value is the corresponding
    value for that feature.

    * You don't have to order the features, just add them as you obtain them and you don't have to have the same size
    of features for all instances; vectorize function will do all that work for you! - Sakhar
    '''

    # implement your code here

    '''
    a) Add collocational features such as: surrounding words w-2 , w-1 , wo w1 , w2 and part-of-speech tags POS-2 , POS-1, POS0 POS1 , POS2.
    b) Remove stop words, remove punctuations, do stemming, etc.
    '''
    # features to add

    derp = True

    part_c = {}
    for item in data:
        feat_dict = {}
        instance_id = item[0]
        labels[instance_id] = item[4] # get the instance - sense combination as before


        '''
        Part C: Finding Frequent Words
        '''
        # get a count of all the senses of each word
        # if item[2] not in part_c:
        #     part_c[item[2]] = {}
        # this_dict = part_c[item[2]]
        # if item[4] in this_dict:
        #     this_dict[item[4]] += 1
        # else:
        #     this_dict[item[4]] = 1


        '''
        Add Nearby Words
        '''
        left_two, right_two = get_colloquial(item[1], item[3], stemmer, language)

        feat_dict['W_N2'] = left_two[0]
        feat_dict['W_N1'] = left_two[1]
        feat_dict['W_0'] = item[2] # Makes Position 0 the head
        feat_dict['W_1'] = right_two[0]
        feat_dict['W_2'] = right_two[1]

        '''
        Part of Speech Tags
        '''
        #add tags -- adds a significant amount of time to process

        # if language != 'German':
        #     tagged = tagger.tag(left_two + list(item[2]) + right_two)
        #
        #     pos_list = []
        #     for taggy in tagged:
        #         pos_list.append(taggy[1])
        #
        #     feat_dict['POS_N2'] = pos_list[0]
        #     # print feat_dict['POS_N2']
        #     # exit(1)
        #     feat_dict['POS_N1'] = pos_list[1]
        #     feat_dict['POS_0'] = pos_list[2]
        #     feat_dict['POS_1'] = pos_list[3]
        #     feat_dict['POS_2'] = pos_list[4]

        '''
        Count Lists
        '''
        # get context and count lists - similar to part A
        #count_list = []
        c_index = 0
        context = get_context(item[1], item[3], language)
        cont_dict = {}
        for word in context:
            if word not in cont_dict:
                cont_dict[word] = 1
            else:
                cont_dict[word] += 1

        for word in s:
            key = 'COUNT_W' + str(c_index)
            c_index += 1
            if word in context:
                #count_list.append(cont_dict[word])
                feat_dict[key] = cont_dict[word]
            else:
                feat_dict[key] = 0
                #count_list.append(0)

        #feat_dict['COUNT'] = count_list
        
        # print count_list
        # print type(count_list)
        # print type(count_list[0])
        # exit(1)

        '''
        Synonyms, Hypernyms, Hyponyms
        '''
        # getting synonyms and other stuff using wn
        # collo = left_two + list(item[2]) + right_two
        # if language == 'English':
        #     ll = 'en'
        # elif language == 'Catalan':
        #     ll = 'cat'
        # elif language == 'Spanish':
        #     ll = 'spa'
        #
        # for word in collo:
        #     if word != '_':
        #         # Synonyms
        #         syn_list = wn.synsets(word, lang=ll)
        #         #amount = max(len(syn_list), 5)
        #         idx = 0
        #         #syn_word = ''
        #         for syn in syn_list:
        #             # if idx == 0:
        #             #     syn_word = syn
        #             feat_dict['SYN_'+str(idx)] = syn.name()
        #             idx +=1

                # Hypernyms?
                #hyper = wn.synset(syn_word)
                # hyp_list = syn_word.hypernyms()
                # hidx = 0
                # for hyp in hyp_list:
                #     feat_dict['HYP_'+str(hidx)] = hyp.name()
                #     hidx += 1

        # when we're all done
        features[instance_id] = feat_dict

    '''
    Continue Part C
    '''
    # for c_item in data:
    #     c_instance = c_item[0]
    #     c_word = c_item[2]
    #     c_list = get_frequent(part_c[c_word])
    #
    #     cidx = 0
    #
    #     for sense in c_list:
    #         key = 'Sense_f' + str(cidx)
    #         cidx += 1
    #         features[c_instance][key] = sense


    return features, labels

def get_frequent(sense_dict):
    result = []
    total = sum(sense_dict.values())
    for key, value in sense_dict.iteritems():
        print log10(float(value/total) / float((total-value)/total))


# similar to get_context
def get_colloquial(before_head, after_head, stemmer, language):
    left_context = nltk.word_tokenize(before_head)
    left_context = remove_punctuation(left_context)
    #left_context = remove_stopwords(left_context, language)

    right_context = nltk.word_tokenize(after_head)
    right_context = remove_punctuation(right_context)
    #right_context = remove_stopwords(right_context, language)

    # if language == 'English':
    #     left_context = stem_words(left_context, stemmer)
    #     right_context = stem_words(right_context, stemmer)

    left_window = left_context[-2:] # 2 words before head
    right_window = right_context[:2] # 2 words after head

    if len(left_window) == 1:
        left_window = ['_', left_window[0]]
    if len(left_window) < 1:
        left_window = ['_', '_']

    if len(right_window) == 1:
        right_window = [right_window[0], '_']
    if len(right_window) < 1:
        right_window = ['_', '_']

    return left_window, right_window

def remove_stopwords(s, language):
    result = []
    if language == 'English':
        for word in s:
            if word not in english_stopwords:
                result.append(word)
    else:
        for word in s:
            if word not in spanish_stopwords:
                result.append(word)

    return result

def stem_words(s, stemmer):
    result = []
    for word in s:
        result.append(stemmer.stem(word))
    return result

# STRAIGHT COPIED FROM PART A
def remove_punctuation(s):
    # Borrowed this from here:
    # http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
    # import string
    # s = "string. With. Punctuation?" # Sample string
    #out = "".join(c for c in s if c not in string.punctuation)

    result = []
    for word in s:
        if word not in string.punctuation:
            result.append(word)

    # I want to change this so it remains unicode
    # So that Spanish and Catalan will work
    return result

def get_context(before_head, after_head, language):
    # set up words before and after the head
    #lc = remove_punctuation(before_head)
    #lc = replace_accented(before_head)
    left_context = nltk.word_tokenize(before_head)
    left_context = remove_punctuation(left_context)
    left_context = remove_stopwords(left_context, language)
    #print left_context

    #rc = remove_punctuation(after_head)
    #rc = replace_accented(after_head)
    right_context = nltk.word_tokenize(after_head)
    right_context = remove_punctuation(right_context)
    right_context = remove_stopwords(right_context, language)
    #print right_context

    if language == 'English':
        wind = english_window
    elif language == 'Catalan':
        wind = catalan_window
    elif language == 'Spanish':
        wind = spanish_window

    left_window = left_context[-wind:] # 10 words before head

    left_len = len(left_window)
    # if left_len < wind:
    #     for i in range (left_len, 0, -1):
    #         left_window.insert(0, '_')

    right_window = right_context[:wind] # 10 words after head

    right_len = len(right_window)
    # if right_len < 10:
    #     for i in range (right_len, 0, -1):
    #         right_window.append('_')
    #print left_window
    #print right_window

    all_context = left_window + right_window
    return all_context

# implemented for you
def vectorize(train_features,test_features):
    '''
    convert set of features to vector representation
    :param train_features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
    :param test_features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
    :return: X_train: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
            X_test: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    '''
    X_train = {}
    X_test = {}

    vec = DictVectorizer()
    vec.fit(train_features.values())
    for instance_id in train_features:
        X_train[instance_id] = vec.transform(train_features[instance_id]).toarray()[0]

    for instance_id in test_features:
        X_test[instance_id] = vec.transform(test_features[instance_id]).toarray()[0]

    return X_train, X_test

#B.1.e
def feature_selection(X_train,X_test,y_train, language):
    '''
    Try to select best features using good feature selection methods (chi-square or PMI)
    or simply you can return train, test if you want to select all features
    :param X_train: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    :param X_test: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    :param y_train: A dictionary with the following structure
            { instance_id : sense_id }
    :return:
    '''

    # implement your code here

    #return X_train_new, X_test_new
    # or return all feature (no feature selection):

    if language != 'English':
        X = [] # our list of word counts for an instance
        Y = [] # the corresponding sense id for each instance

        for key, value in X_train.iteritems():
            if y_train[key] != 'U':
                Y.append(y_train[key])
                X.append(value)

        #print len(X), len(X[0])
        num_feats = 0.9 * len(X[0])
        feature_selector = SelectKBest(chi2, k=num_feats)
        feature_selector.fit(X, Y)

        X_train_final = {}
        X_test_final = {}

        for instance_id in X_train:
            X_train_final[instance_id] = feature_selector.transform(X_train[instance_id])[0]
            #print len(X_train[instance_id])

        for instance_id in X_test:
            X_test_final[instance_id] = feature_selector.transform(X_test[instance_id])[0]

        return X_train_final, X_test_final

    else:
        # given return statement
        return X_train, X_test

# B.2
def classify(X_train, X_test, y_train):
    '''
    Train the best classifier on (X_train, and y_train) then predict X_test labels

    :param X_train: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }

    :param X_test: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }

    :param y_train: A dictionary with the following structure
            { instance_id : sense_id }

    :return: results: a list of tuples (instance_id, label) where labels are predicted by the best classifier
    '''


    results = []


    # implement your code here

    # going to use the SVM classifier since that seemed to be the better option than before
    # might be good to change some options later on if we want
    svm_clf = svm.LinearSVC()

    X = [] # our list of word counts for an instance
    Y = [] # the corresponding sense id for each instance

    for key, value in X_train.iteritems():
        if y_train[key] != 'U':
            Y.append(y_train[key])
            X.append(value)

    svm_clf.fit(X, Y)
    for key, value in X_test.iteritems():
        result_svm = svm_clf.predict(value) # get classification based on the list of counts
        results.append((key, result_svm)) # add the key, classification to the return set

    return results

def build_s(data, language):
    print 'Building S: Part B'
    s = {}
    derp = True
    for key in data:
        # access with data[lexelt]
        # the key in this case is the word at the head of the sentence
        lexelt_list = data[key]
        context_list = [] # make a new list for each key
        for item in lexelt_list:
            all_context = get_context(item[1], item[3], language)
            context_list = list(set(context_list) | set(all_context)) # acts as a union of two sets
            #context_list = context_list + all_context
        s[key] = context_list

    return s

# run part B
def run(train, test, language, answer):
    results = {}

    total = len(train)
    counter = 1

    s = build_s(train, language)
    #s = {}

    # if language == 'English':
    #     tagger = set_tagger(language)
    # else:
    tagger = None
    #tagger = set_tagger(language)
    stemmer = set_stemmer(language)

    for lexelt in train:
        train_features, y_train = extract_features(train[lexelt], language, tagger, stemmer, s[lexelt])
        test_features, _ = extract_features(test[lexelt], language, tagger, stemmer, s[lexelt])

        X_train, X_test = vectorize(train_features,test_features)
        X_train_new, X_test_new = feature_selection(X_train, X_test,y_train, language)
        results[lexelt] = classify(X_train_new, X_test_new,y_train)

        print str(counter) + ' out of ' + str(total) + ' completed'
        counter += 1

    A.print_results(results, answer)