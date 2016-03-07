import random
from providedcode import dataset
from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from transition import Transition
import time

if __name__ == '__main__':
    t0 = time.time() # start the clock

    # BAD FEATURES AND SWEDISH
    data = dataset.get_swedish_train_corpus().parsed_sents()
    random.seed(1234)
    subdata = random.sample(data, 200) # use this subdata for bad features and swedish

    # NEED DANISH AND ENGLISH
    data_e = dataset.get_english_train_corpus().parsed_sents()
    random.seed(1234)
    subdata_e = random.sample(data_e, 200)

    data_d = dataset.get_danish_train_corpus().parsed_sents()
    random.seed(1234)
    subdata_d = random.sample(data_d, 200)

    try:
        # BAD FEATURES MODEL (SWEDISH DATA)
        print "Starting Bad Features"
        testdata = dataset.get_swedish_test_corpus().parsed_sents()
        tp = TransitionParser.load('badfeatures.model')

        parsed = tp.parse(testdata)

        with open('test.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        ev = DependencyEvaluator(testdata, parsed)
        print "Bad Features Results"
        print "UAS: {} \nLAS: {}".format(*ev.eval())
        t1 = time.time()
        print "Time: "+str(t1 - t0) + '\n'

        # SWEDISH FEATURE MODELS
        print 'Starting Swedish'
        tp_s = TransitionParser(Transition, FeatureExtractor)
        tp_s.train(subdata)
        tp_s.save('swedish.model')

        testdata = dataset.get_swedish_test_corpus().parsed_sents()
        tp_s = TransitionParser.load('swedish.model')

        parsed = tp_s.parse(testdata)

        with open('swedish.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        ev = DependencyEvaluator(testdata, parsed)
        print "Swedish Results"
        print "UAS: {} \nLAS: {}".format(*ev.eval())
        t2 = time.time()
        print "Time: " + str(t2 - t1) + "\n"

        # NEED TO ALSO DO DANISH AND ENGLISH, BUT IT'S PRACTICALLY THE SAME

        # ENGLISH FEATURE MODELS
        print 'Starting English'
        tp_e = TransitionParser(Transition, FeatureExtractor)
        tp_e.train(subdata_e)
        tp_e.save('english.model')

        testdata_e = dataset.get_english_test_corpus().parsed_sents()
        tp_e = TransitionParser.load('english.model')

        parsed = tp_e.parse(testdata_e)

        with open('english.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        ev = DependencyEvaluator(testdata_e, parsed)
        print "English Results"
        print "UAS: {} \nLAS: {}".format(*ev.eval())
        t3 = time.time()
        print "Time: " + str(t3 - t2) + "\n"

        # DANISH FEATURE MODELS
        print 'Starting Danish'
        tp_d = TransitionParser(Transition, FeatureExtractor)
        tp_d.train(subdata_d)
        tp_d.save('danish.model')

        testdata_d = dataset.get_danish_test_corpus().parsed_sents()
        tp_d = TransitionParser.load('danish.model')

        parsed = tp_d.parse(testdata_d)

        with open('danish.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        ev = DependencyEvaluator(testdata_d, parsed)
        print "Danish Results"
        print "UAS: {} \nLAS: {}".format(*ev.eval())
        t4 = time.time()
        print "Time: " + str(t4 - t3) + "\n"

        # parsing arbitrary sentences (english):
        # sentence = DependencyGraph.from_sentence('Hi, this is a test')

        # tp = TransitionParser.load('english.model')
        # parsed = tp.parse([sentence])
        # print parsed[0].to_conll(10).encode('utf-8')
    except NotImplementedError:
        print """
        This file is currently broken! We removed the implementation of Transition
        (in transition.py), which tells the transitionparser how to go from one
        Configuration to another Configuration. This is an essential part of the
        arc-eager dependency parsing algorithm, so you should probably fix that :)

        The algorithm is described in great detail here:
            http://aclweb.org/anthology//C/C12/C12-1059.pdf

        We also haven't actually implemented most of the features for for the
        support vector machine (in featureextractor.py), so as you might expect the
        evaluator is going to give you somewhat bad results...

        Your output should look something like this:

            UAS: 0.23023302131
            LAS: 0.125273849831

            What I'm getting for my implmentation:
            UAS: 0.229038040231
            LAS: 0.125473013344

        Not this:

            Traceback (most recent call last):
                File "test.py", line 41, in <module>
                    ...
                    NotImplementedError: Please implement shift!


        """
