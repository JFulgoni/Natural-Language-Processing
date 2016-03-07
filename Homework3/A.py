from main import replace_accented
from sklearn import svm
from sklearn import neighbors
import string
import nltk
# import sys
# reload(sys)

# sys.setdefaultencoding('utf-8')

# don't change the window size
window_size = 10

# A.1
def build_s(data):
    '''
    Compute the context vector for each lexelt
    :param data: dic with the following structure:
        {
			lexelt: [(instance_id, left_context, head, right_context, sense_id), ...],
			...
        }
    :return: dic s with the following structure:
        {
			lexelt: [w1,w2,w3, ...],
			...
        }

    '''
    s = {}

    # implement your code here

    # 57 sentences in total
    # iterate one key at a time

    derp = True
    for key in data:
        # access with data[lexelt]
        # the key in this case is the word at the head of the sentence
        lexelt_list = data[key]
        context_list = [] # make a new list for each key
        for item in lexelt_list:
            # if derp:
            #     print key
            #     print "before head"
            #     print item[1]
            #     print "head"
            #     print item[2]
            #     print "after head"
            #     print item[3]
            #     derp = False
            #     print '==============='

            # # set up words before and after the head
            # lc = remove_punctuation(item[1])
            # lc = replace_accented(lc)
            # left_context = nltk.word_tokenize(lc)
            # #print left_context
            #
            # rc = remove_punctuation(item[3])
            # rc = replace_accented(rc)
            # right_context = nltk.word_tokenize(rc)
            # #print right_context
            #
            # left_window = left_context[-window_size:] # 10 words before head
            # right_window = right_context[:window_size] # 10 words after head
            # #print left_window
            # #print right_window
            #
            # all_context = left_window + right_window
            all_context = get_context(item[1], item[3])
            context_list = list(set(context_list) | set(all_context)) # acts as a union of two sets
            #context_list = context_list + all_context
        s[key] = context_list

    return s

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

def get_context(before_head, after_head):
     # set up words before and after the head
    #lc = remove_punctuation(before_head)
    #lc = replace_accented(before_head)
    left_context = nltk.word_tokenize(before_head)
    left_context = remove_punctuation(left_context)
    #print left_context

    #rc = remove_punctuation(after_head)
    #rc = replace_accented(after_head)
    right_context = nltk.word_tokenize(after_head)
    right_context = remove_punctuation(right_context)
    #print right_context

    left_window = left_context[-window_size:] # 10 words before head
    right_window = right_context[:window_size] # 10 words after head
    #print left_window
    #print right_window

    all_context = left_window + right_window
    return all_context

# A.1
def vectorize(data, s):
    '''
    :param data: list of instances for a given lexelt with the following structure:
        {
			[(instance_id, left_context, head, right_context, sense_id), ...]
        }
    :param s: list of words (features) for a given lexelt: [w1,w2,w3, ...]
    :return: vectors: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }
            labels: A dictionary with the following structure
            { instance_id : sense_id }

    '''
    vectors = {}
    labels = {}
    # data is not a dictionary, it's a list for a particular lexelt
    # so one step down from last time

    # derp = True
    #
    # # get the word count list for this
    # word_vect = {}
    # # print(len(s))
    # for sentence in s:
    #     if derp:
    #         #print sentence
    #         derp = False;
    #     for word in sentence:
    #         if word not in word_vect:
    #             word_vect[word] = 1
    #         else:
    #             word_vect[word] += 1


    # might be a way to optimize this, but want to keep them separate for now
    for item in data:
        count_list = []
        if item[0] in labels:
            print 'huh?'
        labels[item[0]] = item[4]    # add each instance_id, sense_id combo to the labels vector

        # ask the TA about this!!!
        # so each item in the data gets the same word count for the given lexelt?
        # or do we use the window size, get the words, and then

        # vectors[item[0]] = word_list # fill in the word count list for each instance id in the set

        context = get_context(item[1], item[3])
        cont_dict = {}
        for word in context:
            if word not in cont_dict:
                cont_dict[word] = 1
            else:
                cont_dict[word] += 1
        # for word in context:
        #     try:
        #         # why am I getting errors here!
        #         count_list.append(word_vect[word])
        #     except:
        #         count_list.append(0) # word appears once, only happens in the test cases

        for word in s:
            if word in context:
                count_list.append(cont_dict[word])
            else:
                count_list.append(0)

        vectors[item[0]] = count_list

    return vectors, labels


# A.2
def classify(X_train, X_test, y_train):
    '''
    Train two classifiers on (X_train, and y_train) then predict X_test labels

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

    :return: svm_results: a list of tuples (instance_id, label) where labels are predicted by LinearSVC
             knn_results: a list of tuples (instance_id, label) where labels are predicted by KNeighborsClassifier
    '''

    svm_results = []
    knn_results = []

    svm_clf = svm.LinearSVC()
    knn_clf = neighbors.KNeighborsClassifier()

    # implement your code here

    X = [] # our list of word counts for an instance
    Y = [] # the corresponding sense id for each instance
    derp = True
    u_count = 0
    for key, value in X_train.iteritems():
        # if derp:
        #     print type(value[0])
        #     print type(y_train[key])
        #     print y_train[key]
        #     derp = False

        if y_train[key] != 'U':
            Y.append(y_train[key])
            X.append(value)
        # try:
        #     test = int(y_train[key])
        #     # print test
        #     Y.append(test)
        #     X.append(value)
        #     # if len(value) < 20 or len(value) > 20:
        #     #     print 'hey'
        # except ValueError:
        #     # Just skip it
        #     u_count += 1

    # print(len(X))
    # print(len(Y))
    # print(u_count)
    # should be the same, otherwise you'll get errors

    # http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC
    svm_clf.fit(X, Y)

    # http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    knn_clf.fit(X, Y)

    for key, value in X_test.iteritems():
        result_svm = svm_clf.predict(value) # get classification based on the list of counts
        svm_results.append((key, result_svm)) # add the key, classification to the return set

        result_knn = knn_clf.predict(value)
        knn_results.append((key, result_knn))


    return svm_results, knn_results

# A.3, A.4 output
def print_results(results ,output_file):
    '''

    :param results: A dictionary with key = lexelt and value = a list of tuples (instance_id, label)
    :param output_file: file to write output

    '''

    # implement your code here
    # don't forget to remove the accent of characters using main.replace_accented(input_str)
    # you should sort results on instance_id before printing

    f = open(output_file, 'w')
    for key, value in sorted(results.items()):
        for instance in sorted(value):
            f.write(replace_accented(key) + ' ' + replace_accented(instance[0]) + ' ')
            f.write(instance[1])
            f.write('\n')
    f.close()


# run part A
def run(train, test, language, knn_file, svm_file):
    s = build_s(train)

    print 'Done Building S ... Starting Results'
    svm_results = {}
    knn_results = {}

    for lexelt in s:
        X_train, y_train = vectorize(train[lexelt], s[lexelt])
        X_test, _ = vectorize(test[lexelt], s[lexelt])
        #print y_train
        svm_results[lexelt], knn_results[lexelt] = classify(X_train, X_test, y_train)

    print_results(svm_results, svm_file)
    print_results(knn_results, knn_file)